"""06 · AI 与你（上）：工作。程序员：过去一行行敲代码 → 现在描述需求、拆解任务、审查结果
（谷歌：超过三成新代码由 AI 生成）→ 办公室：周报 / 表格 / PPT / 邮件全流程 →
一个人带着一群智能体 = 一支队伍 → 会提问、会判断、会验收的人越来越值钱。"""
import math

from mascot import draw_mascot

from ..core import (TAU, Cam, at, box_shadow, circle, clamp, ease_back, ease_in, ease_io, ease_out, ease_out5,
                    fill, glow, lerp, lin, line, pop, prog, rad, ring_burst, rng, rrect, setc, smooth,
                    sparkle_burst, star4, stroke_pts, text, text_w, view, check_mark, arrow)
from ..props import bg_grad, doc_card, price_tag, tag
from ..ui import term_lines, window
from .common import host, mini_icon, talk_lines

DUR = 34.0
CHAPTER = ("06", "AI 与你")

VO = [
    (1.0, '说回我们自己。AI 最先改变的，是{程序员}。'),
    (5.7, '过去一行行敲代码，现在是描述需求、拆解任务、审查结果；谷歌就说，公司里超过三成的新代码已由 AI 生成。'),
    (16.0, '接着是{办公室}：周报、表格、PPT、邮件，智能体能跑完全流程。'),
    (22.6, '一个人，带着一群智能体，就是一支{队伍}。'),
    (26.7, '重复的活会越来越少，会{提问}、会{判断}、会{验收}的人，会越来越值钱。'),
]

G = 900
XA, XC, XE = 960, 3200, 5400

P = (host(XA - 300, G - 40, 0.62, "focused", seed=14.4)
     .look(0, 0.9, -0.3).type(0.3, 4.6).fx(2.6, ("sweat",)).fx(4.6, ())
     .expr(4.7, "tired")
     .move(5.2, 5.8, XA - 420, G).expr(6.6, "smile").look(6.6, 0.6, -0.6)
     .expr(9.0, "smug").front(9.2, "cross").front(12.6, None)
     .expr(12.8, "surprised").look(12.8, 1.0, -0.6).expr(13.8, "awe")
     .expr(15.2, "smile").run_to(15.3, 16.1, XC - 780, G)
     .expr(16.2, "curious").look(16.2, 0.9, -0.5)
     .expr(19.0, "happy").nod(20.4, 2)
     .expr(21.9, "determined").fx(21.9, ()).walk_to(22.2, 25.6, XC + 120, G)
     .expr(25.7, "proud").wave(25.8, 26.6, "r")
     .expr(26.4, "smile").run_to(26.7, 27.5, XE - 700, G)
     .expr(27.6, "curious").look(27.6, 0.9, -0.6)
     .expr(29.2, "excited").expr(31.0, "proud"))
talk_lines(P, VO, [0, 1, 3, 4], smile=0.35)

CAM = Cam([
    (0.0, (XA, 560, 1.12)),
    (5.0, (XA, 545, 1.0), ease_io),
    (15.1, (XA + 20, 545, 1.02)),
    (16.1, (XC, 540, 1.0), ease_io),
    (21.9, (XC + 20, 540, 1.0)),
    (25.6, (XC + 300, 560, 0.94), ease_io),
    (26.6, (XC + 360, 560, 0.94)),
    (27.5, (XE, 540, 1.0), ease_io),
    (34.0, (XE + 20, 530, 1.05)),
], drift=6, seed=29.0)


def _bg(ctx, t, cam):
    bg_grad(ctx, "#FFF3E2", "#FFD9C2", "#FFE9D2", 0.6)
    ctx.set_source(rad(1500, 100, 50, 1200, [(0, "#FFF6D8", 0.8), (1, "#FFF6D8", 0)]))
    ctx.paint()
    with view(ctx, cam, 1.0):
        ctx.rectangle(-1000, G, 8000, 400)
        ctx.set_source(lin(0, G, 0, G + 260, [(0, "#E9C9A8"), (1, "#D7AE88")]))
        ctx.fill()
        ctx.rectangle(-1000, G - 4, 8000, 8)
        fill(ctx, "#C99A72", 0.6)


def mini(ctx, x, y, s, t, seed, expr="focused", walk=None, carry=None, look=(0.3, -0.2)):
    """迷你 Claude：充当"智能体"的小帮手（头顶有一个小天线灯）。"""
    draw_mascot(ctx, x, y, s, expr, t, since=5, seed=seed, walk=walk, look=look,
                arm_l=0.9 if carry else 0.0, arm_r=0.9 if carry else 0.0, shadow=0.8)
    hy = y - 262 * s
    line(ctx, x, hy, x, hy - 60 * s, 6 * s, "#6B4436")
    k = 0.6 + 0.4 * math.sin(t * 6 + seed * 3)
    glow(ctx, x, hy - 64 * s, 40 * s, "#7CFFB2", 0.8 * k)
    circle(ctx, x, hy - 64 * s, 12 * s)
    fill(ctx, "#7CFFB2")
    if carry:
        carry(ctx, x, hy - 110 * s)


def _desk_front(ctx, t, a=1.0):
    """桌子（画在 Claude 前面，只挡住腿）+ 侧面一台背对我们的笔记本、一杯咖啡。"""
    if a <= 0:
        return
    x, y = XA - 300, G - 92
    rrect(ctx, x - 300, y, 600, 30, 10)
    ctx.set_source(lin(0, y, 0, y + 30, [(0, "#C48A5C", a), (1, "#9C6A44", a)]))
    ctx.fill()
    rrect(ctx, x - 280, y + 30, 560, 62, 6)
    fill(ctx, "#A8754C", a)
    rrect(ctx, x + 150, y - 96, 150, 96, 10)
    fill(ctx, "#C9C5D3", a)
    circle(ctx, x + 225, y - 48, 11)
    fill(ctx, "#FFFFFF", 0.7 * a)
    rrect(ctx, x - 260, y - 62, 56, 62, 12)
    fill(ctx, "#FFFFFF", a)
    rrect(ctx, x - 254, y - 46, 44, 14, 6)
    fill(ctx, "#E88E64", a)


def _part_a(ctx, t):
    a = 1 - smooth(prog(t, 5.4, 6.0))
    if a <= 0:
        return
    mx, my = XA + 360, 400
    cx, cy, cw, ch = window(ctx, mx - 360, my - 230, 720, 420, "app.py", a, "dark")
    lines = [(f"for i in range({k * 3 + 2}):", "#7CC6FF", 0.3 + k * 0.9) for k in range(5)]
    term_lines(ctx, lines, cx + 30, cy + 40, t, a, size=28, lh=58, cps=9)
    tag(ctx, "程序员的一天", mx, my - 285, 32, "#FFFFFF", "#8B6CFF", a * smooth(prog(t, 1.0, 1.4)))


def _part_b(ctx, t):
    a = smooth(prog(t, 5.6, 6.2)) * (1 - smooth(prog(t, 15.4, 16.0)))
    if a <= 0:
        return
    # 过去
    x0 = XA - 620
    box_shadow(ctx, x0 - 260, 150, 520, 520, 26, blur=22, a=0.18 * a, dy=8)
    rrect(ctx, x0 - 260, 150, 520, 520, 26)
    fill(ctx, "#FFFFFF", 0.95 * a)
    text(ctx, "过去", x0, 200, 40, "#7A7186", a, "black")
    n = int(clamp((t - 6.0) * 6, 0, 60))
    for i in range(min(9, n // 6 + 1)):
        w = 380 if i < n // 6 else (n % 6) * 60
        rrect(ctx, x0 - 200, 260 + i * 42, w, 16, 8)
        fill(ctx, "#C9C3D3", a)
    text(ctx, "一行行敲代码", x0, 640, 32, "#2B2233", a, "black")
    # 现在
    x1 = XA + 380
    box_shadow(ctx, x1 - 380, 150, 760, 520, 26, blur=22, a=0.18 * a, dy=8)
    rrect(ctx, x1 - 380, 150, 760, 520, 26)
    fill(ctx, "#FFFFFF", 0.95 * a)
    text(ctx, "现在", x1, 200, 40, "#FF9F68", a, "black")
    steps = [("描述需求", "#8B6CFF", 7.2), ("拆解任务", "#2EC4B6", 8.0), ("审查结果", "#FF9F68", 8.8)]
    for i, (lab, c, st) in enumerate(steps):
        q = pop(t, st, 0.45)
        if q > 0:
            with at(ctx, x1 - 240 + i * 240, 290, q):
                rrect(ctx, -105, -38, 210, 76, 38)
                fill(ctx, c, a)
                text(ctx, lab, 0, 0, 30, "#FFFFFF", a, "black")
            if i > 0:
                arrow(ctx, x1 - 240 + (i - 1) * 240 + 110, 290, x1 - 240 + i * 240 - 110, 290, 5, "#B9A68A", a * q)
    # 迷你智能体在干活
    if t > 8.2:
        for k in range(4):
            ph = (t * 0.35 + k / 4) % 1
            mxx = x1 - 300 + ph * 600
            q = smooth(prog(t, 8.2 + k * 0.2, 8.6 + k * 0.2))
            if q <= 0:
                continue
            def carry(ctx2, xx, yy, k=k):
                rrect(ctx2, xx - 26, yy - 16, 52, 32, 6)
                fill(ctx2, ["#7CC6FF", "#FFC857", "#7CFFB2", "#FF7AA2"][k], a)
            mini(ctx, mxx, 580, 0.24 * q, t, k + 1, "focused", walk=ph * 6, carry=carry)
    # 谷歌：三成新代码由 AI 生成
    g = pop(t, 12.8, 0.55)
    if g > 0:
        with at(ctx, x1 + 120, 780, g, -0.04):
            glow(ctx, 0, 0, 260, "#4285F4", 0.3)
            rrect(ctx, -330, -60, 660, 120, 60)
            fill(ctx, "#2B2233")
            text(ctx, "谷歌：超过三成新代码由 AI 生成", 0, -6, 34, "#FFD36B", 1, "black")
        text(ctx, "谷歌 CEO 皮查伊 · 2025 年财报电话会", x1 + 120, 865, 20, "#9A7A62", a * g, "bold")


OFFICE = [("doc", "周报", "#4C8DFF"), ("sheet", "表格", "#20A464"), ("slide", "PPT", "#F5A623"), ("mail", "邮件", "#E5484D")]


def _part_c(ctx, t):
    a = smooth(prog(t, 15.6, 16.2)) * (1 - smooth(prog(t, 26.4, 27.0)))
    if a <= 0:
        return
    # 传送带
    by = 640
    rrect(ctx, XC - 820, by, 1640, 40, 20)
    fill(ctx, "#6B6377", a)
    for i in range(20):
        x = XC - 820 + ((i * 90 + t * 120) % 1640)
        rrect(ctx, x, by + 10, 40, 20, 6)
        fill(ctx, "#8C8496", a)
    for i, (kind, title, c) in enumerate(OFFICE):
        st = 16.4 + i * 0.9
        u = clamp((t - st) / 3.2)
        if u <= 0:
            continue
        x = XC - 700 + ease_io(clamp(u)) * 1150 + i * 40
        p = clamp((u - 0.15) / 0.6)
        with at(ctx, x, by - 175, 1.0):
            doc_card(ctx, 0, 0, 240, 280, kind, a, p, title)
            if p >= 1:
                circle(ctx, 100, -120, 26)
                fill(ctx, "#3CCB7F", a)
                check_mark(ctx, 100, -120, 30, "#FFFFFF", clamp((u - 0.75) / 0.15), a)
        # 旁边的小智能体
        mini(ctx, x - 150, by - 4, 0.22, t, 10 + i, "focused", walk=t * 1.5 + i, look=(0.8, -0.3))
    # 完成托盘
    rrect(ctx, XC + 560, by - 70, 260, 110, 20)
    fill(ctx, "#3CCB7F", 0.9 * a)
    text(ctx, "全流程完成", XC + 690, by - 15, 32, "#FFFFFF", a, "black")
    tag(ctx, "智能体跑完全流程", XC, 170, 34, "#FFFFFF", "#FF9F68", a * smooth(prog(t, 19.4, 19.8)))


def _part_d(ctx, t):
    """一个人 + 一群智能体 = 一支队伍：Claude 走在前面，后面跟着一排迷你 Claude。"""
    a = smooth(prog(t, 22.2, 22.8)) * (1 - smooth(prog(t, 26.6, 27.2)))
    if a <= 0:
        return
    st = P.state(t)
    hx = st["x"]
    for k in range(7):
        row, col = divmod(k, 4)
        x = hx - 260 - col * 130 - row * 60
        y = G - row * 0
        mini(ctx, x, y - row * 20, 0.26, t, 20 + k, "determined" if k % 2 else "happy",
             walk=(t * 1.3 + k * 0.17) if st["walk"] is not None else None, look=(0.9, 0.0))
    k = pop(t, 24.2, 0.5)
    if k > 0:
        with at(ctx, XC + 360, 300, k):
            rrect(ctx, -380, -66, 760, 132, 66)
            fill(ctx, "#2B2233", 0.92)
            text(ctx, "一个人 + 一群智能体 = 一支队伍", 0, 0, 40, "#FFD36B", 1, "black")


def _part_e(ctx, t):
    a = smooth(prog(t, 27.0, 27.6))
    if a <= 0:
        return
    # 重复的活越来越少
    for i in range(6):
        k = 1 - smooth(prog(t, 27.6 + i * 0.15, 28.4 + i * 0.15))
        if k <= 0:
            continue
        with at(ctx, XE - 560 + (i % 3) * 120, 360 + (i // 3) * 130, k):
            rrect(ctx, -50, -50, 100, 100, 14)
            fill(ctx, "#B9B2C8", a)
            text(ctx, "重复", 0, 0, 26, "#FFFFFF", a, "black")
    if t > 27.6:
        tag(ctx, "重复的活越来越少", XE - 440, 620, 28, "#FFFFFF", "#6B6377", a * (1 - smooth(prog(t, 29.0, 29.6))))
    # 三种能力越来越值钱
    skills = [("会提问", "#8B6CFF", 28.6), ("会判断", "#2EC4B6", 29.4), ("会验收", "#FF9F68", 30.2)]
    for i, (lab, c, stt) in enumerate(skills):
        q = pop(t, stt, 0.5)
        if q <= 0:
            continue
        x = XE - 200 + i * 360
        rise = ease_out(prog(t, stt + 0.2, stt + 1.4))
        y = 560 - rise * 120
        with at(ctx, x, y, q):
            glow(ctx, 0, 0, 160, c, 0.35)
            circle(ctx, 0, 0, 110)
            fill(ctx, c, a)
            text(ctx, lab, 0, 0, 44, "#FFFFFF", a, "black")
        price_tag(ctx, x + 40, y + 160, 0.9, "价值上涨", "#FFC857", a * q, 0.08)


def draw(ctx, t):
    cam = CAM.at(t)
    _bg(ctx, t, cam)
    with view(ctx, cam, 1.0):
        _part_a(ctx, t)
        _part_b(ctx, t)
        _part_c(ctx, t)
        _part_d(ctx, t)
        _part_e(ctx, t)
        P.draw(ctx, t)
        _desk_front(ctx, t, 1 - smooth(prog(t, 5.0, 5.6)))


def sfx():
    return [
        (0.3, "typing", {"dur": 4.2, "gain": 0.3}),
        (4.7, "womp", {"gain": 0.25}),
        (6.0, "typing", {"dur": 1.6, "gain": 0.15}),
        (7.2, "pop", {"gain": 0.3}), (8.0, "pop", {"gain": 0.3, "pitch": 1.2}), (8.8, "pop", {"gain": 0.3, "pitch": 1.4}),
        (8.6, "shuffle", {"dur": 3.0, "gain": 0.15}),
        (12.8, "impact_soft", {"gain": 0.4}), (12.85, "shimmer", {"dur": 1.0, "gain": 0.3}),
        (15.3, "whoosh_short", {"gain": 0.3}),
        (16.2, "gears_run", {"dur": 5.8, "gain": 0.2}),
        (18.0, "check", {"gain": 0.25}), (18.9, "check", {"gain": 0.25, "pitch": 1.1}),
        (19.8, "check", {"gain": 0.25, "pitch": 1.2}), (20.7, "check", {"gain": 0.25, "pitch": 1.3}),
        (21.6, "success", {"gain": 0.35}),
        (22.4, "shuffle", {"dur": 3.0, "gain": 0.2}),
        (24.2, "pop_big", {"gain": 0.4}),
        (26.7, "whoosh_short", {"gain": 0.3}),
        (27.6, "womp", {"gain": 0.2}),
        (28.6, "rise", {"dur": 1.2, "gain": 0.25}), (29.4, "rise", {"dur": 1.2, "gain": 0.25, "pitch": 1.15}),
        (30.2, "rise", {"dur": 1.2, "gain": 0.25, "pitch": 1.3}),
        (31.0, "coin", {"gain": 0.35}),
    ]
