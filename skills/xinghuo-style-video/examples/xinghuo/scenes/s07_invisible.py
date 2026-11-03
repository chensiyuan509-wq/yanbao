"""第七章 看不见的世界：X 射线与居里夫人（真实照片）；爱因斯坦与 1905 奇迹年；相对论的证据——
迈克耳孙–莫雷实验、μ 子、E=mc²、水星近日点、1919 年日食底片、LIGO 引力波、黑洞照片；应用——GPS、核电；
索尔维会议与量子力学的应用；哈勃深场；1945；DNA；阿波罗 11 号。关键词：协作。"""
import math

from ..core import (TAU, H, W, arrow, at, circle, clamp, dashed, ease_in, ease_io, ease_out, ellipse, glow, lerp, lin,
                    mix, poly, polyline_partial, prog, rad, rng, rrect, setc, smooth, star4, stroke_pts, text)
from .. import film
from ..archive import caption, framed, kb, show
from ..exhibit import blueprint_bg, panel
from .common import arch, claude, label, lit, role, sequence

DUR = 66.0
CHAPTER = dict(num="第 七 章", title="看不见的世界", era="1895 — 1969 年", key="协作", at=0.4, dur=4.0)
GRAIN = 0.07

VO = [
    (4.4, "伦琴的 {X 射线}照出骨骼，居里夫人发现镭、两获诺奖。"),
    (8.6, "1905 年，26 岁的爱因斯坦一年发表了 4 篇划时代的论文。"),
    (12.8, "相对论怎么被证明？1887 年的实验发现：光速在各个方向都{一样}；"),
    (17.6, "μ 子寿命只有 2.2 微秒，本该飞不到地面，"),
    (21.0, "却大量落到地面——运动让它的时间{变慢}了。"),
    (24.2, "{E=mc²}：太阳每秒约 400 万吨质量化为光热，核电也靠它。"),
    (28.6, "广义相对论算准了水星轨道每百年多转的 {43 角秒}；"),
    (31.6, "1919 年日食，人们测到星光经过太阳{拐了弯}。"),
    (35.2, "2015 年，LIGO 探测到两个黑洞合并发出的{引力波}；"),
    (38.6, "2019 年，人类拍到了{黑洞}。"),
    (41.2, "应用：GPS 卫星上的钟每天快 {38 微秒}，"),
    (43.8, "不修正，定位每天就会偏差约 10 公里。"),
    (47.2, "1927 年索尔维会议，17 位诺奖得主争论{量子力学}；"),
    (50.8, "晶体管、激光、核磁共振都由它而来；哈勃发现宇宙在{膨胀}。"),
    (55.2, "1945 年原子之力被释放，人类开始反思科学的力量；"),
    (58.4, "1953 年，DNA 双螺旋揭开了{遗传密码}。"),
    (61.0, "1969 年，约 40 万人协作，把人类送上{月球}；"),
    (64.0, "导航计算机的内存只有约 4KB。", {"spill": 0.6}),
]

SUPERS = []

# ================================================================ S1：X 射线与居里夫人（0–8.5）

VIEWER = (claude(-160, 950, 0.62, "curious", seed=71.0).walk_to(0.5, 3.9, 960, 950, stride=0.8)
          .look(4.0, -0.7, -0.6).expr(4.2, "wonder").look(5.9, 0.7, -0.6).expr(6.8, "awe"))


def _s1(ctx, t):
    ctx.set_source(lin(0, 0, 0, H, [(0, "#16120F"), (0.75, "#241C16"), (1, "#0C0907")]))
    ctx.paint()
    film.paint_texture(ctx, "stone", 0, 0, W, H, 0.12, scale=0.5)
    # 先是一片昏暗（章节标题），然后两盏顶灯"咔"地依次亮起
    for x, key, ttl, sub, t0 in ((560, "xray", "伦琴拍下的第一张 X 光片", "1895 年 12 月 · 夫人的手 · 公有领域", 4.0),
                                 (1360, "curie", "玛丽·居里", "约 1920 年 · 1903 物理 / 1911 化学诺奖 · 公有领域", 4.7)):
        k = smooth(prog(t, t0, t0 + 0.18)) * (0.82 + 0.18 * smooth(prog(t, t0 + 0.25, t0 + 0.6)))
        ctx.move_to(x - 40, 60)
        ctx.line_to(x + 40, 60)
        ctx.line_to(x + 340, 860)
        ctx.line_to(x - 340, 860)
        ctx.close_path()
        ctx.set_source(lin(0, 60, 0, 860, [(0, "#FFE2B0", 0.24 * k), (1, "#FFE2B0", 0)]))
        ctx.fill()
        glow(ctx, x, 450, 400, "#FFD9A0", 0.12 * k)
        framed(ctx, key, x, 450, 520, 0.14 + 0.86 * k)
        kt = smooth(prog(t, t0 + 0.4, t0 + 1.0))
        text(ctx, ttl, x, 770, 30, "#F2E6CE", kt, "serif_sb")
        text(ctx, sub, x, 812, 22, "#BFAE8E", kt, "serif_r")
    amb = 0.45 + 0.55 * smooth(prog(t, 4.0, 5.2))
    with lit("#FFE2B0", 0.2, amb):
        VIEWER.draw(ctx, t)
    film.vignette(ctx, 0.5)


# ================================================================ S2：爱因斯坦（8.5–13）


def _s2(ctx, t):
    kb(ctx, "einstein", t, 8.5, 13.0, (0.5, 0.4, 1.05), (0.42, 0.33, 1.3), rect=(0, 0, W * 0.58, H), grade="sepia")
    ctx.rectangle(W * 0.58, 0, W * 0.42, H)
    setc(ctx, "#0E0C0A")
    ctx.fill()
    film.vignette(ctx, 0.4)
    caption(ctx, "爱因斯坦", "施穆策尔摄 · 1921 年 · 公有领域", smooth(prog(t, 8.8, 9.3)))
    items = [("光电效应", "光是一份一份的（1921 年诺奖）"), ("布朗运动", "证明原子真实存在"), ("狭义相对论", "时间和空间是相对的"),
             ("E = mc²", "质量就是能量")]
    text(ctx, "1905 · 奇迹年", 1400, 230, 44, "#D9B26A", smooth(prog(t, 9.0, 9.5)), "serif_k")
    for i, (a_, b_) in enumerate(items):
        k = smooth(prog(t, 9.4 + i * 0.4, 9.9 + i * 0.4))
        y = 340 + i * 130
        circle(ctx, 1190, y, 8)
        setc(ctx, "#D9B26A", k)
        ctx.fill()
        text(ctx, a_, 1220, y - 6, 38, "#F6EEDF", k, "serif_k" if i < 3 else "latin_b", "l")
        text(ctx, b_, 1220, y + 42, 26, "#CFC4B0", k, "serif_r", "l")


# ================================================================ S3：迈克耳孙–莫雷（13–18）


def _s3a(ctx, t):
    arch(ctx, t, "michelson", 13.0, 15.4, (0.5, 0.5, 1.0), (0.56, 0.52, 1.14), "迈克耳孙–莫雷实验的装置",
         "1887 · 整块石板浮在水银槽上，可以缓缓转动 · 公有领域", grade="cool_mono", cap=(0.2, None))


def _s3b(ctx, t):
    u = t - 14.8
    blueprint_bg(ctx, W, H, t)
    rot = 0.9 * ease_io(prog(u, 0.8, 2.0))
    cx, cy = 720, 560
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(rot)
    L = 290
    src, bs = (-L - 40, 0), (0, 0)
    m1, m2 = (L, 0), (0, -L)
    det = (0, L * 0.8)
    rrect(ctx, -L - 90, -L - 60, 2 * L + 150, 2 * L + 120, 30)
    setc(ctx, "#7FC8FF", 0.06)
    ctx.fill()
    rrect(ctx, -L - 90, -L - 60, 2 * L + 150, 2 * L + 120, 30)
    ctx.set_line_width(2)
    setc(ctx, "#7FC8FF", 0.3)
    ctx.stroke()
    for (p, q) in ((src, bs), (bs, m1), (bs, m2), (bs, det)):
        stroke_pts(ctx, [p, q], 8, "#7FD8FF", 0.15)
    ph = (u * 1.4) % 1
    for (p, q) in ((src, bs), (bs, m1), (bs, m2), (bs, det)):
        for k in range(3):
            f = (ph + k / 3) % 1
            glow(ctx, lerp(p[0], q[0], f), lerp(p[1], q[1], f), 18, "#BFEFFF", 0.8)
    for (x, y, rw, rh) in ((L, 0, 14, 90), (0, -L, 90, 14)):
        rrect(ctx, x - rw / 2, y - rh / 2, rw, rh, 4)
        setc(ctx, "#E8F2FF")
        ctx.fill()
    ctx.save()
    ctx.rotate(math.pi / 4)
    rrect(ctx, -60, -6, 120, 12, 3)
    setc(ctx, "#BFEFFF", 0.9)
    ctx.fill()
    ctx.restore()
    circle(ctx, *src, 20)
    setc(ctx, "#FFD27A")
    ctx.fill()
    ctx.restore()
    if rot > 0.02:
        ctx.set_line_width(4)
        setc(ctx, "#FFD27A", 0.8)
        ctx.arc(cx, cy, L + 150, -math.pi / 2, -math.pi / 2 + rot)
        ctx.stroke()
    text(ctx, "两束光：一束顺着地球运动方向，一束垂直", cx, 190, 28, "#E8F2FF", smooth(prog(u, 0.1, 0.6)), "serif_sb")
    # 干涉条纹（不随转动而移动）
    fx, fy = 1500, 540
    panel(ctx, fx - 230, fy - 230, 460, 460, 1.0, "#7FC8FF")
    for i in range(9):
        x = fx - 180 + i * 45
        ctx.rectangle(x, fy - 170, 22, 340)
    setc(ctx, "#BFEFFF", 0.85)
    ctx.fill()
    text(ctx, "干涉条纹", fx, fy - 200, 28, "#E8F2FF", 1.0, "serif_sb")
    k = smooth(prog(u, 1.6, 2.2))
    text(ctx, "仪器转了方向，条纹纹丝不动", fx, fy + 270, 28, "#FFD27A", k, "serif_sb")
    text(ctx, "→ 光速不变：狭义相对论的出发点", fx, fy + 320, 28, "#FFD27A", smooth(prog(u, 2.2, 2.7)), "serif_sb")


# ================================================================ S4：μ 子（18–23.5）

OBS = (claude(1120, 950, 0.52, "curious", seed=74.0).look(18.2, -0.5, -0.9).look(21.3, -0.9, 0.3)
       .expr(21.5, "wonder"))


def _s4(ctx, t):
    u = t - 18.0
    ctx.set_source(lin(0, 0, 0, H, [(0, "#040814"), (0.75, "#16243E"), (1, "#3A3020")]))
    ctx.paint()
    film.star_field(ctx, t, 140, 7, area=(0, 90, W, 560), a=0.6)
    x0 = 300
    top, bot = 160, 880
    ctx.set_line_width(3)
    setc(ctx, "#BFD6FF", 0.6)
    ctx.move_to(x0, top)
    ctx.line_to(x0, bot)
    ctx.stroke()
    for km in (15, 10, 5, 0):
        y = lerp(bot, top, km / 15)
        ctx.move_to(x0 - 12, y)
        ctx.line_to(x0 + 12, y)
        ctx.stroke()
        text(ctx, f"{km} 公里", x0 - 30, y, 24, "#BFD6FF", 0.9, "serif_r", "r")
    ctx.set_source(lin(0, bot, 0, H, [(0, "#3A3020"), (1, "#1A140C")]))
    ctx.rectangle(-50, bot, W + 100, 300)
    ctx.fill()
    # 宇宙线在高空撞上大气，产生 μ 子
    mx = 860
    hit = smooth(prog(u, 0.2, 0.5)) * (1 - smooth(prog(u, 0.6, 1.6)))
    glow(ctx, mx, top + 10, 160, "#FFFFFF", 0.6 * hit)
    text(ctx, "宇宙线撞上高层大气", mx + 40, top - 20, 24, "#E8F2FF", smooth(prog(u, 0.3, 0.8)), "serif_r", "l")
    # 按经典计算：飞约 0.66 公里就衰变
    yc = top + (bot - top) * 0.66 / 15
    kc = smooth(prog(u, 0.9, 1.4))
    dashed(ctx, 620, top + 10, 620, yc, 5, "#FF8A6A", kc, (10, 8))
    for sgn in (-1, 1):
        ctx.move_to(620 - 16, yc - 16 * sgn)
        ctx.line_to(620 + 16, yc + 16 * sgn)
    ctx.set_line_width(5)
    setc(ctx, "#FF8A6A", kc)
    ctx.stroke()
    text(ctx, "按经典计算：飞约 0.66 公里就衰变", 600, yc + 50, 26, "#FF8A6A", kc, "serif_sb", "r")
    # 实际：一路落到地面，被探测器记录
    f = ease_in(prog(u, 0.6, 3.4))
    my = lerp(top + 20, bot - 30, f)
    if u < 3.6:
        for i in range(10):
            glow(ctx, mx, my - i * 26, 22 - i * 2, "#FF9AD2", 0.5 * (1 - i / 10))
        circle(ctx, mx, my, 10)
        setc(ctx, "#FFD2EE")
        ctx.fill()
    ping = smooth(prog(u, 3.4, 3.6)) * (1 - smooth(prog(u, 3.8, 5.0)))
    glow(ctx, mx, bot - 10, 140, "#FF9AD2", 0.7 * ping)
    rrect(ctx, mx - 70, bot - 34, 140, 44, 8)
    setc(ctx, mix("#4A5A7A", "#FFD2EE", ping))
    ctx.fill()
    text(ctx, "探测器", mx, bot + 40, 24, "#E8DCC8", 0.9, "serif_r")
    with lit("#9AB6FF", 0.25, 0.85):
        OBS.draw(ctx, t)
    # 数据
    k = smooth(prog(u, 1.4, 1.9))
    panel(ctx, 1220, 190, 600, 470, k)
    text(ctx, "μ 子自己的钟：2.2 微秒", 1520, 245, 30, "#FFD2EE", k, "serif_sb")
    k2 = smooth(prog(u, 2.0, 2.5))
    text(ctx, "1963 年 · 华盛顿山顶 vs 海平面", 1520, 320, 26, "#D9B26A", k2, "serif_sb")
    text(ctx, "山顶：每小时约 563 个", 1260, 385, 28, "#F6EEDF", k2, "serif_sb", "l")
    text(ctx, "海平面：约 408 个", 1260, 440, 28, "#F6EEDF", k2, "serif_sb", "l")
    k3 = smooth(prog(u, 2.8, 3.3))
    text(ctx, "如果时间不变慢：只剩约 27 个", 1260, 500, 28, "#FF8A6A", k3, "serif_sb", "l")
    k4 = smooth(prog(u, 3.5, 4.0))
    text(ctx, "→ 运动的钟真的走得慢", 1520, 590, 30, "#FFD27A", k4, "serif_sb")
    text(ctx, "罗西–霍尔（1941）· 弗里施–史密斯（1963）", 960, 930, 22, "#BFD6FF", 0.8, "serif_r")


# ================================================================ S5：E=mc²（23.5–28.5）


def _s5(ctx, t):
    u = t - 23.5
    ctx.set_source(rad(700, 540, 0, 1000, [(0, "#3A1A08"), (0.6, "#120804"), (1, "#050302")]))
    ctx.paint()
    film.sun(ctx, 520, 540, 150, 1.0, "#FFF2C8", "#FF8A2A", 800)
    for i in range(16):
        ang = i / 16 * TAU + t * 0.1
        film.beams(ctx, 520, 540, ang, 0.05, 900, 1, "#FFD27A", 0.06, t, i)
    x0 = 1060
    text(ctx, "E = mc²", 1440, 220, 70, "#FFE8C0", smooth(prog(u, 0.1, 0.6)), "eq")
    rows = [("4 个氢核", "4 × 1.0078 = 4.031", 0.6), ("1 个氦核", "4.0026", 1.2), ("少了 0.7% 的质量", "→ 变成光和热", 1.8)]
    for i, (a_, b_, t0) in enumerate(rows):
        k = smooth(prog(u, t0, t0 + 0.5))
        text(ctx, a_, x0, 380 + i * 110, 34, "#F6EEDF", k, "serif_sb", "l")
        text(ctx, b_, x0 + 360, 380 + i * 110, 34, "#FFD27A", k, "eq" if i < 2 else "serif_sb", "l")
    k = smooth(prog(u, 2.6, 3.2))
    panel(ctx, x0 - 20, 720, 760, 150, k)
    text(ctx, "太阳：每秒约 400 万吨质量化为光热", x0 + 360, 770, 30, "#F6EEDF", k, "serif_sb")
    text(ctx, "应用：核电站、PET 医学影像", x0 + 360, 830, 30, "#FFD27A", k, "serif_sb")


# ================================================================ S6：水星近日点（28.5–31.4）


def _tick(ctx, x, y, s, color, a):
    ctx.move_to(x - s * 0.5, y)
    ctx.line_to(x - s * 0.1, y + s * 0.4)
    ctx.line_to(x + s * 0.6, y - s * 0.5)
    ctx.set_line_width(s * 0.18)
    ctx.set_line_cap(1)
    setc(ctx, color, a)
    ctx.stroke()


def _s6a(ctx, t):
    u = t - 28.5
    blueprint_bg(ctx, W, H, t)
    cx, cy = 720, 540
    glow(ctx, cx, cy, 110, "#FFC46B", 0.8)
    circle(ctx, cx, cy, 30)
    setc(ctx, "#FFE8A8")
    ctx.fill()
    for k in range(7):
        ang = k * 0.22 + u * 0.12
        ctx.save()
        ctx.translate(cx, cy)
        ctx.rotate(ang)
        ctx.translate(70, 0)
        ctx.set_line_width(2.5)
        setc(ctx, "#7FD8FF", 0.2 + 0.11 * k)
        ellipse(ctx, 0, 0, 330, 250)
        ctx.stroke()
        ctx.restore()
    # 水星沿最外一圈轨道走
    ang = 0.66 + u * 0.12
    ph = u * 1.6
    px, py = 70 + 330 * math.cos(ph), 250 * math.sin(ph)
    gx = cx + px * math.cos(ang) - py * math.sin(ang)
    gy = cy + px * math.sin(ang) + py * math.cos(ang)
    glow(ctx, gx, gy, 30, "#BFEFFF", 0.8)
    circle(ctx, gx, gy, 9)
    setc(ctx, "#E8F2FF")
    ctx.fill()
    text(ctx, "近日点每绕一圈都往前挪一点（图中夸大）", cx, 900, 26, "#BFE0FF", 0.9, "serif_r")
    panel(ctx, 1240, 280, 580, 440, 1.0, "#7FC8FF")
    rows = [("观测：每百年进动", "574″"), ("牛顿理论能解释", "531″"), ("还差", "43″"), ("广义相对论算出", "43″")]
    for i, (a_, b_) in enumerate(rows):
        k = smooth(prog(u, 0.3 + i * 0.5, 0.8 + i * 0.5))
        y = 350 + i * 92
        text(ctx, a_, 1280, y, 30, "#E8F2FF", k, "serif_sb", "l")
        text(ctx, b_, 1730, y, 36, "#FFD27A" if i >= 2 else "#E8F2FF", k, "eq", "r")
        if i == 3:
            _tick(ctx, 1772, y, 34, "#7FE0A0", k)
    text(ctx, "水星近日点进动 · 1915", 960, 160, 34, "#E8F2FF", 1.0, "serif_k")


# ================================================================ S7：1919 年日食（31.4–35）


def _s6b(ctx, t):
    u = t - 31.4
    ctx.set_source(rad(520, 500, 0, 1300, [(0, "#1E1A16"), (1, "#060504")]))
    ctx.paint()
    # 灯箱上的玻璃底片
    w, h = 470, 604
    X, Y = 520 - w / 2, 500 - h / 2
    glow(ctx, 520, 500, 560, "#FFF6E0", 0.18)
    rrect(ctx, X - 40, Y - 40, w + 80, h + 80, 14)
    setc(ctx, "#F6F1E6", 0.95)
    ctx.fill()
    show(ctx, "eclipse1919", (0.5, 0.5, 1.0 + 0.05 * u), (X, Y, w, h), 0.92, grade="mono")
    rrect(ctx, X, Y, w, h, 4)
    ctx.set_line_width(3)
    setc(ctx, "#2A2620", 0.8)
    ctx.stroke()
    text(ctx, "1919 年 5 月 29 日日全食 · 玻璃底片", 520, Y + h + 80, 26, "#F2E6CE", 1.0, "serif_sb")
    text(ctx, "戴森、爱丁顿、戴维森 · 公有领域", 520, Y + h + 118, 20, "#BFAE8E", 1.0, "serif_r")
    # 右：星光偏折示意
    sx, sy, r = 1380, 690, 50
    E = (1800, 690)
    P = (sx, sy - 78)
    s2 = (E[1] - P[1]) / (E[0] - P[0])
    T = (1020, P[1] - 0.03 * (P[0] - 1020))
    A = (1020, P[1] - s2 * (P[0] - 1020))
    glow(ctx, sx, sy, 140, "#FFC46B", 0.5)
    circle(ctx, sx, sy, r)
    setc(ctx, "#111111")
    ctx.fill()
    circle(ctx, sx, sy, r)
    ctx.set_line_width(3)
    setc(ctx, "#FFE8B0", 0.9)
    ctx.stroke()
    text(ctx, "太阳（被月亮挡住）", sx, sy + r + 34, 22, "#E8DCC8", 0.9, "serif_r")
    circle(ctx, *E, 16)
    setc(ctx, "#6FA8FF")
    ctx.fill()
    text(ctx, "地球", E[0], E[1] + 44, 22, "#E8DCC8", 0.9, "serif_r")
    kp = ease_io(prog(u, 0.4, 1.8))
    path = [T]
    for i in range(1, 41):
        f = i / 40
        x = lerp(T[0], E[0], f)
        if x <= P[0]:
            y = T[1] + (x - T[0]) * 0.03
        else:
            y = P[1] + (x - P[0]) * s2
        # 在太阳附近圆滑过渡
        d = (x - P[0]) / 60
        if abs(d) < 1:
            y0 = T[1] + (x - T[0]) * 0.03
            y1 = P[1] + (x - P[0]) * s2
            m = smooth((d + 1) / 2)
            y = lerp(y0, y1, m)
        path.append((x, y))
    stroke_pts(ctx, polyline_partial(path, kp), 4, "#FFD27A", 0.95)
    ka = smooth(prog(u, 1.9, 2.4))
    dashed(ctx, E[0], E[1], A[0], A[1], 3, "#7FD8FF", ka, (12, 10))
    star4(ctx, *T, 16, "#FFD27A", 0.5 + 0.5 * smooth(prog(u, 0.2, 0.5)))
    text(ctx, "星的真实位置", T[0], T[1] + 40, 22, "#FFD27A", smooth(prog(u, 0.2, 0.7)), "serif_r")
    star4(ctx, *A, 20, "#BFEFFF", ka)
    text(ctx, "底片上看到的位置", A[0], A[1] - 36, 22, "#BFEFFF", ka, "serif_r")
    k = smooth(prog(u, 0.6, 1.2))
    panel(ctx, 1020, 180, 800, 250, k)
    text(ctx, "日全食时太阳被遮住，才拍得到它身边的星", 1420, 235, 28, "#F6EEDF", k, "serif_sb")
    text(ctx, "和半年前夜里同一片星空对比：星被\"推\"开了", 1420, 290, 26, "#CFC4B0", k, "serif_r")
    k2 = smooth(prog(u, 2.2, 2.7))
    text(ctx, "实测约 1.75 角秒 = 广义相对论的预言（牛顿理论只有一半）", 1420, 360, 28, "#FFD27A", k2, "serif_sb")
    text(ctx, "偏折角度在图中被夸大", 1420, 900, 20, "#8C8478", 0.8, "serif_r")


# ================================================================ S8：LIGO 与黑洞（35–41）


def _s7a(ctx, t):
    u = t - 35.0
    kb(ctx, "ligo", t, 35.0, 38.8, (0.45, 0.6, 1.1), (0.42, 0.68, 1.4))
    film.vignette(ctx, 0.5)
    caption(ctx, "LIGO 汉福德天文台：4 公里长的激光臂", "照片：公有领域", smooth(prog(u, 0.2, 0.7)))
    k = smooth(prog(u, 0.6, 1.2))
    panel(ctx, 1160, 180, 640, 270, k, "#7FC8FF")
    text(ctx, "2015.9.14 · GW150914", 1480, 230, 30, "#E8F2FF", k, "latin")
    pts = []
    for i in range(260):
        x = i / 259
        f = 4 + 60 * x ** 6
        amp = 0.2 + 0.8 * x ** 3
        if x > 0.93:
            amp *= max(0.0, 1 - (x - 0.93) / 0.07)
        pts.append((1190 + x * 580, 320 + math.sin(x * f * 6) * 55 * amp))
    stroke_pts(ctx, polyline_partial(pts, ease_io(prog(u, 0.8, 2.6))), 3, "#7FD8FF", k)
    text(ctx, "13 亿光年外两个黑洞合并", 1480, 400, 24, "#BFE0FF", k, "serif_r")
    text(ctx, "能测出质子直径万分之一的长度变化", 1480, 432, 22, "#BFE0FF", k, "serif_r")


def _s7b(ctx, t):
    u = t - 38.4
    kb(ctx, "m87", t, 38.0, 41.4, (0.5, 0.5, 1.0), (0.5, 0.5, 1.25))
    film.vignette(ctx, 0.4)
    caption(ctx, "M87 星系中心的黑洞", "事件视界望远镜合作组织 · 2019 · CC BY 4.0", smooth(prog(u, 0.4, 0.9)))
    k = smooth(prog(u, 0.6, 1.1))
    text(ctx, "8 台射电望远镜联成\"地球那么大\"的一台", 1580, 230, 26, "#F6EEDF", k, "serif_sb")
    text(ctx, "距离 5500 万光年 · 质量约 65 亿个太阳", 1580, 276, 22, "#CFC4B0", k, "serif_r")


# ================================================================ S9：GPS（41–47）


def _s8(ctx, t):
    u = t - 41.0
    kb(ctx, "gps", t, 40.6, 47.4, (0.56, 0.6, 1.0), (0.52, 0.56, 1.15))
    film.vignette(ctx, 0.45)
    caption(ctx, "GPS III 卫星（示意图）", "美国空军 · 公有领域", smooth(prog(u, 0.2, 0.7)))
    k = smooth(prog(u, 0.4, 1.0))
    panel(ctx, 1240, 180, 580, 450, k, "#7FC8FF")
    text(ctx, "卫星上的原子钟", 1530, 230, 30, "#D9B26A", k, "serif_sb")
    rows = [("轨道高处引力弱：钟变快", "+45 微秒/天", "#FFD27A"), ("高速运动：钟变慢", "−7 微秒/天", "#7FD8FF"),
            ("合计", "+38 微秒/天", "#FFFFFF")]
    for i, (a_, b_, c) in enumerate(rows):
        kk = smooth(prog(u, 0.6 + i * 0.5, 1.1 + i * 0.5))
        text(ctx, a_, 1270, 290 + i * 96, 28, "#E8F2FF", kk, "serif_sb", "l")
        text(ctx, b_, 1790, 332 + i * 96, 32, c, kk, "serif_k", "r")
    k2 = smooth(prog(u, 2.8, 3.4))
    text(ctx, "不修正：定位每天偏差约 10 公里", 1530, 590, 28, "#FF9A7A", k2, "serif_sb")


# ================================================================ S10：量子力学与宇宙（47–55）


def _s9a(ctx, t):
    arch(ctx, t, "solvay", 47.0, 51.4, (0.5, 0.55, 1.05), (0.52, 0.6, 1.4), "第五届索尔维会议",
         "布鲁塞尔 · 1927 年 · 本杰明·库普里摄 · 公有领域", grade="mono", cap=(0.2, 3.6))


def _s9b(ctx, t):
    u = t - 51.0
    kb(ctx, "hudf", t, 50.6, 55.4, (0.5, 0.5, 1.0), (0.48, 0.52, 1.6))
    film.vignette(ctx, 0.45)
    caption(ctx, "哈勃极深场：约一万个星系", "NASA/ESA · 公有领域", smooth(prog(u, 0.2, 0.7)))
    k = smooth(prog(u, 0.0, 0.5))
    panel(ctx, 1220, 190, 600, 330, k)
    text(ctx, "量子力学的应用", 1520, 240, 30, "#D9B26A", k, "serif_sb")
    for i, s in enumerate(("晶体管 → 一切芯片", "激光 → 光纤通信", "核磁共振 → 医学成像")):
        text(ctx, s, 1260, 310 + i * 56, 30, "#F6EEDF", smooth(prog(u, 0.3 + i * 0.3, 0.8 + i * 0.3)), "serif_sb", "l")
    text(ctx, "1929 · 哈勃：星系都在远离我们", 1520, 482, 24, "#CFC4B0", smooth(prog(u, 1.4, 1.9)), "serif_r")


# ================================================================ S11：1945 与 DNA（55–61）

BASES = [("A", "T"), ("C", "G"), ("G", "C"), ("T", "A"), ("A", "T"), ("G", "C"), ("C", "G"), ("T", "A"),
         ("G", "C"), ("A", "T"), ("C", "G"), ("T", "A")]
BCOL = {"A": "#FF7A6A", "T": "#FFD27A", "C": "#7FD8A8", "G": "#7FB6FF"}


def _s10a(ctx, t):
    arch(ctx, t, "trinity", 55.0, 58.6, (0.5, 0.5, 1.05), (0.5, 0.48, 1.2), "\"三位一体\"核试验",
         "新墨西哥 · 1945 年 7 月 16 日 · 公有领域", grade="mono", cap=(0.2, 3.0))
    film.fade_black(ctx, 0.2)


def _s10b(ctx, t):
    u = t - 58.2
    ctx.set_source(rad(960, 540, 0, 1300, [(0, "#121A2A"), (1, "#03050A")]))
    ctx.paint()
    x0, x1, cy, amp = 160, 1180, 540, 170
    ph = t * 1.4
    n = len(BASES)
    for i in range(n):
        f = (i + 0.5) / n
        x = lerp(x0, x1, f)
        a = f * TAU * 2.2 + ph
        y1, y2 = cy + math.sin(a) * amp, cy + math.sin(a + math.pi) * amp
        b1, b2 = BASES[i]
        ctx.set_line_width(12)
        setc(ctx, BCOL[b1], 0.85)
        ctx.move_to(x, y1)
        ctx.line_to(x, (y1 + y2) / 2)
        ctx.stroke()
        setc(ctx, BCOL[b2], 0.85)
        ctx.move_to(x, (y1 + y2) / 2)
        ctx.line_to(x, y2)
        ctx.stroke()
    for off in (0, math.pi):
        pts = []
        for i in range(121):
            f = i / 120
            a = f * TAU * 2.2 + ph + off
            pts.append((lerp(x0, x1, f), cy + math.sin(a) * amp, math.cos(a)))
        for p, q in zip(pts, pts[1:]):
            front = (p[2] + 1) / 2
            ctx.set_line_width(10 + 6 * front)
            setc(ctx, mix("#4A5A8A", "#DCE6FF", front), 0.95)
            ctx.move_to(p[0], p[1])
            ctx.line_to(q[0], q[1])
            ctx.stroke()
    k = smooth(prog(u, 0.2, 0.7))
    panel(ctx, 1280, 260, 540, 380, k)
    text(ctx, "DNA 双螺旋 · 1953", 1550, 310, 32, "#D9B26A", k, "serif_sb")
    text(ctx, "A–T、C–G 两两配对", 1550, 380, 30, "#F6EEDF", k, "serif_sb")
    for i, s in enumerate(("基因测序", "人类基因组计划（2003）", "基因疗法、mRNA 疫苗")):
        text(ctx, "· " + s, 1320, 450 + i * 52, 28, "#CFC4B0", smooth(prog(u, 0.6 + i * 0.3, 1.0 + i * 0.3)), "serif_r", "l")


# ================================================================ S12：阿波罗（61–66）


def _s11a(ctx, t):
    kb(ctx, "apollo_launch", t, 60.6, 63.2, (0.5, 0.4, 1.1), (0.5, 0.33, 1.25))
    film.vignette(ctx, 0.4)
    caption(ctx, "阿波罗 11 号发射", "1969 年 7 月 16 日 · NASA · 公有领域", smooth(prog(t, 61.1, 61.5)))


def _s11b(ctx, t):
    kb(ctx, "aldrin", t, 62.4, 64.8, (0.5, 0.35, 1.05), (0.5, 0.3, 1.3))
    film.vignette(ctx, 0.4)
    caption(ctx, "奥尔德林在月面", "1969 年 7 月 20 日 · NASA · 公有领域", smooth(prog(t, 62.9, 63.3)))


def _s11c(ctx, t):
    u = t - 64.4
    kb(ctx, "earthrise", t, 64.0, 66.8, (0.5, 0.6, 1.0), (0.52, 0.58, 1.12))
    film.vignette(ctx, 0.35)
    k = smooth(prog(u, 0.0, 0.4))
    framed(ctx, "dsky", 400, 380, 240, k)
    text(ctx, "阿波罗导航计算机 · 内存约 4KB", 400, 560, 24, "#F2E6CE", k, "serif_sb")
    caption(ctx, "\"地出\"", "阿波罗 8 号 · 1968 · NASA · 公有领域", smooth(prog(u, 0.2, 0.6)))


SHOTS = [(0.0, _s1), (8.5, _s2), (13.0, _s3a), (14.8, _s3b), (18.0, _s4), (23.5, _s5), (28.5, _s6a), (31.4, _s6b),
         (35.0, _s7a), (38.4, _s7b), (41.0, _s8), (47.0, _s9a), (51.0, _s9b), (55.0, _s10a), (58.2, _s10b),
         (61.0, _s11a), (62.8, _s11b), (64.4, _s11c)]
TRANS = {1: ("dissolve", 0.9), 2: ("lightsweep", 0.9, {"color": "#BFE0FF"}), 3: ("luma", 0.8),
         4: ("zoomblur", 0.7, {"y": 300}), 5: ("flare", 0.9, {"x": 520, "y": 540}), 6: ("defocus", 1.0, {"max": 10}),
         7: ("dissolve", 0.8), 8: ("lightsweep", 0.9, {"angle": 0.4, "color": "#BFE0FF"}),
         9: ("dissolve", 0.8, {"zoom": 0.08}), 10: ("luma", 0.9), 11: ("dissolve", 1.0), 12: ("defocus", 1.0, {"max": 10}),
         13: ("flash", 0.6), 14: ("dip", 0.8), 15: ("zoomblur", 0.6, {"y": 700}), 16: ("dissolve", 0.6),
         17: ("dissolve", 0.8)}


def draw(ctx, t):
    sequence(ctx, t, SHOTS, TRANS)


def sfx():
    return [
        (0.0, "ambience_room", {"dur": 8.5, "gain": 0.35}), (0.4, "shutter", {"gain": 0.3}), (1.4, "shutter", {"gain": 0.3}),
        (2.4, "geiger", {"dur": 3.0, "rate": 6, "gain": 0.18}),
        (8.5, "ambience_room", {"dur": 4.5, "gain": 0.3}), (9.0, "chalk", {"dur": 1.6, "gain": 0.25}),
        (13.0, "hum", {"dur": 5.0, "gain": 0.15}), (13.2, "zap", {"dur": 0.6, "gain": 0.1}), (15.6, "whoosh_short", {"gain": 0.18}),
        (18.0, "ambience_space", {"dur": 5.5, "gain": 0.4}), (18.3, "impact_soft", {"gain": 0.3}), (18.6, "fall", {"dur": 3.0, "gain": 0.25}),
        (23.5, "ambience_fire", {"dur": 5.0, "gain": 0.35}), (23.6, "rumble", {"dur": 3.0, "gain": 0.3}),
        (28.5, "ambience_space", {"dur": 6.5, "gain": 0.35}), (31.4, "shutter", {"gain": 0.3}), (32.2, "shimmer", {"dur": 1.6, "gain": 0.18}),
        (35.0, "ambience_wind", {"dur": 3.4, "gain": 0.3}), (36.0, "rise", {"dur": 2.4, "gain": 0.25}),
        (38.4, "boom", {"gain": 0.45}), (38.5, "ambience_space", {"dur": 2.6, "gain": 0.45}),
        (41.0, "ambience_space", {"dur": 6.0, "gain": 0.4}), (41.6, "blip", {"gain": 0.15}), (42.1, "blip", {"gain": 0.15, "pitch": 1.2}),
        (42.6, "blip", {"gain": 0.15, "pitch": 1.4}), (43.8, "alert", {"gain": 0.12}),
        (47.0, "ambience_room", {"dur": 4.0, "gain": 0.3}), (47.2, "shutter", {"gain": 0.3}),
        (51.0, "ambience_space", {"dur": 4.0, "gain": 0.45}), (51.2, "shimmer", {"dur": 2.0, "gain": 0.2}),
        (55.0, "boom", {"gain": 0.7}), (55.2, "rumble", {"dur": 2.8, "gain": 0.4}), (58.2, "ambience_room", {"dur": 2.8, "gain": 0.3}),
        (58.4, "shimmer", {"dur": 1.6, "gain": 0.15}),
        (61.0, "rocket", {"dur": 2.0, "gain": 0.7}), (62.8, "ambience_space", {"dur": 3.2, "gain": 0.5}), (63.0, "hush", {"dur": 2.0, "gain": 0.25}),
        (64.6, "relays", {"dur": 1.4, "gain": 0.15}),
    ]
