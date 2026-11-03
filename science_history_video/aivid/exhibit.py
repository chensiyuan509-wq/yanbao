"""展品卡片：上半是真实器物照片（缓慢推近），下面是年份、名称、原理 / 应用两三行。
用于科技段落：信息多，但每张卡留白一致，排成一排、镜头匀速横移，版面不拥挤。"""
import math

from .archive import show
from .core import clamp, ease_out, glow, lin, rad, rrect, setc, smooth, text


def card(ctx, key, x, y, w=500, h=660, year="", title="", lines=(), a=1.0, k=1.0, crop=(0.5, 0.5, 1.0), t=0.0,
         hot=0.0, accent="#D9B26A"):
    """(x, y) 为卡片中心。k：入场程度（上浮 + 淡入）；hot：高亮程度（边框发光）。"""
    if a <= 0.003 or k <= 0.003:
        return
    a = a * smooth(k)
    y = y + (1 - ease_out(k)) * 60
    X, Y = x - w / 2, y - h / 2
    # 投影 + 玻璃面板
    for i in range(5):
        e = (i + 1) * 8
        rrect(ctx, X - e / 2 + 6, Y - e / 2 + 16, w + e, h + e, 18 + e / 2)
        setc(ctx, "#000000", 0.08 * a)
        ctx.fill()
    rrect(ctx, X, Y, w, h, 18)
    ctx.set_source(lin(0, Y, 0, Y + h, [(0, "#1C1A22", 0.86 * a), (1, "#0E0D12", 0.92 * a)]))
    ctx.fill()
    if hot > 0:
        glow(ctx, x, Y + h * 0.3, w * 0.9, accent, 0.12 * hot * a)
    rrect(ctx, X, Y, w, h, 18)
    ctx.set_line_width(2 + 2 * hot)
    setc(ctx, accent, (0.35 + 0.6 * hot) * a)
    ctx.stroke()
    # 照片
    ph = h * 0.5
    pad = 16
    zoom = crop[2] * (1 + 0.06 * (0.5 + 0.5 * math.sin(t * 0.25)))
    ctx.save()
    rrect(ctx, X + pad, Y + pad, w - 2 * pad, ph, 12)
    ctx.clip()
    show(ctx, key, (crop[0], crop[1], zoom), (X + pad, Y + pad, w - 2 * pad, ph), a)
    ctx.set_source(lin(0, Y + pad + ph * 0.6, 0, Y + pad + ph, [(0, "#000000", 0), (1, "#000000", 0.45 * a)]))
    ctx.rectangle(X, Y, w, ph + pad)
    ctx.fill()
    ctx.restore()
    # 文字
    ty = Y + pad + ph + 42
    text(ctx, year, X + 28, ty, 30, accent, a, "serif_sb", "l")
    text(ctx, title, X + 28, ty + 54, 46, "#F6EEDF", a, "serif_k", "l")
    for i, s in enumerate(lines):
        text(ctx, s, X + 28, ty + 110 + i * 42, 29, "#D8CEBC", a, "serif_m", "l")


def panel(ctx, x, y, w, h, a=1.0, accent="#D9B26A"):
    """半透明信息面板（用于在照片 / 地图上放解释文字）。"""
    if a <= 0.003:
        return
    rrect(ctx, x, y, w, h, 16)
    setc(ctx, "#0E0C10", 0.78 * a)
    ctx.fill()
    rrect(ctx, x, y, w, h, 16)
    ctx.set_line_width(2)
    setc(ctx, accent, 0.45 * a)
    ctx.stroke()


def blueprint_bg(ctx, W, H, t=0.0, a=1.0):
    """蓝图背景：深蓝底 + 细网格 + 中心微光。"""
    ctx.set_source(rad(W / 2, H / 2, 0, W * 0.8, [(0, "#123056", a), (1, "#06101F", a)]))
    ctx.paint()
    ctx.set_line_width(1)
    setc(ctx, "#7FC8FF", 0.08 * a)
    for x in range(0, W + 1, 60):
        ctx.move_to(x, 0)
        ctx.line_to(x, H)
    for y in range(0, H + 1, 60):
        ctx.move_to(0, y)
        ctx.line_to(W, y)
    ctx.stroke()
    ctx.set_line_width(1.5)
    setc(ctx, "#7FC8FF", 0.14 * a)
    for x in range(0, W + 1, 300):
        ctx.move_to(x, 0)
        ctx.line_to(x, H)
    for y in range(0, H + 1, 300):
        ctx.move_to(0, y)
        ctx.line_to(W, y)
    ctx.stroke()
