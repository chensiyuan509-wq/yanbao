"""第二章 文字与数：古地图上四条大河亮起；第一视角在泥板上压楔形文字（记账 → 六十进制 → 勾股数）；
尼罗河泛滥与拉绳丈量；星轨下的金字塔；甲骨上的日食；立竿测影与二十四节气。关键词：记录。"""
import math

from ..core import (TAU, H, W, Cam, at, circle, clamp, ease_in, ease_io, ease_out, ellipse, fbm, glow, kf, lerp,
                    lin, mix, poly, polyline_partial, prog, rad, rng, rrect, setc, smooth, star4, stroke_pts, text,
                    view)
from .. import film, oldmap
from .common import claude, fade_io, label, lit

DUR = 50.0
CHAPTER = dict(num="第 二 章", title="文字与数", era="约公元前 3500 年 — 公元前 100 年", key="记录", at=0.9, dur=4.4)
GRAIN = 0.09

VO = [
    (5.6, "大河两岸，{城市}出现了。"),
    (8.0, "两河、尼罗河、印度河、黄河——四条大河，孕育了最早的文明。"),
    (13.8, "苏美尔人在泥板上，刻下了{文字}。"),
    (17.0, "最早记下的，多是账：几只羊、几袋麦。"),
    (20.2, "他们用 {60 进制}：1 小时 60 分、1 圈 360 度，都源于此。"),
    (23.9, "泥板上的{勾股数}，比毕达哥拉斯早了一千多年。"),
    (27.4, "尼罗河每年泛滥，冲掉田界；"),
    (29.7, "埃及人一次次重新丈量土地——{几何学}由此萌芽。"),
    (33.4, "他们定下一年 {365 天}的历法；"),
    (35.8, "大金字塔的四边，几乎{正对东南西北}。"),
    (39.8, "商代的甲骨上，记下了{日食和月食}。"),
    (43.0, "中国人立竿测影，定出了{二十四节气}。"),
    (46.8, "文字和数字，让知识能{跨越生死}，传给后人。", {"spill": 0.5}),
]

SUPERS = [
    (14.0, 17.0, "约公元前 3200 年", "乌鲁克 · 美索不达米亚"),
    (24.0, 27.0, "约公元前 1800 年", "普林顿 322 号泥板"),
    (33.5, 37.0, "约公元前 2560 年", "吉萨大金字塔"),
    (39.9, 42.8, "约公元前 1250 年", "殷墟（今河南安阳）"),
]

# ================================================================ 镜头 A：四条大河

MCAM = oldmap.MapCam([(0.0, (31.0, 27.5, 30)), (5.2, (32.0, 28.5, 27)), (7.4, (44.5, 32.0, 25), ease_io),
                      (9.4, (69.0, 28.5, 21), ease_io), (11.2, (110.0, 35.5, 19), ease_io),
                      (13.6, (72.0, 30.0, 10.5), ease_io)])

RIVERS_A = [("nile", 0.4, "古埃及", "约前 3100 年", (24.0, 23.5)), ("nile_d", 1.5, None, None, None),
            ("euphrates", 5.6, "美索不达米亚", "约前 3500 年", (47.5, 36.8)), ("tigris", 5.9, None, None, None),
            ("indus", 8.0, "古印度", "约前 2600 年", (62.0, 31.5)),
            ("yellow", 9.8, "古代中国", "约前 2000 年", (106.0, 41.5)), ("yangtze", 10.5, None, None, None)]


def _shot_a(ctx, t):
    cam = MCAM.at(t)
    rp = {name: ease_io(prog(t, t0, t0 + 2.4)) for name, t0, *_ in RIVERS_A}
    oldmap.draw_map(ctx, cam, t, 1.0, rivers=["nile", "nile_d", "blue_nile", "euphrates", "tigris", "indus",
                                             "ganges", "yellow", "yangtze", "danube", "rhine"],
                    river_p={**{k: 0.0 for k in ("blue_nile", "ganges", "danube", "rhine")}, **rp})
    # 河流发出金色的光
    for name, t0, title, sub, pos in RIVERS_A:
        p = rp[name]
        if p <= 0:
            continue
        seg = polyline_partial(cam.pts(oldmap.RIVERS[name]), p)
        stroke_pts(ctx, seg, 26, "#FFC76A", 0.18 * p)
        stroke_pts(ctx, seg, 6, "#F2A93A", 0.7)
        if title:
            x, y = cam.xy(*pos)
            a = smooth(prog(t, t0 + 0.8, t0 + 1.6))
            label(ctx, title, x, y, 46 if cam.k > 15 else 32, "#5A2810", a, "serif_k", sub=sub,
                  sub_color="#7A4A26", shadow=False)
    for (nm, t0) in (("孟菲斯", 2.0), ("乌鲁克", 6.6), ("摩亨佐-达罗", 8.9), ("安阳", 10.7)):
        oldmap.city(ctx, cam, nm, smooth(prog(t, t0, t0 + 0.6)), 1.0, size=26, t=t, pulse=True)
    oldmap.compass_rose(ctx, *cam.xy(88, 8), 90 * clamp(cam.k / 20, 0.6, 1.2), 0.8)
    oldmap.map_vignette(ctx, 0.75)
    film.grade(ctx, "#FFB070", 0.15)


# ================================================================ 镜头 B：泥板（第一视角）

TAB = (960, 560, 860, 600)      # 泥板中心与宽高

ROWS1 = [("𒇻", "𒐙", "羊 × 5", 14.3), ("𒊺", "𒎙𒐖", "大麦 × 22", 15.4), ("𒇻", "𒌋𒐗", "羊 × 13", 16.5)]


def _tablet(ctx, t, x, y, w, h, a=1.0):
    box_x, box_y = x - w / 2, y - h / 2
    rrect(ctx, box_x + 14, box_y + 26, w, h, 60)
    setc(ctx, "#000000", 0.45 * a)
    ctx.fill()
    rrect(ctx, box_x, box_y, w, h, 60)
    ctx.set_source(lin(0, box_y, 0, box_y + h, [(0, "#D9A878", a), (1, "#9A6A42", a)]))
    ctx.fill()
    film.paint_texture(ctx, "clay", box_x, box_y, w, h, 0.55 * a,
                       clip_path=lambda c: rrect(c, box_x, box_y, w, h, 60))
    rrect(ctx, box_x + 6, box_y + 6, w - 12, h - 12, 56)
    ctx.set_line_width(6)
    setc(ctx, "#F2C9A0", 0.35 * a)
    ctx.stroke()


def _imp(ctx, s, x, y, size, a=1.0, fnt="cune", col="#5A3418"):
    """压进泥里的字：亮边 + 暗槽。"""
    text(ctx, s, x + 2, y + 2.5, size, "#F4D2A6", 0.55 * a, fnt, "l")
    text(ctx, s, x, y, size, col, 0.92 * a, fnt, "l")


def _shot_b(ctx, t):
    u = t - 13.5
    lampk = film.flicker(t, 8.0, 0.12)
    ctx.set_source(rad(500, 300, 0, 1500, [(0, "#3A2414"), (0.5, "#1C110A"), (1, "#080503")]))
    ctx.paint()
    glow(ctx, 240, 420, 700, "#FFA850", 0.35 * lampk)
    push = 1 + 0.05 * prog(u, 0, 13.5)
    ctx.save()
    ctx.translate(960, 560)
    ctx.scale(push, push)
    ctx.translate(-960, -560)
    x, y, w, h = TAB
    _tablet(ctx, t, x, y, w, h)
    x0, y0 = x - w / 2 + 70, y - h / 2 + 80
    pen = None
    # 第 1 段：记账
    if u < 7.2:
        for i, (pict, num, tr, ts) in enumerate(ROWS1):
            k = smooth(prog(t, ts, ts + 0.25))
            yy = y0 + 40 + i * 150
            if k > 0:
                _imp(ctx, num, x0, yy, 92, k)
                _imp(ctx, pict, x0 + 330, yy, 100, smooth(prog(t, ts + 0.45, ts + 0.7)))
                label(ctx, tr, x0 + 640, yy + 4, 38, "#FFF0D8", smooth(prog(t, ts + 0.7, ts + 1.1)), "serif_sb")
            if ts - 0.2 < t < ts + 0.9:
                pen = (x0 + (60 if t < ts + 0.4 else 380), yy + 10)
    # 第 2 段：六十进制
    elif u < 10.4:
        q = u - 7.2
        a2 = smooth(q / 0.4)
        _imp(ctx, "𒁹", x0 + 10, y0 + 60, 120, a2)
        label(ctx, "= 1", x0 + 110, y0 + 66, 44, "#FFF0D8", a2, "serif_sb", align="l")
        _imp(ctx, "𒌋", x0 + 330, y0 + 60, 120, smooth((q - 0.3) / 0.4))
        label(ctx, "= 10", x0 + 420, y0 + 66, 44, "#FFF0D8", smooth((q - 0.3) / 0.4), "serif_sb", align="l")
        k3 = smooth((q - 0.8) / 0.5)
        _imp(ctx, "𒁹", x0 + 10, y0 + 250, 120, k3)
        _imp(ctx, "𒁹", x0 + 230, y0 + 250, 120, k3)
        label(ctx, "= 1×60 + 1 = 61", x0 + 330, y0 + 256, 44, "#FFF0D8", k3, "serif_sb", align="l")
        label(ctx, "逢六十进一位", x0 + 360, y0 + 340, 30, "#F6D6A8", k3, "serif_r", align="l")
        # 360 度与 60 分钟的表盘浮现
        dk = smooth((q - 1.6) / 0.8)
        if dk > 0:
            cx, cy, r = 1250, 690, 150
            ctx.set_line_width(3)
            setc(ctx, "#FFE2A8", 0.9 * dk)
            circle(ctx, cx, cy, r)
            ctx.stroke()
            for i in range(60):
                ang = i / 60 * TAU - math.pi / 2
                L = 22 if i % 5 == 0 else 10
                ctx.move_to(cx + math.cos(ang) * r, cy + math.sin(ang) * r)
                ctx.line_to(cx + math.cos(ang) * (r - L), cy + math.sin(ang) * (r - L))
            ctx.stroke()
            hand = q * 1.2
            ctx.set_line_width(5)
            ctx.move_to(cx, cy)
            ctx.line_to(cx + math.cos(hand - math.pi / 2) * r * 0.8, cy + math.sin(hand - math.pi / 2) * r * 0.8)
            ctx.stroke()
            label(ctx, "60 分 · 60 秒 · 360°", cx, cy + r + 46, 32, "#FFE2A8", dk, "serif_sb")
        if q < 1.4:
            pen = (x0 + 60 + (300 if q > 0.4 else 0) + (0 if q < 0.8 else -300), y0 + 80 + (190 if q > 0.8 else 0))
    # 第 3 段：普林顿 322 号泥板上的勾股数
    else:
        q = u - 10.4
        cols = [("𒌋𒐖𒁹", "119"), ("𒌋𒐗", "169"), ("𒌋𒐘", "4601"), ("𒐙𒐕", "12709")]
        for r_ in range(5):
            for c_ in range(3):
                k = smooth(prog(q, 0.05 * (r_ * 3 + c_), 0.05 * (r_ * 3 + c_) + 0.3))
                _imp(ctx, "𒌋𒐖" if (r_ + c_) % 2 else "𒐗𒌋𒁹", x0 + c_ * 200, y0 + 30 + r_ * 92, 64, k * 0.85)
        hk = smooth(prog(q, 0.9, 1.3))
        rrect(ctx, x0 - 20, y0 - 15, 590, 92, 16)
        ctx.set_line_width(5)
        setc(ctx, "#FFD27A", hk)
        ctx.stroke()
        # 三角形 119 / 120 / 169
        tk = ease_out(prog(q, 1.2, 2.2))
        if tk > 0:
            ax, ay = 1080, 760
            bx, by = ax + 300 * tk, ay
            cx_, cy_ = ax + 300 * tk, ay - 298 * tk
            poly(ctx, [(ax, ay), (bx, by), (cx_, cy_)])
            setc(ctx, "#FFE2A8", 0.12 * tk)
            ctx.fill_preserve()
            ctx.set_line_width(5)
            setc(ctx, "#FFE2A8", tk)
            ctx.stroke()
            ctx.rectangle(bx - 26, by - 26, 26, 26)
            ctx.set_line_width(3)
            ctx.stroke()
            label(ctx, "120", (ax + bx) / 2, ay + 40, 34, "#FFF0D8", tk, "serif_sb")
            label(ctx, "119", bx + 50, (by + cy_) / 2, 34, "#FFF0D8", tk, "serif_sb")
            label(ctx, "169", (ax + cx_) / 2 - 40, (ay + cy_) / 2 - 30, 34, "#FFD27A", tk, "serif_sb")
            label(ctx, "119² + 120² = 169²", 1230, 470, 36, "#FFD27A", smooth(prog(q, 2.0, 2.6)), "latin")
    ctx.restore()
    # 第一视角：手持芦苇笔
    bob = math.sin(t * 1.4) * 6
    if pen is None:
        pen = (1500, 860)
    px, py = pen
    with lit("#FFA860", 0.5, 0.8 + 0.2 * lampk):
        tip = (px + 200, py + 230 + bob)
        film.pov_arm(ctx, (1700, 1400), tip, 140)
        ctx.save()
        ctx.translate(tip[0] - 40, tip[1] - 40)
        ctx.rotate(-2.3)
        rrect(ctx, -10, -8, 330, 16, 8)
        ctx.set_source(lin(0, -8, 0, 8, [(0, "#E8D29A"), (1, "#9A8044")]))
        ctx.fill()
        ctx.restore()
    film.vignette(ctx, 0.65)


# ================================================================ 镜头 C：尼罗河与金字塔


def _shot_c1(ctx, t):
    u = t - 27.0
    flood = smooth(prog(u, 0.2, 1.8)) * (1 - smooth(prog(u, 2.0, 3.0)))
    film.sky(ctx, [(0, "#7FA7C9"), (0.5, "#E8D3A8"), (0.62, "#F2DDB0"), (1, "#C9A06A")])
    film.sun(ctx, 1600, 260, 40, 0.9, "#FFF6DA", "#FFE0A0", 400)
    film.ridge(ctx, -50, W + 50, 560, 40, 0.003, 3.0, "#C9A675", 1.0, step=20)
    for (yb, sd) in ((600, 4.0),):
        film.ridge(ctx, -50, W + 50, yb, 25, 0.004, sd, "#B48E5C", 1.0, step=20)
    # 田地与界桩
    ctx.set_source(lin(0, 600, 0, H, [(0, "#6E8A3A"), (1, "#4A5A22")]))
    ctx.rectangle(-50, 610, W + 100, H)
    ctx.fill()
    mud = smooth(prog(u, 2.2, 3.0))
    if mud > 0:
        ctx.set_source(lin(0, 610, 0, H, [(0, "#6A4A2A", mud), (1, "#4A3218", mud)]))
        ctx.rectangle(-50, 610, W + 100, H)
        ctx.fill()
    for i in range(9):
        x = 140 + i * 210
        gone = smooth(prog(u, 0.8 + i * 0.05, 1.6 + i * 0.05))
        ctx.save()
        ctx.translate(x + gone * 120, 760 + gone * 30)
        ctx.rotate(gone * 1.3)
        rrect(ctx, -7, -60, 14, 70, 3)
        setc(ctx, "#5A3A1E", 1 - gone)
        ctx.fill()
        ctx.restore()
        if i < 8:
            ctx.set_line_width(3)
            setc(ctx, "#3E4E1A", 0.6 * (1 - gone))
            ctx.move_to(x, 760)
            ctx.line_to(x + 210, 760)
            ctx.stroke()
    # 河水
    lvl = 690 - 210 * flood
    ctx.set_source(lin(0, lvl, 0, H, [(0, "#4F7FA0", 0.92), (1, "#2C4E66", 0.95)]))
    ctx.move_to(-50, H + 50)
    ctx.line_to(-50, lvl + 260 * (1 - flood) + 20)
    for i in range(0, W + 100, 40):
        ctx.line_to(i, (lvl + 260 * (1 - flood) if flood < 0.99 else lvl) + math.sin(i * 0.03 + t * 2) * 5
                    + (0 if flood > 0.3 else 200 * (1 - flood / 0.3) * (abs(i - 960) / 960) ** 0.5))
    ctx.line_to(W + 50, H + 50)
    ctx.close_path()
    ctx.fill()
    # 拉绳丈量的人
    sk = smooth(prog(u, 3.1, 3.6))
    if sk > 0:
        pts = [(420, 860), (1060, 860), (1060, 690), (420, 690)]
        pr = ease_io(prog(u, 3.3, 5.6))
        seg = polyline_partial(pts + [pts[0]], pr)
        stroke_pts(ctx, seg, 4, "#E8D8B0", sk)
        for j in range(13):
            pt = polyline_partial(pts + [pts[0]], 0, j / 12)
            if j / 12 <= pr and len(pt) > 0:
                circle(ctx, pt[-1][0], pt[-1][1], 6)
                setc(ctx, "#F2E2BC", sk)
                ctx.fill()
        film.human(ctx, 420, 880, 210, "reach", t, "#2A1A10", sk, rim="#FFE0A0", rim_a=0.6, hat="cap")
        film.human(ctx, 1080, 880, 210, "reach", t, "#2A1A10", sk, flip=True, rim="#FFE0A0", rim_a=0.6, hat="cap")
        label(ctx, "geo（土地）+ metria（测量）= geometry 几何", 960, 300, 36, "#3A2414",
              smooth(prog(u, 4.0, 4.8)), "serif_sb", shadow=False)
    film.grade(ctx, "#FFC27A", 0.18)
    film.vignette(ctx, 0.45)


def _pyramid(ctx, x, y, w, h, light, dark, a=1.0):
    poly(ctx, [(x - w / 2, y), (x, y - h), (x + w / 2, y)])
    setc(ctx, dark, a)
    ctx.fill()
    poly(ctx, [(x, y - h), (x + w / 2, y), (x + w * 0.12, y)])
    setc(ctx, light, a)
    ctx.fill()


def _shot_c2(ctx, t):
    u = t - 33.0
    film.sky(ctx, [(0, "#02040C"), (0.6, "#0C1530"), (0.75, "#2A2A48"), (1, "#3A2A2A")])
    # 星轨：绕北天极旋转
    px, py = 1380, 300
    R = rng(91)
    sweep = 0.35 + 0.9 * ease_out(prog(u, 0, 6.5))
    for i in range(170):
        r = R.uniform(30, 1300)
        a0 = R.uniform(0, TAU)
        br = R.uniform(0.25, 0.9)
        ctx.new_path()
        ctx.arc(px, py, r, a0, a0 + sweep * (0.3 + 0.7 * R.random()))
        ctx.set_line_width(R.uniform(1.2, 2.6))
        setc(ctx, mix("#CFE0FF", "#FFE2B0", R.random()), br * 0.6)
        ctx.stroke()
    star4(ctx, px, py, 16, "#FFFFFF", 0.9)
    label(ctx, "北天极", px, py - 44, 26, "#DCE6FF", smooth(prog(u, 1.5, 2.2)), "serif_r")
    film.ridge(ctx, -50, W + 50, 860, 20, 0.003, 6.0, "#3A2A20", 1.0, step=20)
    _pyramid(ctx, 700, 870, 900, 520, "#7A5A3E", "#3E2C1E")
    _pyramid(ctx, 1270, 875, 520, 320, "#6A4E36", "#34261A")
    _pyramid(ctx, 1560, 880, 260, 160, "#5E4430", "#2E2216")
    ctx.set_source(lin(0, 860, 0, H, [(0, "#3A2A1E"), (1, "#140E08")]))
    ctx.rectangle(-50, 868, W + 100, 300)
    ctx.fill()
    # 俯视小图：底边对准正北
    k = smooth(prog(u, 2.6, 3.3))
    if k > 0:
        cx, cy, s = 330, 360, 120
        rrect(ctx, cx - 170, cy - 190, 340, 380, 20)
        setc(ctx, "#0A0C14", 0.7 * k)
        ctx.fill()
        ctx.save()
        ctx.translate(cx, cy + 20)
        ctx.rotate(math.radians(-0.05))
        ctx.rectangle(-s / 2 - 20, -s / 2 - 20, s + 40, s + 40)
        setc(ctx, "#C9A06A", k)
        ctx.fill()
        poly(ctx, [(-s / 2 - 20, -s / 2 - 20), (0, 0), (s / 2 + 20, -s / 2 - 20)])
        setc(ctx, "#E2C08A", k)
        ctx.fill()
        ctx.restore()
        ctx.set_line_width(3)
        setc(ctx, "#FFD27A", k)
        ctx.move_to(cx, cy - 60)
        ctx.line_to(cx, cy - 150)
        ctx.stroke()
        from ..core import arrow_head
        arrow_head(ctx, cx, cy - 160, -math.pi / 2, 22, "#FFD27A", k)
        label(ctx, "N", cx + 26, cy - 150, 28, "#FFD27A", k, "latin_b")
        label(ctx, "偏差不到 0.1°", cx, cy + 140, 28, "#F2E2BC", k, "serif_sb")
    # 365 天
    k2 = smooth(prog(u, 0.3, 1.0)) * (1 - smooth(prog(u, 2.4, 2.8)))
    if k2 > 0:
        label(ctx, "365 天", 330, 330, 80, "#FFE8C0", k2, "serif_k")
        label(ctx, "12 个月 × 30 天 + 5 天", 330, 410, 30, "#E2D2B0", k2, "serif_r")
    film.vignette(ctx, 0.55)


# ================================================================ 镜头 D：甲骨、二十四节气


def _shot_d1(ctx, t):
    u = t - 39.5
    ctx.set_source(rad(960, 560, 0, 1100, [(0, "#2E2016"), (1, "#0A0705")]))
    ctx.paint()
    glow(ctx, 960, 560, 700, "#FFB060", 0.18)
    push = 1 + 0.08 * ease_io(prog(u, 0, 5))
    ctx.save()
    ctx.translate(960, 560)
    ctx.scale(push, push)
    ctx.rotate(-0.04)
    # 龟甲
    def shell(c):
        c.move_to(0, -380)
        c.curve_to(260, -370, 330, -150, 320, 40)
        c.curve_to(310, 250, 200, 380, 0, 390)
        c.curve_to(-200, 380, -310, 250, -320, 40)
        c.curve_to(-330, -150, -260, -370, 0, -380)
        c.close_path()
    shell(ctx)
    ctx.set_source(lin(-300, -380, 300, 380, [(0, "#EFE2C2"), (0.6, "#D3BE92"), (1, "#A88E62")]))
    ctx.fill()
    film.paint_texture(ctx, "paper", -330, -390, 660, 780, 0.3, clip_path=shell)
    setc(ctx, "#8A7450", 0.5)
    ctx.set_line_width(3)
    for yy in (-200, -40, 120, 260):
        ctx.move_to(-280, yy)
        ctx.curve_to(-100, yy + 20, 100, yy + 20, 280, yy)
    ctx.move_to(0, -370)
    ctx.line_to(0, 380)
    ctx.stroke()
    # 灼烧出的"卜"字形裂纹
    for i, (cx, cy) in enumerate(((-150, -120), (140, -100), (-150, 200), (150, 210))):
        k = ease_out(prog(u, 0.4 + i * 0.35, 0.9 + i * 0.35))
        if k <= 0:
            continue
        ctx.set_line_width(4)
        setc(ctx, "#3A2410", 0.9)
        ctx.move_to(cx, cy - 70 * k)
        ctx.line_to(cx, cy + 70 * k)
        ctx.move_to(cx, cy - 10)
        ctx.line_to(cx + (1 if cx < 0 else -1) * 60 * k, cy - 10 - 34 * k)
        ctx.stroke()
        glow(ctx, cx, cy, 90, "#FF8A3A", 0.5 * (1 - k))
    # 刻辞
    chars = "日有食"
    for i, ch in enumerate(chars):
        k = smooth(prog(u, 1.8 + i * 0.35, 2.3 + i * 0.35))
        text(ctx, ch, -40, -150 + i * 110, 96, "#6A2A16", k, "kai")
    chars2 = "月有食"
    for i, ch in enumerate(chars2):
        k = smooth(prog(u, 2.9 + i * 0.3, 3.4 + i * 0.3))
        text(ctx, ch, 40, -40 + i * 110, 96, "#6A2A16", k * 0.9, "kai")
    ctx.restore()
    film.vignette(ctx, 0.6)


TERMS = ["立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
         "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"]


def _shot_d2(ctx, t):
    u = t - 44.5
    ctx.set_source(rad(960, 540, 0, 1200, [(0, "#2A2016"), (1, "#0A0806")]))
    ctx.paint()
    film.paint_texture(ctx, "paper", 0, 0, W, H, 0.12)
    center = ease_io(prog(u, 3.8, 5.5))
    wx, wy, R0 = lerp(1240, 960, center), 540, 300
    # 圭表
    gk = 1 - center
    if gk > 0.01:
        gx, gy = 330, 820
        rrect(ctx, gx - 12, gy - 320, 24, 320, 6)
        setc(ctx, "#6A4A2A", gk)
        ctx.fill()
        rrect(ctx, gx - 20, gy, 560, 26, 6)
        setc(ctx, "#8A6A42", gk)
        ctx.fill()
        for i in range(12):
            ctx.rectangle(gx + 30 + i * 44, gy + 4, 3, 18)
        setc(ctx, "#3A2410", gk)
        ctx.fill()
        ang = u * 1.3
        L = 120 + 300 * (0.5 - 0.5 * math.cos(ang))
        rrect(ctx, gx, gy - 6, L, 12, 4)
        setc(ctx, "#140C06", 0.75 * gk)
        ctx.fill()
        label(ctx, "圭表：立竿测影", gx + 260, gy + 80, 32, "#F2D79B", gk, "serif_sb")
        label(ctx, "影子最短 → 夏至　最长 → 冬至", gx + 260, gy + 126, 26, "#E2D2B0", gk, "serif_r")
    # 二十四节气轮盘
    ctx.set_line_width(4)
    setc(ctx, "#D9B26A", 0.9)
    circle(ctx, wx, wy, R0)
    ctx.stroke()
    ctx.set_line_width(1.5)
    circle(ctx, wx, wy, R0 - 70)
    ctx.stroke()
    sun_a = -math.pi / 2 + u * 0.9
    for i, nm in enumerate(TERMS):
        ang = -math.pi / 2 + i / 24 * TAU
        k = smooth(prog(u, 0.2 + i * 0.06, 0.6 + i * 0.06))
        x1, y1 = wx + math.cos(ang) * R0, wy + math.sin(ang) * R0
        x2, y2 = wx + math.cos(ang) * (R0 - 22), wy + math.sin(ang) * (R0 - 22)
        ctx.set_line_width(3)
        setc(ctx, "#D9B26A", k)
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()
        lx, ly = wx + math.cos(ang) * (R0 + 48), wy + math.sin(ang) * (R0 + 40)
        hot = max(0.0, math.cos(ang - sun_a)) ** 30
        text(ctx, nm, lx, ly, 26, mix("#E8D8B8", "#FFD27A", hot), k, "kai")
    film.sun(ctx, wx + math.cos(sun_a) * R0, wy + math.sin(sun_a) * R0, 18, 1.0, "#FFF2C8", "#FFB766", 120)
    label(ctx, "二十四节气", wx, wy - 18, 46, "#F4E6C8", smooth(prog(u, 0.6, 1.2)), "serif_k")
    label(ctx, "太阳一年走一圈", wx, wy + 40, 26, "#CDBA92", smooth(prog(u, 0.9, 1.5)), "serif_r")
    film.vignette(ctx, 0.55)


# ================================================================ 主绘制


def draw(ctx, t):
    if t < 13.5:
        _shot_a(ctx, t)
    elif t < 27.0:
        _shot_b(ctx, t)
    elif t < 33.0:
        _shot_c1(ctx, t)
    elif t < 39.5:
        _shot_c2(ctx, t)
    elif t < 44.5:
        _shot_d1(ctx, t)
    else:
        _shot_d2(ctx, t)


def sfx():
    out = [
        (0.0, "ambience_wind", {"dur": 13.5, "gain": 0.3}),
        (0.4, "quill", {"dur": 2.2, "gain": 0.12}),
        (5.6, "whoosh", {"dur": 1.8, "gain": 0.18}),
        (7.6, "whoosh", {"dur": 1.6, "gain": 0.16}),
        (9.4, "whoosh", {"dur": 1.6, "gain": 0.16}),
        (11.2, "whoosh", {"dur": 2.2, "gain": 0.2}),
        (13.5, "ambience_room", {"dur": 13.5, "gain": 0.5}),
        (13.5, "ambience_fire", {"dur": 13.5, "gain": 0.18}),
    ]
    for (pict, num, tr, ts) in ROWS1:
        out += [(ts, "wedge", {"gain": 0.5}), (ts + 0.15, "wedge", {"gain": 0.4}), (ts + 0.45, "wedge", {"gain": 0.5})]
    out += [(20.7, "wedge", {"gain": 0.5}), (21.0, "wedge", {"gain": 0.45}), (21.5, "wedge", {"gain": 0.5}),
            (22.3, "ticks", {"dur": 1.6, "rate": 4, "gain": 0.2}),
            (24.3, "chalk", {"dur": 0.8, "gain": 0.12}), (24.7, "brass", {"gain": 0.2}),
            (27.0, "ambience_river", {"dur": 6.0, "gain": 0.6}), (27.2, "water", {"gain": 0.35}),
            (28.2, "rumble", {"dur": 1.4, "gain": 0.3}), (30.3, "stretch", {"dur": 1.4, "gain": 0.2}),
            (33.0, "ambience_wind", {"dur": 6.5, "gain": 0.35}), (33.0, "ambience_night", {"dur": 6.5, "gain": 0.3}),
            (35.6, "chime", {"gain": 0.15}),
            (39.5, "ambience_room", {"dur": 5.0, "gain": 0.4})]
    for i in range(4):
        out.append((39.9 + i * 0.35, "crackle", {"dur": 0.4, "gain": 0.28}))
    out += [(41.3, "carve", {"dur": 0.4, "gain": 0.3}), (41.7, "carve", {"dur": 0.4, "gain": 0.3}),
            (44.5, "ambience_wind", {"dur": 5.5, "gain": 0.25}), (44.7, "shimmer", {"dur": 1.5, "gain": 0.15}),
            (48.0, "swell", {"dur": 1.8, "gain": 0.25})]
    return out
