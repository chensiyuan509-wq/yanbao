"""第三章 追问为什么：沙地上的圆规作图；希腊柱廊；《几何原本》的公理大厦；
第一视角俯看赛伊尼的井；埃拉托色尼测地球；阿基米德与祖冲之逼近圆周率；亚历山大图书馆。关键词：证明。"""
import math

from ..core import (TAU, H, W, Cam, arrow_head, at, circle, clamp, dashed, ease_in, ease_io, ease_out, ellipse,
                    fbm, glow, kf, lerp, lin, mix, poly, polyline_partial, prog, rad, rng, rrect, setc, smooth,
                    star4, stroke_pts, text, view)
from .. import film
from mascot import draw_prop
from .common import claude, fade_io, label, lit

DUR = 54.0
CHAPTER = dict(num="第 三 章", title="追问为什么", era="约公元前 600 年 — 公元 500 年", key="证明", at=0.8, dur=4.4)
GRAIN = 0.09

VO = [
    (5.2, "古希腊人，不再满足于用神话解释自然。"),
    (8.4, "泰勒斯追问万物的本原；毕达哥拉斯说：{万物皆数}。"),
    (12.2, "欧几里得写成了《{几何原本}》："),
    (15.0, "从 5 条公设出发，一步步推出 {465 个命题}。"),
    (18.3, "不只要知道'是什么'，还要{证明}'为什么'。"),
    (21.6, "夏至正午，赛伊尼的井底映出了{太阳}。"),
    (25.5, "同一时刻，亚历山大港的立柱影子偏了 {7.2 度}，正是圆周的 1/50。"),
    (30.2, "埃拉托色尼由此算出：地球周长约 {4 万公里}。"),
    (34.4, "阿基米德用 96 边形，把圆周率夹在 3.1408 和 3.1429 之间。"),
    (38.4, "刘徽用割圆术逼近圆；祖冲之算出 π 在 {3.1415926} 与 3.1415927 之间，"),
    (43.5, "这个纪录，保持了{九百多年}。"),
    (46.0, "亚历山大图书馆，汇集了地中海世界的书卷。"),
    (49.5, "可许多典籍，后来都在战乱和岁月里{散失}了……", {"spill": 0.6}),
]

SUPERS = [
    (6.0, 11.4, "公元前 6 世纪", "爱琴海东岸 · 米利都"),
    (12.3, 15.8, "约公元前 300 年", "亚历山大港"),
    (21.7, 25.0, "公元前 240 年前后", "赛伊尼（今阿斯旺）· 夏至正午"),
    (34.5, 38.0, "约公元前 250 年", "阿基米德 · 叙拉古"),
    (38.5, 42.6, "263 年 / 约 480 年", "刘徽 · 祖冲之"),
]

# ================================================================ A1：沙地上的圆规作图（与上一章的圆形匹配）


def _sand(ctx, t):
    ctx.set_source(lin(0, 0, W, H, [(0, "#E2C48E"), (1, "#C49A62")]))
    ctx.paint()
    film.paint_texture(ctx, "parchment", 0, 0, W, H, 0.45, scale=0.6)
    R = rng(3)
    for i in range(160):
        x, y = R.uniform(0, W), R.uniform(0, H)
        setc(ctx, "#8A6A3A", 0.15)
        circle(ctx, x, y, R.uniform(1, 2.5))
        ctx.fill()


def _groove(ctx, pts, w=7):
    stroke_pts(ctx, [(x + 2, y + 2.5) for x, y in pts], w, "#FFF1D2", 0.55)
    stroke_pts(ctx, pts, w, "#6E4A24", 0.85)


def _circle_pts(cx, cy, r, a0=0.0, a1=TAU, n=90):
    return [(cx + math.cos(a0 + (a1 - a0) * i / n) * r, cy + math.sin(a0 + (a1 - a0) * i / n) * r) for i in range(n + 1)]


def _shot_a1(ctx, t):
    _sand(ctx, t)
    A, B, r = (960, 540), (1260, 540), 300
    C = (1110, 540 - 300 * math.sqrt(3) / 2)
    _groove(ctx, _circle_pts(*A, r))
    p2 = ease_io(prog(t, 1.0, 2.6))
    tip = None
    if p2 > 0:
        pts = _circle_pts(*B, r, math.pi, math.pi + TAU * p2)
        _groove(ctx, pts)
        tip = pts[-1]
    p3 = ease_io(prog(t, 2.8, 4.2))
    if p3 > 0:
        tri = polyline_partial([A, B, C, A], p3)
        stroke_pts(ctx, tri, 9, "#3A2410", 0.85)
        if p3 < 1:
            tip = tri[-1]
    for pt, nm, dy in ((A, "Α", 40), (B, "Β", 40), (C, "Γ", -44)):
        circle(ctx, *pt, 9)
        setc(ctx, "#3A2410", 0.9)
        ctx.fill()
        text(ctx, nm, pt[0] + (-34 if nm == "Α" else 30), pt[1] + dy, 44, "#3A2410", smooth(prog(t, 2.6, 3.2)), "latin")
    label(ctx, "等边三角形 · 《几何原本》第一卷 命题 1", 960, 860, 30, "#3A2410", smooth(prog(t, 3.6, 4.4)), "serif_sb",
          shadow=False)
    # 柱廊的影子缓缓扫过
    ctx.save()
    ctx.rotate(0.35)
    for i in range(7):
        x = -400 + i * 420 + t * 18
        ctx.rectangle(x, -600, 170, 2400)
    setc(ctx, "#3A2410", 0.18)
    ctx.fill()
    ctx.restore()
    # 第一视角：手握木棍
    if tip is None:
        tip = (A[0] - math.cos(0.3) * r, A[1] + 20)
    with lit("#FFD49A", 0.3, 1.0):
        film.pov_arm(ctx, (1700, 1350), (tip[0] + 260, tip[1] + 330), 140)
        ctx.set_line_width(14)
        ctx.set_line_cap(1)
        setc(ctx, "#6A4A28")
        ctx.move_to(tip[0] + 280, tip[1] + 320)
        ctx.line_to(tip[0], tip[1])
        ctx.stroke()
    film.vignette(ctx, 0.45)


# ================================================================ A2：希腊柱廊


def _column(ctx, x, y, w, h, light, dark):
    rrect(ctx, x - w / 2, y - h, w, h, 4)
    ctx.set_source(lin(x - w / 2, 0, x + w / 2, 0, [(0, dark), (0.35, light), (1, dark)]))
    ctx.fill()
    for k in range(1, 6):
        ctx.rectangle(x - w / 2 + k * w / 6 - 1.5, y - h + 30, 3, h - 60)
    setc(ctx, dark, 0.35)
    ctx.fill()
    rrect(ctx, x - w * 0.7, y - h - 26, w * 1.4, 30, 6)
    setc(ctx, light)
    ctx.fill()
    rrect(ctx, x - w * 0.65, y - 22, w * 1.3, 22, 4)
    setc(ctx, dark)
    ctx.fill()


G = (claude(1180, 905, 0.5, "curious", seed=8.0, hat="laurel").look(5.6, -0.7, -0.2)
     .expr(8.6, "wonder").look(9.0, -0.4, -0.3).nod(10.4))


def _shot_a2(ctx, t):
    u = t - 5.6
    dx = 80 * ease_io(prog(u, 0, 6.0))
    film.sky(ctx, [(0, "#6C8FB8"), (0.5, "#E8C890"), (0.66, "#F5D6A0"), (1, "#C49A62")])
    film.sun(ctx, 1650 - dx * 0.2, 420, 42, 1.0, "#FFF4D8", "#FFC27A", 500)
    # 远处的海
    ctx.set_source(lin(0, 600, 0, 700, [(0, "#7FA0B0"), (1, "#5A7A8A")]))
    ctx.rectangle(-100, 610, W + 200, 100)
    ctx.fill()
    for i in range(30):
        R = rng(i)
        x = R.uniform(0, W)
        setc(ctx, "#FFF2D0", 0.4)
        ctx.rectangle(x + math.sin(t + i) * 10, 620 + R.uniform(0, 70), R.uniform(20, 70), 2)
        ctx.fill()
    ctx.save()
    ctx.translate(-dx, 0)
    ctx.set_source(lin(0, 700, 0, H, [(0, "#D8B47E"), (1, "#9A7448")]))
    ctx.rectangle(-200, 700, W + 400, 500)
    ctx.fill()
    # 柱廊（近大远小的两排）
    for i in range(8):
        x = 120 + i * 280
        _column(ctx, x, 760, 70, 520, "#F2E2C2", "#B89A70")
    rrect(ctx, -100, 160, W + 300, 70, 4)
    setc(ctx, "#E8D5B0")
    ctx.fill()
    ctx.rectangle(-100, 230, W + 300, 14)
    setc(ctx, "#B89A70")
    ctx.fill()
    # 地上的柱影
    for i in range(8):
        x = 120 + i * 280
        poly(ctx, [(x - 35, 760), (x + 35, 760), (x - 260, H + 40), (x - 360, H + 40)])
        setc(ctx, "#5A3E20", 0.25)
        ctx.fill()
    ctx.restore()
    # 人物：泰勒斯（指天）、毕达哥拉斯（在沙上画）
    film.human(ctx, 560, 900, 330, "point", t, "#3A2A1C", 1.0, rim="#FFE0A8", rim_a=0.8, robe=True, hat="hair",
               arms=(0.2, 2.5 + 0.1 * math.sin(t * 1.5)))
    label(ctx, "泰勒斯", 560, 520, 34, "#FFF0D8", smooth(prog(u, 2.6, 3.2)), "serif_sb", sub="万物的本原是水？")
    film.human(ctx, 860, 905, 320, "reach", t, "#2E2116", 1.0, flip=True, rim="#FFE0A8", rim_a=0.8, robe=True,
               hat="hair", arms=(0.3, 1.0 + 0.2 * math.sin(t * 2)))
    label(ctx, "毕达哥拉斯", 860, 520, 34, "#FFF0D8", smooth(prog(u, 3.4, 4.0)), "serif_sb", sub="万物皆数")
    with lit("#FFD49A", 0.35, 1.0):
        G.draw(ctx, t)
    film.grade(ctx, "#FFC27A", 0.15)
    film.vignette(ctx, 0.45)


# ================================================================ B：公理大厦

POSTULATES = ["连线", "延长", "作圆", "直角相等", "平行公设"]


def _shot_b(ctx, t):
    u = t - 11.6
    ctx.set_source(rad(960, 700, 0, 1200, [(0, "#2C2016"), (1, "#0A0705")]))
    ctx.paint()
    film.paint_texture(ctx, "parchment", 0, 0, W, H, 0.12)
    climb = ease_io(prog(u, 2.6, 7.2)) * 520
    ctx.save()
    ctx.translate(0, climb)
    # 5 块地基
    bw, bh = 250, 92
    base_y = 860
    for i, nm in enumerate(POSTULATES):
        x = 960 + (i - 2) * (bw + 14)
        k = smooth(prog(u, 0.3 + i * 0.25, 0.7 + i * 0.25))
        rrect(ctx, x - bw / 2, base_y - bh, bw, bh, 10)
        ctx.set_source(lin(0, base_y - bh, 0, base_y, [(0, "#FFE2A0", k), (1, "#C9963F", k)]))
        ctx.fill()
        text(ctx, f"公设 {i + 1}", x, base_y - bh + 28, 22, "#5A3410", k, "serif_r")
        text(ctx, nm, x, base_y - 30, 34, "#3A2008", k, "serif_k")
    # 往上垒命题
    n_show = int(clamp((u - 1.8) / 5.4) * 465)
    R = rng(5)
    rows = 26
    count = 0
    for r_ in range(rows):
        nper = max(1, 9 - r_ // 4)
        yy = base_y - bh - 12 - (r_ + 1) * 48
        wid = 1300 - r_ * 36
        for c in range(nper):
            count += 1
            idx_need = int(count / (rows * 6) * 465)
            if idx_need > n_show:
                break
            bx = 960 - wid / 2 + (c + 0.5) * wid / nper
            k = 1.0
            rrect(ctx, bx - wid / nper / 2 + 4, yy, wid / nper - 8, 40, 6)
            setc(ctx, mix("#8A6A3A", "#F2D79B", R.random() * 0.6 + 0.2), 0.85 * k)
            ctx.fill()
    # 推理的连线（证明链）
    pk = smooth(prog(u, 6.6, 7.6))
    if pk > 0:
        R2 = rng(9)
        for i in range(14):
            x0 = 960 + R2.uniform(-500, 500)
            y0 = base_y - bh - 20
            x1 = 960 + R2.uniform(-300, 300)
            y1 = base_y - bh - R2.uniform(300, 1200)
            from ..core import curve_arrow
            curve_arrow(ctx, (x0, y0), (x0, (y0 + y1) / 2), (x1, (y0 + y1) / 2), (x1, y1), 3, "#FFE2A0", 0.6 * pk,
                        ease_out(prog(u, 6.6 + i * 0.05, 7.8 + i * 0.05)))
    ctx.restore()
    # 计数与书名
    a = smooth(prog(u, 1.8, 2.4))
    label(ctx, f"命题 {max(1, n_show)}", 1600, 300, 56, "#FFE8C0", a, "serif_k")
    label(ctx, "ΣΤΟΙΧΕΙΑ · 几何原本 · 13 卷", 1600, 370, 28, "#D9C49A", a, "serif_r")
    film.vignette(ctx, 0.6)


# ================================================================ C1：第一视角俯看井底


W2 = None


def _shot_c1(ctx, t):
    u = t - 21.2
    ctx.set_source_rgb(0.05, 0.035, 0.02)
    ctx.paint()
    cx, cy = 960, 540
    zoom = 1 + 0.12 * ease_io(prog(u, 0, 4))
    # 一圈圈石砌井壁（透视）
    for i in range(18, -1, -1):
        f = i / 18
        r = lerp(90, 980, f ** 1.6) * zoom
        shade = 0.12 + 0.75 * f ** 1.3
        circle(ctx, cx + (1 - f) * 20, cy + (1 - f) * 10, r)
        setc(ctx, mix("#2A1A0E", "#C9A170", shade))
        ctx.fill()
        ctx.set_line_width(3)
        setc(ctx, "#1A0E06", 0.5)
        circle(ctx, cx + (1 - f) * 20, cy + (1 - f) * 10, r)
        ctx.stroke()
        R = rng(i)
        for k in range(int(10 + 20 * f)):
            ang = R.uniform(0, TAU)
            ctx.move_to(cx + (1 - f) * 20 + math.cos(ang) * r, cy + (1 - f) * 10 + math.sin(ang) * r)
            ctx.line_to(cx + (1 - f) * 20 + math.cos(ang) * r * 0.93, cy + (1 - f) * 10 + math.sin(ang) * r * 0.93)
        setc(ctx, "#1A0E06", 0.35)
        ctx.stroke()
    # 井底水面：太阳的倒影，和低头的自己
    wx, wy, wr = cx + 20, cy + 10, 88 * zoom
    circle(ctx, wx, wy, wr)
    setc(ctx, "#1C3040")
    ctx.fill()
    ripple = math.sin(t * 3) * 2
    sk = smooth(prog(u, 0.6, 1.6))
    glow(ctx, wx + 6, wy - 4, 220, "#FFF2C8", 0.8 * sk)
    circle(ctx, wx + 6 + ripple, wy - 4, 26 * zoom)
    setc(ctx, "#FFFBEA", sk)
    ctx.fill()
    from mascot import draw_mascot
    ctx.save()
    circle(ctx, wx, wy, wr)
    ctx.clip()
    draw_mascot(ctx, wx - 40, wy + 70, 0.2 * zoom, expr="wonder", t=t, alpha=0.55 * smooth(prog(u, 1.4, 2.2)))
    ctx.restore()
    label(ctx, "太阳正好在头顶 · 没有影子", 960, 900, 32, "#FFE8C0", smooth(prog(u, 1.8, 2.6)), "serif_sb")
    # 第一视角：双手扶着井沿
    with lit("#FFD49A", 0.3, 1.0):
        film.pov_arm(ctx, (220, 1350), (560, 960), 150)
        film.pov_arm(ctx, (1700, 1350), (1360, 960), 150)
    film.vignette(ctx, 0.5)


# ================================================================ C2：测地球示意图


def _shot_c2(ctx, t):
    u = t - 25.2
    ctx.set_source(lin(0, 0, 0, H, [(0, "#E6D2A6"), (1, "#C9AE7E")]))
    ctx.paint()
    film.paint_texture(ctx, "parchment", 0, 0, W, H, 0.7)
    ink = "#3A2414"
    # 地球（大圆的一部分）
    ox, oy, R0 = 760, 1500, 1050
    ctx.set_line_width(5)
    setc(ctx, ink, 0.9)
    ctx.new_path()
    ctx.arc(ox, oy, R0, math.radians(-150), math.radians(-30))
    ctx.stroke()
    a_sy = math.radians(-90)
    a_al = math.radians(-90 - 7.2 * 3)      # 夸大 3 倍便于看清（图上注明）
    sy = (ox + math.cos(a_sy) * R0, oy + math.sin(a_sy) * R0)
    al = (ox + math.cos(a_al) * R0, oy + math.sin(a_al) * R0)
    # 平行的太阳光
    k1 = smooth(prog(u, 0.2, 1.0))
    for i in range(7):
        x = 300 + i * 150
        dashed(ctx, x, 120, x, 360 if i != 3 else 0, 3, "#C9781E", k1 * 0.8, (16, 10), -t * 30)
    film.sun(ctx, 1640, 200, 44, k1, "#FFE8B0", "#FFB766", 260)
    label(ctx, "阳光几乎平行地照来", 1640, 300, 28, ink, k1, "serif_sb", shadow=False)
    # 赛伊尼：井，光直射井底
    k2 = smooth(prog(u, 0.6, 1.2))
    dashed(ctx, sy[0], 150, sy[0], sy[1], 4, "#C9781E", k2, (16, 10), -t * 30)
    rrect(ctx, sy[0] - 20, sy[1] - 10, 40, 60, 4)
    setc(ctx, ink, k2)
    ctx.fill()
    label(ctx, "赛伊尼：井底有阳光", sy[0] + 190, sy[1] - 40, 30, ink, k2, "serif_sb", shadow=False)
    # 亚历山大港：立柱与影子
    k3 = smooth(prog(u, 1.4, 2.2))
    nx, ny = math.cos(a_al), math.sin(a_al)
    top = (al[0] + nx * 200, al[1] + ny * 200)
    ctx.set_line_width(9)
    setc(ctx, ink, k3)
    ctx.move_to(*al)
    ctx.line_to(*top)
    ctx.stroke()
    dashed(ctx, top[0], 150, top[0], top[1], 4, "#C9781E", k3, (16, 10), -t * 30)
    sh = (top[0], top[1] + 200 / math.cos(math.radians(21.6)))
    ctx.set_line_width(5)
    setc(ctx, "#7A3A12", k3)
    ctx.move_to(*top)
    ctx.line_to(al[0] + (top[0] - al[0]) * 0 + 70, al[1] + 10)
    ctx.stroke()
    label(ctx, "亚历山大港：影子偏 7.2°", al[0] - 40, al[1] - 280, 30, ink, k3, "serif_sb", shadow=False)
    # 延长到地心：同样的 7.2°
    k4 = smooth(prog(u, 2.6, 3.6))
    if k4 > 0:
        for p in (sy, al):
            dashed(ctx, p[0], p[1], lerp(p[0], ox, k4 * 0.45), lerp(p[1], oy, k4 * 0.45), 3, ink, 0.7, (10, 8))
        label(ctx, "圆心角也是 7.2°", 640, 900, 32, "#7A3A12", k4, "serif_sb", shadow=False)
    # 计算
    k5 = smooth(prog(u, 3.8, 4.6))
    k6 = smooth(prog(u, 5.4, 6.2))
    rrect(ctx, 1240, 430, 600, 360, 18)
    setc(ctx, "#F6E8C6", 0.85 * k5)
    ctx.fill()
    label(ctx, "7.2° = 360° ÷ 50", 1540, 490, 36, ink, k5, "serif_k", shadow=False)
    label(ctx, "两地相距 5000 斯塔德", 1540, 560, 30, ink, k5, "serif_r", shadow=False)
    label(ctx, "周长 = 5000 × 50", 1540, 630, 34, ink, k6, "serif_sb", shadow=False)
    label(ctx, "= 25 万斯塔德 ≈ 4 万公里", 1540, 700, 36, "#9A3A12", k6, "serif_k", shadow=False)
    label(ctx, "（示意图，角度已放大）", 300, 930, 22, "#6A4A2A", 0.8, "serif_r", shadow=False)
    film.vignette(ctx, 0.4, color="#2A1A0A")


# ================================================================ D：逼近圆周率

STAGES = [(6, 34.0), (12, 34.8), (24, 35.6), (48, 36.4), (96, 37.2), (3072, 39.4)]


def _shot_d(ctx, t):
    u = t - 33.8
    china = smooth(prog(t, 38.6, 39.6))
    bg = mix("#1E1610", "#141210", china)
    ctx.set_source(rad(960, 520, 0, 1200, [(0, mix("#3A2A1A", "#2A2622", china)), (1, bg)]))
    ctx.paint()
    film.paint_texture(ctx, "paper", 0, 0, W, H, 0.15 + 0.15 * china)
    cx, cy, r = 760, 540, 330
    n = 6
    for nn, ts in STAGES:
        if t >= ts:
            n = nn
    # 外切与内接多边形
    def ngon(rr, k):
        return [(cx + math.cos(-math.pi / 2 + i / k * TAU) * rr, cy + math.sin(-math.pi / 2 + i / k * TAU) * rr)
                for i in range(k + 1)]
    ctx.set_line_width(4)
    setc(ctx, "#F2E2C2", 0.85)
    circle(ctx, cx, cy, r)
    ctx.stroke()
    if n <= 96:
        outer = r / math.cos(math.pi / n)
        stroke_pts(ctx, ngon(outer, n), 3, "#FF9A5A", 0.85)
        stroke_pts(ctx, ngon(r, n), 3, "#7FC8FF", 0.85)
        lo = n * math.sin(math.pi / n)
        hi = n * math.tan(math.pi / n)
        if n == 96:            # 阿基米德用分数估算得到的（略宽的）区间
            lo, hi = 3 + 10 / 71, 3 + 1 / 7
    else:
        stroke_pts(ctx, ngon(r, 192), 3, "#7FC8FF", 0.85)
        lo, hi = 3.14159, 3.14160
    label(ctx, f"{n} 边形", cx, cy - 14, 64, "#FFE8C0", 1.0, "serif_k")
    label(ctx, "内接 ↔ 外切", cx, cy + 50, 28, "#CDBA92", 1.0, "serif_r")
    # 右侧：区间
    x0 = 1320
    if t < 38.6:
        label(ctx, f"{lo:.4f}  <  π  <  {hi:.4f}", x0 + 130, 420, 46, "#FFE8C0", 1.0, "latin")
        if n >= 96:
            label(ctx, "阿基米德：3 10/71 < π < 3 1/7", x0 + 130, 500, 30, "#F2D79B", smooth(prog(t, 37.2, 37.8)),
                  "serif_sb")
    else:
        k = china
        label(ctx, "刘徽 · 割圆术", x0 + 130, 300, 40, "#F4E6C8", k, "serif_k")
        label(ctx, "割之弥细，所失弥少", x0 + 130, 360, 32, "#D9C49A", k, "kai")
        label(ctx, "3072 边形 → π ≈ 3.1416", x0 + 130, 420, 34, "#FFE8C0", smooth(prog(t, 39.6, 40.2)), "serif_sb")
        k2 = smooth(prog(t, 40.6, 41.4))
        label(ctx, "祖冲之", x0 + 130, 540, 40, "#F4E6C8", k2, "serif_k")
        label(ctx, "3.1415926  <  π  <  3.1415927", x0 + 130, 610, 40, "#FFD27A", smooth(prog(t, 41.0, 41.8)),
              "latin")
        k3 = smooth(prog(t, 43.4, 44.2))
        label(ctx, "领先世界 900 多年", x0 + 130, 700, 36, "#FF9A5A", k3, "serif_k")
    film.vignette(ctx, 0.55)


# ================================================================ E：亚历山大图书馆

L1 = (claude(1240, 905, 0.46, "awe", seed=9.0, hat="laurel").hold(45.6, ("scroll",), "front")
      .look(45.8, -0.6, -0.4).expr(49.4, "sad").look(49.6, 0.0, 0.3).sigh(50.4))


def _shot_e(ctx, t):
    u = t - 45.6
    dim = smooth(prog(u, 3.6, 8.0))
    fl = film.flicker(t, 11.0, 0.12)
    dx = 140 * ease_io(prog(u, 0, 8.4))
    ctx.set_source(rad(960, 500, 0, 1300, [(0, "#3A2616"), (1, "#0C0805")]))
    ctx.paint()
    ctx.save()
    ctx.translate(-dx, 0)
    # 一格格的书卷架
    for col in range(9):
        x = -60 + col * 260
        for row in range(7):
            y = 140 + row * 108
            rrect(ctx, x, y, 240, 98, 4)
            setc(ctx, "#24160C")
            ctx.fill()
            R = rng(col * 10 + row)
            for k in range(7):
                sx, sy = x + 22 + (k % 4) * 58 + (k // 4) * 28, y + 30 + (k // 4) * 40
                circle(ctx, sx, sy, 18)
                setc(ctx, mix("#A88A5A", "#5E4428", R.random()))
                ctx.fill()
                circle(ctx, sx, sy, 6)
                setc(ctx, "#6A4A2A")
                ctx.fill()
    ctx.restore()
    ctx.set_source(rad(1000, 560, 200, 1200, [(0, "#000000", 0), (1, "#000000", 0.6)]))
    ctx.paint()
    # 地面与人物
    ctx.set_source(lin(0, 880, 0, H, [(0, "#2A1A0E"), (1, "#0E0905")]))
    ctx.rectangle(-50, 900, W + 100, 200)
    ctx.fill()
    film.shaft(ctx, 1500, 0, 1000, 960, 160, 500, "#FFD49A", 0.16 * (1 - dim * 0.7))
    film.dust(ctx, t, 60, 4, (900, 100, 700, 860), "#FFE6B8", 0.5 * (1 - dim * 0.5))
    film.human(ctx, 600, 910, 330, "hold", t, "#1A100A", 1.0, rim="#FFB060", rim_a=0.7, robe=True, hat="hair")
    with at(ctx, 660, 700, 0.9):
        draw_prop(ctx, ("scroll",), t)
    glow(ctx, 380, 620, 260, "#FFB24A", 0.5 * fl)
    with at(ctx, 380, 700, 1.0):
        draw_prop(ctx, ("lamp",), t)
    with lit("#FFB070", 0.45, 0.85 * (1 - dim * 0.3)):
        L1.draw(ctx, t)
    film.vignette(ctx, 0.55 + 0.3 * dim)
    film.fade_black(ctx, 0.35 * dim)


# ================================================================ 主绘制


def draw(ctx, t):
    if t < 5.6:
        _shot_a1(ctx, t)
    elif t < 11.6:
        _shot_a2(ctx, t)
    elif t < 21.2:
        _shot_b(ctx, t)
    elif t < 25.2:
        _shot_c1(ctx, t)
    elif t < 33.8:
        _shot_c2(ctx, t)
    elif t < 45.6:
        _shot_d(ctx, t)
    else:
        _shot_e(ctx, t)


def sfx():
    out = [
        (0.0, "ambience_wind", {"dur": 5.6, "gain": 0.25}),
        (0.9, "sand", {"dur": 1.7, "gain": 0.35}),
        (2.8, "sand", {"dur": 1.4, "gain": 0.35}),
        (5.6, "ambience_sea", {"dur": 6.0, "gain": 0.5}),
        (5.6, "ambience_birds", {"dur": 6.0, "gain": 0.25}),
        (11.6, "ambience_room", {"dur": 9.6, "gain": 0.4}),
    ]
    for i in range(5):
        out.append((11.9 + i * 0.25, "thud", {"gain": 0.3, "pitch": 0.8 + i * 0.05}))
    out += [(13.4, "gears_run", {"dur": 5.0, "gain": 0.15}), (14.2, "rise", {"dur": 4.0, "gain": 0.2}),
            (18.2, "shimmer", {"dur": 1.6, "gain": 0.2}),
            (21.2, "ambience_cave", {"dur": 4.0, "gain": 0.4}), (21.8, "drip", {"gain": 0.3}),
            (22.2, "sparkle", {"dur": 1.2, "gain": 0.2}),
            (25.2, "ambience_room", {"dur": 8.6, "gain": 0.35}), (25.4, "quill", {"dur": 2.0, "gain": 0.25}),
            (27.0, "quill", {"dur": 1.6, "gain": 0.22}), (29.0, "chalk", {"dur": 1.0, "gain": 0.15}),
            (30.6, "quill", {"dur": 1.8, "gain": 0.22}), (31.4, "ding", {"gain": 0.18}),
            (33.8, "ambience_room", {"dur": 11.8, "gain": 0.35})]
    for nn, ts in STAGES:
        out.append((ts, "tick", {"gain": 0.3}))
    out += [(38.6, "swish", {"gain": 0.2}), (41.0, "ticks", {"dur": 1.4, "rate": 6, "gain": 0.15}),
            (43.4, "chime", {"gain": 0.18}),
            (45.6, "ambience_room", {"dur": 8.4, "gain": 0.5}), (45.6, "ambience_fire", {"dur": 8.4, "gain": 0.15}),
            (46.2, "paper", {"gain": 0.25}), (49.5, "hush", {"dur": 3.0, "gain": 0.3}), (51.2, "rumble", {"dur": 2.0, "gain": 0.25})]
    return out
