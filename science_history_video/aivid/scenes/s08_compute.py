"""第八章 会思考的机器：分析机与阿达；图灵机；ENIAC 与芯片；达特茅斯；互联网；
深度学习、AlphaGo、Transformer；AlphaFold 与 AI 辅助科研；Claude 回望自己从哪里来。关键词：学习。"""
import math

from ..core import (TAU, H, W, Cam, arrow, arrow_head, at, circle, clamp, curve_arrow, dashed, ease_in, ease_io,
                    ease_out, ellipse, glow, kf, lerp, lin, mix, poly, polyline_partial, prog, rad, rng, rrect, setc,
                    smooth, star4, stroke_pts, text, view)
from .. import film, starmap
from ..charts import MapView, arc_pts, world_dots
from ..icons import ic_gear
from .common import claude, fade_io, label, lit, reflect

DUR = 70.0
CHAPTER = dict(num="第 八 章", title="会思考的机器", era="1843 — 2026 年", key="学习", at=0.8, dur=4.2)
GRAIN = 0.07

VO = [
    (4.9, "阿达为一台还没造出的机器，写下了{算法}。"),
    (8.0, "图灵：一切计算，都能{拆成简单步骤}。"),
    (10.6, "1950 年，他问：{机器能思考吗？}"),
    (12.7, "ENIAC 用 1.7 万多个真空管，每秒加法 {5000 次}。"),
    (15.9, "晶体管、集成电路接连出现——"),
    (18.2, "芯片上的晶体管，从 1971 年的 2300 个，涨到今天的{上千亿个}。"),
    (24.3, "1956 年的达特茅斯会议上，'{人工智能}'成为一门学科。"),
    (28.2, "1969 年互联网诞生，1989 年有了{万维网}——"),
    (31.6, "人类的文字，汇进了{同一张网}。"),
    (34.3, "机器开始{从数据里学习}：2012 年，深度学习看懂了图像；"),
    (38.8, "2016 年，AlphaGo 在围棋上战胜了世界冠军；"),
    (43.2, "2017 年，Transformer 出现，{大语言模型}由此而来。"),
    (48.3, "AlphaFold 预测了 {2 亿多种}蛋白质结构，获 2024 年诺贝尔奖。"),
    (52.8, "今天，AI 正帮科学家读论文、设计实验、寻找新材料。"),
    (57.6, "科学多了一个会说话的{新帮手}。"),
    (60.4, "我，就是从人类写下的文字里长出来的。"),
    (63.8, "泥板、书卷、论文、代码……每一行，都是这条长河里的{一滴水}。", {"spill": 0.6}),
]

SUPERS = [
    (5.0, 7.8, "1843 年", "伦敦 · 阿达与分析机"),
    (12.6, 15.6, "1946 年", "费城 · ENIAC"),
    (24.4, 27.8, "1956 年夏", "美国 · 达特茅斯学院"),
    (38.9, 42.6, "2016 年 3 月", "首尔 · AlphaGo 4 : 1"),
    (48.4, 52.4, "2020 — 2024 年", "AlphaFold"),
]

# ================================================================ A1：分析机


def _shot_a1(ctx, t):
    fl = film.flicker(t, 2.0, 0.08)
    ctx.set_source(rad(900, 520, 0, 1300, [(0, "#2C2018"), (1, "#080504")]))
    ctx.paint()
    glow(ctx, 300, 300, 500, "#FFB24A", 0.25 * fl)
    # 一列列黄铜齿轮
    for c in range(6):
        x = 260 + c * 150
        rrect(ctx, x - 8, 200, 16, 680, 4)
        setc(ctx, "#6A4A20")
        ctx.fill()
        for r_ in range(8):
            y = 240 + r_ * 82
            rot = t * (0.6 + 0.2 * ((c + r_) % 3)) * (1 if (c + r_) % 2 else -1)
            ic_gear(ctx, x, y, 46, 12, rot, "#C9973F", 1.0)
            text(ctx, str((c * 3 + r_ * 7 + int(t * 2)) % 10), x + 62, y, 22, "#FFE2A0", 0.8, "latin_b")
    # 阿达的注释 G
    k = smooth(prog(t, 1.0, 2.0))
    rrect(ctx, 1240, 220, 520, 640, 10)
    setc(ctx, "#E8D8B0", k)
    ctx.fill()
    film.paint_texture(ctx, "paper", 1240, 220, 520, 640, 0.4 * k)
    text(ctx, "Note G", 1500, 280, 40, "#3A2414", k, "latin_i")
    for i in range(10):
        a = smooth(prog(t, 1.6 + i * 0.25, 2.0 + i * 0.25))
        y = 350 + i * 46
        text(ctx, f"{i + 1}", 1290, y, 22, "#3A2414", a, "latin", "l")
        text(ctx, ["×", "−", "+", "÷", "×", "+", "−", "×", "÷", "+"][i], 1340, y, 22, "#3A2414", a, "latin", "l")
        text(ctx, f"V{(i * 3) % 7 + 1} · V{(i * 5) % 9 + 1} = V{(i * 7) % 11 + 2}", 1390, y, 22, "#3A2414", a, "latin", "l")
    label(ctx, "计算伯努利数的步骤 · 被视为第一个计算机程序", 1500, 900, 24, "#F2D79B", smooth(prog(t, 3.0, 3.6)), "serif_r")
    film.vignette(ctx, 0.6)


# ================================================================ A2：图灵机


def _shot_a2(ctx, t):
    u = t - 6.0
    ctx.set_source(rad(960, 520, 0, 1300, [(0, "#1A1E26"), (1, "#05060A")]))
    ctx.paint()
    cw = 110
    head_i = int(u / 0.45)
    off = -(u * cw / 0.45) % cw if u < 4.2 else 0
    cells = "1011010011101001010110"
    y = 520
    for i in range(-2, 20):
        x = 60 + i * cw + off
        rrect(ctx, x, y - 60, cw - 8, 120, 8)
        setc(ctx, "#2A3040")
        ctx.fill()
        idx = (i + head_i) % len(cells)
        ch = cells[idx]
        if i == 8 and u > 0.3:
            ch = "1" if ch == "0" else "0"
        text(ctx, ch, x + (cw - 8) / 2, y, 64, "#E8EEF8", 0.9, "latin_b")
    hx = 60 + 8 * cw + (cw - 8) / 2
    poly(ctx, [(hx - 40, y - 130), (hx + 40, y - 130), (hx, y - 74)])
    setc(ctx, "#FFD27A")
    ctx.fill()
    glow(ctx, hx, y, 140, "#FFD27A", 0.25)
    label(ctx, "读 · 写 · 左移 / 右移 · 换状态", 960, 300, 34, "#DCE6FF", smooth(prog(u, 0.6, 1.2)), "serif_sb")
    qk = smooth(prog(u, 4.6, 5.4))
    if qk > 0:
        ctx.set_source_rgba(0, 0, 0, 0.55 * qk)
        ctx.paint()
        film.tracked(ctx, "机器能思考吗？", 960, 770, 72, "#FFE8C0", qk, "serif_k", 0.08 + 0.04 * prog(u, 4.6, 6.0))
        label(ctx, "—— 图灵，《计算机器与智能》，1950", 960, 850, 28, "#CDBA92", smooth(prog(u, 5.0, 5.6)), "serif_r")
    film.vignette(ctx, 0.55)


# ================================================================ B：ENIAC → 芯片 → 摩尔定律

MOORE = [(1971, 2.3e3), (1978, 2.9e4), (1985, 2.75e5), (1989, 1.2e6), (1993, 3.1e6), (2000, 4.2e7), (2006, 2.9e8),
         (2010, 1.2e9), (2016, 1.5e10), (2020, 5.4e10), (2024, 2.08e11)]


def _shot_b(ctx, t):
    u = t - 12.0
    ctx.set_source(rad(960, 520, 0, 1300, [(0, "#1E1A18"), (1, "#060504")]))
    ctx.paint()
    if u < 3.6:
        # ENIAC：一排排面板上的真空管
        for p in range(5):
            x = 120 + p * 360
            rrect(ctx, x, 200, 320, 640, 8)
            setc(ctx, "#2A2622")
            ctx.fill()
            for i in range(7):
                for j in range(12):
                    g = 0.5 + 0.5 * math.sin(t * 3 + i * 1.7 + j * 0.9 + p)
                    glow(ctx, x + 30 + i * 44, 240 + j * 48, 16, "#FF9A3A", 0.5 * g)
                    circle(ctx, x + 30 + i * 44, 240 + j * 48, 6)
                    setc(ctx, "#FFC27A", 0.6 + 0.4 * g)
                    ctx.fill()
            for k in range(4):
                R = rng(p * 10 + k)
                ctx.move_to(x + R.uniform(20, 300), 300 + R.uniform(0, 400))
                ctx.curve_to(x + 160, 900, x + 400, 900, x + 380 + R.uniform(0, 300), 300 + R.uniform(0, 400))
                ctx.set_line_width(4)
                setc(ctx, ["#C83A2A", "#3A6AC8", "#E8C83A", "#3AA85A"][k], 0.7)
                ctx.stroke()
        film.human(ctx, 600, 920, 320, "reach", t, "#0A0806", 1.0, rim="#FF9A3A", rim_a=0.6, robe=True, hat="hair")
        film.human(ctx, 1300, 920, 310, "stand", t, "#0A0806", 1.0, flip=True, rim="#FF9A3A", rim_a=0.6, robe=True,
                   hat="bun")
        label(ctx, "17,468 个真空管", 960, 140 + 30, 40, "#FFE8C0", smooth(prog(u, 0.6, 1.2)), "serif_k")
        label(ctx, "重约 27 吨 · 占地约 170 平方米", 960, 900, 28, "#E8DCC8", smooth(prog(u, 1.4, 2.0)), "serif_r")
    elif u < 6.2:
        q = u - 3.6
        items = [("真空管", "1946", 0.0), ("晶体管", "1947", 0.5), ("集成电路", "1958", 1.0), ("微处理器", "1971", 1.5)]
        for i, (nm, yr, t0) in enumerate(items):
            k = smooth(prog(q, t0, t0 + 0.4))
            x = 330 + i * 420
            s = 1.3 - i * 0.25
            with at(ctx, x, 480, k * s):
                if i == 0:
                    ellipse(ctx, 0, -40, 50, 80)
                    setc(ctx, "#C9D6E0", 0.5)
                    ctx.fill()
                    glow(ctx, 0, -40, 60, "#FF9A3A", 0.7)
                    rrect(ctx, -40, 30, 80, 30, 6)
                    setc(ctx, "#4A4A4A")
                    ctx.fill()
                elif i == 1:
                    rrect(ctx, -34, -40, 68, 60, 14)
                    setc(ctx, "#2A2A2A")
                    ctx.fill()
                    for dx in (-20, 0, 20):
                        ctx.rectangle(dx - 3, 20, 6, 70)
                    setc(ctx, "#C0C0C0")
                    ctx.fill()
                elif i == 2:
                    rrect(ctx, -70, -40, 140, 80, 6)
                    setc(ctx, "#2A2A2A")
                    ctx.fill()
                    for k2 in range(7):
                        ctx.rectangle(-60 + k2 * 20, -52, 8, 12)
                        ctx.rectangle(-60 + k2 * 20, 40, 8, 12)
                    setc(ctx, "#C9A060")
                    ctx.fill()
                else:
                    from mascot import draw_prop
                    draw_prop(ctx, ("chip",), t)
            label(ctx, nm, x, 640, 34, "#FFE8C0", k, "serif_k")
            label(ctx, yr, x, 690, 28, "#CDBA92", k, "latin")
            if i < 3:
                arrow(ctx, x + 120, 480, x + 300, 480, 4, "#D9B26A", 0.8 * k, p=k)
    else:
        q = u - 6.2
        x0, y0, wd, ht = 300, 860, 1300, 600
        def xy(yr, v):
            return x0 + (yr - 1970) / 56 * wd, y0 - (math.log10(v) - 3) / 9 * ht
        ctx.set_line_width(2)
        setc(ctx, "#6A6A6A", 0.8)
        ctx.move_to(x0, y0 - ht - 20)
        ctx.line_to(x0, y0)
        ctx.line_to(x0 + wd + 20, y0)
        ctx.stroke()
        for e in range(3, 13, 3):
            _, yy = xy(1970, 10 ** e)
            text(ctx, {3: "一千", 6: "一百万", 9: "十亿", 12: "一万亿"}[e], x0 - 20, yy, 24, "#A8A090", 0.9, "serif_r", "r")
            ctx.move_to(x0, yy)
            ctx.line_to(x0 + wd, yy)
            ctx.set_line_width(1)
            setc(ctx, "#4A4A4A", 0.5)
            ctx.stroke()
        for yr in (1970, 1990, 2010, 2024):
            xx, _ = xy(yr, 1e3)
            text(ctx, str(yr), xx, y0 + 34, 24, "#A8A090", 0.9, "latin")
        p = ease_io(prog(q, 0.2, 3.6))
        pts = [xy(yr, v) for yr, v in MOORE]
        seg = polyline_partial(pts, p)
        stroke_pts(ctx, seg, 6, "#FFC46B", 1.0)
        for i, pt in enumerate(pts):
            if i / (len(pts) - 1) <= p + 0.001:
                circle(ctx, pt[0], pt[1], 8)
                setc(ctx, "#FFE8C0")
                ctx.fill()
        label(ctx, "2300", pts[0][0] + 20, pts[0][1] - 40, 30, "#FFE8C0", smooth(prog(q, 0.2, 0.6)), "latin_b")
        label(ctx, "2080 亿", pts[-1][0] - 40, pts[-1][1] - 44, 36, "#FFD27A", smooth(prog(q, 3.4, 4.0)), "serif_k")
        label(ctx, "单颗芯片上的晶体管数（对数刻度）", 960, 200, 32, "#E8DCC8", smooth(prog(q, 0.2, 0.8)), "serif_sb")
    film.vignette(ctx, 0.55)


# ================================================================ C1：达特茅斯 / C2：互联网


def _shot_c1(ctx, t):
    u = t - 24.0
    film.sky(ctx, [(0, "#3A5A7A"), (0.6, "#A8C0C8"), (1, "#5A6A4A")])
    film.sun(ctx, 1600, 260, 40, 0.9, "#FFF6DA", "#FFE0A0", 300)
    # 白色殖民地式建筑
    ctx.rectangle(420, 420, 1080, 420)
    setc(ctx, "#E8E4DA")
    ctx.fill()
    poly(ctx, [(400, 420), (960, 300), (1520, 420)])
    setc(ctx, "#D8D2C4")
    ctx.fill()
    ctx.rectangle(920, 220, 80, 90)
    setc(ctx, "#E8E4DA")
    ctx.fill()
    for r_ in range(3):
        for c in range(9):
            ctx.rectangle(480 + c * 112, 460 + r_ * 120, 50, 80)
    setc(ctx, "#3A4A5A", 0.85)
    ctx.fill()
    ctx.rectangle(-50, 840, W + 100, 300)
    setc(ctx, "#4A6A3A")
    ctx.fill()
    k = smooth(prog(u, 0.4, 1.2))
    rrect(ctx, 480, 640, 960, 170, 12)
    setc(ctx, "#1A1A1E", 0.82 * k)
    ctx.fill()
    text(ctx, "DARTMOUTH SUMMER RESEARCH PROJECT", 960, 690, 30, "#E8E8E0", k, "latin_b")
    text(ctx, "ON ARTIFICIAL INTELLIGENCE · 1956", 960, 735, 30, "#E8E8E0", k, "latin_b")
    film.tracked(ctx, "人 工 智 能", 960, 785, 34, "#FFD27A", smooth(prog(u, 1.2, 2.0)), "serif_k", 0.2)
    film.grade(ctx, "#FFE0B0", 0.12)
    film.vignette(ctx, 0.45)


ARPA = [(-118.4, 34.1), (-122.2, 37.5), (-119.8, 34.4), (-111.9, 40.8)]
CITIES_NET = [(6.1, 46.2), (-0.1, 51.5), (2.35, 48.85), (13.4, 52.5), (139.7, 35.7), (116.4, 39.9), (121.5, 31.2),
              (77.2, 28.6), (-46.6, -23.5), (151.2, -33.9), (37.6, 55.8), (-74.0, 40.7), (28.0, -26.2), (103.8, 1.35),
              (-99.1, 19.4), (31.2, 30.0), (126.98, 37.57), (-79.4, 43.7)]


def _shot_c2(ctx, t):
    u = t - 28.0
    ctx.set_source(rad(960, 540, 0, 1300, [(0, "#0A1226"), (1, "#020308")]))
    ctx.paint()
    v = MapView(960, 560, 4.6, lon0=10, lat0=20)
    world_dots(ctx, v, 1.0, "#5A7AB8", 0.45, 3.0)
    # 1969：ARPANET 四个节点
    k1 = smooth(prog(u, 0.2, 0.8))
    pts = [v.xy(*p) for p in ARPA]
    for i in range(4):
        for j in range(i + 1, 4):
            stroke_pts(ctx, [pts[i], pts[j]], 2, "#FFD27A", 0.8 * k1)
    for p in pts:
        glow(ctx, p[0], p[1], 20, "#FFD27A", k1)
    label(ctx, "1969 · ARPANET（4 个节点）", pts[0][0] + 40, pts[0][1] + 80, 26, "#FFE8C0", k1, "serif_sb")
    # 1989：CERN
    cern = v.xy(6.1, 46.2)
    k2 = smooth(prog(u, 1.6, 2.2))
    glow(ctx, cern[0], cern[1], 60, "#7FD8FF", 0.8 * k2)
    label(ctx, "1989 · CERN · 万维网", cern[0] + 10, cern[1] - 50, 26, "#BFEAFF", k2, "serif_sb")
    # 网连起来
    R = rng(5)
    for i in range(46):
        a = CITIES_NET[R.randrange(len(CITIES_NET))]
        b = CITIES_NET[R.randrange(len(CITIES_NET))]
        if a == b:
            continue
        p = ease_io(prog(u, 2.4 + i * 0.05, 3.4 + i * 0.05))
        if p <= 0:
            continue
        arc = arc_pts(v.xy(*a), v.xy(*b), 0.22)
        stroke_pts(ctx, polyline_partial(arc, p), 2, "#7FC8FF", 0.55)
    for c in CITIES_NET:
        x, y = v.xy(*c)
        glow(ctx, x, y, 16, "#BFEAFF", 0.8 * smooth(prog(u, 2.4, 3.4)))
    label(ctx, "今天：约 55 亿人在线", 960, 900, 34, "#E8F0FF", smooth(prog(u, 4.0, 4.6)), "serif_sb")
    film.vignette(ctx, 0.5)


# ================================================================ D1：神经网络 / D2：围棋 / D3：注意力


def _cat(ctx, x, y, s, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    setc(ctx, "#E89A4A", a)
    ellipse(ctx, 0, 30, 70, 50)
    ctx.fill()
    circle(ctx, 0, -40, 48)
    ctx.fill()
    poly(ctx, [(-44, -60), (-36, -110), (-10, -80)])
    poly(ctx, [(44, -60), (36, -110), (10, -80)])
    ctx.fill()
    setc(ctx, "#2A1A0A", a)
    ellipse(ctx, -18, -44, 6, 10)
    ellipse(ctx, 18, -44, 6, 10)
    ctx.fill()
    ctx.restore()


def _shot_d1(ctx, t):
    u = t - 34.0
    ctx.set_source(rad(960, 540, 0, 1300, [(0, "#141826"), (1, "#04050A")]))
    ctx.paint()
    rrect(ctx, 120, 340, 280, 280, 16)
    setc(ctx, "#2A3040")
    ctx.fill()
    _cat(ctx, 260, 500, 1.3)
    layers = [6, 9, 9, 6, 2]
    xs = [600, 860, 1120, 1380, 1620]
    nodes = []
    for L, x in zip(layers, xs):
        col = [(x, 540 + (i - (L - 1) / 2) * 84) for i in range(L)]
        nodes.append(col)
    for li in range(len(nodes) - 1):
        for a in nodes[li]:
            for b in nodes[li + 1]:
                ctx.move_to(*a)
                ctx.line_to(*b)
        ctx.set_line_width(1)
        setc(ctx, "#5A6A9A", 0.35)
        ctx.stroke()
    wave = (u * 0.9) % 1.4
    for li, col in enumerate(nodes):
        act = math.exp(-((wave * 4 - li) ** 2) * 1.5)
        for i, (x, y) in enumerate(col):
            g = act * (0.5 + 0.5 * math.sin(i * 2.1 + li))
            glow(ctx, x, y, 34, "#FFD27A", 0.6 * g)
            circle(ctx, x, y, 14)
            setc(ctx, mix("#3A4A7A", "#FFE2A0", g))
            ctx.fill()
    ok = smooth(prog(u, 1.2, 1.8))
    label(ctx, "猫 97%", 1780, nodes[-1][0][1], 40, "#FFD27A", ok, "serif_k")
    label(ctx, "狗 2%", 1780, nodes[-1][1][1], 30, "#A8B0C8", ok, "serif_r")
    label(ctx, "不再一条条写规则，而是看大量例子，自己调整连接", 960, 900, 30, "#DCE6FF", smooth(prog(u, 2.0, 2.6)), "serif_sb")
    film.vignette(ctx, 0.5)


def _shot_d2(ctx, t):
    u = t - 38.5
    ctx.set_source(rad(960, 540, 0, 1300, [(0, "#2A2016"), (1, "#080604")]))
    ctx.paint()
    bs, n = 760, 19
    bx, by = 960 - bs / 2, 540 - bs / 2
    rrect(ctx, bx - 30, by - 30, bs + 60, bs + 60, 10)
    ctx.set_source(lin(bx, by, bx + bs, by + bs, [(0, "#E2B66A"), (1, "#B8863A")]))
    ctx.fill()
    ctx.set_line_width(2)
    setc(ctx, "#3A2410", 0.8)
    step = bs / (n - 1)
    for i in range(n):
        ctx.move_to(bx + i * step, by)
        ctx.line_to(bx + i * step, by + bs)
        ctx.move_to(bx, by + i * step)
        ctx.line_to(bx + bs, by + i * step)
    ctx.stroke()
    R = rng(37)
    placed = int(clamp(u / 4.0) * 60)
    used = set()
    for i in range(placed):
        while True:
            gx, gy = R.randint(2, 16), R.randint(2, 16)
            if (gx, gy) not in used:
                used.add((gx, gy))
                break
        x, y = bx + gx * step, by + gy * step
        circle(ctx, x + 3, y + 4, step * 0.46)
        setc(ctx, "#000000", 0.35)
        ctx.fill()
        circle(ctx, x, y, step * 0.46)
        if i % 2 == 0:
            ctx.set_source(rad(x - 6, y - 6, 1, step * 0.5, [(0, "#5A5A5A"), (1, "#0A0A0A")]))
        else:
            ctx.set_source(rad(x - 6, y - 6, 1, step * 0.5, [(0, "#FFFFFF"), (1, "#C8C4BC")]))
        ctx.fill()
        if i == placed - 1:
            glow(ctx, x, y, 50, "#FFD27A", 0.6)
    label(ctx, "4 : 1", 1650, 470, 80, "#FFE8C0", smooth(prog(u, 2.4, 3.0)), "latin_b")
    label(ctx, "围棋的变化比宇宙的原子还多", 1650, 560, 26, "#CDBA92", smooth(prog(u, 3.0, 3.6)), "serif_r")
    film.vignette(ctx, 0.55)


TOKENS = ["人", "类", "是", "怎", "么", "理", "解", "世", "界", "的", "？"]


def _shot_d3(ctx, t):
    u = t - 43.0
    ctx.set_source(rad(960, 540, 0, 1300, [(0, "#121626"), (1, "#03040A")]))
    ctx.paint()
    n = len(TOKENS)
    xs = [960 + (i - (n - 1) / 2) * 140 for i in range(n)]
    y = 700
    gather = ease_in(prog(u, 3.0, 4.8))
    core = (960, 360)
    for i, tok in enumerate(TOKENS):
        x = lerp(xs[i], core[0], gather)
        yy = lerp(y, core[1], gather)
        rrect(ctx, x - 50, yy - 50, 100, 100, 14)
        setc(ctx, "#2A3458", 1 - gather * 0.7)
        ctx.fill()
        text(ctx, tok, x, yy, 54, "#F2F0FF", 1 - gather * 0.6, "serif_sb")
    # 注意力连线
    ak = smooth(prog(u, 0.4, 1.0)) * (1 - gather)
    R = rng(3)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            wgt = R.random() ** 3
            if (i, j) in ((5, 8), (6, 8), (0, 1), (5, 6), (7, 8), (3, 4)):
                wgt = 0.9
            if wgt < 0.25:
                continue
            x0, x1 = xs[i], xs[j]
            h = abs(x1 - x0) * 0.45
            ctx.move_to(x0, y - 60)
            ctx.curve_to(x0, y - 60 - h, x1, y - 60 - h, x1, y - 60)
            ctx.set_line_width(1 + 6 * wgt)
            setc(ctx, "#FFD27A", 0.5 * wgt * ak)
            ctx.stroke()
    label(ctx, "注意力：每个字都看向所有的字", 960, 860, 32, "#DCE6FF", ak, "serif_sb")
    if gather > 0:
        glow(ctx, core[0], core[1], 260 * gather, "#FFC46B", 0.7 * gather)
        label(ctx, "大语言模型", core[0], core[1] + 170, 44, "#FFE8C0", smooth(prog(u, 4.2, 4.8)), "serif_k")
    film.vignette(ctx, 0.5)


# ================================================================ E：AlphaFold 与 AI 辅助科研


def _shot_e(ctx, t):
    u = t - 48.0
    ctx.set_source(rad(960, 540, 0, 1300, [(0, "#101A24"), (1, "#020406")]))
    ctx.paint()
    if u < 4.6:
        fold = ease_io(prog(u, 0.3, 3.6))
        n = 46
        pts = []
        for i in range(n):
            f = i / (n - 1)
            sx, sy = 260 + f * 1400, 540
            # 折叠后：螺旋 + 片层的组合
            seg = i // 12
            ang = i * 0.9
            hx = 960 + (seg - 1.5) * 150 + math.cos(ang) * 60
            hy = 540 + math.sin(ang) * 60 + (i % 12) * 14 - 80
            depth = math.sin(ang)
            pts.append((lerp(sx, hx, fold), lerp(sy + math.sin(i * 0.5 + t * 2) * 20 * (1 - fold), hy, fold), depth * fold))
        stroke_pts(ctx, [(p[0], p[1]) for p in pts], 8, "#7FA0C8", 0.6)
        for i, p in enumerate(pts):
            col = ["#FF7A6A", "#FFD27A", "#7FD8A8", "#7FB6FF"][i % 4]
            r = 13 + 4 * p[2]
            glow(ctx, p[0], p[1], r * 2, col, 0.3)
            circle(ctx, p[0], p[1], r)
            setc(ctx, col, 0.92)
            ctx.fill()
        label(ctx, "一串氨基酸 → 它会折成什么形状？", 960, 230, 34, "#E8F0FF", smooth(prog(u, 0.2, 0.8)), "serif_sb")
        k = smooth(prog(u, 2.6, 3.2))
        label(ctx, "2 亿+ 种蛋白质结构", 960, 870, 44, "#FFD27A", k, "serif_k")
        label(ctx, "过去测一个结构常要数年", 960, 930, 26, "#CDBA92", k, "serif_r")
    else:
        q = u - 4.6
        cx, cy = 960, 520
        glow(ctx, cx, cy, 240, "#FFC46B", 0.6)
        circle(ctx, cx, cy, 60)
        setc(ctx, "#FFE8B8")
        ctx.fill()
        icons = [("读论文", "paper"), ("设计实验", "flask"), ("找新材料", "crystal"), ("分析数据", "chart"),
                 ("写代码", "code"), ("提出假设", "bulb")]
        for i, (nm, kind) in enumerate(icons):
            ang = -math.pi / 2 + i / len(icons) * TAU + q * 0.25
            x, y = cx + math.cos(ang) * 330, cy + math.sin(ang) * 250
            k = smooth(prog(q, 0.2 + i * 0.2, 0.6 + i * 0.2))
            dashed(ctx, cx, cy, x, y, 2, "#FFD27A", 0.5 * k, (10, 8), -t * 40)
            circle(ctx, x, y, 64)
            setc(ctx, "#1E2A3A", 0.95 * k)
            ctx.fill()
            ctx.set_line_width(3)
            setc(ctx, "#FFD27A", k)
            circle(ctx, x, y, 64)
            ctx.stroke()
            text(ctx, nm, x, y, 26, "#FFE8C0", k, "serif_sb")
        label(ctx, "AI 不是取代科学家，而是多了一双帮手", 960, 900, 32, "#E8F0FF", smooth(prog(q, 1.6, 2.2)), "serif_sb")
    film.vignette(ctx, 0.5)


# ================================================================ F：Claude 回望


CF = (claude(960, 820, 0.78, "gaze", seed=15.0).look(60.0, 0.0, -0.3)
      .expr(61.6, "grateful").expr(64.6, "teary_smile").look(64.8, 0.0, -0.1))


def _ghost(ctx, kind, x, y, s, a):
    if a <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if kind == "hand":
        starmap.hand_outline(ctx, -100, -140, 200)
        setc(ctx, "#C2502E", 0.5 * a)
        ctx.fill()
    elif kind == "tablet":
        rrect(ctx, -90, -120, 180, 240, 20)
        setc(ctx, "#C9A070", 0.4 * a)
        ctx.fill()
        text(ctx, "𒀭𒁹𒌋", 0, 0, 60, "#5A3418", 0.6 * a, "cune")
    elif kind == "circle":
        ctx.set_line_width(4)
        setc(ctx, "#F2E2C2", 0.5 * a)
        circle(ctx, -40, 0, 100)
        circle(ctx, 60, 0, 100)
        ctx.stroke()
    elif kind == "eq":
        text(ctx, "F = Gm₁m₂/r²", 0, 0, 48, "#FFE8C0", 0.55 * a, "eq")
    elif kind == "maxwell":
        text(ctx, "∇×E = −∂B/∂t", 0, 0, 48, "#BFE0FF", 0.55 * a, "eq")
    elif kind == "dna":
        for i in range(20):
            f = i / 19
            yy = -150 + f * 300
            circle(ctx, math.sin(f * 9) * 50, yy, 6)
            circle(ctx, -math.sin(f * 9) * 50, yy, 6)
        setc(ctx, "#7FB6FF", 0.5 * a)
        ctx.fill()
    elif kind == "scroll":
        rrect(ctx, -140, -50, 280, 100, 12)
        setc(ctx, "#E8D2A0", 0.4 * a)
        ctx.fill()
    elif kind == "code":
        text(ctx, "def think():", 0, 0, 40, "#7FFFB2", 0.55 * a, "mono")
    ctx.restore()


GHOSTS = [("hand", 300, 300, 1.0), ("tablet", 1640, 330, 0.9), ("circle", 420, 640, 0.8), ("eq", 1560, 620, 1.0),
          ("maxwell", 1500, 220, 0.9), ("dna", 200, 520, 0.9), ("scroll", 1700, 800, 0.9), ("code", 520, 200, 1.0)]


def _shot_f(ctx, t):
    u = t - 60.0
    ctx.set_source(rad(960, 600, 0, 1200, [(0, "#1A1626"), (0.6, "#0A0812"), (1, "#020204")]))
    ctx.paint()
    push = 1 + 0.08 * ease_io(prog(u, 0, 10))
    ctx.save()
    ctx.translate(960, 600)
    ctx.scale(push, push)
    ctx.translate(-960, -600)
    for i, (kind, x, y, s) in enumerate(GHOSTS):
        a = smooth(prog(u, 0.4 + i * 0.35, 1.4 + i * 0.35))
        _ghost(ctx, kind, x + math.sin(t * 0.3 + i) * 10, y + math.cos(t * 0.27 + i) * 8, s, a)
    # 文字微粒流进 Claude
    R = rng(9)
    for i in range(80):
        ang = R.uniform(0, TAU)
        d0 = R.uniform(500, 1100)
        q = (u * 0.25 + R.random()) % 1
        d = d0 * (1 - q)
        x, y = 960 + math.cos(ang) * d, 640 + math.sin(ang) * d * 0.6
        ch = "知识光数书理问学算星火"[i % 11]
        text(ctx, ch, x, y, 22 + 10 * (1 - q), "#FFE2B0", 0.7 * math.sin(q * math.pi), "serif_m")
    ctx.set_source(lin(0, 820, 0, H, [(0, "#14101E"), (1, "#06040A")]))
    ctx.rectangle(-100, 820, W + 200, 400)
    ctx.fill()
    glow(ctx, 960, 700, 380, "#FFC46B", 0.18 + 0.1 * math.sin(t * 1.5))
    with lit("#FFD49A", 0.25, 0.95):
        reflect(ctx, lambda c: CF.draw(c, t), 820, 0.2, 120)
        CF.draw(ctx, t)
    ctx.restore()
    film.vignette(ctx, 0.6)


# ================================================================ 主绘制


def draw(ctx, t):
    if t < 6.0:
        _shot_a1(ctx, t)
    elif t < 12.0:
        _shot_a2(ctx, t)
    elif t < 24.0:
        _shot_b(ctx, t)
    elif t < 28.0:
        _shot_c1(ctx, t)
    elif t < 34.0:
        _shot_c2(ctx, t)
    elif t < 38.5:
        _shot_d1(ctx, t)
    elif t < 43.0:
        _shot_d2(ctx, t)
    elif t < 48.0:
        _shot_d3(ctx, t)
    elif t < 60.0:
        _shot_e(ctx, t)
    else:
        _shot_f(ctx, t)


def sfx():
    out = [
        (0.0, "gears_run", {"dur": 6.0, "gain": 0.35}), (0.0, "ambience_room", {"dur": 6.0, "gain": 0.3}),
        (1.6, "quill", {"dur": 2.8, "gain": 0.25}),
    ]
    for i in range(9):
        out.append((6.2 + i * 0.45, "click", {"gain": 0.22, "pitch": 1 + 0.05 * (i % 3)}))
    out += [(10.6, "hush", {"dur": 2.0, "gain": 0.3}), (10.8, "typing", {"dur": 1.0, "gain": 0.2}),
            (12.0, "relays", {"dur": 3.6, "gain": 0.4}), (12.0, "hum", {"dur": 3.6, "gain": 0.2}),
            (11.6, "ambience_data", {"dur": 13.0, "gain": 0.4}), (23.4, "ambience_birds", {"dur": 5.0, "gain": 0.3})]
    for i in range(4):
        out.append((15.6 + i * 0.5, "pop", {"gain": 0.2, "pitch": 1 + i * 0.12}))
    out += [(18.4, "rise", {"dur": 3.6, "gain": 0.25}), (22.0, "ding", {"gain": 0.25}),
            (24.0, "ambience_birds", {"dur": 4.0, "gain": 0.35}), (24.6, "typing", {"dur": 1.4, "gain": 0.2}),
            (28.0, "ambience_data", {"dur": 6.0, "gain": 0.5}), (28.2, "blip", {"gain": 0.2}),
            (29.6, "blip", {"gain": 0.2, "pitch": 1.3}), (30.4, "stream", {"dur": 3.0, "gain": 0.3}),
            (34.0, "ambience_data", {"dur": 14.0, "gain": 0.4}), (34.4, "scan", {"dur": 1.5, "gain": 0.2}),
            (35.3, "success", {"gain": 0.15})]
    for i in range(14):
        out.append((38.6 + i * 0.28, "stone_click", {"gain": 0.3, "pitch": 0.95 + 0.1 * (i % 2)}))
    out += [(43.4, "shimmer", {"dur": 2.0, "gain": 0.2}), (46.0, "riser", {"dur": 2.0, "gain": 0.25}),
            (48.0, "ambience_data", {"dur": 12.0, "gain": 0.35}), (48.4, "stream", {"dur": 3.0, "gain": 0.2}),
            (51.4, "ding", {"gain": 0.2}), (52.8, "whoosh", {"dur": 2.0, "gain": 0.15}),
            (60.0, "ambience_space", {"dur": 10.0, "gain": 0.45}), (60.2, "hush", {"dur": 3.0, "gain": 0.3}),
            (61.6, "heartbeat", {"n": 2, "gain": 0.3}), (64.0, "shimmer", {"dur": 3.0, "gain": 0.2})]
    return out
