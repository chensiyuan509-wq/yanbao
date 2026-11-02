"""界面组件：卡片、标签、聊天气泡、窗口、终端、按钮、进度条等。"""
import math

import cairo

from .core import (TAU, box_shadow, check_mark, circle, clamp, ease_out, fill, font, lerp,
                   lin, rrect, setc, text, text_w)


def card(ctx, x, y, w, h, r=26, color="#FFFFFF", a=1.0, shadow=0.22, border=None,
         border_w=2.5, grad=None, blur=30, dy=14):
    """圆角卡片。grad=(上色, 下色) 时用竖直渐变填充。"""
    if a <= 0.003:
        return
    if shadow:
        box_shadow(ctx, x, y, w, h, r, blur=blur, a=shadow * a, dy=dy)
    rrect(ctx, x, y, w, h, r)
    if grad:
        ctx.set_source(lin(0, y, 0, y + h, [(0, grad[0], a), (1, grad[1], a)]))
    else:
        setc(ctx, color, a)
    ctx.fill()
    if border:
        rrect(ctx, x, y, w, h, r)
        ctx.set_line_width(border_w)
        setc(ctx, border, a)
        ctx.stroke()


def pill(ctx, s, x, y, size, fg="#FFFFFF", bg="#000000", a=1.0, bg_a=0.55,
         pad=(0.62, 0.34), weight="bold", align="c", border=None, dot=None):
    """胶囊标签，返回 (宽, 高)。pad 以字号为单位。dot=颜色 时在左侧画一个小圆点。"""
    if a <= 0.003:
        return 0, 0
    tw = text_w(ctx, s, size, weight)
    px, py = pad[0] * size, pad[1] * size
    dw = size * 0.8 if dot else 0
    w, h = tw + px * 2 + dw, size + py * 2
    x0 = x - w / 2 if align == "c" else (x - w if align == "r" else x)
    rrect(ctx, x0, y - h / 2, w, h, h / 2)
    setc(ctx, bg, a * bg_a)
    ctx.fill()
    if border:
        rrect(ctx, x0, y - h / 2, w, h, h / 2)
        ctx.set_line_width(max(2, size * 0.07))
        setc(ctx, border, a)
        ctx.stroke()
    if dot:
        circle(ctx, x0 + px + size * 0.25, y, size * 0.22)
        fill(ctx, dot, a)
    text(ctx, s, x0 + px + dw, y, size, fg, a, weight, "l")
    return w, h


def bubble(ctx, x, y, w, h, color="#FFFFFF", a=1.0, tail="left", r=None, shadow=0.16,
           tail_x=None):
    """聊天气泡，(x, y) 为左上角。tail: left / right / bottom / none。"""
    if a <= 0.003:
        return
    r = r if r is not None else min(28, h / 2)
    if shadow:
        box_shadow(ctx, x, y, w, h, r, blur=20, a=shadow * a, dy=8)
    rrect(ctx, x, y, w, h, r)
    setc(ctx, color, a)
    ctx.fill()
    if tail == "left":
        ctx.move_to(x + 6, y + h - 26)
        ctx.curve_to(x - 4, y + h - 6, x - 14, y + h + 4, x - 20, y + h + 6)
        ctx.curve_to(x + 2, y + h + 6, x + 18, y + h - 2, x + 26, y + h - 10)
        ctx.close_path()
        ctx.fill()
    elif tail == "right":
        ctx.move_to(x + w - 6, y + h - 26)
        ctx.curve_to(x + w + 4, y + h - 6, x + w + 14, y + h + 4, x + w + 20, y + h + 6)
        ctx.curve_to(x + w - 2, y + h + 6, x + w - 18, y + h - 2, x + w - 26, y + h - 10)
        ctx.close_path()
        ctx.fill()
    elif tail == "bottom":
        tx = tail_x if tail_x is not None else x + w / 2
        ctx.move_to(tx - 18, y + h - 2)
        ctx.line_to(tx, y + h + 22)
        ctx.line_to(tx + 18, y + h - 2)
        ctx.close_path()
        ctx.fill()


def thought(ctx, x, y, w, h, a=1.0, color="#FFFFFF", tail_to=None):
    """思考气泡（云朵 + 小圆点尾巴）。(x, y) 左上角。"""
    if a <= 0.003:
        return
    box_shadow(ctx, x, y, w, h, h / 2.4, blur=22, a=0.14 * a, dy=8)
    rrect(ctx, x, y, w, h, h / 2.4)
    setc(ctx, color, a)
    ctx.fill()
    if tail_to:
        tx, ty = tail_to
        sx, sy = x + w * 0.22, y + h
        for i, rr in enumerate((13, 9, 6)):
            u = (i + 1) / 4
            circle(ctx, lerp(sx, tx, u), lerp(sy, ty, u), rr)
            ctx.fill()


def typing_dots(ctx, x, y, t, color="#9AA0AE", a=1.0, size=9):
    for i in range(3):
        k = 0.5 + 0.5 * math.sin(t * 9 - i * 0.9)
        circle(ctx, x + (i - 1) * size * 2.6, y - k * size * 0.7, size * (0.8 + 0.2 * k))
        fill(ctx, color, a * (0.45 + 0.55 * k))


def window(ctx, x, y, w, h, title="", a=1.0, theme="light", r=22, shadow=0.24,
           title_size=24, accent=None):
    """应用窗口（带标题栏和三个小圆点），返回内容区 (x, y, w, h)。"""
    if a <= 0.003:
        return (x, y + 50, w, h - 50)
    dark = theme == "dark"
    body = "#1D1B26" if dark else "#FFFFFF"
    bar = "#2A2735" if dark else "#F1EEF5"
    card(ctx, x, y, w, h, r, body, a, shadow=shadow)
    ctx.save()
    rrect(ctx, x, y, w, h, r)
    ctx.clip()
    ctx.rectangle(x, y, w, 50)
    setc(ctx, accent or bar, a)
    ctx.fill()
    ctx.restore()
    for i, c in enumerate(("#FF6159", "#FFBD2E", "#28C941")):
        circle(ctx, x + 26 + i * 24, y + 25, 7.5)
        fill(ctx, c, a)
    if title:
        text(ctx, title, x + w / 2, y + 25, title_size, "#D8D4E3" if dark else "#6B6377", a, "medium")
    return (x, y + 50, w, h - 50)


def term_lines(ctx, lines, x, y, t, a=1.0, size=26, lh=40, cps=30, start=0.0, cursor=True,
               max_w=None):
    """终端逐字打印。lines = [(文字, 颜色, 开始时间), ...]；返回已显示到的最后一行 y。"""
    font(ctx, size, "mono")
    last_y = y
    for i, item in enumerate(lines):
        s, col, t0 = item[0], item[1], item[2]
        if t < t0:
            break
        n = len(s) if cps <= 0 else min(len(s), int((t - t0) * cps))
        shown = s[:n]
        yy = y + i * lh
        if max_w is not None:
            while shown and text_w(ctx, shown, size, "mono") > max_w:
                shown = shown[1:]
        text(ctx, shown, x, yy, size, col, a, "mono", "l")
        last_y = yy
        if cursor and n < len(s):
            cw = text_w(ctx, shown, size, "mono")
            ctx.rectangle(x + cw + 3, yy - size * 0.5, size * 0.55, size * 1.0)
            fill(ctx, col, a * 0.85)
    return last_y


def blink_cursor(ctx, x, y, t, size, color, a=1.0):
    if (t * 2.2) % 1 < 0.6:
        ctx.rectangle(x, y - size * 0.5, size * 0.55, size)
        fill(ctx, color, a)


def button(ctx, label, x, y, w, h, color="#4C8DFF", a=1.0, press=0.0, size=26, fg="#FFFFFF"):
    """居中按钮；press 0..1 按下程度。"""
    if a <= 0.003:
        return
    k = 1 - 0.08 * math.sin(clamp(press) * math.pi)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, k)
    box_shadow(ctx, -w / 2, -h / 2, w, h, h / 2, blur=14, a=0.2 * a, dy=6)
    rrect(ctx, -w / 2, -h / 2, w, h, h / 2)
    setc(ctx, color, a)
    ctx.fill()
    text(ctx, label, 0, 0, size, fg, a, "bold")
    ctx.restore()


def progress(ctx, x, y, w, h, p, color="#4C8DFF", track="#E6E1EE", a=1.0):
    rrect(ctx, x, y, w, h, h / 2)
    setc(ctx, track, a)
    ctx.fill()
    if p > 0.001:
        rrect(ctx, x, y, max(h, w * clamp(p)), h, h / 2)
        setc(ctx, color, a)
        ctx.fill()


def checkbox(ctx, x, y, s, p, color="#3CCB7F", a=1.0, box="#C9C3D3"):
    """方形复选框，p 为勾选进度。"""
    rrect(ctx, x - s / 2, y - s / 2, s, s, s * 0.24)
    if p > 0:
        setc(ctx, color, a * ease_out(clamp(p * 3)))
        ctx.fill()
        check_mark(ctx, x, y, s * 0.82, "#FFFFFF", p, a)
    else:
        ctx.set_line_width(3)
        setc(ctx, box, a)
        ctx.stroke()


def chip(ctx, s, x, y, size=28, color="#4C8DFF", a=1.0, fg=None, weight="bold", solid=False):
    """带彩色圆点的名称牌（公司 / 产品名）。"""
    if solid:
        return pill(ctx, s, x, y, size, fg or "#FFFFFF", color, a, 1.0, weight=weight)
    return pill(ctx, s, x, y, size, fg or "#2B2233", "#FFFFFF", a, 0.96, weight=weight,
                dot=color, border=None)


def badge_num(ctx, n, x, y, r, color="#FF5A5F", a=1.0):
    circle(ctx, x, y, r)
    fill(ctx, color, a)
    text(ctx, str(n), x, y, r * 1.15, "#FFFFFF", a, "black")


def stamp(ctx, s, x, y, size, color="#E5484D", a=1.0, rot=-0.18, k=1.0):
    """印章（"拒绝""不"等）。k 为落下时的缩放。"""
    if a <= 0.003:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(k, k)
    tw = text_w(ctx, s, size, "black")
    w, h = tw + size * 0.9, size * 1.55
    rrect(ctx, -w / 2, -h / 2, w, h, size * 0.22)
    ctx.set_line_width(size * 0.12)
    setc(ctx, color, a)
    ctx.stroke()
    rrect(ctx, -w / 2 + size * 0.14, -h / 2 + size * 0.14, w - size * 0.28, h - size * 0.28, size * 0.14)
    ctx.set_line_width(size * 0.04)
    ctx.stroke()
    text(ctx, s, 0, 0, size, color, a, "black")
    ctx.restore()


def table(ctx, x, y, cols, rows, cw, rh, a=1.0, head_color="#E8F5EC", line_color="#D4E5D9",
          fill_p=1.0, size=22, head_text=None, cells=None, accent="#1E8E4F"):
    """简易表格。cells[r][c] 为字符串；fill_p 控制逐格填入。"""
    total = rows * cols
    ctx.rectangle(x, y, cols * cw, rh)
    setc(ctx, head_color, a)
    ctx.fill()
    ctx.set_line_width(2)
    setc(ctx, line_color, a)
    for r in range(rows + 2):
        ctx.move_to(x, y + r * rh)
        ctx.line_to(x + cols * cw, y + r * rh)
    for c in range(cols + 1):
        ctx.move_to(x + c * cw, y)
        ctx.line_to(x + c * cw, y + (rows + 1) * rh)
    ctx.stroke()
    if head_text:
        for c, s in enumerate(head_text):
            text(ctx, s, x + c * cw + cw / 2, y + rh / 2, size, accent, a, "bold")
    if cells:
        k = 0
        for r in range(rows):
            for c in range(cols):
                k += 1
                if k / total <= fill_p + 1e-6:
                    text(ctx, cells[r][c], x + c * cw + cw / 2, y + (r + 1.5) * rh, size, "#3A3442", a, "medium")


def lines_block(ctx, x, y, w, n, lh=22, color="#C9C3D3", a=1.0, p=1.0, th=9, seed=1, last=0.6):
    """抽象的"文字行"（文档预览用），p 控制逐行出现。"""
    import random
    R = random.Random(seed)
    for i in range(n):
        q = clamp(p * n - i)
        if q <= 0:
            break
        lw = w * (last if i == n - 1 else R.uniform(0.78, 1.0)) * ease_out(q)
        rrect(ctx, x, y + i * lh, lw, th, th / 2)
        setc(ctx, color, a)
        ctx.fill()


def glass_panel(ctx, x, y, w, h, r=24, a=1.0, tint="#FFFFFF", alpha=0.10, border_a=0.25):
    """深色背景上的半透明玻璃面板。"""
    rrect(ctx, x, y, w, h, r)
    ctx.set_source(lin(0, y, 0, y + h, [(0, tint, alpha * 1.4 * a), (1, tint, alpha * 0.6 * a)]))
    ctx.fill()
    rrect(ctx, x, y, w, h, r)
    ctx.set_line_width(2)
    setc(ctx, tint, border_a * a)
    ctx.stroke()


def arc_progress(ctx, x, y, r, p, w, color, a=1.0, track=None):
    if track:
        ctx.set_line_width(w)
        setc(ctx, track, a)
        circle(ctx, x, y, r)
        ctx.stroke()
    if p > 0.001:
        ctx.set_line_width(w)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        setc(ctx, color, a)
        ctx.new_sub_path()
        ctx.arc(x, y, r, -math.pi / 2, -math.pi / 2 + TAU * clamp(p))
        ctx.stroke()
