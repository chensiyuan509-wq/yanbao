"""第一章 火与石：第一视角打石、打火；拉斯科洞窟壁画（火光下）；阿根廷手洞；巨角鹿下的一排点与刻痕骨；
麦田；康斯太布尔《巨石阵》；夏至日出。人物都是扮成原始人的 Claude。关键词：观察。"""
import math

from ..core import (TAU, H, W, at, circle, clamp, ease_in, ease_io, ease_out, ellipse, fbm, glow, lerp, lin, mix,
                    poly, prog, rad, rng, rrect, setc, smooth, text)
from .. import film
from ..archive import caption, kb
from mascot import draw_prop
from .common import arch, claude, label, lit, role, sequence

DUR = 38.0
CHAPTER = dict(num="第 一 章", title="火与石", era="约 330 万年前 — 5000 年前", key="观察", at=0.4, dur=4.0)
GRAIN = 0.1

VO = [
    (4.6, "330 万年前，祖先敲出了第一批{石器}；"),
    (6.9, "至少 100 万年前，他们学会了{用火}。"),
    (9.5, "火光下，人们在洞壁上画下野牛和骏马——"),
    (12.4, "这是最早的{记录}：把看见的世界，留给后来的人。"),
    (15.6, "各地的洞穴里，还留着一个个手印，像在说：{我来过}。"),
    (19.3, "人们也在数月亮：拉斯科的巨角鹿下方有一排点，"),
    (22.4, "一根 4 万多年前的骨头上，刻着 {29 道}刻痕——月亮约 29.5 天圆缺一轮。"),
    (27.2, "约 1 万年前，人类开始{种庄稼}，播种要看季节；"),
    (30.6, "5000 年前的巨石阵，主轴正对{夏至日出}。"),
    (34.0, "日升月落，周而复始——发现规律，是科学的{第一步}。", {"spill": 0.6}),
]

SUPERS = [
    (4.7, 7.6, "约 330 万年前", "东非 · 已知最早的石器"),
    (27.3, 30.4, "约 1 万年前", "新月沃地 · 农业出现"),
]

# ================================================================ A：第一视角打石、打火（0–9）

KNAPS = [0.9, 1.7, 2.5, 3.3]
FLINTS = [4.3, 5.0, 5.7]
IGNITE = 5.9


def _strike(t, times, rest, wind, hit):
    for ts in times:
        if ts - 0.5 <= t <= ts + 0.35:
            if t < ts - 0.22:
                u = ease_out((t - (ts - 0.5)) / 0.28)
                return (lerp(rest[0], wind[0], u), lerp(rest[1], wind[1], u))
            if t < ts:
                u = ease_in((t - (ts - 0.22)) / 0.22)
                return (lerp(wind[0], hit[0], u), lerp(wind[1], hit[1], u))
            u = ease_out((t - ts) / 0.35)
            return (lerp(hit[0], rest[0], u), lerp(hit[1], rest[1], u) - math.sin(u * math.pi) * 30)
    return rest


def _flakes(ctx, t, ts, x, y, seed, n=7):
    u = t - ts
    if u < 0 or u > 1.0:
        return
    R = rng(seed)
    for i in range(n):
        vx, vy = R.uniform(-420, 420), R.uniform(-520, -150)
        px, py = x + vx * u, y + vy * u + 900 * u * u
        s = R.uniform(6, 14) * (1 - u * 0.4)
        ctx.save()
        ctx.translate(px, py)
        ctx.rotate(u * R.uniform(-12, 12))
        poly(ctx, [(-s, -s * 0.4), (s * 0.8, -s * 0.7), (s, s * 0.5), (-s * 0.6, s * 0.6)])
        setc(ctx, "#9A948C", 1 - u)
        ctx.fill()
        ctx.restore()


def _sparks(ctx, t, ts, x, y, seed, n=22, big=1.0):
    u = t - ts
    if u < 0 or u > 0.9:
        return
    R = rng(seed)
    glow(ctx, x, y, 160 * big * (1 - u), "#FFB347", 0.7 * (1 - u) ** 2)
    for i in range(n):
        ang = R.uniform(-math.pi * 0.95, -math.pi * 0.05)
        sp = R.uniform(300, 900) * big
        px = x + math.cos(ang) * sp * u
        py = y + math.sin(ang) * sp * u + 700 * u * u
        q = max(0, u - 0.05)
        qx = x + math.cos(ang) * sp * q
        qy = y + math.sin(ang) * sp * q + 700 * q * q
        ctx.set_line_width(3.2 * (1 - u))
        setc(ctx, "#FFD27A", 1 - u / 0.9)
        ctx.move_to(qx, qy)
        ctx.line_to(px, py)
        ctx.stroke()


def _acacia(ctx, x, y, s, color):
    setc(ctx, color)
    ctx.set_line_width(10 * s)
    ctx.move_to(x, y)
    ctx.curve_to(x + 5 * s, y - 60 * s, x - 10 * s, y - 100 * s, x + 4 * s, y - 140 * s)
    ctx.stroke()
    ctx.set_line_width(6 * s)
    for dx in (-60, -25, 30, 70):
        ctx.move_to(x + 2 * s, y - 110 * s)
        ctx.line_to(x + dx * s, y - 150 * s)
        ctx.stroke()
    ellipse(ctx, x + 5 * s, y - 160 * s, 130 * s, 24 * s)
    ctx.fill()


CAVE_FOLK = [role(560, 790, 0.36, "caveman", "wonder", seed=11.0, palette="clay").sit(0, 1.0, 0.01).look(0, 0.6, -0.2),
             role(1370, 800, 0.38, "caveman", "awe", seed=12.0, palette="sienna", flip=True).sit(0, 1.0, 0.01)
             .look(0, -0.6, -0.2),
             role(1580, 770, 0.3, "caveman", "smile", seed=13.0, palette="ochre", flip=True).sit(0, 1.0, 0.01)]


def _shot_a(ctx, t):
    fire_k = smooth(prog(t, IGNITE, IGNITE + 1.4))
    warm = fire_k * film.flicker(t, 3.0, 0.15)
    film.sky(ctx, [(0, "#060A16"), (0.55, "#101C34"), (0.62, "#1C2A44"), (1, "#0A0C12")])
    film.star_field(ctx, t, 220, 41, area=(0, 90, W, 560), a=0.85 * (1 - 0.4 * fire_k))
    film.moon(ctx, 1520, 230, 34, 0.18, 0.9, glow_a=0.35)
    film.ridge(ctx, -50, W + 50, 640, 70, 0.004, 3.0, "#0F1522", 1.0, step=16)
    _acacia(ctx, 1380, 652, 1.0, "#0A0F18")
    _acacia(ctx, 420, 650, 0.6, "#0C121C")
    ctx.set_source(lin(0, 630, 0, H, [(0, "#0D1018"), (1, "#05060A")]))
    ctx.rectangle(-50, 632, W + 100, H)
    ctx.fill()
    if fire_k > 0:
        glow(ctx, 960, 860, 900, "#FF8A2A", 0.35 * warm)
        with lit("#FF9A50", 0.55, 0.25 + 0.7 * fire_k):
            for f in CAVE_FOLK:
                f.draw(ctx, t)
    nx, ny = 960, 880
    for i in range(26):
        R = rng(i + 5)
        a0 = R.uniform(-math.pi, 0)
        L = R.uniform(30, 70)
        ctx.set_line_width(3)
        setc(ctx, mix("#4A3A22", "#C9963F", 0.3 + 0.7 * warm), 0.9)
        ctx.move_to(nx + R.uniform(-40, 40), ny + 10)
        ctx.line_to(nx + math.cos(a0) * L, ny + math.sin(a0) * L * 0.5)
        ctx.stroke()
    smold = smooth(prog(t, FLINTS[-1], IGNITE + 0.3))
    if smold > 0:
        glow(ctx, nx, ny - 5, 80, "#FF6A1A", 0.8 * smold * (1 - fire_k * 0.5))
    if fire_k > 0:
        film.fire(ctx, nx, ny + 10, 190 * ease_out(fire_k), t, 1.0, seed=2.0)
        film.embers(ctx, t, nx, ny - 60, 26, 7, spread=120, height=520, a=fire_k)
    down = ease_in(prog(t, IGNITE + 0.4, IGNITE + 1.5)) * 520
    bob = math.sin(t * 1.5) * 6
    left_tip = (820, 830 + down + bob)
    rt = _strike(t, KNAPS + FLINTS, (1210, 760), (1330, 560), (900, 800))
    right_tip = (rt[0], rt[1] + down + bob)
    with lit(mix("#7A9CFF", "#FFB070", fire_k), 0.55, 0.55 + 0.45 * max(fire_k, smold * 0.4)):
        film.pov_arm(ctx, (260, 1320), left_tip, 150)
        film.pov_arm(ctx, (1660, 1320), right_tip, 150)
        with at(ctx, left_tip[0] + 30, left_tip[1] - 60, 1.7, 0.2):
            draw_prop(ctx, ("stone",), t)
        with at(ctx, right_tip[0] - 20, right_tip[1] - 50, 1.25, -0.4):
            draw_prop(ctx, ("stone",), t)
    for k, ts in enumerate(KNAPS):
        _flakes(ctx, t, ts, 880, 790, 10 + k)
        if t >= ts:
            glow(ctx, 880, 790, 120, "#BFD6FF", 0.5 * max(0, 1 - (t - ts) / 0.25))
    for k, ts in enumerate(FLINTS):
        _sparks(ctx, t, ts, 880, 780, 30 + k, 24, 1.0 + 0.2 * k)
    u = prog(t, FLINTS[-1], IGNITE)
    if 0 < u < 1:
        glow(ctx, lerp(880, nx, u), lerp(780, ny - 10, ease_in(u)) - math.sin(u * math.pi) * 60, 30, "#FFC46B", 0.9)
    film.vignette(ctx, 0.65)


# ================================================================ B：拉斯科（火光下）与手洞（9–19）

FIRE_FOLK = [role(420, 960, 0.5, "caveman", "wonder", seed=21.0, palette="clay").sit(0, 1.0, 0.01).look(0, 0.4, -0.7),
             role(1560, 965, 0.55, "caveman", "smile", seed=22.0, palette="sienna", flip=True).sit(0, 1.0, 0.01)
             .look(0, -0.5, -0.6).wave(10.5, 12.0, "r"),
             claude(1220, 968, 0.42, "awe", seed=23.0).sit(0, 1.0, 0.01).look(0, -0.3, -0.9)]


def _shot_b1(ctx, t):
    fl = film.flicker(t, 5.0, 0.22)
    kb(ctx, "lascaux_replica", t, 9.0, 14.6, (0.42, 0.5, 1.35), (0.62, 0.55, 1.75), grade="fire")
    # 火光：随火焰明暗起伏，画面四周压暗
    ctx.set_source_rgba(0.05, 0.02, 0.0, 0.45 - 0.25 * (fl - 0.85) / 0.15)
    ctx.paint()
    ctx.set_source(rad(980, 1100, 100, 1500, [(0, "#FFB060", 0.25 * fl), (0.5, "#FF8A2A", 0.06), (1, "#000000", 0.55)]))
    ctx.paint()
    # 前景：火堆与围坐的 Claude 们（逆光）
    film.fire(ctx, 900, 975, 200, t, 1.0, seed=6.0)
    film.embers(ctx, t, 900, 880, 26, 15, spread=180, height=700, a=0.9)
    with lit("#2A1408", 0.65, 0.5 + 0.2 * fl):
        for f in FIRE_FOLK:
            f.draw(ctx, t)
    film.vignette(ctx, 0.6)
    caption(ctx, "拉斯科洞窟壁画（复制洞）", "法国 · 约 1.7 万年前 · 照片：公有领域",
            smooth(prog(t, 9.6, 10.2)) * (1 - smooth(prog(t, 13.9, 14.4))))


def _shot_b2(ctx, t):
    """阿根廷手洞：镜头慢慢推近手印墙，第一视角的手伸过去，和几千年前的手印对齐。"""
    arch(ctx, t, "manos", 14.6, 19.0, (0.35, 0.52, 1.15), (0.6, 0.5, 1.7), "阿根廷 · 手洞（Cueva de las Manos）",
         "约 9300 — 1300 年前 · 照片：公有领域", grade="warm", cap=(0.4, 4.0))
    reach = ease_out(prog(t, 15.6, 17.8))
    if reach > 0:
        with lit("#FFC890", 0.3, 0.9):
            film.pov_arm(ctx, (1500, 1400), (lerp(1500, 1150, reach), lerp(1300, 640, reach)), 150)


# ================================================================ C：数月亮（19–27）

DOTS = [(0.405, 0.885), (0.435, 0.875), (0.47, 0.885), (0.51, 0.882), (0.555, 0.885), (0.6, 0.875),
        (0.642, 0.86), (0.685, 0.86), (0.725, 0.858), (0.77, 0.865), (0.82, 0.86), (0.87, 0.86), (0.925, 0.858)]


def _shot_c1(ctx, t):
    to = arch(ctx, t, "lascaux_megaloceros", 19.0, 22.4, (0.5, 0.55, 1.05), (0.6, 0.7, 1.3),
              "拉斯科：巨角鹿下的一排点", "约 1.7 万年前 · 有学者推测与月相计数有关", grade="warm", cap=(0.3, 3.2))
    for i, (u, v) in enumerate(DOTS):
        k = smooth(prog(t, 20.0 + i * 0.12, 20.3 + i * 0.12))
        if k > 0 and to:
            x, y = to(u, v)
            glow(ctx, x, y, 60, "#FFE2A0", 0.55 * k)
            film.moon(ctx, x, y - 90, 24, (i + 1) / 26.0, k, dark_a=0.35, glow_a=0.3, craters=False)


def _shot_c2(ctx, t):
    """第一视角：在骨头上刻痕，每一道对应一个月相。"""
    u = t - 22.4
    warm = film.flicker(t, 6.0, 0.1)
    ctx.set_source(rad(960, 620, 0, 1100, [(0, "#3A2414"), (0.6, "#1A0F08"), (1, "#070402")]))
    ctx.paint()
    glow(ctx, 1700, 900, 900, "#FF8A3A", 0.25 * warm)
    bx0, bx1, by = 330, 1590, 640

    def bone(c):
        c.move_to(bx0, by - 40)
        c.curve_to(700, by - 62, 1200, by - 60, bx1, by - 44)
        c.curve_to(bx1 + 40, by - 40, bx1 + 50, by + 40, bx1, by + 44)
        c.curve_to(1200, by + 58, 700, by + 62, bx0, by + 40)
        c.curve_to(bx0 - 50, by + 30, bx0 - 50, by - 30, bx0, by - 40)
        c.close_path()
    bone(ctx)
    ctx.set_source(lin(0, by - 60, 0, by + 60, [(0, "#F1E3C4"), (0.45, "#D7C29A"), (1, "#8C7650")]))
    ctx.fill()
    film.paint_texture(ctx, "paper", bx0 - 60, by - 70, bx1 - bx0 + 120, 140, 0.25, clip_path=bone)
    nmax = 29
    nk = min(nmax, int(max(0.0, u) / 0.12))
    for i in range(nk):
        x = bx0 + 60 + i * (bx1 - bx0 - 120) / (nmax - 1)
        ctx.set_line_width(5)
        setc(ctx, "#4A3420", 0.9)
        ctx.move_to(x - 3, by - 34)
        ctx.line_to(x + 3, by + 30)
        ctx.stroke()
        film.moon(ctx, x, by - 110 - (i % 2) * 34, 13, (i + 1) / 29.5, 0.9, dark_a=0.25, glow_a=0.15, craters=False)
    label(ctx, f"{nk}", 960, 300, 96, "#FFE8C0", 1.0, "serif_k")
    label(ctx, "道刻痕 · 列邦博骨（约 4.4 万年前）", 960, 380, 30, "#D9C49A", 1.0, "serif_r")
    if nk >= 29:
        label(ctx, "≈ 一个月相周期（29.5 天）", 960, 860, 34, "#F2D79B", smooth(prog(u, 3.6, 4.0)), "serif_sb")
    i = min(nk, nmax - 1)
    tx = bx0 + 60 + i * (bx1 - bx0 - 120) / (nmax - 1) + 20
    cut = math.sin(t * TAU * 7) * 10
    with lit("#FF9A50", 0.45, 0.8 + 0.2 * warm):
        film.pov_arm(ctx, (1500, 1350), (tx + 120, 760 + cut), 140)
        with at(ctx, tx + 40, 700 + cut, 0.9, -0.6):
            draw_prop(ctx, ("stone",), t)
        film.pov_arm(ctx, (180, 1350), (bx0 + 120, by + 120), 150)
    film.vignette(ctx, 0.6)


# ================================================================ D：麦田、巨石阵（27–38）


def _wheat(ctx, t, x0, x1, y_base, h, n, seed, color, head, wind=1.0):
    R = rng(seed)
    for i in range(n):
        x = R.uniform(x0, x1)
        hh = h * R.uniform(0.75, 1.15)
        sway = (fbm(t * 0.6 + x * 0.004, seed) * 18 + math.sin(t * 2.0 + x * 0.02) * 6) * wind
        tx, ty = x + sway, y_base - hh
        ctx.set_line_width(2.4)
        setc(ctx, color)
        ctx.move_to(x, y_base + 20)
        ctx.curve_to(x, y_base - hh * 0.4, tx - sway * 0.3, ty + hh * 0.3, tx, ty)
        ctx.stroke()
        ctx.save()
        ctx.translate(tx, ty)
        ctx.rotate(sway * 0.01 + 0.2)
        ellipse(ctx, 0, -10, 6, 22)
        setc(ctx, head)
        ctx.fill()
        ctx.restore()


FARMERS = [role(1300, 860, 0.36, "caveman", "focused", seed=31.0, palette="clay").type(27.0, 30.6),
           role(1560, 850, 0.32, "caveman", "smile", seed=32.0, palette="sienna", flip=True)]
W1 = (claude(380, 905, 0.5, "smile", seed=6.0).look(27.0, 0.6, -0.2)
      .walk_to(27.1, 30.6, 900, 905, stride=0.8).expr(28.8, "curious").look(29.0, 0.5, -0.7))


def _shot_d1(ctx, t):
    u = t - 27.0
    camx = 90 * ease_io(prog(u, 0, 3.6))
    film.sky(ctx, [(0, "#3B4A73"), (0.45, "#E39A62"), (0.62, "#F6C27A"), (1, "#7A4A2A")])
    film.sun(ctx, 360, 560, 44, 1.0, "#FFE7B8", "#FFB766", 600)
    film.beams(ctx, 360, 560, 0.1, 1.3, 1400, 9, "#FFE2A8", 0.08, t, 4)
    for (yb, amp, sd, col, par) in ((640, 90, 11.0, "#8A5A4A", 0.2), (690, 60, 12.0, "#6E4636", 0.4)):
        ctx.save()
        ctx.translate(-camx * par, 0)
        film.ridge(ctx, -100, W + 300, yb, amp, 0.003, sd, col, 1.0, step=18)
        ctx.restore()
    ctx.save()
    ctx.translate(-camx * 0.6, 0)
    ctx.set_source(lin(0, 690, 0, 1000, [(0, "#B57A3A"), (1, "#5A3A1A")]))
    ctx.rectangle(-200, 700, W + 600, 400)
    ctx.fill()
    _wheat(ctx, t, -200, W + 400, 760, 60, 220, 3, "#C8913E", "#E6B65A", 0.6)
    with lit("#FFC890", 0.3, 0.95):
        for f in FARMERS:
            f.draw(ctx, t)
    _wheat(ctx, t, -200, W + 400, 860, 80, 180, 4, "#B9802F", "#E2AE4F", 0.8)
    ctx.restore()
    ctx.save()
    ctx.translate(-camx, 0)
    with lit("#FFC890", 0.3, 1.0):
        W1.draw(ctx, t)
    _wheat(ctx, t, -200, W + 400, 975, 120, 150, 5, "#9C6828", "#D99E45", 1.0)
    ctx.restore()
    film.grade(ctx, "#FFB070", 0.25)
    film.vignette(ctx, 0.5)


def _megalith(ctx, x, y, w, h, color, rim, rim_a, seed):
    R = rng(seed)
    for dx in (0, w * 0.62):
        pts = [(x + dx + R.uniform(-4, 4), y), (x + dx + w * 0.38 + R.uniform(-4, 4), y),
               (x + dx + w * 0.36 + R.uniform(-3, 3), y - h), (x + dx + w * 0.02 + R.uniform(-3, 3), y - h)]
        poly(ctx, pts)
        setc(ctx, color)
        ctx.fill()
        ctx.set_line_width(3)
        setc(ctx, rim, rim_a)
        ctx.move_to(*pts[1])
        ctx.line_to(*pts[2])
        ctx.stroke()
    rrect(ctx, x - 6, y - h - h * 0.17, w + 12, h * 0.18, 6)
    setc(ctx, color)
    ctx.fill()


S1 = claude(960, 930, 0.42, "gaze", seed=7.0)


def _shot_d2(ctx, t):
    """康斯太布尔的《巨石阵》（1835）。"""
    arch(ctx, t, "stonehenge", 30.6, 34.0, (0.46, 0.5, 1.18), (0.5, 0.56, 1.45),
         "约翰·康斯太布尔《巨石阵》", "1835 年 · 水彩 · 维多利亚与阿尔伯特博物馆 · 公有领域", cap=(0.3, 3.2))


def _shot_d3(ctx, t):
    """夏至日出：太阳从巨石缝里升起，光带铺到 Claude 脚下。"""
    u = t - 34.0
    rise = ease_out(prog(u, 0.0, 3.0))
    push = 1 + 0.08 * ease_in(prog(u, 1.5, 4.0))
    ctx.save()
    ctx.translate(960, 600)
    ctx.scale(push, push)
    ctx.translate(-960, -600)
    film.sky(ctx, [(0, "#2A3150"), (0.4, "#9A6A6A"), (0.6, "#F0A86A"), (0.68, "#FFD49A"), (1, "#3A2418")])
    sx, sy = 960, lerp(720, 590, rise)
    film.sun(ctx, sx, sy, 32, 1.0, "#FFF0C8", "#FFB766", 700)
    film.beams(ctx, sx, sy, math.pi / 2, 0.5, 900, 7, "#FFE6B0", 0.18 * rise, t, 8, 0.03)
    film.ridge(ctx, -50, W + 50, 700, 40, 0.002, 21.0, "#4A3030", 1.0, step=20)
    ctx.set_source(lin(0, 690, 0, H, [(0, "#3A2A22"), (1, "#120C08")]))
    ctx.rectangle(-50, 700, W + 100, 500)
    ctx.fill()
    ctx.move_to(sx - 30, 705)
    ctx.line_to(sx + 30, 705)
    ctx.line_to(sx + 420, H + 50)
    ctx.line_to(sx - 420, H + 50)
    ctx.close_path()
    ctx.set_source(lin(0, 705, 0, H, [(0, "#FFD89A", 0.75 * rise), (1, "#FFB060", 0.15 * rise)]))
    ctx.fill()
    rim_a = 0.4 + 0.6 * rise
    for (x, y, w, h, sd) in ((-120, 900, 300, 420, 1), (250, 840, 250, 330, 2), (560, 790, 220, 250, 3),
                             (1140, 790, 220, 250, 4), (1420, 840, 250, 330, 5), (1740, 900, 300, 420, 6)):
        _megalith(ctx, x, y, w, h, "#120C0A", "#FFC27A", rim_a, sd)
    _megalith(ctx, 805, 745, 310, 200, "#140E0B", "#FFD49A", rim_a, 9)
    glow(ctx, 960, 830, 200, "#FFD49A", 0.3 * rise)
    with lit("#3A2010", 0.7, 0.35 + 0.2 * rise):
        S1.draw(ctx, t, spin=math.pi)
    ctx.restore()
    label(ctx, "夏至日出 · 主轴方向", 960, 470, 30, "#FFF0D8", smooth(prog(u, 1.2, 1.8)) * (1 - smooth(prog(u, 3.4, 3.8))),
          "serif_sb")
    film.grade(ctx, "#FF9A50", 0.2)
    film.vignette(ctx, 0.55)
    if u > 2.6:
        glow(ctx, 960, 590, 900, "#FFE6B8", 0.6 * ease_in(prog(u, 2.6, 4.0)))


# ================================================================ 主绘制


SHOTS = [(0.0, _shot_a), (9.0, _shot_b1), (14.6, _shot_b2), (19.0, _shot_c1), (22.4, _shot_c2), (27.0, _shot_d1),
         (30.6, _shot_d2), (34.0, _shot_d3)]
TRANS = {1: ("dissolve", 1.0), 2: ("luma", 0.9), 3: ("dissolve", 0.8), 4: ("defocus", 0.8, {"max": 10}),
         5: ("lightsweep", 1.0, {"color": "#FFE2B0"}), 6: ("dissolve", 1.0), 7: ("luma", 1.0)}


def draw(ctx, t):
    sequence(ctx, t, SHOTS, TRANS)


def sfx():
    out = [(0.0, "ambience_wind", {"dur": 9.0, "gain": 0.45}), (0.0, "ambience_night", {"dur": 9.0, "gain": 0.3})]
    for k, ts in enumerate(KNAPS):
        out.append((ts - 0.01, "knap", {"gain": 0.55, "pitch": 1 + 0.06 * (k % 3)}))
    for ts in FLINTS:
        out.append((ts - 0.01, "flint", {"gain": 0.55}))
    out += [
        (IGNITE - 0.1, "ignite", {"gain": 0.6}), (IGNITE + 0.2, "ambience_fire", {"dur": 3.0, "gain": 0.6}),
        (9.0, "ambience_fire", {"dur": 10.0, "gain": 0.7}), (9.0, "ambience_cave", {"dur": 10.0, "gain": 0.4}),
        (15.6, "hush", {"dur": 2.5, "gain": 0.3}), (17.6, "impact_soft", {"gain": 0.25}),
        (19.0, "ambience_night", {"dur": 8.0, "gain": 0.4}),
    ]
    for i in range(13):
        out.append((20.0 + i * 0.12, "sparkle", {"dur": 0.3, "gain": 0.05}))
    for i in range(0, 29, 2):
        out.append((22.5 + i * 0.12, "carve", {"dur": 0.22, "gain": 0.33}))
    out += [(27.0, "ambience_birds", {"dur": 3.8, "gain": 0.45}), (27.0, "ambience_wind", {"dur": 7.2, "gain": 0.3}),
            (30.6, "rumble", {"dur": 2.5, "gain": 0.2}), (34.0, "hush", {"dur": 3.0, "gain": 0.3}),
            (35.6, "swell", {"dur": 2.4, "gain": 0.3})]
    return out
