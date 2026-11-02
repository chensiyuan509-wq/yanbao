"""角色库自带的最小绘图工具（不依赖任何项目引擎，只依赖 pycairo）。

颜色钩子：项目引擎可以调用 set_color_hook(fn) 把自己的调色滤镜（去色、色调、亮度）
接进来，fn 接收 (r, g, b) 元组（0..1），返回新的 (r, g, b)。
"""
import math
import random

import cairo

TAU = math.tau

# ---------------------------------------------------------------- 颜色

_HOOK = [None]


def set_color_hook(fn):
    """设置全局颜色钩子（None 表示不处理）。"""
    _HOOK[0] = fn


def hexc(c):
    if isinstance(c, tuple):
        return c
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb(c):
    v = hexc(c)
    return _HOOK[0](v) if _HOOK[0] else v


def mix(c1, c2, t):
    a, b = hexc(c1), hexc(c2)
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def setc(ctx, c, a=1.0):
    r, g, b = rgb(c)
    ctx.set_source_rgba(r, g, b, max(0.0, min(1.0, a)))


def _stops(grad, pairs):
    for p in pairs:
        r, g, b = rgb(p[1])
        grad.add_color_stop_rgba(p[0], r, g, b, max(0.0, min(1.0, p[2] if len(p) > 2 else 1.0)))
    return grad


def lin(x0, y0, x1, y1, pairs):
    return _stops(cairo.LinearGradient(x0, y0, x1, y1), pairs)


def rad(x, y, r0, r1, pairs, fx=None, fy=None):
    return _stops(cairo.RadialGradient(x if fx is None else fx, y if fy is None else fy, r0, x, y, r1), pairs)


# ---------------------------------------------------------------- 数学 / 缓动


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, t):
    return a + (b - a) * t


def prog(t, t0, t1):
    if t1 == t0:
        return 1.0 if t >= t1 else 0.0
    return clamp((t - t0) / (t1 - t0))


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_in(x):
    x = clamp(x)
    return x * x * x


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_io(x):
    x = clamp(x)
    return 4 * x * x * x if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def ease_back(x, s=1.70158):
    x = clamp(x)
    c3 = s + 1
    return 1 + c3 * (x - 1) ** 3 + s * (x - 1) ** 2


def ease_elastic(x):
    x = clamp(x)
    if x in (0.0, 1.0):
        return x
    return 2 ** (-10 * x) * math.sin((x * 10 - 0.75) * (TAU / 3)) + 1


def kf(t, keys, ease=ease_io):
    """关键帧插值：keys = [(时间, 值[, 缓动]), ...]，值可为数字或元组。"""
    if t <= keys[0][0]:
        return keys[0][1]
    for k0, k1 in zip(keys, keys[1:]):
        if t <= k1[0]:
            e = (k1[2] if len(k1) > 2 else ease)(prog(t, k0[0], k1[0]))
            v0, v1 = k0[1], k1[1]
            if isinstance(v0, (tuple, list)):
                return tuple(a + (b - a) * e for a, b in zip(v0, v1))
            return v0 + (v1 - v0) * e
    return keys[-1][1]


def _hash(i, seed):
    x = math.sin(i * 127.1 + seed * 311.7) * 43758.5453123
    return x - math.floor(x)


def noise(x, seed=0.0):
    """平滑一维值噪声，约 [-1, 1]。"""
    i = math.floor(x)
    f = x - i
    a = _hash(i, seed) * 2 - 1
    b = _hash(i + 1, seed) * 2 - 1
    return a + (b - a) * (f * f * (3 - 2 * f))


def rng(seed):
    return random.Random(seed)


# ---------------------------------------------------------------- 图形


def rrect(ctx, x, y, w, h, r):
    r = max(0.0, min(r, abs(w) / 2, abs(h) / 2))
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


def fill(ctx, c, a=1.0):
    setc(ctx, c, a)
    ctx.fill()


def stroke(ctx, c, w, a=1.0, cap=cairo.LINE_CAP_ROUND, join=cairo.LINE_JOIN_ROUND):
    ctx.set_line_width(w)
    ctx.set_line_cap(cap)
    ctx.set_line_join(join)
    setc(ctx, c, a)
    ctx.stroke()


def line(ctx, x0, y0, x1, y1, w, c, a=1.0):
    if a <= 0.002:
        return
    ctx.move_to(x0, y0)
    ctx.line_to(x1, y1)
    stroke(ctx, c, w, a)


def glow(ctx, x, y, r, c, a=1.0):
    if a <= 0.002 or r <= 0.5:
        return
    ctx.set_source(rad(x, y, 0, r, [(0, c, a), (0.3, c, a * 0.42), (0.65, c, a * 0.12), (1, c, 0)]))
    circle(ctx, x, y, r)
    ctx.fill()


def soft_shadow(ctx, x, y, rx, ry, a=0.3, c="#2a1a14"):
    if a <= 0.002 or rx <= 0.5:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(1, max(ry, 0.5) / rx)
    ctx.set_source(rad(0, 0, 0, rx, [(0, c, a), (0.55, c, a * 0.55), (1, c, 0)]))
    circle(ctx, 0, 0, rx)
    ctx.fill()
    ctx.restore()


def star4(ctx, x, y, r, c, a=1.0, rot=0.0):
    if a <= 0.002 or r <= 0.2:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    k = r * 0.2
    ctx.move_to(0, -r)
    ctx.curve_to(k * 0.4, -k, k, -k * 0.4, r, 0)
    ctx.curve_to(k, k * 0.4, k * 0.4, k, 0, r)
    ctx.curve_to(-k * 0.4, k, -k, k * 0.4, -r, 0)
    ctx.curve_to(-k, -k * 0.4, -k * 0.4, -k, 0, -r)
    fill(ctx, c, a)
    ctx.restore()


def star5(ctx, x, y, r, c, a=1.0, rot=0.0, inner=0.47):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + rot + i * math.pi / 5
        rr = r if i % 2 == 0 else r * inner
        pts.append((x + math.cos(ang) * rr, y + math.sin(ang) * rr))
    poly(ctx, pts)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    fill(ctx, c, a)


def heart(ctx, x, y, s, c, a=1.0, hl=True):
    """心形，(x, y) 为中心，s 约为宽度的一半。"""
    if a <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s / 20, s / 20)
    ctx.move_to(0, 14)
    ctx.curve_to(-26, -2, -16, -26, 0, -11)
    ctx.curve_to(16, -26, 26, -2, 0, 14)
    ctx.close_path()
    fill(ctx, c, a)
    if hl:
        ellipse(ctx, -9, -9, 4.5, 3)
        fill(ctx, "#FFFFFF", 0.7 * a)
    ctx.restore()


_FO = cairo.FontOptions()
_FO.set_antialias(cairo.ANTIALIAS_GRAY)
_FO.set_hint_style(cairo.HINT_STYLE_NONE)
_FO.set_hint_metrics(cairo.HINT_METRICS_OFF)
FONT = "Noto Sans CJK SC"


def text(ctx, s, x, y, size, c="#FFFFFF", a=1.0, bold=True, outline=None, outline_w=0.0, align="c"):
    """单行文字，(x, y) 为视觉中心。"""
    if a <= 0.003 or not s:
        return 0.0
    ctx.select_font_face(FONT + (" Black" if bold == "black" else ""), cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold is True else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_options(_FO)
    ctx.set_font_size(size)
    w = ctx.text_extents(s).x_advance
    x0 = x - w / 2 if align == "c" else (x - w if align == "r" else x)
    ctx.new_path()
    ctx.move_to(x0, y + size * 0.355)
    ctx.text_path(s)
    if outline and outline_w > 0:
        ctx.set_line_width(outline_w)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        setc(ctx, outline, a)
        ctx.stroke_preserve()
    setc(ctx, c, a)
    ctx.fill()
    return w


def text_w(ctx, s, size, bold=True):
    ctx.select_font_face(FONT + (" Black" if bold == "black" else ""), cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold is True else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    return ctx.text_extents(s).x_advance


def nz(v):
    """避免 0 缩放（cairo 矩阵不可逆）。"""
    return v if abs(v) > 1e-4 else (1e-4 if v >= 0 else -1e-4)
