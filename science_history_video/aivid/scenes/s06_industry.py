"""第六章 蒸汽与电：瓦特蒸汽机；科学中心的迁移（古地图）；法拉第电磁感应；麦克斯韦与赫兹；
门捷列夫的周期表与被预言的元素；城市电气化。关键词：预言。"""
import math

from ..core import (TAU, H, W, Cam, arrow, arrow_head, at, circle, clamp, dashed, ease_in, ease_io, ease_out,
                    ellipse, glow, kf, lerp, lin, mix, poly, polyline_partial, prog, rad, rng, rrect, setc, smooth,
                    star4, stroke_pts, text, view)
from .. import film, oldmap
from ..icons import gear_path
from .common import claude, fade_io, label, lit

DUR = 44.0
CHAPTER = dict(num="第 六 章", title="蒸汽与电", era="1769 — 1900 年", key="预言", at=0.9, dur=4.4)
GRAIN = 0.08

VO = [
    (5.2, "瓦特改良蒸汽机，{工业革命}轰鸣而来。"),
    (8.0, "为了更好的机器，人们研究热——{热力学}诞生。"),
    (11.4, "近代科学的中心，大约每 {80 年}转移一次："),
    (14.8, "意大利、英国、法国、德国，再到美国。"),
    (18.8, "1831 年，法拉第发现：磁铁一动，线圈里就生出{电流}。"),
    (23.8, "麦克斯韦用一组方程统一电、磁和光，预言了{电磁波}。"),
    (27.8, "20 多年后，赫兹{捉到了}它。"),
    (30.4, "门捷列夫排出周期表，给未知元素{留了空位}。"),
    (33.9, "镓、钪、锗陆续被找到，和预言几乎一样。"),
    (37.6, "理论开始{预言}还没看见的东西。"),
    (41.0, "电灯亮了，电报和电话把世界连在一起。", {"spill": 0.6}),
]

SUPERS = [
    (5.3, 9.6, "1769 年", "格拉斯哥 · 瓦特"),
    (18.9, 22.8, "1831 年", "伦敦 · 法拉第"),
    (30.5, 33.6, "1869 年", "圣彼得堡 · 门捷列夫"),
]

# ================================================================ A：蒸汽机

E6 = (claude(1500, 905, 0.46, "awe", seed=13.0, glasses="goggles").look(0.5, -0.8, -0.3)
      .expr(6.0, "excited").look(6.2, -0.6, -0.6))


def _shot_a(ctx, t):
    fl = film.flicker(t, 4.0, 0.15)
    ctx.set_source(rad(800, 600, 0, 1400, [(0, "#3A2414"), (0.6, "#160C06"), (1, "#060302")]))
    ctx.paint()
    film.shaft(ctx, 1300, 90, 900, 980, 220, 600, "#FFC890", 0.08)
    # 炉火
    glow(ctx, 360, 860, 520, "#FF6A1A", 0.45 * fl)
    rrect(ctx, 200, 700, 320, 240, 20)
    setc(ctx, "#1A100A")
    ctx.fill()
    rrect(ctx, 260, 790, 200, 110, 50)
    ctx.set_source(rad(360, 860, 0, 120, [(0, "#FFE2A0"), (0.5, "#FF7A2A"), (1, "#8A2A0A")]))
    ctx.fill()
    # 气缸、横梁、飞轮、离心调速器
    ang = t * 2.2
    rrect(ctx, 640, 420, 130, 420, 14)
    ctx.set_source(lin(640, 0, 770, 0, [(0, "#4A3A2E"), (0.4, "#8A7460"), (1, "#3A2E24")]))
    ctx.fill()
    piston_y = 470 + (1 - math.cos(ang)) * 70
    rrect(ctx, 695, 260, 20, piston_y - 260, 6)
    setc(ctx, "#B8A890")
    ctx.fill()
    beam_tilt = math.sin(ang) * 0.12
    ctx.save()
    ctx.translate(960, 250)
    ctx.rotate(beam_tilt)
    rrect(ctx, -300, -26, 600, 52, 10)
    setc(ctx, "#2A1C12")
    ctx.fill()
    ctx.restore()
    rrect(ctx, 945, 250, 30, 640, 6)
    setc(ctx, "#2A1C12")
    ctx.fill()
    fx_, fy_ = 1240, 640
    rod_end = (fx_ + math.cos(ang) * 150, fy_ + math.sin(ang) * 150)
    ctx.set_line_width(18)
    ctx.set_line_cap(1)
    setc(ctx, "#5A4636")
    ctx.move_to(1260, 250 + math.sin(ang) * 36)
    ctx.line_to(*rod_end)
    ctx.stroke()
    circle(ctx, fx_, fy_, 250)
    ctx.set_line_width(36)
    setc(ctx, "#3A2C20")
    ctx.stroke()
    for k in range(6):
        a2 = ang + k * TAU / 6
        ctx.set_line_width(16)
        ctx.move_to(fx_, fy_)
        ctx.line_to(fx_ + math.cos(a2) * 235, fy_ + math.sin(a2) * 235)
        ctx.stroke()
    circle(ctx, fx_, fy_, 34)
    setc(ctx, "#6A5440")
    ctx.fill()
    # 调速器：两个飞球
    gx, gy = 600, 300
    spin = t * 6
    open_ = 0.55 + 0.1 * math.sin(t * 0.8)
    ctx.set_line_width(5)
    setc(ctx, "#C9A060")
    ctx.move_to(gx, gy - 120)
    ctx.line_to(gx, gy + 60)
    ctx.stroke()
    for sg in (-1, 1):
        sx = math.cos(spin) * sg
        bx, by = gx + sx * 110 * open_, gy - 40 + 40 * (1 - open_)
        ctx.move_to(gx, gy - 100)
        ctx.line_to(bx, by)
        ctx.stroke()
        circle(ctx, bx, by, 22)
        ctx.set_source(rad(bx - 6, by - 6, 2, 24, [(0, "#FFE2A0"), (1, "#8A6A2A")]))
        ctx.fill()
    film.smoke_puffs(ctx, t, 700, 230, 10, 3, "#D8D0C4", 0.35, rise=260, size=60, drift=120, speed=0.35)
    film.smoke_puffs(ctx, t, 1500, 720, 6, 9, "#D8D0C4", 0.25, rise=200, size=50, drift=-80, speed=0.3)
    ctx.set_source(lin(0, 880, 0, H, [(0, "#2A1A0E"), (1, "#0A0604")]))
    ctx.rectangle(-50, 900, W + 100, 200)
    ctx.fill()
    with lit("#FF9A50", 0.45, 0.85):
        E6.draw(ctx, t)
    label(ctx, "离心调速器：让机器自己调节转速", 600, 470, 24, "#F2D79B", smooth(prog(t, 6.2, 6.8)), "serif_r")
    film.vignette(ctx, 0.6)


# ================================================================ B：科学中心的迁移

MCAM6 = oldmap.MapCam([(10.0, (12.0, 45.0, 26)), (11.6, (5.0, 48.0, 22), ease_io), (14.6, (4.0, 49.0, 20), ease_io),
                       (16.4, (-30.0, 44.0, 9.5), ease_io), (18.6, (-36.0, 44.0, 8.8))])


def _shot_b(ctx, t):
    cam = MCAM6.at(t)
    oldmap.draw_map(ctx, cam, t, 1.0, world=True, rivers=["danube", "rhine"])
    times = [10.4, 12.2, 13.4, 14.6, 16.4]
    prev = None
    for i, (nm, lon, lat, yrs) in enumerate(oldmap.CENTERS):
        k = smooth(prog(t, times[i], times[i] + 0.5))
        x, y = cam.xy(lon, lat)
        if prev is not None and k > 0:
            from ..charts import arc_pts
            pts = arc_pts(prev, (x, y), 0.25)
            stroke_pts(ctx, polyline_partial(pts, ease_io(prog(t, times[i] - 0.3, times[i] + 0.5))), 4, "#A8321E", 0.9,
                       dash=(14, 8), offset=-t * 40)
        if k > 0:
            cur = i == max(j for j in range(5) if t >= times[j])
            glow(ctx, x, y, 90 if cur else 50, "#FFC46B", (0.7 if cur else 0.35) * k)
            circle(ctx, x, y, 12)
            setc(ctx, "#A8321E", k)
            ctx.fill()
            sz = 40 if cam.k > 15 else 30
            label(ctx, nm, x, y - 50, sz, "#3A1A0A", k, "serif_k", shadow=False)
            label(ctx, yrs, x, y + 40, sz * 0.7, "#6A3A1A", k, "serif_sb", shadow=False)
        prev = (x, y)
    label(ctx, "近代科学中心的转移（汤浅光朝，1962）", 960, 880, 30, "#3A2414", smooth(prog(t, 10.6, 11.4)), "serif_sb",
          shadow=False)
    oldmap.map_vignette(ctx, 0.7)


# ================================================================ C1：法拉第


def _shot_c1(ctx, t):
    u = t - 18.5
    ctx.set_source(rad(960, 560, 0, 1300, [(0, "#2A2420"), (1, "#0A0806")]))
    ctx.paint()
    film.shaft(ctx, 1500, 90, 1100, 980, 160, 420, "#FFE0B0", 0.1)
    ctx.set_source(lin(0, 780, 0, H, [(0, "#4A3420"), (1, "#1A1008")]))
    ctx.rectangle(-50, 780, W + 100, 400)
    ctx.fill()
    # 线圈
    cx, cy = 820, 620
    for i in range(14):
        x = cx - 180 + i * 26
        ellipse(ctx, x, cy, 18, 120)
        ctx.set_line_width(9)
        setc(ctx, "#C9783A")
        ctx.stroke()
    # 磁铁进出
    mx = lerp(260, 640, 0.5 - 0.5 * math.cos(clamp(u - 0.6, 0, 99) * 2.4)) if u > 0.6 else 260
    v = math.sin(clamp(u - 0.6, 0, 99) * 2.4) if u > 0.6 else 0.0
    rrect(ctx, mx - 220, cy - 40, 200, 80, 8)
    setc(ctx, "#C83A2A")
    ctx.fill()
    rrect(ctx, mx - 20, cy - 40, 140, 80, 8)
    setc(ctx, "#3A5AC8")
    ctx.fill()
    text(ctx, "N", mx - 120, cy, 40, "#FFFFFF", 1, "latin_b")
    text(ctx, "S", mx + 50, cy, 40, "#FFFFFF", 1, "latin_b")
    # 导线与电流计
    ctx.set_line_width(6)
    setc(ctx, "#C9783A")
    ctx.move_to(cx + 180, cy + 100)
    ctx.curve_to(1100, 860, 1250, 860, 1360, 760)
    ctx.move_to(cx - 180, cy + 100)
    ctx.curve_to(700, 900, 1200, 940, 1420, 790)
    ctx.stroke()
    gx, gy = 1420, 620
    circle(ctx, gx, gy, 170)
    setc(ctx, "#E8DCC4")
    ctx.fill()
    ctx.set_line_width(10)
    setc(ctx, "#6A4A28")
    circle(ctx, gx, gy, 170)
    ctx.stroke()
    for k in range(-5, 6):
        a = -math.pi / 2 + k * 0.15
        ctx.set_line_width(3)
        setc(ctx, "#3A2A1A")
        ctx.move_to(gx + math.cos(a) * 150, gy + 60 + math.sin(a) * 150 * 1.0)
        ctx.line_to(gx + math.cos(a) * 130, gy + 60 + math.sin(a) * 130)
        ctx.stroke()
    needle = -math.pi / 2 + clamp(v * 0.9, -0.8, 0.8)
    ctx.set_line_width(6)
    setc(ctx, "#C83A2A")
    ctx.move_to(gx, gy + 60)
    ctx.line_to(gx + math.cos(needle) * 160, gy + 60 + math.sin(needle) * 160)
    ctx.stroke()
    circle(ctx, gx, gy + 60, 12)
    setc(ctx, "#3A2A1A")
    ctx.fill()
    if abs(v) > 0.2:
        glow(ctx, gx, gy - 60, 120, "#FFD27A", 0.3 * abs(v))
    label(ctx, "磁 → 电", 1420, 360, 40, "#FFE8C0", smooth(prog(u, 1.2, 1.8)), "serif_k")
    label(ctx, "发电机、电动机都从这里开始", 1420, 860, 28, "#D9C49A", smooth(prog(u, 2.4, 3.0)), "serif_r")
    film.vignette(ctx, 0.55)


# ================================================================ C2：麦克斯韦与赫兹


def _shot_c2(ctx, t):
    u = t - 23.5
    ctx.set_source(lin(0, 0, 0, H, [(0, "#1A2420"), (1, "#0A100E")]))
    ctx.paint()
    film.paint_texture(ctx, "stone", 0, 0, W, H, 0.18)
    eqs = ["∇⋅E = ρ/ε₀", "∇⋅B = 0", "∇×E = −∂B/∂t", "∇×B = μ₀J + μ₀ε₀ ∂E/∂t"]
    for i, e in enumerate(eqs):
        k = smooth(prog(u, 0.2 + i * 0.45, 0.6 + i * 0.45))
        text(ctx, e, 120, 210 + i * 76, 46, "#EDEDE4", k * 0.92, "eq", "l")
    label(ctx, "麦克斯韦方程组（今天的写法）", 380, 520, 26, "#A8C8B8", smooth(prog(u, 1.8, 2.4)), "serif_r")
    # 电磁波
    wk = smooth(prog(u, 1.8, 2.4))
    head = 900 + 900 * ease_io(prog(u, 2.0, 4.6))
    y0 = 760
    ptsE, ptsB = [], []
    x = 820
    while x < head:
        ph = (x - 820) * 0.022 - u * 6
        ptsE.append((x, y0 - math.sin(ph) * 120))
        ptsB.append((x, y0 + math.sin(ph) * 34))
        x += 6
    if len(ptsE) > 1:
        stroke_pts(ctx, ptsE, 5, "#FFD27A", wk)
        stroke_pts(ctx, ptsB, 5, "#7FC8FF", wk * 0.8)
        ctx.set_line_width(2)
        setc(ctx, "#FFFFFF", 0.3 * wk)
        ctx.move_to(820, y0)
        ctx.line_to(head, y0)
        ctx.stroke()
        label(ctx, "电场", 900, y0 - 160, 26, "#FFD27A", wk, "serif_sb")
        label(ctx, "磁场", 900, y0 + 70, 26, "#7FC8FF", wk, "serif_sb")
        label(ctx, "以光速传播", (820 + head) / 2, y0 + 150, 28, "#E8E8DC", wk, "serif_sb")
    # 发射端与赫兹的接收环
    for (sx, sy) in ((800, y0),):
        circle(ctx, sx - 30, sy, 22)
        circle(ctx, sx + 0, sy, 22)
        setc(ctx, "#C9A060")
        ctx.fill()
    rx, ry = 1720, y0
    ctx.set_line_width(8)
    setc(ctx, "#C9A060")
    circle(ctx, rx, ry, 90)
    ctx.stroke()
    hit = head > rx - 100
    if hit:
        q = (u * 7) % 1
        glow(ctx, rx - 90, ry, 70, "#BFE0FF", 0.9 * (1 - q))
        for k in range(4):
            R = rng(int(u * 20) + k)
            ctx.set_line_width(2)
            setc(ctx, "#E8F4FF", 0.9)
            ctx.move_to(rx - 90, ry - 8)
            ctx.line_to(rx - 90 + R.uniform(-14, 14), ry + R.uniform(-6, 6))
            ctx.line_to(rx - 90, ry + 8)
            ctx.stroke()
        label(ctx, "1887 年 · 赫兹：火花跳了！", rx - 120, ry - 150, 30, "#BFE0FF", smooth(prog(u, 4.4, 5.0)), "serif_sb")
    film.vignette(ctx, 0.5)


# ================================================================ D1：元素周期表

ROWS = ["H                He", "LiBe     BCNOFNe", "NaMg     AlSiPSClAr", "KCaScTiVCrMnFeCoNiCuZnGaGeAsSeBrKr"]
TABLE = [
    [("H", 1)] + [None] * 16 + [("He", 18)],
    [("Li", 1), ("Be", 2)] + [None] * 10 + [("B", 13), ("C", 14), ("N", 15), ("O", 16), ("F", 17), ("Ne", 18)],
    [("Na", 1), ("Mg", 2)] + [None] * 10 + [("Al", 13), ("Si", 14), ("P", 15), ("S", 16), ("Cl", 17), ("Ar", 18)],
    [(s, i + 1) for i, s in enumerate(["K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge",
                                       "As", "Se", "Br", "Kr"])],
    [(s, i + 1) for i, s in enumerate(["Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
                                       "Sb", "Te", "I", "Xe"])],
]
GAPS = {"Ga": ("类铝", "1875", 33.6), "Sc": ("类硼", "1879", 34.6), "Ge": ("类硅", "1886", 35.6)}


def _shot_d1(ctx, t):
    u = t - 30.0
    ctx.set_source(rad(960, 560, 0, 1300, [(0, "#22201E"), (1, "#0A0908")]))
    ctx.paint()
    film.paint_texture(ctx, "paper", 0, 0, W, H, 0.1)
    cw, ch = 82, 92
    x0, y0 = 960 - 9 * cw, 236
    for r_, row in enumerate(TABLE):
        for c_, el in enumerate(row):
            if not el:
                continue
            sym = el[0]
            x, y = x0 + c_ * cw, y0 + r_ * ch
            k = smooth(prog(u, 0.1 + (r_ * 18 + c_) * 0.012, 0.4 + (r_ * 18 + c_) * 0.012))
            gap = GAPS.get(sym)
            found = gap and t >= gap[2]
            if gap and not found:
                rrect(ctx, x + 4, y + 4, cw - 8, ch - 8, 8)
                ctx.set_line_width(3)
                ctx.set_dash((8, 6))
                setc(ctx, "#FFD27A", k)
                ctx.stroke()
                ctx.set_dash(())
                text(ctx, "?", x + cw / 2, y + ch / 2 - 8, 44, "#FFD27A", k, "serif_k")
                text(ctx, gap[0], x + cw / 2, y + ch - 20, 18, "#FFD27A", k, "serif_r")
                continue
            pop_k = 1.0
            if found:
                q = t - gap[2]
                pop_k = 1 + 0.25 * math.exp(-q * 4) * math.sin(q * 20)
                glow(ctx, x + cw / 2, y + ch / 2, 90, "#FFD27A", 0.6 * math.exp(-q * 1.5))
            ctx.save()
            ctx.translate(x + cw / 2, y + ch / 2)
            ctx.scale(pop_k, pop_k)
            rrect(ctx, -cw / 2 + 4, -ch / 2 + 4, cw - 8, ch - 8, 8)
            col = "#3A5A7A" if c_ < 2 else ("#7A5A3A" if c_ >= 12 else "#4A4A5A")
            if found:
                col = "#A8781E"
            setc(ctx, col, 0.9 * k)
            ctx.fill()
            text(ctx, sym, 0, -6, 34, "#F4EEE2", k, "latin_b")
            if found:
                text(ctx, gap[1], 0, 28, 18, "#FFF0D0", 1, "latin")
            ctx.restore()
    # 预言 vs 实测
    k = smooth(prog(u, 3.9, 4.5))
    if k > 0:
        bx, by = 1300, 760
        rrect(ctx, bx - 420, by - 70, 840, 190, 16)
        setc(ctx, "#0E0C0A", 0.85 * k)
        ctx.fill()
        text(ctx, "门捷列夫预言\"类铝\"：原子量 ≈ 68　密度 ≈ 5.9", bx, by - 18, 28, "#E8DCC4", k, "serif_r")
        text(ctx, "1875 年发现的镓：原子量 69.7　密度 5.9", bx, by + 34, 28, "#FFD27A", smooth(prog(u, 4.6, 5.2)), "serif_sb")
    label(ctx, "1869 · 元素周期表", 380, 760, 40, "#F4E6C8", smooth(prog(u, 0.6, 1.2)), "serif_k")
    film.vignette(ctx, 0.55)


# ================================================================ D2：城市亮起来


def _shot_d2(ctx, t):
    u = t - 38.0
    film.sky(ctx, [(0, "#05070F"), (0.6, "#121A30"), (1, "#2A2A3A")])
    film.star_field(ctx, t, 120, 81, area=(0, 90, W, 500), a=0.6 * (1 - smooth(prog(u, 1, 4)) * 0.6))
    R = rng(17)
    x = -40
    builds = []
    while x < W + 40:
        w = R.uniform(70, 170)
        h = R.uniform(120, 380)
        builds.append((x, w, h, R.random()))
        x += w + R.uniform(0, 12)
    gy = 900
    for (bx, w, h, sd) in builds:
        ctx.rectangle(bx, gy - h, w, h)
        setc(ctx, "#0C0E16")
        ctx.fill()
        R2 = rng(int(sd * 1000))
        for i in range(int(w // 26)):
            for j in range(int(h // 34)):
                on_t = 0.3 + R2.random() * 3.5 + (bx / W) * 1.2
                if u > on_t and R2.random() < 0.55:
                    ctx.rectangle(bx + 8 + i * 26, gy - h + 12 + j * 34, 12, 16)
                    setc(ctx, "#FFD27A", 0.85)
                    ctx.fill()
    glow(ctx, 960, gy, 1200, "#FFB24A", 0.25 * smooth(prog(u, 1.0, 4.0)))
    # 电线杆与电线
    for i in range(6):
        px = 120 + i * 360
        ctx.rectangle(px - 6, gy - 220, 12, 220)
        ctx.rectangle(px - 50, gy - 210, 100, 8)
        setc(ctx, "#050608")
        ctx.fill()
        if i < 5:
            for k in (-40, 0, 40):
                ctx.move_to(px + k, gy - 210)
                ctx.curve_to(px + 120 + k, gy - 150, px + 240 + k, gy - 150, px + 360 + k, gy - 210)
            ctx.set_line_width(2)
            setc(ctx, "#050608")
            ctx.stroke()
    # 电报脉冲沿电线跑
    for k in range(5):
        q = (u * 0.5 + k * 0.2) % 1
        x = 120 + q * 1800
        glow(ctx, x, gy - 190, 20, "#BFE0FF", 0.8)
    # 前景灯泡
    bk = smooth(prog(u, 0.2, 1.2))
    bx, by = 1600, 380
    glow(ctx, bx, by, 300, "#FFC46B", 0.5 * bk * film.flicker(t, 3.0, 0.06))
    circle(ctx, bx, by, 70)
    setc(ctx, "#FFF2D0", 0.25 + 0.6 * bk)
    ctx.fill()
    ctx.set_line_width(4)
    setc(ctx, "#FFE8A0", bk)
    ctx.move_to(bx - 22, by + 20)
    for i in range(7):
        ctx.line_to(bx - 22 + i * 7, by - 10 + (i % 2) * 18)
    ctx.stroke()
    rrect(ctx, bx - 34, by + 60, 68, 50, 6)
    setc(ctx, "#8A8A8A")
    ctx.fill()
    film.vignette(ctx, 0.5)


# ================================================================ 主绘制


def draw(ctx, t):
    if t < 10.0:
        _shot_a(ctx, t)
    elif t < 18.5:
        _shot_b(ctx, t)
    elif t < 23.5:
        _shot_c1(ctx, t)
    elif t < 30.0:
        _shot_c2(ctx, t)
    elif t < 38.0:
        _shot_d1(ctx, t)
    else:
        _shot_d2(ctx, t)


def sfx():
    out = [
        (0.0, "ambience_engine", {"dur": 10.0, "rate": 1.4, "gain": 0.8}),
        (0.4, "steam", {"dur": 1.5, "gain": 0.4}), (3.2, "steam", {"dur": 1.2, "gain": 0.3}),
        (6.4, "steam", {"dur": 1.5, "gain": 0.35}),
        (10.0, "ambience_room", {"dur": 8.5, "gain": 0.35}), (10.2, "paper", {"gain": 0.25}),
    ]
    for tt in (10.4, 12.2, 13.4, 14.6, 16.4):
        out.append((tt, "pin", {"gain": 0.3}))
    out += [(16.0, "whoosh", {"dur": 1.6, "gain": 0.2}),
            (18.5, "ambience_room", {"dur": 5.0, "gain": 0.35})]
    for k in range(3):
        out.append((19.2 + k * 2.62, "zap", {"dur": 0.5, "gain": 0.12}))
    out += [(23.5, "hum", {"dur": 6.5, "gain": 0.2}), (23.7, "chalk", {"dur": 1.8, "gain": 0.3}),
            (25.6, "rise", {"dur": 2.0, "gain": 0.2}), (27.2, "crackle", {"dur": 2.8, "gain": 0.35}),
            (30.0, "ambience_room", {"dur": 8.0, "gain": 0.35})]
    for sym, (nm, yr, tt) in GAPS.items():
        out.append((tt, "ding", {"gain": 0.3}))
    out += [(38.0, "ambience_city", {"dur": 6.0, "gain": 0.5}), (38.3, "hum", {"dur": 5.0, "gain": 0.15}),
            (39.0, "telegraph", {"dur": 3.5, "gain": 0.3}), (42.0, "zap", {"dur": 1.2, "gain": 0.2})]
    return out
