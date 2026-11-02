"""渲染引擎核心：画布常量、缓动函数、颜色、文字、基础图形、镜头。"""
import math
import random
from contextlib import contextmanager

import cairo

W, H, FPS = 1920, 1080, 30
TAU = math.pi * 2

# ---------------------------------------------------------------- 数学 / 缓动


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, t):
    return a + (b - a) * t


def prog(t, t0, t1):
    """t 在 [t0, t1] 区间内的进度，夹在 0..1。"""
    if t1 == t0:
        return 1.0 if t >= t1 else 0.0
    return clamp((t - t0) / (t1 - t0))


def ease_io(x):
    x = clamp(x)
    return 4 * x * x * x if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_in(x):
    x = clamp(x)
    return x * x * x


def ease_back(x, s=1.70158):
    x = clamp(x)
    c3 = s + 1
    return 1 + c3 * (x - 1) ** 3 + s * (x - 1) ** 2


def ease_elastic(x):
    x = clamp(x)
    if x in (0, 1):
        return x
    return 2 ** (-10 * x) * math.sin((x * 10 - 0.75) * (TAU / 3)) + 1


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def env(t, t0, t1, fin=0.4, fout=0.4):
    """淡入淡出包络：t0 开始淡入，t1 结束淡出。"""
    if t < t0 or t > t1:
        return 0.0
    a = smooth(prog(t, t0, t0 + fin)) if fin > 0 else 1.0
    b = smooth(prog(t, t1, t1 - fout)) if fout > 0 else 1.0
    return min(a, b)


def kf(t, keys, ease=ease_io):
    """关键帧插值，keys=[(时间, 值), ...]；值可以是数字或元组。"""
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t1:
            e = ease(prog(t, t0, t1))
            if isinstance(v0, (tuple, list)):
                return tuple(lerp(a, b, e) for a, b in zip(v0, v1))
            return lerp(v0, v1, e)
    return keys[-1][1]


def pick(t, keys):
    """阶梯取值：返回 (当前值, 距切换的时间)。keys=[(时间, 值), ...]"""
    cur, since = keys[0][1], t - keys[0][0]
    for tk, v in keys:
        if t >= tk:
            cur, since = v, t - tk
    return cur, since


def rng(seed):
    return random.Random(seed)


# ---------------------------------------------------------------- 颜色

STYLE = {"desat": 0.0, "tint": None, "tint_amt": 0.0, "bright": 1.0}


def hexc(h):
    if isinstance(h, tuple):
        return h
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def mix(c1, c2, t):
    a, b = hexc(c1), hexc(c2)
    return tuple(lerp(x, y, t) for x, y in zip(a, b))


def styled(c):
    """全局滤镜：去色（冻结效果）、着色（引力红移）、亮度。"""
    r, g, b = hexc(c)
    d = STYLE["desat"]
    if d > 0:
        lum = 0.3 * r + 0.59 * g + 0.11 * b
        cool = (lum * 0.92, lum * 0.97, lum * 1.06)
        r, g, b = lerp(r, cool[0], d), lerp(g, cool[1], d), lerp(b, cool[2], d)
    if STYLE["tint"] is not None and STYLE["tint_amt"] > 0:
        tr, tg, tb = hexc(STYLE["tint"])
        k = STYLE["tint_amt"]
        r, g, b = lerp(r, r * tr, k), lerp(g, g * tg, k), lerp(b, b * tb, k)
    br = STYLE["bright"]
    return (clamp(r * br), clamp(g * br), clamp(b * br))


def setc(ctx, c, a=1.0):
    r, g, b = styled(c)
    ctx.set_source_rgba(r, g, b, a)


def stops(grad, pairs):
    """pairs=[(offset, color, alpha), ...]"""
    for p in pairs:
        off, c = p[0], p[1]
        a = p[2] if len(p) > 2 else 1.0
        r, g, b = styled(c)
        grad.add_color_stop_rgba(off, r, g, b, a)
    return grad


def lin(x0, y0, x1, y1, pairs):
    return stops(cairo.LinearGradient(x0, y0, x1, y1), pairs)


def rad(x, y, r0, r1, pairs, x1=None, y1=None):
    return stops(cairo.RadialGradient(x, y, r0, x if x1 is None else x1,
                                      y if y1 is None else y1, r1), pairs)


# ---------------------------------------------------------------- 图形


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


def glow(ctx, x, y, r, color, a=1.0, core=0.0):
    """柔和光晕。"""
    if a <= 0 or r <= 0:
        return
    g = rad(x, y, 0, r, [(0, color, a), (max(core, 0.001), color, a),
                         (0.35 + core * 0.5, color, a * 0.35), (1, color, 0)])
    ctx.set_source(g)
    circle(ctx, x, y, r)
    ctx.fill()


def soft_shadow(ctx, x, y, rx, ry, a=0.3, color="#3a2418"):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(1, ry / rx)
    g = rad(0, 0, 0, rx, [(0, color, a), (0.6, color, a * 0.5), (1, color, 0)])
    ctx.set_source(g)
    circle(ctx, 0, 0, rx)
    ctx.fill()
    ctx.restore()


def line(ctx, x0, y0, x1, y1, w, color, a=1.0, cap=cairo.LINE_CAP_ROUND):
    ctx.set_line_width(w)
    ctx.set_line_cap(cap)
    setc(ctx, color, a)
    ctx.move_to(x0, y0)
    ctx.line_to(x1, y1)
    ctx.stroke()


def dashed(ctx, x0, y0, x1, y1, w, color, a=1.0, dash=(14, 10), offset=0):
    ctx.save()
    ctx.set_dash(dash, offset)
    line(ctx, x0, y0, x1, y1, w, color, a, cairo.LINE_CAP_BUTT)
    ctx.restore()


def arrow(ctx, x0, y0, x1, y1, w, color, a=1.0, head=None):
    head = head or w * 3.2
    ang = math.atan2(y1 - y0, x1 - x0)
    bx, by = x1 - math.cos(ang) * head * 0.9, y1 - math.sin(ang) * head * 0.9
    line(ctx, x0, y0, bx, by, w, color, a)
    setc(ctx, color, a)
    ctx.move_to(x1, y1)
    ctx.line_to(x1 - math.cos(ang - 0.45) * head, y1 - math.sin(ang - 0.45) * head)
    ctx.line_to(x1 - math.cos(ang + 0.45) * head, y1 - math.sin(ang + 0.45) * head)
    ctx.close_path()
    ctx.fill()


def star4(ctx, x, y, r, color, a=1.0, rot=0.0):
    """四角闪光星。"""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    setc(ctx, color, a)
    k = r * 0.22
    ctx.move_to(0, -r)
    ctx.curve_to(k * 0.4, -k, k, -k * 0.4, r, 0)
    ctx.curve_to(k, k * 0.4, k * 0.4, k, 0, r)
    ctx.curve_to(-k * 0.4, k, -k, k * 0.4, -r, 0)
    ctx.curve_to(-k, -k * 0.4, -k * 0.4, -k, 0, -r)
    ctx.fill()
    ctx.restore()


def bg_vertical(ctx, top, bottom, mid=None, mid_at=0.5):
    if mid:
        g = lin(0, 0, 0, H, [(0, top), (mid_at, mid), (1, bottom)])
    else:
        g = lin(0, 0, 0, H, [(0, top), (1, bottom)])
    ctx.set_source(g)
    ctx.paint()


def vignette(ctx, a=0.45, color="#000000"):
    g = rad(W / 2, H / 2, H * 0.35, H * 1.05, [(0, color, 0), (1, color, a)])
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


def text(ctx, s, x, y, size, color="#ffffff", a=1.0, weight="bold",
         align="c", valign="m", outline=None, outline_w=0, shadow=None,
         spacing=0.0):
    """绘制单行文字。align: l/c/r；valign: m(居中) / b(基线)。返回宽度。"""
    if a <= 0.003 or not s:
        return 0
    font(ctx, size, weight)
    if spacing:
        widths = [ctx.text_extents(ch).x_advance + spacing * size for ch in s]
        tw = sum(widths) - spacing * size
    else:
        tw = ctx.text_extents(s).x_advance
    if align == "c":
        x0 = x - tw / 2
    elif align == "r":
        x0 = x - tw
    else:
        x0 = x
    y0 = y + size * 0.36 if valign == "m" else y

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
        ctx.translate(*shadow[0:2])
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


def text_reveal(ctx, s, x, y, size, color, p, weight="bold", align="c",
                rise=24, stagger=0.6, outline=None, outline_w=0, glow_c=None):
    """逐字浮现。p: 0..1 整体进度。"""
    font(ctx, size, weight)
    adv = [ctx.text_extents(ch).x_advance for ch in s]
    tw = sum(adv)
    x0 = x - tw / 2 if align == "c" else (x - tw if align == "r" else x)
    n = len(s)
    cx = x0
    for i, ch in enumerate(s):
        start = (i / max(n, 1)) * stagger
        q = ease_out(prog(p, start, start + (1 - stagger)))
        if q > 0:
            text(ctx, ch, cx, y + (1 - q) * rise, size, color, q, weight, "l",
                 outline=outline, outline_w=outline_w)
        cx += adv[i]
    return tw


def label_pill(ctx, s, x, y, size, fg="#ffffff", bg="#000000", a=1.0,
               bg_a=0.5, pad=(18, 10), weight="bold", align="c", border=None):
    """带圆角底的标签。"""
    if a <= 0.003:
        return
    tw = text_w(ctx, s, size, weight)
    w, h = tw + pad[0] * 2, size + pad[1] * 2
    x0 = x - w / 2 if align == "c" else (x - w if align == "r" else x)
    rrect(ctx, x0, y - h / 2, w, h, h / 2)
    setc(ctx, bg, a * bg_a)
    ctx.fill_preserve()
    if border:
        ctx.set_line_width(2)
        setc(ctx, border, a * 0.8)
        ctx.stroke()
    ctx.new_path()
    text(ctx, s, x0 + pad[0], y, size, fg, a, weight, "l")


# ---------------------------------------------------------------- 镜头


@contextmanager
def camera(ctx, cx=W / 2, cy=H / 2, zoom=1.0, rot=0.0):
    """镜头：世界坐标 (cx, cy) 位于画面中心，zoom 缩放，rot 旋转。"""
    ctx.save()
    ctx.translate(W / 2, H / 2)
    if rot:
        ctx.rotate(rot)
    ctx.scale(zoom, zoom)
    ctx.translate(-cx, -cy)
    try:
        yield
    finally:
        ctx.restore()


@contextmanager
def group_alpha(ctx, a):
    """整组透明度。"""
    if a >= 0.999:
        yield
        return
    ctx.push_group()
    try:
        yield
    finally:
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(max(a, 0.0))


@contextmanager
def at(ctx, x, y, s=1.0, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    if rot:
        ctx.rotate(rot)
    if s != 1.0:
        ctx.scale(s, s)
    try:
        yield
    finally:
        ctx.restore()


def new_surface():
    return cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
