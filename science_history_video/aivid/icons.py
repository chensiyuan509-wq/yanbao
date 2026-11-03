"""矢量图标：全部用代码绘制的通用风格图标（不使用任何商标图片）。

约定：ic_xxx(ctx, x, y, s=100, a=1.0, t=0.0)，以 (x, y) 为中心、边长约 s。
"""
import math

import cairo

from .core import (TAU, box_shadow, check_mark, circle, clamp, ellipse, fill, glow, lin, poly,
                   rad, rrect, setc, star4, text)


def _tile(ctx, x, y, s, top, bottom, a=1.0, r=0.24, shadow=0.22):
    h = s
    if shadow:
        box_shadow(ctx, x - h / 2, y - h / 2, h, h, h * r, blur=h * 0.22, a=shadow * a, dy=h * 0.07)
    rrect(ctx, x - h / 2, y - h / 2, h, h, h * r)
    ctx.set_source(lin(0, y - h / 2, 0, y + h / 2, [(0, top, a), (1, bottom, a)]))
    ctx.fill()
    # 顶部高光
    rrect(ctx, x - h / 2 + h * 0.06, y - h / 2 + h * 0.05, h * 0.88, h * 0.4, h * r * 0.8)
    ctx.set_source(lin(0, y - h / 2, 0, y - h * 0.05, [(0, "#FFFFFF", 0.22 * a), (1, "#FFFFFF", 0)]))
    ctx.fill()


class _U:
    """把 0..100 的图标坐标映射到实际坐标。"""

    def __init__(self, x, y, s):
        self.x, self.y, self.k = x - s / 2, y - s / 2, s / 100.0

    def __call__(self, px, py):
        return self.x + px * self.k, self.y + py * self.k

    def d(self, v):
        return v * self.k


# ---------------------------------------------------------------- Google 系 / 常用应用


def ic_gmail(ctx, x, y, s=100, a=1.0, t=0.0):
    _tile(ctx, x, y, s, "#FFFFFF", "#F2F2F5", a)
    u = _U(x, y, s)
    rrect(ctx, *u(18, 30), u.d(64), u.d(44), u.d(6))
    fill(ctx, "#FFFFFF", a)
    ctx.set_line_width(u.d(7))
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    setc(ctx, "#EA4335", a)
    poly(ctx, [u(22, 70), u(22, 34), u(50, 54), u(78, 34), u(78, 70)], close=False)
    ctx.stroke()
    line_w = u.d(7)
    ctx.set_line_width(line_w)
    setc(ctx, "#4285F4", a)
    ctx.move_to(*u(22, 70))
    ctx.line_to(*u(22, 45))
    ctx.stroke()
    setc(ctx, "#34A853", a)
    ctx.move_to(*u(78, 70))
    ctx.line_to(*u(78, 45))
    ctx.stroke()


def _page(ctx, u, color, a, fold=True):
    ctx.move_to(*u(26, 14))
    ctx.line_to(*u(62, 14))
    ctx.line_to(*u(76, 28))
    ctx.line_to(*u(76, 86))
    ctx.line_to(*u(26, 86))
    ctx.close_path()
    fill(ctx, color, a)
    if fold:
        poly(ctx, [u(62, 14), u(62, 28), u(76, 28)])
        fill(ctx, "#FFFFFF", 0.45 * a)


def ic_docs(ctx, x, y, s=100, a=1.0, t=0.0):
    _tile(ctx, x, y, s, "#FFFFFF", "#F2F2F5", a)
    u = _U(x, y, s)
    _page(ctx, u, "#4285F4", a)
    for i, w in enumerate((32, 32, 32, 20)):
        rrect(ctx, *u(34, 40 + i * 10), u.d(w), u.d(5), u.d(2.5))
        fill(ctx, "#FFFFFF", a)


def ic_sheets(ctx, x, y, s=100, a=1.0, t=0.0):
    _tile(ctx, x, y, s, "#FFFFFF", "#F2F2F5", a)
    u = _U(x, y, s)
    _page(ctx, u, "#0F9D58", a)
    rrect(ctx, *u(34, 40), u.d(34), u.d(34), u.d(2))
    fill(ctx, "#FFFFFF", a)
    ctx.set_line_width(u.d(3))
    setc(ctx, "#0F9D58", a)
    for i in (1, 2):
        ctx.move_to(*u(34, 40 + i * 11.3))
        ctx.line_to(*u(68, 40 + i * 11.3))
    ctx.move_to(*u(48, 40))
    ctx.line_to(*u(48, 74))
    ctx.stroke()


def ic_tasks(ctx, x, y, s=100, a=1.0, t=0.0):
    _tile(ctx, x, y, s, "#FFFFFF", "#F2F2F5", a)
    u = _U(x, y, s)
    circle(ctx, *u(50, 50), u.d(30))
    fill(ctx, "#1A73E8", a)
    check_mark(ctx, *u(50, 51), u.d(36), "#FFFFFF", 1.0, a)


def ic_calendar(ctx, x, y, s=100, a=1.0, t=0.0, day="31"):
    _tile(ctx, x, y, s, "#FFFFFF", "#F2F2F5", a)
    u = _U(x, y, s)
    rrect(ctx, *u(20, 20), u.d(60), u.d(62), u.d(8))
    fill(ctx, "#FFFFFF", a)
    ctx.set_line_width(u.d(3))
    setc(ctx, "#D7DCE5", a)
    rrect(ctx, *u(20, 20), u.d(60), u.d(62), u.d(8))
    ctx.stroke()
    ctx.save()
    rrect(ctx, *u(20, 20), u.d(60), u.d(62), u.d(8))
    ctx.clip()
    ctx.rectangle(*u(20, 20), u.d(60), u.d(16))
    fill(ctx, "#4285F4", a)
    ctx.restore()
    text(ctx, day, *u(50, 61), u.d(30), "#4285F4", a, "black")


def ic_instagram(ctx, x, y, s=100, a=1.0, t=0.0):
    u = _U(x, y, s)
    box_shadow(ctx, x - s / 2, y - s / 2, s, s, s * 0.26, blur=s * 0.22, a=0.22 * a, dy=s * 0.07)
    rrect(ctx, x - s / 2, y - s / 2, s, s, s * 0.26)
    ctx.set_source(lin(x - s / 2, y + s / 2, x + s / 2, y - s / 2,
                       [(0, "#FEDA75", a), (0.3, "#FA7E1E", a), (0.6, "#D62976", a), (1, "#4F5BD5", a)]))
    ctx.fill()
    ctx.set_line_width(u.d(7))
    setc(ctx, "#FFFFFF", a)
    rrect(ctx, *u(22, 22), u.d(56), u.d(56), u.d(16))
    ctx.stroke()
    circle(ctx, *u(50, 50), u.d(13))
    ctx.stroke()
    circle(ctx, *u(66, 34), u.d(4))
    fill(ctx, "#FFFFFF", a)


def ic_slack(ctx, x, y, s=100, a=1.0, t=0.0):
    _tile(ctx, x, y, s, "#FFFFFF", "#F2F2F5", a)
    u = _U(x, y, s)
    cols = ("#36C5F0", "#2EB67D", "#ECB22E", "#E01E5A")
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_width(u.d(11))
    segs = [((38, 26), (38, 62)), ((26, 62), (62, 62)), ((62, 74), (62, 38)), ((74, 38), (38, 38))]
    for (p0, p1), c in zip(segs, cols):
        setc(ctx, c, a)
        ctx.move_to(*u(*p0))
        ctx.line_to(*u(*p1))
        ctx.stroke()


def ic_notion(ctx, x, y, s=100, a=1.0, t=0.0):
    _tile(ctx, x, y, s, "#FFFFFF", "#F2F2F5", a)
    u = _U(x, y, s)
    rrect(ctx, *u(24, 20), u.d(52), u.d(60), u.d(6))
    ctx.set_line_width(u.d(5))
    setc(ctx, "#111111", a)
    ctx.stroke()
    text(ctx, "N", *u(50, 51), u.d(40), "#111111", a, "serif")


def ic_github(ctx, x, y, s=100, a=1.0, t=0.0):
    _tile(ctx, x, y, s, "#2B3137", "#16191D", a)
    u = _U(x, y, s)
    text(ctx, "</>", *u(50, 50), u.d(34), "#FFFFFF", a, "monob")


def ic_wiki(ctx, x, y, s=100, a=1.0, t=0.0):
    _tile(ctx, x, y, s, "#FFFFFF", "#ECECEF", a)
    u = _U(x, y, s)
    circle(ctx, *u(50, 50), u.d(30))
    ctx.set_line_width(u.d(3))
    setc(ctx, "#9AA0AE", a)
    ctx.stroke()
    ellipse(ctx, *u(50, 50), u.d(13), u.d(30))
    ctx.stroke()
    ctx.move_to(*u(20, 50))
    ctx.line_to(*u(80, 50))
    ctx.stroke()
    text(ctx, "W", *u(50, 51), u.d(36), "#222222", a, "serif")


def ic_paper(ctx, x, y, s=100, a=1.0, t=0.0):
    _tile(ctx, x, y, s, "#FFFFFF", "#F1EDEA", a)
    u = _U(x, y, s)
    rrect(ctx, *u(24, 16), u.d(52), u.d(68), u.d(4))
    fill(ctx, "#FFFFFF", a)
    ctx.set_line_width(u.d(2.5))
    setc(ctx, "#D9D2CC", a)
    rrect(ctx, *u(24, 16), u.d(52), u.d(68), u.d(4))
    ctx.stroke()
    rrect(ctx, *u(30, 23), u.d(40), u.d(8), u.d(2))
    fill(ctx, "#B31B1B", a)
    for i in range(5):
        rrect(ctx, *u(30, 38 + i * 8), u.d(40 if i % 2 == 0 else 32), u.d(4), u.d(2))
        fill(ctx, "#C9C1BA", a)
    text(ctx, "∑", *u(62, 74), u.d(16), "#B31B1B", a, "bold")


def ic_qa(ctx, x, y, s=100, a=1.0, t=0.0):
    _tile(ctx, x, y, s, "#FFFFFF", "#F2F2F5", a)
    u = _U(x, y, s)
    rrect(ctx, *u(16, 20), u.d(46), u.d(32), u.d(10))
    fill(ctx, "#F48024", a)
    text(ctx, "Q", *u(39, 36), u.d(22), "#FFFFFF", a, "black")
    rrect(ctx, *u(38, 48), u.d(46), u.d(32), u.d(10))
    fill(ctx, "#BCBBBB", a)
    text(ctx, "A", *u(61, 64), u.d(22), "#FFFFFF", a, "black")


def ic_reddit(ctx, x, y, s=100, a=1.0, t=0.0):
    u = _U(x, y, s)
    box_shadow(ctx, x - s / 2, y - s / 2, s, s, s / 2, blur=s * 0.2, a=0.2 * a, dy=s * 0.06)
    circle(ctx, x, y, s / 2)
    fill(ctx, "#FF4500", a)
    rrect(ctx, *u(22, 28), u.d(56), u.d(38), u.d(16))
    fill(ctx, "#FFFFFF", a)
    poly(ctx, [u(34, 62), u(28, 76), u(46, 64)])
    fill(ctx, "#FFFFFF", a)
    for px in (40, 60):
        circle(ctx, *u(px, 46), u.d(4.5))
        fill(ctx, "#FF4500", a)


# ---------------------------------------------------------------- 通用物件


def ic_browser(ctx, x, y, s=100, a=1.0, t=0.0):
    _tile(ctx, x, y, s, "#5B9BFF", "#3A6FE0", a)
    u = _U(x, y, s)
    rrect(ctx, *u(16, 22), u.d(68), u.d(56), u.d(8))
    fill(ctx, "#FFFFFF", a)
    ctx.rectangle(*u(16, 34), u.d(68), u.d(2.5))
    fill(ctx, "#C8D6F5", a)
    for i in range(3):
        circle(ctx, *u(24 + i * 7, 28), u.d(2.4))
        fill(ctx, "#9DB4E8", a)
    circle(ctx, *u(50, 56), u.d(14))
    ctx.set_line_width(u.d(3))
    setc(ctx, "#3A6FE0", a)
    ctx.stroke()
    ellipse(ctx, *u(50, 56), u.d(6), u.d(14))
    ctx.stroke()
    ctx.move_to(*u(36, 56))
    ctx.line_to(*u(64, 56))
    ctx.stroke()


def ic_terminal(ctx, x, y, s=100, a=1.0, t=0.0, accent="#7CFFB2"):
    _tile(ctx, x, y, s, "#3A3646", "#1E1B26", a)
    u = _U(x, y, s)
    ctx.set_line_width(u.d(7))
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    setc(ctx, accent, a)
    poly(ctx, [u(26, 36), u(42, 50), u(26, 64)], close=False)
    ctx.stroke()
    if (t * 2) % 1 < 0.6:
        rrect(ctx, *u(50, 60), u.d(24), u.d(7), u.d(3))
        fill(ctx, accent, a)


def ic_folder(ctx, x, y, s=100, a=1.0, t=0.0, color="#FFB547"):
    u = _U(x, y, s)
    box_shadow(ctx, *u(12, 24), u.d(76), u.d(56), u.d(8), blur=s * 0.18, a=0.18 * a, dy=s * 0.05)
    rrect(ctx, *u(12, 22), u.d(34), u.d(16), u.d(5))
    fill(ctx, "#E89A2C", a)
    rrect(ctx, *u(12, 30), u.d(76), u.d(52), u.d(8))
    ctx.set_source(lin(0, u(0, 30)[1], 0, u(0, 82)[1], [(0, color, a), (1, "#F09A2B", a)]))
    ctx.fill()


def ic_mail(ctx, x, y, s=100, a=1.0, t=0.0, color="#FFFFFF", line="#E36A5E"):
    u = _U(x, y, s)
    box_shadow(ctx, *u(12, 24), u.d(76), u.d(54), u.d(8), blur=s * 0.16, a=0.18 * a, dy=s * 0.05)
    rrect(ctx, *u(12, 24), u.d(76), u.d(54), u.d(8))
    fill(ctx, color, a)
    ctx.set_line_width(u.d(4.5))
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    setc(ctx, line, a)
    poly(ctx, [u(16, 30), u(50, 56), u(84, 30)], close=False)
    ctx.stroke()


def ic_chat(ctx, x, y, s=100, a=1.0, t=0.0, color="#2EC4B6"):
    u = _U(x, y, s)
    rrect(ctx, *u(12, 18), u.d(62), u.d(44), u.d(14))
    fill(ctx, color, a)
    poly(ctx, [u(24, 58), u(20, 74), u(38, 60)])
    fill(ctx, color, a)
    rrect(ctx, *u(40, 46), u.d(48), u.d(34), u.d(12))
    fill(ctx, "#FFFFFF", a)
    ctx.set_line_width(u.d(3))
    setc(ctx, color, a)
    rrect(ctx, *u(40, 46), u.d(48), u.d(34), u.d(12))
    ctx.stroke()
    for i in range(3):
        circle(ctx, *u(54 + i * 10, 63), u.d(3))
        fill(ctx, color, a)


def ic_book(ctx, x, y, s=100, a=1.0, t=0.0, color="#8B6CFF"):
    u = _U(x, y, s)
    box_shadow(ctx, *u(20, 14), u.d(60), u.d(72), u.d(6), blur=s * 0.16, a=0.18 * a, dy=s * 0.05)
    rrect(ctx, *u(20, 14), u.d(60), u.d(72), u.d(6))
    fill(ctx, color, a)
    ctx.rectangle(*u(26, 14), u.d(6), u.d(72))
    fill(ctx, "#000000", 0.18 * a)
    rrect(ctx, *u(38, 30), u.d(32), u.d(6), u.d(3))
    fill(ctx, "#FFFFFF", 0.85 * a)
    rrect(ctx, *u(38, 42), u.d(24), u.d(5), u.d(2.5))
    fill(ctx, "#FFFFFF", 0.6 * a)
    ctx.rectangle(*u(24, 78), u.d(56), u.d(6))
    fill(ctx, "#FFFFFF", 0.9 * a)


def ic_code(ctx, x, y, s=100, a=1.0, t=0.0):
    _tile(ctx, x, y, s, "#2D2A3A", "#1A1824", a)
    u = _U(x, y, s)
    cols = ("#FF7AA2", "#7CC6FF", "#FFC857", "#7CFFB2")
    for i in range(4):
        rrect(ctx, *u(22 + (i % 2) * 8, 26 + i * 13), u.d(30 + (i * 7) % 20), u.d(6), u.d(3))
        fill(ctx, cols[i], a)


def ic_web(ctx, x, y, s=100, a=1.0, t=0.0):
    _tile(ctx, x, y, s, "#FFFFFF", "#EEF2F8", a)
    u = _U(x, y, s)
    text(ctx, "www", *u(50, 50), u.d(28), "#4C8DFF", a, "black")


def ic_junk(ctx, x, y, s=100, a=1.0, t=0.0):
    _tile(ctx, x, y, s, "#B9B5BE", "#8D8894", a)
    u = _U(x, y, s)
    text(ctx, "广告", *u(50, 40), u.d(26), "#FFFFFF", a, "black")
    text(ctx, "!!!", *u(50, 66), u.d(22), "#FF5A5F", a, "black")


def ic_brain(ctx, x, y, s=100, a=1.0, t=0.0, color="#8B6CFF", glow_a=0.5):
    """神经网络"大脑"：圆形中的节点与连线，会脉动。"""
    u = _U(x, y, s)
    glow(ctx, x, y, s * 0.9, color, glow_a * a)
    circle(ctx, x, y, s / 2)
    ctx.set_source(rad(x, y, 0, s / 2, [(0, "#FFFFFF", 0.95 * a), (0.6, "#E9E2FF", a), (1, "#C9BBFF", a)],
                       fx=x - s * 0.15, fy=y - s * 0.2))
    ctx.fill()
    layers = [(28, (36, 64)), (50, (26, 50, 74)), (72, (36, 64))]
    pts = [[u(lx, ly) for ly in ys] for lx, ys in layers]
    ctx.set_line_width(u.d(2.4))
    for L in range(2):
        for p in pts[L]:
            for q in pts[L + 1]:
                setc(ctx, color, 0.45 * a)
                ctx.move_to(*p)
                ctx.line_to(*q)
                ctx.stroke()
    for li, layer in enumerate(pts):
        for ni, p in enumerate(layer):
            k = 0.5 + 0.5 * math.sin(t * 4 + li * 1.3 + ni * 0.9)
            circle(ctx, p[0], p[1], u.d(6 + 1.5 * k))
            fill(ctx, color, a)


def ic_gpu(ctx, x, y, s=100, a=1.0, t=0.0, spin=0.0, glow_a=0.0):
    """显卡（两个会转的风扇）。尺寸以宽 s 计，高约 0.55s。"""
    w, h = s, s * 0.55
    x0, y0 = x - w / 2, y - h / 2
    box_shadow(ctx, x0, y0, w, h, h * 0.12, blur=s * 0.12, a=0.3 * a, dy=s * 0.04)
    rrect(ctx, x0, y0, w, h, h * 0.12)
    ctx.set_source(lin(0, y0, 0, y0 + h, [(0, "#3B3F48", a), (1, "#1C1E24", a)]))
    ctx.fill()
    ctx.rectangle(x0 + w * 0.06, y0 + h - h * 0.08, w * 0.6, h * 0.12)
    fill(ctx, "#D9A441", a)
    rrect(ctx, x0, y0, w, h * 0.12, h * 0.06)
    fill(ctx, "#76B900", a)
    if glow_a > 0:
        glow(ctx, x, y, s * 0.8, "#76B900", glow_a * a)
    for i in (0, 1):
        fx, fy, fr = x0 + w * (0.29 + 0.42 * i), y0 + h * 0.55, h * 0.33
        circle(ctx, fx, fy, fr)
        fill(ctx, "#111216", a)
        ctx.set_line_width(2)
        setc(ctx, "#5A5F6B", a)
        circle(ctx, fx, fy, fr)
        ctx.stroke()
        for b in range(7):
            ang = spin * TAU + b / 7 * TAU
            ctx.move_to(fx, fy)
            ctx.arc(fx, fy, fr * 0.88, ang, ang + 0.5)
            ctx.close_path()
        fill(ctx, "#4A4F5B", a)
        circle(ctx, fx, fy, fr * 0.22)
        fill(ctx, "#76B900", a)


def gear_path(ctx, x, y, r, teeth=10, depth=0.18, rot=0.0, hole=0.35):
    n = teeth * 4
    pts = []
    for i in range(n):
        ang = rot + i / n * TAU
        rr = r if (i % 4) in (1, 2) else r * (1 - depth)
        pts.append((x + math.cos(ang) * rr, y + math.sin(ang) * rr))
    poly(ctx, pts)
    if hole > 0:
        ctx.new_sub_path()
        ctx.arc_negative(x, y, r * hole, TAU, 0)


def ic_gear(ctx, x, y, r, teeth=10, rot=0.0, color="#8FA3BF", a=1.0, shade=True):
    if a <= 0.003:
        return
    gear_path(ctx, x, y, r, teeth, 0.2, rot)
    if shade:
        ctx.set_source(rad(x, y, r * 0.3, r, [(0, color, a), (1, _dark(color), a)],
                           fx=x - r * 0.3, fy=y - r * 0.3))
    else:
        setc(ctx, color, a)
    ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    ctx.fill()
    ctx.set_fill_rule(cairo.FILL_RULE_WINDING)


def _dark(c):
    from .core import hexc
    r, g, b = hexc(c)
    return (r * 0.62, g * 0.62, b * 0.62)


def ic_lock(ctx, x, y, s=100, a=1.0, t=0.0, color="#9AA0AE", open_=0.0):
    u = _U(x, y, s)
    ctx.set_line_width(u.d(9))
    setc(ctx, "#6E7380", a)
    ctx.new_sub_path()
    ctx.arc(*u(50, 40 - 14 * open_), u.d(18), math.pi, TAU)
    ctx.stroke()
    ctx.move_to(*u(32, 40 - 14 * open_))
    ctx.line_to(*u(32, 48))
    ctx.move_to(*u(68, 40 - 14 * open_))
    ctx.line_to(*u(68, 48))
    ctx.stroke()
    rrect(ctx, *u(22, 44), u.d(56), u.d(42), u.d(8))
    ctx.set_source(lin(0, u(0, 44)[1], 0, u(0, 86)[1], [(0, "#FFD25C", a), (1, "#E9A93A", a)]))
    ctx.fill()
    circle(ctx, *u(50, 62), u.d(6))
    fill(ctx, "#7A5512", a)
    ctx.rectangle(*u(48, 63), u.d(4), u.d(11))
    fill(ctx, "#7A5512", a)


def ic_plug(ctx, x, y, s=100, a=1.0, t=0.0, color="#4C8DFF", rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    u = _U(0, 0, s)
    for px in (40, 60):
        rrect(ctx, *u(px - 3, 6), u.d(6), u.d(20), u.d(2))
        fill(ctx, "#C9CED8", a)
    rrect(ctx, *u(26, 22), u.d(48), u.d(42), u.d(10))
    fill(ctx, color, a)
    rrect(ctx, *u(42, 60), u.d(16), u.d(30), u.d(6))
    fill(ctx, color, a)
    ctx.restore()


def ic_phone(ctx, x, y, s=100, a=1.0, t=0.0, screen="#FFFFFF"):
    """竖屏手机，高 s，宽 0.52s。"""
    w, h = s * 0.52, s
    box_shadow(ctx, x - w / 2, y - h / 2, w, h, w * 0.18, blur=s * 0.16, a=0.25 * a, dy=s * 0.05)
    rrect(ctx, x - w / 2, y - h / 2, w, h, w * 0.18)
    fill(ctx, "#25222D", a)
    rrect(ctx, x - w / 2 + w * 0.07, y - h / 2 + w * 0.07, w * 0.86, h - w * 0.14, w * 0.13)
    fill(ctx, screen, a)
    rrect(ctx, x - w * 0.14, y - h / 2 + w * 0.1, w * 0.28, w * 0.07, w * 0.035)
    fill(ctx, "#25222D", a)


def ic_laptop(ctx, x, y, s=100, a=1.0, t=0.0, screen="#1E1B26"):
    w, h = s, s * 0.62
    rrect(ctx, x - w * 0.42, y - h / 2, w * 0.84, h * 0.82, s * 0.04)
    fill(ctx, "#3A3646", a)
    rrect(ctx, x - w * 0.38, y - h / 2 + s * 0.035, w * 0.76, h * 0.82 - s * 0.07, s * 0.02)
    fill(ctx, screen, a)
    rrect(ctx, x - w / 2, y + h * 0.32, w, h * 0.12, s * 0.03)
    fill(ctx, "#C9C5D3", a)


def ic_plane(ctx, x, y, s=100, a=1.0, t=0.0, color="#4C8DFF", rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    u = _U(0, 0, s)
    poly(ctx, [u(10, 50), u(88, 44), u(96, 50), u(88, 56)])
    fill(ctx, color, a)
    poly(ctx, [u(44, 48), u(64, 46), u(40, 14), u(32, 14)])
    fill(ctx, color, a)
    poly(ctx, [u(44, 52), u(64, 54), u(40, 86), u(32, 86)])
    fill(ctx, color, a)
    poly(ctx, [u(14, 50), u(22, 49), u(14, 34), u(8, 34)])
    fill(ctx, color, a)
    ctx.restore()


def ic_coin(ctx, x, y, s=100, a=1.0, t=0.0, spin=0.0):
    k = abs(math.cos(spin * math.pi))
    ellipse(ctx, x, y, s / 2 * max(k, 0.08), s / 2)
    ctx.set_source(rad(x, y, 0, s / 2, [(0, "#FFE58A", a), (1, "#E9A93A", a)], fx=x - s * 0.15, fy=y - s * 0.15))
    ctx.fill()
    if k > 0.4:
        text(ctx, "$", x, y, s * 0.55 * k, "#B9771B", a, "black")


def ic_scroll(ctx, x, y, s=100, a=1.0, t=0.0):
    u = _U(x, y, s)
    box_shadow(ctx, *u(20, 12), u.d(60), u.d(76), u.d(6), blur=s * 0.16, a=0.2 * a, dy=s * 0.05)
    rrect(ctx, *u(20, 12), u.d(60), u.d(76), u.d(6))
    fill(ctx, "#FFF8E8", a)
    text(ctx, "授权", *u(50, 28), u.d(16), "#8A5A2B", a, "black")
    for i in range(4):
        rrect(ctx, *u(30, 40 + i * 9), u.d(40 if i < 3 else 26), u.d(4), u.d(2))
        fill(ctx, "#D8C8A8", a)
    circle(ctx, *u(64, 76), u.d(9))
    fill(ctx, "#E5484D", a)
    check_mark(ctx, *u(64, 76), u.d(11), "#FFFFFF", 1.0, a)


def ic_building(ctx, x, y, s=100, a=1.0, t=0.0, color="#E9E4F2", label=None):
    u = _U(x, y, s)
    poly(ctx, [u(10, 34), u(50, 10), u(90, 34)])
    fill(ctx, color, a)
    ctx.rectangle(*u(14, 34), u.d(72), u.d(6))
    fill(ctx, color, a)
    for i in range(5):
        ctx.rectangle(*u(18 + i * 15, 42), u.d(7), u.d(36))
        fill(ctx, color, a)
    ctx.rectangle(*u(10, 80), u.d(80), u.d(8))
    fill(ctx, color, a)


def ic_trophy(ctx, x, y, s=100, a=1.0, t=0.0):
    u = _U(x, y, s)
    glow(ctx, x, y - s * 0.1, s * 0.9, "#FFD25C", 0.35 * a)
    ctx.set_line_width(u.d(7))
    setc(ctx, "#E9A93A", a)
    for side in (-1, 1):
        ctx.new_sub_path()
        ctx.arc(*u(50 + side * 30, 36), u.d(10), 0, TAU)
        ctx.stroke()
    ctx.move_to(*u(26, 18))
    ctx.line_to(*u(74, 18))
    ctx.curve_to(*u(74, 52), *u(62, 60), *u(50, 62))
    ctx.curve_to(*u(38, 60), *u(26, 52), *u(26, 18))
    ctx.set_source(lin(0, u(0, 18)[1], 0, u(0, 62)[1], [(0, "#FFE58A", a), (1, "#E9A93A", a)]))
    ctx.fill()
    ctx.rectangle(*u(45, 60), u.d(10), u.d(14))
    fill(ctx, "#E9A93A", a)
    rrect(ctx, *u(32, 72), u.d(36), u.d(12), u.d(3))
    fill(ctx, "#B9771B", a)
    star4(ctx, *u(50, 36), u.d(10), "#FFFFFF", 0.9 * a, t)


def ic_penguin(ctx, x, y, s=100, a=1.0, t=0.0):
    u = _U(x, y, s)
    ellipse(ctx, *u(50, 54), u.d(28), u.d(36))
    fill(ctx, "#1E1E24", a)
    ellipse(ctx, *u(50, 60), u.d(19), u.d(26))
    fill(ctx, "#FFFFFF", a)
    for px in (43, 57):
        circle(ctx, *u(px, 34), u.d(5))
        fill(ctx, "#FFFFFF", a)
        circle(ctx, *u(px + 1, 35), u.d(2.4))
        fill(ctx, "#1E1E24", a)
    poly(ctx, [u(44, 42), u(56, 42), u(50, 49)])
    fill(ctx, "#FFB547", a)
    for px in (38, 62):
        ellipse(ctx, *u(px, 90), u.d(10), u.d(4))
        fill(ctx, "#FFB547", a)


def ic_ubuntu(ctx, x, y, s=100, a=1.0, t=0.0, rot=0.0):
    u = _U(x, y, s)
    circle(ctx, x, y, s / 2)
    fill(ctx, "#E95420", a)
    ctx.set_line_width(u.d(8))
    setc(ctx, "#FFFFFF", a)
    for i in range(3):
        ang = rot + i * TAU / 3
        ctx.new_sub_path()
        ctx.arc(x, y, u.d(22), ang + 0.42, ang + TAU / 3 - 0.42)
        ctx.stroke()
        circle(ctx, x + math.cos(ang) * u.d(31), y + math.sin(ang) * u.d(31), u.d(7.5))
        fill(ctx, "#FFFFFF", a)


def ic_flame(ctx, x, y, s=100, a=1.0, t=0.0):
    u = _U(x, y, s)
    k = 1 + 0.04 * math.sin(t * 9)
    ctx.save()
    ctx.translate(x, y + s * 0.4)
    ctx.scale(1, k)
    ctx.translate(-x, -(y + s * 0.4))
    ctx.move_to(*u(50, 10))
    ctx.curve_to(*u(66, 30), *u(82, 48), *u(78, 66))
    ctx.curve_to(*u(74, 84), *u(60, 92), *u(50, 92))
    ctx.curve_to(*u(34, 92), *u(22, 80), *u(24, 62))
    ctx.curve_to(*u(26, 46), *u(42, 36), *u(50, 10))
    ctx.set_source(lin(0, u(0, 10)[1], 0, u(0, 92)[1], [(0, "#FF9A3C", a), (1, "#EE4C2C", a)]))
    ctx.fill()
    ellipse(ctx, *u(50, 70), u.d(12), u.d(14))
    fill(ctx, "#FFFFFF", a)
    ctx.restore()


def ic_cake(ctx, x, y, s=100, a=1.0, t=0.0, size=1.0):
    u = _U(x, y, s)
    ellipse(ctx, *u(50, 86), u.d(44), u.d(8))
    fill(ctx, "#E9E4F2", a)
    rrect(ctx, *u(16, 46), u.d(68), u.d(40), u.d(8))
    ctx.set_source(lin(0, u(0, 46)[1], 0, u(0, 86)[1], [(0, "#FFD7E2", a), (1, "#F7A8BE", a)]))
    ctx.fill()
    rrect(ctx, *u(16, 40), u.d(68), u.d(14), u.d(7))
    fill(ctx, "#FFFFFF", a)
    for i in range(5):
        circle(ctx, *u(24 + i * 13, 54), u.d(5))
        fill(ctx, "#FFFFFF", a)
    rrect(ctx, *u(47, 18), u.d(6), u.d(22), u.d(2))
    fill(ctx, "#7CC6FF", a)
    ellipse(ctx, *u(50, 14), u.d(5), u.d(8))
    fill(ctx, "#FFC857", a)
    glow(ctx, *u(50, 13), u.d(16), "#FFE58A", 0.5 * a)


def ic_server(ctx, x, y, s=100, a=1.0, t=0.0):
    u = _U(x, y, s)
    for i in range(3):
        rrect(ctx, *u(18, 14 + i * 25), u.d(64), u.d(21), u.d(4))
        fill(ctx, "#2D3446", a)
        for j in range(3):
            on = (math.sin(t * 6 + i * 2 + j * 1.7) > 0)
            circle(ctx, *u(28 + j * 9, 24.5 + i * 25), u.d(2.6))
            fill(ctx, "#7CFFB2" if on else "#2E5E46", a)
        rrect(ctx, *u(56, 22 + i * 25), u.d(20), u.d(5), u.d(2))
        fill(ctx, "#56607A", a)


# ---------------------------------------------------------------- 产品图标（通用风格，非官方 Logo）


def ic_chatgpt(ctx, x, y, s=100, a=1.0, t=0.0):
    _tile(ctx, x, y, s, "#19C39C", "#0E8F73", a)
    u = _U(x, y, s)
    rrect(ctx, *u(20, 24), u.d(60), u.d(42), u.d(16))
    fill(ctx, "#FFFFFF", a)
    poly(ctx, [u(32, 62), u(28, 78), u(46, 64)])
    fill(ctx, "#FFFFFF", a)
    star4(ctx, *u(50, 45), u.d(13), "#19C39C", a, t * 0.8)


def ic_codex(ctx, x, y, s=100, a=1.0, t=0.0):
    _tile(ctx, x, y, s, "#3B3A4A", "#15141C", a)
    u = _U(x, y, s)
    ellipse(ctx, *u(58, 34), u.d(22), u.d(12))
    fill(ctx, "#8AB4FF", 0.9 * a)
    circle(ctx, *u(46, 32), u.d(11))
    fill(ctx, "#8AB4FF", 0.9 * a)
    ctx.set_line_width(u.d(6.5))
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    setc(ctx, "#FFFFFF", a)
    poly(ctx, [u(26, 54), u(38, 64), u(26, 74)], close=False)
    ctx.stroke()
    rrect(ctx, *u(46, 70), u.d(24), u.d(6), u.d(3))
    fill(ctx, "#FFFFFF", a)


def ic_claude_code(ctx, x, y, s=100, a=1.0, t=0.0):
    _tile(ctx, x, y, s, "#F0A07A", "#D9774F", a)
    u = _U(x, y, s)
    cx, cy = u(50, 40)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_width(u.d(6))
    setc(ctx, "#FFFFFF", a)
    for i in range(8):
        ang = i * TAU / 8 + t * 0.3
        L = u.d(17 if i % 2 == 0 else 12)
        ctx.move_to(cx, cy)
        ctx.line_to(cx + math.cos(ang) * L, cy + math.sin(ang) * L)
    ctx.stroke()
    ctx.set_line_width(u.d(5.5))
    poly(ctx, [u(28, 66), u(38, 73), u(28, 80)], close=False)
    ctx.stroke()
    rrect(ctx, *u(44, 76), u.d(22), u.d(5.5), u.d(2.7))
    fill(ctx, "#FFFFFF", a)


def ic_opencode(ctx, x, y, s=100, a=1.0, t=0.0):
    _tile(ctx, x, y, s, "#26262B", "#0B0B0E", a)
    u = _U(x, y, s)
    text(ctx, "{ }", *u(50, 48), u.d(40), "#FFFFFF", a, "monob")
    rrect(ctx, *u(30, 72), u.d(40), u.d(5), u.d(2.5))
    fill(ctx, "#7CFFB2", a)


def ic_openclaw(ctx, x, y, s=100, a=1.0, t=0.0):
    """龙虾钳：上下两片钳子，偶尔"咔"地夹一下。"""
    _tile(ctx, x, y, s, "#FF6B5B", "#D83A2E", a)
    u = _U(x, y, s)
    snap = 0.22 * max(0.0, math.sin(t * 2.6)) ** 10
    setc(ctx, "#FFFFFF", a)
    ctx.set_line_width(u.d(15))
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(*u(22, 84))
    ctx.line_to(*u(38, 66))
    ctx.stroke()
    circle(ctx, *u(42, 62), u.d(16))
    fill(ctx, "#FFFFFF", a)
    px, py = u(42, 62)
    for sgn in (-1, 1):
        ctx.save()
        ctx.translate(px, py)
        ctx.rotate(sgn * snap)
        ctx.translate(-px, -py)
        if sgn < 0:   # 上钳（大）
            ctx.move_to(*u(32, 54))
            ctx.curve_to(*u(34, 24), *u(66, 10), *u(86, 30))
            ctx.curve_to(*u(72, 27), *u(58, 33), *u(52, 52))
        else:         # 下钳（小）
            ctx.move_to(*u(50, 72))
            ctx.curve_to(*u(64, 78), *u(82, 70), *u(88, 50))
            ctx.curve_to(*u(78, 59), *u(66, 60), *u(54, 58))
        ctx.close_path()
        fill(ctx, "#FFFFFF", a)
        ctx.restore()
    circle(ctx, *u(43, 61), u.d(4))
    fill(ctx, "#D83A2E", a)


def ic_workbuddy(ctx, x, y, s=100, a=1.0, t=0.0):
    _tile(ctx, x, y, s, "#3E8BFF", "#1D5FD6", a)
    u = _U(x, y, s)
    rrect(ctx, *u(22, 30), u.d(56), u.d(44), u.d(12))
    fill(ctx, "#FFFFFF", a)
    rrect(ctx, *u(40, 22), u.d(20), u.d(10), u.d(4))
    ctx.set_line_width(u.d(4))
    setc(ctx, "#FFFFFF", a)
    ctx.stroke()
    for px in (40, 60):
        circle(ctx, *u(px, 48), u.d(4.2))
        fill(ctx, "#1D5FD6", a)
    ctx.set_line_width(u.d(3.5))
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    setc(ctx, "#1D5FD6", a)
    ctx.new_sub_path()
    ctx.arc(*u(50, 56), u.d(8), 0.25, math.pi - 0.25)
    ctx.stroke()


def ic_muse(ctx, x, y, s=100, a=1.0, t=0.0):
    u = _U(x, y, s)
    glow(ctx, x, y, s * 0.85, "#8B6CFF", 0.35 * a)
    circle(ctx, x, y, s / 2)
    ctx.set_source(lin(x - s / 2, y + s / 2, x + s / 2, y - s / 2,
                       [(0, "#3D7BFF", a), (0.55, "#8B5CF6", a), (1, "#FF7AC6", a)]))
    ctx.fill()
    circle(ctx, x - s * 0.14, y - s * 0.16, s * 0.2)
    fill(ctx, "#FFFFFF", 0.18 * a)
    text(ctx, "M", x, y + u.d(1), u.d(46), "#FFFFFF", a, "black")


PRODUCT_ICONS = {
    "chatgpt": ic_chatgpt, "codex": ic_codex, "claude_code": ic_claude_code,
    "opencode": ic_opencode, "openclaw": ic_openclaw, "workbuddy": ic_workbuddy, "muse": ic_muse,
}

APP_ICONS = {
    "gmail": ic_gmail, "docs": ic_docs, "sheets": ic_sheets, "tasks": ic_tasks,
    "calendar": ic_calendar, "instagram": ic_instagram, "slack": ic_slack, "notion": ic_notion,
    "github": ic_github,
}


def google_word(ctx, x, y, size, a=1.0, align="c"):
    """四色 "Google" 字样（普通字体着色，非官方字标）。"""
    from .core import font
    cols = ("#4285F4", "#EA4335", "#FBBC05", "#4285F4", "#34A853", "#EA4335")
    font(ctx, size, "bold")
    adv = [ctx.text_extents(ch).x_advance for ch in "Google"]
    tw = sum(adv)
    cx = x - tw / 2 if align == "c" else (x - tw if align == "r" else x)
    for ch, w_, c in zip("Google", adv, cols):
        text(ctx, ch, cx, y, size, c, a, "bold", "l")
        cx += w_
    return tw
