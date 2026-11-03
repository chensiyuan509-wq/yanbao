"""第三章 追问为什么：拉斐尔《雅典学院》；扮成欧几里得的 Claude 讲四个经典证明（内角和、勾股定理、
质数无穷、辗转相除）；斯特罗齐画的埃拉托色尼 + 第一视角看井 + 测地示意图；费蒂画的阿基米德与圆周率；
亚历山大图书馆（19 世纪想象图）。关键词：证明。"""
import math

from ..core import (TAU, H, W, circle, clamp, dashed, ease_io, ease_out, glow, lerp, lin, mix, prog, rad, rng,
                    rrect, setc, smooth, stroke_pts, text)
from ..gallery import Gallery
from .. import film, proofs
from ..archive import caption, framed, kb, show
from .common import arch, claude, label, lit, role, sequence

DUR = 70.0
CHAPTER = dict(num="第 三 章", title="追问为什么", era="约公元前 600 年 — 公元 500 年", key="证明", at=0.4, dur=4.0, x=620)
GRAIN = 0.08

VO = [
    (4.6, "古希腊人开始追问'为什么'，并且要求{证明}。"),
    (7.4, "《雅典学院》右下角弯腰拿圆规的，常被认为是{欧几里得}。"),
    (10.4, "《几何原本》从 5 条公设出发，推出 {465 个命题}。"),
    (13.3, "例一：三角形内角和，为什么是 180°？"),
    (16.2, "过顶点作平行线，内错角相等，三个角拼成一条{直线}。"),
    (20.3, "例二：勾股定理——同一个正方形里，移动 4 个三角形，"),
    (24.4, "空白处先是 c²，后是 a² + b²，所以 {a² + b² = c²}。"),
    (28.3, "例三：质数有无穷多个——把已知质数全乘起来再加 1，"),
    (31.9, "它除以名单里任何一个都余 1，必有{新质数}。"),
    (35.3, "例四：辗转相除求最大公约数，人类最早的{算法}之一，"),
    (38.8, "两千多年后，计算机还在用它。"),
    (42.3, "约公元前 240 年，埃拉托色尼注意到：夏至正午，赛伊尼的井底映出太阳；"),
    (46.6, "亚历山大港的立柱，影子却偏了 {7.2°}——圆周的 1/50；"),
    (50.3, "两城相距 5000 斯塔德，地球周长约 25 万斯塔德，约 {4 万公里}。"),
    (56.3, "阿基米德用 96 边形，把 π 夹在 3.1408 与 3.1429 之间；"),
    (60.4, "祖冲之算到 {3.1415926}，领先世界九百多年。"),
    (64.3, "亚历山大图书馆汇集了古代书卷，可许多典籍后来都{散失}了……", {"spill": 0.6}),
]

SUPERS = []

# ================================================================ A：雅典学院（0–10）


VIS3 = (claude(300, 905, 0.55, "curious", seed=31.0).walk_to(1.0, 3.4, 860, 905, stride=0.8).look(3.5, 0.3, -0.9)
        .expr(3.7, "awe"))
HALL3 = Gallery([("athens", "拉斐尔《雅典学院》", "1509—1511 年 · 湿壁画 · 梵蒂冈宫 · 公有领域")], VIS3, 3.6, 6.2,
                push=0, push_dur=1.4, lead=420)


def _shot_a0(ctx, t):
    """Claude 走进展厅，镜头推进《雅典学院》的画框里。"""
    with lit("#FFE2B0", 0.15, 0.95):
        HALL3.draw(ctx, t)


def _shot_a(ctx, t):
    to = kb(ctx, "athens", t, 6.2, 10.0, (0.5, 0.5, 1.02), (0.76, 0.76, 2.4))
    film.vignette(ctx, 0.5)
    caption(ctx, "拉斐尔《雅典学院》", "1509—1511 年 · 湿壁画 · 梵蒂冈宫 · 公有领域",
            smooth(prog(t, 6.6, 7.2)) * (1 - smooth(prog(t, 9.4, 9.9))))
    k = smooth(prog(t, 7.6, 8.4))
    if k > 0:
        label(ctx, "欧几里得（一说阿基米德）", 960, 220, 38, "#FFE8C0", k, "serif_sb")


# ================================================================ B：四个证明（10–42）

EUCLID = (role(1760, 960, 0.4, "euclid", "smile", seed=41.0, palette="ochre", flip=True)
          .point(10.4, "r", 0.6, 60).arms_down(12.0)
          .expr(13.3, "think").expr(16.2, "proud").nod(17.0)
          .expr(20.3, "focused").point(24.4, "r", 0.5, 60).arms_down(26.0).expr(26.4, "happy")
          .expr(28.3, "hmm").expr(32.6, "starry").fx(32.6, ("sparkle",)).fx(33.6, ())
          .expr(35.3, "focused").expr(39.0, "smile"))


def _shot_b0(ctx, t):
    u = t - 10.0
    proofs.paper(ctx)
    framed(ctx, "byrne_title", 640, 520, 300, smooth(prog(u, 0.1, 0.6)))
    caption(ctx, "拜恩版《几何原本》（彩色图解）", "伦敦 · 1847 年 · 公有领域", smooth(prog(u, 0.3, 0.8)), x=360, y=820, size=30)
    rows = [("13 卷", 0.4), ("23 个定义", 0.8), ("5 条公设 · 5 条公理", 1.2), ("→ 465 个命题", 1.8)]
    for i, (s, t0) in enumerate(rows):
        k = smooth(prog(u, t0, t0 + 0.5))
        proofs.eq(ctx, s, 1200, 360 + i * 90, 52 if i == 3 else 44, proofs.RED if i == 3 else proofs.INK, k, "l",
                  "serif_k" if i == 3 else "serif_sb")


def _shot_proof(ctx, t, fn, t0, title):
    proofs.paper(ctx)
    fn(ctx, t - t0)
    proofs.eq(ctx, title, 110, 175, 34, proofs.INK, smooth(prog(t - t0, 0.0, 0.5)), "l", "serif_k")
    with lit("#FFE0B0", 0.15, 1.0):
        EUCLID.draw(ctx, t)


def _shot_b(ctx, t):
    if t < 13.0:
        _shot_b0(ctx, t)
        with lit("#FFE0B0", 0.15, 1.0):
            EUCLID.draw(ctx, t)
    elif t < 20.0:
        _shot_proof(ctx, t, proofs.angle_sum, 13.0, "例一 · 卷一命题 32")
    elif t < 28.0:
        _shot_proof(ctx, t, proofs.pythagoras, 20.0, "例二 · 卷一命题 47（拼图证法）")
    elif t < 35.0:
        _shot_proof(ctx, t, proofs.primes, 28.0, "例三 · 卷九命题 20")
    else:
        _shot_proof(ctx, t, proofs.gcd, 35.0, "例四 · 卷七命题 2")
    film.vignette(ctx, 0.35, color="#2A1A0A")


# ================================================================ C：埃拉托色尼（42–56）


def _shot_c0(ctx, t):
    arch(ctx, t, "eratosthenes", 42.0, 45.0, (0.5, 0.45, 1.05), (0.42, 0.4, 1.3), "伯纳多·斯特罗齐《埃拉托色尼在亚历山大授课》",
         "1635 年 · 蒙特利尔美术馆 · 公有领域", cap=(0.2, 2.8))


def _shot_well(ctx, t, u):
    ctx.set_source_rgb(0.05, 0.035, 0.02)
    ctx.paint()
    cx, cy = 960, 540
    zoom = 1 + 0.12 * ease_io(prog(u, 0, 3.4))
    for i in range(18, -1, -1):
        f = i / 18
        r = lerp(90, 980, f ** 1.6) * zoom
        shade = 0.12 + 0.75 * f ** 1.3
        ox, oy = cx + (1 - f) * 20, cy + (1 - f) * 10
        circle(ctx, ox, oy, r)
        setc(ctx, mix("#2A1A0E", "#C9A170", shade))
        ctx.fill()
        ctx.set_line_width(3)
        setc(ctx, "#1A0E06", 0.5)
        circle(ctx, ox, oy, r)
        ctx.stroke()
        R = rng(i)
        for k in range(int(10 + 20 * f)):
            ang = R.uniform(0, TAU)
            ctx.move_to(ox + math.cos(ang) * r, oy + math.sin(ang) * r)
            ctx.line_to(ox + math.cos(ang) * r * 0.93, oy + math.sin(ang) * r * 0.93)
        setc(ctx, "#1A0E06", 0.35)
        ctx.stroke()
    wx, wy, wr = cx + 20, cy + 10, 88 * zoom
    circle(ctx, wx, wy, wr)
    setc(ctx, "#1C3040")
    ctx.fill()
    sk = smooth(prog(u, 0.3, 1.0))
    glow(ctx, wx + 6, wy - 4, 220, "#FFF2C8", 0.8 * sk)
    circle(ctx, wx + 6 + math.sin(t * 3) * 2, wy - 4, 26 * zoom)
    setc(ctx, "#FFFBEA", sk)
    ctx.fill()
    from mascot import draw_mascot
    ctx.save()
    circle(ctx, wx, wy, wr)
    ctx.clip()
    draw_mascot(ctx, wx - 40, wy + 70, 0.2 * zoom, expr="wonder", t=t, alpha=0.55 * smooth(prog(u, 0.8, 1.5)))
    ctx.restore()
    label(ctx, "夏至正午 · 太阳正好在头顶", 960, 900, 32, "#FFE8C0", smooth(prog(u, 1.0, 1.6)), "serif_sb")
    with lit("#FFD49A", 0.3, 1.0):
        film.pov_arm(ctx, (220, 1350), (560, 960), 150)
        film.pov_arm(ctx, (1700, 1350), (1360, 960), 150)
    film.vignette(ctx, 0.5)


def _shot_diagram(ctx, t, u):
    ctx.set_source(lin(0, 0, 0, H, [(0, "#E6D2A6"), (1, "#C9AE7E")]))
    ctx.paint()
    film.paint_texture(ctx, "parchment", 0, 0, W, H, 0.7)
    ink = "#3A2414"
    ox, oy, R0 = 760, 1500, 1050
    ctx.set_line_width(5)
    setc(ctx, ink, 0.9)
    ctx.new_path()
    ctx.arc(ox, oy, R0, math.radians(-150), math.radians(-30))
    ctx.stroke()
    a_sy, a_al = math.radians(-90), math.radians(-90 - 7.2 * 3)
    sy = (ox + math.cos(a_sy) * R0, oy + math.sin(a_sy) * R0)
    al = (ox + math.cos(a_al) * R0, oy + math.sin(a_al) * R0)
    k1 = smooth(prog(u, 0.1, 0.7))
    for i in range(7):
        x = 300 + i * 150
        dashed(ctx, x, 120, x, 360 if i != 3 else 0, 3, "#C9781E", k1 * 0.8, (16, 10), -t * 30)
    film.sun(ctx, 1640, 200, 44, k1, "#FFE8B0", "#FFB766", 260)
    label(ctx, "阳光几乎平行", 1640, 300, 28, ink, k1, "serif_sb", shadow=False)
    k2 = smooth(prog(u, 0.4, 0.9))
    dashed(ctx, sy[0], 150, sy[0], sy[1], 4, "#C9781E", k2, (16, 10), -t * 30)
    rrect(ctx, sy[0] - 20, sy[1] - 10, 40, 60, 4)
    setc(ctx, ink, k2)
    ctx.fill()
    label(ctx, "赛伊尼：井底有阳光", sy[0] + 190, sy[1] - 40, 30, ink, k2, "serif_sb", shadow=False)
    k3 = smooth(prog(u, 1.0, 1.6))
    nx, ny = math.cos(a_al), math.sin(a_al)
    top = (al[0] + nx * 200, al[1] + ny * 200)
    ctx.set_line_width(9)
    setc(ctx, ink, k3)
    ctx.move_to(*al)
    ctx.line_to(*top)
    ctx.stroke()
    dashed(ctx, top[0], 150, top[0], top[1], 4, "#C9781E", k3, (16, 10), -t * 30)
    ctx.set_line_width(5)
    setc(ctx, "#7A3A12", k3)
    ctx.move_to(*top)
    ctx.line_to(al[0] + 70, al[1] + 10)
    ctx.stroke()
    label(ctx, "亚历山大港：影子偏 7.2°", al[0] - 40, al[1] - 280, 30, ink, k3, "serif_sb", shadow=False)
    k4 = smooth(prog(u, 1.8, 2.6))
    if k4 > 0:
        for p in (sy, al):
            dashed(ctx, p[0], p[1], lerp(p[0], ox, k4 * 0.45), lerp(p[1], oy, k4 * 0.45), 3, ink, 0.7, (10, 8))
        label(ctx, "圆心角也是 7.2°", 640, 900, 32, "#7A3A12", k4, "serif_sb", shadow=False)
    k5, k6 = smooth(prog(u, 2.6, 3.2)), smooth(prog(u, 4.0, 4.6))
    rrect(ctx, 1240, 430, 600, 360, 18)
    setc(ctx, "#F6E8C6", 0.85 * k5)
    ctx.fill()
    label(ctx, "7.2° = 360° ÷ 50", 1540, 490, 36, ink, k5, "serif_k", shadow=False)
    label(ctx, "两地相距 5000 斯塔德", 1540, 560, 30, ink, k5, "serif_r", shadow=False)
    label(ctx, "周长 = 5000 × 50", 1540, 630, 34, ink, k6, "serif_sb", shadow=False)
    label(ctx, "= 25 万斯塔德 ≈ 4 万公里", 1540, 700, 36, "#9A3A12", k6, "serif_k", shadow=False)
    label(ctx, "（示意图，角度已放大）", 300, 930, 22, "#6A4A2A", 0.8, "serif_r", shadow=False)
    film.vignette(ctx, 0.4, color="#2A1A0A")


# ================================================================ D：阿基米德与圆周率（56–64）

STAGES = [(6, 58.4), (12, 58.9), (24, 59.4), (48, 59.9), (96, 60.4), (3072, 61.4)]


def _shot_pi(ctx, t):
    china = smooth(prog(t, 61.0, 61.8))
    ctx.set_source(rad(960, 520, 0, 1200, [(0, mix("#3A2A1A", "#2A2622", china)), (1, mix("#1E1610", "#141210", china))]))
    ctx.paint()
    film.paint_texture(ctx, "paper", 0, 0, W, H, 0.15 + 0.15 * china)
    cx, cy, r = 700, 540, 320
    n = 6
    for nn, ts in STAGES:
        if t >= ts:
            n = nn

    def ngon(rr, k):
        return [(cx + math.cos(-math.pi / 2 + i / k * TAU) * rr, cy + math.sin(-math.pi / 2 + i / k * TAU) * rr)
                for i in range(k + 1)]
    ctx.set_line_width(4)
    setc(ctx, "#F2E2C2", 0.85)
    circle(ctx, cx, cy, r)
    ctx.stroke()
    if n <= 96:
        stroke_pts(ctx, ngon(r / math.cos(math.pi / n), n), 3, "#FF9A5A", 0.85)
        stroke_pts(ctx, ngon(r, n), 3, "#7FC8FF", 0.85)
        lo, hi = n * math.sin(math.pi / n), n * math.tan(math.pi / n)
        if n == 96:
            lo, hi = 3 + 10 / 71, 3 + 1 / 7
    else:
        stroke_pts(ctx, ngon(r, 192), 3, "#7FC8FF", 0.85)
        lo, hi = 3.14159, 3.14160
    label(ctx, f"{n} 边形", cx, cy - 14, 64, "#FFE8C0", 1.0, "serif_k")
    label(ctx, "内接 ↔ 外切", cx, cy + 50, 28, "#CDBA92", 1.0, "serif_r")
    x0 = 1450
    if t < 61.0:
        label(ctx, f"{lo:.4f}  <  π  <  {hi:.4f}", x0, 420, 46, "#FFE8C0", 1.0, "latin")
        if n >= 96:
            label(ctx, "阿基米德：3 10/71 < π < 3 1/7", x0, 500, 30, "#F2D79B", smooth(prog(t, 60.4, 60.9)), "serif_sb")
    else:
        label(ctx, "刘徽 · 割圆术（263 年）", x0, 300, 40, "#F4E6C8", china, "serif_k")
        label(ctx, "割之弥细，所失弥少", x0, 360, 32, "#D9C49A", china, "kai")
        label(ctx, "3072 边形 → π ≈ 3.1416", x0, 420, 34, "#FFE8C0", smooth(prog(t, 61.6, 62.0)), "serif_sb")
        k2 = smooth(prog(t, 62.0, 62.6))
        label(ctx, "祖冲之（约 480 年）", x0, 540, 40, "#F4E6C8", k2, "serif_k")
        label(ctx, "3.1415926  <  π  <  3.1415927", x0, 610, 40, "#FFD27A", k2, "latin")
        label(ctx, "领先世界 900 多年", x0, 700, 36, "#FF9A5A", smooth(prog(t, 62.8, 63.4)), "serif_k")
    film.vignette(ctx, 0.55)


def _shot_d(ctx, t):
    if t < 58.4:
        arch(ctx, t, "archimedes", 56.0, 58.4, (0.5, 0.4, 1.05), (0.5, 0.33, 1.3), "多梅尼科·费蒂《沉思的阿基米德》",
             "1620 年 · 德累斯顿历代大师画廊 · 公有领域", cap=(0.1, 2.3))
    else:
        _shot_pi(ctx, t)


# ================================================================ E：亚历山大图书馆（64–70）


def _shot_e(ctx, t):
    u = t - 64.0
    dim = smooth(prog(u, 2.8, 6.0))
    arch(ctx, t, "library_alex", 64.0, 70.0, (0.5, 0.45, 1.05), (0.5, 0.58, 1.4), "亚历山大图书馆（想象图）",
         "O. 冯·科文绘 · 19 世纪 · 公有领域", grade="sepia", cap=(0.3, 5.2))
    film.dust(ctx, t, 50, 4, (400, 100, 1100, 860), "#FFE6B8", 0.4 * (1 - dim))
    film.vignette(ctx, 0.3 + 0.4 * dim)
    film.fade_black(ctx, 0.4 * dim)


# ================================================================ 主绘制


SHOTS = [(0.0, _shot_a0), (6.2, _shot_a), (10.0, _shot_b), (42.0, _shot_c0), (45.0, lambda c, t: _shot_well(c, t, t - 45.0)),
         (48.4, lambda c, t: _shot_diagram(c, t, t - 48.4)), (56.0, _shot_d), (64.0, _shot_e)]
TRANS = {2: ("dissolve", 1.0), 3: ("luma", 0.9), 4: ("dissolve", 0.7), 5: ("zoomblur", 0.6, {"y": 600}),
         6: ("lightsweep", 0.9, {"color": "#FFE2B0"}), 7: ("dissolve", 1.0)}


def draw(ctx, t):
    sequence(ctx, t, SHOTS, TRANS)


def sfx():
    out = [
        (0.0, "ambience_sea", {"dur": 10.0, "gain": 0.35}), (0.0, "ambience_birds", {"dur": 10.0, "gain": 0.2}),
        (10.0, "ambience_room", {"dur": 32.0, "gain": 0.35}), (10.2, "page", {"gain": 0.3}),
        (13.0, "chalk", {"dur": 1.6, "gain": 0.25}), (15.2, "sand", {"dur": 0.8, "gain": 0.2}),
        (16.4, "slide", {"gain": 0.2}), (17.8, "ding", {"gain": 0.25}),
        (20.0, "chalk", {"dur": 1.6, "gain": 0.25}), (23.2, "slide", {"gain": 0.18}), (23.6, "slide", {"gain": 0.18}),
        (24.0, "slide", {"gain": 0.18}), (26.0, "ding", {"gain": 0.28}),
        (28.0, "quill", {"dur": 3.0, "gain": 0.2}), (32.6, "sparkle", {"dur": 1.0, "gain": 0.2}),
        (35.0, "chalk", {"dur": 1.0, "gain": 0.2}),
    ]
    for i in range(2):
        out.append((35.4 + i * 0.6, "thud", {"gain": 0.25, "pitch": 0.9}))
    for i in range(3):
        out.append((36.8 + i * 0.4, "thud", {"gain": 0.22, "pitch": 1.05}))
    for i in range(7):
        out.append((38.2 + i * 0.14, "tick", {"gain": 0.2}))
    out += [(39.4, "ding", {"gain": 0.28}),
            (42.0, "ambience_room", {"dur": 3.0, "gain": 0.35}), (45.0, "ambience_cave", {"dur": 3.4, "gain": 0.4}),
            (45.4, "drip", {"gain": 0.3}), (45.8, "sparkle", {"dur": 1.0, "gain": 0.2}),
            (48.4, "ambience_room", {"dur": 7.6, "gain": 0.35}), (48.6, "quill", {"dur": 2.0, "gain": 0.22}),
            (51.0, "quill", {"dur": 1.6, "gain": 0.2}), (53.0, "ding", {"gain": 0.18}),
            (56.0, "ambience_room", {"dur": 8.0, "gain": 0.35})]
    for nn, ts in STAGES:
        out.append((ts, "tick", {"gain": 0.3}))
    out += [(61.0, "swish", {"gain": 0.2}), (62.8, "chime", {"gain": 0.16}),
            (64.0, "ambience_room", {"dur": 6.0, "gain": 0.45}), (66.6, "hush", {"dur": 2.4, "gain": 0.3}),
            (68.0, "rumble", {"dur": 2.0, "gain": 0.25})]
    return out
