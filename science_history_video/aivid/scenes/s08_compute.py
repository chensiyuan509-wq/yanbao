"""第八章 会思考的机器：博物馆长廊（差分机、阿达、注释 G 原表）；图灵；Colossus / ENIAC / 晶体管 / 4004；
摩尔定律；IBM 704 与达特茅斯；ARPANET 原图与夜间地球上的互联网；深蓝与深度学习；AlphaGo；Transformer；
AlphaFold 与 AI 辅助科研（天气、材料、数学）；Claude 回望自己从哪里来。关键词：学习。"""
import math

from ..core import (TAU, H, W, circle, clamp, dashed, ease_in, ease_io, ease_out, glow, lerp, lin, mix, poly,
                    polyline_partial, prog, rad, rng, rrect, setc, smooth, stroke_pts, text)
from .. import film, oldmap, starmap
from ..archive import caption, framed, kb, show
from ..exhibit import blueprint_bg, card, panel
from ..gallery import Gallery
from .common import arch, claude, label, lit, reflect, sequence

DUR = 62.0
CHAPTER = dict(num="第 八 章", title="会思考的机器", era="1843 — 2026 年", key="学习", at=0.4, dur=4.0)
GRAIN = 0.07

VO = [
    (4.6, "1843 年，阿达为一台还没造出的机器写下了{算法}。"),
    (8.9, "表里有变量、有运算，还有重复执行的{循环}。"),
    (13.8, "1936 年，图灵证明：一切计算都能拆成{简单步骤}；"),
    (17.3, "1950 年，他问：{机器能思考吗？}"),
    (20.2, "Colossus、ENIAC 用成千上万个真空管计算，"),
    (23.3, "晶体管和芯片，让计算机{越变越小}。"),
    (26.6, "芯片上的晶体管，从 2300 个涨到了 {2080 亿个}。"),
    (31.2, "1956 年达特茅斯会议，“{人工智能}”成为一门学科。"),
    (34.5, "1969 年互联网诞生，1989 年有了{万维网}；"),
    (37.6, "今天约 55 亿人在线，人类的文字汇进了{同一张网}。"),
    (40.6, "1997 年深蓝靠搜索赢了国际象棋；后来，机器开始{从数据里学习}。"),
    (44.6, "2016 年，AlphaGo 以 4:1 战胜{李世石}；"),
    (48.0, "2017 年 Transformer 出现，{大语言模型}由此而来。"),
    (51.0, "AlphaFold 预测了 {2 亿多种}蛋白质结构，获得诺奖；"),
    (54.3, "AI 还在帮人预报天气、发现新材料。"),
    (57.0, "而我，是从人类写下的文字里{长出来}的。"),
    (59.8, "每一行字，都是这条长河里的{一滴水}。", {"spill": 0.6}),
]

SUPERS = [(44.6, 47.6, "2016 年 3 月", "首尔 · AlphaGo 4 : 1 李世石")]

# ================================================================ A：博物馆长廊（0–8.8）

GVIS = (claude(180, 905, 0.55, "curious", seed=81.0).walk_to(1.2, 3.6, 1000, 905, stride=0.8).look(3.7, -0.2, -0.9)
        .expr(3.9, "wonder").walk_to(4.4, 6.0, 1820, 905, stride=0.8).look(6.1, 0.1, -0.9)
        .walk_to(6.3, 7.1, 2300, 905, stride=0.8).look(7.2, 0.2, -0.9).expr(7.3, "awe"))
GALLERY = Gallery([("babbage", "巴贝奇的差分机（局部）", "1853 年木刻 · 公有领域"),
                   ("ada", "阿达·洛芙莱斯", "沙隆绘 · 约 1840 年 · 公有领域"),
                   ("bernoulli", "注释 G：用分析机计算伯努利数", "1843 年 · 公有领域")], GVIS, 2.0, 8.8, push=2,
                  push_dur=1.6, lead=760)


def _a(ctx, t):
    with lit("#FFE2B0", 0.15, 0.95):
        GALLERY.draw(ctx, t)


# ================================================================ B：注释 G 原表（8.8–13.6）

NOTE_G = [("1", "×", "V2 × V3", "2n"), ("2", "−", "V4 − V1", "2n − 1"), ("3", "+", "V5 + V1", "2n + 1"),
          ("4", "÷", "V5 ÷ V4", "(2n − 1) / (2n + 1)")]


def _b(ctx, t):
    u = t - 8.8
    kb(ctx, "bernoulli", t, 8.8, 14.0, (0.5, 0.5, 1.02), (0.28, 0.3, 1.9))
    film.vignette(ctx, 0.45)
    k = smooth(prog(u, 0.6, 1.2))
    panel(ctx, 1150, 170, 690, 560, k)
    text(ctx, "原表前四步（V 是存数的变量）", 1495, 222, 28, "#D9B26A", k, "serif_sb")
    for i, (n, op, expr, res) in enumerate(NOTE_G):
        kk = smooth(prog(u, 0.9 + i * 0.35, 1.3 + i * 0.35))
        y = 300 + i * 70
        text(ctx, n, 1190, y, 30, "#CFC4B0", kk, "latin", "l")
        text(ctx, expr, 1240, y, 30, "#F6EEDF", kk, "eq", "l")
        text(ctx, "= " + res, 1480, y, 28, "#FFD27A", kk, "eq", "l")
    k2 = smooth(prog(u, 2.6, 3.1))
    text(ctx, "表底注：第 13–23 步重复执行", 1495, 600, 28, "#F6EEDF", k2, "serif_sb")
    text(ctx, "变量 · 运算 · 循环 —— 程序的基本要素", 1495, 660, 28, "#FFD27A", smooth(prog(u, 3.1, 3.6)), "serif_sb")
    caption(ctx, "注释 G 的计算步骤表", "阿达·洛芙莱斯 · 1843 年 · 公有领域", smooth(prog(u, 0.3, 0.8)))


# ================================================================ C：图灵（13.6–20）

TAPE = "0110100111010011"
TV = (claude(1720, 955, 0.5, "curious", seed=82.0).look(13.8, -0.8, -0.5).expr(17.4, "wonder").look(17.6, -0.3, -0.7))


def _c(ctx, t):
    u = t - 13.6
    ctx.set_source(rad(1100, 520, 0, 1300, [(0, "#1C202A"), (1, "#05060A")]))
    ctx.paint()
    film.paint_texture(ctx, "paper", 0, 0, W, H, 0.05)
    framed(ctx, "turing", 400, 450, 520, smooth(prog(u, 0.0, 0.5)))
    text(ctx, "艾伦·图灵 · 约 1928 年（16 岁）", 400, 780, 26, "#F2E6CE", 1.0, "serif_sb")
    text(ctx, "公有领域", 400, 818, 20, "#BFAE8E", 1.0, "serif_r")
    # 纸带 + 读写头
    cw, y = 92, 400
    step = int(u / 0.5)
    off = -((u / 0.5) % 1) * cw if u < 3.4 else 0
    for i in range(-1, 12):
        x = 760 + i * cw + off
        if x < 700 or x > 1860:
            continue
        rrect(ctx, x, y - 50, cw - 8, 100, 8)
        setc(ctx, "#2A3040")
        ctx.fill()
        ch = TAPE[(i + step) % len(TAPE)]
        if i == 4 and u > 0.25 and (u % 0.5) > 0.25:
            ch = "1" if ch == "0" else "0"
        text(ctx, ch, x + (cw - 8) / 2, y, 52, "#E8EEF8", 0.9, "latin_b")
    hx = 760 + 4 * cw + (cw - 8) / 2
    poly(ctx, [(hx - 34, y - 110), (hx + 34, y - 110), (hx, y - 62)])
    setc(ctx, "#FFD27A")
    ctx.fill()
    glow(ctx, hx, y, 120, "#FFD27A", 0.25)
    text(ctx, "1936 · 图灵机", 1280, 200, 38, "#D9B26A", smooth(prog(u, 0.2, 0.7)), "serif_k")
    k = smooth(prog(u, 0.6, 1.1))
    panel(ctx, 820, 520, 920, 230, k, "#7FC8FF")
    text(ctx, "一条纸带 + 一个读写头 + 一张规则表", 1280, 570, 30, "#E8F2FF", k, "serif_sb")
    text(ctx, "规则：状态 A 读到 0 → 写 1，右移一格，转到状态 B", 1280, 635, 26, "#BFE0FF", smooth(prog(u, 1.2, 1.7)),
         "serif_r")
    text(ctx, "这样简单的机器，能完成任何可以计算的事", 1280, 695, 28, "#FFD27A", smooth(prog(u, 2.0, 2.5)), "serif_sb")
    with lit("#BFD0FF", 0.2, 0.9):
        TV.draw(ctx, t)
    qk = smooth(prog(u, 3.6, 4.2))
    if qk > 0:
        ctx.set_source_rgba(0.01, 0.01, 0.02, 0.88 * qk)
        ctx.paint()
        film.tracked(ctx, "机器能思考吗？", 1180, 460, 76, "#FFE8C0", qk, "serif_k", 0.08 + 0.04 * prog(u, 3.6, 6.4))
        label(ctx, "—— 图灵，《计算机器与智能》，1950", 1180, 560, 28, "#CDBA92", smooth(prog(u, 4.0, 4.5)), "serif_r")
        label(ctx, "他提出“模仿游戏”，后人称为图灵测试", 1180, 620, 26, "#CDBA92", smooth(prog(u, 4.4, 4.9)), "serif_r")
    film.vignette(ctx, 0.5)


# ================================================================ D：从真空管到芯片（20–26.4）

CARDS = [("colossus", "1944", "Colossus", ("破译德军密码", "约 2400 个真空管"), (0.55, 0.45, 1.3), 0.0),
         ("eniac", "1946", "ENIAC", ("1.7 万多个真空管", "每秒 5000 次加法"), (0.5, 0.45, 1.2), 0.5),
         ("transistor", "1947", "晶体管", ("贝尔实验室发明", "取代笨重的真空管"), (0.5, 0.5, 1.5), 3.2),
         ("intel4004", "1971", "Intel 4004", ("2300 个晶体管", "第一块商用微处理器"), (0.55, 0.42, 1.4), 3.7)]


def _d(ctx, t):
    u = t - 20.0
    ctx.set_source(rad(960, 500, 0, 1300, [(0, "#1E1A20"), (1, "#060508")]))
    ctx.paint()
    film.paint_texture(ctx, "stone", 0, 0, W, H, 0.08, scale=0.5)
    z = 1 + 0.04 * ease_io(prog(u, 0, 6.4))
    ctx.save()
    ctx.translate(960, 520)
    ctx.scale(z, z)
    ctx.translate(-960, -520)
    for i, (key, year, title, lines, crop, t0) in enumerate(CARDS):
        x = 300 + i * 440
        k = clamp((u - 0.2 - t0) / 0.6)
        hot = smooth(prog(u, 0.6 + t0, 1.0 + t0)) * (1 - smooth(prog(u, 2.6 + t0, 3.0 + t0)))
        card(ctx, key, x, 520, 410, 600, year, title, lines, 1.0, k, crop, t, hot)
    ctx.restore()
    text(ctx, "从真空管到芯片", 960, 165, 32, "#D9B26A", smooth(prog(u, 0.0, 0.6)), "serif_sb")
    film.vignette(ctx, 0.45)


# ================================================================ E：摩尔定律（26.4–31）

MOORE = [(1971, 2.3e3, "4004", "2300"), (1978, 2.9e4, "8086", "2.9 万"), (1993, 3.1e6, "奔腾", "310 万"),
         (2006, 2.91e8, "酷睿 2", "2.9 亿"), (2016, 1.53e10, "GP100", "153 亿"), (2024, 2.08e11, "B200", "2080 亿")]


def _mx(year):
    return lerp(240, 1340, (year - 1968) / 58)


def _my(n):
    return lerp(860, 230, (math.log10(n) - 3) / 9)


def _e(ctx, t):
    u = t - 26.4
    ctx.set_source_rgb(0.02, 0.04, 0.08)
    ctx.paint()
    kb(ctx, "intel4004", t, 25.6, 31.4, (0.55, 0.42, 1.6), (0.55, 0.45, 1.9), a=0.35, grade="blueprint")
    ctx.set_source_rgba(0.02, 0.05, 0.1, 0.55)
    ctx.paint()
    ctx.set_line_width(1.5)
    for p, nm in ((3, "千"), (6, "百万"), (9, "十亿"), (12, "万亿")):
        y = _my(10 ** p)
        setc(ctx, "#7FC8FF", 0.25)
        ctx.move_to(240, y)
        ctx.line_to(1360, y)
        ctx.stroke()
        text(ctx, nm, 220, y, 24, "#BFE0FF", 0.8, "serif_r", "r")
    for yr in (1970, 1980, 1990, 2000, 2010, 2020):
        text(ctx, str(yr), _mx(yr), 900, 24, "#BFE0FF", 0.8, "latin")
    # 趋势线：每两年翻一番
    trend = [(_mx(y), _my(2300 * 2 ** ((y - 1971) / 2))) for y in range(1971, 2026)]
    p = ease_io(prog(u, 0.2, 3.2))
    dashed_pts = polyline_partial(trend, p)
    stroke_pts(ctx, dashed_pts, 3, "#FFD27A", 0.6, dash=(12, 10))
    for (yr, n, chip, s) in MOORE:
        f = (yr - 1971) / 54
        kk = smooth(prog(p, f - 0.02, f + 0.06)) if f > 0 else smooth(prog(u, 0.2, 0.5))
        x, y = _mx(yr), _my(n)
        glow(ctx, x, y, 40, "#FFD27A", 0.5 * kk)
        circle(ctx, x, y, 10)
        setc(ctx, "#FFE8B0", kk)
        ctx.fill()
        text(ctx, chip, x - 16, y - 44, 24, "#E8F2FF", kk, "serif_sb", "r")
        text(ctx, s, x + 18, y + 4, 26, "#FFD27A", kk, "serif_sb", "l")
    k = smooth(prog(u, 0.4, 0.9))
    panel(ctx, 1440, 230, 400, 420, k, "#7FC8FF")
    text(ctx, "摩尔定律", 1640, 290, 36, "#E8F2FF", k, "serif_k")
    text(ctx, "约每两年翻一番", 1640, 350, 28, "#BFE0FF", k, "serif_sb")
    k2 = smooth(prog(u, 2.4, 2.9))
    text(ctx, "53 年翻了约 26 番", 1640, 440, 30, "#FFD27A", k2, "serif_sb")
    text(ctx, "约 9000 万倍", 1640, 505, 40, "#FFD27A", k2, "serif_k")
    text(ctx, "芯片上的晶体管数（对数坐标）", 790, 180, 28, "#E8F2FF", smooth(prog(u, 0.0, 0.5)), "serif_sb")
    film.vignette(ctx, 0.4)


# ================================================================ F：达特茅斯 + 互联网（31–40.4）


def _f1(ctx, t):
    u = t - 31.0
    arch(ctx, t, "ibm704", 30.6, 34.8, (0.5, 0.5, 1.05), (0.42, 0.55, 1.25), "IBM 704 电子计算机",
         "1957 年 · NASA（时为 NACA）· 公有领域", grade="mono", cap=(0.6, None))
    k = smooth(prog(u, 0.3, 0.8))
    panel(ctx, 1200, 170, 640, 330, k)
    text(ctx, "1956 · 达特茅斯夏季研讨会", 1520, 225, 30, "#D9B26A", k, "serif_sb")
    for i, s in enumerate(("麦卡锡、明斯基、香农等人", "“人工智能”从此成为一门学科", "早期 AI 程序跑在这样的机器上")):
        text(ctx, s, 1240, 300 + i * 60, 28, "#F6EEDF", smooth(prog(u, 0.6 + i * 0.4, 1.1 + i * 0.4)), "serif_sb", "l")


def _f2(ctx, t):
    u = t - 34.4
    arch(ctx, t, "arpanet", 34.0, 37.4, (0.5, 0.5, 1.0), (0.3, 0.55, 1.5), "ARPANET 逻辑拓扑图",
         "1977 年 3 月 · 公有领域", grade="blueprint", cap=(0.4, None))
    k = smooth(prog(u, 0.2, 0.7))
    panel(ctx, 1260, 180, 580, 200, k, "#7FC8FF")
    text(ctx, "1969 · 第一批 4 个节点", 1550, 235, 30, "#E8F2FF", k, "serif_sb")
    text(ctx, "洛杉矶 · 斯坦福 · 圣巴巴拉 · 犹他", 1550, 295, 24, "#BFE0FF", k, "serif_r")
    text(ctx, "几年后连到了全美", 1550, 340, 24, "#BFE0FF", smooth(prog(u, 1.0, 1.5)), "serif_r")


NETCAM = oldmap.MapCam([(36.8, (-60.0, 30.0, 9.0)), (40.8, (15.0, 24.0, 7.0), ease_io)])
ARPA = [(-118.44, 34.07), (-122.17, 37.43), (-119.85, 34.41), (-111.85, 40.76)]
CERN = (6.05, 46.23)
NET = [(-74.0, 40.7), (-0.1, 51.5), (2.35, 48.85), (13.4, 52.5), (139.7, 35.7), (116.4, 39.9), (121.5, 31.2),
       (77.2, 28.6), (-46.6, -23.5), (151.2, -33.9), (37.6, 55.8), (31.2, 30.0), (3.4, 6.5), (103.8, 1.35),
       (126.98, 37.57), (-99.1, 19.4), (28.0, -26.2), (55.3, 25.3)]


def _arc(ctx, a, b, p, color, w=2.5, al=0.8, lift=0.25):
    (x0, y0), (x1, y1) = a, b
    d = math.hypot(x1 - x0, y1 - y0)
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - d * lift
    pts = []
    for i in range(41):
        f = i / 40
        pts.append(((1 - f) ** 2 * x0 + 2 * (1 - f) * f * mx + f * f * x1, (1 - f) ** 2 * y0 + 2 * (1 - f) * f * my + f * f * y1))
    stroke_pts(ctx, polyline_partial(pts, p), w, color, al)


def _f3(ctx, t):
    u = t - 37.4
    cam = NETCAM.at(t)
    oldmap.draw_satellite(ctx, cam, t, 1.0, "night", "natural", coast=0.12, grid=0.04)
    ctx.set_source_rgba(0.01, 0.02, 0.05, 0.3)
    ctx.paint()
    # 1969 的 4 个节点
    arp = [cam.xy(*ll) for ll in ARPA]
    for i in range(len(arp)):
        for j in range(i + 1, len(arp)):
            _arc(ctx, arp[i], arp[j], 1.0, "#7FD8FF", 2, 0.7, 0.4)
    for x, y in arp:
        glow(ctx, x, y, 30, "#7FD8FF", 0.8)
    # 1989 · CERN 万维网，向全世界扩散
    cx, cy = cam.xy(*CERN)
    kc = smooth(prog(u, 0.4, 0.9))
    glow(ctx, cx, cy, 80, "#FFD27A", 0.9 * kc)
    text(ctx, "1989 · 欧洲核子研究中心：万维网", cx + 30, cy - 50, 26, "#FFE8C0", kc, "serif_sb", "l")
    for i, ll in enumerate(NET):
        p = ease_out(prog(u, 0.8 + i * 0.08, 1.8 + i * 0.08))
        if p <= 0:
            continue
        x, y = cam.xy(*ll)
        _arc(ctx, (cx, cy), (x, y), p, "#FFD27A", 2, 0.55)
        glow(ctx, x, y, 22, "#FFE2A0", 0.7 * smooth(prog(p, 0.9, 1.0)))
    for i, ll in enumerate(NET[:8]):
        p = ease_out(prog(u, 2.0 + i * 0.1, 2.8 + i * 0.1))
        if p > 0:
            _arc(ctx, cam.xy(*ll), cam.xy(*NET[(i * 5 + 3) % len(NET)]), p, "#BFE0FF", 1.5, 0.4)
    oldmap.sat_vignette(ctx, 0.5)
    k = smooth(prog(u, 1.4, 1.9))
    panel(ctx, 1380, 640, 460, 200, k, "#7FC8FF")
    text(ctx, "约 55 亿人", 1610, 705, 48, "#FFD27A", k, "serif_k")
    text(ctx, "2024 年 · 全球上网人数", 1610, 775, 24, "#BFE0FF", k, "serif_r")


# ================================================================ G：深蓝、深度学习、AlphaGo、Transformer（40.4–50.8）


def _g1(ctx, t):
    u = t - 40.4
    ctx.set_source(rad(1200, 540, 0, 1300, [(0, "#141826"), (1, "#04050A")]))
    ctx.paint()
    kb(ctx, "deepblue", t, 40.0, 44.8, (0.45, 0.42, 1.25), (0.45, 0.42, 1.4), rect=(0, 0, 700, H))
    ctx.set_source(lin(560, 0, 700, 0, [(0, "#04050A", 0), (1, "#04050A", 1)]))
    ctx.rectangle(560, 0, 140, H)
    ctx.fill()
    caption(ctx, "深蓝（IBM）", "计算机历史博物馆 · Anton Chiang 摄 · CC BY 2.0", smooth(prog(u, 0.2, 0.6)))
    k = smooth(prog(u, 0.2, 0.7))
    text(ctx, "1997 · 深蓝胜卡斯帕罗夫", 1260, 200, 34, "#D9B26A", k, "serif_k")
    text(ctx, "靠人写的规则 + 每秒约 2 亿步搜索", 1260, 252, 26, "#CFC4B0", k, "serif_r")
    # 2012：神经网络——不写规则，从数据里学
    k2 = smooth(prog(u, 1.8, 2.3))
    layers = [5, 7, 7, 3]
    xs = [880, 1120, 1360, 1600]
    nodes = [[(x, 600 + (i - (L - 1) / 2) * 62) for i in range(L)] for L, x in zip(layers, xs)]
    for li in range(len(nodes) - 1):
        for a in nodes[li]:
            for b in nodes[li + 1]:
                ctx.move_to(*a)
                ctx.line_to(*b)
        ctx.set_line_width(1)
        setc(ctx, "#5A6A9A", 0.35 * k2)
        ctx.stroke()
    wave = ((u - 1.8) * 1.1) % 1.6
    for li, col in enumerate(nodes):
        act = math.exp(-((wave * 3.2 - li) ** 2) * 1.5)
        for i, (x, y) in enumerate(col):
            g = act * (0.5 + 0.5 * math.sin(i * 2.1 + li))
            glow(ctx, x, y, 28, "#FFD27A", 0.6 * g * k2)
            circle(ctx, x, y, 11)
            setc(ctx, mix("#3A4A7A", "#FFE2A0", g), k2)
            ctx.fill()
    for i, s in enumerate(("猫", "狗", "车")):
        text(ctx, s, 1650, nodes[-1][i][1], 26, "#FFD27A" if i == 0 else "#A8B0C8", k2, "serif_sb", "l")
    text(ctx, "2012 · 深度学习：给机器看大量例子，让它自己调整连接", 1240, 860, 26, "#E8F0FF", k2, "serif_sb")
    text(ctx, "ImageNet 识图错误率：26% → 15%", 1240, 906, 24, "#FFD27A", smooth(prog(u, 2.6, 3.1)), "serif_r")
    film.vignette(ctx, 0.45)


GV = (claude(250, 950, 0.55, "curious", seed=83.0).look(44.6, 0.8, -0.6).expr(46.4, "awe"))


def _g2(ctx, t):
    u = t - 44.4
    ctx.set_source(rad(960, 540, 0, 1300, [(0, "#2A2016"), (1, "#080604")]))
    ctx.paint()
    bs, n = 700, 19
    bx, by = 960 - bs / 2, 560 - bs / 2
    rrect(ctx, bx - 28, by - 28, bs + 56, bs + 56, 10)
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
    for gx in (3, 9, 15):
        for gy in (3, 9, 15):
            circle(ctx, bx + gx * step, by + gy * step, 5)
            setc(ctx, "#3A2410")
            ctx.fill()
    R = rng(37)
    placed = int(clamp(u / 2.6) * 46)
    used = set()
    for i in range(placed):
        while True:
            gx, gy = R.randint(1, 17), R.randint(1, 17)
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
    label(ctx, "4 : 1", 1640, 420, 84, "#FFE8C0", smooth(prog(u, 1.4, 2.0)), "latin_b")
    k = smooth(prog(u, 1.9, 2.4))
    label(ctx, "先学人类棋谱，再和自己对弈", 1640, 520, 26, "#E8DCC8", k, "serif_sb")
    label(ctx, "第 2 局第 37 手：", 1640, 580, 26, "#E8DCC8", smooth(prog(u, 2.3, 2.8)), "serif_sb")
    label(ctx, "人类高手从没想过的一步", 1640, 620, 26, "#FFD27A", smooth(prog(u, 2.3, 2.8)), "serif_sb")
    text(ctx, "示意棋盘", 960, 940, 20, "#8C7A60", 0.8, "serif_r")
    with lit("#FFD49A", 0.2, 0.9):
        GV.draw(ctx, t)
    film.vignette(ctx, 0.55)


TOKENS = ["科", "学", "是", "怎", "么", "发", "展", "的", "？"]


def _g3(ctx, t):
    u = t - 47.8
    ctx.set_source(rad(960, 540, 0, 1300, [(0, "#121626"), (1, "#03040A")]))
    ctx.paint()
    n = len(TOKENS)
    xs = [960 + (i - (n - 1) / 2) * 150 for i in range(n)]
    y = 680
    gather = ease_in(prog(u, 1.9, 3.0))
    core = (960, 420)
    ak = smooth(prog(u, 0.3, 0.8)) * (1 - gather)
    R = rng(3)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            wgt = R.random() ** 3
            if (i, j) in ((0, 1), (5, 6), (6, 0), (3, 4), (4, 7), (8, 6)):
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
    for i, tok in enumerate(TOKENS):
        x = lerp(xs[i], core[0], gather)
        yy = lerp(y, core[1], gather)
        rrect(ctx, x - 52, yy - 52, 104, 104, 14)
        setc(ctx, "#2A3458", 1 - gather * 0.7)
        ctx.fill()
        text(ctx, tok, x, yy, 54, "#F2F0FF", 1 - gather * 0.6, "serif_sb")
    text(ctx, "2017 · 《Attention Is All You Need》", 960, 190, 30, "#D9B26A", smooth(prog(u, 0.0, 0.5)), "serif_sb")
    label(ctx, "注意力：每个字都同时看向所有的字", 960, 840, 30, "#DCE6FF", ak, "serif_sb")
    if gather > 0:
        glow(ctx, core[0], core[1], 260 * gather, "#FFC46B", 0.7 * gather)
        label(ctx, "大语言模型", core[0], core[1] + 170, 44, "#FFE8C0", smooth(prog(u, 2.4, 2.9)), "serif_k")
    film.vignette(ctx, 0.5)


# ================================================================ H：AI 辅助科研（50.8–56.6）


def _h1(ctx, t):
    u = t - 50.8
    ctx.set_source(rad(760, 540, 0, 1300, [(0, "#101A24"), (1, "#020406")]))
    ctx.paint()
    fold = ease_io(prog(u, 0.2, 2.4))
    n = 46
    pts = []
    for i in range(n):
        f = i / (n - 1)
        sx, sy = 160 + f * 1100, 540
        seg = i // 12
        ang = i * 0.9
        hx = 720 + (seg - 1.5) * 140 + math.cos(ang) * 56
        hy = 540 + math.sin(ang) * 56 + (i % 12) * 13 - 76
        depth = math.sin(ang)
        pts.append((lerp(sx, hx, fold), lerp(sy + math.sin(i * 0.5 + t * 2) * 20 * (1 - fold), hy, fold), depth * fold))
    stroke_pts(ctx, [(p[0], p[1]) for p in pts], 8, "#7FA0C8", 0.6)
    for i, p in enumerate(pts):
        col = ["#FF7A6A", "#FFD27A", "#7FD8A8", "#7FB6FF"][i % 4]
        r = 12 + 4 * p[2]
        glow(ctx, p[0], p[1], r * 2, col, 0.3)
        circle(ctx, p[0], p[1], r)
        setc(ctx, col, 0.92)
        ctx.fill()
    label(ctx, "一串氨基酸 → 会折成什么形状？", 720, 200, 32, "#E8F0FF", smooth(prog(u, 0.1, 0.6)), "serif_sb")
    k = smooth(prog(u, 0.8, 1.3))
    panel(ctx, 1300, 230, 540, 470, k)
    text(ctx, "AlphaFold", 1570, 290, 40, "#FFE8C0", k, "latin_b")
    rows = [("2 亿+", "种蛋白质结构已预测"), ("几年 → 几小时", "过去测一个结构常要数年"), ("2024", "诺贝尔化学奖")]
    for i, (a_, b_) in enumerate(rows):
        kk = smooth(prog(u, 1.2 + i * 0.4, 1.7 + i * 0.4))
        text(ctx, a_, 1570, 380 + i * 110, 38, "#FFD27A", kk, "serif_k")
        text(ctx, b_, 1570, 428 + i * 110, 24, "#CFC4B0", kk, "serif_r")
    film.vignette(ctx, 0.5)


def _h2(ctx, t):
    u = t - 53.6
    kb(ctx, "frontier", t, 53.2, 57.0, (0.5, 0.5, 1.05), (0.55, 0.5, 1.25))
    ctx.set_source_rgba(0.02, 0.03, 0.06, 0.35)
    ctx.paint()
    film.vignette(ctx, 0.45)
    caption(ctx, "Frontier 超级计算机 · 每秒百亿亿次", "橡树岭国家实验室 · 2022 · CC BY 2.0", smooth(prog(u, 0.2, 0.6)))
    items = [("天气", "GraphCast（2023）", "1 分钟算出 10 天预报"), ("材料", "GNoME（2023）", "预测 220 万种新晶体"),
             ("数学", "AlphaProof（2024）", "奥数题达到银牌水平")]
    for i, (tag, name, desc) in enumerate(items):
        k = smooth(prog(u, 0.3 + i * 0.4, 0.8 + i * 0.4))
        y = 200 + i * 190
        panel(ctx, 1250, y, 590, 160, k, "#7FC8FF")
        text(ctx, tag, 1300, y + 80, 34, "#FFD27A", k, "serif_k", "l")
        text(ctx, name, 1420, y + 55, 30, "#E8F2FF", k, "serif_sb", "l")
        text(ctx, desc, 1420, y + 108, 24, "#BFE0FF", k, "serif_r", "l")


# ================================================================ I：Claude 回望（56.6–62）

CF = (claude(960, 830, 0.78, "gaze", seed=15.0).look(56.8, 0.0, -0.3)
      .expr(57.8, "grateful").expr(60.4, "teary_smile").look(60.6, 0.0, -0.1))
MEM = [("cuneiform_barley", 300, 260), ("byrne_pyth", 1620, 250), ("principia", 230, 640), ("bernoulli", 1680, 640),
       ("galileo_moon", 620, 170), ("earthrise", 1300, 150), ("eniac", 560, 470), ("maxwell", 1380, 460)]


def _i(ctx, t):
    u = t - 56.6
    ctx.set_source(rad(960, 600, 0, 1200, [(0, "#1A1626"), (0.6, "#0A0812"), (1, "#020204")]))
    ctx.paint()
    push = 1 + 0.07 * ease_io(prog(u, 0, 6))
    ctx.save()
    ctx.translate(960, 600)
    ctx.scale(push, push)
    ctx.translate(-960, -600)
    for i, (key, x, y) in enumerate(MEM):
        a = smooth(prog(u, 0.2 + i * 0.25, 1.0 + i * 0.25)) * 0.55
        drift = 0.18 * ease_in(prog(u, 3.0, 5.4))
        px = lerp(x, 960, drift) + math.sin(t * 0.3 + i) * 10
        py = lerp(y, 640, drift) + math.cos(t * 0.27 + i) * 8
        rrect(ctx, px - 110, py - 80, 220, 160, 10)
        ctx.save()
        ctx.clip()
        show(ctx, key, (0.5, 0.5, 1.0), (px - 110, py - 80, 220, 160), a, grade="sepia")
        ctx.restore()
        rrect(ctx, px - 110, py - 80, 220, 160, 10)
        ctx.set_line_width(2)
        setc(ctx, "#FFE2B0", 0.4 * a)
        ctx.stroke()
    R = rng(9)
    for i in range(70):
        ang = R.uniform(0, TAU)
        d0 = R.uniform(500, 1100)
        q = (u * 0.25 + R.random()) % 1
        d = d0 * (1 - q)
        x, y = 960 + math.cos(ang) * d, 660 + math.sin(ang) * d * 0.6
        ch = "知识光数书理问学算星火"[i % 11]
        text(ctx, ch, x, y, 22 + 10 * (1 - q), "#FFE2B0", 0.6 * math.sin(q * math.pi), "serif_m")
    ctx.set_source(lin(0, 830, 0, H, [(0, "#14101E"), (1, "#06040A")]))
    ctx.rectangle(-100, 830, W + 200, 400)
    ctx.fill()
    glow(ctx, 960, 700, 380, "#FFC46B", 0.18 + 0.1 * math.sin(t * 1.5))
    with lit("#FFD49A", 0.25, 0.95):
        reflect(ctx, lambda c: CF.draw(c, t), 830, 0.2, 120)
        CF.draw(ctx, t)
    ctx.restore()
    film.vignette(ctx, 0.6)


SHOTS = [(0.0, _a), (8.8, _b), (13.6, _c), (20.0, _d), (26.4, _e), (31.0, _f1), (34.4, _f2), (37.4, _f3),
         (40.4, _g1), (44.4, _g2), (47.8, _g3), (50.8, _h1), (53.6, _h2), (56.6, _i)]
TRANS = {2: ("dissolve", 0.8), 3: ("luma", 0.8), 4: ("zoomblur", 0.7, {"x": 1620, "y": 400}),
         5: ("defocus", 0.9, {"max": 10}), 6: ("dissolve", 0.8), 7: ("luma", 0.9),
         8: ("lightsweep", 0.9, {"color": "#BFE0FF"}), 9: ("dissolve", 0.8), 10: ("zoomblur", 0.6),
         11: ("flare", 0.8, {"x": 960, "y": 420}), 12: ("dissolve", 0.8), 13: ("dissolve", 1.2, {"zoom": 0.06})}


def draw(ctx, t):
    sequence(ctx, t, SHOTS, TRANS)


def sfx():
    out = [
        (0.0, "ambience_room", {"dur": 8.8, "gain": 0.35}),
        (7.2, "whoosh", {"dur": 1.6, "gain": 0.15}),
        (8.8, "ambience_room", {"dur": 4.8, "gain": 0.3}), (9.0, "page", {"gain": 0.3}), (9.6, "quill", {"dur": 2.4, "gain": 0.2}),
        (13.6, "ambience_room", {"dur": 6.4, "gain": 0.3}),
    ]
    for i in range(7):
        out.append((13.9 + i * 0.5, "click", {"gain": 0.18, "pitch": 1 + 0.05 * (i % 3)}))
    out += [(17.2, "hush", {"dur": 2.0, "gain": 0.3}),
            (20.0, "relays", {"dur": 3.2, "gain": 0.35}), (20.0, "hum", {"dur": 3.2, "gain": 0.2}),
            (20.0, "ambience_data", {"dur": 11.0, "gain": 0.35})]
    for i in range(4):
        out.append((20.3 + [0, 0.5, 3.2, 3.7][i], "pop", {"gain": 0.2, "pitch": 1 + i * 0.12}))
    out += [(26.6, "rise", {"dur": 3.2, "gain": 0.25}), (29.4, "ding", {"gain": 0.22}),
            (31.0, "ambience_room", {"dur": 3.4, "gain": 0.3}), (31.2, "relays", {"dur": 2.4, "gain": 0.2}),
            (34.4, "ambience_data", {"dur": 6.0, "gain": 0.45}), (34.6, "telegraph", {"dur": 1.4, "gain": 0.15}),
            (37.6, "blip", {"gain": 0.2}), (38.2, "stream", {"dur": 2.2, "gain": 0.25}),
            (40.4, "ambience_data", {"dur": 10.4, "gain": 0.35}), (42.2, "scan", {"dur": 1.5, "gain": 0.2}),
            (43.6, "success", {"gain": 0.15})]
    for i in range(10):
        out.append((44.5 + i * 0.26, "stone_click", {"gain": 0.3, "pitch": 0.95 + 0.1 * (i % 2)}))
    out += [(45.8, "shimmer", {"dur": 1.6, "gain": 0.18}), (49.6, "riser", {"dur": 1.4, "gain": 0.25}),
            (50.8, "ambience_data", {"dur": 5.8, "gain": 0.35}), (51.0, "stream", {"dur": 2.2, "gain": 0.2}),
            (52.2, "ding", {"gain": 0.2}), (53.6, "hum", {"dur": 3.0, "gain": 0.25}),
            (56.6, "ambience_space", {"dur": 5.6, "gain": 0.45}), (56.8, "hush", {"dur": 3.0, "gain": 0.3}),
            (58.0, "heartbeat", {"n": 2, "gain": 0.3}), (60.0, "shimmer", {"dur": 2.0, "gain": 0.2})]
    return out
