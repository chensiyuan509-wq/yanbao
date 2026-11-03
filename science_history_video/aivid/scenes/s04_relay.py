"""第四章 薪火相传：巴格达"智慧之家"的翻译运动；花拉子米与"代数""算法"；数字 0 的旅程；
伊本·海赛姆的暗室；丝绸之路上西传的发明；古腾堡印刷机。关键词：传承。"""
import math

from ..core import (TAU, H, W, Cam, arrow, at, circle, clamp, ease_in, ease_io, ease_out, ellipse, glow, kf,
                    lerp, lin, mix, poly, polyline_partial, prog, rad, rng, rrect, setc, smooth, star4, stroke_pts,
                    text, view)
from .. import film, oldmap
from mascot import draw_prop
from .common import claude, fade_io, label, lit

DUR = 42.0
CHAPTER = dict(num="第 四 章", title="薪火相传", era="约公元 500 — 1450 年", key="传承", at=0.8, dur=4.4)
GRAIN = 0.09

VO = [
    (5.2, "'{智慧之家}'把希腊、印度的典籍译成阿拉伯文。"),
    (9.2, "花拉子米写下《代数学》——"),
    (11.4, "'{代数}'来自他的书名，'{算法}'来自他的名字。"),
    (14.8, "印度人发明的 {0}，经阿拉伯传入欧洲，成了今天的数字。"),
    (18.8, "伊本·海赛姆用暗室证明：光是{射进眼睛}的。"),
    (22.8, "在东方，造纸术、印刷术、指南针和火药，沿着丝绸之路{一路西传}；"),
    (27.6, "11 世纪，毕昇发明了{活字印刷}。"),
    (32.2, "古腾堡的印刷机，让书变得便宜："),
    (35.4, "到 1500 年，欧洲已印出{两千多万册}书——"),
    (38.6, "知识，第一次能被{大规模复制}。", {"spill": 0.5}),
]

SUPERS = [
    (5.3, 8.6, "9 世纪", "巴格达 · 智慧之家"),
    (18.9, 22.3, "1011 — 1021 年", "开罗 · 《光学之书》"),
    (32.3, 35.2, "约 1450 年", "美因茨 · 古腾堡"),
]

# ================================================================ A1：智慧之家


def _arch(ctx, x, y, w, h, color):
    """尖拱（伊斯兰建筑的拱门）。"""
    ctx.move_to(x - w / 2, y)
    ctx.line_to(x - w / 2, y - h * 0.6)
    ctx.curve_to(x - w / 2, y - h * 0.85, x - w * 0.15, y - h * 0.95, x, y - h)
    ctx.curve_to(x + w * 0.15, y - h * 0.95, x + w / 2, y - h * 0.85, x + w / 2, y - h * 0.6)
    ctx.line_to(x + w / 2, y)
    ctx.close_path()
    setc(ctx, color)
    ctx.fill()


def _lantern(ctx, x, y, t, seed):
    fl = film.flicker(t, seed, 0.15)
    ctx.set_line_width(2)
    setc(ctx, "#3A2410")
    ctx.move_to(x, y - 200)
    ctx.line_to(x, y - 26)
    ctx.stroke()
    glow(ctx, x, y, 200 * fl, "#FFB24A", 0.45)
    poly(ctx, [(x - 18, y - 26), (x + 18, y - 26), (x + 24, y + 6), (x, y + 30), (x - 24, y + 6)])
    setc(ctx, "#FFD27A", 0.95)
    ctx.fill()


H1 = (claude(1480, 905, 0.46, "wonder", seed=10.0).hold(0.0, ("book", {"color": "#2E7A5A"}), "front")
      .look(0.5, -0.7, -0.3).expr(4.0, "smile"))


def _shot_a1(ctx, t):
    dx = 120 * ease_io(prog(t, 0, 8.6))
    ctx.set_source(rad(960, 500, 0, 1300, [(0, "#2A1C3A"), (0.6, "#140E20"), (1, "#06040A")]))
    ctx.paint()
    ctx.save()
    ctx.translate(-dx * 0.4, 0)
    # 拱门外的夜空与月亮
    for i in range(5):
        x = 200 + i * 400
        ctx.save()
        ctx.move_to(x - 140, 760)
        ctx.line_to(x - 140, 430)
        ctx.curve_to(x - 140, 300, x - 40, 260, x, 240)
        ctx.curve_to(x + 40, 260, x + 140, 300, x + 140, 430)
        ctx.line_to(x + 140, 760)
        ctx.close_path()
        ctx.clip()
        ctx.set_source(lin(0, 240, 0, 760, [(0, "#1A2448"), (1, "#3A3A5A")]))
        ctx.paint()
        film.star_field(ctx, t, 30, i + 3, area=(x - 140, 240, 280, 400), a=0.8)
        if i == 3:
            film.moon(ctx, x + 30, 380, 30, 0.12, 0.9, glow_a=0.3)
        ctx.restore()
    ctx.restore()
    # 墙（拱门之间）用一张大遮罩做出来
    ctx.save()
    ctx.translate(-dx * 0.4, 0)
    ctx.set_fill_rule(1)
    ctx.rectangle(-300, 0, W + 600, H)
    for i in range(5):
        x = 200 + i * 400
        ctx.move_to(x - 140, 760)
        ctx.line_to(x - 140, 430)
        ctx.curve_to(x - 140, 300, x - 40, 260, x, 240)
        ctx.curve_to(x + 40, 260, x + 140, 300, x + 140, 430)
        ctx.line_to(x + 140, 760)
        ctx.close_path()
    ctx.set_source(lin(0, 0, 0, H, [(0, "#3A2A20"), (1, "#1A120C")]))
    ctx.fill()
    ctx.restore()
    ctx.save()
    ctx.translate(-dx, 0)
    for i, x in enumerate((360, 960, 1560)):
        _lantern(ctx, x, 330, t, i + 2.0)
    # 地面、矮桌、译者
    ctx.set_source(lin(0, 760, 0, H, [(0, "#3A2618"), (1, "#140C06")]))
    ctx.rectangle(-300, 760, W + 600, 400)
    ctx.fill()
    for (x, fl, hat) in ((520, False, "turban"), (900, True, "turban"), (1180, False, "cap")):
        film.human(ctx, x, 900, 300, "sit", t, "#140C08", 1.0, flip=fl, rim="#FFB060", rim_a=0.8, robe=True, hat=hat,
                   arms=(0.6, 1.2 + 0.15 * math.sin(t * 3 + x)))
        rrect(ctx, x + (-150 if fl else 60), 830, 100, 16, 4)
        setc(ctx, "#E8D2A0", 0.9)
        ctx.fill()
    # 从希腊书卷飞向阿拉伯文抄本的光点
    for k in range(18):
        u = (t * 0.35 + k / 18) % 1.0
        x = lerp(560, 860, u)
        y = 820 - math.sin(u * math.pi) * 140
        glow(ctx, x, y, 18, "#FFE2A8", 0.7 * math.sin(u * math.pi))
    label(ctx, "希腊文", 560, 945, 26, "#F2D79B", 0.8, "serif_r")
    label(ctx, "阿拉伯文", 860, 945, 26, "#F2D79B", 0.8, "serif_r")
    ctx.restore()
    with lit("#FFB070", 0.45, 0.8):
        H1.draw(ctx, t)
    film.vignette(ctx, 0.6)


# ================================================================ A2：词源


def _shot_a2(ctx, t):
    u = t - 8.6
    ctx.set_source(lin(0, 0, 0, H, [(0, "#E8D6AC"), (1, "#C9AE7E")]))
    ctx.paint()
    film.paint_texture(ctx, "parchment", 0, 0, W, H, 0.75, scale=0.9)
    ink = "#3A2414"
    ctx.save()
    ctx.translate(960, 540)
    ctx.scale(1 + 0.05 * u / 6, 1 + 0.05 * u / 6)
    ctx.translate(-960, -540)
    label(ctx, "花拉子米 · 约 780 — 850 年", 960, 220, 36, ink, smooth(prog(u, 0.2, 0.8)), "serif_k", shadow=False)
    rows = [("al-jabr", "algebra", "代数", 2.6, 360), ("al-Khwārizmī", "Algoritmi", "algorithm · 算法", 3.4, 560)]
    for (a_, b_, c_, t0, y) in rows:
        k1 = smooth(prog(u, t0 - 1.6, t0 - 1.0))
        k2 = smooth(prog(u, t0 - 0.6, t0))
        k3 = smooth(prog(u, t0 + 0.4, t0 + 1.0))
        text(ctx, a_, 460, y, 54, ink, k1, "latin_i")
        arrow(ctx, 640, y, 790, y, 4, "#8A4A1E", k2, p=k2)
        text(ctx, b_, 1000, y, 54, ink, k2, "latin_i")
        arrow(ctx, 1190, y, 1300, y, 4, "#8A4A1E", k3, p=k3)
        text(ctx, c_, 1550, y, 50, "#8A2A10", k3, "serif_k")
    label(ctx, "《还原与对消计算概要》→ 代数", 960, 740, 32, ink, smooth(prog(u, 3.6, 4.4)), "serif_sb", shadow=False)
    label(ctx, "他的名字被拉丁化为 Algoritmi → 今天的\"算法\"", 960, 800, 32, ink, smooth(prog(u, 4.2, 5.0)), "serif_sb",
          shadow=False)
    ctx.restore()
    film.vignette(ctx, 0.45, color="#2A1A0A")


# ================================================================ B1：数字的演变

SCRIPTS = [("婆罗米数字 · 印度", "brahmi", ["𑁦", "𑁧", "𑁨", "𑁩", "𑁪", "𑁫", "𑁬", "𑁭", "𑁮", "𑁯"]),
           ("天城体数字 · 印度", "deva", ["०", "१", "२", "३", "४", "५", "६", "७", "८", "९"]),
           ("东阿拉伯数字 · 巴格达", "arabic", ["٠", "١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩"]),
           ("今天的数字", "latin", ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])]


def _shot_b1(ctx, t):
    u = t - 14.5
    ctx.set_source(rad(960, 540, 0, 1200, [(0, "#2A2018"), (1, "#0A0806")]))
    ctx.paint()
    film.paint_texture(ctx, "paper", 0, 0, W, H, 0.1)
    for r_, (name, fnt, digs) in enumerate(SCRIPTS):
        y = 250 + r_ * 170
        k = smooth(prog(u, 0.2 + r_ * 0.7, 0.8 + r_ * 0.7))
        label(ctx, name, 330, y, 28, "#CDBA92", k, "serif_r")
        for i, d in enumerate(digs):
            x = 600 + i * 120
            hot = 1.0 if i == 0 else 0.0
            if hot and k > 0:
                glow(ctx, x, y, 70, "#FFD27A", 0.4 * k)
            text(ctx, d, x, y, 76 if fnt != "brahmi" else 64, "#FFE8C0" if not hot else "#FFD27A", k, fnt)
        if r_ < 3:
            arrow(ctx, 1840, y + 30, 1840, y + 140, 4, "#D9B26A", 0.8 * k, p=smooth(prog(u, 0.6 + r_ * 0.7, 1.2 + r_ * 0.7)))
    label(ctx, "0：表示\"什么都没有\"，也让位值成为可能", 1110, 920, 32, "#FFD27A", smooth(prog(u, 2.8, 3.4)), "serif_sb")
    film.vignette(ctx, 0.55)


# ================================================================ B2：暗室（小孔成像）


def _shot_b2(ctx, t):
    u = t - 18.5
    ctx.set_source_rgb(0.03, 0.025, 0.02)
    ctx.paint()
    # 左墙小孔；右墙上倒立的火焰像
    wall_x = 520
    ctx.rectangle(wall_x - 30, 90, 60, 900)
    setc(ctx, "#1E140C")
    ctx.fill()
    hx, hy = wall_x, 520
    # 墙外的蜡烛（从缝里能看到一点光）
    glow(ctx, 230, 560, 260, "#FFB24A", 0.5)
    with at(ctx, 230, 700, 1.4):
        draw_prop(ctx, ("candle",), t)
    k = smooth(prog(u, 0.3, 1.2))
    # 光线：两条交叉的光束
    top, bot = (230, 590), (230, 700)
    img_x = 1560
    for (src, dst) in ((top, (img_x, 520 + (520 - 590) * -2.6)), (bot, (img_x, 520 + (520 - 700) * -2.6))):
        ctx.move_to(*src)
        ctx.line_to(hx, hy)
        ctx.line_to(*dst)
        ctx.set_line_width(3)
        setc(ctx, "#FFD27A", 0.5 * k)
        ctx.stroke()
    ctx.move_to(hx, hy - 4)
    ctx.line_to(img_x, 520 - 330)
    ctx.line_to(img_x, 520 + 330)
    ctx.line_to(hx, hy + 4)
    ctx.close_path()
    ctx.set_source(lin(hx, 0, img_x, 0, [(0, "#FFE2A8", 0.35 * k), (1, "#FFE2A8", 0.05 * k)]))
    ctx.fill()
    # 右墙上的倒像
    ctx.rectangle(img_x, 90, 400, 900)
    setc(ctx, "#2A2016")
    ctx.fill()
    ctx.save()
    ctx.translate(img_x + 200, 330)
    ctx.scale(-1.8, -1.8)                 # 上下、左右都颠倒
    draw_prop(ctx, ("candle",), t, k * 0.75)
    ctx.restore()
    label(ctx, "倒立的像", img_x + 170, 900, 30, "#FFE8C0", smooth(prog(u, 1.4, 2.0)), "serif_sb")
    film.human(ctx, 1150, 920, 330, "point", t, "#0E0906", 1.0, rim="#FFB060", rim_a=0.6, robe=True, hat="turban",
               arms=(0.3, 2.0))
    label(ctx, "光沿直线传播", 960, 230, 32, "#F2D79B", smooth(prog(u, 1.8, 2.4)), "serif_sb")
    label(ctx, "与《墨经》的小孔成像遥相呼应", 960, 280, 26, "#CDBA92", smooth(prog(u, 2.4, 3.0)), "serif_r")
    film.vignette(ctx, 0.5)


# ================================================================ C：丝绸之路

SILK = [(108.9, 34.3), (103.8, 36.1), (98.5, 39.7), (94.7, 40.1), (88.0, 41.5), (80.0, 41.0), (76.0, 39.5),
        (71.0, 40.5), (67.0, 39.65), (61.8, 37.6), (54.0, 36.5), (51.4, 35.7), (44.4, 33.3), (38.8, 35.5),
        (36.3, 33.5), (35.5, 35.5), (29.0, 41.0), (23.0, 40.0), (19.0, 41.5), (12.33, 45.44)]
SEA_ROUTE = [(44.4, 33.3), (36.3, 33.5), (31.2, 30.05), (20.0, 33.5), (10.0, 37.0), (0.0, 38.0), (-4.0, 39.9)]
CCAM = oldmap.MapCam([(22.5, (106.0, 36.0, 26)), (25.0, (80.0, 39.5, 20), ease_io), (27.2, (55.0, 37.0, 18), ease_io),
                      (29.4, (30.0, 38.0, 17), ease_io), (32.0, (55.0, 37.0, 8.5), ease_io)])
INVENTIONS = [("纸", "105 年 蔡伦改进", 22.7), ("活字印刷", "1040 年代 毕昇", 23.3), ("指南针", "11 世纪", 23.9),
              ("火药", "9 世纪", 24.5)]


def _shot_c(ctx, t):
    cam = CCAM.at(t)
    oldmap.draw_map(ctx, cam, t, 1.0, rivers=["yellow", "yangtze", "indus", "euphrates", "tigris", "nile", "danube"])
    p = ease_io(prog(t, 22.8, 30.8))
    end = oldmap.route(ctx, cam, SILK, p, "#A8321E", 1.0, 5, t=t)
    oldmap.route(ctx, cam, SEA_ROUTE, ease_io(prog(t, 29.0, 31.2)), "#7A3A9A", 0.9, 4, t=t)
    for nm, t0 in (("长安", 22.6), ("敦煌", 23.8), ("撒马尔罕", 25.0), ("巴格达", 27.0), ("君士坦丁堡", 28.6),
                   ("威尼斯", 29.6), ("托莱多", 30.6)):
        oldmap.city(ctx, cam, nm, smooth(prog(t, t0, t0 + 0.5)), 1.0, size=26, t=t)
    # 驼队剪影跟在线路前端（往西走，队伍拖在东边）
    if end:
        ex, ey = end
        for i in range(3):
            bob = math.sin(t * 6 + i * 1.7) * 3
            cx, cy = ex + 50 + i * 58, ey + 46 + bob
            setc(ctx, "#3A2414", 0.9)
            ellipse(ctx, cx, cy, 20, 10)
            ctx.fill()
            ellipse(ctx, cx + 2, cy - 10, 9, 8)
            ctx.fill()
            ctx.set_line_width(5)
            ctx.set_line_cap(1)
            ctx.move_to(cx - 16, cy + 2)
            ctx.line_to(cx - 26, cy - 16)
            ctx.line_to(cx - 32, cy - 14)
            ctx.stroke()
            ctx.set_line_width(3.5)
            for lx in (-12, -5, 8, 15):
                ctx.move_to(cx + lx, cy + 6)
                ctx.line_to(cx + lx + math.sin(t * 8 + lx + i) * 3, cy + 24)
            ctx.stroke()
    # 发明卡片：沿路线往西漂
    for i, (nm, sub, t0) in enumerate(INVENTIONS):
        k = smooth(prog(t, t0, t0 + 0.5)) * (1 - smooth(prog(t, 31.0, 31.8)))
        if k <= 0:
            continue
        x = 300 + i * 230
        y = 210
        rrect(ctx, x - 100, y - 50, 200, 104, 14)
        setc(ctx, "#F6E8C6", 0.92 * k)
        ctx.fill()
        ctx.set_line_width(3)
        setc(ctx, "#8A4A1E", k)
        rrect(ctx, x - 100, y - 50, 200, 104, 14)
        ctx.stroke()
        text(ctx, nm, x, y - 12, 34, "#5A1E0E", k, "serif_k")
        text(ctx, sub, x, y + 28, 20, "#5A3A1E", k, "serif_r")
    oldmap.map_vignette(ctx, 0.7)
    film.grade(ctx, "#FFB070", 0.12)


# ================================================================ D：古腾堡印刷机


def _press(ctx, t, x, y, down):
    wood, dark = "#5A3A1E", "#2E1C0C"
    for dx in (-260, 230):
        rrect(ctx, x + dx, y - 620, 34, 640, 6)
        setc(ctx, wood)
        ctx.fill()
    rrect(ctx, x - 290, y - 640, 580, 60, 8)
    setc(ctx, wood)
    ctx.fill()
    rrect(ctx, x - 290, y - 300, 580, 40, 6)
    setc(ctx, dark)
    ctx.fill()
    # 螺杆与压板
    sy = y - 580 + down * 90
    for i in range(10):
        ctx.rectangle(x - 22, y - 580 + i * 14 + (down * 90) % 14, 44, 6)
    setc(ctx, "#8A6A3A")
    ctx.fill()
    rrect(ctx, x - 170, sy + 130, 340, 40, 6)
    setc(ctx, "#6A4A28")
    ctx.fill()
    # 手柄
    ang = -0.4 + down * 1.4
    ctx.set_line_width(14)
    ctx.set_line_cap(1)
    setc(ctx, dark)
    ctx.move_to(x, sy + 60)
    ctx.line_to(x + math.cos(ang) * 260, sy + 60 + math.sin(ang) * 60)
    ctx.stroke()
    # 印版
    rrect(ctx, x - 200, y - 110, 400, 40, 4)
    setc(ctx, "#3A3A3A")
    ctx.fill()
    return x + math.cos(ang) * 260, sy + 60 + math.sin(ang) * 60


def _shot_d(ctx, t):
    u = t - 32.0
    fl = film.flicker(t, 13.0, 0.12)
    ctx.set_source(rad(900, 500, 0, 1300, [(0, "#3A2614"), (1, "#0A0604")]))
    ctx.paint()
    film.shaft(ctx, 1500, 90, 900, 980, 200, 600, "#FFD49A", 0.14)
    film.dust(ctx, t, 50, 8, (700, 100, 900, 880), "#FFE6B8", 0.45)
    ctx.set_source(lin(0, 880, 0, H, [(0, "#2A1A0E"), (1, "#0E0905")]))
    ctx.rectangle(-50, 900, W + 100, 200)
    ctx.fill()
    presses = [0.6, 2.0]
    down = 0.0
    for tp in presses:
        if tp - 0.5 < u < tp + 0.6:
            down = ease_in(clamp((u - (tp - 0.5)) / 0.5)) if u < tp else 1 - ease_out(clamp((u - tp) / 0.6))
    hx, hy = _press(ctx, t, 760, 900, down)
    film.human(ctx, hx + 90, 910, 330, "reach", t, "#140C06", 1.0, flip=True, rim="#FFB060", rim_a=0.7,
               arms=(1.3, 1.5), hat="hair")
    # 印好的纸一张张飞出来、越来越多
    n = int(clamp((u - 2.4) / 6.0) ** 1.5 * 120)
    R = rng(7)
    for i in range(n):
        tt = 2.4 + 6.0 * (i / 120) ** (1 / 1.5)
        q = clamp((u - tt) / 3.0)
        sx, sy = 760, 780
        ex, ey = R.uniform(900, 2200), R.uniform(100, 1000)
        x = lerp(sx, ex, ease_out(q))
        y = lerp(sy, ey, ease_out(q)) - math.sin(q * math.pi) * 200
        s = lerp(0.4, 1.6, q)
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(R.uniform(-1, 1) * q * 2)
        ctx.scale(s, s)
        rrect(ctx, -50, -66, 100, 132, 3)
        setc(ctx, "#F2E6C8", 0.95 * (1 - q * 0.3))
        ctx.fill()
        for j in range(8):
            ctx.rectangle(-38, -52 + j * 13, 76 if j % 3 else 50, 4)
        setc(ctx, "#3A2A1A", 0.6)
        ctx.fill()
        ctx.restore()
    film.vignette(ctx, 0.6)
    # 计数（压在纸页上面）
    k = smooth(prog(u, 3.4, 4.0))
    cnt = 20000000 * ease_out(prog(u, 3.4, 6.4))
    ctx.set_source(rad(1480, 450, 0, 420, [(0, "#0A0604", 0.75 * k), (1, "#0A0604", 0)]))
    ctx.paint()
    label(ctx, f"{cnt / 1e4:,.0f} 万册", 1480, 420, 84, "#FFE8C0", k, "serif_k")
    label(ctx, "1450 → 1500 年 · 欧洲印刷的书", 1480, 500, 30, "#E9D9BE", k, "serif_r")


# ================================================================ 主绘制


def draw(ctx, t):
    if t < 8.6:
        _shot_a1(ctx, t)
    elif t < 14.5:
        _shot_a2(ctx, t)
    elif t < 18.5:
        _shot_b1(ctx, t)
    elif t < 22.5:
        _shot_b2(ctx, t)
    elif t < 32.0:
        _shot_c(ctx, t)
    else:
        _shot_d(ctx, t)


def sfx():
    return [
        (0.0, "ambience_room", {"dur": 8.6, "gain": 0.5}),
        (0.0, "ambience_night", {"dur": 8.6, "gain": 0.25}),
        (2.0, "page", {"gain": 0.3}), (4.4, "page", {"gain": 0.25}), (6.2, "quill", {"dur": 2.0, "gain": 0.25}),
        (8.6, "ambience_room", {"dur": 5.9, "gain": 0.4}),
        (9.0, "quill", {"dur": 1.6, "gain": 0.3}), (10.4, "quill", {"dur": 1.6, "gain": 0.3}),
        (11.6, "swish", {"gain": 0.18}), (12.2, "swish", {"gain": 0.18}),
        (14.5, "ambience_room", {"dur": 4.0, "gain": 0.4}),
        (14.7, "blip", {"gain": 0.12}), (15.4, "blip", {"gain": 0.12, "pitch": 1.1}),
        (16.1, "blip", {"gain": 0.12, "pitch": 1.2}), (16.8, "blip", {"gain": 0.12, "pitch": 1.3}),
        (18.5, "ambience_cave", {"dur": 4.0, "gain": 0.35}), (18.8, "hush", {"dur": 1.5, "gain": 0.25}),
        (22.5, "caravan", {"dur": 9.5, "gain": 0.5}), (22.5, "ambience_wind", {"dur": 9.5, "gain": 0.3}),
        (22.7, "paper", {"gain": 0.2}), (23.3, "stone_click", {"gain": 0.2}), (23.9, "brass", {"gain": 0.2}),
        (24.5, "crackle", {"dur": 0.5, "gain": 0.2}),
        (32.0, "ambience_room", {"dur": 10.0, "gain": 0.45}),
        (32.1, "press", {"gain": 0.6}), (33.5, "press", {"gain": 0.55}),
        (34.4, "pages_flurry", {"dur": 2.0, "gain": 0.35}), (36.4, "pages_flurry", {"dur": 2.4, "gain": 0.45}),
        (38.8, "pages_flurry", {"dur": 3.0, "gain": 0.55}),
    ]
