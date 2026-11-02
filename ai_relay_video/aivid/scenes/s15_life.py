"""06 · AI 与你（下）：生活与世界。私人助理（订票、比价、日程、吃药提醒）→ AI 老师、AI 看影像 →
AI 预测蛋白质结构，2024 诺贝尔化学奖 → 像电和互联网一样的新基础设施。"""
import math

from mascot import draw_mascot

from ..core import (TAU, Cam, at, box_shadow, circle, clamp, ease_back, ease_in, ease_io, ease_out, ease_out5,
                    ellipse, fill, glow, lerp, lin, line, pop, prog, rad, ring_burst, rng, rrect, setc, smooth,
                    sparkle_burst, star4, stroke_pts, text, text_w, view, check_mark, bezier_pts, polyline_partial)
from ..icons import ic_calendar, ic_plane
from ..props import bg_grad, iphone, medal, pylon, price_tag, tag
from .common import host, mini_icon, talk_lines

DUR = 28.0
CHAPTER = ("06", "AI 与你")

VO = [
    (0.7, '再往后，AI 会走进{生活}：每个人都有一个懂你的私人助理，帮你订票、比价、管日程、提醒吃药；'),
    (9.2, '孩子有一对一的 AI 老师，医生有 AI 帮忙看影像；'),
    (14.4, '科学家用 AI 预测蛋白质结构，2024 年的诺贝尔化学奖，就颁给了 {AlphaFold} 的研发者。'),
    (21.5, 'AI 不只是新工具，而是像电和互联网一样的{新基础设施}。'),
]

G = 900
XA, XB, XC, XD = 960, 3100, 5200, 7300

P = (host(XA - 380, G, 0.64, "relieved", seed=15.5)
     .fx(0, ()).hold(0.0, ("coffee",), "r", 0.0).arm(0.0, "r", 0.6)
     .look(0.0, 0.8, -0.6)
     .expr(1.4, "smile").sit(1.6, 1.0)
     .expr(3.6, "happy").expr(6.6, "love").fx(7.4, ())
     .stand(8.2).drop(8.4).arm(8.4, "r", 0.0)
     .run_to(8.5, 9.3, XB - 60, G).expr(9.4, "curious").look(9.4, -0.8, -0.5).look(11.6, 0.8, -0.5)
     .expr(13.6, "smile").run_to(13.8, 14.6, XC - 720, G)
     .expr(14.7, "awe").look(14.7, 0.9, -0.8)
     .expr(18.0, "starry").hop(18.1, 50, 0.4)
     .expr(20.8, "smile").run_to(20.9, 21.7, XD - 760, G)
     .expr(21.8, "awe").look(21.8, 0.9, -0.7)
     .expr(24.0, "starry"))
talk_lines(P, VO, [0, 3], smile=0.4)

CAM = Cam([
    (0.0, (XA, 540, 1.08)),
    (8.4, (XA + 20, 540, 1.0)),
    (9.3, (XB, 540, 1.0), ease_io),
    (13.7, (XB + 20, 540, 1.02)),
    (14.6, (XC, 540, 1.0), ease_io),
    (20.8, (XC + 20, 540, 1.03)),
    (21.7, (XD, 520, 0.95), ease_io),
    (28.0, (XD + 20, 500, 1.02)),
], drift=6, seed=31.0)


def _bg(ctx, t, cam):
    bg_grad(ctx, "#FFF1DC", "#FFD7C6", "#FFE6D2", 0.6)
    ctx.set_source(rad(1600, 160, 40, 900, [(0, "#FFF7DA", 0.9), (1, "#FFF7DA", 0)]))
    ctx.paint()
    with view(ctx, cam, 1.0):
        ctx.rectangle(-1000, G, 10000, 400)
        ctx.set_source(lin(0, G, 0, G + 260, [(0, "#E7C6A6"), (1, "#D2A884")]))
        ctx.fill()


def _part_a(ctx, t):
    a = 1 - smooth(prog(t, 8.8, 9.4))
    if a <= 0:
        return
    # 窗户 + 植物 + 沙发
    wx, wy = XA - 620, 330
    rrect(ctx, wx - 170, wy - 170, 340, 300, 18)
    fill(ctx, "#FFFFFF", a)
    rrect(ctx, wx - 156, wy - 156, 312, 272, 12)
    ctx.set_source(lin(0, wy - 156, 0, wy + 116, [(0, "#9FD8FF", a), (1, "#FFE0B8", a)]))
    ctx.fill()
    glow(ctx, wx + 60, wy + 60, 120, "#FFD36B", 0.8 * a)
    circle(ctx, wx + 60, wy + 70, 40)
    fill(ctx, "#FFC857", a)
    line(ctx, wx, wy - 156, wx, wy + 116, 8, "#FFFFFF", a)
    rrect(ctx, XA - 560, G - 170, 360, 120, 40)
    fill(ctx, "#8B6CFF", 0.85 * a)
    rrect(ctx, XA - 590, G - 230, 60, 230, 30)
    fill(ctx, "#7A5AE8", 0.9 * a)
    rrect(ctx, XA - 230, G - 230, 60, 230, 30)
    fill(ctx, "#7A5AE8", 0.9 * a)
    # 私人助理：手机 + 四件事
    px, py = XA + 300, 470
    sx, sy, sw, sh = iphone(ctx, px, py, 560, a)
    ctx.save()
    rrect(ctx, sx, sy, sw, sh, 24)
    ctx.clip()
    ctx.set_source(lin(0, sy, 0, sy + sh, [(0, "#F7F5FA", a), (1, "#ECE7F5", a)]))
    ctx.paint()
    text(ctx, "我的 AI 助理", px, sy + 26, 24, "#6B6377", a, "black")
    ctx.restore()
    items = [("plane", "机票订好了", "周五 09:20 · 靠窗", 3.5, -1), ("bag", "比价完成", "帮你省 128 元", 4.5, 1),
             ("cal", "日程已安排", "周一 10:00 复盘会", 5.4, -1), ("pill", "该吃药了", "饭后 · 1 片", 6.4, 1)]
    for i, (ic, a1, a2, st, side) in enumerate(items):
        q = pop(t, st, 0.5)
        if q <= 0:
            continue
        cx = px + side * 400
        cy = 250 + (i // 2) * 300 + (i % 2) * 0
        with at(ctx, cx, cy, q):
            box_shadow(ctx, -170, -60, 340, 120, 24, blur=20, a=0.2, dy=8)
            rrect(ctx, -170, -60, 340, 120, 24)
            fill(ctx, "#FFFFFF", a)
            if ic == "pill":
                rrect(ctx, -140, -22, 60, 44, 22)
                fill(ctx, "#FF6B9A", a)
                rrect(ctx, -110, -22, 30, 44, 0)
                fill(ctx, "#FFFFFF", a)
            else:
                mini_icon(ctx, ic, -110, 0, 64, "#4C8DFF" if ic == "plane" else "#FF9F68")
            text(ctx, a1, -60, -18, 30, "#2B2233", a, "black", "l")
            text(ctx, a2, -60, 22, 22, "#7A7186", a, "bold", "l")
        # 连到手机
        line(ctx, px + side * 150, py - 100 + (i // 2) * 120, cx - side * 170, cy, 3, "#FF9F68", 0.5 * a * q)
    tag(ctx, "懂你的私人助理", px, 110, 32, "#FFFFFF", "#FF9F68", a * smooth(prog(t, 2.0, 2.4)))


def _part_b(ctx, t):
    a = smooth(prog(t, 8.9, 9.5)) * (1 - smooth(prog(t, 14.0, 14.6)))
    if a <= 0:
        return
    # 左：AI 老师
    lx = XB - 520
    rrect(ctx, lx - 300, 170, 600, 360, 20)
    fill(ctx, "#2F5D4E", a)
    rrect(ctx, lx - 300, 170, 600, 360, 20)
    ctx.set_line_width(14)
    setc(ctx, "#B07A50", a)
    ctx.stroke()
    n = int(clamp((t - 9.6) * 10, 0, 24))
    text(ctx, "x² + 2x + 1 = (x + 1)²"[:n], lx, 300, 40, "#FFFFFF", a, "bold")
    if t > 11.0:
        check_mark(ctx, lx + 200, 400, 70, "#7CFFB2", clamp((t - 11.0) / 0.4), a)
    tag(ctx, "一对一 AI 老师", lx, 120, 30, "#FFFFFF", "#2E9A55", a)
    draw_mascot(ctx, lx - 120, G, 0.38, "starry" if t > 11.0 else "curious", t, since=1.0, seed=3, hat="grad",
                look=(0.5, -0.8))
    # 右：AI 看影像
    rx = XB + 560
    rrect(ctx, rx - 260, 160, 520, 420, 24)
    fill(ctx, "#101520", a)
    # 简化的胸片
    for sd in (-1, 1):
        ellipse(ctx, rx + sd * 95, 360, 80, 150)
        ctx.set_source(rad(rx + sd * 95, 360, 10, 160, [(0, "#C9D6E8", 0.55 * a), (1, "#5A6A85", 0.2 * a)]))
        ctx.fill()
    for k in range(6):
        y = 250 + k * 40
        ctx.move_to(rx - 180, y)
        ctx.curve_to(rx - 60, y - 20, rx + 60, y - 20, rx + 180, y)
        ctx.set_line_width(5)
        setc(ctx, "#DCE6F5", 0.35 * a)
        ctx.stroke()
    sc = smooth(prog(t, 11.6, 12.2))
    if sc > 0:
        bx, by = rx + 110, 330
        rrect(ctx, bx - 46, by - 46, 92, 92, 10)
        ctx.set_line_width(5)
        setc(ctx, "#FFD36B", a * sc)
        ctx.stroke()
        tag(ctx, "AI：这里请再看看", bx, by - 80, 22, "#3A2A00", "#FFD36B", a * sc)
    tag(ctx, "AI 帮医生看影像", rx, 120, 30, "#FFFFFF", "#4C8DFF", a)


def _helix(ctx, x0, y0, w, t, p, a, color, amp=60, ph=0.0):
    pts = []
    n = 120
    for i in range(n + 1):
        u = i / n
        fold = smooth(p)
        xx = x0 + u * w
        yy = y0 + math.sin(u * TAU * 3 + ph + t * 0.8) * amp * (0.3 + 0.7 * fold)
        # 折叠：后半段绕回来
        if u > 0.5:
            v = (u - 0.5) * 2
            xx = lerp(xx, x0 + w * 0.5 - v * w * 0.3, fold)
            yy = lerp(yy, y0 + 160 + math.sin(v * TAU * 2 + ph) * amp * 0.8, fold)
        pts.append((xx, yy))
    stroke_pts(ctx, pts, 16, color, a)
    stroke_pts(ctx, pts, 6, "#FFFFFF", 0.35 * a)


def _part_c(ctx, t):
    a = smooth(prog(t, 14.0, 14.6)) * (1 - smooth(prog(t, 21.2, 21.8)))
    if a <= 0:
        return
    p = prog(t, 15.0, 17.6)
    glow(ctx, XC - 160, 400, 380, "#8B6CFF", 0.25 * a)
    _helix(ctx, XC - 560, 330, 800, t, p, a, "#8B6CFF", 60, 0.0)
    _helix(ctx, XC - 560, 360, 800, t, p, a * 0.9, "#2EC4B6", 45, 1.6)
    tag(ctx, "AI 预测蛋白质结构", XC - 160, 130, 32, "#FFFFFF", "#6A4FD8", a * smooth(prog(t, 14.6, 15.0)))
    m = pop(t, 18.0, 0.6)
    if m > 0:
        with at(ctx, XC + 520, 500, m):
            medal(ctx, 0, 0, 120, a, t, "诺奖")
        with at(ctx, XC + 520, 720, m):
            rrect(ctx, -250, -60, 500, 120, 30)
            fill(ctx, "#2B2233", 0.92 * a)
            text(ctx, "2024 诺贝尔化学奖", 0, -18, 32, "#FFD36B", a, "black")
            text(ctx, "AlphaFold 的研发者", 0, 26, 26, "#FFFFFF", a, "bold")
        sparkle_burst(ctx, t, 18.05, XC + 520, 500, 12, 260, "#FFE58A", 1.0, 5, 22)


def _part_d(ctx, t):
    a = smooth(prog(t, 21.2, 21.8))
    if a <= 0:
        return
    # 城市天际线逐层亮起：电 → 互联网 → AI
    R = rng(12)
    base = G
    for i in range(16):
        x = XD - 900 + i * 120
        h = R.uniform(160, 420)
        rrect(ctx, x, base - h, 100, h, 6)
        fill(ctx, "#4A4458", 0.9 * a)
        for r in range(int(h / 50)):
            for c in range(2):
                lit = R.random() < smooth(prog(t, 22.0 + i * 0.05, 23.0 + i * 0.05))
                rrect(ctx, x + 18 + c * 40, base - h + 20 + r * 50, 24, 26, 3)
                fill(ctx, "#FFE29A" if lit else "#2E2A3A", a)
    layers = [("电", "#FFC857", 22.0), ("互联网", "#4C8DFF", 22.9), ("AI", "#FF9F68", 23.8)]
    for i, (lab, c, st) in enumerate(layers):
        q = pop(t, st, 0.5)
        if q <= 0:
            continue
        y = 420 - i * 110
        with at(ctx, XD + 0, y, q):
            rrect(ctx, -330 + i * 40, -42, 660 - i * 80, 84, 42)
            fill(ctx, c, 0.92 * a)
            text(ctx, lab, 0, 0, 44, "#FFFFFF", a, "black")
        if i == 0:
            pylon(ctx, XD - 520, base, 300, a * q, "#9AA3B5")
            pylon(ctx, XD + 520, base, 300, a * q, "#9AA3B5")
    if t > 24.6:
        with at(ctx, XD, 90, pop(t, 24.6, 0.5)):
            rrect(ctx, -260, -48, 520, 96, 48)
            fill(ctx, "#2B2233", 0.92)
            text(ctx, "新基础设施", 0, 0, 48, "#FFD36B", 1, "black")


def draw(ctx, t):
    cam = CAM.at(t)
    _bg(ctx, t, cam)
    with view(ctx, cam, 1.0):
        _part_a(ctx, t)
        _part_b(ctx, t)
        _part_c(ctx, t)
        _part_d(ctx, t)
        P.draw(ctx, t)


def sfx():
    return [
        (0.0, "ambience_dawn", {"dur": 9.0, "gain": 0.35}),
        (1.6, "thud", {"gain": 0.2}),
        (3.5, "notify", {"gain": 0.3}), (4.5, "coin", {"gain": 0.3}), (5.4, "notify", {"gain": 0.3, "pitch": 1.12}),
        (6.4, "chime", {"gain": 0.3}),
        (8.5, "whoosh_short", {"gain": 0.3}),
        (9.6, "typing", {"dur": 1.4, "gain": 0.15}), (11.0, "check", {"gain": 0.3}),
        (11.6, "scan", {"dur": 0.8, "gain": 0.25}), (12.2, "ding", {"gain": 0.3}),
        (13.8, "whoosh_short", {"gain": 0.3}),
        (15.0, "stretch", {"dur": 2.4, "gain": 0.2}),
        (18.0, "success", {"gain": 0.4}), (18.05, "shimmer", {"dur": 1.4, "gain": 0.3}),
        (20.9, "whoosh_short", {"gain": 0.3}),
        (22.0, "powerup", {"gain": 0.3}), (22.9, "connect", {"gain": 0.3}), (23.8, "shimmer", {"dur": 1.2, "gain": 0.3}),
        (24.6, "impact_soft", {"gain": 0.4}),
    ]
