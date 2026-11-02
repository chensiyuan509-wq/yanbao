"""引擎核心：画布常量、缓动、噪声、颜色、基础图形、文字、镜头。

所有绘制都在 1920×1080 的"设计坐标"里进行，输出时整体缩放到 720p / 480p，
因此画面是矢量的，任何分辨率下都清晰。
"""
import math
import random
from contextlib import contextmanager

import cairo

W, H = 1920, 1080
FPS = 30
TAU = math.tau

# ---------------------------------------------------------------- 数学 / 缓动


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, t):
    return a + (b - a) * t


def lerp2(p, q, t):
    return (lerp(p[0], q[0], t), lerp(p[1], q[1], t))


def prog(t, t0, t1):
    """t 在 [t0, t1] 区间内的进度，夹在 0..1。"""
    if t1 == t0:
        return 1.0 if t >= t1 else 0.0
    return clamp((t - t0) / (t1 - t0))


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def smoother(x):
    x = clamp(x)
    return x * x * x * (x * (x * 6 - 15) + 10)


def ease_in(x):
    x = clamp(x)
    return x * x * x


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_out5(x):
    x = clamp(x)
    return 1 - (1 - x) ** 5


def ease_io(x):
    x = clamp(x)
    return 4 * x * x * x if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def ease_io5(x):
    x = clamp(x)
    return 16 * x ** 5 if x < 0.5 else 1 - (-2 * x + 2) ** 5 / 2


def ease_sine(x):
    x = clamp(x)
    return -(math.cos(math.pi * x) - 1) / 2


def ease_back(x, s=1.70158):
    x = clamp(x)
    c3 = s + 1
    return 1 + c3 * (x - 1) ** 3 + s * (x - 1) ** 2


def ease_elastic(x):
    x = clamp(x)
    if x in (0.0, 1.0):
        return x
    return 2 ** (-10 * x) * math.sin((x * 10 - 0.75) * (TAU / 3)) + 1


def env(t, t0, t1, fin=0.35, fout=0.35):
    """淡入淡出包络：[t0, t0+fin] 淡入，[t1-fout, t1] 淡出。"""
    if t <= t0 or t >= t1:
        return 0.0
    a = smooth((t - t0) / fin) if fin > 0 else 1.0
    b = smooth((t1 - t) / fout) if fout > 0 else 1.0
    return min(a, b)


def kf(t, keys, ease=ease_io):
    """关键帧插值。keys = [(时间, 值[, 缓动]), ...]，值可为数字或元组。

    第三项缓动作用于"到达这一帧"的那一段。
    """
    if t <= keys[0][0]:
        return keys[0][1]
    for k0, k1 in zip(keys, keys[1:]):
        t0, v0 = k0[0], k0[1]
        t1, v1 = k1[0], k1[1]
        if t <= t1:
            e = (k1[2] if len(k1) > 2 else ease)(prog(t, t0, t1))
            if isinstance(v0, (tuple, list)):
                return tuple(lerp(a, b, e) for a, b in zip(v0, v1))
            return lerp(v0, v1, e)
    return keys[-1][1]


def step(t, keys):
    """阶梯取值：返回 (当前值, 自切换以来的时间, 上一个值)。"""
    cur, since, prev = keys[0][1], t - keys[0][0], keys[0][1]
    for i, (tk, v) in enumerate(keys):
        if t >= tk:
            prev = keys[i - 1][1] if i > 0 else v
            cur, since = v, t - tk
    return cur, since, prev


def pop(t, t0, dur=0.45, s=1.9):
    """弹出：0 → 1，带回弹。t<t0 时为 0。"""
    if t <= t0:
        return 0.0
    return ease_back((t - t0) / dur, s)


def pop_io(t, t0, t1, din=0.45, dout=0.3):
    """弹入 + 缩小消失，返回缩放值。"""
    if t <= t0 or t >= t1:
        return 0.0
    a = ease_back((t - t0) / din)
    b = ease_in(clamp((t1 - t) / dout)) if t > t1 - dout else 1.0
    return a * b if t > t1 - dout else a


def wobble(t, t0, amp=1.0, freq=7.0, decay=5.0):
    """t0 之后衰减振荡（用于抖动、回弹）。"""
    if t < t0:
        return 0.0
    u = t - t0
    return amp * math.sin(u * freq * TAU / 2) * math.exp(-u * decay)


def _hash(i, seed):
    x = math.sin(i * 127.1 + seed * 311.7) * 43758.5453123
    return x - math.floor(x)


def noise(x, seed=0.0):
    """平滑一维值噪声，范围约 [-1, 1]。"""
    i = math.floor(x)
    f = x - i
    a = _hash(i, seed) * 2 - 1
    b = _hash(i + 1, seed) * 2 - 1
    return lerp(a, b, f * f * (3 - 2 * f))


def fbm(x, seed=0.0):
    return noise(x, seed) * 0.65 + noise(x * 2.13, seed + 7.3) * 0.35


def rng(seed):
    return random.Random(seed)


# ---------------------------------------------------------------- 颜色

FILTER = {"desat": 0.0, "bright": 1.0, "tint": None, "tint_amt": 0.0}


def reset_filter():
    FILTER.update(desat=0.0, bright=1.0, tint=None, tint_amt=0.0)


def hexc(h):
    if isinstance(h, tuple):
        return h
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def mix(c1, c2, t):
    a, b = hexc(c1), hexc(c2)
    return tuple(lerp(x, y, t) for x, y in zip(a, b))


def styled(c):
    r, g, b = hexc(c)
    d = FILTER["desat"]
    if d > 0:
        lum = 0.3 * r + 0.59 * g + 0.11 * b
        r, g, b = lerp(r, lum * 0.95, d), lerp(g, lum * 0.98, d), lerp(b, lum * 1.06, d)
    if FILTER["tint"] is not None and FILTER["tint_amt"] > 0:
        tr, tg, tb = hexc(FILTER["tint"])
        k = FILTER["tint_amt"]
        r, g, b = lerp(r, r * tr, k), lerp(g, g * tg, k), lerp(b, b * tb, k)
    br = FILTER["bright"]
    return (clamp(r * br), clamp(g * br), clamp(b * br))


def setc(ctx, c, a=1.0):
    r, g, b = styled(c)
    ctx.set_source_rgba(r, g, b, clamp(a))


def _stops(grad, pairs):
    for p in pairs:
        off, c = p[0], p[1]
        a = p[2] if len(p) > 2 else 1.0
        r, g, b = styled(c)
        grad.add_color_stop_rgba(off, r, g, b, clamp(a))
    return grad


def lin(x0, y0, x1, y1, pairs):
    return _stops(cairo.LinearGradient(x0, y0, x1, y1), pairs)


def rad(x, y, r0, r1, pairs, fx=None, fy=None):
    return _stops(cairo.RadialGradient(x if fx is None else fx, y if fy is None else fy,
                                       r0, x, y, r1), pairs)


# 调色板
C = {
    "orange": "#E88E64", "orange_d": "#C7694A", "orange_l": "#F6B089",
    "ink": "#2B2233", "ink2": "#5A4E63", "paper": "#FBF5EC", "cream": "#FFF4E0",
    "yellow": "#FFC857", "gold": "#F5B83D", "teal": "#2EC4B6", "blue": "#4C8DFF",
    "sky": "#7CC6FF", "purple": "#8B6CFF", "pink": "#FF6B9A", "green": "#3CCB7F",
    "red": "#FF5A5F", "white": "#FFFFFF", "night": "#0E1330", "night2": "#1E1B44",
    "grey": "#9AA0AE",
}

# ---------------------------------------------------------------- 基础图形


def rrect(ctx, x, y, w, h, r):
    r = max(0.0, min(r, w / 2, h / 2))
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()


def circle(ctx, x, y, r):
    ctx.new_sub_path()
    ctx.arc(x, y, max(r, 0.01), 0, TAU)


def ellipse(ctx, x, y, rx, ry):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(max(rx, 0.01), max(ry, 0.01))
    ctx.new_sub_path()
    ctx.arc(0, 0, 1, 0, TAU)
    ctx.restore()


def poly(ctx, pts, close=True):
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    if close:
        ctx.close_path()


def fill(ctx, color, a=1.0):
    setc(ctx, color, a)
    ctx.fill()


def line(ctx, x0, y0, x1, y1, w, color, a=1.0, cap=cairo.LINE_CAP_ROUND):
    if a <= 0.002:
        return
    ctx.set_line_width(w)
    ctx.set_line_cap(cap)
    setc(ctx, color, a)
    ctx.move_to(x0, y0)
    ctx.line_to(x1, y1)
    ctx.stroke()


def dashed(ctx, x0, y0, x1, y1, w, color, a=1.0, dash=(14, 10), offset=0.0):
    ctx.save()
    ctx.set_dash(dash, offset)
    line(ctx, x0, y0, x1, y1, w, color, a, cairo.LINE_CAP_ROUND)
    ctx.restore()


def arrow_head(ctx, x, y, ang, size, color, a=1.0):
    setc(ctx, color, a)
    ctx.move_to(x, y)
    ctx.line_to(x - math.cos(ang - 0.48) * size, y - math.sin(ang - 0.48) * size)
    ctx.line_to(x - math.cos(ang) * size * 0.62, y - math.sin(ang) * size * 0.62)
    ctx.line_to(x - math.cos(ang + 0.48) * size, y - math.sin(ang + 0.48) * size)
    ctx.close_path()
    ctx.fill()


def arrow(ctx, x0, y0, x1, y1, w, color, a=1.0, head=None, p=1.0):
    """直箭头，p 为绘制进度。"""
    if a <= 0.002 or p <= 0.001:
        return
    head = head or w * 3.4
    x1, y1 = lerp(x0, x1, p), lerp(y0, y1, p)
    ang = math.atan2(y1 - y0, x1 - x0)
    bx, by = x1 - math.cos(ang) * head * 0.55, y1 - math.sin(ang) * head * 0.55
    line(ctx, x0, y0, bx, by, w, color, a)
    arrow_head(ctx, x1, y1, ang, head, color, a)


def bezier_pts(p0, p1, p2, p3, n=48):
    pts = []
    for i in range(n + 1):
        u = i / n
        v = 1 - u
        pts.append((v * v * v * p0[0] + 3 * v * v * u * p1[0] + 3 * v * u * u * p2[0] + u * u * u * p3[0],
                    v * v * v * p0[1] + 3 * v * v * u * p1[1] + 3 * v * u * u * p2[1] + u * u * u * p3[1]))
    return pts


def polyline_partial(pts, p0, p1=None):
    """按长度截取折线的 [p0, p1] 部分（p 为 0..1）。"""
    if p1 is None:
        p0, p1 = 0.0, p0
    segs = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    total = sum(segs) or 1.0
    s0, s1 = p0 * total, p1 * total
    out, acc = [], 0.0
    for (a, b), L in zip(zip(pts, pts[1:]), segs):
        if acc + L >= s0 and acc <= s1 and L > 0:
            u0 = clamp((s0 - acc) / L)
            u1 = clamp((s1 - acc) / L)
            pa = lerp2(a, b, u0)
            pb = lerp2(a, b, u1)
            if not out:
                out.append(pa)
            out.append(pb)
        acc += L
    return out


def point_on(pts, p):
    seg = polyline_partial(pts, 0.0, clamp(p))
    if len(seg) < 2:
        return pts[0], math.atan2(pts[1][1] - pts[0][1], pts[1][0] - pts[0][0])
    a, b = seg[-2], seg[-1]
    return b, math.atan2(b[1] - a[1], b[0] - a[0])


def stroke_pts(ctx, pts, w, color, a=1.0, dash=None, offset=0.0):
    if len(pts) < 2 or a <= 0.002:
        return
    ctx.save()
    if dash:
        ctx.set_dash(dash, offset)
    ctx.set_line_width(w)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    setc(ctx, color, a)
    poly(ctx, pts, close=False)
    ctx.stroke()
    ctx.restore()


def curve_arrow(ctx, p0, p1, p2, p3, w, color, a=1.0, p=1.0, head=None, start=0.0):
    """三次贝塞尔箭头（可只画出一部分，用于"描线"动画）。"""
    if p <= start + 0.001 or a <= 0.002:
        return
    pts = bezier_pts(p0, p1, p2, p3)
    seg = polyline_partial(pts, start, p)
    head = head or w * 3.4
    if len(seg) >= 2:
        (bx, by), ang = seg[-1], math.atan2(seg[-1][1] - seg[-2][1], seg[-1][0] - seg[-2][0])
        body = seg[:-1] + [(bx - math.cos(ang) * head * 0.5, by - math.sin(ang) * head * 0.5)]
        stroke_pts(ctx, body, w, color, a)
        arrow_head(ctx, bx, by, ang, head, color, a)


def star4(ctx, x, y, r, color, a=1.0, rot=0.0):
    """四角闪光星。"""
    if a <= 0.002 or r <= 0.2:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    setc(ctx, color, a)
    k = r * 0.2
    ctx.move_to(0, -r)
    ctx.curve_to(k * 0.4, -k, k, -k * 0.4, r, 0)
    ctx.curve_to(k, k * 0.4, k * 0.4, k, 0, r)
    ctx.curve_to(-k * 0.4, k, -k, k * 0.4, -r, 0)
    ctx.curve_to(-k, -k * 0.4, -k * 0.4, -k, 0, -r)
    ctx.fill()
    ctx.restore()


def star5(ctx, x, y, r, color, a=1.0, rot=0.0, inner=0.45):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + rot + i * math.pi / 5
        rr = r if i % 2 == 0 else r * inner
        pts.append((x + math.cos(ang) * rr, y + math.sin(ang) * rr))
    poly(ctx, pts)
    fill(ctx, color, a)


def check_mark(ctx, x, y, s, color, p=1.0, a=1.0, w=None):
    """对勾（p 为描线进度）。中心在 (x, y)，大小 s。"""
    if p <= 0.001 or a <= 0.002:
        return
    pts = [(x - 0.42 * s, y + 0.02 * s), (x - 0.12 * s, y + 0.32 * s), (x + 0.45 * s, y - 0.3 * s)]
    seg = polyline_partial(pts, p)
    stroke_pts(ctx, seg, w or s * 0.16, color, a)


def cross_mark(ctx, x, y, s, color, p=1.0, a=1.0, w=None):
    if p <= 0.001 or a <= 0.002:
        return
    w = w or s * 0.16
    p1, p2 = clamp(p * 2), clamp(p * 2 - 1)
    if p1 > 0:
        line(ctx, x - s * 0.36, y - s * 0.36, x - s * 0.36 + s * 0.72 * p1, y - s * 0.36 + s * 0.72 * p1, w, color, a)
    if p2 > 0:
        line(ctx, x + s * 0.36, y - s * 0.36, x + s * 0.36 - s * 0.72 * p2, y - s * 0.36 + s * 0.72 * p2, w, color, a)


def glow(ctx, x, y, r, color, a=1.0, core=0.0):
    """柔和光晕（径向渐变）。"""
    if a <= 0.002 or r <= 0.5:
        return
    g = rad(x, y, 0, r, [(0, color, a), (max(core, 0.001), color, a),
                         (0.3 + core * 0.6, color, a * 0.42), (0.65, color, a * 0.12), (1, color, 0)])
    ctx.set_source(g)
    circle(ctx, x, y, r)
    ctx.fill()


def soft_shadow(ctx, x, y, rx, ry, a=0.3, color="#2a1a14"):
    """椭圆形接触阴影。"""
    if a <= 0.002 or rx <= 0.5:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(1, max(ry, 0.5) / rx)
    g = rad(0, 0, 0, rx, [(0, color, a), (0.55, color, a * 0.55), (1, color, 0)])
    ctx.set_source(g)
    circle(ctx, 0, 0, rx)
    ctx.fill()
    ctx.restore()


def box_shadow(ctx, x, y, w, h, r, blur=26, a=0.22, dy=12, color="#1b1230", steps=7):
    """圆角矩形的柔和投影（多层叠加近似高斯模糊）。"""
    if a <= 0.002:
        return
    setc(ctx, color, a / steps * 1.15)
    for i in range(steps):
        e = blur * (i + 1) / steps
        rrect(ctx, x - e * 0.5, y + dy - e * 0.5, w + e, h + e, r + e * 0.5)
        ctx.fill()


def bg_vertical(ctx, top, bottom, mid=None, mid_at=0.5):
    stops = [(0, top), (mid_at, mid), (1, bottom)] if mid else [(0, top), (1, bottom)]
    ctx.set_source(lin(0, 0, 0, H, stops))
    ctx.paint()


def vignette(ctx, a=0.4, color="#000000", inner=0.42):
    g = rad(W / 2, H / 2, H * inner, H * 1.08, [(0, color, 0), (1, color, a)])
    ctx.set_source(g)
    ctx.paint()


# ---------------------------------------------------------------- 文字

_FO = cairo.FontOptions()
_FO.set_antialias(cairo.ANTIALIAS_GRAY)
_FO.set_hint_style(cairo.HINT_STYLE_NONE)
_FO.set_hint_metrics(cairo.HINT_METRICS_OFF)

FONTS = {
    "regular": ("Noto Sans CJK SC", cairo.FONT_WEIGHT_NORMAL),
    "medium": ("Noto Sans CJK SC Medium", cairo.FONT_WEIGHT_NORMAL),
    "bold": ("Noto Sans CJK SC", cairo.FONT_WEIGHT_BOLD),
    "black": ("Noto Sans CJK SC Black", cairo.FONT_WEIGHT_NORMAL),
    "mono": ("Noto Sans Mono CJK SC", cairo.FONT_WEIGHT_NORMAL),
    "monob": ("Noto Sans Mono CJK SC", cairo.FONT_WEIGHT_BOLD),
    "serif": ("Noto Serif CJK SC", cairo.FONT_WEIGHT_BOLD),
}


def font(ctx, size, weight="bold"):
    fam, w = FONTS[weight]
    ctx.select_font_face(fam, cairo.FONT_SLANT_NORMAL, w)
    ctx.set_font_options(_FO)
    ctx.set_font_size(size)


def text_w(ctx, s, size, weight="bold"):
    font(ctx, size, weight)
    return ctx.text_extents(s).x_advance


def text(ctx, s, x, y, size, color="#ffffff", a=1.0, weight="bold", align="c",
         valign="m", outline=None, outline_w=0, shadow=None, spacing=0.0):
    """单行文字。align: l/c/r；valign: m(视觉居中) / b(基线)。返回宽度。"""
    if a <= 0.003 or not s:
        return 0.0
    font(ctx, size, weight)
    if spacing:
        widths = [ctx.text_extents(ch).x_advance + spacing * size for ch in s]
        tw = sum(widths) - spacing * size
    else:
        tw = ctx.text_extents(s).x_advance
    x0 = x - tw / 2 if align == "c" else (x - tw if align == "r" else x)
    y0 = y + size * 0.355 if valign == "m" else y

    def path():
        ctx.new_path()
        if spacing:
            cx = x0
            for ch, wch in zip(s, widths):
                ctx.move_to(cx, y0)
                ctx.text_path(ch)
                cx += wch
        else:
            ctx.move_to(x0, y0)
            ctx.text_path(s)

    if shadow:
        ctx.save()
        ctx.translate(shadow[0], shadow[1])
        path()
        setc(ctx, shadow[2], a * shadow[3])
        ctx.fill()
        ctx.restore()
    path()
    if outline and outline_w > 0:
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_line_width(outline_w)
        setc(ctx, outline, a)
        ctx.stroke_preserve()
    setc(ctx, color, a)
    ctx.fill()
    return tw


def text_reveal(ctx, s, x, y, size, color, p, weight="bold", align="c", rise=26,
                stagger=0.55, outline=None, outline_w=0, scale_in=False):
    """逐字浮现，p 为整体进度 0..1。"""
    if p <= 0:
        return 0.0
    font(ctx, size, weight)
    adv = [ctx.text_extents(ch).x_advance for ch in s]
    tw = sum(adv)
    x0 = x - tw / 2 if align == "c" else (x - tw if align == "r" else x)
    n = max(len(s), 1)
    cx = x0
    for i, ch in enumerate(s):
        st = (i / n) * stagger
        q = prog(p, st, st + (1 - stagger))
        if q > 0:
            e = ease_out(q)
            if scale_in:
                k = ease_back(q, 2.2)
                ctx.save()
                ctx.translate(cx + adv[i] / 2, y)
                ctx.scale(k, k)
                text(ctx, ch, 0, 0, size, color, min(1, q * 2), weight, "c",
                     outline=outline, outline_w=outline_w)
                ctx.restore()
            else:
                text(ctx, ch, cx, y + (1 - e) * rise, size, color, e, weight, "l",
                     outline=outline, outline_w=outline_w)
        cx += adv[i]
    return tw


def parse_marked(s):
    """'普通{高亮}普通' → [(文字, 是否高亮), ...]"""
    out, buf, hi = [], "", False
    for ch in s:
        if ch == "{" and not hi:
            if buf:
                out.append((buf, False))
            buf, hi = "", True
        elif ch == "}" and hi:
            if buf:
                out.append((buf, True))
            buf, hi = "", False
        else:
            buf += ch
    if buf:
        out.append((buf, hi))
    return out


def rich_w(ctx, segs, size, weight="bold"):
    font(ctx, size, weight)
    return sum(ctx.text_extents(s).x_advance for s, _ in segs)


def rich_text(ctx, segs, x, y, size, color, hi_color, a=1.0, weight="bold", align="c"):
    tw = rich_w(ctx, segs, size, weight)
    cx = x - tw / 2 if align == "c" else (x - tw if align == "r" else x)
    for s, h in segs:
        cx += text(ctx, s, cx, y, size, hi_color if h else color, a, weight, "l")
    return tw


_BREAK_AFTER = "，。：；！？、）」》…—,;:!? "


def wrap_marked(ctx, s, size, weight, max_w):
    """把带 {高亮} 标记的字符串按宽度折成至多两行，优先在标点后断开。"""
    plain = s.replace("{", "").replace("}", "")
    if text_w(ctx, plain, size, weight) <= max_w:
        return [s]
    # 原串中每个可见字符的位置
    vis = [i for i, ch in enumerate(s) if ch not in "{}"]
    n = len(plain)
    best, best_score = None, 1e9
    for k in range(4, n - 3):
        a, b = plain[:k], plain[k:]
        wa, wb = text_w(ctx, a, size, weight), text_w(ctx, b, size, weight)
        if max(wa, wb) > max_w:
            continue
        score = abs(wa - wb)
        if plain[k - 1] in _BREAK_AFTER:
            score -= 400
        elif plain[k - 1].isascii() and plain[k].isascii() and plain[k - 1] != " ":
            score += 900  # 不在英文单词中间断开
        if score < best_score:
            best, best_score = k, score
    if best is None:
        best = n // 2
    cut = vis[best]
    first, second = s[:cut], s[cut:]
    # 补全被拆开的高亮括号
    if first.count("{") > first.count("}"):
        first += "}"
        second = "{" + second
    return [first.rstrip(), second.lstrip()]


# ---------------------------------------------------------------- 组合 / 变换


@contextmanager
def group_alpha(ctx, a):
    """整组透明度（用中间图层，代价较高，按需使用）。"""
    if a >= 0.999:
        yield
        return
    ctx.push_group()
    try:
        yield
    finally:
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(clamp(a))


def _nz(v):
    """避免缩放为 0（cairo 会因矩阵不可逆而报错）。"""
    return v if abs(v) > 1e-4 else (1e-4 if v >= 0 else -1e-4)


@contextmanager
def at(ctx, x, y, s=1.0, rot=0.0, sx=None, sy=None):
    ctx.save()
    ctx.translate(x, y)
    if rot:
        ctx.rotate(rot)
    if sx is not None or sy is not None:
        ctx.scale(_nz(sx if sx is not None else s), _nz(sy if sy is not None else s))
    elif s != 1.0:
        ctx.scale(_nz(s), _nz(s))
    try:
        yield
    finally:
        ctx.restore()


# ---------------------------------------------------------------- 镜头


class Cam:
    """镜头：keys = [(t, (cx, cy, zoom[, rot])[, ease]), ...]。

    (cx, cy) 是画面中心对准的世界坐标；drift 为轻微"手持感"漂移强度（像素）。
    """

    def __init__(self, keys, drift=6.0, seed=1.0, rot_drift=0.004):
        self.keys = [(k[0], tuple(k[1]) + (0.0,) * (4 - len(k[1]))) + tuple(k[2:]) for k in keys]
        self.drift = drift
        self.seed = seed
        self.rot_drift = rot_drift

    def at(self, t):
        cx, cy, z, r = kf(t, self.keys)
        if self.drift:
            cx += fbm(t * 0.23, self.seed) * self.drift
            cy += fbm(t * 0.19, self.seed + 3.1) * self.drift * 0.7
            r += fbm(t * 0.17, self.seed + 9.7) * self.rot_drift
        return cx, cy, z, r


@contextmanager
def view(ctx, cam, depth=1.0):
    """应用镜头。depth<1 表示远景层（视差：移动和缩放都更少）。"""
    cx, cy, z, r = cam
    ctx.save()
    ctx.translate(W / 2, H / 2)
    if r:
        ctx.rotate(r * depth)
    zz = z ** depth
    ctx.scale(zz, zz)
    ctx.translate(-(W / 2 + (cx - W / 2) * depth), -(H / 2 + (cy - H / 2) * depth))
    try:
        yield
    finally:
        ctx.restore()


# ---------------------------------------------------------------- 粒子 / 氛围


def bokeh(ctx, t, n, seed, colors, area=(0, 0, W, H), r=(8, 40), a=(0.05, 0.18),
          speed=(4, 16), rise=1.0):
    """缓慢漂浮的柔光圆点（可无限循环、可任意帧独立计算）。"""
    R = rng(seed)
    x0, y0, w, h = area
    for i in range(n):
        px, py = R.random(), R.random()
        rr = R.uniform(*r)
        aa = R.uniform(*a)
        sp = R.uniform(*speed)
        ph = R.random() * TAU
        col = colors[i % len(colors)]
        y = y0 + ((py * h - t * sp * rise) % (h + 2 * rr)) - rr
        x = x0 + px * w + math.sin(t * 0.3 + ph) * 18
        tw = 0.65 + 0.35 * math.sin(t * 0.8 + ph * 3)
        glow(ctx, x, y, rr, col, aa * tw, core=0.25)


def stars(ctx, t, n, seed, area=(0, 0, W, H), color="#ffffff", a=0.8, size=(1.2, 3.2)):
    R = rng(seed)
    x0, y0, w, h = area
    setc(ctx, color, a)
    for i in range(n):
        x, y = x0 + R.random() * w, y0 + R.random() * h
        s = R.uniform(*size)
        ph = R.random() * TAU
        f = R.uniform(0.6, 2.2)
        k = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(t * f + ph))
        setc(ctx, color, a * k)
        circle(ctx, x, y, s)
        ctx.fill()
        if s > 2.7:
            star4(ctx, x, y, s * 3.2 * k, color, a * 0.5 * k)


def sparkle_burst(ctx, t, t0, x, y, n=8, radius=120, color="#FFE7A3", dur=0.8, seed=3, size=16):
    """t0 时刻在 (x, y) 迸发一圈闪光星。"""
    u = (t - t0) / dur
    if u <= 0 or u >= 1:
        return
    R = rng(seed)
    for i in range(n):
        ang = i / n * TAU + R.uniform(-0.3, 0.3)
        d = radius * ease_out(u) * R.uniform(0.6, 1.1)
        s = size * (1 - u) * R.uniform(0.6, 1.2)
        star4(ctx, x + math.cos(ang) * d, y + math.sin(ang) * d, s, color, 1 - u * u, u * 2)


def ring_burst(ctx, t, t0, x, y, r0=20, r1=140, color="#ffffff", dur=0.6, w=6, a=0.8):
    u = (t - t0) / dur
    if u <= 0 or u >= 1:
        return
    e = ease_out(u)
    ctx.set_line_width(w * (1 - u) + 0.5)
    setc(ctx, color, a * (1 - u))
    circle(ctx, x, y, lerp(r0, r1, e))
    ctx.stroke()


def light_rays(ctx, x, y, n, r, color, a=0.15, rot=0.0, width=0.12):
    """放射光束。"""
    if a <= 0.002:
        return
    for i in range(n):
        ang = rot + i / n * TAU
        ctx.move_to(x, y)
        ctx.arc(x, y, r, ang - width / 2, ang + width / 2)
        ctx.close_path()
    ctx.set_source(rad(x, y, 0, r, [(0, color, a), (1, color, 0)]))
    ctx.fill()


# ---------------------------------------------------------------- 景深 / 角色调色


def soft_layer(ctx, fn, k=4, a=1.0):
    """把 fn(ctx) 画到 1/k 分辨率的图层再放大贴回：便宜的"景深模糊"，用于远景。"""
    if a <= 0.003:
        return
    tgt = ctx.get_group_target()
    pw, ph = tgt.get_width(), tgt.get_height()
    if pw <= 0 or ph <= 0:
        fn(ctx)
        return
    sw, sh = max(1, pw // k), max(1, ph // k)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw, sh)
    c2 = cairo.Context(surf)
    c2.scale(sw / pw, sh / ph)
    c2.transform(ctx.get_matrix())
    fn(c2)
    surf.flush()
    ctx.save()
    ctx.identity_matrix()
    ctx.scale(pw / sw, ph / sh)
    ctx.set_source_surface(surf, 0, 0)
    ctx.get_source().set_filter(cairo.FILTER_BILINEAR)
    ctx.paint_with_alpha(clamp(a))
    ctx.restore()


try:   # 让角色库的颜色也受场景滤镜（去色 / 色调 / 亮度）影响
    import mascot as _mascot
    _mascot.set_color_hook(styled)
except ImportError:  # pragma: no cover
    pass
