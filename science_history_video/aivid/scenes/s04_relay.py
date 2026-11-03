"""第四章 薪火相传：《玛卡梅》插图里的图书馆；花拉子米手稿与配方法 x² + 10x = 39；
伊本·海赛姆《光学宝库》；数字 0 的旅程；《清明上河图》与活字印刷；丝绸之路；1568 年的印刷作坊木刻与古腾堡圣经。
关键词：传承。"""
import math

from ..core import (TAU, H, W, arrow, at, circle, clamp, ease_io, ease_out, ellipse, glow, lerp, lin, mix, poly,
                    polyline_partial, prog, rad, rng, rrect, setc, smooth, stroke_pts, text)
from .. import film, oldmap, proofs
from ..archive import caption, framed, kb
from .common import arch, label, lit, role, sequence

DUR = 38.0
CHAPTER = dict(num="第 四 章", title="薪火相传", era="约公元 500 — 1450 年", key="传承", at=0.4, dur=4.0)
GRAIN = 0.09

VO = [
    (4.6, "9 世纪的巴格达，'{智慧之家}'把希腊、波斯、印度的典籍译成阿拉伯文。"),
    (9.4, "花拉子米的《代数学》这样解 x² + 10x = 39："),
    (12.6, "补一个 5×5 的方块：(x+5)² = 64，{x = 3}。"),
    (15.4, "'代数'和'算法'两个词，都来自他。"),
    (17.4, "伊本·海赛姆用暗室实验证明：光是{射进眼睛}的；"),
    (20.8, "印度人发明的 {0}，也经阿拉伯世界传到了欧洲。"),
    (24.3, "在中国，宋代的毕昇发明了{活字印刷}；"),
    (27.6, "造纸、印刷、指南针、火药，沿丝绸之路{一路西传}。"),
    (31.4, "1450 年前后，古腾堡的印刷机让书变得便宜："),
    (34.4, "50 年里，欧洲印出了{两千多万册}书——知识第一次能被大规模复制。", {"spill": 0.6}),
]

SUPERS = []


def _shot_a(ctx, t):
    arch(ctx, t, "maqamat_library", 0.0, 9.0, (0.5, 0.5, 1.05), (0.5, 0.45, 1.5), "哈里里《玛卡梅》插图：图书馆里的学者",
         "瓦西提绘 · 1237 年 · 法国国家图书馆 · 公有领域", grade="warm", cap=(4.6, 8.6))
    for k in range(14):
        u = (t * 0.3 + k / 14) % 1.0
        glow(ctx, lerp(500, 1450, u), 300 - math.sin(u * math.pi) * 120, 16, "#FFE2A8", 0.5 * math.sin(u * math.pi) *
             smooth(prog(t, 5.0, 5.6)))


TRANSLATOR = role(1720, 960, 0.4, "arab_scholar", "focused", seed=51.0, palette="amber", flip=True)


def _shot_b(ctx, t):
    if t < 11.0:
        arch(ctx, t, "khwarizmi", 9.0, 11.0, (0.5, 0.5, 1.05), (0.5, 0.5, 1.3), "花拉子米《代数学》抄本",
             "牛津博德利图书馆 · 公有领域", grade="warm", cap=(0.1, 1.9))
        return
    u = t - 11.0
    proofs.paper(ctx)
    proofs.complete_square(ctx, u)
    proofs.eq(ctx, "花拉子米的配方法（约 820 年）", 110, 175, 34, proofs.INK, smooth(prog(u, 0, 0.5)), "l", "serif_k")
    k = smooth(prog(u, 4.6, 5.2))
    if k > 0:
        rrect(ctx, 1060, 720, 760, 170, 16)
        setc(ctx, "#E6D9BA", 0.95 * k)
        ctx.fill()
        proofs.eq(ctx, "al-jabr → algebra 代数", 1090, 772, 34, proofs.INK, k, "l", "serif_sb")
        proofs.eq(ctx, "al-Khwārizmī → algorithm 算法", 1090, 840, 34, proofs.RED, k, "l", "serif_sb")
    TRANSLATOR.draw(ctx, t)
    film.vignette(ctx, 0.35, color="#2A1A0A")


SCRIPTS = [("婆罗米", "brahmi", ["𑁦", "𑁧", "𑁨", "𑁩", "𑁪", "𑁫", "𑁬", "𑁭", "𑁮", "𑁯"]),
           ("天城体", "deva", ["०", "१", "२", "३", "४", "५", "६", "७", "८", "९"]),
           ("东阿拉伯", "arabic", ["٠", "١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩"]),
           ("今天", "latin", ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])]


def _shot_c(ctx, t):
    if t < 20.8:
        arch(ctx, t, "opticae", 17.0, 20.8, (0.5, 0.5, 1.05), (0.5, 0.6, 1.45), "《光学宝库》扉页（海赛姆《光学之书》拉丁文版）",
             "巴塞尔 · 1572 年 · 公有领域", grade="warm", cap=(0.2, 3.5))
        k = smooth(prog(t, 18.2, 18.8))
        label(ctx, "光沿直线进入眼睛 · 小孔成像 · 反射与折射", 960, 210, 34, "#FFE8C0", k, "serif_sb")
        return
    u = t - 20.8
    ctx.set_source(rad(960, 540, 0, 1200, [(0, "#2A2018"), (1, "#0A0806")]))
    ctx.paint()
    film.paint_texture(ctx, "paper", 0, 0, W, H, 0.1)
    for r_, (name, fnt, digs) in enumerate(SCRIPTS):
        y = 280 + r_ * 160
        k = smooth(prog(u, 0.1 + r_ * 0.4, 0.5 + r_ * 0.4))
        label(ctx, name, 360, y, 32, "#CDBA92", k, "serif_r")
        for i, d in enumerate(digs):
            x = 620 + i * 120
            if i == 0 and k > 0:
                glow(ctx, x, y, 70, "#FFD27A", 0.4 * k)
            text(ctx, d, x, y, 76 if fnt != "brahmi" else 64, "#FFD27A" if i == 0 else "#FFE8C0", k, fnt)
    label(ctx, "0：让\"位值制\"成为可能（婆罗摩笈多，628 年）", 960, 920, 32, "#FFD27A", smooth(prog(u, 1.8, 2.4)), "serif_sb")
    film.vignette(ctx, 0.55)


SILK = [(108.9, 34.3), (103.8, 36.1), (98.5, 39.7), (94.7, 40.1), (88.0, 41.5), (80.0, 41.0), (76.0, 39.5),
        (71.0, 40.5), (67.0, 39.65), (61.8, 37.6), (54.0, 36.5), (51.4, 35.7), (44.4, 33.3), (38.8, 35.5),
        (36.3, 33.5), (35.5, 35.5), (29.0, 41.0), (23.0, 40.0), (19.0, 41.5), (12.33, 45.44)]
CCAM = oldmap.MapCam([(27.6, (95.0, 37.0, 13)), (31.0, (55.0, 38.0, 9.5), ease_io)])
INVENTIONS = [("纸", "105 年 · 蔡伦改进"), ("活字印刷", "1040 年代 · 毕昇"), ("指南针", "11 世纪"), ("火药", "9 世纪")]


def _shot_d(ctx, t):
    if t < 27.6:
        u = t - 24.0
        to = kb(ctx, "qingming", t, 24.0, 27.6, (0.15, 0.5, 1.0), (0.75, 0.5, 1.0))
        film.vignette(ctx, 0.5)
        caption(ctx, "张择端《清明上河图》（局部）", "北宋 · 描绘都城汴京（今开封）· 故宫博物院 · 公有领域",
                smooth(prog(u, 0.2, 0.7)) * (1 - smooth(prog(u, 3.1, 3.5))))
        k = smooth(prog(u, 0.8, 1.3))
        framed(ctx, "tiangong_paper", 1640, 380, 300, k)
        label(ctx, "《天工开物》造纸图（1637）", 1640, 580, 26, "#FFE8C0", k, "serif_sb")
        return
    cam = CCAM.at(t)
    oldmap.draw_satellite(ctx, cam, t, 1.0, "day", "warm", rivers=["yellow", "yangtze", "indus", "euphrates", "tigris",
                                                                    "nile", "danube"], coast=0.18, grid=0.05)
    p = ease_io(prog(t, 27.7, 30.6))
    oldmap.route(ctx, cam, SILK, p, "#FFD27A", 1.0, 5, t=t)
    for nm, t0 in (("长安", 27.7), ("敦煌", 28.2), ("撒马尔罕", 28.9), ("巴格达", 29.6), ("君士坦丁堡", 30.1),
                   ("威尼斯", 30.4)):
        oldmap.city_sat(ctx, cam, nm, smooth(prog(t, t0, t0 + 0.4)), 1.0, size=26, t=t, pulse=False)
    for i, (nm, sub) in enumerate(INVENTIONS):
        k = smooth(prog(t, 27.8 + i * 0.3, 28.2 + i * 0.3))
        x, y = 330 + i * 250, 200
        rrect(ctx, x - 110, y - 52, 220, 108, 14)
        setc(ctx, "#F6E8C6", 0.92 * k)
        ctx.fill()
        ctx.set_line_width(3)
        setc(ctx, "#8A4A1E", k)
        rrect(ctx, x - 110, y - 52, 220, 108, 14)
        ctx.stroke()
        text(ctx, nm, x, y - 12, 34, "#5A1E0E", k, "serif_k")
        text(ctx, sub, x, y + 28, 20, "#5A3A1E", k, "serif_r")
    oldmap.sat_vignette(ctx, 0.6)
    film.grade(ctx, "#FFB070", 0.08)


def _shot_e(ctx, t):
    if t < 34.4:
        arch(ctx, t, "printer_1568", 31.0, 34.4, (0.5, 0.45, 1.05), (0.45, 0.5, 1.35), "约斯特·安曼《印刷工》木刻",
             "《职业之书》· 1568 年 · 公有领域", grade="sepia", cap=(0.2, 3.1))
        return
    u = t - 34.4
    kb(ctx, "gutenberg_bible", t, 34.4, 38.0, (0.5, 0.5, 1.05), (0.4, 0.45, 1.4))
    film.vignette(ctx, 0.55)
    caption(ctx, "古腾堡圣经", "美因茨 · 约 1455 年 · 法国国家图书馆藏本 · CC0", smooth(prog(u, 0.1, 0.6)))
    k = smooth(prog(u, 0.6, 1.1))
    cnt = 20000000 * ease_out(prog(u, 0.6, 2.8))
    ctx.set_source(rad(1480, 420, 0, 420, [(0, "#0A0604", 0.75 * k), (1, "#0A0604", 0)]))
    ctx.paint()
    label(ctx, f"{cnt / 1e4:,.0f} 万册", 1480, 400, 84, "#FFE8C0", k, "serif_k")
    label(ctx, "1450 → 1500 年 · 欧洲印刷的书", 1480, 480, 30, "#E9D9BE", k, "serif_r")


SHOTS = [(0.0, _shot_a), (9.0, _shot_b), (17.0, _shot_c), (24.0, _shot_d), (31.0, _shot_e)]
TRANS = {1: ("dissolve", 1.0), 2: ("luma", 0.9), 3: ("lightsweep", 0.9, {"color": "#FFE2B0"}), 4: ("dissolve", 1.0)}


def draw(ctx, t):
    sequence(ctx, t, SHOTS, TRANS)


def sfx():
    return [
        (0.0, "ambience_room", {"dur": 9.0, "gain": 0.45}), (0.0, "ambience_night", {"dur": 9.0, "gain": 0.2}),
        (2.0, "page", {"gain": 0.3}), (5.0, "quill", {"dur": 2.4, "gain": 0.22}),
        (9.0, "ambience_room", {"dur": 8.0, "gain": 0.4}), (9.2, "page", {"gain": 0.25}),
        (11.2, "chalk", {"dur": 1.0, "gain": 0.2}), (13.6, "slide", {"gain": 0.2}), (15.4, "ding", {"gain": 0.25}),
        (17.0, "ambience_room", {"dur": 7.0, "gain": 0.4}), (17.4, "hush", {"dur": 1.5, "gain": 0.2}),
        (21.0, "blip", {"gain": 0.12}), (21.4, "blip", {"gain": 0.12, "pitch": 1.1}),
        (21.8, "blip", {"gain": 0.12, "pitch": 1.2}), (22.2, "blip", {"gain": 0.12, "pitch": 1.3}),
        (24.0, "ambience_birds", {"dur": 3.6, "gain": 0.3}), (24.0, "ambience_river", {"dur": 3.6, "gain": 0.25}),
        (27.6, "caravan", {"dur": 3.6, "gain": 0.5}), (27.8, "paper", {"gain": 0.2}), (28.4, "stone_click", {"gain": 0.2}),
        (28.7, "brass", {"gain": 0.2}), (29.0, "crackle", {"dur": 0.5, "gain": 0.2}),
        (31.0, "ambience_room", {"dur": 7.0, "gain": 0.45}), (31.2, "press", {"gain": 0.6}), (32.8, "press", {"gain": 0.55}),
        (34.6, "pages_flurry", {"dur": 2.0, "gain": 0.4}), (36.4, "pages_flurry", {"dur": 1.8, "gain": 0.5}),
    ]
