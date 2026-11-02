"""场景共用的小部件：背景、浮岛、通知卡片、标签等。"""
import math

from ..core import (TAU, W, H, box_shadow, circle, clamp, ease_back, ease_out, ellipse, fill,
                    glow, lerp, lin, poly, rad, rrect, setc, smooth, text, text_w)
from ..ui import card


def night_sky(ctx, t, top="#0A0F25", mid="#191543", bottom="#2E1E4A", warm=0.0):
    ctx.set_source(lin(0, 0, 0, H, [(0, top), (0.55, mid), (1, bottom)]))
    ctx.paint()
    if warm > 0:
        ctx.set_source(rad(W / 2, H * 1.05, 0, H * 1.1,
                           [(0, "#FF9F68", 0.55 * warm), (0.45, "#FF6B9A", 0.18 * warm), (1, "#FF6B9A", 0)]))
        ctx.paint()


def floating_island(ctx, x, y, rx=300, t=0.0, top="#4A4170", side="#2A2348", glow_c="#FFB27A", seed=0):
    """漂浮小岛（顶面为椭圆）。(x, y) 为顶面中心。"""
    ry = rx * 0.16
    bob = math.sin(t * 1.1 + seed) * 3
    y += bob
    # 下方岩体
    ctx.move_to(x - rx, y)
    ctx.curve_to(x - rx * 0.9, y + rx * 0.35, x - rx * 0.35, y + rx * 0.62, x, y + rx * 0.82)
    ctx.curve_to(x + rx * 0.35, y + rx * 0.62, x + rx * 0.9, y + rx * 0.35, x + rx, y)
    ctx.close_path()
    ctx.set_source(lin(0, y, 0, y + rx * 0.8, [(0, side), (1, "#140F28")]))
    ctx.fill()
    # 岩体上的亮纹
    for i in range(3):
        k = (i + 1) / 4
        ctx.move_to(x - rx * (0.8 - k * 0.5), y + rx * 0.08 * (i + 1))
        ctx.line_to(x - rx * (0.5 - k * 0.3), y + rx * (0.18 + 0.12 * i))
        ctx.set_line_width(3)
        setc(ctx, "#8C7FC8", 0.25)
        ctx.stroke()
    # 顶面
    ellipse(ctx, x, y, rx, ry)
    ctx.set_source(lin(0, y - ry, 0, y + ry, [(0, "#6B5FA0"), (1, top)]))
    ctx.fill()
    ellipse(ctx, x, y - 2, rx * 0.98, ry * 0.9)
    ctx.set_line_width(3)
    setc(ctx, glow_c, 0.35)
    ctx.stroke()
    # 边缘小晶体
    for i, (dx, s) in enumerate(((-0.78, 1.0), (0.7, 0.8), (0.86, 0.6))):
        cx, cy = x + rx * dx, y - 4
        k = 0.6 + 0.4 * math.sin(t * 2 + i * 2)
        poly(ctx, [(cx, cy - 34 * s), (cx + 10 * s, cy - 8 * s), (cx, cy + 4), (cx - 10 * s, cy - 8 * s)])
        fill(ctx, "#9FE7FF", 0.85)
        glow(ctx, cx, cy - 14 * s, 50 * s, "#7FDBFF", 0.35 * k)
    return y


def notif(ctx, x, y, icon_fn, app, msg, a=1.0, k=1.0, t=0.0, w=470):
    """手机推送样式的通知卡片，(x, y) 为中心，k 为缩放。"""
    if a <= 0.003 or k <= 0.01:
        return
    h = 96
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, k)
    card(ctx, -w / 2, -h / 2, w, h, 26, "#FFFFFF", 0.96 * a, shadow=0.3)
    icon_fn(ctx, -w / 2 + 52, 0, 60, a, t)
    text(ctx, app, -w / 2 + 96, -18, 22, "#8A8296", a, "bold", "l")
    text(ctx, "刚刚", w / 2 - 22, -18, 20, "#B0A9BA", a, "medium", "r")
    text(ctx, msg, -w / 2 + 96, 16, 27, "#2B2233", a, "bold", "l")
    ctx.restore()


def light_bg(ctx, top, bottom, dots=None, t=0.0, dot_a=0.08, spacing=60, drift=(0, 0)):
    ctx.set_source(lin(0, 0, 0, H, [(0, top), (1, bottom)]))
    ctx.paint()
    if dots:
        setc(ctx, dots, dot_a)
        ox, oy = drift[0] % spacing, drift[1] % spacing
        for i in range(-1, W // spacing + 2):
            for j in range(-1, H // spacing + 2):
                circle(ctx, i * spacing + ox, j * spacing + oy, 2.6)
        ctx.fill()


def label(ctx, s, x, y, size=30, color="#2B2233", a=1.0, weight="bold", align="c", bg=None,
          bg_a=0.9, pad=0.5):
    if bg:
        tw = text_w(ctx, s, size, weight)
        w, h = tw + size * pad * 2, size * 1.7
        x0 = x - w / 2 if align == "c" else (x - w if align == "r" else x)
        rrect(ctx, x0, y - h / 2, w, h, h / 2)
        setc(ctx, bg, bg_a * a)
        ctx.fill()
        text(ctx, s, x0 + w / 2, y, size, color, a, weight, "c")
        return w
    return text(ctx, s, x, y, size, color, a, weight, align)


def danmaku(ctx, t, items, y0=150, rows=5, row_h=62, speed=260, a=1.0, t0=0.0, size=30,
            colors=("#FFFFFF",)):
    """从右向左飘过的弹幕。items 为 [(出现时间, 文字, 行号), ...]。"""
    for (ts, s, row) in items:
        u = t - ts
        if u < 0:
            continue
        w = text_w(ctx, s, size, "bold")
        x = W + 40 - u * speed
        if x < -w - 40:
            continue
        col = colors[hash(s) % len(colors)]
        text(ctx, s, x, y0 + (row % rows) * row_h, size, col, 0.85 * a, "bold", "l",
             outline="#1A1430", outline_w=4)


def wave_lines(ctx, t, y, color, a=0.3, amp=8, n=3, gap=26, speed=1.0, length=W):
    for i in range(n):
        ctx.move_to(0, y + i * gap)
        for x in range(0, int(length) + 40, 40):
            ctx.line_to(x, y + i * gap + math.sin(x * 0.012 + t * speed * (1 + i * 0.3) + i) * amp)
        ctx.set_line_width(3)
        setc(ctx, color, a * (1 - i / (n + 1)))
        ctx.stroke()
