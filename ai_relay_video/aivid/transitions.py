"""转场合成：把前后两个场景的画面（像素坐标）按不同方式合成。

种类：fade / dip / zoom / whip / iris / wipe / blob / push / push_up / glitch / blinds / flash
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

    else:
        _paint(ctx, sb if p >= 0.5 else sa, pw, ph)
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
