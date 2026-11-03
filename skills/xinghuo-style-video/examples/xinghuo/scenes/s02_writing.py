"""第二章 文字与数：精确地图上四条大河亮起；大都会博物馆的楔形文字账目泥板；第一视角压楔形字讲六十进制；
普林顿 322 号泥板上的勾股数；莱因德数学纸草书与 π≈3.16；麦纳墓壁画里的拉绳丈量；罗伯茨笔下的金字塔；
商代卜骨；敦煌星图；立竿测影与二十四节气。关键词：记录。"""
import math
import os

from ..core import (TAU, H, W, at, circle, clamp, ease_io, ease_out, glow, lerp, lin, mix, poly, polyline_partial,
                    prog, rad, rrect, setc, smooth, stroke_pts, text)
from .. import film, oldmap
from ..archive import DIR, caption, kb, show
from .common import arch, label, lit, sequence

DUR = 44.0
CHAPTER = dict(num="第 二 章", title="文字与数", era="约公元前 3500 年 — 公元前 100 年", key="记录", at=0.4, dur=4.0)
GRAIN = 0.09

VO = [
    (4.4, "大河两岸，最早的城市和{文字}出现了。"),
    (7.3, "苏美尔人在泥板上{记账}：几只羊、几袋麦。"),
    (10.7, "他们用 {60 进制}：今天的 60 分钟、360 度，都源于此。"),
    (14.7, "3800 年前的泥板上，列着{勾股数}："),
    (17.4, "119、120、169——比毕达哥拉斯早一千多年。"),
    (20.4, "埃及的《莱因德纸草书》里，有 80 多道数学题："),
    (23.4, "直径 9 的圆 ≈ 边长 8 的正方形，于是 {π ≈ 3.16}。"),
    (26.6, "尼罗河年年泛滥，田界要重新丈量——{几何}由此萌芽；"),
    (30.0, "大金字塔四边，几乎{正对东南西北}。"),
    (33.4, "商代甲骨上，刻着{日食和月食}的记录；"),
    (36.4, "敦煌星图画了 1300 多颗星，是现存最古老的星图之一；"),
    (40.0, "中国人立竿测影，定出了{二十四节气}。", {"spill": 0.5}),
]

SUPERS = []

# ================================================================ A：四条大河（0–7）

MCAM = oldmap.MapCam([(0.0, (31.5, 27.0, 26)), (2.6, (40.0, 31.0, 22), ease_io), (4.4, (70.0, 31.0, 14), ease_io),
                      (7.0, (75.0, 31.0, 9.6), ease_io)])
RIVERS_A = [("nile", 0.2, "古埃及", "约前 3100 年", (24.5, 22.0)),
            ("euphrates", 1.6, "美索不达米亚", "约前 3500 年", (47.5, 37.0)), ("tigris", 1.8, None, None, None),
            ("indus", 3.2, "古印度", "约前 2600 年", (62.0, 31.5)),
            ("yellow", 4.2, "古代中国", "约前 2000 年", (106.0, 42.0)), ("yangtze", 4.6, None, None, None)]


def _shot_a(ctx, t):
    cam = MCAM.at(t)
    rp = {name: ease_io(prog(t, t0, t0 + 1.6)) for name, t0, *_ in RIVERS_A}
    oldmap.draw_satellite(ctx, cam, t, 1.0, "day", "warm", coast=0.18, grid=0.05)
    for name, t0, title, sub, pos in RIVERS_A:
        p = rp[name]
        if p <= 0:
            continue
        for line in oldmap.river_lines(name):
            seg = polyline_partial(cam.pts(line), p)
            stroke_pts(ctx, seg, 26, "#FFC76A", 0.22 * p)
            stroke_pts(ctx, seg, 5, "#FFD98A", 0.95)
        if title:
            x, y = cam.xy(*pos)
            a = smooth(prog(t, t0 + 0.6, t0 + 1.2))
            label(ctx, title, x, y, 44 if cam.k > 15 else 34, "#FFF2DC", a, "serif_k", sub=sub, sub_color="#F0D2A0")
    for (nm, t0) in (("孟菲斯", 0.8), ("乌鲁克", 2.0), ("摩亨佐-达罗", 3.6), ("安阳", 4.8)):
        oldmap.city_sat(ctx, cam, nm, smooth(prog(t, t0, t0 + 0.5)), 1.0, size=26, t=t)
    oldmap.sat_vignette(ctx, 0.6)
    film.grade(ctx, "#FFB070", 0.08)


# ================================================================ B：泥板（7–20）


def _shot_b1(ctx, t):
    arch(ctx, t, "cuneiform_barley", 7.0, 10.6, (0.5, 0.5, 1.05), (0.42, 0.52, 1.35), "楔形文字泥板：大麦分配账目",
         "美索不达米亚 · 约公元前 3100 年 · 大都会博物馆 · CC0", cap=(0.3, 3.3))
    k = smooth(prog(t, 8.2, 8.8))
    label(ctx, "账目 · 印章 · 数字", 1500, 210, 34, "#FFE8C0", k * (1 - smooth(prog(t, 10.2, 10.6))), "serif_sb")


def _imp(ctx, s, x, y, size, a=1.0):
    text(ctx, s, x + 2, y + 2.5, size, "#F4D2A6", 0.55 * a, "cune", "l")
    text(ctx, s, x, y, size, "#5A3418", 0.92 * a, "cune", "l")


def _shot_b2(ctx, t):
    """第一视角：用芦苇笔压出 1、10，再讲"逢六十进一"。"""
    u = t - 10.6
    lampk = film.flicker(t, 8.0, 0.12)
    ctx.set_source(rad(500, 300, 0, 1500, [(0, "#3A2414"), (0.5, "#1C110A"), (1, "#080503")]))
    ctx.paint()
    glow(ctx, 240, 420, 700, "#FFA850", 0.35 * lampk)
    x, y, w, h = 900, 560, 980, 600
    bx, by = x - w / 2, y - h / 2
    rrect(ctx, bx + 14, by + 26, w, h, 60)
    setc(ctx, "#000000", 0.45)
    ctx.fill()
    rrect(ctx, bx, by, w, h, 60)
    ctx.set_source(lin(0, by, 0, by + h, [(0, "#D9A878"), (1, "#9A6A42")]))
    ctx.fill()
    film.paint_texture(ctx, "clay", bx, by, w, h, 0.55, clip_path=lambda c: rrect(c, bx, by, w, h, 60))
    x0, y0 = bx + 70, by + 120
    a1 = smooth(prog(u, 0.1, 0.4))
    _imp(ctx, "𒁹", x0, y0, 120, a1)
    label(ctx, "= 1", x0 + 100, y0 + 6, 44, "#FFF0D8", a1, "serif_sb", align="l")
    a2 = smooth(prog(u, 0.6, 0.9))
    _imp(ctx, "𒌋", x0 + 330, y0, 120, a2)
    label(ctx, "= 10", x0 + 420, y0 + 6, 44, "#FFF0D8", a2, "serif_sb", align="l")
    a3 = smooth(prog(u, 1.2, 1.6))
    _imp(ctx, "𒁹", x0, y0 + 200, 120, a3)
    _imp(ctx, "𒁹", x0 + 210, y0 + 200, 120, a3)
    label(ctx, "= 1×60 + 1 = 61", x0 + 320, y0 + 206, 44, "#FFF0D8", a3, "serif_sb", align="l")
    label(ctx, "逢六十进一位", x0 + 350, y0 + 290, 32, "#F6D6A8", a3, "serif_r", align="l")
    dk = smooth(prog(u, 2.0, 2.6))
    if dk > 0:
        cx, cy, r = 1630, 560, 170
        ctx.set_line_width(3)
        setc(ctx, "#FFE2A8", 0.9 * dk)
        circle(ctx, cx, cy, r)
        ctx.stroke()
        for i in range(60):
            ang = i / 60 * TAU - math.pi / 2
            L = 24 if i % 5 == 0 else 10
            ctx.move_to(cx + math.cos(ang) * r, cy + math.sin(ang) * r)
            ctx.line_to(cx + math.cos(ang) * (r - L), cy + math.sin(ang) * (r - L))
        ctx.stroke()
        hand = u * 1.4
        ctx.set_line_width(5)
        ctx.move_to(cx, cy)
        ctx.line_to(cx + math.cos(hand - math.pi / 2) * r * 0.8, cy + math.sin(hand - math.pi / 2) * r * 0.8)
        ctx.stroke()
        label(ctx, "60 分 · 60 秒 · 360°", cx, cy + r + 50, 32, "#FFE2A8", dk, "serif_sb")
    pen = (x0 + 60 + (330 if u > 0.5 else 0), y0 + 20) if u < 1.0 else ((x0 + 60 + (210 if u > 1.4 else 0)), y0 + 220)
    if u > 1.9:
        pen = (1400, 860)
    bob = math.sin(t * 1.4) * 6
    with lit("#FFA860", 0.5, 0.8 + 0.2 * lampk):
        tip = (pen[0] + 200, pen[1] + 230 + bob)
        film.pov_arm(ctx, (1700, 1400), tip, 140)
        ctx.save()
        ctx.translate(tip[0] - 40, tip[1] - 40)
        ctx.rotate(-2.3)
        rrect(ctx, -10, -8, 330, 16, 8)
        ctx.set_source(lin(0, -8, 0, 8, [(0, "#E8D29A"), (1, "#9A8044")]))
        ctx.fill()
        ctx.restore()
    film.vignette(ctx, 0.65)


def _shot_b3(ctx, t):
    """普林顿 322 号泥板（真实照片）+ 勾股数标注。"""
    u = t - 14.6
    ctx.set_source_rgb(0.06, 0.05, 0.05)
    ctx.paint()
    to = kb(ctx, "plimpton", t, 14.6, 20.0, (0.5, 0.5, 0.92), (0.42, 0.36, 1.25), rect=(0, 0, W, H), fit="cover")
    film.vignette(ctx, 0.55)
    hk = smooth(prog(u, 1.0, 1.6))
    if to and hk > 0:
        x0, y0 = to(0.08, 0.15)
        x1, y1 = to(0.97, 0.235)
        rrect(ctx, x0, y0, x1 - x0, y1 - y0, 12)
        setc(ctx, "#FFD27A", 0.18 * hk)
        ctx.fill_preserve()
        ctx.set_line_width(5)
        setc(ctx, "#FFD27A", hk)
        ctx.stroke()
    # 右侧解释卡
    k = smooth(prog(u, 2.2, 2.8))
    if k > 0:
        cx, cy = 1490, 640
        rrect(ctx, cx - 300, cy - 230, 600, 460, 18)
        setc(ctx, "#120E0A", 0.82 * k)
        ctx.fill()
        ax, ay = cx - 200, cy + 150
        s = 1.25
        poly(ctx, [(ax, ay), (ax + 240 * s, ay), (ax + 240 * s, ay - 238 * s)])
        ctx.set_line_width(4)
        setc(ctx, "#FFE2A8", k)
        ctx.stroke()
        label(ctx, "120", ax + 120 * s, ay + 36, 32, "#FFF0D8", k, "latin_b")
        label(ctx, "119", ax + 240 * s + 46, ay - 119 * s, 32, "#FFF0D8", k, "latin_b")
        label(ctx, "169", ax + 100 * s - 30, ay - 140 * s, 32, "#FFD27A", k, "latin_b")
        label(ctx, "119² + 120² = 169²", cx, cy - 180, 40, "#FFD27A", smooth(prog(u, 3.0, 3.6)), "latin")
    caption(ctx, "普林顿 322 号泥板", "古巴比伦 · 约公元前 1800 年 · 哥伦比亚大学 · 公有领域",
            smooth(prog(u, 0.3, 0.9)) * (1 - smooth(prog(u, 4.9, 5.4))))


# ================================================================ C：埃及（20–33）


def _shot_c1(ctx, t):
    u = t - 20.0
    arch(ctx, t, "rhind", 20.0, 26.4, (0.35, 0.45, 1.08), (0.6, 0.5, 1.45), "莱因德数学纸草书",
         "古埃及 · 约公元前 1550 年 · 大英博物馆 · 公有领域", grade="warm", cap=(0.3, 6.0))
    k = smooth(prog(u, 3.2, 3.8))
    if k > 0:
        cx, cy = 1460, 520
        rrect(ctx, cx - 330, cy - 250, 660, 500, 18)
        setc(ctx, "#F2E8D2", 0.92 * k)
        ctx.fill()
        ox, oy = cx - 150, cy + 30
        R = 120
        circle(ctx, ox, oy, R)
        setc(ctx, "#C8372D", 0.75 * k)
        ctx.fill()
        sq = R * 2 * 8 / 9
        ctx.rectangle(ox - sq / 2, oy - sq / 2, sq, sq)
        ctx.set_line_width(5)
        setc(ctx, "#2457A8", k)
        ctx.stroke()
        label(ctx, "直径 9", ox, oy + R + 34, 28, "#1C1A18", k, "serif_sb", shadow=False)
        label(ctx, "边长 8", ox, oy - R - 30, 28, "#2457A8", k, "serif_sb", shadow=False)
        label(ctx, "面积相等", cx + 150, cy - 120, 34, "#1C1A18", k, "serif_sb", shadow=False)
        label(ctx, "π·(9/2)² ≈ 8²", cx + 150, cy - 40, 34, "#1C1A18", smooth(prog(u, 4.2, 4.8)), "eq", shadow=False)
        label(ctx, "π ≈ 256/81", cx + 150, cy + 40, 40, "#C8372D", smooth(prog(u, 4.8, 5.4)), "eq", shadow=False)
        label(ctx, "≈ 3.16", cx + 150, cy + 110, 40, "#C8372D", smooth(prog(u, 5.2, 5.8)), "eq", shadow=False)


def _shot_c2(ctx, t):
    u = t - 26.4
    key = "menna" if os.path.exists(os.path.join(DIR, "menna.jpg")) else "nebamun"
    if key == "menna":
        arch(ctx, t, "menna", 26.4, 30.0, (0.5, 0.5, 1.1), (0.55, 0.5, 1.35), "麦纳墓壁画：拉绳丈量农田",
             "古埃及第 18 王朝 · 约公元前 1400 年 · 公有领域", grade="warm", cap=(0.3, 3.3))
    else:
        arch(ctx, t, "nebamun", 26.4, 30.0, (0.5, 0.5, 1.05), (0.5, 0.42, 1.3), "内巴蒙墓壁画：尼罗河沼泽",
             "古埃及 · 约公元前 1350 年 · 大英博物馆 · 公有领域", grade="warm", cap=(0.3, 3.3))
    k = smooth(prog(u, 1.0, 1.6))
    rrect(ctx, 1200, 180, 620, 120, 14)
    setc(ctx, "#120E0A", 0.7 * k)
    ctx.fill()
    label(ctx, "geo（土地）+ metria（测量）", 1510, 222, 32, "#FFE8C0", k, "serif_sb")
    label(ctx, "= geometry 几何", 1510, 270, 32, "#FFD27A", k, "serif_sb")


def _shot_c3(ctx, t):
    u = t - 30.0
    arch(ctx, t, "pyramids_roberts", 30.0, 33.4, (0.45, 0.5, 1.08), (0.36, 0.42, 1.3), "大卫·罗伯茨《吉萨的狮身人面像与金字塔》",
         "1839 年 · 石版画 · 公有领域", cap=(0.2, 3.1))
    k = smooth(prog(u, 0.8, 1.4))
    if k > 0:
        cx, cy, s = 1560, 400, 130
        rrect(ctx, cx - 190, cy - 210, 380, 430, 18)
        setc(ctx, "#120E0A", 0.75 * k)
        ctx.fill()
        ctx.rectangle(cx - s / 2, cy - s / 2 + 30, s, s)
        setc(ctx, "#E2C08A", k)
        ctx.fill()
        poly(ctx, [(cx - s / 2, cy - s / 2 + 30), (cx, cy + 30), (cx + s / 2, cy - s / 2 + 30)])
        setc(ctx, "#C9A06A", k)
        ctx.fill()
        from ..core import arrow
        arrow(ctx, cx, cy - s / 2 + 10, cx, cy - 170, 4, "#FFD27A", k)
        label(ctx, "N", cx + 28, cy - 160, 28, "#FFD27A", k, "latin_b")
        label(ctx, "偏差约 4 角分", cx, cy + 150, 28, "#F2E2BC", k, "serif_sb")
        label(ctx, "（不到 0.1°）", cx, cy + 190, 24, "#CDBA92", k, "serif_r")


# ================================================================ D：中国（33–44）


def _shot_d1(ctx, t):
    arch(ctx, t, "oracle", 33.0, 36.4, (0.5, 0.5, 1.05), (0.5, 0.45, 1.45), "商代卜骨（牛肩胛骨）",
         "约公元前 1200 年 · 照片：CC0", grade="warm", cap=(0.3, 3.1))


def _shot_d2(ctx, t):
    arch(ctx, t, "dunhuang", 36.4, 40.0, (0.5, 0.5, 1.05), (0.45, 0.55, 1.5), "敦煌星图（局部）",
         "唐代 · 约 7 世纪 · 大英图书馆 · 公有领域", grade="warm", cap=(0.3, 3.3))
    k = smooth(prog(t, 37.4, 38.0))
    label(ctx, "1300 多颗星", 1560, 230, 44, "#FFE8C0", k, "serif_k")


TERMS = ["立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
         "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"]


def _shot_d3(ctx, t):
    u = t - 40.0
    ctx.set_source(rad(960, 540, 0, 1200, [(0, "#2A2016"), (1, "#0A0806")]))
    ctx.paint()
    film.paint_texture(ctx, "paper", 0, 0, W, H, 0.12)
    center = ease_io(prog(u, 2.2, 3.8))
    wx, wy, R0 = lerp(1240, 960, center), 540, 300
    gk = 1 - center
    if gk > 0.01:
        gx, gy = 330, 820
        rrect(ctx, gx - 12, gy - 320, 24, 320, 6)
        setc(ctx, "#6A4A2A", gk)
        ctx.fill()
        rrect(ctx, gx - 20, gy, 560, 26, 6)
        setc(ctx, "#8A6A42", gk)
        ctx.fill()
        L = 120 + 300 * (0.5 - 0.5 * math.cos(u * 2.0))
        rrect(ctx, gx, gy - 6, L, 12, 4)
        setc(ctx, "#140C06", 0.75 * gk)
        ctx.fill()
        label(ctx, "圭表：立竿测影", gx + 260, gy + 80, 32, "#F2D79B", gk, "serif_sb")
        label(ctx, "影子最短 → 夏至　最长 → 冬至", gx + 260, gy + 126, 26, "#E2D2B0", gk, "serif_r")
    ctx.set_line_width(4)
    setc(ctx, "#D9B26A", 0.9)
    circle(ctx, wx, wy, R0)
    ctx.stroke()
    ctx.set_line_width(1.5)
    circle(ctx, wx, wy, R0 - 70)
    ctx.stroke()
    sun_a = -math.pi / 2 + u * 1.2
    for i, nm in enumerate(TERMS):
        ang = -math.pi / 2 + i / 24 * TAU
        k = smooth(prog(u, 0.1 + i * 0.04, 0.4 + i * 0.04))
        ctx.set_line_width(3)
        setc(ctx, "#D9B26A", k)
        ctx.move_to(wx + math.cos(ang) * R0, wy + math.sin(ang) * R0)
        ctx.line_to(wx + math.cos(ang) * (R0 - 22), wy + math.sin(ang) * (R0 - 22))
        ctx.stroke()
        hot = max(0.0, math.cos(ang - sun_a)) ** 30
        text(ctx, nm, wx + math.cos(ang) * (R0 + 48), wy + math.sin(ang) * (R0 + 40), 26,
             mix("#E8D8B8", "#FFD27A", hot), k, "kai")
    film.sun(ctx, wx + math.cos(sun_a) * R0, wy + math.sin(sun_a) * R0, 18, 1.0, "#FFF2C8", "#FFB766", 120)
    label(ctx, "二十四节气", wx, wy - 18, 46, "#F4E6C8", smooth(prog(u, 0.4, 1.0)), "serif_k")
    label(ctx, "太阳一年走一圈", wx, wy + 40, 26, "#CDBA92", smooth(prog(u, 0.7, 1.3)), "serif_r")
    film.vignette(ctx, 0.55)


# ================================================================ 主绘制


SHOTS = [(0.0, _shot_a), (7.0, _shot_b1), (10.6, _shot_b2), (14.6, _shot_b3), (20.0, _shot_c1), (26.4, _shot_c2),
         (30.0, _shot_c3), (33.0, _shot_d1), (36.4, _shot_d2), (40.0, _shot_d3)]
TRANS = {1: ("zoomblur", 0.7, {"x": 960, "y": 540}), 2: ("dissolve", 0.7), 3: ("luma", 0.8),
         4: ("lightsweep", 0.9, {"color": "#FFE2B0"}), 5: ("dissolve", 0.8), 6: ("dissolve", 0.8),
         7: ("lightsweep", 0.9, {"angle": 0.4, "color": "#FFE2B0"}), 8: ("dissolve", 0.8), 9: ("luma", 0.9)}


def draw(ctx, t):
    sequence(ctx, t, SHOTS, TRANS)


def sfx():
    return [
        (0.0, "ambience_wind", {"dur": 7.0, "gain": 0.3}), (0.3, "quill", {"dur": 2.0, "gain": 0.12}),
        (2.4, "whoosh", {"dur": 1.6, "gain": 0.16}), (4.2, "whoosh", {"dur": 2.4, "gain": 0.18}),
        (7.0, "ambience_room", {"dur": 7.6, "gain": 0.45}), (7.2, "paper", {"gain": 0.2}),
        (10.7, "wedge", {"gain": 0.5}), (11.2, "wedge", {"gain": 0.45}), (11.8, "wedge", {"gain": 0.5}),
        (12.0, "wedge", {"gain": 0.45}), (12.6, "ticks", {"dur": 2.0, "rate": 4, "gain": 0.18}),
        (14.6, "ambience_room", {"dur": 5.4, "gain": 0.4}), (15.6, "brass", {"gain": 0.2}), (17.2, "chalk", {"dur": 0.8, "gain": 0.12}),
        (20.0, "ambience_room", {"dur": 6.4, "gain": 0.4}), (20.2, "paper", {"gain": 0.25}), (23.4, "quill", {"dur": 2.0, "gain": 0.2}),
        (26.4, "ambience_river", {"dur": 3.8, "gain": 0.5}), (30.0, "ambience_wind", {"dur": 3.2, "gain": 0.35}),
        (30.9, "chime", {"gain": 0.12}),
        (33.0, "ambience_room", {"dur": 7.0, "gain": 0.35}), (33.3, "crackle", {"dur": 0.6, "gain": 0.25}),
        (36.6, "shimmer", {"dur": 2.0, "gain": 0.15}),
        (40.0, "ambience_wind", {"dur": 4.0, "gain": 0.25}), (42.0, "swell", {"dur": 1.8, "gain": 0.25}),
    ]
