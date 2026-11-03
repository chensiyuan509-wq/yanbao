"""转场合成：把前后两个场景的画面（像素坐标）按不同方式合成。

种类：fade / dip / zoom / whip / iris / wipe / blob / push / push_up / glitch / blinds / flash
电影化：blink（第一视角眨眼）/ flare（强光过曝）/ burn（纸面燃烧）/ pages（书页飞过遮挡）/
        smoke（蒸汽遮挡）/ defocus（虚焦切换）/ match（形状匹配剪辑）
参数里的坐标一律使用设计坐标（1920×1080），这里会自动换算到实际像素。
"""
import math

import cairo
import numpy as np

from .core import TAU, clamp, ease_in, ease_io, ease_io5, ease_out, hexc, lerp, rrect, smooth


def _paint(ctx, surf, pw, ph, alpha=1.0, scale=1.0, dx=0.0, dy=0.0, cx=None, cy=None, rot=0.0):
    if alpha <= 0.002:
        return
    cx = pw / 2 if cx is None else cx
    cy = ph / 2 if cy is None else cy
    ctx.save()
    ctx.translate(cx + dx, cy + dy)
    if rot:
        ctx.rotate(rot)
    ctx.scale(scale, scale)
    ctx.translate(-cx, -cy)
    ctx.set_source_surface(surf, 0, 0)
    ctx.get_source().set_filter(cairo.FILTER_GOOD)
    ctx.paint_with_alpha(clamp(alpha))
    ctx.restore()


def _blur_paint(ctx, surf, pw, ph, dx, dy, spread_x, spread_y, n=10, alpha=1.0, scale=1.0):
    """沿运动方向叠加多份，近似运动模糊（等权平均）。"""
    if abs(spread_x) + abs(spread_y) < 1.0:
        _paint(ctx, surf, pw, ph, alpha, scale, dx, dy)
        return
    ctx.push_group()
    for i in range(n):
        f = i / (n - 1) - 0.5
        _paint(ctx, surf, pw, ph, 1.0 / (i + 1), scale, dx + spread_x * f, dy + spread_y * f)
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(clamp(alpha))


def composite(ctx, kind, p, sa, sb, pw, ph, params):
    k = pw / 1920.0
    e = ease_io(p)
    ctx.save()
    ctx.identity_matrix()
    ctx.set_source_rgb(0, 0, 0)
    ctx.paint()

    if kind == "fade":
        _paint(ctx, sa, pw, ph)
        _paint(ctx, sb, pw, ph, smooth(p))

    elif kind == "dip":
        col = hexc(params.get("color", "#000000"))
        if p < 0.5:
            _paint(ctx, sa, pw, ph)
            ctx.set_source_rgba(*col, smooth(p * 2))
        else:
            _paint(ctx, sb, pw, ph)
            ctx.set_source_rgba(*col, smooth((1 - p) * 2))
        ctx.paint()

    elif kind == "zoom":
        # 推进穿越：A 向某点放大并淡出，B 从略小处推近
        cx, cy = params.get("x", 960) * k, params.get("y", 540) * k
        za = 1 + 2.6 * ease_in(clamp(p / 0.62))
        aa = 1 - smooth(clamp((p - 0.3) / 0.35))
        zb = lerp(1.35, 1.0, ease_out(clamp((p - 0.3) / 0.7)))
        ab = smooth(clamp((p - 0.3) / 0.35))
        _paint(ctx, sa, pw, ph, 1.0, za, cx=cx, cy=cy)
        if aa < 1:
            _paint(ctx, sa, pw, ph, 0.35 * (1 - aa), za * 1.05, cx=cx, cy=cy)
        _paint(ctx, sb, pw, ph, ab, zb)
        if 0.25 < p < 0.6:
            f = math.sin((p - 0.25) / 0.35 * math.pi)
            ctx.set_source_rgba(1, 0.97, 0.92, 0.35 * f)
            ctx.paint()

    elif kind == "whip":
        d = params.get("dir", -1)        # -1：画面向左甩
        ex = ease_io5(p)
        off_a = d * pw * ex                  # 两幅画面首尾相接，中间不留黑缝
        off_b = -d * pw * (1 - ex)
        speed = math.sin(p * math.pi)    # 中段最快
        spread = d * pw * 0.13 * speed
        _blur_paint(ctx, sa, pw, ph, off_a, 0, spread, 0)
        _blur_paint(ctx, sb, pw, ph, off_b, 0, spread, 0)

    elif kind == "push":
        # 横向推屏：A 被推出、B 推入，中段带运动模糊
        d = params.get("dir", -1)
        ex = ease_io5(p)
        sp = math.sin(p * math.pi)
        _blur_paint(ctx, sa, pw, ph, d * pw * ex, 0, d * pw * 0.09 * sp, 0, scale=1 - 0.05 * sp)
        _blur_paint(ctx, sb, pw, ph, -d * pw * (1 - ex), 0, d * pw * 0.09 * sp, 0, scale=1 - 0.05 * sp)

    elif kind == "push_up":
        ex = ease_io5(p)
        _blur_paint(ctx, sa, pw, ph, 0, -ph * ex, 0, -ph * 0.12 * math.sin(p * math.pi), alpha=1.0,
                    scale=1 - 0.06 * ex)
        _blur_paint(ctx, sb, pw, ph, 0, ph * (1 - ex), 0, -ph * 0.12 * math.sin(p * math.pi))

    elif kind == "iris":
        cx, cy = params.get("x", 960) * k, params.get("y", 540) * k
        _paint(ctx, sa, pw, ph, 1.0, 1 + 0.08 * e, cx=cx, cy=cy)
        R = math.hypot(max(cx, pw - cx), max(cy, ph - cy)) * 1.02
        r = ease_io(p) * R
        if r > 0.5:
            ctx.save()
            ctx.arc(cx, cy, r, 0, TAU)
            ctx.clip()
            _paint(ctx, sb, pw, ph, 1.0, 1.06 - 0.06 * e, cx=cx, cy=cy)
            ctx.restore()
            col = hexc(params.get("ring", "#FFE2A8"))
            ctx.set_line_width(max(2, 16 * (1 - p)) * k)
            ctx.set_source_rgba(*col, 0.9 * (1 - p))
            ctx.arc(cx, cy, r, 0, TAU)
            ctx.stroke()

    elif kind == "wipe":
        ang = params.get("angle", 0.35)
        _paint(ctx, sa, pw, ph)
        ux, uy = math.cos(ang), math.sin(ang)
        L = abs(pw * ux) + abs(ph * uy)
        band = 240 * k
        s = -L / 2 - band + (L + 2 * band) * e
        cx, cy = pw / 2, ph / 2
        g = cairo.LinearGradient(cx + ux * (s - band), cy + uy * (s - band), cx + ux * (s + band), cy + uy * (s + band))
        g.add_color_stop_rgba(0, 0, 0, 0, 1)
        g.add_color_stop_rgba(1, 0, 0, 0, 0)
        ctx.set_source_surface(sb, 0, 0)
        ctx.mask(g)
        col = hexc(params.get("edge", "#FFE2A8"))
        g2 = cairo.LinearGradient(cx + ux * (s - 30 * k), cy + uy * (s - 30 * k), cx + ux * (s + 30 * k), cy + uy * (s + 30 * k))
        f = math.sin(math.pi * p)
        g2.add_color_stop_rgba(0, *col, 0)
        g2.add_color_stop_rgba(0.5, *col, 0.55 * f)
        g2.add_color_stop_rgba(1, *col, 0)
        ctx.set_source(g2)
        ctx.paint()

    elif kind == "blob":
        # 橙色圆角方块（Claude 的身体）先盖住画面，再从中心"开窗"露出新画面
        col = hexc(params.get("color", "#E88E64"))
        cx, cy = params.get("x", 960) * k, params.get("y", 540) * k
        diag = math.hypot(pw, ph)
        if p < 0.5:
            _paint(ctx, sa, pw, ph, 1.0, 1 + 0.06 * ease_in(p * 2), cx=cx, cy=cy)
            q = ease_in(p * 2) if p < 0.5 else 1.0
            size = lerp(20 * k, diag * 1.15, q)
            ctx.save()
            ctx.translate(lerp(cx, pw / 2, q), lerp(cy, ph / 2, q))
            ctx.rotate(lerp(0.6, 0.0, q))
            rrect(ctx, -size / 2, -size * 0.33, size, size * 0.66, size * 0.06)
            ctx.set_source_rgb(*col)
            ctx.fill()
            ctx.restore()
        else:
            q = ease_out((p - 0.5) * 2)
            _paint(ctx, sb, pw, ph, 1.0, 1.06 - 0.06 * q)
            hole = lerp(0, diag * 1.2, q)
            ctx.save()
            ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
            ctx.rectangle(0, 0, pw, ph)
            ctx.translate(pw / 2, ph / 2)
            ctx.rotate(lerp(-0.35, 0.0, q))
            rrect(ctx, -hole / 2, -hole * 0.33, hole, hole * 0.66, hole * 0.08)
            ctx.set_source_rgb(*col)
            ctx.fill()
            ctx.restore()

    elif kind == "blinds":
        n = params.get("n", 9)
        _paint(ctx, sa, pw, ph)
        bw = pw / n
        ctx.save()
        for i in range(n):
            q = ease_io(clamp((p - i / n * 0.45) / 0.55))
            if q > 0:
                ctx.rectangle(i * bw + bw * (1 - q) / 2, 0, bw * q + 1, ph)
        ctx.clip()
        _paint(ctx, sb, pw, ph)
        ctx.restore()

    elif kind == "flash":
        if p < 0.5:
            _paint(ctx, sa, pw, ph, 1.0, 1 + 0.05 * p)
            ctx.set_source_rgba(1, 0.98, 0.94, smooth(p * 2))
        else:
            _paint(ctx, sb, pw, ph, 1.0, 1.03 - 0.03 * p)
            ctx.set_source_rgba(1, 0.98, 0.94, smooth((1 - p) * 2))
        ctx.paint()

    elif kind == "glitch":
        src = sa if p < 0.5 else sb
        _paint(ctx, src, pw, ph)
        ctx.restore()
        _glitch(ctx.get_target(), p, params.get("seed", 7))
        ctx.save()

    elif kind == "blink":
        _blink(ctx, p, sa, sb, pw, ph, k, params)

    elif kind == "flare":
        _flare(ctx, p, sa, sb, pw, ph, k, params)

    elif kind == "burn":
        _burn(ctx, p, sa, sb, pw, ph, params)

    elif kind == "pages":
        _paint(ctx, sa if p < 0.5 else sb, pw, ph, 1.0, 1 + 0.04 * math.sin(p * math.pi))
        _pages(ctx, p, pw, ph, k, params)

    elif kind == "smoke":
        _smoke(ctx, p, sa, sb, pw, ph, k, params)

    elif kind == "defocus":
        _defocus(ctx, p, sa, sb, pw, ph, params)

    elif kind == "match":
        _match(ctx, p, sa, sb, pw, ph, k, params)

    elif kind == "zoomblur":
        _zoomblur(ctx, p, sa, sb, pw, ph, k, params)

    elif kind == "lightsweep":
        _lightsweep(ctx, p, sa, sb, pw, ph, k, params)

    elif kind == "luma":
        _luma(ctx, p, sa, sb, pw, ph, params)

    elif kind == "dissolve":
        z = params.get("zoom", 0.04)
        _paint(ctx, sa, pw, ph, 1.0, 1 + z * p)
        _paint(ctx, sb, pw, ph, smooth(p), 1 + z * (p - 1))

    else:
        _paint(ctx, sb if p >= 0.5 else sa, pw, ph)
    ctx.restore()


# ---------------------------------------------------------------- 电影化转场


def _blurred(surf, pw, ph, f):
    """近似模糊：缩小 f 倍再放大（f<=1 返回原图）。"""
    if f <= 1.05:
        return surf
    sw, sh = max(1, int(pw / f)), max(1, int(ph / f))
    small = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw, sh)
    c = cairo.Context(small)
    c.scale(sw / pw, sh / ph)
    c.set_source_surface(surf, 0, 0)
    c.get_source().set_filter(cairo.FILTER_GOOD)
    c.paint()
    small.flush()
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, pw, ph)
    c2 = cairo.Context(out)
    c2.scale(pw / sw, ph / sh)
    c2.set_source_surface(small, 0, 0)
    c2.get_source().set_filter(cairo.FILTER_BILINEAR)
    c2.paint()
    out.flush()
    return out


def _blink(ctx, p, sa, sb, pw, ph, k, params):
    """第一视角眨眼：眼睑合上 → 黑一下 → 睁开（新画面先虚后实）。"""
    from .film import eyelids
    hold = params.get("hold", 0.12)
    a_end = 0.5 - hold / 2
    b_start = 0.5 + hold / 2
    if p < a_end:
        q = p / a_end
        _paint(ctx, _blurred(sa, pw, ph, 1 + 5 * ease_in(q)), pw, ph, 1.0, 1 + 0.03 * q)
        ok = 1 - ease_in(q)
    elif p < b_start:
        ok = 0.0
    else:
        q = (p - b_start) / (1 - b_start)
        _paint(ctx, _blurred(sb, pw, ph, 1 + 7 * (1 - ease_out(q)) ** 2), pw, ph, 1.0, 1.04 - 0.04 * q)
        ok = ease_out(q)
        # 第二次轻眨（还没完全清醒）
        if params.get("double", True) and 0.35 < q < 0.6:
            ok *= 1 - 0.55 * math.sin((q - 0.35) / 0.25 * math.pi)
    ctx.save()
    ctx.scale(k, k)
    eyelids(ctx, ok)
    ctx.restore()


def _flare(ctx, p, sa, sb, pw, ph, k, params):
    """强光过曝：画面越来越亮（暖色光晕 + 横向镜头光斑），在最亮处换到新画面。"""
    cx, cy = params.get("x", 960) * k, params.get("y", 540) * k
    col = hexc(params.get("color", "#FFD9A0"))
    src = sa if p < 0.5 else sb
    q = 1 - abs(p - 0.5) * 2               # 0 → 1 → 0
    _paint(ctx, src, pw, ph, 1.0, 1 + 0.05 * (p if p < 0.5 else 1 - p), cx=cx, cy=cy)
    e = ease_in(q)
    ctx.save()
    ctx.set_operator(cairo.OPERATOR_ADD)
    g = cairo.RadialGradient(cx, cy, 0, cx, cy, max(pw, ph) * (0.3 + 0.9 * e))
    g.add_color_stop_rgba(0, *col, 0.95 * e)
    g.add_color_stop_rgba(0.5, *col, 0.45 * e)
    g.add_color_stop_rgba(1, *col, 0.0)
    ctx.set_source(g)
    ctx.paint()
    # 横向光斑
    g2 = cairo.LinearGradient(0, cy - 30 * k, 0, cy + 30 * k)
    g2.add_color_stop_rgba(0, 1, 0.8, 0.5, 0)
    g2.add_color_stop_rgba(0.5, 1, 0.85, 0.6, 0.6 * e)
    g2.add_color_stop_rgba(1, 1, 0.8, 0.5, 0)
    ctx.set_source(g2)
    ctx.rectangle(0, cy - 30 * k, pw, 60 * k)
    ctx.fill()
    ctx.restore()
    ctx.set_source_rgba(1, 0.97, 0.9, smooth(clamp((q - 0.55) / 0.45)))
    ctx.paint()


_NOISE = {}


def _noise_field(pw, ph, seed):
    key = (pw, ph, seed)
    if key not in _NOISE:
        from .film import _value_noise_img
        n = _value_noise_img(pw, ph, seed, ((3, 0.45), (7, 0.3), (18, 0.17), (50, 0.08)))
        n = (n - n.min()) / (n.max() - n.min() + 1e-6)
        _NOISE[key] = n.astype(np.float32)
    return _NOISE[key]


def _a8(arr):
    h, w = arr.shape
    stride = cairo.ImageSurface.format_stride_for_width(cairo.FORMAT_A8, w)
    buf = np.zeros((h, stride), dtype=np.uint8)
    buf[:, :w] = arr
    return cairo.ImageSurface.create_for_data(bytearray(buf.tobytes()), cairo.FORMAT_A8, w, h, stride)


def _burn(ctx, p, sa, sb, pw, ph, params):
    """纸面燃烧：噪声阈值决定烧穿的区域，边缘发出橙红的火光、外圈焦黑。"""
    n = _noise_field(pw, ph, params.get("seed", 11))
    th = -0.08 + 1.2 * ease_io(p)
    soft = 0.018
    reveal = np.clip((th - n) / soft, 0, 1)
    char = np.clip(1 - np.abs(n - th - 0.035) / 0.05, 0, 1)
    edge = np.clip(1 - np.abs(n - th) / 0.022, 0, 1)
    _paint(ctx, sa, pw, ph)
    # 焦黑
    ctx.set_source_rgba(0.08, 0.04, 0.02, 0.9)
    ctx.mask_surface(_a8((char * 255).astype(np.uint8)), 0, 0)
    # 烧穿处露出新画面
    ctx.set_source_surface(sb, 0, 0)
    ctx.mask_surface(_a8((reveal * 255).astype(np.uint8)), 0, 0)
    # 火边
    ctx.save()
    ctx.set_operator(cairo.OPERATOR_ADD)
    ctx.set_source_rgba(1.0, 0.55, 0.15, 1.0)
    ctx.mask_surface(_a8((edge * 230).astype(np.uint8)), 0, 0)
    ctx.restore()


def _pages(ctx, p, pw, ph, k, params):
    """一阵书页从右向左飞过镜头，最密的时候切换画面。"""
    import random
    R = random.Random(params.get("seed", 5))
    n = params.get("n", 34)
    d = params.get("dir", -1)
    for i in range(n):
        delay = R.uniform(0, 0.42)
        q = (p - delay) / 0.58
        if q <= 0 or q >= 1:
            continue
        depth = R.uniform(0.6, 1.8)
        w, h = 260 * k * depth, 340 * k * depth
        x0 = pw + w if d < 0 else -w
        x1 = -w if d < 0 else pw + w
        x = lerp(x0, x1, q)
        y = R.uniform(-0.1, 1.1) * ph + math.sin(q * 5 + i) * 60 * k
        rot = R.uniform(-1, 1) + q * R.uniform(-3, 3)
        sq = abs(math.cos(q * R.uniform(4, 9) + i))      # 翻动时的透视压缩
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(rot)
        ctx.scale(max(0.15, sq), 1)
        shade = 0.8 + 0.2 * sq
        ctx.rectangle(-w / 2, -h / 2, w, h)
        ctx.set_source_rgba(0.93 * shade, 0.88 * shade, 0.76 * shade, 1)
        ctx.fill()
        ctx.set_source_rgba(0.25, 0.18, 0.1, 0.35)
        for j in range(9):
            ctx.rectangle(-w / 2 + w * 0.1, -h / 2 + h * (0.12 + j * 0.085), w * (0.8 if j % 4 else 0.55), h * 0.022)
        ctx.fill()
        ctx.restore()


def _smoke(ctx, p, sa, sb, pw, ph, k, params):
    """一大团蒸汽 / 烟从画面一侧涌过，遮住切换点。"""
    import random
    _paint(ctx, sa if p < 0.5 else sb, pw, ph, 1.0, 1 + 0.03 * math.sin(p * math.pi))
    col = hexc(params.get("color", "#D9D4CC"))
    R = random.Random(params.get("seed", 3))
    cover = math.sin(p * math.pi)
    for i in range(46):
        sx = R.uniform(-0.3, 1.3)
        sy = R.uniform(-0.1, 1.1)
        r = R.uniform(0.18, 0.42) * pw
        lag = R.uniform(-0.25, 0.25)
        q = clamp(p + lag * 0.5)
        x = (sx + (0.6 - q * 1.6)) * pw
        y = sy * ph - q * 80 * k
        a = clamp(cover * 1.6 - abs(lag)) * 0.55
        if a <= 0.01:
            continue
        g = cairo.RadialGradient(x, y, 0, x, y, r)
        g.add_color_stop_rgba(0, *col, a)
        g.add_color_stop_rgba(0.6, *col, a * 0.5)
        g.add_color_stop_rgba(1, *col, 0)
        ctx.set_source(g)
        ctx.arc(x, y, r, 0, TAU)
        ctx.fill()
    ctx.set_source_rgba(*col, 0.6 * smooth(clamp((cover - 0.6) / 0.4)))
    ctx.paint()


def _defocus(ctx, p, sa, sb, pw, ph, params):
    """虚焦切换：A 慢慢失焦，B 从失焦里清晰起来。"""
    m = params.get("max", 14)
    if p < 0.5:
        f = 1 + m * ease_in(p * 2)
        _paint(ctx, _blurred(sa, pw, ph, f), pw, ph, 1.0, 1 + 0.03 * p)
        if p > 0.35:
            _paint(ctx, _blurred(sb, pw, ph, 1 + m), pw, ph, smooth((p - 0.35) / 0.15) * 0.5)
    else:
        f = 1 + m * (1 - ease_out((p - 0.5) * 2))
        if p < 0.65:
            _paint(ctx, _blurred(sa, pw, ph, 1 + m), pw, ph, 1.0)
        _paint(ctx, _blurred(sb, pw, ph, f), pw, ph, smooth((p - 0.5) / 0.15) if p < 0.65 else 1.0,
               1.03 - 0.03 * p)


def _match(ctx, p, sa, sb, pw, ph, k, params):
    """形状匹配剪辑：A 中的某个圆形物体（中心 a、半径 ra）与 B 中的（中心 b、半径 rb）在屏幕上重合着交叉溶解。"""
    ax, ay = params["a"][0] * k, params["a"][1] * k
    bx, by = params["b"][0] * k, params["b"][1] * k
    ra, rb = params.get("ra", 100), params.get("rb", 100)
    e = ease_io(p)
    sx, sy = lerp(ax, bx, e), lerp(ay, by, e)
    sA = lerp(1.0, rb / ra, e) * (1 + 0.06 * math.sin(p * math.pi))
    sB = sA * ra / rb
    fa = smooth(clamp((p - 0.3) / 0.4))

    def draw(surf, anchor, s, alpha):
        ctx.save()
        ctx.translate(sx, sy)
        ctx.scale(s, s)
        ctx.translate(-anchor[0], -anchor[1])
        ctx.set_source_surface(surf, 0, 0)
        ctx.get_source().set_filter(cairo.FILTER_GOOD)
        ctx.paint_with_alpha(alpha)
        ctx.restore()

    draw(sa, (ax, ay), sA, 1.0)
    draw(sb, (bx, by), sB, fa)


def _zoomblur(ctx, p, sa, sb, pw, ph, k, params):
    """变焦模糊：镜头猛地推进 A（径向拖影），在最快处换成 B，B 从拖影里稳住。"""
    cx, cy = params.get("x", 960) * k, params.get("y", 540) * k
    n = 8
    if p < 0.5:
        q = ease_in(p * 2)
        base = 1 + 0.9 * q
        for i in range(n):
            f = i / (n - 1)
            _paint(ctx, sa, pw, ph, 1.0 if i == 0 else 0.22 * q, base * (1 + 0.35 * q * f), cx=cx, cy=cy)
        ctx.set_source_rgba(1, 0.97, 0.92, 0.25 * q)
        ctx.paint()
    else:
        q = 1 - ease_out((p - 0.5) * 2)
        base = 1 + 0.5 * q
        for i in range(n):
            f = i / (n - 1)
            _paint(ctx, sb, pw, ph, 1.0 if i == 0 else 0.22 * q, base * (1 + 0.35 * q * f), cx=cx, cy=cy)
        ctx.set_source_rgba(1, 0.97, 0.92, 0.25 * q)
        ctx.paint()


def _lightsweep(ctx, p, sa, sb, pw, ph, k, params):
    """光带扫过：一道带辉光的斜向光带掠过画面，光带后面是新画面。"""
    ang = params.get("angle", -0.5)
    col = hexc(params.get("color", "#FFE6B8"))
    e = ease_io(p)
    ux, uy = math.cos(ang), math.sin(ang)
    L = abs(pw * ux) + abs(ph * uy)
    s = -L / 2 - 200 * k + (L + 400 * k) * e
    cx, cy = pw / 2, ph / 2
    _paint(ctx, sa, pw, ph, 1.0, 1 + 0.03 * p)
    soft = 90 * k
    g = cairo.LinearGradient(cx + ux * (s - soft), cy + uy * (s - soft), cx + ux * (s + soft), cy + uy * (s + soft))
    g.add_color_stop_rgba(0, 0, 0, 0, 1)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(1.03 - 0.03 * p, 1.03 - 0.03 * p)
    ctx.translate(-cx, -cy)
    ctx.set_source_surface(sb, 0, 0)
    ctx.mask(g)
    ctx.restore()
    f = math.sin(math.pi * p)
    ctx.save()
    ctx.set_operator(cairo.OPERATOR_ADD)
    for w, a in ((260, 0.25), (90, 0.45), (22, 0.9)):
        g2 = cairo.LinearGradient(cx + ux * (s - w * k), cy + uy * (s - w * k), cx + ux * (s + w * k), cy + uy * (s + w * k))
        g2.add_color_stop_rgba(0, *col, 0)
        g2.add_color_stop_rgba(0.5, *col, a * f)
        g2.add_color_stop_rgba(1, *col, 0)
        ctx.set_source(g2)
        ctx.paint()
    ctx.restore()


def _lum(surf, pw, ph, step=2):
    surf.flush()
    stride = surf.get_stride()
    buf = np.ndarray((ph, stride // 4, 4), dtype=np.uint8, buffer=surf.get_data())[:ph, :pw]
    sub = buf[::step, ::step, :3].astype(np.float32)
    return (0.11 * sub[..., 0] + 0.59 * sub[..., 1] + 0.3 * sub[..., 2]) / 255.0


def _luma(ctx, p, sa, sb, pw, ph, params):
    """亮度溶解：新画面从最亮的地方先显现，像胶片冲洗时影像慢慢浮出来。"""
    step = 2
    lum = _lum(sb, pw, ph, step)
    th = 1.15 - 1.3 * ease_io(p)
    m = np.clip((lum - th) / 0.18, 0, 1)
    mh, mw = m.shape
    mask = _a8((m * 255).astype(np.uint8))
    _paint(ctx, sa, pw, ph, 1.0, 1 + 0.03 * p)
    ctx.save()
    ctx.set_source_surface(sb, 0, 0)
    ms = cairo.SurfacePattern(mask)
    mt = cairo.Matrix()
    mt.scale(1 / step, 1 / step)
    ms.set_matrix(mt)
    ms.set_filter(cairo.FILTER_BILINEAR)
    ctx.mask(ms)
    ctx.restore()


def _glitch(surf, p, seed):
    """数字故障：横向错位条带 + RGB 通道分离（直接改像素）。"""
    surf.flush()
    w, h = surf.get_width(), surf.get_height()
    stride = surf.get_stride()
    buf = np.ndarray((h, stride // 4, 4), dtype=np.uint8, buffer=surf.get_data())
    img = buf[:, :w, :]
    amt = math.sin(p * math.pi) ** 1.5
    if amt < 0.02:
        return
    rnd = np.random.default_rng(seed + int(p * 40))
    n = 14
    for _ in range(n):
        y0 = int(rnd.integers(0, h - 4))
        hh = int(rnd.integers(4, max(6, h // 12)))
        sh = int(rnd.normal(0, w * 0.06 * amt))
        if sh:
            img[y0:y0 + hh] = np.roll(img[y0:y0 + hh], sh, axis=1)
    split = int(w * 0.012 * amt) + 1
    img[:, :, 2] = np.roll(img[:, :, 2], split, axis=1)    # R
    img[:, :, 0] = np.roll(img[:, :, 0], -split, axis=1)   # B
    surf.mark_dirty()
