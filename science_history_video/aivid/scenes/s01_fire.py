"""第一章 火与石：第一视角打制石器、燧石打火；山洞里的篝火、人影与手印；月相与刻痕骨；
麦田；巨石阵的夏至日出。关键词：观察。"""
import math

from ..core import (TAU, H, W, Cam, at, circle, clamp, ease_in, ease_io, ease_out, ellipse, fbm, glow, kf,
                    lerp, lin, mix, noise, poly, prog, rad, rng, rrect, setc, smooth, star4, text, view)
from .. import film, starmap
from mascot import draw_prop
from .common import claude, fade_io, label, lit

DUR = 48.0
CHAPTER = dict(num="第 一 章", title="火与石", era="约 330 万年前 — 5000 年前", key="观察", at=0.7, dur=4.4)
GRAIN = 0.1

VO = [
    (5.2, "330 万年前，人类的祖先敲出了{石器}。"),
    (8.4, "敲哪里、用多大力？——这是最早的{试错}。"),
    (11.3, "至少 100 万年前，他们学会了{用火}。"),
    (13.9, "火让食物更好消化，让黑夜变短，"),
    (16.9, "也让人们围坐在一起：讲述、模仿、{传授}。"),
    (20.4, "至少 4 万年前，有人在洞壁上留下了{手印}。"),
    (24.9, "夜里，他们看着月亮一天天变化。"),
    (27.5, "一根 4 万多年前的骨头上，刻着 {29 道}刻痕——"),
    (30.9, "也许是在数日子：月亮每 {29 天半}，圆缺一轮。"),
    (34.9, "大约 1 万年前，人类开始{种庄稼}。"),
    (37.5, "什么时候播种？要看{太阳和星星}。"),
    (40.4, "巨石阵，正对着{夏至日出}的方向。"),
    (43.4, "日升月落，世界是{有规律}的。"),
    (45.9, "发现规律，是科学的{第一步}。", {"spill": 0.6}),
]

SUPERS = [
    (5.3, 8.6, "约 330 万年前", "东非 · 已知最早的石器"),
    (11.4, 13.4, "至少 100 万年前", "人类学会用火"),
    (20.5, 24.2, "4 万多年前", "洞穴岩画与手印"),
    (27.6, 30.8, "约 4.4 万年前", "列邦博骨 · 29 道刻痕"),
    (35.0, 38.6, "约 1 万年前", "新月沃地 · 农业出现"),
    (40.5, 43.6, "约 5000 年前", "巨石阵 · 正对夏至日出"),
]

# ================================================================ 镜头 A：第一视角，打石头、打火

KNAPS = [1.9, 3.1, 4.3, 5.5, 6.7]
FLINTS = [8.6, 9.4, 10.2]
IGNITE = 10.35


def _strike_pose(t, times, rest, wind, hit):
    """右手：举起 → 砸下 → 回弹。"""
    best = rest
    for ts in times:
        if ts - 0.55 <= t <= ts + 0.4:
            if t < ts - 0.25:
                u = ease_out((t - (ts - 0.55)) / 0.3)
                return (lerp(rest[0], wind[0], u), lerp(rest[1], wind[1], u))
            if t < ts:
                u = ease_in((t - (ts - 0.25)) / 0.25)
                return (lerp(wind[0], hit[0], u), lerp(wind[1], hit[1], u))
            u = ease_out((t - ts) / 0.4)
            return (lerp(hit[0], rest[0], u), lerp(hit[1], rest[1], u) - math.sin(u * math.pi) * 30)
    return best


def _flakes(ctx, t, ts, x, y, seed, n=7, color="#9A948C"):
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
        setc(ctx, color, 1 - u)
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
        tail = 0.05
        qx = x + math.cos(ang) * sp * max(0, u - tail)
        qy = y + math.sin(ang) * sp * max(0, u - tail) + 700 * max(0, u - tail) ** 2
        ctx.set_line_width(3.2 * (1 - u))
        setc(ctx, "#FFD27A", (1 - u / 0.9))
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
    ellipse(ctx, x - 40 * s, y - 150 * s, 60 * s, 16 * s)
    ellipse(ctx, x + 60 * s, y - 152 * s, 60 * s, 15 * s)
    ctx.fill()


def _shot_a(ctx, t):
    fire_k = smooth(prog(t, IGNITE, IGNITE + 1.8))
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
    # 远处围火的人（火着起来之后被照亮）
    if fire_k > 0:
        glow(ctx, 960, 860, 900, "#FF8A2A", 0.35 * warm)
        for (x, y, h, fl) in ((560, 760, 150, False), (1380, 770, 160, True), (1600, 740, 120, True)):
            film.human(ctx, x, y, h, "sit", t, "#140C08", fire_k, flip=fl, rim="#FF9A4A", rim_a=0.8 * fire_k)
    # 草团（火绒）与火
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
    # 第一视角的手（火着以后慢慢放下）
    down = ease_in(prog(t, IGNITE + 0.4, IGNITE + 1.6)) * 520
    bob = math.sin(t * 1.5) * 6
    left_tip = (820, 830 + down + bob)
    rest, wind, hit = (1210, 760), (1330, 560), (900, 800)
    times = KNAPS + FLINTS
    rt = _strike_pose(t, times, rest, wind, hit)
    right_tip = (rt[0], rt[1] + down + bob)
    tint = mix("#7A9CFF", "#FFB070", fire_k)
    with lit(tint, 0.55, 0.55 + 0.45 * max(fire_k, smold * 0.4)):
        film.pov_arm(ctx, (260, 1320), left_tip, 150)
        film.pov_arm(ctx, (1660, 1320), right_tip, 150)
        with at(ctx, left_tip[0] + 30, left_tip[1] - 60, 1.7, 0.2):
            draw_prop(ctx, ("stone",), t)
        with at(ctx, right_tip[0] - 20, right_tip[1] - 50, 1.25, -0.4):
            draw_prop(ctx, ("stone",), t)
    for k, ts in enumerate(KNAPS):
        _flakes(ctx, t, ts, 880, 790, 10 + k)
        glow(ctx, 880, 790, 120, "#BFD6FF", 0.5 * max(0, 1 - (t - ts) / 0.25) if t >= ts else 0)
    for k, ts in enumerate(FLINTS):
        _sparks(ctx, t, ts, 880, 780, 30 + k, 24, 1.0 + 0.2 * k)
    # 最后一颗火星落进草团
    u = prog(t, FLINTS[-1], IGNITE)
    if 0 < u < 1:
        px, py = lerp(880, nx, u), lerp(780, ny - 10, ease_in(u)) - math.sin(u * math.pi) * 60
        glow(ctx, px, py, 30, "#FFC46B", 0.9)
    film.vignette(ctx, 0.65)


# ================================================================ 镜头 B：山洞

C = (claude(1340, 868, 0.48, "wonder", seed=3.0)
     .sit(13.5, 1.0, 0.01)
     .look(13.6, -0.8, -0.1)
     .expr(16.8, "moved").look(17.0, -0.5, -0.3)
     .expr(20.0, "awe").look(20.2, -0.9, -0.6))

CAVE_CAM = Cam([(13.5, (930, 600, 1.02)), (19.2, (900, 590, 1.1), ease_io), (22.0, (560, 430, 1.75), ease_io),
                (24.5, (540, 420, 1.85))], drift=5, seed=7.0)


def _cave_wall(ctx, t, warm):
    # 洞壁：大块岩石 + 纹理 + 火光
    ctx.set_source(lin(0, 0, 0, H, [(0, "#1B120D"), (1, "#0B0705")]))
    ctx.rectangle(-600, -400, W + 1200, H + 800)
    ctx.fill()
    film.paint_texture(ctx, "stone", -600, -400, W + 1200, H + 800, 0.35, scale=0.8)
    # 洞口（右侧的夜空）
    ctx.save()
    ctx.move_to(1500, 980)
    ctx.curve_to(1480, 640, 1580, 380, 1760, 330)
    ctx.curve_to(1920, 300, 2100, 360, 2200, 420)
    ctx.line_to(2200, 980)
    ctx.close_path()
    ctx.clip()
    ctx.set_source(lin(0, 300, 0, 980, [(0, "#0C1730"), (1, "#22304A")]))
    ctx.paint()
    film.star_field(ctx, t, 60, 9, area=(1500, 300, 700, 500), a=0.8)
    film.moon(ctx, 1840, 470, 26, 0.35, 0.9, glow_a=0.2)
    ctx.restore()
    # 火光照在洞壁上
    glow(ctx, 900, 760, 1300, "#FF7A2A", 0.42 * warm)
    glow(ctx, 900, 760, 600, "#FFB24A", 0.25 * warm)


def _hand_stencil(ctx, x, y, w, rot, a, seed, warm):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    hw = w * 0.82
    hh = w * 1.18
    R = rng(seed)
    ctx.set_source(rad(0, 0, 0, w * 0.95, [(0, "#A63A22", 0.7 * a), (0.65, "#A63A22", 0.45 * a), (1, "#A63A22", 0)]))
    ellipse(ctx, 0, 0, w * 0.8, w * 0.95)
    ctx.fill()
    for i in range(6):        # 喷吹不均匀的颜料
        gx, gy = R.uniform(-0.5, 0.5) * hw, R.uniform(-0.5, 0.5) * hh
        ctx.set_source(rad(gx, gy, 0, w * 0.35, [(0, "#C2502E", 0.3 * a), (1, "#C2502E", 0)]))
        circle(ctx, gx, gy, w * 0.35)
        ctx.fill()
    starmap.hand_outline(ctx, -hw * 0.5 - 0.02 * w, -hh * 0.5, w)
    setc(ctx, mix("#5A4334", "#9A7458", warm), a * 0.95)
    ctx.fill()
    ctx.restore()


def _shot_b(ctx, t):
    warm = film.flicker(t, 5.0, 0.18)
    cam = CAVE_CAM.at(t)
    with view(ctx, cam, 1.0):
        _cave_wall(ctx, t, warm)
        # 手印（左上方洞壁）
        for (x, y, w, r, sd) in ((380, 300, 150, -0.25, 1), (560, 360, 130, 0.15, 2), (470, 470, 120, -0.05, 3),
                                 (700, 280, 110, 0.35, 4), (260, 450, 100, -0.4, 5)):
            _hand_stencil(ctx, x, y, w, r, 0.85, sd, warm)
        # 洞壁上的人影（被火光放大、晃动）
        for (x, h, pose, fl, ph) in ((600, 330, "sit", False, 0), (1200, 340, "sit", True, 1), (960, 420, "stand", False, 2)):
            sx = 900 + (x - 900) * 1.35
            sk = 1 + 0.05 * math.sin(t * 6 + ph) + 0.03 * math.sin(t * 13 + ph)
            film.human(ctx, sx, 700, h * sk, pose, t, "#0A0604", 0.3, flip=fl, hat="hair" if pose == "stand" else None,
                       arms=((1.2 + 0.6 * math.sin(t * 2.2), 2.0 + 0.7 * math.sin(t * 1.7 + 1)) if pose == "stand" else None))
        # 地面（向里延伸，人能站在火后面）
        ctx.set_source(lin(0, 660, 0, 1100, [(0, "#22150D"), (0.4, "#2A1A10"), (1, "#0E0805")]))
        ctx.move_to(-600, 1300)
        ctx.line_to(-600, 760)
        ctx.curve_to(300, 690, 1300, 680, 2400, 740)
        ctx.line_to(2400, 1300)
        ctx.close_path()
        ctx.fill()
        glow(ctx, 900, 860, 700, "#FF8A3A", 0.3 * warm)
        film.logs(ctx, 900, 865, 120)
        film.fire(ctx, 900, 862, 200, t, 1.0, seed=4.0)
        film.embers(ctx, t, 900, 780, 30, 13, spread=140, height=600, a=0.9)
        # 围火的人
        film.human(ctx, 640, 880, 230, "sit", t, "#120A06", 1.0, rim="#FF9A4A", rim_dx=3, rim_a=0.9)
        film.human(ctx, 1160, 885, 240, "sit", t, "#120A06", 1.0, flip=True, rim="#FF9A4A", rim_dx=3, rim_a=0.9)
        film.human(ctx, 990, 790, 250, "stand", t, "#100804", 1.0, rim="#FFB060", rim_dx=-3, rim_a=0.7,
                   arms=(1.2 + 0.6 * math.sin(t * 2.2), 2.0 + 0.7 * math.sin(t * 1.7 + 1)), hat="hair")
        with lit("#FF9A50", 0.6, 0.75 + 0.25 * warm):
            C.draw(ctx, t)
    film.vignette(ctx, 0.7)


# ================================================================ 镜头 C：月相与刻痕骨


def _shot_c1(ctx, t):
    u = t - 24.5
    film.sky(ctx, [(0, "#03050C"), (0.6, "#0B1428"), (1, "#18243C")])
    # 银河
    ctx.save()
    ctx.translate(960, 500)
    ctx.rotate(-0.35)
    ctx.set_source(lin(0, -160, 0, 160, [(0, "#8FA6FF", 0), (0.5, "#B8C4FF", 0.16), (1, "#8FA6FF", 0)]))
    ctx.rectangle(-1400, -160, 2800, 320)
    ctx.fill()
    film.star_field(ctx, t, 260, 61, area=(-1300, -140, 2600, 280), a=0.7, size=(0.6, 1.8))
    ctx.restore()
    film.star_field(ctx, t, 200, 62, area=(0, 90, W, 700), a=0.8)
    # 一排月相（从左到右逐个出现）
    n = 9
    for i in range(n):
        ph = i / (n - 1)
        ang = math.pi + (i / (n - 1)) * math.pi
        x = 960 + math.cos(ang) * 720
        y = 640 + math.sin(ang) * 380
        k = smooth(prog(u, 0.3 + i * 0.32, 0.8 + i * 0.32))
        film.moon(ctx, x, y, 34, max(0.001, ph if ph < 1 else 0.999), k, dark_a=0.35, glow_a=0.3)
        if i in (0, 2, 4, 6, 8):
            nm = {0: "新月", 2: "上弦", 4: "满月", 6: "下弦", 8: "新月"}[i]
            label(ctx, nm, x, y + 66, 24, "#E8DDC8", k * 0.9, "serif_r")
    # 悬崖与坐着的人、Claude
    film.ridge(ctx, -50, 1100, 900, 120, 0.003, 8.0, "#05070C", 1.0, step=14)
    ctx.set_source(lin(0, 820, 0, 1000, [(0, "#06080E"), (1, "#020305")]))
    ctx.move_to(-50, 1100)
    ctx.line_to(-50, 830)
    ctx.curve_to(400, 800, 760, 812, 1020, 845)
    ctx.line_to(1060, 1100)
    ctx.close_path()
    ctx.fill()
    film.human(ctx, 520, 820, 170, "sit", t, "#030406", 1.0, rim="#8FA6FF", rim_dx=2, rim_dy=-2, rim_a=0.5,
               arms=(0.4, 2.3), lean=-0.15, hat="hair")
    with lit("#7A9CFF", 0.55, 0.55):
        Cc.draw(ctx, t)
    film.vignette(ctx, 0.55)


Cc = (claude(720, 826, 0.4, "wonder", seed=5.0).sit(24.0, 1.0, 0.01).look(24.5, 0.3, -1.0)
      .look(26.5, 0.8, -0.9).look(28.0, 0.2, -1.0))


def _shot_c2(ctx, t):
    """第一视角特写：在骨头上一道道刻下记号，每一道对应一个月相。"""
    u = t - 29.0
    warm = film.flicker(t, 6.0, 0.1)
    ctx.set_source(rad(960, 620, 0, 1100, [(0, "#3A2414"), (0.6, "#1A0F08"), (1, "#070402")]))
    ctx.paint()
    glow(ctx, 1700, 900, 900, "#FF8A3A", 0.25 * warm)
    # 骨头
    bx0, bx1, by = 330, 1590, 640
    ctx.save()
    ctx.translate(0, math.sin(t * 0.9) * 4)
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
    nk = int(clamp(u / 4.2) * nmax + 0.0001) if u > 0.3 else 0
    nk = min(nmax, int(max(0.0, u - 0.3) / 0.14))
    for i in range(nk):
        x = bx0 + 60 + i * (bx1 - bx0 - 120) / (nmax - 1)
        ctx.set_line_width(5)
        setc(ctx, "#4A3420", 0.9)
        ctx.move_to(x - 3, by - 34)
        ctx.line_to(x + 3, by + 30)
        ctx.stroke()
        ph = (i + 1) / 29.5
        film.moon(ctx, x, by - 110 - (i % 2) * 34, 13, ph, 0.9, dark_a=0.25, glow_a=0.15, craters=False)
    ctx.restore()
    # 计数
    label(ctx, f"{nk}", 960, 300, 96, "#FFE8C0", smooth(prog(u, 0.3, 0.8)), "serif_k")
    label(ctx, "道刻痕", 960, 380, 30, "#D9C49A", smooth(prog(u, 0.3, 0.8)), "serif_r")
    if nk >= 29:
        label(ctx, "≈ 一个月相周期（29.5 天）", 960, 860, 34, "#F2D79B", smooth(prog(u, 4.6, 5.0)), "serif_sb")
    # 第一视角：手握燧石刀在刻
    i = min(nk, nmax - 1)
    tx = bx0 + 60 + i * (bx1 - bx0 - 120) / (nmax - 1) + 20
    cut = math.sin(t * TAU * 7) * 10
    with lit("#FF9A50", 0.45, 0.8 + 0.2 * warm):
        film.pov_arm(ctx, (1500, 1350), (tx + 120, 760 + cut), 140)
        with at(ctx, tx + 40, 700 + cut, 0.9, -0.6):
            draw_prop(ctx, ("stone",), t)
        film.pov_arm(ctx, (180, 1350), (bx0 + 120, by + 120), 150)
    film.vignette(ctx, 0.6)


# ================================================================ 镜头 D：麦田、巨石阵


def _wheat(ctx, t, x0, x1, y_base, h, n, seed, color, head, wind=1.0, dark=0.0):
    R = rng(seed)
    for i in range(n):
        x = R.uniform(x0, x1)
        hh = h * R.uniform(0.75, 1.15)
        sway = (fbm(t * 0.6 + x * 0.004, seed) * 18 + math.sin(t * 2.0 + x * 0.02) * 6) * wind
        tx, ty = x + sway, y_base - hh
        ctx.set_line_width(2.4)
        setc(ctx, mix(color, "#000000", dark))
        ctx.move_to(x, y_base + 20)
        ctx.curve_to(x, y_base - hh * 0.4, tx - sway * 0.3, ty + hh * 0.3, tx, ty)
        ctx.stroke()
        ctx.save()
        ctx.translate(tx, ty)
        ctx.rotate(sway * 0.01 + 0.2)
        ellipse(ctx, 0, -10, 6, 22)
        setc(ctx, mix(head, "#000000", dark))
        ctx.fill()
        ctx.restore()


W1 = (claude(400, 905, 0.55, "smile", seed=6.0).look(34.5, 0.6, -0.2)
      .walk_to(34.6, 39.6, 1060, 905, stride=0.8).expr(37.2, "curious").look(37.4, 0.5, -0.7))


def _shot_d1(ctx, t):
    u = t - 34.5
    camx = 120 * ease_io(prog(u, 0, 5.5))
    film.sky(ctx, [(0, "#3B4A73"), (0.45, "#E39A62"), (0.62, "#F6C27A"), (1, "#7A4A2A")])
    film.sun(ctx, 360 - camx * 0.1, 560, 44, 1.0, "#FFE7B8", "#FFB766", 600)
    film.beams(ctx, 360 - camx * 0.1, 560, 0.1, 1.3, 1400, 9, "#FFE2A8", 0.08, t, 4)
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
    _wheat(ctx, t, -200, W + 400, 760, 60, 240, 3, "#C8913E", "#E6B65A", 0.6, 0.15)
    for (x, pose, fl) in ((1380, "crouch", True), (1600, "crouch", False), (1230, "stand", True)):
        film.human(ctx, x, 800, 150, pose, t, "#3A2412", 1.0, flip=fl, rim="#FFD08A", rim_dx=-2, rim_a=0.8,
                   arms=((1.6 + 0.5 * math.sin(t * 3 + x), 1.2) if pose == "crouch" else None))
    _wheat(ctx, t, -200, W + 400, 840, 80, 200, 4, "#B9802F", "#E2AE4F", 0.8, 0.05)
    ctx.restore()
    ctx.save()
    ctx.translate(-camx, 0)
    with lit("#FFC890", 0.35, 1.0):
        W1.draw(ctx, t)
    _wheat(ctx, t, -200, W + 400, 975, 120, 160, 5, "#9C6828", "#D99E45", 1.0, 0.0)
    ctx.restore()
    film.grade(ctx, "#FFB070", 0.25)
    film.vignette(ctx, 0.5)


S1 = claude(960, 930, 0.42, "gaze", seed=7.0)


def _megalith(ctx, x, y, w, h, color, rim, rim_a, seed, lintel=True):
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
    if lintel:
        rrect(ctx, x - 6, y - h - h * 0.17, w + 12, h * 0.18, 6)
        setc(ctx, color)
        ctx.fill()
        ctx.set_line_width(3)
        setc(ctx, rim, rim_a * 0.8)
        ctx.move_to(x - 4, y - h - h * 0.17)
        ctx.line_to(x + w + 8, y - h - h * 0.17)
        ctx.stroke()


def _shot_d2(ctx, t):
    u = t - 40.0
    rise = ease_out(prog(u, 0.0, 4.5))
    push = 1 + 0.1 * ease_in(prog(u, 3.0, 8.0))
    ctx.save()
    ctx.translate(960, 600)
    ctx.scale(push, push)
    ctx.translate(-960, -600)
    film.sky(ctx, [(0, "#2A3150"), (0.4, "#9A6A6A"), (0.6, "#F0A86A"), (0.68, "#FFD49A"), (1, "#3A2418")])
    sx, sy = 960, lerp(720, 560, rise)
    film.sun(ctx, sx, sy, 32, 1.0, "#FFF0C8", "#FFB766", 700)
    film.beams(ctx, sx, sy, math.pi / 2, 0.5, 900, 7, "#FFE6B0", 0.18 * rise, t, 8, 0.03)
    film.ridge(ctx, -50, W + 50, 700, 40, 0.002, 21.0, "#4A3030", 1.0, step=20)
    ctx.set_source(lin(0, 690, 0, H, [(0, "#3A2A22"), (1, "#120C08")]))
    ctx.rectangle(-50, 700, W + 100, 500)
    ctx.fill()
    # 地面上的光带（从巨石缝里射过来）
    ctx.move_to(sx - 30, 705)
    ctx.line_to(sx + 30, 705)
    ctx.line_to(sx + 420, H + 50)
    ctx.line_to(sx - 420, H + 50)
    ctx.close_path()
    ctx.set_source(lin(0, 705, 0, H, [(0, "#FFD89A", 0.75 * rise), (1, "#FFB060", 0.15 * rise)]))
    ctx.fill()
    # 巨石（两侧排开，中间留缝）
    rim_a = 0.4 + 0.6 * rise
    stones = [(-120, 900, 300, 420, 1), (250, 840, 250, 330, 2), (560, 790, 220, 250, 3),
              (1140, 790, 220, 250, 4), (1420, 840, 250, 330, 5), (1740, 900, 300, 420, 6)]
    for (x, y, w, h, sd) in stones:
        _megalith(ctx, x, y, w, h, "#120C0A", "#FFC27A", rim_a, sd)
    _megalith(ctx, 805, 745, 310, 200, "#140E0B", "#FFD49A", rim_a, 9)
    glow(ctx, 960, 830, 200, "#FFD49A", 0.3 * rise)
    with lit("#3A2010", 0.7, 0.35 + 0.2 * rise):        # 逆光：背影几乎是剪影
        S1.draw(ctx, t, spin=math.pi)
    ctx.restore()
    film.grade(ctx, "#FF9A50", 0.2)
    film.vignette(ctx, 0.55)
    # 最后推向太阳（与下一章的强光转场衔接）
    if u > 6.6:
        glow(ctx, 960, 560, 900, "#FFE6B8", 0.6 * ease_in(prog(u, 6.6, 8.0)))


# ================================================================ 主绘制


def draw(ctx, t):
    if t < 13.5:
        _shot_a(ctx, t)
    elif t < 24.5:
        _shot_b(ctx, t)
    elif t < 29.0:
        _shot_c1(ctx, t)
    elif t < 34.5:
        _shot_c2(ctx, t)
    elif t < 40.0:
        _shot_d1(ctx, t)
    else:
        _shot_d2(ctx, t)


def sfx():
    out = [
        (0.0, "ambience_wind", {"dur": 13.5, "gain": 0.45}),
        (0.0, "ambience_night", {"dur": 13.5, "gain": 0.3}),
    ]
    for k, ts in enumerate(KNAPS):
        out.append((ts - 0.01, "knap", {"gain": 0.55, "pitch": 1 + 0.06 * (k % 3)}))
    for k, ts in enumerate(FLINTS):
        out.append((ts - 0.01, "flint", {"gain": 0.55}))
    out += [
        (IGNITE - 0.1, "ignite", {"gain": 0.6}),
        (IGNITE + 0.2, "ambience_fire", {"dur": 3.2, "gain": 0.6}),
        (13.5, "ambience_fire", {"dur": 11.0, "gain": 0.75}),
        (13.5, "ambience_cave", {"dur": 11.0, "gain": 0.4}),
        (19.4, "whoosh", {"dur": 2.4, "gain": 0.16}),
        (20.4, "boom", {"gain": 0.3}),
        (24.5, "ambience_night", {"dur": 10.0, "gain": 0.45}),
        (24.5, "ambience_wind", {"dur": 10.0, "gain": 0.25}),
    ]
    for i in range(9):
        out.append((24.8 + i * 0.32, "sparkle", {"dur": 0.4, "gain": 0.06}))
    for i in range(0, 29, 2):
        out.append((29.3 + i * 0.14, "carve", {"dur": 0.24, "gain": 0.35}))
    out += [
        (34.5, "ambience_birds", {"dur": 5.6, "gain": 0.45}),
        (34.5, "ambience_wind", {"dur": 5.6, "gain": 0.3}),
        (40.0, "ambience_wind", {"dur": 8.5, "gain": 0.35}),
        (40.0, "hush", {"dur": 4.0, "gain": 0.3}),
        (43.4, "swell", {"dur": 2.5, "gain": 0.3}),
        (45.9, "riser", {"dur": 2.2, "gain": 0.25}),
    ]
    return out
