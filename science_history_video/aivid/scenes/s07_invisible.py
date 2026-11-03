"""第七章 看不见的世界：X 射线与放射性；相对论与 1919 年日食；量子力学与索尔维会议；
膨胀的宇宙；1945 年；DNA 双螺旋；登月（第一视角看地球升起）。关键词：协作。"""
import math

from ..core import (TAU, H, W, Cam, arrow, arrow_head, at, circle, clamp, dashed, ease_in, ease_io, ease_out,
                    ellipse, glow, kf, lerp, lin, mix, poly, polyline_partial, prog, rad, rng, rrect, setc, smooth,
                    star4, stroke_pts, text, view)
from .. import film, starmap
from .common import claude, fade_io, label, lit

DUR = 52.0
CHAPTER = dict(num="第 七 章", title="看不见的世界", era="1895 — 1969 年", key="协作", at=0.8, dur=4.2)
GRAIN = 0.08

VO = [
    (4.8, "伦琴发现 {X 射线}：人第一次看见自己的骨骼。"),
    (8.0, "居里夫人研究放射性，两获{诺贝尔奖}。"),
    (11.4, "1905 年，26 岁的爱因斯坦写下 {E=mc²}。"),
    (14.8, "广义相对论：质量让{时空弯曲}。"),
    (17.6, "1919 年日全食：星光经过太阳，真的{拐了弯}。"),
    (21.2, "看得越深，世界越不像我们想的样子。"),
    (24.2, "原子世界只讲{概率}：量子力学诞生。"),
    (27.3, "1927 年索尔维会议：29 人中有 {17 位}诺奖得主。"),
    (30.8, "1929 年，哈勃发现：宇宙在{膨胀}。"),
    (34.2, "1945 年，原子之力被释放——人类开始思考如何{驾驭}科学的力量。"),
    (38.9, "1953 年，DNA 双螺旋被揭开：生命的密码，只用 {4 个字母}书写。"),
    (43.2, "1969 年，人类登上月球——阿波罗计划动员了约 {40 万人}。"),
    (47.6, "科学，成了千万人的{协作}。"),
    (50.0, "登月飞船上的计算机，内存只有约 {4KB}。", {"spill": 0.7}),
]

SUPERS = [
    (4.9, 7.6, "1895 年", "维尔茨堡 · 伦琴"),
    (17.7, 21.0, "1919 年 5 月 29 日", "日全食观测"),
    (27.4, 30.4, "1927 年", "布鲁塞尔 · 第五届索尔维会议"),
    (38.9, 42.6, "1953 年", "剑桥 · DNA 双螺旋结构"),
    (43.3, 46.8, "1969 年 7 月 20 日", "阿波罗 11 号"),
]

# ================================================================ A1：X 射线

BONES = [[(0.30, 0.98), (0.21, 0.82), (0.13, 0.70), (0.07, 0.60)],
         [(0.36, 0.95), (0.31, 0.62), (0.28, 0.43), (0.26, 0.29), (0.245, 0.18)],
         [(0.43, 0.95), (0.42, 0.58), (0.415, 0.37), (0.415, 0.21), (0.425, 0.08)],
         [(0.50, 0.95), (0.53, 0.60), (0.55, 0.41), (0.575, 0.25), (0.59, 0.13)],
         [(0.56, 0.97), (0.63, 0.66), (0.67, 0.49), (0.715, 0.37), (0.755, 0.28)]]


def _xray_hand(ctx, x, y, w, a):
    k = w / (0.82 * starmap.S)
    starmap.hand_outline(ctx, x, y, w)
    setc(ctx, "#9FE0C8", 0.22 * a)
    ctx.fill()
    for chain in BONES:
        pts = [(x + px * starmap.S * k, y + py * starmap.S * k) for px, py in chain]
        for p, q in zip(pts, pts[1:]):
            mx, my = lerp(p[0], q[0], 0.08), lerp(p[1], q[1], 0.08)
            nx, ny = lerp(p[0], q[0], 0.92), lerp(p[1], q[1], 0.92)
            ctx.set_line_width(w * 0.045)
            ctx.set_line_cap(1)
            setc(ctx, "#E8FFF4", 0.85 * a)
            ctx.move_to(mx, my)
            ctx.line_to(nx, ny)
            ctx.stroke()
    for i in range(8):
        circle(ctx, x + (0.36 + (i % 4) * 0.06) * starmap.S * k, y + (1.0 + (i // 4) * 0.06) * starmap.S * k, w * 0.028)
        setc(ctx, "#E8FFF4", 0.8 * a)
        ctx.fill()
    rx, ry = x + 0.545 * starmap.S * k, y + 0.5 * starmap.S * k
    rrect(ctx, rx - w * 0.04, ry - w * 0.02, w * 0.08, w * 0.04, w * 0.01)
    setc(ctx, "#203028", 0.95 * a)
    ctx.fill()


def _shot_a1(ctx, t):
    u = t
    ctx.set_source(rad(960, 540, 0, 1300, [(0, "#101A18"), (1, "#020404")]))
    ctx.paint()
    # 克鲁克斯管
    tk = film.flicker(t, 6.0, 0.25, 14)
    glow(ctx, 380, 420, 360, "#7FFFC8", 0.35 * tk)
    ellipse(ctx, 380, 420, 160, 90)
    setc(ctx, "#AFFFE0", 0.25 * tk)
    ctx.fill()
    ctx.set_line_width(3)
    setc(ctx, "#DFFFF0", 0.6)
    ellipse(ctx, 380, 420, 160, 90)
    ctx.stroke()
    rrect(ctx, 180, 410, 60, 20, 6)
    rrect(ctx, 520, 410, 60, 20, 6)
    setc(ctx, "#8A8A8A")
    ctx.fill()
    # 荧光屏上的手骨
    sk = smooth(prog(u, 0.8, 2.6))
    rrect(ctx, 900, 150, 720, 780, 16)
    setc(ctx, "#0C1412")
    ctx.fill()
    glow(ctx, 1260, 540, 500, "#5FE0A8", 0.18 * sk * tk)
    _xray_hand(ctx, 990, 190, 540, sk * (0.85 + 0.15 * tk))
    label(ctx, "1895 年 12 月 · 伦琴夫人的手", 1260, 890, 26, "#BFF0D8", smooth(prog(u, 2.6, 3.2)), "serif_r")
    film.vignette(ctx, 0.55)


def _shot_a2(ctx, t):
    u = t - 7.6
    ctx.set_source(rad(900, 560, 0, 1300, [(0, "#14181C"), (1, "#030405")]))
    ctx.paint()
    ctx.set_source(lin(0, 760, 0, H, [(0, "#2A2420"), (1, "#0E0B09")]))
    ctx.rectangle(-50, 760, W + 100, 400)
    ctx.fill()
    for i in range(7):
        x = 440 + i * 150
        h = 120 + (i % 3) * 40
        g = 0.6 + 0.4 * math.sin(t * 2 + i)
        glow(ctx, x, 760 - h / 2, 110, "#7FD8FF", 0.35 * g)
        rrect(ctx, x - 24, 760 - h, 48, h, 10)
        setc(ctx, "#BFEAFF", 0.35)
        ctx.fill()
        rrect(ctx, x - 18, 760 - h * 0.5, 36, h * 0.5 - 6, 8)
        setc(ctx, "#8FE8FF", 0.75 * g)
        ctx.fill()
    film.human(ctx, 1500, 920, 340, "hold", t, "#08090A", 1.0, rim="#7FD8FF", rim_a=0.6, robe=True, hat="bun")
    for i, (yr, nm) in enumerate((("1903", "诺贝尔物理学奖"), ("1911", "诺贝尔化学奖"))):
        k = smooth(prog(u, 0.6 + i * 0.6, 1.1 + i * 0.6))
        cx, cy = 560 + i * 380, 300
        glow(ctx, cx, cy, 120, "#FFD27A", 0.35 * k)
        circle(ctx, cx, cy, 70)
        ctx.set_source(rad(cx - 20, cy - 20, 4, 74, [(0, "#FFF0B0", k), (1, "#B8862A", k)]))
        ctx.fill()
        text(ctx, yr, cx, cy, 36, "#5A3A0A", k, "latin_b")
        label(ctx, nm, cx, cy + 110, 28, "#FFE8C0", k, "serif_sb")
    film.vignette(ctx, 0.55)


# ================================================================ B1：E=mc² 与弯曲的时空


def _shot_b1(ctx, t):
    u = t - 11.0
    ctx.set_source(lin(0, 0, 0, H, [(0, "#0E1622"), (1, "#05080E")]))
    ctx.paint()
    # 黑板
    rrect(ctx, 80, 160, 640, 420, 12)
    setc(ctx, "#1E2A26")
    ctx.fill()
    film.paint_texture(ctx, "stone", 80, 160, 640, 420, 0.15)
    k = smooth(prog(u, 0.3, 1.4))
    ctx.save()
    ctx.rectangle(80, 160, 640 * k, 420)
    ctx.clip()
    text(ctx, "E = mc²", 400, 340, 120, "#F2F0E8", 0.95, "latin")
    ctx.restore()
    label(ctx, "质量与能量可以互相转化", 400, 480, 28, "#BFD0C8", smooth(prog(u, 1.4, 2.0)), "serif_r")
    # 时空网格被压弯
    wk = smooth(prog(u, 2.2, 3.4))
    cx, cy = 1320, 600
    depth = 230 * wk
    n = 15
    def proj(gx, gy):
        d = math.hypot(gx, gy)
        z = -depth * math.exp(-(d / 2.6) ** 2)
        sx = cx + gx * 62 + gy * 14
        sy = cy + gy * 26 - z * 0.9 + gx * 2
        return sx, sy
    for i in range(n):
        g = i - (n - 1) / 2
        rowpts = [proj(-7 + j * 0.25, g) for j in range(57)]
        colpts = [proj(g, -7 + j * 0.25) for j in range(57)]
        stroke_pts(ctx, rowpts, 2, "#6FA8FF", 0.55)
        stroke_pts(ctx, colpts, 2, "#6FA8FF", 0.55)
    sx, sy = proj(0, 0)
    glow(ctx, sx, sy - 50, 160, "#FFC46B", 0.6 * wk)
    circle(ctx, sx, sy - 50, 46 * (0.3 + 0.7 * wk))
    setc(ctx, "#FFE6A8", 0.4 + 0.6 * wk)
    ctx.fill()
    label(ctx, "质量让时空弯曲", 1320, 250, 36, "#DCE8FF", smooth(prog(u, 3.6, 4.2)), "serif_sb")
    film.vignette(ctx, 0.5)


def _shot_b2(ctx, t):
    u = t - 17.0
    ctx.set_source_rgb(0.01, 0.01, 0.02)
    ctx.paint()
    film.star_field(ctx, t, 160, 92, a=0.4)
    cx, cy = 960, 520
    # 日冕：柔和的光丝
    R = rng(44)
    for i in range(90):
        ang = R.uniform(0, TAU)
        L = R.uniform(140, 330) * (1.3 if abs(math.sin(ang)) < 0.4 else 1.0)
        w = R.uniform(0.01, 0.04)
        ctx.move_to(cx + math.cos(ang - w) * 90, cy + math.sin(ang - w) * 90)
        ctx.line_to(cx + math.cos(ang) * L, cy + math.sin(ang) * L)
        ctx.line_to(cx + math.cos(ang + w) * 90, cy + math.sin(ang + w) * 90)
        ctx.close_path()
        ctx.set_source(rad(cx, cy, 90, L, [(0, "#FFFFFF", 0.35), (1, "#DCE6FF", 0)]))
        ctx.fill()
    glow(ctx, cx, cy, 260, "#E8F0FF", 0.55)
    circle(ctx, cx, cy, 96)
    setc(ctx, "#000000")
    ctx.fill()
    # 星星：真实位置（空心） → 看到的位置（被推开）
    k = smooth(prog(u, 1.2, 2.4))
    for i, (ang, d) in enumerate(((0.3, 190), (1.4, 220), (2.5, 180), (3.6, 240), (4.6, 200), (5.6, 230))):
        x0, y0 = cx + math.cos(ang) * d, cy + math.sin(ang) * d
        x1, y1 = cx + math.cos(ang) * (d + 60 * k), cy + math.sin(ang) * (d + 60 * k)
        ctx.set_line_width(2)
        setc(ctx, "#FFFFFF", 0.6)
        circle(ctx, x0, y0, 9)
        ctx.stroke()
        star4(ctx, x1, y1, 16, "#FFFFFF", 0.95)
        if k > 0.1:
            arrow(ctx, x0 + math.cos(ang) * 12, y0 + math.sin(ang) * 12, x1 - math.cos(ang) * 12, y1 - math.sin(ang) * 12,
                  3, "#FFD27A", k)
    label(ctx, "空心圈：星星的真实位置 · 亮星：我们看到的位置", 960, 880, 30, "#E8E8F2", smooth(prog(u, 2.0, 2.6)), "serif_sb")
    label(ctx, "偏折约 1.75 角秒 · 与广义相对论预言相符", 960, 930, 26, "#CDBA92", smooth(prog(u, 2.6, 3.2)), "serif_r")
    # 第 21.2 秒：越看越深
    if u > 4.0:
        film.fade_black(ctx, 0.0)
    film.vignette(ctx, 0.5)


# ================================================================ C1：原子 → 概率云；索尔维会议


def _shot_c1(ctx, t):
    u = t - 24.0
    ctx.set_source(rad(960, 540, 0, 1300, [(0, "#121428"), (1, "#03030A")]))
    ctx.paint()
    if u < 3.0:
        cx, cy = 960, 520
        cloud = smooth(prog(u, 0.6, 2.2))
        glow(ctx, cx, cy, 40, "#FF9A5A", 0.9)
        circle(ctx, cx, cy, 16)
        setc(ctx, "#FFB07A")
        ctx.fill()
        for i, (rx, ry, rot) in enumerate(((260, 90, 0.3), (260, 90, 1.35), (260, 90, 2.4))):
            ctx.save()
            ctx.translate(cx, cy)
            ctx.rotate(rot)
            ctx.set_line_width(3)
            setc(ctx, "#7FB6FF", 0.7 * (1 - cloud))
            ellipse(ctx, 0, 0, rx, ry)
            ctx.stroke()
            ang = t * 2.5 + i * 2
            circle(ctx, math.cos(ang) * rx, math.sin(ang) * ry, 10)
            setc(ctx, "#BFE0FF", 1 - cloud)
            ctx.fill()
            ctx.restore()
        R = rng(int(t * 30))
        for i in range(int(900 * cloud)):
            r = abs(R.gauss(0, 140))
            a = R.uniform(0, TAU)
            setc(ctx, "#9FC8FF", 0.5)
            circle(ctx, cx + math.cos(a) * r, cy + math.sin(a) * r * 0.9, 2.2)
            ctx.fill()
        label(ctx, "电子不在确定的轨道上，只有出现的概率", 960, 860, 30, "#DCE8FF", smooth(prog(u, 1.6, 2.2)), "serif_sb")
    else:
        q = u - 3.0
        # 一张泛黄的合影：29 个人影，17 颗星
        ctx.set_source(rad(960, 540, 0, 1300, [(0, "#2A2218"), (1, "#0A0806")]))
        ctx.paint()
        rrect(ctx, 260, 170, 1400, 740, 10)
        setc(ctx, "#D8C49A")
        ctx.fill()
        film.paint_texture(ctx, "paper", 260, 170, 1400, 740, 0.5)
        rrect(ctx, 300, 210, 1320, 600, 6)
        ctx.set_source(lin(0, 210, 0, 810, [(0, "#9A8462"), (1, "#5A4A34")]))
        ctx.fill()
        rows = [(9, 520, 230), (9, 640, 250), (11, 780, 270)]
        idx = 0
        nobel = {0, 1, 2, 4, 5, 7, 9, 10, 11, 13, 14, 16, 18, 20, 23, 25, 27}
        for (n, y, h) in rows:
            for j in range(n):
                x = 960 + (j - (n - 1) / 2) * (1180 / n)
                film.human(ctx, x, y + 40, h, "stand", t, "#2A2016", 0.9, hat="hair")
                if idx in nobel:
                    k = smooth(prog(q, 0.4 + idx * 0.04, 0.7 + idx * 0.04))
                    star4(ctx, x, y + 40 - h - 18, 18 * k, "#FFD27A", k)
                    glow(ctx, x, y + 40 - h - 18, 36, "#FFD27A", 0.5 * k)
                idx += 1
        label(ctx, "29 人 · 其中 17 位诺贝尔奖得主", 960, 860, 34, "#3A2A1A", smooth(prog(q, 1.4, 2.0)), "serif_k",
              shadow=False)
    film.vignette(ctx, 0.5)


def _galaxy(ctx, x, y, r, rot, col, a):
    for arm in range(2):
        pts = []
        for i in range(40):
            f = i / 39
            ang = rot + arm * math.pi + f * 4.0
            pts.append((x + math.cos(ang) * r * f, y + math.sin(ang) * r * f * 0.5))
        stroke_pts(ctx, pts, r * 0.12, col, 0.35 * a)
    glow(ctx, x, y, r * 0.7, col, 0.6 * a)


def _shot_c2(ctx, t):
    u = t - 29.5
    ctx.set_source_rgb(0.01, 0.01, 0.025)
    ctx.paint()
    film.star_field(ctx, t, 200, 94, a=0.5)
    cx, cy = 960, 540
    R = rng(33)
    s = 1 + 0.45 * ease_out(prog(u, 0.3, 4.5))
    for i in range(16):
        ang = R.uniform(0, TAU)
        d = R.uniform(120, 520)
        x, y = cx + math.cos(ang) * d * s, cy + math.sin(ang) * d * s * 0.65
        red = clamp((d * (s - 1)) / 200)
        col = mix("#BFD8FF", "#FF8A6A", red)
        _galaxy(ctx, x, y, R.uniform(30, 60), R.uniform(0, TAU) + t * 0.1, col, 1.0)
        if u > 0.8:
            arrow(ctx, x + math.cos(ang) * 50, y + math.sin(ang) * 30, x + math.cos(ang) * 110, y + math.sin(ang) * 70,
                  3, col, 0.6 * smooth(prog(u, 0.8, 1.4)))
    label(ctx, "越远的星系，离开得越快 · 光被拉长、变红", 960, 900, 30, "#F2E6E0", smooth(prog(u, 1.4, 2.0)), "serif_sb")
    film.vignette(ctx, 0.5)


# ================================================================ D1：1945


C7 = claude(360, 905, 0.5, "solemn", seed=14.0).look(34.0, 0.8, -0.2)


def _shot_d1(ctx, t):
    u = t - 34.0
    flash = math.exp(-max(0, u - 0.6) * 2.2) if u > 0.6 else 0.0
    film.sky(ctx, [(0, "#2A2C30"), (0.65, "#6A6660"), (1, "#3A3632")])
    rise = ease_out(prog(u, 0.7, 4.5))
    hx, hy = 1250, 760
    # 蘑菇云剪影
    if rise > 0:
        sh = 420 * rise
        ctx.move_to(hx - 40, hy)
        ctx.curve_to(hx - 30, hy - sh * 0.5, hx - 50, hy - sh * 0.8, hx - 30, hy - sh)
        ctx.line_to(hx + 30, hy - sh)
        ctx.curve_to(hx + 50, hy - sh * 0.8, hx + 30, hy - sh * 0.5, hx + 40, hy)
        ctx.close_path()
        setc(ctx, "#4A4440")
        ctx.fill()
        for i in range(7):
            ang = i / 7 * TAU
            film.cloud(ctx, hx + math.cos(ang) * 90 * rise, hy - sh - 30 + math.sin(ang) * 40 * rise, 220 * rise,
                       120 * rise, "#5A544E", 0.9, i)
    film.ridge(ctx, -50, W + 50, 780, 40, 0.003, 5.0, "#2A2622", 1.0, step=16)
    ctx.rectangle(-50, 780, W + 100, 400)
    setc(ctx, "#1E1A18")
    ctx.fill()
    with lit(None, 0, 0.55, 0.9):
        C7.draw(ctx, t)
    if flash > 0:
        ctx.set_source_rgba(1, 0.98, 0.94, 0.9 * flash)
        ctx.paint()
    film.vignette(ctx, 0.6)


# ================================================================ D2：DNA 双螺旋

BASES = [("A", "T"), ("C", "G"), ("G", "C"), ("T", "A"), ("A", "T"), ("G", "C"), ("C", "G"), ("T", "A"),
         ("G", "C"), ("A", "T"), ("C", "G"), ("T", "A")]
BCOL = {"A": "#FF7A6A", "T": "#FFD27A", "C": "#7FD8A8", "G": "#7FB6FF"}


def _shot_d2(ctx, t):
    u = t - 38.5
    ctx.set_source(rad(960, 540, 0, 1300, [(0, "#121A2A"), (1, "#03050A")]))
    ctx.paint()
    # 51 号照片的 X 形衍射图（淡淡地在背后）
    pk = 0.35 * smooth(prog(u, 0.2, 1.2))
    for i in range(12):
        for sgn in (-1, 1):
            d = 60 + i * 34
            circle(ctx, 1480 + sgn * d * 0.55, 520 + d * 0.9 * (1 if i % 2 else -1), 12)
            setc(ctx, "#DDE6FF", pk * (1 - i / 14))
            ctx.fill()
    label(ctx, "51 号照片 · 罗莎琳德·富兰克林", 1480, 900, 26, "#BFC8E0", smooth(prog(u, 0.8, 1.4)), "serif_r")
    # 双螺旋（横躺，缓缓旋转）
    x0, x1, cy, amp = 160, 1180, 540, 170
    ph = t * 1.4
    n = len(BASES)
    pts1, pts2 = [], []
    for i in range(121):
        f = i / 120
        x = lerp(x0, x1, f)
        a = f * TAU * 2.2 + ph
        pts1.append((x, cy + math.sin(a) * amp, math.cos(a)))
        pts2.append((x, cy + math.sin(a + math.pi) * amp, math.cos(a + math.pi)))
    for i in range(n):
        f = (i + 0.5) / n
        x = lerp(x0, x1, f)
        a = f * TAU * 2.2 + ph
        y1, y2 = cy + math.sin(a) * amp, cy + math.sin(a + math.pi) * amp
        b1, b2 = BASES[i]
        k = smooth(prog(u, 0.3 + i * 0.08, 0.6 + i * 0.08))
        ctx.set_line_width(12)
        setc(ctx, BCOL[b1], 0.85 * k)
        ctx.move_to(x, y1)
        ctx.line_to(x, (y1 + y2) / 2)
        ctx.stroke()
        setc(ctx, BCOL[b2], 0.85 * k)
        ctx.move_to(x, (y1 + y2) / 2)
        ctx.line_to(x, y2)
        ctx.stroke()
        if abs(y1 - y2) > 120:
            text(ctx, b1, x + 18, lerp(y1, y2, 0.25), 26, "#FFFFFF", k, "latin_b")
            text(ctx, b2, x + 18, lerp(y1, y2, 0.75), 26, "#FFFFFF", k, "latin_b")
    for pts in (pts1, pts2):
        for p, q in zip(pts, pts[1:]):
            front = (p[2] + 1) / 2
            ctx.set_line_width(10 + 6 * front)
            setc(ctx, mix("#4A5A8A", "#DCE6FF", front), 0.95)
            ctx.move_to(p[0], p[1])
            ctx.line_to(q[0], q[1])
            ctx.stroke()
    label(ctx, "A — T  ·  C — G", 670, 840, 40, "#FFE8C0", smooth(prog(u, 1.4, 2.0)), "latin_b")
    film.vignette(ctx, 0.5)


# ================================================================ E1：发射 / E2：月面上看地球


def _shot_e1(ctx, t):
    u = t - 43.0
    shake = (math.sin(t * 50) * 4 + math.sin(t * 37) * 3) * smooth(prog(u, 0.3, 1.0))
    ctx.save()
    ctx.translate(shake, shake * 0.6)
    film.sky(ctx, [(0, "#1A2A4A"), (0.6, "#6A7A9A"), (1, "#C9A07A")])
    lift = 600 * ease_in(prog(u, 1.0, 4.2))
    # 发射塔
    ctx.rectangle(700, 300, 60, 700)
    setc(ctx, "#1A1A1E")
    ctx.fill()
    for i in range(14):
        ctx.move_to(700, 300 + i * 50)
        ctx.line_to(760, 350 + i * 50)
    ctx.set_line_width(4)
    ctx.stroke()
    # 火箭
    rx, ry = 900, 860 - lift
    rrect(ctx, rx - 34, ry - 520, 68, 520, 10)
    ctx.set_source(lin(rx - 34, 0, rx + 34, 0, [(0, "#9A9AA2"), (0.4, "#F4F4F0"), (1, "#7A7A82")]))
    ctx.fill()
    poly(ctx, [(rx - 34, ry - 520), (rx, ry - 610), (rx + 34, ry - 520)])
    setc(ctx, "#E8E8E4")
    ctx.fill()
    for yy in (ry - 300, ry - 160):
        ctx.rectangle(rx - 34, yy, 68, 14)
    setc(ctx, "#1A1A1E")
    ctx.fill()
    fk = smooth(prog(u, 0.2, 0.8))
    glow(ctx, rx, ry + 60, 300, "#FFB24A", 0.7 * fk)
    for i in range(5):
        h = (180 + 60 * math.sin(t * 20 + i)) * fk
        poly(ctx, [(rx - 30 + i * 15, ry), (rx - 22 + i * 15 + math.sin(t * 30 + i) * 6, ry + h), (rx - 14 + i * 15, ry)])
        setc(ctx, "#FFE2A0" if i % 2 else "#FF8A2A", 0.9 * fk)
        ctx.fill()
    film.smoke_puffs(ctx, t, 900, 1000, 26, 5, "#E8E0D8", 0.7 * fk, rise=-80, size=140, drift=600, speed=0.3)
    film.smoke_puffs(ctx, t, 900, 1000, 26, 6, "#D8D0C8", 0.6 * fk, rise=-60, size=150, drift=-600, speed=0.3)
    ctx.rectangle(-50, 980, W + 100, 200)
    setc(ctx, "#2A2420")
    ctx.fill()
    label(ctx, "约 40 万人参与", 1450, 380, 44, "#FFF2D8", smooth(prog(u, 1.8, 2.4)), "serif_k")
    label(ctx, "科学家 · 工程师 · 工人 · 程序员", 1450, 445, 26, "#E8DCC8", smooth(prog(u, 2.2, 2.8)), "serif_r")
    ctx.restore()
    film.vignette(ctx, 0.5)


def _earth(ctx, x, y, r, t, a=1.0):
    glow(ctx, x, y, r * 1.5, "#6FA8FF", 0.35 * a)
    circle(ctx, x, y, r)
    ctx.set_source(rad(x - r * 0.3, y - r * 0.3, 0, r * 1.1, [(0, "#7FC0FF", a), (0.6, "#2A6AC8", a), (1, "#0A2A6A", a)]))
    ctx.fill()
    ctx.save()
    circle(ctx, x, y, r)
    ctx.clip()
    R = rng(3)
    for i in range(7):
        ellipse(ctx, x + R.uniform(-0.6, 0.6) * r + t * 3, y + R.uniform(-0.6, 0.6) * r, R.uniform(0.15, 0.35) * r,
                R.uniform(0.1, 0.2) * r)
        setc(ctx, "#5A9A4A", 0.8 * a)
        ctx.fill()
    for i in range(10):
        ellipse(ctx, x + R.uniform(-0.8, 0.8) * r - t * 2, y + R.uniform(-0.8, 0.8) * r, R.uniform(0.15, 0.4) * r, 0.05 * r)
        setc(ctx, "#FFFFFF", 0.55 * a)
        ctx.fill()
    # 地球上的昼夜
    ctx.set_source(lin(x - r * 0.2, 0, x + r, 0, [(0, "#000000", 0), (1, "#000000", 0.85)]))
    ctx.rectangle(x - r, y - r, 2 * r, 2 * r)
    ctx.fill()
    ctx.restore()


def _shot_e2(ctx, t):
    u = t - 47.0
    ctx.set_source_rgb(0, 0, 0.01)
    ctx.paint()
    film.star_field(ctx, t, 80, 97, a=0.3)
    ey = lerp(760, 470, ease_out(prog(u, 0, 5.0)))
    _earth(ctx, 1150, ey, 150, t)
    # 月面地平线
    ctx.move_to(-50, H + 50)
    ctx.line_to(-50, 700)
    ctx.curve_to(600, 640, 1300, 650, W + 50, 720)
    ctx.line_to(W + 50, H + 50)
    ctx.close_path()
    ctx.set_source(lin(0, 650, 0, H, [(0, "#A8A49C"), (1, "#3A3834")]))
    ctx.fill()
    R = rng(8)
    for i in range(40):
        x, y = R.uniform(0, W), R.uniform(720, 1000)
        ellipse(ctx, x, y, R.uniform(10, 50), R.uniform(4, 14))
        setc(ctx, "#5A5650", 0.45)
        ctx.fill()
    # 脚印
    for i in range(6):
        x, y = 700 + i * 70, 900 - i * 30
        rrect(ctx, x, y, 34, 16, 6)
        setc(ctx, "#4A4640", 0.7)
        ctx.fill()
    # 第一视角：Claude 的手臂
    with lit("#C9D6FF", 0.25, 0.85):
        film.pov_arm(ctx, (260, 1320), (660, 850 + math.sin(t) * 8), 150)
        film.pov_arm(ctx, (1680, 1320), (1290, 840 + math.sin(t + 1) * 8), 150)
    film.vignette(ctx, 0.5)


# ================================================================ 主绘制


def draw(ctx, t):
    if t < 7.6:
        _shot_a1(ctx, t)
    elif t < 11.0:
        _shot_a2(ctx, t)
    elif t < 17.0:
        _shot_b1(ctx, t)
    elif t < 24.0:
        _shot_b2(ctx, t)
    elif t < 29.5:
        _shot_c1(ctx, t)
    elif t < 34.0:
        _shot_c2(ctx, t)
    elif t < 38.5:
        _shot_d1(ctx, t)
    elif t < 43.0:
        _shot_d2(ctx, t)
    elif t < 47.0:
        _shot_e1(ctx, t)
    else:
        _shot_e2(ctx, t)


def sfx():
    return [
        (0.0, "whine", {"dur": 7.6, "gain": 0.12}), (0.0, "ambience_room", {"dur": 7.6, "gain": 0.3}),
        (0.8, "shutter", {"gain": 0.35}),
        (7.0, "ambience_room", {"dur": 5.0, "gain": 0.35}), (10.6, "ambience_room", {"dur": 7.0, "gain": 0.35}),
        (7.6, "geiger", {"dur": 3.4, "rate": 9, "gain": 0.3}), (8.2, "ding", {"gain": 0.2}), (8.8, "ding", {"gain": 0.2, "pitch": 1.1}),
        (11.0, "chalk", {"dur": 1.4, "gain": 0.35}), (13.2, "rise", {"dur": 2.0, "gain": 0.2}),
        (17.0, "hush", {"dur": 3.5, "gain": 0.35}), (17.0, "ambience_space", {"dur": 7.0, "gain": 0.4}),
        (18.3, "shimmer", {"dur": 1.8, "gain": 0.2}),
        (23.6, "ambience_space", {"dur": 7.6, "gain": 0.35}), (24.6, "stream", {"dur": 2.0, "gain": 0.15}),
        (27.0, "shutter", {"gain": 0.3}),
        (29.5, "ambience_space", {"dur": 4.5, "gain": 0.45}), (29.8, "whoosh", {"dur": 3.0, "gain": 0.2}),
        (33.4, "ambience_wind", {"dur": 5.6, "gain": 0.3}), (34.6, "boom", {"gain": 0.75}), (35.2, "rumble", {"dur": 3.0, "gain": 0.4}),
        (38.0, "ambience_room", {"dur": 5.6, "gain": 0.35}), (38.8, "shimmer", {"dur": 2.0, "gain": 0.15}),
        (43.0, "rocket", {"dur": 4.6, "gain": 0.7}),
        (47.0, "ambience_space", {"dur": 5.0, "gain": 0.5}), (47.1, "hush", {"dur": 3.0, "gain": 0.3}),
        (49.4, "relays", {"dur": 2.5, "gain": 0.15}),
    ]
