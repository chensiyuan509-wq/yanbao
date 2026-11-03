"""第六章 蒸汽与电：卢瑟堡《夜色中的煤溪谷》；蒸汽机原理剖面（纽科门 → 瓦特独立冷凝器）配真实版画；
真实的"火箭号"机车；卫星图上科学中心的迁移；法拉第讲座与感应线圈；麦克斯韦与赫兹（蓝图风格）；
电气革命六件真实展品（发电机、电话、电灯、电力机车、交流电、无线电）；周期表的预言。关键词：预言。"""
import math

from ..core import (TAU, H, W, arrow, at, circle, clamp, dashed, ease_in, ease_io, ease_out, ellipse, glow, lerp,
                    lin, mix, poly, polyline_partial, prog, rad, rng, rrect, setc, smooth, stroke_pts, text)
from .. import film, oldmap
from ..archive import caption, framed, kb, show
from ..exhibit import blueprint_bg, card, panel
from ..charts import arc_pts
from .common import arch, claude, label, lit, role, sequence

DUR = 66.0
CHAPTER = dict(num="第 六 章", title="蒸汽与电", era="1712 — 1901 年", key="预言", at=0.4, dur=4.0)
GRAIN = 0.07

VO = [
    (4.6, "18 世纪，煤和铁点燃了{工业革命}。"),
    (6.8, "纽科门蒸汽机：往汽缸里喷冷水，蒸汽凝结，大气把活塞{压下去}；"),
    (10.6, "可每次都得把冷下来的汽缸重新烧热，非常费煤。"),
    (13.4, "1769 年，瓦特加了{独立冷凝器}：汽缸一直热着，省煤约四分之三。"),
    (17.4, "他又把往复运动变成{旋转}，配上离心调速器，驱动整座工厂；"),
    (20.8, "1830 年，蒸汽机车跑上铁路——功率单位'{瓦特}'由他得名。"),
    (24.4, "科学的中心也在迁移：意大利、英国、法国、德国，再到美国。"),
    (29.4, "1831 年，法拉第发现{电磁感应}：磁场一变，就产生电流——"),
    (33.0, "这是所有发电机的原理。"),
    (35.4, "麦克斯韦用一组方程统一电与磁，算出电磁波的速度正是{光速}；"),
    (39.2, "1887 年，赫兹在实验室证实了它。"),
    (41.4, "随后，{电气革命}改变了每个人的生活："),
    (44.0, "发电机把机械能变成电能；1876 年{电话}，1879 年实用的{电灯}；"),
    (48.6, "电动机拉动了电车；交流电把电送到几十公里外；"),
    (52.8, "1901 年，{无线电}越过大西洋，海上从此有了救命的电波。"),
    (57.2, "电，成了现代文明的血液。"),
    (60.2, "化学也学会了预言：门捷列夫的周期表留下空位，镓、钪、锗随后{一一被找到}。", {"spill": 0.5}),
]

SUPERS = []

# ================================================================ A：煤溪谷之夜（0–5.2）


def _a(ctx, t):
    arch(ctx, t, "coalbrookdale", 0.0, 6.0, (0.52, 0.48, 1.08), (0.6, 0.46, 1.35), "卢瑟堡《夜色中的煤溪谷》",
         "1801 年 · 油画 · 伦敦科学博物馆 · 公有领域", cap=(4.4, 5.6))
    film.embers(ctx, t, 1150, 700, 30, 3, spread=600, height=700, color="#FFB04A", a=0.6, size=3, speed=0.3)


# ================================================================ B：蒸汽机剖面（5.2–17）


def _engine(ctx, t, u, watt):
    """蒸汽机剖面动画。u：本镜头内时间；watt：0..1 从纽科门过渡到瓦特。"""
    x0, y0 = 620, 560
    INK, PAPER = "#E8F2FF", "#7FC8FF"
    period = 1.8
    ph = (u % period) / period
    # 活塞位置：吸汽时上升，凝结后被大气压下
    if ph < 0.45:
        py = lerp(120, -110, ease_io(ph / 0.45))
    elif ph < 0.6:
        py = -110
    else:
        py = lerp(-110, 120, ease_in((ph - 0.6) / 0.4))
    spray = 0.45 <= ph < 0.75
    heat_cyl = 1.0 if watt > 0.5 else (0.25 if ph >= 0.5 else lerp(0.25, 1.0, clamp(ph / 0.45)))
    # 锅炉与火
    bx, by = x0 - 330, y0 + 170
    rrect(ctx, bx - 120, by - 80, 240, 160, 30)
    setc(ctx, "#0E2440")
    ctx.fill_preserve()
    ctx.set_line_width(4)
    setc(ctx, INK)
    ctx.stroke()
    ctx.rectangle(bx - 104, by - 10, 208, 74)
    setc(ctx, "#2A6AB0", 0.8)
    ctx.fill()
    film.fire(ctx, bx, by + 140, 70, t, 1.0, seed=4.0, glow_a=0.6)
    label(ctx, "锅炉", bx, by - 110, 28, INK, 1.0, "serif_sb")
    # 管道
    stroke_pts(ctx, [(bx + 30, by - 80), (bx + 30, y0 + 40), (x0 - 70, y0 + 40)], 14, "#3A5A80")
    stroke_pts(ctx, [(bx + 30, by - 80), (bx + 30, y0 + 40), (x0 - 70, y0 + 40)], 4, INK)
    # 汽缸
    cx0, cy0, cw, chh = x0 - 70, y0 - 200, 140, 300
    cyl_col = mix("#2A6AB0", "#FF7A3A", heat_cyl)
    rrect(ctx, cx0 - 12, cy0 - 12, cw + 24, chh + 24, 10)
    setc(ctx, cyl_col, 0.85)
    ctx.fill()
    rrect(ctx, cx0, cy0, cw, chh, 6)
    setc(ctx, "#0A1A30")
    ctx.fill()
    steam_h = y0 + 100 - (y0 - 50 + py) - 10
    if ph < 0.6 or watt > 0.5:
        ctx.rectangle(cx0, y0 - 50 + py + 20, cw, max(0, steam_h))
        setc(ctx, "#F2F6FF", 0.55 if not spray or watt > 0.5 else 0.25)
        ctx.fill()
    if spray and watt < 0.5:
        R = rng(int(u * 30))
        for i in range(26):
            setc(ctx, "#7FD8FF", 0.9)
            circle(ctx, cx0 + R.uniform(10, cw - 10), cy0 + chh * 0.4 + R.uniform(0, chh * 0.55), 4)
            ctx.fill()
        label(ctx, "喷冷水 → 蒸汽凝结 → 真空", x0 + 330, y0 - 80, 28, "#7FD8FF", 1.0, "serif_sb")
    # 活塞与活塞杆、横梁
    pyy = y0 - 50 + py
    rrect(ctx, cx0 + 4, pyy, cw - 8, 22, 4)
    setc(ctx, "#C9D6E8")
    ctx.fill()
    rod_top = y0 - 400
    stroke_pts(ctx, [(x0, pyy), (x0, rod_top + (py + 110) * 0.3)], 10, "#C9D6E8")
    piv = (x0 + 260, y0 - 400)
    ang = (py + 0) / 900
    L = 300
    p1 = (piv[0] - math.cos(ang) * L, piv[1] - math.sin(ang) * L)
    p2 = (piv[0] + math.cos(ang) * L, piv[1] + math.sin(ang) * L)
    stroke_pts(ctx, [p1, p2], 22, "#3A5A80")
    stroke_pts(ctx, [p1, p2], 5, INK)
    poly(ctx, [(piv[0] - 30, piv[1] + 160), (piv[0], piv[1]), (piv[0] + 30, piv[1] + 160)])
    setc(ctx, "#3A5A80")
    ctx.fill()
    stroke_pts(ctx, [p2, (p2[0], y0 + 120)], 6, INK)
    label(ctx, "抽水", p2[0] + 50, y0 + 130, 26, INK, 1.0, "serif_r")
    if ph >= 0.6 and watt < 0.5:
        for dx in (-40, 0, 40):
            arrow(ctx, x0 + dx, cy0 - 120, x0 + dx, cy0 - 40, 4, "#FFD27A", 0.9)
        label(ctx, "大气压", x0 + 110, cy0 - 120, 26, "#FFD27A", 1.0, "serif_sb")
    # 瓦特：独立冷凝器
    if watt > 0:
        k = smooth(watt)
        kx, ky = x0 + 160, y0 + 120
        stroke_pts(ctx, [(x0 + 70, y0 + 80), (kx, y0 + 80), (kx, ky - 50)], 12, "#3A5A80", k)
        rrect(ctx, kx - 70, ky - 50, 140, 120, 14)
        setc(ctx, "#1E5AA0", 0.9 * k)
        ctx.fill_preserve()
        ctx.set_line_width(4)
        setc(ctx, "#7FD8FF", k)
        ctx.stroke()
        if spray:
            R = rng(int(u * 30) + 9)
            for i in range(16):
                circle(ctx, kx + R.uniform(-55, 55), ky + R.uniform(-35, 60), 4)
            setc(ctx, "#BFEFFF", k)
            ctx.fill()
        label(ctx, "独立冷凝器", kx, ky + 110, 30, "#7FD8FF", k, "serif_k")
        label(ctx, "汽缸始终保持高温", x0 - 0, cy0 - 50, 26, "#FFB070", k, "serif_sb")
    # 煤耗计
    mx, my = 160, 300
    rate = 1.0 if watt < 0.5 else 0.25
    label(ctx, "耗煤", mx + 90, my - 60, 28, INK, 1.0, "serif_sb")
    rrect(ctx, mx, my, 180, 360, 10)
    setc(ctx, "#0A1A30")
    ctx.fill_preserve()
    ctx.set_line_width(3)
    setc(ctx, INK, 0.6)
    ctx.stroke()
    lvl = 340 * (1.0 if watt < 0.5 else lerp(1.0, 0.25, smooth(clamp((watt - 0.5) * 2))))
    rrect(ctx, mx + 12, my + 350 - lvl, 156, lvl, 6)
    setc(ctx, "#FF8A4A", 0.85)
    ctx.fill()
    if watt > 0.6:
        label(ctx, "约 1/4", mx + 90, my + 400, 34, "#FFD27A", smooth((watt - 0.6) / 0.3), "serif_k")


WATT = (role(1060, 960, 0.36, "watt", "focused", seed=61.0, palette="coral", flip=True)
        .point(6.8, "r", 0.5, 50).arms_down(8.4).expr(10.6, "worried").fx(10.6, ("sweat",)).fx(12.0, ())
        .expr(13.4, "excited").fx(13.4, ("bulb",)).fx(14.6, ()).point(14.0, "r", 0.3, 60).arms_down(15.6))
VISITOR = (claude(-150, 975, 0.36, "wonder", seed=62.0).walk_to(41.4, 47.4, 1100, 975, stride=0.7)
           .look(47.5, 0.2, -0.9).walk_to(48.2, 54.0, 2100, 975, stride=0.7).look(54.0, 0.0, -0.9))


def _b(ctx, t):
    u = t - 5.2
    watt = smooth(prog(t, 12.8, 13.8))
    blueprint_bg(ctx, W, H, t)
    _engine(ctx, t, u, watt)
    with lit("#BFE0FF", 0.25, 0.95):
        WATT.draw(ctx, t)
    # 右侧：真实图纸（蓝图化）
    key = "newcomen" if t < 13.0 else "watt_section"
    a = smooth(prog(t, 5.6, 6.2)) if t < 13.0 else smooth(prog(t, 13.0, 13.6))
    X, Y, w, h = 1290, 170, 520, 560
    panel(ctx, X - 16, Y - 16, w + 32, h + 100, a, "#7FC8FF")
    show(ctx, key, (0.5, 0.5, 1.0 if key == "newcomen" else 1.25), (X, Y, w, h), a, grade="blueprint", fit="contain")
    title = "纽科门蒸汽机图解（1712 年的设计）" if key == "newcomen" else "瓦特双作用蒸汽机剖面（1782）"
    text(ctx, title, X + w / 2, Y + h + 46, 26, "#E8F2FF", a, "serif_sb")
    film.vignette(ctx, 0.45)


# ================================================================ C：旋转运动、机车（17–24）


def _c(ctx, t):
    if t < 20.6:
        arch(ctx, t, "watt_1782", 17.0, 20.6, (0.5, 0.48, 1.05), (0.62, 0.55, 1.5), "瓦特双作用蒸汽机说明书插图",
             "1782 年专利 · 美国国会图书馆 · 公有领域", grade="blueprint", cap=(0.2, 3.3))
        k = smooth(prog(t, 17.8, 18.4))
        panel(ctx, 1260, 200, 560, 230, k, "#7FC8FF")
        text(ctx, "行星齿轮：往复 → 旋转", 1540, 260, 32, "#E8F2FF", k, "serif_sb")
        text(ctx, "离心调速器：自动稳住转速", 1540, 320, 30, "#BFE0FF", k, "serif_r")
        text(ctx, "→ 纺织厂、面粉厂、炼铁厂", 1540, 380, 30, "#FFD27A", k, "serif_sb")
        return
    kb(ctx, "rocket_loco", t, 20.6, 24.0, (0.45, 0.55, 1.1), (0.4, 0.52, 1.3), grade="warm")
    film.vignette(ctx, 0.5)
    caption(ctx, "\"火箭号\"机车（1829 年原型的 1931 年复制品）", "芝加哥科学与工业博物馆 · CC0",
            smooth(prog(t, 20.8, 21.3)) * (1 - smooth(prog(t, 23.5, 23.9))))
    k = smooth(prog(t, 21.2, 21.8))
    panel(ctx, 1300, 180, 520, 200, k)
    text(ctx, "1829 年雨山试验 · 时速约 48 公里", 1560, 240, 28, "#F6EEDF", k, "serif_sb")
    text(ctx, "1830 年 利物浦—曼彻斯特铁路通车", 1560, 300, 28, "#D9B26A", k, "serif_sb")


# ================================================================ D：科学中心迁移（24–29）

MCAM6 = oldmap.MapCam([(24.0, (8.0, 47.0, 20)), (26.4, (2.0, 48.0, 16), ease_io), (29.0, (-32.0, 44.0, 8.0), ease_io)])


def _d(ctx, t):
    cam = MCAM6.at(t)
    oldmap.draw_satellite(ctx, cam, t, 1.0, "day", "natural", rivers=["danube", "rhine", "thames"])
    times = [24.3, 25.2, 26.0, 26.8, 27.8]
    prev = None
    for i, (nm, lon, lat, yrs) in enumerate(oldmap.CENTERS):
        k = smooth(prog(t, times[i], times[i] + 0.5))
        x, y = cam.xy(lon, lat)
        if prev is not None and k > 0:
            pts = arc_pts(prev, (x, y), 0.25)
            stroke_pts(ctx, polyline_partial(pts, ease_io(prog(t, times[i] - 0.3, times[i] + 0.5))), 4, "#FFD27A", 0.9,
                       dash=(14, 8), offset=-t * 40)
        if k > 0:
            glow(ctx, x, y, 60, "#FFC46B", 0.7 * k)
            circle(ctx, x, y, 9)
            setc(ctx, "#FFFFFF", k)
            ctx.fill()
            text(ctx, nm, x + 2, y - 44, 34, "#000000", 0.6 * k, "serif_k")
            text(ctx, nm, x, y - 46, 34, "#FFF4E0", k, "serif_k")
            text(ctx, yrs, x, y + 36, 24, "#FFD27A", k, "serif_sb")
        prev = (x, y)
    oldmap.sat_vignette(ctx, 0.6)
    caption(ctx, "近代科学中心的转移", "汤浅光朝统计 · 1962 年", smooth(prog(t, 24.4, 24.9)))


# ================================================================ E：法拉第、麦克斯韦（29–41）


def _e(ctx, t):
    if t < 35.0:
        arch(ctx, t, "faraday_lecture", 29.0, 35.0, (0.6, 0.55, 1.1), (0.7, 0.58, 1.6), "法拉第在英国皇家研究院讲课",
             "布莱克利绘 · 1856 年 · 公有领域", grade="warm", cap=(0.3, 5.4))
        k = smooth(prog(t, 31.0, 31.6))
        framed(ctx, "faraday_ring", 360, 420, 300, k)
        label(ctx, "法拉第的感应线圈（1831）", 360, 640, 26, "#FFE8C0", k, "serif_sb")
        return
    u = t - 35.0
    blueprint_bg(ctx, W, H, t)
    framed(ctx, "maxwell", 290, 400, 380, smooth(prog(u, 0.0, 0.5)))
    label(ctx, "麦克斯韦（1831—1879）", 290, 650, 26, "#E8F2FF", 1.0, "serif_sb")
    eqs = ["∇⋅E = ρ/ε₀", "∇⋅B = 0", "∇×E = −∂B/∂t", "∇×B = μ₀J + μ₀ε₀ ∂E/∂t"]
    for i, e in enumerate(eqs):
        text(ctx, e, 620, 230 + i * 70, 42, "#EDF4FF", smooth(prog(u, 0.2 + i * 0.25, 0.6 + i * 0.25)), "eq", "l")
    text(ctx, "c = 1/√(μ₀ε₀)", 620, 530, 36, "#FFD27A", smooth(prog(u, 1.4, 2.0)), "eq", "l")
    text(ctx, "≈ 每秒 30 万公里 = 光速", 900, 530, 34, "#FFD27A", smooth(prog(u, 1.6, 2.2)), "serif_sb", "l")
    wk = smooth(prog(u, 1.6, 2.2))
    head = 640 + 1100 * ease_io(prog(u, 1.8, 4.4))
    y0 = 760
    ptsE, ptsB = [], []
    x = 640
    while x < head:
        phs = (x - 640) * 0.022 - u * 6
        ptsE.append((x, y0 - math.sin(phs) * 100))
        ptsB.append((x, y0 + math.sin(phs) * 30))
        x += 6
    if len(ptsE) > 1:
        stroke_pts(ctx, ptsE, 5, "#FFD27A", wk)
        stroke_pts(ctx, ptsB, 5, "#7FC8FF", wk * 0.8)
    rx, ry = 1780, y0
    ctx.set_line_width(8)
    setc(ctx, "#C9A060")
    circle(ctx, rx, ry, 80)
    ctx.stroke()
    if head > rx - 90:
        q = (u * 7) % 1
        glow(ctx, rx - 80, ry, 70, "#BFE0FF", 0.9 * (1 - q))
        label(ctx, "1887 · 赫兹：火花跳了", rx - 100, ry - 130, 28, "#BFE0FF", smooth(prog(u, 4.2, 4.8)), "serif_sb")
    film.vignette(ctx, 0.45)


# ================================================================ F：电气革命六件展品（41–60）

EXHIBITS = [
    ("gramme", "1871 · 格拉姆", "发电机", ("机械能 → 电能", "电站的心脏"), (0.56, 0.6, 1.35)),
    ("bell_phone", "1876 · 贝尔", "电话", ("声音 → 电流 → 声音", "千里之外听见人声"), (0.5, 0.5, 1.0)),
    ("edison_bulb", "1879 · 爱迪生", "白炽灯", ("1882 年纽约珍珠街电站", "开始商业供电"), (0.5, 0.42, 1.25)),
    ("siemens_loco", "1879 · 西门子", "电力机车", ("电动机：电能 → 运动", "1881 年柏林开通电车"), (0.55, 0.6, 1.2)),
    ("tesla_lab", "1888 · 特斯拉", "交流电", ("变压器升压，远距离输电", "1896 年尼亚加拉电送 40 公里"), (0.5, 0.5, 1.05)),
    ("marconi_room", "1901 · 马可尼", "无线电", ("电波横跨大西洋", "海上求救从此有了电波"), (0.45, 0.55, 1.1)),
]
NIGHT = oldmap.MapCam([(41.0, (-35.0, 38.0, 7.5)), (60.0, (15.0, 40.0, 8.5))])


def _f(ctx, t):
    u = t - 41.0
    cam = NIGHT.at(t)
    oldmap.draw_satellite(ctx, cam, t, 1.0, "night", "natural", coast=0.15, grid=0.05)
    ctx.set_source_rgba(0.02, 0.03, 0.06, 0.45)
    ctx.paint()
    pan = ease_io(prog(u, 6.6, 9.4))
    pitch = 600
    for i, (key, year, title, lines, crop) in enumerate(EXHIBITS):
        x = 360 + i * pitch - pan * 3 * pitch
        if x < -400 or x > W + 400:
            continue
        k = clamp((u - (0.3 + i * 0.45 if i < 3 else 7.2 + (i - 3) * 0.45)) / 0.6)
        hot_t = [3.0, 3.8, 4.8, 8.0, 9.6, 11.8][i]
        hot = smooth(prog(u, hot_t, hot_t + 0.4)) * (1 - smooth(prog(u, hot_t + 2.4, hot_t + 2.9)))
        card(ctx, key, x, 500, 500, 640, year, title, lines, 1.0, k, crop, t, hot)
    with lit("#BFD0FF", 0.3, 0.85):
        VISITOR.draw(ctx, t)
    film.vignette(ctx, 0.5)
    text(ctx, "电气革命 · 第二次工业革命", 960, 150, 30, "#D9B26A", smooth(prog(u, 0.0, 0.6)) * (1 - smooth(prog(u, 17.4, 18.4))),
         "serif_sb")


# ================================================================ G：周期表的预言（60–66）

TABLE = [
    [("H", 1)] + [None] * 16 + [("He", 18)],
    [("Li", 1), ("Be", 2)] + [None] * 10 + [("B", 13), ("C", 14), ("N", 15), ("O", 16), ("F", 17), ("Ne", 18)],
    [("Na", 1), ("Mg", 2)] + [None] * 10 + [("Al", 13), ("Si", 14), ("P", 15), ("S", 16), ("Cl", 17), ("Ar", 18)],
    [(s, i + 1) for i, s in enumerate(["K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge",
                                       "As", "Se", "Br", "Kr"])],
    [(s, i + 1) for i, s in enumerate(["Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
                                       "Sb", "Te", "I", "Xe"])],
]
GAPS = {"Ga": ("类铝", "1875", 62.6), "Sc": ("类硼", "1879", 63.2), "Ge": ("类硅", "1886", 63.8)}


def _g(ctx, t):
    u = t - 60.0
    ctx.set_source(rad(960, 560, 0, 1300, [(0, "#22201E"), (1, "#0A0908")]))
    ctx.paint()
    film.paint_texture(ctx, "paper", 0, 0, W, H, 0.1)
    cw, ch = 74, 82
    x0, y0 = 360, 230
    for r_, row in enumerate(TABLE):
        for c_, el in enumerate(row):
            if not el:
                continue
            sym = el[0]
            x, y = x0 + c_ * cw, y0 + r_ * ch
            k = smooth(prog(u, 0.05 + (r_ * 18 + c_) * 0.008, 0.3 + (r_ * 18 + c_) * 0.008))
            gap = GAPS.get(sym)
            found = gap and t >= gap[2]
            if gap and not found:
                rrect(ctx, x + 4, y + 4, cw - 8, ch - 8, 8)
                ctx.set_line_width(3)
                ctx.set_dash((8, 6))
                setc(ctx, "#FFD27A", k)
                ctx.stroke()
                ctx.set_dash(())
                text(ctx, "?", x + cw / 2, y + ch / 2 - 8, 40, "#FFD27A", k, "serif_k")
                text(ctx, gap[0], x + cw / 2, y + ch - 18, 16, "#FFD27A", k, "serif_r")
                continue
            pk = 1.0
            if found:
                q = t - gap[2]
                pk = 1 + 0.25 * math.exp(-q * 4) * math.sin(q * 20)
                glow(ctx, x + cw / 2, y + ch / 2, 80, "#FFD27A", 0.6 * math.exp(-q * 1.5))
            ctx.save()
            ctx.translate(x + cw / 2, y + ch / 2)
            ctx.scale(pk, pk)
            rrect(ctx, -cw / 2 + 4, -ch / 2 + 4, cw - 8, ch - 8, 8)
            setc(ctx, "#A8781E" if found else ("#3A5A7A" if c_ < 2 else ("#7A5A3A" if c_ >= 12 else "#4A4A5A")), 0.9 * k)
            ctx.fill()
            text(ctx, sym, 0, -6, 30, "#F4EEE2", k, "latin_b")
            if found:
                text(ctx, gap[1], 0, 24, 16, "#FFF0D0", 1, "latin")
            ctx.restore()
    k = smooth(prog(u, 2.6, 3.2))
    panel(ctx, 400, 720, 1120, 150, k)
    text(ctx, "门捷列夫预言\"类铝\"：原子量 ≈ 68　密度 ≈ 5.9", 960, 770, 30, "#E8DCC4", k, "serif_r")
    text(ctx, "1875 年发现的镓：原子量 69.7　密度 5.9", 960, 825, 30, "#FFD27A", smooth(prog(u, 3.0, 3.6)), "serif_sb")
    text(ctx, "1869 · 元素周期表（示意）", 960, 170, 34, "#F4E6C8", smooth(prog(u, 0.2, 0.7)), "serif_k")
    film.vignette(ctx, 0.55)


SHOTS = [(0.0, _a), (5.2, _b), (17.0, _c), (24.0, _d), (29.0, _e), (41.0, _f), (60.0, _g)]
TRANS = {1: ("dissolve", 1.0), 2: ("lightsweep", 1.0, {"angle": -0.4, "color": "#BFE0FF"}),
         3: ("zoomblur", 0.8, {"x": 960, "y": 540}), 4: ("luma", 1.2), 5: ("lightsweep", 1.0, {"angle": 0.4}),
         6: ("dissolve", 1.0)}


def draw(ctx, t):
    sequence(ctx, t, SHOTS, TRANS)


def sfx():
    return [
        (0.0, "ambience_engine", {"dur": 5.4, "rate": 1.0, "gain": 0.45}), (0.0, "ambience_fire", {"dur": 5.4, "gain": 0.35}),
        (5.2, "ambience_engine", {"dur": 12.0, "rate": 0.56, "gain": 0.6}),
        (6.4, "steam", {"dur": 1.2, "gain": 0.3}), (8.2, "steam", {"dur": 1.2, "gain": 0.3}), (10.0, "steam", {"dur": 1.2, "gain": 0.3}),
        (13.0, "shimmer", {"dur": 1.5, "gain": 0.18}),
        (17.0, "gears_run", {"dur": 3.6, "gain": 0.3}), (20.6, "ambience_engine", {"dur": 3.4, "rate": 2.0, "gain": 0.6}),
        (21.0, "steam", {"dur": 1.6, "gain": 0.4}),
        (24.0, "whoosh", {"dur": 2.0, "gain": 0.2}), (24.3, "pin", {"gain": 0.25}), (25.2, "pin", {"gain": 0.25}),
        (26.0, "pin", {"gain": 0.25}), (26.8, "pin", {"gain": 0.25}), (27.8, "pin", {"gain": 0.28}),
        (29.0, "ambience_room", {"dur": 6.0, "gain": 0.4}), (31.2, "zap", {"dur": 0.6, "gain": 0.15}),
        (35.0, "hum", {"dur": 6.0, "gain": 0.18}), (35.2, "chalk", {"dur": 1.4, "gain": 0.25}), (38.6, "crackle", {"dur": 2.4, "gain": 0.3}),
        (41.0, "ambience_city", {"dur": 19.0, "gain": 0.45}), (41.0, "hum", {"dur": 19.0, "gain": 0.12}),
        (44.0, "zap", {"dur": 0.4, "gain": 0.12}), (44.4, "telegraph", {"dur": 1.6, "gain": 0.2}),
        (45.6, "ding", {"gain": 0.2}), (48.2, "whoosh", {"dur": 2.8, "gain": 0.18}), (52.8, "telegraph", {"dur": 2.4, "gain": 0.25}),
        (55.2, "crackle", {"dur": 1.0, "gain": 0.2}),
        (60.0, "ambience_room", {"dur": 6.0, "gain": 0.35}), (62.6, "ding", {"gain": 0.3}), (63.2, "ding", {"gain": 0.3, "pitch": 1.1}),
        (63.8, "ding", {"gain": 0.3, "pitch": 1.2}),
    ]
