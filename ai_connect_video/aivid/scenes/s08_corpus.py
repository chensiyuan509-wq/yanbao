"""第四章 · 语料：模型的粮食。

A 餐桌：吃下书籍 / 论文 / 代码，"聪明度"上涨；推开垃圾广告
B 英文互联网是一座敞开大门的粮仓
C 公开网页语料（Common Crawl）语言占比：英文 46%，中文不到 6%
D 中文网民约占全球五分之一，内容却锁在一个个 App 里
"""
import math

from ..core import (TAU, W, H, Cam, at, circle, clamp, ease_back, ease_in, ease_io, ease_out,
                    fill, glow, kf, lerp, line, lin, pop, poly, prog, rad, rng, rrect, setc, smooth,
                    text, text_w, view, sparkle_burst, ring_burst, bezier_pts, point_on, stroke_pts,
                    light_rays)
from ..icons import (ic_book, ic_code, ic_github, ic_junk, ic_lock, ic_paper, ic_qa, ic_reddit,
                     ic_wiki)
from ..mascot import Puppet
from ..ui import card, pill, progress
from .common import light_bg

DUR = 25.0
CHAPTER = ("04", "语料：模型的粮食")

SUBS = [
    (0.8, 5.8, "模型是「吃」数据长大的：{吃得好}，才长得聪明。"),
    (6.0, 12.0, "英文互联网是一座开放的大粮仓：维基百科、GitHub、论文、问答社区……"),
    (12.2, 18.2, "最常用的公开网页语料里，{英文接近一半}，中文不到 6%。"),
    (18.4, 24.6, "而中文网民约占全球{五分之一}，大量好内容锁在一个个 App 里。"),
]

AX, BX, CX, DX = 960, 2900, 4700, 6500
TABLE_Y = 742
FOODS = [(ic_book, 760, 1.25), (ic_paper, 960, 2.05), (ic_code, 1160, 2.85)]
T_JUNK, T_PUSH = 4.15, 4.85

P = (Puppet(AX, 800, 0.82, "happy", seed=8.8)
     .look(0, 0, 0.6)
     .expr(1.2, "surprised").expr(1.65, "happy").look(1.2, -0.4, 0.8)
     .expr(2.0, "surprised").expr(2.45, "happy").look(2.0, 0.0, 0.8)
     .expr(2.8, "surprised").expr(3.25, "happy").look(2.8, 0.4, 0.8)
     .expr(3.7, "proud").fx(3.7, ("sparkle",))
     .fx(4.2, None).expr(4.3, "tired").look(4.3, 1.0, 0.5)
     .arm(4.75, "r", 0.5, 0.25).ext(4.75, "r", 50, 0.2).arm(5.2, "r", 0.0, 0.4).ext(5.2, "r", 0, 0.4)
     .expr(5.3, "smile")
     .move(5.95, 6.85, 2170, 905, walk=False).hop(5.95, 160, 0.9).scale(5.95, 0.6, 0.9).land(6.85)
     .expr(6.9, "surprised").look(6.9, 1.0, -0.8).expr(7.8, "excited")
     .move(11.95, 12.75, 3930, 905, walk=False).hop(11.95, 160, 0.8).land(12.75)
     .expr(12.8, "curious").look(12.8, 1.0, -0.5).expr(14.3, "surprised").expr(15.5, "shock")
     .expr(16.6, "worried")
     .move(18.15, 18.95, 5780, 905, walk=False).hop(18.15, 160, 0.8).land(18.95)
     .expr(19.0, "curious").look(19.0, -1.0, -0.6)
     .look(20.4, 1.0, -0.4)
     .move(21.0, 21.9, 6470, 905).expr(21.9, "determined").look(21.9, 1.0, -0.6)
     .arm(22.0, "r", 0.85, 0.25).ext(22.0, "r", 55, 0.25).strain(22.2, 23.0, "r")
     .arm(23.1, "r", 0.0, 0.35).ext(23.1, "r", 0, 0.3)
     .expr(23.2, "tired").fx(23.2, ("sweat",)).look(23.2, 0.0, 0.0))

CAM = Cam([
    (0.0, (AX + 60, 545, 1.16)), (5.6, (AX + 70, 540, 1.2)),
    (6.8, (BX, 520, 1.0), ease_io), (11.8, (BX + 30, 520, 1.03)),
    (12.6, (CX, 520, 1.0), ease_io), (18.0, (CX + 30, 520, 1.03)),
    (18.8, (DX, 520, 1.0), ease_io), (25.0, (DX + 30, 520, 1.03)),
], drift=5, seed=19.0)


def draw(ctx, t):
    light_bg(ctx, "#FFF6E6", "#F5DCC0", dots="#D2A57C", dot_a=0.14, spacing=64, drift=(-t * 10, 0))
    cam = CAM.at(t)
    with view(ctx, cam, 0.45):
        for gx in (AX, BX * 0.45 + 900, CX * 0.45 + 800, DX * 0.45 + 700):
            glow(ctx, gx, 420, 650, "#FFFFFF", 0.45)
    with view(ctx, cam):
        lo, hi = cam[0] - 1500, cam[0] + 1500
        if lo < AX < hi:
            dining_back(ctx, t)
        if lo < BX < hi:
            granary(ctx, t)
        if lo < CX < hi:
            chart(ctx, t)
        if lo < DX < hi:
            apps(ctx, t)
        P.draw(ctx, t)
        if lo < AX < hi:
            dining_front(ctx, t)


# ---------------------------------------------------------------- A 餐桌

def dining_back(ctx, t):
    # 聪明度表
    bites = sum(1 for (_, _, t0) in FOODS if t > t0 + 0.45)
    lvl = kf(t, [(0, 0.25)] + [(FOODS[i][2] + 0.45 + 0.3, 0.25 + 0.22 * (i + 1)) for i in range(3)], ease_back)
    mx, my = 1350, 330
    ma = smooth(prog(t, 0.6, 1.0))
    if ma > 0:
        card(ctx, mx - 60, my - 170, 120, 380, 30, "#FFFFFF", ma, shadow=0.15)
        rrect(ctx, mx - 22, my - 140, 44, 300, 22)
        fill(ctx, "#F1E6DA", ma)
        h = 300 * clamp(lvl)
        rrect(ctx, mx - 22, my + 160 - h, 44, h, 22)
        ctx.set_source(lin(0, my + 160 - h, 0, my + 160, [(0, "#FFC65C", ma), (1, "#FF7A59", ma)]))
        ctx.fill()
        text(ctx, "聪明度", mx, my + 240, 30, "#7A5C48", ma, "black")
        for i in range(3):
            sparkle_burst(ctx, t, FOODS[i][2] + 0.75, mx, my + 160 - 300 * (0.25 + 0.22 * (i + 1)), 6, 80, "#FFC65C", 0.6, i + 9, 14)
    la = smooth(prog(t, 0.5, 0.9)) * (1 - smooth(prog(t, 3.6, 4.0)))
    if la > 0:
        pill(ctx, "优质语料：书籍 · 论文 · 代码", AX, 285, 34, "#FFFFFF", "#3CB371", la, 1.0)


def dining_front(ctx, t):
    # 桌子
    rrect(ctx, 470, TABLE_Y, 980, 46, 20)
    ctx.set_source(lin(0, TABLE_Y, 0, TABLE_Y + 46, [(0, "#C98B5E"), (1, "#A86E46")]))
    ctx.fill()
    rrect(ctx, 470, TABLE_Y, 980, 12, 6)
    fill(ctx, "#E2A97C")
    for lx in (540, 1360):
        rrect(ctx, lx, TABLE_Y + 40, 26, 160, 8)
        fill(ctx, "#9A6240")
    # 盘子与食物
    for i, (ic, x, t0) in enumerate(FOODS):
        pk = ease_out(prog(t, 0.2 + i * 0.15, 0.7 + i * 0.15))
        if pk <= 0:
            continue
        px = lerp(1700, x, pk)
        _plate(ctx, px, TABLE_Y + 2)
        u = prog(t, t0, t0 + 0.45)
        if u < 1:
            fx = lerp(px, AX, ease_in(u))
            fy = lerp(TABLE_Y - 50, 800 - 100, ease_in(u)) - math.sin(u * math.pi) * 120
            ic(ctx, fx, fy, 110 * (1 - 0.6 * ease_in(u)), 1.0, t)
        # 咬一口的碎屑
        for k in range(6):
            cu = prog(t, t0 + 0.45, t0 + 1.1)
            if 0 < cu < 1:
                ang = -math.pi / 2 + (k - 2.5) * 0.45
                cx = AX + math.cos(ang) * 90 * cu
                cy = 700 + math.sin(ang) * 60 * cu + 160 * cu * cu
                circle(ctx, cx, cy, 6 * (1 - cu))
                fill(ctx, ["#FFC65C", "#8B6CFF", "#FF9F68"][k % 3], 1 - cu)
    # 垃圾信息盘
    jk = ease_out(prog(t, T_JUNK, T_JUNK + 0.5))
    if jk > 0:
        out = ease_in(prog(t, T_PUSH, T_PUSH + 0.6))
        jx = lerp(1750, 1250, jk) + out * 700
        ja = 1 - out
        _plate(ctx, jx, TABLE_Y + 2, ja)
        ic_junk(ctx, jx, TABLE_Y - 48, 110, ja, t)
        pill(ctx, "垃圾信息", jx, TABLE_Y - 150, 30, "#FFFFFF", "#8D8894", ja * smooth(prog(t, T_JUNK + 0.2, T_JUNK + 0.5)), 1.0)
        if out == 0 and t > T_JUNK + 0.4:
            from ..core import cross_mark
            cross_mark(ctx, jx + 60, TABLE_Y - 100, 50, "#E5484D", prog(t, T_JUNK + 0.4, T_JUNK + 0.7))


def _plate(ctx, x, y, a=1.0):
    from ..core import ellipse
    ellipse(ctx, x, y, 92, 18)
    fill(ctx, "#FFFFFF", a)
    ellipse(ctx, x, y - 2, 70, 12)
    fill(ctx, "#F1ECE6", a)


# ---------------------------------------------------------------- B 粮仓

CRATES = [(ic_wiki, "维基百科"), (ic_github, "GitHub 代码"), (ic_paper, "arXiv 论文"),
          (ic_qa, "问答社区"), (ic_reddit, "Reddit 讨论"), (ic_book, "书籍 · 新闻")]


def granary(ctx, t):
    x0, y0 = BX, 520
    w, h = 1180, 560
    a = smooth(prog(t, 5.6, 6.4))
    if a <= 0:
        return
    # 光芒
    light_rays(ctx, x0, y0 + 40, 14, 900, "#FFE7B3", 0.25 * a, t * 0.05, 0.14)
    # 屋身
    box = (x0 - w / 2, y0 - h / 2 + 60, w, h - 60)
    rrect(ctx, *box, 30)
    ctx.set_source(lin(0, box[1], 0, box[1] + box[3], [(0, "#FFF8EE", a), (1, "#F6E2C8", a)]))
    ctx.fill()
    # 屋顶
    poly(ctx, [(x0 - w / 2 - 50, y0 - h / 2 + 80), (x0, y0 - h / 2 - 120), (x0 + w / 2 + 50, y0 - h / 2 + 80)])
    ctx.set_source(lin(0, y0 - h / 2 - 120, 0, y0 - h / 2 + 80, [(0, "#E07A4F", a), (1, "#C25E3A", a)]))
    ctx.fill()
    text(ctx, "英文互联网", x0, y0 - h / 2 - 6, 54, "#FFFFFF", a, "black")
    # 敞开的门（左右门扇）
    dk = ease_out(prog(t, 6.2, 7.0))
    for sgn in (-1, 1):
        dx = x0 + sgn * (w / 2 + 10)
        poly(ctx, [(dx, box[1] + 30), (dx + sgn * 120 * dk, box[1] + 70), (dx + sgn * 120 * dk, box[1] + box[3] - 10), (dx, box[1] + box[3])])
        fill(ctx, "#D9A177", a)
    # 货架与箱子
    for i, (ic, lab) in enumerate(CRATES):
        k = pop(t, 6.7 + i * 0.32, 0.45)
        if k <= 0:
            continue
        cx = x0 - 380 + (i % 3) * 380
        cy = y0 + 20 + (i // 3) * 200
        with at(ctx, cx, cy, k):
            rrect(ctx, -160, -70, 320, 150, 24)
            fill(ctx, "#FFFFFF", a)
            ic(ctx, -90, 4, 96, a, t)
            text(ctx, lab, 40, 4, 30, "#5A4335", a, "black")
    # 往外流动的数据
    fa = smooth(prog(t, 8.5, 9.2)) * a
    if fa > 0:
        R = rng(7)
        for k in range(26):
            ph = (t * 0.45 + k / 26) % 1
            sx, sy = x0 + R.uniform(-400, 400), y0 + R.uniform(-60, 220)
            ex, ey = x0 + R.uniform(-1300, 1300), y0 + R.uniform(-500, 500)
            px, py = lerp(sx, ex, ph), lerp(sy, ey, ph)
            glow(ctx, px, py, 18, ["#FFC65C", "#7CC6FF", "#B6A4FF"][k % 3], fa * math.sin(ph * math.pi))
    tk = pop(t, 9.2, 0.45)
    if tk > 0:
        with at(ctx, x0, y0 + 330, tk):
            pill(ctx, "公开 · 可链接 · 可授权", 0, 0, 34, "#FFFFFF", "#E07A4F", a, 1.0)


# ---------------------------------------------------------------- C 语言占比

LANGS = [("英文", 46, "46%"), ("德语", 5.6, "< 6%"), ("俄语", 5.6, "< 6%"), ("日语", 5.4, "< 6%"),
         ("法语", 5.0, "< 6%"), ("中文", 4.9, "< 6%")]


def chart(ctx, t):
    x0, y0 = CX + 80, 470
    w, h = 1240, 680
    a = smooth(prog(t, 12.1, 12.8))
    if a <= 0:
        return
    k = ease_back(prog(t, 12.1, 12.8), 1.2)
    with at(ctx, x0, y0, 0.9 + 0.1 * k):
        card(ctx, -w / 2, -h / 2, w, h, 40, "#FFFFFF", a, shadow=0.2)
        text(ctx, "公开网页语料（Common Crawl）里的语言占比", 0, -h / 2 + 66, 40, "#2B2233", a, "black")
        text(ctx, "数据来源：Common Crawl，2023 年 3 月抓取", 0, h / 2 - 40, 24, "#9A8F86", a, "medium")
        bx0, bwmax = -w / 2 + 210, 820
        for i, (lab, v, s) in enumerate(LANGS):
            ry = -h / 2 + 160 + i * 78
            q = ease_out(prog(t, 12.8 + i * 0.22, 13.8 + i * 0.22))
            hl = lab == "中文" and t > 14.6
            en = lab == "英文"
            col = "#FF7A59" if en else ("#E5484D" if hl else "#C9BDB2")
            text(ctx, lab, bx0 - 40, ry, 36, "#E5484D" if hl else "#2B2233", a, "black", "r")
            rrect(ctx, bx0, ry - 22, bwmax, 44, 22)
            fill(ctx, "#F4EEE8", a)
            bw = bwmax * v / 50 * q
            if bw > 1:
                rrect(ctx, bx0, ry - 22, max(44, bw), 44, 22)
                fill(ctx, col, a)
            lab_v = f"{v * q:.0f}%" if en else s
            text(ctx, lab_v, bx0 + max(44, bw) + 20, ry, 36 if en else 30, col if (en or hl) else "#8A7F92",
                 a * min(1, q * 2), "black", "l")
        # 高亮框
        hk = smooth(prog(t, 14.6, 15.0))
        if hk > 0:
            ry = -h / 2 + 160 + 5 * 78
            ctx.set_line_width(5)
            setc(ctx, "#E5484D", a * hk)
            rrect(ctx, bx0 - 140, ry - 38, 1040 * ease_out(hk), 76, 26)
            ctx.stroke()


# ---------------------------------------------------------------- D 网民占比 + 上锁的 App

APPS = [("公众号", "#07C160"), ("抖音", "#161823"), ("小红书", "#FF2442"), ("淘宝", "#FF5000")]


def apps(ctx, t):
    a = smooth(prog(t, 18.0, 18.8))
    if a <= 0:
        return
    # 甜甜圈图
    cx, cy, R = DX - 430, 430, 230
    p = ease_out(prog(t, 18.6, 19.6))
    ctx.set_line_width(80)
    setc(ctx, "#E9DDD0", a)
    circle(ctx, cx, cy, R)
    ctx.stroke()
    if p > 0:
        ctx.set_line_width(86)
        ctx.set_line_cap(0)
        setc(ctx, "#E5484D", a)
        ctx.new_sub_path()
        ctx.arc(cx, cy, R, -math.pi / 2, -math.pi / 2 + TAU * 0.2 * p)
        ctx.stroke()
    text(ctx, "全球网民", cx, cy - 34, 38, "#5A4335", a, "black")
    text(ctx, "中文 ≈ 1/5", cx, cy + 30, 50, "#E5484D", a * smooth(prog(t, 19.2, 19.6)), "black")
    # App 方块
    for i, (name, col) in enumerate(APPS):
        k = pop(t, 19.2 + i * 0.2, 0.45)
        if k <= 0:
            continue
        ax, ay = DX + 230 + (i % 2) * 330, 270 + (i // 2) * 320
        with at(ctx, ax, ay, k):
            card(ctx, -130, -130, 260, 260, 56, col, a, shadow=0.3)
            glow(ctx, 0, -10, 120, "#FFFFFF", 0.18 * a)
            from ..ui import lines_block
            lines_block(ctx, -80, -62, 160, 4, 26, "#FFFFFF", 0.5 * a, 1.0, 10, seed=i + 3)
            text(ctx, name, 0, 82, 40, "#FFFFFF", a, "black")
        lk = ease_out(prog(t, 20.0 + i * 0.25, 20.35 + i * 0.25))
        if lk > 0:
            drop = (1 - lk) * -120
            ic_lock(ctx, ax + 92, ay + 92 + drop, 110, a, t)
            ring_burst(ctx, t, 20.35 + i * 0.25, ax + 92, ay + 92, 20, 90, "#FFD25C", 0.5, 5)
    tk = pop(t, 21.4, 0.45)
    if tk > 0:
        with at(ctx, DX + 395, 790, tk):
            pill(ctx, "内容锁在 App 里，外部很难获取", 0, 0, 32, "#FFFFFF", "#5A4335", a, 0.9)


def sfx():
    out = []
    for i in range(3):
        out.append((0.2 + i * 0.15, "slide", {"gain": 0.25}))
    for (_, _, t0) in FOODS:
        out.append((t0, "whoosh_short", {"gain": 0.3}))
        out.append((t0 + 0.45, "chomp", {"gain": 0.55}))
        out.append((t0 + 0.75, "rise", {"gain": 0.3}))
    out += [(3.7, "chime", {"gain": 0.4}),
            (T_JUNK, "slide", {"gain": 0.3}), (T_JUNK + 0.45, "buzz", {"gain": 0.3}),
            (T_PUSH, "swish", {"gain": 0.4}),
            (5.95, "hop", {"gain": 0.3}), (6.85, "thud", {"gain": 0.3}),
            (6.2, "door", {"gain": 0.45})]
    for i in range(len(CRATES)):
        out.append((6.7 + i * 0.32, "pop", {"gain": 0.35, "pitch": 0.9 + i * 0.08}))
    out += [(8.5, "stream", {"dur": 3.2, "gain": 0.22}), (9.2, "ding", {"gain": 0.35, "pitch": 1.2}),
            (11.95, "hop", {"gain": 0.3}), (12.75, "thud", {"gain": 0.3}),
            (12.2, "pop", {"gain": 0.35, "pitch": 0.8})]
    for i in range(len(LANGS)):
        out.append((12.8 + i * 0.22, "rise", {"gain": 0.3 if i == 0 else 0.18, "pitch": 1.0 + i * 0.1}))
    out += [(14.3, "surprise", {"gain": 0.35}), (14.6, "alert", {"gain": 0.4}),
            (15.5, "womp", {"gain": 0.18}), (16.6, "think", {"dur": 1.5, "gain": 0.15}),
            (18.15, "hop", {"gain": 0.3}), (18.95, "thud", {"gain": 0.3}),
            (18.6, "rise", {"gain": 0.3})]
    for i in range(4):
        out.append((19.2 + i * 0.2, "pop", {"gain": 0.3, "pitch": 1.0 + i * 0.1}))
        out.append((20.35 + i * 0.25, "lock", {"gain": 0.5}))
    out += [(21.4, "pop", {"gain": 0.3, "pitch": 0.8})]
    for k in range(3):
        out.append((22.1 + k * 0.35 + 0.2, "knock", {"gain": 0.55}))
    out.append((23.2, "womp", {"gain": 0.3}))
    return out
