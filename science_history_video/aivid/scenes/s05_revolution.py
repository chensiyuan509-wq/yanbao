"""第五章 科学革命：哥白尼原版日心说图；伽利略肖像、手绘月相、第一视角看木星卫星；第谷的墙象限仪；
开普勒的 8 角分与椭圆；扮成伽利略的 Claude 做斜面实验；皇家学会；牛顿肖像与"月球检验"。关键词：实验。"""
import math

from ..core import (TAU, H, W, arrow, at, circle, clamp, dashed, ease_in, ease_io, ease_out, ellipse, glow, lerp, lin,
                    mix, poly, polyline_partial, prog, rad, rng, rrect, setc, smooth, star4, stroke_pts, text)
from .. import film, proofs
from ..archive import caption, framed, kb
from mascot import draw_prop
from .common import arch, claude, label, lit, role, sequence

DUR = 52.0
CHAPTER = dict(num="第 五 章", title="科学革命", era="1543 — 1687 年", key="实验", at=0.4, dur=4.0)
GRAIN = 0.08

VO = [
    (4.6, "1543 年，哥白尼：是地球绕着{太阳}转。"),
    (7.4, "1609 年，伽利略把{望远镜}对准天空："),
    (10.2, "月亮上有山有坑——他亲手画了下来；"),
    (13.6, "木星旁的四颗小星每晚换位置：它们{绕着木星转}。"),
    (17.6, "原来，地球不是万物的中心。"),
    (20.4, "第谷用巨大的墙象限仪，观测了二十多年；"),
    (23.4, "开普勒发现：火星数据和圆轨道差了 {8 角分}，"),
    (26.4, "他选择相信数据：行星轨道是{椭圆}。"),
    (29.4, "伽利略用斜面实验，测出下落距离与{时间平方}成正比；"),
    (33.2, "皇家学会的格言：'{不要只听信任何人}'——结论要靠实验检验。"),
    (37.3, "1687 年，牛顿出版《原理》，提出{万有引力}："),
    (40.4, "苹果会落地，月亮为什么不掉下来？"),
    (44.2, "月球远 60 倍，引力减为 1/3600：9.8 ÷ 3600 ≈ 0.0027；"),
    (48.4, "实测月球的向心加速度，也是 0.0027——{同一种力}。", {"spill": 0.5}),
]

SUPERS = []


def _shot_a(ctx, t):
    to = arch(ctx, t, "copernicus", 0.0, 7.0, (0.5, 0.5, 1.0), (0.5, 0.48, 1.35), "哥白尼《天体运行论》中的日心体系图",
              "1543 年 · 纽伦堡 · 公有领域", grade="warm", cap=(4.4, 6.6))
    k = smooth(prog(t, 5.2, 5.8))
    if k > 0:
        label(ctx, "Sol 太阳 · 位于中心", 1500, 260, 34, "#FFE8C0", k, "serif_sb")
        label(ctx, "Terra 地球 · 第三圈", 1500, 320, 30, "#F2D79B", k, "serif_sb")


def _shot_b(ctx, t):
    if t < 10.0:
        arch(ctx, t, "galileo", 7.0, 10.0, (0.5, 0.35, 1.05), (0.5, 0.3, 1.3), "伽利略像",
             "朱斯托·苏斯特曼斯 · 1636 年 · 英国国家海事博物馆 · 公有领域", cap=(0.2, 2.8))
        return
    if t < 13.6:
        arch(ctx, t, "galileo_moon", 10.0, 13.6, (0.5, 0.3, 1.05), (0.5, 0.42, 1.35), "伽利略手绘的月相",
             "1609 年 · 水彩 · 佛罗伦萨国家中央图书馆 · 公有领域", grade="warm", cap=(0.2, 3.3))
        return
    if t < 17.6:
        _jupiter(ctx, t)
        return
    _rooftop(ctx, t)


JUP = [("1610.1.7", [-2.4, -1.1, 1.4]), ("1.8", [0.9, 1.6, 2.4]), ("1.10", [-2.0, -1.0]), ("1.13", [-1.2, 0.8, 1.7, 2.6])]


def _jupiter(ctx, t):
    u = t - 13.6
    ctx.set_source_rgb(0.01, 0.01, 0.03)
    ctx.paint()
    jx, jy = math.sin(t * 1.3) * 6, math.cos(t * 1.1) * 5
    cx, cy = 820 + jx, 520 + jy
    film.star_field(ctx, t, 60, 33, area=(400, 120, 900, 800), a=0.5)
    idx = min(3, int(u / 1.0))
    q = u - idx * 1.0
    glow(ctx, cx, cy, 120, "#F2D8A8", 0.4)
    circle(ctx, cx, cy, 40)
    ctx.set_source(lin(0, cy - 40, 0, cy + 40, [(0, "#F2DDB0"), (0.3, "#C9A070"), (0.5, "#F0D8A8"), (0.7, "#B88A5A"),
                                               (1, "#E8CFA0")]))
    ctx.fill()
    name, pos = JUP[idx]
    k = smooth(q / 0.25)
    for p in pos:
        x = cx + p * 110
        glow(ctx, x, cy, 30, "#FFFFFF", 0.5 * k)
        circle(ctx, x, cy, 6)
        setc(ctx, "#FFFFFF", k)
        ctx.fill()
    label(ctx, name, cx, cy + 200, 40, "#FFE8C0", k, "latin")
    film.scope_view(ctx, cx, cy, 420)
    framed(ctx, "medicean", 1600, 520, 560, smooth(prog(u, 0.3, 0.8)))
    label(ctx, "《星际信使》中的记录（1610）", 1600, 860, 26, "#FFE8C0", smooth(prog(u, 0.5, 1.0)), "serif_sb")


GAL = (role(1180, 905, 0.5, "galileo", "wonder", seed=52.0, palette="amber").hold(17.6, ("telescope",), "r", 0.0)
       .look(17.7, -0.6, -0.8).expr(18.8, "awe"))


def _rooftop(ctx, t):
    film.sky(ctx, [(0, "#04060E"), (0.6, "#0E1832"), (1, "#24304A")])
    film.star_field(ctx, t, 260, 51, area=(0, 90, W, 700), a=0.9)
    film.moon(ctx, 420, 280, 46, 0.4, 1.0, glow_a=0.4)
    R = rng(4)
    x = -50
    pts = [(-50, 820)]
    while x < W + 50:
        w = R.uniform(60, 160)
        h = R.uniform(40, 120)
        pts += [(x, 820 - h), (x + w, 820 - h)]
        x += w
    pts.append((W + 50, 820))
    poly(ctx, pts)
    setc(ctx, "#0A0E18")
    ctx.fill()
    ellipse(ctx, 520, 650, 120, 110)
    ctx.rectangle(400, 650, 240, 170)
    ctx.rectangle(1540, 460, 70, 360)
    ctx.fill()
    ctx.set_source(lin(0, 800, 0, H, [(0, "#1A1410"), (1, "#0A0806")]))
    ctx.rectangle(-50, 820, W + 100, 300)
    ctx.fill()
    with lit("#8FA6FF", 0.4, 0.75):
        GAL.draw(ctx, t)
    label(ctx, "Claude 扮演伽利略 · 帕多瓦，1610", 1180, 460, 28, "#DCE6FF", smooth(prog(t, 17.9, 18.5)), "serif_sb")
    film.vignette(ctx, 0.6)


def _shot_c(ctx, t):
    if t < 23.0:
        arch(ctx, t, "tycho", 20.0, 23.0, (0.5, 0.45, 1.05), (0.5, 0.4, 1.3), "第谷的墙象限仪",
             "《新天文学仪器》· 1598 年 · 公有领域", grade="sepia", cap=(0.2, 2.8))
        return
    u = t - 23.0
    ctx.set_source(rad(900, 520, 0, 1300, [(0, "#2C2016"), (1, "#0A0705")]))
    ctx.paint()
    film.paint_texture(ctx, "parchment", 0, 0, W, H, 0.12)
    R = rng(21)
    for r_ in range(13):
        a = smooth(prog(u, r_ * 0.05, r_ * 0.05 + 0.3)) * (1 - 0.6 * smooth(prog(u, 2.0, 2.8)))
        line = f"{1580 + r_ * 2}  {R.randint(0, 359):3d}° {R.randint(0, 59):02d}′"
        text(ctx, line, 130, 250 + r_ * 50, 27, "#E8D8B8", a, "latin", "l")
    label(ctx, "第谷的火星观测（示意）", 330, 920, 26, "#D9B26A", 1.0, "serif_sb")
    cx, cy, a_, b_ = 1250, 540, 330, 300
    c_ = math.sqrt(a_ * a_ - b_ * b_)
    sun = (cx + c_, cy)
    glow(ctx, *sun, 90, "#FFC46B", 0.7)
    circle(ctx, *sun, 18)
    setc(ctx, "#FFE8A8")
    ctx.fill()
    pts = [(cx + a_ * math.cos(i / 16 * TAU + 0.2), cy + b_ * math.sin(i / 16 * TAU + 0.2)) for i in range(16)]
    pk = smooth(prog(u, 0.2, 0.8))
    for p in pts:
        circle(ctx, p[0], p[1], 7)
        setc(ctx, "#FF8A5A", pk)
        ctx.fill()
    ck = smooth(prog(u, 0.8, 1.3)) * (1 - smooth(prog(u, 3.6, 4.2)))
    rc = (a_ + b_) / 2
    ctx.set_line_width(3)
    setc(ctx, "#8FB6FF", 0.9 * ck)
    circle(ctx, cx + c_ * 0.5, cy, rc)
    ctx.stroke()
    mk = smooth(prog(u, 1.3, 1.9)) * (1 - smooth(prog(u, 3.4, 3.9)))
    if mk > 0:
        p = pts[4]
        ang = math.atan2(p[1] - cy, p[0] - cx - c_ * 0.5)
        q = (cx + c_ * 0.5 + rc * math.cos(ang), cy + rc * math.sin(ang))
        circle(ctx, p[0] + 10, p[1] + 10, 90)
        ctx.set_line_width(7)
        setc(ctx, "#C9A060", mk)
        ctx.stroke()
        ctx.set_line_width(4)
        setc(ctx, "#FFD27A", mk)
        ctx.move_to(*p)
        ctx.line_to(*q)
        ctx.stroke()
        label(ctx, "8′", p[0] + 130, p[1] + 20, 56, "#FFD27A", mk, "latin_b")
        label(ctx, "≈ 1/4 个月亮宽", p[0] + 130, p[1] + 80, 28, "#FFE8C0", mk, "serif_sb")
    ek = ease_io(prog(u, 3.6, 4.8))
    if ek > 0:
        ell = [(cx + a_ * math.cos(th), cy + b_ * math.sin(th)) for th in [i / 120 * TAU for i in range(121)]]
        stroke_pts(ctx, polyline_partial(ell, ek), 5, "#FFE2A8", 1.0)
        circle(ctx, cx - c_, cy, 8)
        setc(ctx, "#FFE2A8", ek)
        ctx.fill()
        label(ctx, "椭圆 · 太阳在一个焦点上（开普勒，1609）", cx, cy + b_ + 70, 32, "#FFE2A8", smooth(prog(u, 4.4, 5.0)),
              "serif_sb")
    film.vignette(ctx, 0.55)


GAL2 = (role(330, 900, 0.46, "galileo", "focused", seed=53.0, palette="amber").point(29.6, "r", 0.3, 60)
        .expr(31.6, "excited").arms_down(32.4))


def _shot_d(ctx, t):
    if t < 33.0:
        u = t - 29.0
        ctx.set_source(rad(960, 560, 0, 1300, [(0, "#3A2818"), (1, "#0E0905")]))
        ctx.paint()
        film.shaft(ctx, 300, 90, 700, 980, 160, 420, "#FFD49A", 0.12)
        x0, y0, x1, y1 = 520, 380, 1720, 840
        poly(ctx, [(x0, y0), (x1, y1), (x1, y1 + 60), (x0, y0 + 60)])
        ctx.set_source(lin(0, y0, 0, y1 + 60, [(0, "#8A6A3E"), (1, "#5A3E1E")]))
        ctx.fill()
        T = 4
        tt = clamp((u - 0.3) / 0.8, 0, T)
        frac = (tt / T) ** 2
        bx, by = lerp(x0, x1, frac), lerp(y0, y1, frac)
        ang = math.atan2(y1 - y0, x1 - x0)
        nx, ny = math.sin(ang), -math.cos(ang)
        for k in range(1, T + 1):
            f = (k / T) ** 2
            mx, my = lerp(x0, x1, f), lerp(y0, y1, f)
            hit = tt >= k
            ctx.set_line_width(6)
            setc(ctx, "#FFD27A" if hit else "#6A4A28")
            ctx.move_to(mx, my)
            ctx.line_to(mx + nx * 70, my + ny * 70)
            ctx.stroke()
            text(ctx, f"{k * k}", mx + nx * 110, my + ny * 110, 40, "#FFE8C0", 1.0 if hit else 0.35, "latin_b")
        circle(ctx, bx + nx * 26, by + ny * 26, 26)
        ctx.set_source(rad(bx + nx * 20, by + ny * 20, 2, 30, [(0, "#E8E8F0"), (1, "#6A6A78")]))
        ctx.fill()
        label(ctx, "时间 1 : 2 : 3 : 4 → 距离 1 : 4 : 9 : 16", 1100, 230, 38, "#FFE8C0", smooth(prog(u, 3.0, 3.5)), "serif_sb")
        with lit("#FFC890", 0.3, 0.95):
            GAL2.draw(ctx, t)
        film.vignette(ctx, 0.5)
        return
    u = t - 33.0
    ctx.set_source(rad(960, 520, 0, 1300, [(0, "#2A2420"), (1, "#0A0806")]))
    ctx.paint()
    film.paint_texture(ctx, "stone", 0, 0, W, H, 0.3)
    k = smooth(prog(u, 0.1, 0.6))
    rrect(ctx, 460, 250, 1000, 230, 14)
    ctx.set_source(lin(0, 250, 0, 480, [(0, "#8A8478", k), (1, "#5E5A52", k)]))
    ctx.fill()
    film.tracked(ctx, "NULLIUS IN VERBA", 962, 352, 78, "#2A2620", k, "latin_b", 0.12)
    film.tracked(ctx, "NULLIUS IN VERBA", 960, 348, 78, "#D8D2C4", k * 0.9, "latin_b", 0.12)
    label(ctx, "英国皇家学会 · 1660 年", 960, 440, 34, "#F2E6CE", smooth(prog(u, 0.5, 1.0)), "serif_sb")
    for i in range(8):
        kk = ease_out(prog(u, 1.6 + i * 0.18, 1.9 + i * 0.18))
        if kk <= 0:
            continue
        y = 930 - i * 30 - (1 - kk) * 200
        rrect(ctx, 760 + (i % 3) * 6, y, 400, 28, 4)
        setc(ctx, mix("#7A2E1E", "#3A4A6A", (i % 3) / 2), kk)
        ctx.fill()
    label(ctx, "《哲学汇刊》1665 年创刊 · 发表 → 质疑 → 重复 → 修正", 960, 560, 30, "#FFE8C0", smooth(prog(u, 1.6, 2.2)),
          "serif_sb")
    film.vignette(ctx, 0.55)


NEWTON = (role(1000, 868, 0.5, "newton", "relieved", seed=54.0, palette="coral").sit(40.0, 1.0, 0.01).look(40.0, 0.4, -0.3)
          .expr(41.6, "ko").startle(41.6).expr(42.3, "surprised").look(42.4, 0.8, -0.9)
          .expr(43.0, "excited").fx(43.0, ("bulb",)))


def _tree(ctx, x, y, s, color):
    setc(ctx, color)
    ctx.set_line_width(26 * s)
    ctx.set_line_cap(1)
    ctx.move_to(x, y)
    ctx.curve_to(x + 10 * s, y - 120 * s, x - 20 * s, y - 200 * s, x, y - 280 * s)
    ctx.stroke()
    for (dx, dy, r) in ((-150, -330, 170), (60, -380, 190), (190, -300, 150), (-40, -470, 160), (-230, -250, 120)):
        circle(ctx, x + dx * s, y + dy * s, r * s)
        ctx.fill()


def _shot_e(ctx, t):
    if t < 40.0:
        u = t - 37.0
        kb(ctx, "newton", t, 37.0, 40.0, (0.5, 0.32, 1.1), (0.5, 0.3, 1.35), rect=(0, 0, W * 0.55, H))
        if u > 0.3:
            kb(ctx, "principia", t, 37.0, 40.0, (0.5, 0.45, 1.05), (0.5, 0.42, 1.2), rect=(W * 0.55, 0, W * 0.45, H))
        film.vignette(ctx, 0.5)
        caption(ctx, "牛顿像（内勒，1689）·《自然哲学的数学原理》（1687）", "公有领域", smooth(prog(u, 0.2, 0.7)))
        return
    if t < 44.0:
        u = t - 40.0
        film.sky(ctx, [(0, "#1E2A4A"), (0.55, "#9A6A72"), (0.7, "#E8A070"), (1, "#3A2A2A")])
        film.moon(ctx, 1500, 300, 50, 0.5, 1.0, glow_a=0.45)
        film.ridge(ctx, -50, W + 50, 760, 70, 0.003, 31.0, "#2A1E26", 1.0, step=16)
        ctx.move_to(-50, H + 50)
        ctx.line_to(-50, 880)
        ctx.curve_to(500, 820, 1300, 840, W + 50, 900)
        ctx.line_to(W + 50, H + 50)
        ctx.close_path()
        setc(ctx, "#1A1418")
        ctx.fill()
        _tree(ctx, 820, 880, 1.15, "#140E12")
        ax, ay0 = 1020, 560
        fall = clamp((u - 0.4) / 1.1)
        ay = ay0 + (690 - ay0) * fall ** 2
        if u < 1.6:
            with at(ctx, ax, ay, 0.4):
                draw_prop(ctx, ("apple",), t)
        else:
            q = clamp((u - 1.6) / 0.8)
            with at(ctx, ax + 120 * ease_out(q), 780 + 80 * ease_out(q) - math.sin(q * math.pi) * 70, 0.4, q * 3):
                draw_prop(ctx, ("apple",), t)
        lk = smooth(prog(u, 2.4, 3.2))
        if lk > 0:
            dashed(ctx, ax + 60, 700, 1450, 330, 3, "#FFD27A", 0.7 * lk, (14, 10), -t * 30)
            label(ctx, "同一种力？", 1260, 560, 40, "#FFD27A", lk, "serif_k")
        with lit("#FFB0A0", 0.3, 0.8):
            NEWTON.draw(ctx, t)
        film.vignette(ctx, 0.55)
        return
    proofs.paper(ctx)
    proofs.moon_test(ctx, t - 44.0)
    proofs.eq(ctx, "牛顿的\"月球检验\"", 110, 175, 34, proofs.INK, 1.0, "l", "serif_k")
    film.vignette(ctx, 0.35, color="#2A1A0A")


SHOTS = [(0.0, _shot_a), (7.0, _shot_b), (20.0, _shot_c), (29.0, _shot_d), (37.0, _shot_e)]
TRANS = {1: ("dissolve", 1.0), 2: ("luma", 0.9), 3: ("lightsweep", 0.9, {"color": "#FFE2B0"}), 4: ("dissolve", 1.0)}


def draw(ctx, t):
    sequence(ctx, t, SHOTS, TRANS)


def sfx():
    out = [(0.0, "ambience_room", {"dur": 7.0, "gain": 0.4}), (0.4, "page", {"gain": 0.3}), (4.4, "shimmer", {"dur": 2.0, "gain": 0.15}),
           (7.0, "ambience_room", {"dur": 6.6, "gain": 0.35}), (10.2, "quill", {"dur": 2.0, "gain": 0.18}),
           (13.6, "ambience_space", {"dur": 4.0, "gain": 0.4}), (13.7, "brass", {"gain": 0.3})]
    for i in range(4):
        out.append((13.6 + i * 1.0, "tick", {"gain": 0.25}))
    out += [(17.6, "ambience_night", {"dur": 2.4, "gain": 0.4}), (17.8, "brass", {"gain": 0.2}),
            (20.0, "ambience_room", {"dur": 9.0, "gain": 0.35}), (23.2, "quill", {"dur": 1.5, "gain": 0.18}),
            (24.4, "brass", {"gain": 0.22}), (24.8, "heartbeat", {"n": 2, "gain": 0.3}), (26.6, "shimmer", {"dur": 1.6, "gain": 0.2}),
            (29.0, "ambience_room", {"dur": 4.0, "gain": 0.35}), (29.3, "slide", {"gain": 0.2})]
    for k in range(1, 5):
        out.append((29.3 + k * 0.8, "ding", {"gain": 0.28, "pitch": 1 + k * 0.05}))
    out += [(33.0, "ambience_room", {"dur": 4.0, "gain": 0.4}), (33.2, "stamp", {"gain": 0.35}),
            (34.6, "thud", {"gain": 0.22}), (35.0, "thud", {"gain": 0.2}), (35.4, "thud", {"gain": 0.18}),
            (37.0, "ambience_room", {"dur": 3.0, "gain": 0.35}), (37.2, "page", {"gain": 0.25}),
            (40.0, "ambience_birds", {"dur": 4.0, "gain": 0.3}), (41.6, "thump", {"gain": 0.55}), (41.65, "boing", {"gain": 0.25}),
            (43.0, "ding", {"gain": 0.3}), (44.0, "ambience_room", {"dur": 8.0, "gain": 0.35}),
            (44.6, "chalk", {"dur": 2.0, "gain": 0.2}), (47.4, "chalk", {"dur": 1.6, "gain": 0.2}), (50.0, "chime", {"gain": 0.2}),
            (50.6, "steam", {"dur": 1.4, "gain": 0.2})]
    return out
