"""04 · 为什么是美国（中）：有耐心的钱 + 愿意付费的土壤。
Muse 先做好产品再赚钱 → J 曲线：投入期与收获期的时间错配 → 四大科技公司 2026 年资本开支约 7000 亿美元 →
付费的土壤 → ServiceNow、财捷两棵订阅大树 → AI 订阅 20 / 200 美元、企业按人头付费 → 商业飞轮。"""
import math

from ..core import (TAU, Cam, at, box_shadow, circle, clamp, ease_back, ease_in, ease_io, ease_out,
                    ease_out5, ellipse, fill, glow, lerp, lin, line, pop, prog, rad, ring_burst, rng, rrect,
                    setc, smooth, sparkle_burst, star4, stroke_pts, text, text_w, view, mix)
from ..charts import donut, flywheel, hbars, j_curve
from ..icons import ic_coin, ic_muse
from ..props import bg_grad, name_card, price_tag, tag
from .common import host, mini_icon, talk_lines

DUR = 49.0
CHAPTER = ("04", "为什么是美国")

VO = [
    (0.7, '第二，是{有耐心的钱}。'),
    (3.0, '扎克伯格做 Muse，先把产品做到让用户满意，再考虑怎么赚钱。'),
    (8.2, 'AI 的投入期和收获期之间，隔着好几年的{时间错配}：2026 年，美国四大科技巨头计划的资本开支，合计约 7000 亿美元。'),
    (19.0, '敢这么投，是因为美国早有一片{愿意付费}的土壤。'),
    (23.5, 'AI 之前，ServiceNow、财捷这样的软件公司就靠订阅跑通了商业模式：ServiceNow 一年收入 133 亿美元，97% 来自订阅。'),
    (34.6, '今天，美国用户每月花 20 美元、甚至 200 美元订阅 AI，企业按人头付费。'),
    (41.8, '收入养研发，研发出好产品，好产品又带来收入，{商业飞轮}就转起来了。'),
]

G = 880
XA, XC, XE, XF, XG = 960, 3100, 5500, 7900, 10000

P = (host(XA - 560, G, 0.6, "smile", seed=9.9)
     .look(0, 0.8, -0.7)
     .expr(0.8, "starry").hop(0.9, 40, 0.38)
     .expr(3.0, "smile").look(3.0, 0.9, -0.6).nod(5.6, 1)
     .expr(7.5, "smile").run_to(7.6, 8.5, XC - 780, G)
     .expr(8.6, "focused").look(8.6, 0.9, -0.5)
     .expr(10.6, "worried").fx(10.6, ("sweat",)).expr(12.4, "relieved").fx(12.4, ())
     .expr(13.8, "shock").startle(16.4).expr(17.3, "awe")
     .expr(18.4, "smile").run_to(18.5, 19.4, XE - 820, G)
     .expr(19.5, "happy").look(19.5, 0.8, 0.2)
     .expr(23.4, "curious").look(23.4, 0.9, -0.8)
     .expr(28.0, "awe").look(28.0, 0.8, -0.9)
     .expr(33.6, "smile").run_to(33.7, 34.6, XF - 760, G)
     .expr(34.7, "excited").look(34.7, 0.9, -0.6)
     .expr(41.0, "smile").run_to(41.1, 41.9, XG - 700, G)
     .expr(42.0, "grin").look(42.0, 0.9, -0.5).cheer(46.0, 47.4).expr(47.5, "proud"))
talk_lines(P, VO, [0, 1, 3, 5], smile=0.35)

CAM = Cam([
    (0.0, (XA, 520, 1.16)),
    (7.4, (XA + 20, 515, 1.1)),
    (8.4, (XC, 540, 1.0), ease_io),
    (18.3, (XC + 40, 540, 1.03)),
    (19.3, (XE, 600, 0.9), ease_io),
    (23.3, (XE + 20, 600, 0.92)),
    (24.4, (XE, 540, 1.0), ease_io),
    (33.4, (XE + 20, 540, 1.02)),
    (34.5, (XF, 540, 1.0), ease_io),
    (40.9, (XF + 30, 540, 1.02)),
    (41.9, (XG, 540, 1.0), ease_io),
    (49.0, (XG + 20, 530, 1.06)),
], drift=6, seed=19.0)


def _bg(ctx, t, cam):
    bg_grad(ctx, "#FFF4E2", "#FFE1C7", "#FFF0DA", 0.55)
    with view(ctx, cam, 0.5):
        R = rng(41)
        for i in range(40):
            x, y = R.uniform(-600, 11000), R.uniform(-200, 900)
            k = 0.5 + 0.5 * math.sin(t * 1.2 + i)
            star4(ctx, x, y, 8 + 6 * k, "#FFC857", 0.25 * k, t * 0.3 + i)
    with view(ctx, cam, 1.0):
        ctx.rectangle(-1000, G, 12500, 600)
        ctx.set_source(lin(0, G, 0, G + 500, [(0, "#B98B5E"), (0.12, "#8A5A3A"), (1, "#4E3220")]))
        ctx.fill()
        ctx.rectangle(-1000, G - 10, 12500, 22)
        fill(ctx, "#7DC46B")


def _part_ab(ctx, t):
    k = pop(t, 0.6, 0.55)
    if k > 0 and t < 8.6:
        with at(ctx, XA - 120, 300, k):
            glow(ctx, 0, 0, 220, "#FFC857", 0.45)
            ic_coin(ctx, 0, 0, 220, 1.0, t, 0.0)
            # 钟面
            circle(ctx, 70, 70, 54)
            fill(ctx, "#FFFFFF")
            circle(ctx, 70, 70, 54)
            ctx.set_line_width(6)
            setc(ctx, "#2B2233")
            ctx.stroke()
            for ang, L in ((t * 1.2, 34), (t * 0.12, 24)):
                line(ctx, 70, 70, 70 + math.sin(ang) * L, 70 - math.cos(ang) * L, 6, "#2B2233")
        tag(ctx, "有耐心的钱", XA - 120, 470, 34, "#FFFFFF", "#E0A42B", k)
    # Muse：先让用户满意，再考虑赚钱
    a = smooth(prog(t, 2.8, 3.4))
    if a <= 0:
        return
    mx, my = XA + 420, 380
    glow(ctx, mx, my, 220, "#8B6CFF", 0.3 * a)
    ic_muse(ctx, mx, my, 170, a, t)
    steps = [("① 产品好用", "#8B6CFF", 3.6), ("② 用户满意", "#FF6B9A", 4.6), ("③ 再考虑赚钱", "#E0A42B", 6.2)]
    for i, (lab, c, st) in enumerate(steps):
        q = pop(t, st, 0.45)
        if q > 0:
            with at(ctx, mx - 330 + i * 330, my + 280, q):
                rrect(ctx, -140, -40, 280, 80, 40)
                fill(ctx, c, a)
                text(ctx, lab, 0, 0, 32, "#FFFFFF", a, "black")
            if i > 0:
                from ..core import arrow
                arrow(ctx, mx - 330 + (i - 1) * 330 + 150, my + 280, mx - 330 + i * 330 - 150, my + 280, 5,
                      "#B9A68A", a * q)
    # 用户的爱心
    if t > 4.6:
        R = rng(5)
        for i in range(10):
            ph = ((t - 4.6) * 0.5 + i / 10) % 1
            ang = R.uniform(0, TAU)
            x = mx + math.cos(ang) * (110 + ph * 160)
            y = my + math.sin(ang) * (90 + ph * 120) - ph * 60
            from mascot.gfx import heart
            heart(ctx, x, y, 14 + 6 * R.random(), "#FF6B9A", (1 - ph) * a)
    if t > 6.2:
        tag(ctx, "变现可以慢一点", mx + 330, my + 360, 26, "#7A5A12", "#FFE9B0", smooth(prog(t, 6.4, 6.8)))


CAPEX = [("亚马逊", 2000, "#FF9900", "≈2000 亿"), ("微软", 1900, "#00A4EF", "≈1900 亿"),
         ("谷歌母公司", 1850, "#4285F4", "≈1850 亿"), ("Meta", 1350, "#0866FF", "≈1350 亿")]


def _part_c(ctx, t):
    a = smooth(prog(t, 7.6, 8.2))
    if a <= 0:
        return
    jx, jy, jw, jh = XC - 560, 430, 520, 520
    shrink = smooth(prog(t, 13.4, 14.2))
    with at(ctx, lerp(XC - 300, XC - 560, shrink), lerp(470, 420, shrink), lerp(1.25, 0.85, shrink)):
        j_curve(ctx, -jw / 2, 0, jw, jh, prog(t, 8.2, 12.2), a, "#FF9F68", 0.62)
        q1 = smooth(prog(t, 9.2, 9.6))
        text(ctx, "投入期", -jw / 2 + 120, 150, 32, "#C42A30", a * q1, "black")
        q2 = smooth(prog(t, 11.2, 11.6))
        text(ctx, "收获期", jw / 2 - 90, -200, 32, "#2E9A55", a * q2, "black")
        ctx.save()
        ctx.set_dash((10, 8))
        line(ctx, -jw / 2 + jw * 0.6, -240, -jw / 2 + jw * 0.6, 240, 3, "#2B2233", 0.4 * a * q2)
        ctx.restore()
        text(ctx, "时间 →", jw / 2 - 30, 30, 24, "#7A6A5E", a * q1, "bold")
        k = pop(t, 12.4, 0.5)
        if k > 0:
            with at(ctx, -jw / 2 + jw * 0.3, -150, k, -0.06):
                rrect(ctx, -130, -36, 260, 72, 36)
                fill(ctx, "#2B2233")
                text(ctx, "时间错配", 0, 0, 36, "#FFD36B", 1, "black")
    # 2026 资本开支
    b = smooth(prog(t, 13.8, 14.4))
    if b > 0:
        x0, y0 = XC - 120, 190
        rrect(ctx, x0 - 30, y0 - 40, 760, 500, 30)
        fill(ctx, "#FFFFFF", 0.9 * b)
        text(ctx, "2026 年资本开支计划（美元）", x0 + 350, y0 + 10, 30, "#2B2233", b, "black")
        hbars(ctx, CAPEX, x0, y0 + 90, 640, 84, prog(t, 14.4, 16.4), b, 28, vmax=2100, label_w=200, stagger=0.15)
        k = pop(t, 16.4, 0.5)
        if k > 0:
            with at(ctx, x0 + 350, y0 + 470, k):
                glow(ctx, 0, 0, 220, "#FFC857", 0.4)
                rrect(ctx, -250, -46, 500, 92, 46)
                fill(ctx, "#E0A42B")
                text(ctx, "合计 ≈ 7000 亿美元", 0, 0, 40, "#FFFFFF", 1, "black")
        text(ctx, "数据：各公司 2026 年 4 月财报指引", x0 + 350, y0 + 540, 20, "#9A8A7E", b * 0.9, "bold")


def _tree(ctx, x, y, h, g, c_leaf, a, t, seed=0):
    """订阅之树：树干 + 一团团树冠；g 为生长进度。"""
    if g <= 0:
        return
    th = h * ease_out(clamp(g * 1.4))
    rrect(ctx, x - 22, y - th, 44, th, 14)
    ctx.set_source(lin(x - 22, 0, x + 22, 0, [(0, "#8A5A3A", a), (1, "#6B4430", a)]))
    ctx.fill()
    cg = ease_back(clamp((g - 0.35) / 0.65), 1.4)
    if cg > 0:
        R = rng(seed)
        for i in range(7):
            ang = -math.pi / 2 + (i - 3) * 0.45
            r = h * 0.28 * cg * R.uniform(0.75, 1.05)
            cx = x + math.cos(ang) * h * 0.22 * cg
            cy = y - th - h * 0.05 + math.sin(ang) * h * 0.16 * cg
            circle(ctx, cx, cy, r)
            fill(ctx, mix(c_leaf, "#FFFFFF", 0.08 * (i % 3)), a)
        # 果实：一个个订阅月费
        for i in range(8):
            ph = (t * 0.35 + i / 8) % 1
            fx_ = x + math.cos(i * 1.7) * h * 0.3 * cg
            fy = y - th - h * 0.08 + math.sin(i * 2.3) * h * 0.18 * cg
            ic_coin(ctx, fx_, fy, 34 * cg, a * (0.6 + 0.4 * math.sin(ph * math.pi)), t, 0.0)


def _part_de(ctx, t):
    a = smooth(prog(t, 18.6, 19.3))
    if a <= 0:
        return
    # 土壤剖面
    sx0, sx1 = XE - 900, XE + 980
    rich = smooth(prog(t, 19.6, 20.6))
    ctx.rectangle(sx0, G + 10, sx1 - sx0, 230)
    ctx.set_source(lin(0, G, 0, G + 240, [(0, mix("#8A5A3A", "#5C3A22", rich), a), (1, "#3E2615", a)]))
    ctx.fill()
    R = rng(8)
    for i in range(60):
        x, y = R.uniform(sx0, sx1), R.uniform(G + 30, G + 220)
        circle(ctx, x, y, R.uniform(3, 7))
        fill(ctx, "#FFD36B" if R.random() < 0.3 * rich else "#6B4430", 0.7 * a)
    # 付费的"雨"：硬币落进土里，幼苗冒出来
    for i in range(14):
        st = 19.8 + i * 0.22
        u = clamp((t - st) / 0.9)
        if 0 < u < 1:
            x = XE - 700 + (i * 137) % 1500
            ic_coin(ctx, x, lerp(-60, G + 40, ease_in(u)), 46, a * (1 - smooth((u - 0.85) / 0.15)), t, u * 2)
    for i in range(7):
        g = ease_back(clamp((t - 20.8 - i * 0.25) / 0.6), 1.6) * (1 - smooth(prog(t, 23.4, 23.9)))
        if g > 0:
            x = XE - 620 + i * 210
            line(ctx, x, G, x, G - 46 * g, 6, "#3CCB7F", a)
            for sd in (-1, 1):
                ctx.save()
                ctx.translate(x, G - 40 * g)
                ctx.rotate(sd * 0.7)
                ctx.scale(g, g)
                ellipse(ctx, sd * 16, 0, 18, 9)
                fill(ctx, "#5ED37A", a)
                ctx.restore()
    tg = smooth(prog(t, 20.2, 20.6)) * (1 - smooth(prog(t, 23.2, 23.7)))
    if tg > 0:
        with at(ctx, XE + 40, G + 70, 1):
            rrect(ctx, -170, -40, 340, 80, 40)
            fill(ctx, "#FFD36B", tg * a)
            text(ctx, "愿意付费的土壤", 0, 0, 34, "#5C3A22", tg * a, "black")
    # 两棵大树
    g1 = prog(t, 23.6, 26.0)
    g2 = prog(t, 24.6, 27.0)
    _tree(ctx, XE - 420, G, 560, g1, "#3CCB7F", a, t, 1)
    _tree(ctx, XE + 380, G, 520, g2, "#2EB67D", a, t, 2)
    if g1 > 0.5:
        name_card(ctx, "ServiceNow", XE - 420, 120, "#62D84E", 34, a, pop(t, 25.0, 0.5), sub="企业 IT 流程软件")
    if g2 > 0.5:
        name_card(ctx, "财捷 Intuit", XE + 380, 160, "#236CFF", 34, a, pop(t, 26.0, 0.5), sub="报税 · 记账软件")
    # 数字
    n = smooth(prog(t, 28.4, 28.9))
    if n > 0:
        bx, by = XE - 420, 500
        with at(ctx, bx - 340, by, n):
            rrect(ctx, -170, -120, 340, 240, 28)
            fill(ctx, "#FFFFFF", 0.95)
            text(ctx, "年收入", 0, -80, 26, "#7A7186", 1, "bold")
            text(ctx, "133 亿美元", 0, -30, 46, "#2B2233", 1, "black")
            donut(ctx, -80, 60, 46, [(0.97, "#3CCB7F"), (0.03, "#D9D2E6")], prog(t, 29.8, 31.4), 1.0, 20)
            text(ctx, "97%", 22, 50, 40, "#2E9A55", 1, "black", "l")
            text(ctx, "来自订阅", 24, 90, 22, "#7A7186", 1, "bold", "l")
        tag(ctx, "2025 年报", bx - 340, by + 150, 22, "#FFFFFF", "#4A4458", n)
    m = smooth(prog(t, 31.2, 31.7))
    if m > 0:
        with at(ctx, XE + 380 + 330, 520, m):
            rrect(ctx, -160, -80, 320, 160, 28)
            fill(ctx, "#FFFFFF", 0.95)
            text(ctx, "年收入", 0, -40, 26, "#7A7186", 1, "bold")
            text(ctx, "214 亿美元", 0, 12, 44, "#2B2233", 1, "black")
            text(ctx, "2026 财年", 0, 54, 22, "#7A7186", 1, "bold")


def _part_f(ctx, t):
    a = smooth(prog(t, 34.2, 34.8))
    if a <= 0:
        return
    for i, (lab, sub, c, st) in enumerate((("$20 / 月", "个人订阅", "#FFC857", 35.6), ("$200 / 月", "专业版订阅", "#FF9F68", 37.0))):
        q = pop(t, st, 0.55)
        if q > 0:
            with at(ctx, XF - 360 + i * 20, 260 + i * 200, q):
                price_tag(ctx, 0, 0, 1.5, lab, c, a, -0.1 + i * 0.12)
            text(ctx, sub, XF - 360 + i * 20, 260 + i * 200 + 90, 26, "#5C3A22", a * q, "black")
    # 企业按人头付费：一排排座位
    b = smooth(prog(t, 38.4, 38.8))
    if b > 0:
        x0, y0 = XF + 120, 200
        rrect(ctx, x0 - 40, y0 - 60, 620, 520, 30)
        fill(ctx, "#FFFFFF", 0.9 * b)
        text(ctx, "企业：按人头付费", x0 + 270, y0 - 10, 32, "#2B2233", b, "black")
        for i in range(24):
            q = pop(t, 38.8 + i * 0.06, 0.35)
            if q <= 0:
                continue
            cx, cy = x0 + 40 + (i % 6) * 92, y0 + 80 + (i // 6) * 96
            with at(ctx, cx, cy, q * 0.9):
                circle(ctx, 0, -18, 18)
                fill(ctx, "#8B6CFF")
                rrect(ctx, -26, 4, 52, 34, 14)
                fill(ctx, "#8B6CFF")
                circle(ctx, 22, -26, 12)
                fill(ctx, "#3CCB7F")
                text(ctx, "$", 22, -26, 16, "#FFFFFF", 1, "black")


def _part_g(ctx, t):
    a = smooth(prog(t, 41.4, 42.0))
    if a <= 0:
        return
    sp = 0.4 + 2.6 * smooth(prog(t, 44.5, 47.5))
    rot = (t - 41.4) * sp
    lit = [clamp((t - 42.0) / 0.6), clamp((t - 43.2) / 0.6), clamp((t - 44.6) / 0.6)]
    flywheel(ctx, XG + 180, 470, 330, ["收入", "研发", "好产品"], rot, ["#E0A42B", "#8B6CFF", "#3CCB7F"], a, lit,
             40, center="商业飞轮", thick=120)
    if t > 45.5:
        for i in range(6):
            ang = rot + i * TAU / 6
            sparkle_burst(ctx, t, 45.5 + i * 0.2, XG + 180 + math.cos(ang) * 400, 470 + math.sin(ang) * 400, 4,
                          60, "#FFD36B", 0.6, i, 14)


def draw(ctx, t):
    cam = CAM.at(t)
    _bg(ctx, t, cam)
    with view(ctx, cam, 1.0):
        _part_ab(ctx, t)
        _part_c(ctx, t)
        _part_de(ctx, t)
        _part_f(ctx, t)
        _part_g(ctx, t)
        P.draw(ctx, t)


def sfx():
    return [
        (0.6, "coin", {"gain": 0.4}), (0.9, "sparkle", {"dur": 1.0, "gain": 0.25}),
        (3.6, "pop", {"gain": 0.3}), (4.6, "pop", {"gain": 0.3, "pitch": 1.2}), (4.7, "wink", {"gain": 0.25}),
        (6.2, "pop", {"gain": 0.3, "pitch": 1.4}), (6.3, "coin", {"gain": 0.25}),
        (7.6, "whoosh_short", {"gain": 0.3}),
        (8.6, "fall", {"dur": 1.2, "gain": 0.25}), (10.6, "rise", {"dur": 1.6, "gain": 0.25}),
        (12.4, "stamp", {"gain": 0.4}),
        (14.4, "rise", {"dur": 0.6, "gain": 0.22}), (14.7, "rise", {"dur": 0.6, "gain": 0.22, "pitch": 1.1}),
        (15.0, "rise", {"dur": 0.6, "gain": 0.22, "pitch": 1.2}), (15.3, "rise", {"dur": 0.6, "gain": 0.22, "pitch": 1.3}),
        (16.4, "impact_soft", {"gain": 0.45}), (16.45, "coin", {"gain": 0.3}),
        (18.5, "whoosh_short", {"gain": 0.3}),
        (19.6, "rumble", {"dur": 0.8, "gain": 0.25}),
        (23.6, "grow", {"dur": 2.6, "gain": 0.3}), (24.6, "grow", {"dur": 2.6, "gain": 0.25}),
        (25.0, "pop", {"gain": 0.3}), (26.0, "pop", {"gain": 0.3, "pitch": 1.2}),
        (28.4, "pop", {"gain": 0.3}), (29.8, "rise", {"dur": 1.4, "gain": 0.22}), (31.2, "pop", {"gain": 0.3}),
        (33.7, "whoosh_short", {"gain": 0.3}),
        (35.6, "coin", {"gain": 0.35}), (37.0, "coin", {"gain": 0.35, "pitch": 1.2}),
        (38.8, "shuffle", {"dur": 1.4, "gain": 0.2}),
        (41.1, "whoosh_short", {"gain": 0.3}),
        (42.0, "gear", {"gain": 0.3}), (43.2, "gear", {"gain": 0.3}), (44.6, "gear", {"gain": 0.3}),
        (44.6, "spinup", {"dur": 3.0, "gain": 0.3}), (46.0, "success", {"gain": 0.35}),
    ]
