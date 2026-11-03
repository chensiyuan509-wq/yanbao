"""第五章 科学革命：哥白尼的日心说；伽利略的望远镜（第一视角看月亮、看木星的卫星）；
开普勒的 8 角分；斜面实验；皇家学会与科学期刊；牛顿的苹果与大炮。关键词：实验。"""
import math

from ..core import (TAU, H, W, Cam, arrow_head, at, circle, clamp, dashed, ease_in, ease_io, ease_out, ellipse,
                    fbm, glow, kf, lerp, lin, mix, poly, polyline_partial, prog, rad, rng, rrect, setc, smooth,
                    star4, stroke_pts, text, view)
from .. import film
from mascot import draw_prop
from .common import claude, fade_io, label, lit

DUR = 58.0
CHAPTER = dict(num="第 五 章", title="科学革命", era="1543 — 1687 年", key="实验", at=0.8, dur=4.4)
GRAIN = 0.085

VO = [
    (5.3, "哥白尼说：不是太阳绕着地球转，"),
    (7.9, "而是{地球绕着太阳转}。"),
    (9.9, "1609 年，伽利略把{望远镜}对准了天空。"),
    (13.3, "月亮上有山、有环形坑——天空并不完美。"),
    (17.7, "木星旁的四颗小星，在{绕着木星转}。"),
    (21.2, "原来，并不是万物都绕着地球转。"),
    (23.8, "开普勒用第谷 20 多年的数据，计算火星轨道。"),
    (27.5, "圆轨道差了 {8 角分}，约 1/4 个月亮宽。"),
    (30.6, "他不放过这点误差：轨道是{椭圆}！"),
    (33.7, "斜面实验：距离与{时间的平方}成正比。"),
    (36.7, "伽利略：自然之书，用{数学}写成。"),
    (39.1, "皇家学会的格言：{不要只听信任何人}。"),
    (42.1, "成果要发表，供人{重复检验}。"),
    (44.8, "1687 年，牛顿出版《自然哲学的数学原理》："),
    (47.9, "让苹果落地的力，和拉住月亮的力，是{同一种力}。"),
    (51.6, "天上和地上，服从{同一套规律}。"),
    (54.3, "观察、假设、实验、用数学表达、公开检验——{科学方法}成形了。", {"spill": 0.6}),
]

SUPERS = [
    (5.4, 9.0, "1543 年", "哥白尼《天体运行论》"),
    (10.0, 13.0, "1609 — 1610 年", "帕多瓦 · 伽利略"),
    (23.9, 27.2, "1609 年", "开普勒《新天文学》"),
    (39.1, 42.0, "1660 年", "伦敦 · 英国皇家学会"),
    (44.9, 47.8, "1687 年", "牛顿《原理》"),
]

# ================================================================ A：日心说书页 → 真实的轨道

PLANETS = [("☿", 95, 4.1, "#C9B8A0"), ("♀", 150, 1.6, "#F2D29A"), ("♁", 215, 1.0, "#7FB6FF"), ("♂", 285, 0.53, "#FF8A5A"),
           ("♃", 380, 0.084, "#E8C49A"), ("♄", 470, 0.034, "#E8D6A0")]


def _shot_a(ctx, t):
    u = t
    z = 1 + 1.6 * ease_in(prog(u, 3.6, 8.6))
    real = smooth(prog(u, 5.6, 8.0))
    fl = film.flicker(t, 2.0, 0.1)
    ctx.set_source(rad(960, 540, 0, 1200, [(0, mix("#3A2614", "#0A0C1A", real)), (1, mix("#0A0604", "#020308", real))]))
    ctx.paint()
    ctx.save()
    ctx.translate(960, 560)
    ctx.scale(z, z)
    ctx.translate(-960, -560)
    pa = 1 - real
    if pa > 0.01:
        glow(ctx, 360, 380, 500, "#FFB24A", 0.35 * fl * pa)
        # 书页
        for sx in (-1, 1):
            ctx.save()
            ctx.translate(960, 560)
            ctx.move_to(0, -380)
            ctx.curve_to(sx * 200, -400, sx * 420, -390, sx * 560, -370)
            ctx.line_to(sx * 560, 400)
            ctx.curve_to(sx * 420, 380, sx * 200, 390, 0, 410)
            ctx.close_path()
            ctx.set_source(lin(0, -400, 0, 410, [(0, "#EFE2C2", pa), (1, "#CDB688", pa)]))
            ctx.fill()
            ctx.restore()
        film.paint_texture(ctx, "paper", 400, 170, 1120, 800, 0.35 * pa)
        text(ctx, "DE REVOLUTIONIBUS", 1250, 250, 30, "#3A2414", pa, "latin_b")
        text(ctx, "ORBIUM COELESTIUM", 1250, 292, 26, "#3A2414", pa, "latin")
        for j in range(12):
            ctx.rectangle(1040, 360 + j * 36, 420 if j % 4 else 300, 6)
        setc(ctx, "#5A4430", 0.5 * pa)
        ctx.fill()
        with at(ctx, 360, 560, 1.4):
            draw_prop(ctx, ("candle",), t, pa)
    # 同心圆：书页上的墨线 → 夜空里的轨道
    cx, cy = 700, 580
    ink = mix("#3A2414", "#8FA6D8", real)
    for i, (sym, r, w, col) in enumerate(PLANETS):
        rr = r * (0.75 if real < 0.5 else 0.75 + 0.25 * real)
        ctx.set_line_width(2.5 / z * 1.5)
        setc(ctx, ink, 0.8)
        circle(ctx, cx, cy, rr)
        ctx.stroke()
        ang = -1.2 + i * 1.1 + t * w * 0.35 * real
        px, py = cx + math.cos(ang) * rr, cy + math.sin(ang) * rr
        if real > 0:
            glow(ctx, px, py, 26, col, 0.5 * real)
            circle(ctx, px, py, 7 + (3 if sym == "♃" else 0))
            setc(ctx, col, real)
            ctx.fill()
        text(ctx, sym, px + 20, py - 18, 26, mix("#3A2414", "#E8E2FF", real), 1.0, "sym")
    # 太阳
    glow(ctx, cx, cy, 140, "#FFC46B", 0.2 + 0.6 * real)
    circle(ctx, cx, cy, 24)
    setc(ctx, mix("#C9781E", "#FFE8A8", real))
    ctx.fill()
    circle(ctx, cx, cy, 5)
    setc(ctx, "#3A2414", 1 - real)
    ctx.fill()
    text(ctx, "SOL", cx, cy + 50, 26, "#3A2414", 1 - real, "latin_b")
    ctx.restore()
    if real > 0:
        film.star_field(ctx, t, 120, 23, a=0.7 * real)
    film.vignette(ctx, 0.55)


# ================================================================ B：伽利略的望远镜

G5 = (claude(1180, 905, 0.46, "curious", seed=11.0).hold(9.5, ("telescope",), "r", 0.0)
      .look(9.6, -0.6, -0.8).expr(11.6, "wonder"))


def _skyline(ctx, y, color):
    """意大利城市剪影：圆顶、钟楼、屋顶。"""
    pts = [(-50, y)]
    x = -50
    R = rng(4)
    while x < W + 50:
        kind = R.random()
        w = R.uniform(60, 160)
        h = R.uniform(40, 120)
        pts += [(x, y - h), (x + w, y - h)]
        x += w
    pts += [(W + 50, y)]
    poly(ctx, pts)
    setc(ctx, color)
    ctx.fill()
    # 圆顶与钟楼
    ellipse(ctx, 520, y - 170, 120, 110)
    ctx.rectangle(400, y - 170, 240, 170)
    ctx.fill()
    ctx.rectangle(512, y - 330, 16, 60)
    ctx.fill()
    ctx.rectangle(1540, y - 360, 70, 360)
    poly(ctx, [(1530, y - 360), (1575, y - 450), (1620, y - 360)])
    ctx.fill()


def _shot_b1(ctx, t):
    u = t - 9.5
    film.sky(ctx, [(0, "#04060E"), (0.6, "#0E1832"), (1, "#24304A")])
    film.star_field(ctx, t, 260, 51, area=(0, 90, W, 700), a=0.9)
    film.moon(ctx, 400, 280, 46, 0.4, 1.0, glow_a=0.4)
    _skyline(ctx, 820, "#0A0E18")
    ctx.set_source(lin(0, 800, 0, H, [(0, "#1A1410"), (1, "#0A0806")]))
    ctx.rectangle(-50, 820, W + 100, 300)
    ctx.fill()
    # 伽利略与他的望远镜
    film.human(ctx, 760, 910, 360, "telescope", t, "#0C0A08", 1.0, rim="#8FA6D8", rim_a=0.6, hat="hair", lean=-0.1)
    ctx.save()
    ctx.translate(800, 620)
    ctx.rotate(-0.62)
    rrect(ctx, -20, -14, 320, 28, 8)
    ctx.set_source(lin(0, -14, 0, 14, [(0, "#E8C27A"), (1, "#6A4A1A")]))
    ctx.fill()
    ctx.restore()
    with lit("#8FA6FF", 0.45, 0.6):
        G5.draw(ctx, t)
    film.vignette(ctx, 0.6)


def _scope_jitter(t):
    return math.sin(t * 1.3) * 6, math.cos(t * 1.1) * 5


def _shot_b2(ctx, t):
    """第一视角：望远镜里的月亮。"""
    u = t - 13.0
    ctx.set_source_rgb(0.01, 0.01, 0.02)
    ctx.paint()
    jx, jy = _scope_jitter(t)
    cx, cy = 960 + jx, 540 + jy
    focus = ease_out(prog(u, 0, 1.2))
    mx, my, r = cx + 120 - 80 * ease_io(prog(u, 0, 4.5)), cy + 40, 560
    # 月面
    circle(ctx, mx, my, r)
    ctx.set_source(rad(mx - r * 0.3, my - r * 0.3, 0, r * 1.2, [(0, "#F2EADA"), (0.6, "#C9C0AE"), (1, "#8A8272")]))
    ctx.fill()
    R = rng(12)
    ctx.save()
    circle(ctx, mx, my, r)
    ctx.clip()
    for i in range(34):
        ang, d = R.uniform(0, TAU), R.uniform(0, 0.95) ** 0.7 * r
        cr = R.uniform(8, 55) * (1.4 if i < 4 else 1)
        x, y = mx + math.cos(ang) * d, my + math.sin(ang) * d
        circle(ctx, x, y, cr)
        setc(ctx, "#8A8272", 0.25)
        ctx.fill()
        ctx.new_sub_path()
        ctx.arc(x, y, cr, math.pi * 0.15, math.pi * 1.05)
        ctx.set_line_width(cr * 0.18)
        setc(ctx, "#FFF8E8", 0.35)
        ctx.stroke()
    for i in range(6):          # 月海
        ellipse(ctx, mx + R.uniform(-0.5, 0.4) * r, my + R.uniform(-0.5, 0.5) * r, R.uniform(80, 200), R.uniform(60, 150))
        setc(ctx, "#7A7466", 0.3)
        ctx.fill()
    # 明暗交界线（右侧是夜）
    ctx.set_source(lin(mx + r * 0.15, 0, mx + r * 0.55, 0, [(0, "#000000", 0), (1, "#000000", 0.95)]))
    ctx.rectangle(mx - r, my - r, 2 * r, 2 * r)
    ctx.fill()
    ctx.restore()
    label(ctx, "山与环形坑", cx - 330, cy + 300, 32, "#FFE8C0", smooth(prog(u, 1.4, 2.0)), "serif_sb")
    if focus < 1:
        ctx.set_source_rgba(0, 0, 0, 0.6 * (1 - focus))
        ctx.paint()
    film.scope_view(ctx, cx, cy, 430)


JUP_NIGHTS = [("1610 年 1 月 7 日", [-2.4, -1.1, 1.4]), ("1 月 8 日", [0.9, 1.6, 2.4]), ("1 月 10 日", [-2.0, -1.0]),
              ("1 月 13 日", [-1.2, 0.8, 1.7, 2.6])]


def _shot_b3(ctx, t):
    """第一视角：木星和它的四颗卫星，一夜一夜换位置。"""
    u = t - 17.5
    ctx.set_source_rgb(0.01, 0.01, 0.03)
    ctx.paint()
    jx, jy = _scope_jitter(t)
    cx, cy = 960 + jx, 520 + jy
    film.star_field(ctx, t, 60, 33, area=(500, 120, 900, 800), a=0.5)
    idx = min(3, int(u / 1.45))
    q = u - idx * 1.45
    glow(ctx, cx, cy, 120, "#F2D8A8", 0.4)
    circle(ctx, cx, cy, 40)
    ctx.set_source(lin(0, cy - 40, 0, cy + 40, [(0, "#F2DDB0"), (0.3, "#C9A070"), (0.5, "#F0D8A8"), (0.7, "#B88A5A"), (1, "#E8CFA0")]))
    ctx.fill()
    name, pos = JUP_NIGHTS[idx]
    k = smooth(q / 0.3)
    for p in pos:
        x = cx + p * 110
        glow(ctx, x, cy, 30, "#FFFFFF", 0.5 * k)
        circle(ctx, x, cy, 6)
        setc(ctx, "#FFFFFF", k)
        ctx.fill()
    label(ctx, name, cx, cy + 200, 40, "#FFE8C0", k, "serif_sb")
    # 已经记下的夜晚（小草图，左下角排开）
    for j in range(idx):
        nm, ps = JUP_NIGHTS[j]
        yy = 720 + j * 0
        xx = 700 + j * 170
    film.scope_view(ctx, cx, cy, 430)
    # 伽利略的手绘记录（视野外的纸上）
    for j in range(idx + 1):
        nm, ps = JUP_NIGHTS[j]
        y = 200 + j * 70
        a = smooth(prog(u, j * 1.45 + 0.4, j * 1.45 + 0.8))
        text(ctx, "○", 1600, y, 26, "#F2E2C2", a, "latin")
        for p in ps:
            text(ctx, "*", 1600 + p * 34, y + 6, 26, "#F2E2C2", a, "latin_b")
        text(ctx, nm.replace("1610 年 ", ""), 1600, y + 30, 18, "#CDBA92", a, "serif_r")


# ================================================================ C：开普勒的 8 角分


def _shot_c(ctx, t):
    u = t - 23.5
    fl = film.flicker(t, 9.0, 0.1)
    ctx.set_source(rad(900, 520, 0, 1300, [(0, "#2C2016"), (1, "#0A0705")]))
    ctx.paint()
    film.paint_texture(ctx, "parchment", 0, 0, W, H, 0.12)
    glow(ctx, 200, 300, 500, "#FFB24A", 0.25 * fl)
    # 左：第谷的数据表
    R = rng(21)
    for r_ in range(14):
        a = smooth(prog(u, r_ * 0.08, r_ * 0.08 + 0.3)) * (1 - 0.6 * smooth(prog(u, 3.5, 4.5)))
        line = f"{1580 + r_ * 2}  {R.randint(0, 359):3d}° {R.randint(0, 59):02d}′  {R.randint(0, 7)}° {R.randint(0, 59):02d}′"
        text(ctx, line, 130, 250 + r_ * 46, 27, "#E8D8B8", a, "latin", "l")
    label(ctx, "第谷 · 二十多年的观测", 330, 920, 28, "#D9B26A", smooth(prog(u, 0.4, 1.0)), "serif_sb")
    # 右：火星轨道
    cx, cy = 1250, 540
    a_, b_ = 330, 300
    c_ = math.sqrt(a_ * a_ - b_ * b_)
    sun = (cx + c_, cy)
    glow(ctx, *sun, 90, "#FFC46B", 0.7)
    circle(ctx, *sun, 18)
    setc(ctx, "#FFE8A8")
    ctx.fill()
    # 观测点（落在椭圆上）
    pts = []
    for i in range(16):
        th = i / 16 * TAU + 0.2
        pts.append((cx + a_ * math.cos(th), cy + b_ * math.sin(th)))
    pk = smooth(prog(u, 1.0, 2.2))
    for i, p in enumerate(pts):
        circle(ctx, p[0], p[1], 7)
        setc(ctx, "#FF8A5A", pk)
        ctx.fill()
    # 圆形模型
    ck = smooth(prog(u, 2.2, 3.0)) * (1 - smooth(prog(u, 7.2, 8.0)))
    rc = (a_ + b_) / 2
    ctx.set_line_width(3)
    setc(ctx, "#8FB6FF", 0.9 * ck)
    circle(ctx, cx + c_ * 0.5, cy, rc)
    ctx.stroke()
    # 放大镜看误差
    mk = smooth(prog(u, 3.8, 4.6)) * (1 - smooth(prog(u, 7.0, 7.6)))
    if mk > 0:
        p = pts[4]
        q = (cx + c_ * 0.5 + rc * math.cos(math.atan2(p[1] - cy, p[0] - cx - c_ * 0.5)),
             cy + rc * math.sin(math.atan2(p[1] - cy, p[0] - cx - c_ * 0.5)))
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
    # 椭圆
    ek = ease_io(prog(u, 7.0, 8.6))
    if ek > 0:
        ell = [(cx + a_ * math.cos(th), cy + b_ * math.sin(th)) for th in [i / 120 * TAU for i in range(121)]]
        stroke_pts(ctx, polyline_partial(ell, ek), 5, "#FFE2A8", 1.0)
        f2 = (cx - c_, cy)
        circle(ctx, *f2, 8)
        setc(ctx, "#FFE2A8", ek)
        ctx.fill()
        label(ctx, "椭圆 · 太阳在一个焦点上", cx, cy + b_ + 70, 32, "#FFE2A8", smooth(prog(u, 8.2, 8.8)), "serif_sb")
    film.vignette(ctx, 0.55)


# ================================================================ D1：斜面实验


def _shot_d1(ctx, t):
    u = t - 33.5
    ctx.set_source(rad(960, 560, 0, 1300, [(0, "#3A2818"), (1, "#0E0905")]))
    ctx.paint()
    film.shaft(ctx, 300, 90, 700, 980, 160, 420, "#FFD49A", 0.12)
    x0, y0, x1, y1 = 260, 380, 1660, 840
    poly(ctx, [(x0, y0), (x1, y1), (x1, y1 + 60), (x0, y0 + 60)])
    ctx.set_source(lin(0, y0, 0, y1 + 60, [(0, "#8A6A3E"), (1, "#5A3E1E")]))
    ctx.fill()
    ctx.set_line_width(4)
    setc(ctx, "#C9A060")
    ctx.move_to(x0, y0)
    ctx.line_to(x1, y1)
    ctx.stroke()
    T = 4
    period = 0.9
    tt = clamp((u - 0.4) / period, 0, T)
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
        ctx.move_to(mx - nx * 0, my)
        ctx.line_to(mx + nx * 70, my + ny * 70)
        ctx.stroke()
        if hit:
            glow(ctx, mx + nx * 70, my + ny * 70, 40, "#FFD27A", 0.6 * max(0, 1 - (tt - k) * 1.5))
        text(ctx, f"{k * k}", mx + nx * 110, my + ny * 110, 40, "#FFE8C0", 1.0 if hit else 0.35, "latin_b")
    circle(ctx, bx + nx * 26, by + ny * 26, 26)
    ctx.set_source(rad(bx + nx * 20, by + ny * 20, 2, 30, [(0, "#E8E8F0"), (1, "#6A6A78")]))
    ctx.fill()
    label(ctx, "时间 1 : 2 : 3 : 4  →  距离 1 : 4 : 9 : 16", 960, 230, 40, "#FFE8C0", smooth(prog(u, 3.6, 4.2)), "serif_sb")
    label(ctx, "距离 ∝ 时间²", 1450, 330, 44, "#FFD27A", smooth(prog(u, 4.0, 4.6)), "serif_k")


# ================================================================ D2：皇家学会与期刊


def _shot_d2(ctx, t):
    u = t - 38.5
    ctx.set_source(rad(960, 520, 0, 1300, [(0, "#2A2420"), (1, "#0A0806")]))
    ctx.paint()
    film.paint_texture(ctx, "stone", 0, 0, W, H, 0.3)
    # 石刻铭文
    k = smooth(prog(u, 0.2, 1.0))
    rrect(ctx, 460, 250, 1000, 230, 14)
    ctx.set_source(lin(0, 250, 0, 480, [(0, "#8A8478", k), (1, "#5E5A52", k)]))
    ctx.fill()
    film.tracked(ctx, "NULLIUS IN VERBA", 962, 352, 78, "#2A2620", k, "latin_b", 0.12)
    film.tracked(ctx, "NULLIUS IN VERBA", 960, 348, 78, "#D8D2C4", k * 0.9, "latin_b", 0.12)
    label(ctx, "不要只听信任何人的话", 960, 440, 34, "#F2E6CE", smooth(prog(u, 0.8, 1.4)), "serif_sb")
    # 期刊一本本堆起来
    for i in range(9):
        kk = ease_out(prog(u, 3.0 + i * 0.22, 3.4 + i * 0.22))
        if kk <= 0:
            continue
        y = 930 - i * 30 - (1 - kk) * 200
        rrect(ctx, 760 + (i % 3) * 6, y, 400, 32, 4)
        setc(ctx, mix("#7A2E1E", "#3A4A6A", (i % 3) / 2), kk)
        ctx.fill()
        ctx.rectangle(780 + (i % 3) * 6, y + 12, 360, 4)
        setc(ctx, "#E8C27A", kk * 0.7)
        ctx.fill()
    label(ctx, "Philosophical Transactions · 1665", 960, 545, 36, "#FFE8C0", smooth(prog(u, 3.2, 3.8)), "latin_i")
    label(ctx, "发表 → 质疑 → 重复实验 → 修正", 960, 600, 32, "#D9C49A", smooth(prog(u, 4.0, 4.6)), "serif_sb")
    film.vignette(ctx, 0.55)


# ================================================================ E：牛顿


N5 = (claude(1010, 868, 0.5, "relieved", seed=12.0).sit(44.5, 1.0, 0.01).look(44.6, 0.4, -0.3)
      .expr(47.3, "ko").startle(47.3).expr(47.9, "surprised").look(48.0, 0.8, -0.9)
      .expr(48.6, "excited").fx(48.6, ("bulb",)))


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


def _shot_e1(ctx, t):
    u = t - 44.5
    film.sky(ctx, [(0, "#1E2A4A"), (0.55, "#9A6A72"), (0.7, "#E8A070"), (1, "#3A2A2A")])
    film.moon(ctx, 1500, 300, 50, 0.5, 1.0, glow_a=0.45)
    label(ctx, "月亮", 1500, 390, 28, "#FFF0D8", smooth(prog(u, 3.6, 4.2)), "serif_sb")
    film.ridge(ctx, -50, W + 50, 760, 70, 0.003, 31.0, "#2A1E26", 1.0, step=16)
    ctx.move_to(-50, H + 50)
    ctx.line_to(-50, 880)
    ctx.curve_to(500, 820, 1300, 840, W + 50, 900)
    ctx.line_to(W + 50, H + 50)
    ctx.close_path()
    setc(ctx, "#1A1418")
    ctx.fill()
    _tree(ctx, 820, 880, 1.15, "#140E12")
    # 苹果：挂在树上 → 落下砸中 Claude
    ax, ay0 = 1020, 560
    fall = clamp((u - 1.6) / 1.2)
    ay = ay0 + (720 - ay0) * fall ** 2
    if u < 2.85:
        if fall > 0:
            for k in range(1, 4):
                f2 = clamp(fall - k * 0.05)
                dashed(ctx, ax, ay0 + (720 - ay0) * f2 ** 2 - 6, ax, ay, 3, "#FFE2A8", 0.15)
        with at(ctx, ax, ay, 0.4):
            draw_prop(ctx, ("apple",), t)
    else:
        bx = ax + 120 * ease_out(clamp((u - 2.85) / 0.8))
        by = 780 + 80 * ease_out(clamp((u - 2.85) / 0.8)) - math.sin(clamp((u - 2.85) / 0.8) * math.pi) * 70
        with at(ctx, bx, by, 0.4, (u - 2.85) * 4):
            draw_prop(ctx, ("apple",), t)
    # 从苹果到月亮：同一种力
    lk = smooth(prog(u, 4.0, 5.0))
    if lk > 0:
        dashed(ctx, ax + 60, 700, 1450, 330, 3, "#FFD27A", 0.7 * lk, (14, 10), -t * 30)
        label(ctx, "同一种力：引力", 1260, 560, 38, "#FFD27A", lk, "serif_k")
    with lit("#FFB0A0", 0.3, 0.75):
        N5.draw(ctx, t)
    film.vignette(ctx, 0.55)


def _shot_e2(ctx, t):
    u = t - 50.5
    ctx.set_source(rad(960, 560, 0, 1300, [(0, "#0E1428"), (1, "#020308")]))
    ctx.paint()
    film.star_field(ctx, t, 160, 71, a=0.6)
    ex, ey, R0 = 820, 640, 230
    glow(ctx, ex, ey, 360, "#6FA0FF", 0.25)
    circle(ctx, ex, ey, R0)
    ctx.set_source(rad(ex - 60, ey - 60, 10, R0, [(0, "#8FC0FF"), (1, "#2A4A8A")]))
    ctx.fill()
    # 山与大炮
    poly(ctx, [(ex - 50, ey - R0 + 6), (ex, ey - R0 - 70), (ex + 50, ey - R0 + 6)])
    setc(ctx, "#4A3A2A")
    ctx.fill()
    top = (ex, ey - R0 - 70)
    speeds = [0.35, 0.55, 0.75, 1.0]
    for i, v in enumerate(speeds):
        k = ease_io(prog(u, 0.3 + i * 0.7, 1.0 + i * 0.7))
        if k <= 0:
            continue
        pts = []
        if v < 1.0:
            # 抛物线式下落，最终落回地面
            for j in range(80):
                th = j / 79 * (v * 2.2)
                r = (R0 + 70) * (1 - (th / (v * 2.2)) ** 2 * (70 / (R0 + 70)) - 0.0)
                rr = R0 + 70 - 70 * (th / (v * 2.2)) ** 1.6
                pts.append((ex + math.sin(th) * rr, ey - math.cos(th) * rr))
        else:
            pts = [(ex + math.sin(th) * (R0 + 70), ey - math.cos(th) * (R0 + 70)) for th in [j / 120 * TAU for j in range(121)]]
        seg = polyline_partial(pts, k)
        stroke_pts(ctx, seg, 4, "#FFD27A" if v == 1 else "#FFB07A", 0.9)
        if seg:
            circle(ctx, seg[-1][0], seg[-1][1], 9)
            setc(ctx, "#FFFFFF")
            ctx.fill()
    # 月亮的轨道
    mk = smooth(prog(u, 3.3, 4.0))
    if mk > 0:
        ctx.set_line_width(2)
        setc(ctx, "#C9D6FF", 0.5 * mk)
        circle(ctx, ex, ey, 520)
        ctx.stroke()
        ang = -0.6 + u * 0.25
        film.moon(ctx, ex + math.cos(ang) * 520, ey + math.sin(ang) * 520, 30, 0.5, mk, glow_a=0.3)
    fk = smooth(prog(u, 1.2, 2.0))
    label(ctx, "F = G · m₁m₂ / r²", 1520, 470, 58, "#FFE8C0", fk, "latin")
    label(ctx, "万有引力定律", 1520, 545, 34, "#D9C49A", fk, "serif_sb")
    label(ctx, "速度够快，炮弹就永远\"落\"不到地面——变成卫星", 1520, 640, 26, "#CDBA92", smooth(prog(u, 2.8, 3.4)),
          "serif_r")
    film.vignette(ctx, 0.5)


# ================================================================ 主绘制


def draw(ctx, t):
    if t < 9.5:
        _shot_a(ctx, t)
    elif t < 13.0:
        _shot_b1(ctx, t)
    elif t < 17.5:
        _shot_b2(ctx, t)
    elif t < 23.5:
        _shot_b3(ctx, t)
    elif t < 33.5:
        _shot_c(ctx, t)
    elif t < 38.5:
        _shot_d1(ctx, t)
    elif t < 44.5:
        _shot_d2(ctx, t)
    elif t < 50.5:
        _shot_e1(ctx, t)
    else:
        _shot_e2(ctx, t)


def sfx():
    out = [
        (0.0, "ambience_room", {"dur": 9.5, "gain": 0.45}),
        (0.3, "page", {"gain": 0.3}),
        (3.6, "zoom_in", {"dur": 3.0, "gain": 0.25}),
        (6.0, "shimmer", {"dur": 2.5, "gain": 0.2}),
        (9.5, "ambience_night", {"dur": 3.5, "gain": 0.4}),
        (10.6, "brass", {"gain": 0.35}),
        (13.0, "brass", {"gain": 0.3}), (13.1, "ambience_space", {"dur": 10.5, "gain": 0.4}),
        (14.4, "brass", {"gain": 0.2}),
    ]
    for i in range(4):
        out.append((17.5 + i * 1.45, "tick", {"gain": 0.25}))
        out.append((17.6 + i * 1.45, "quill", {"dur": 0.6, "gain": 0.2}))
    out += [(23.5, "ambience_room", {"dur": 10.0, "gain": 0.4}), (23.6, "quill", {"dur": 2.0, "gain": 0.2}),
            (27.3, "brass", {"gain": 0.25}), (27.8, "heartbeat", {"n": 2, "gain": 0.35}),
            (30.5, "shimmer", {"dur": 1.8, "gain": 0.2}),
            (33.5, "ambience_room", {"dur": 5.0, "gain": 0.4}), (33.9, "slide", {"gain": 0.2})]
    for k in range(1, 5):
        out.append((33.9 + k * 0.9, "ding", {"gain": 0.3, "pitch": 1 + k * 0.05}))
    out += [(38.5, "ambience_room", {"dur": 6.0, "gain": 0.4}), (38.7, "stamp", {"gain": 0.35}),
            (41.6, "thud", {"gain": 0.25}), (42.0, "thud", {"gain": 0.22}), (42.4, "thud", {"gain": 0.2}),
            (44.5, "ambience_birds", {"dur": 6.0, "gain": 0.35}), (44.5, "ambience_wind", {"dur": 6.0, "gain": 0.25}),
            (46.1, "whoosh_short", {"gain": 0.15}), (47.3, "bonk" if False else "thump", {"gain": 0.55}),
            (47.35, "boing", {"gain": 0.25}), (48.6, "ding", {"gain": 0.3}),
            (50.5, "ambience_space", {"dur": 7.5, "gain": 0.4}),
            (50.8, "whoosh_short", {"gain": 0.18}), (51.5, "whoosh_short", {"gain": 0.18}),
            (52.2, "whoosh_short", {"gain": 0.18}), (52.9, "whoosh", {"dur": 1.5, "gain": 0.2}),
            (54.2, "swell", {"dur": 2.5, "gain": 0.25}), (56.0, "steam", {"dur": 2.0, "gain": 0.25})]
    return out
