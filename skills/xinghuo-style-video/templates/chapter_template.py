"""__NUM__ __TITLE__：（一句话写清这一章讲什么、用了哪些真实图像、Claude 在哪里出场）。关键词：__KEY__。

这是脚手架生成的章节骨架，五个镜头演示了星火风格最常用的构图，替换成本章的真实内容即可：
  A 博物馆长廊：Claude 走进展厅，镜头推进画框，画心铺满后无缝接 B
  B 档案推拉（Ken Burns）+ 右侧信息面板（3–4 行，带年份和数字）
  C 蓝图原理图 + 编号步骤（讲"怎么做到的 / 怎么被证明的"）
  D 展品卡片一排（真实器物照片 + 年份 + 名称 + 两行原理 / 应用）
  E 卫星地图：城市亮起、航线描出（讲"在哪里、怎么传播"）
"""
import math

from ..core import H, W, circle, clamp, ease_io, glow, lerp, prog, rad, rrect, setc, smooth, stroke_pts, text
from .. import film, oldmap
from ..archive import caption, framed, kb
from ..exhibit import blueprint_bg, card, panel
from ..gallery import Gallery
from .common import arch, claude, label, lit, role, sequence

DUR = __DUR__
CHAPTER = dict(num="__NUM__", title="__TITLE__", era="__ERA__", key="__KEY__", at=0.4, dur=4.0, x=620)
GRAIN = 0.07

# 字幕（场景内本地秒）：一句一个事实，带年份 / 数字；{} 里是金色高亮；每句 ≲ 8 字/秒
VO = [
    (DUR * 0.10, "（第一句：时间、地点、人物——发生了什么。{高亮关键词}）"),
    (DUR * 0.30, "（第二句：用真实图像讲细节，给出一个具体数字。）"),
    (DUR * 0.48, "（第三句：原理——它是怎么做到的 / 怎么被证明的。）"),
    (DUR * 0.66, "（第四句：落地应用，今天的什么东西来自它。）"),
    (DUR * 0.84, "（第五句：它从哪里传到了哪里，交给了{下一棒}。）", {"spill": 0.4}),
]

# 左上角打字机式的年代 / 地点字幕
SUPERS = [(DUR * 0.30 + 0.2, DUR * 0.30 + 3.4, "（年份）", "（地点 · 事件）")]

T_B, T_C, T_D, T_E = DUR * 0.28, DUR * 0.46, DUR * 0.64, DUR * 0.82

# ---------------------------------------------------------------- A：博物馆长廊

VIS = (claude(300, 905, 0.55, "curious", seed=__SEED__).walk_to(1.0, 3.4, 860, 905, stride=0.8)
       .look(3.5, 0.3, -0.9).expr(3.7, "awe"))
HALL = Gallery([("__HALL_KEY__", "（作品名）", "（年代 · 作者 · 授权）")], VIS, 3.6, T_B, push=0, push_dur=1.4,
               lead=420)


def _a(ctx, t):
    with lit("#FFE2B0", 0.15, 0.95):
        HALL.draw(ctx, t)


# ---------------------------------------------------------------- B：档案推拉 + 信息面板


def _b(ctx, t):
    u = t - T_B
    arch(ctx, t, "__HALL_KEY__", T_B, T_C + 0.5, (0.5, 0.5, 1.02), (0.42, 0.45, 1.5), "（图像标题）",
         "（年代 · 作者 · 公有领域）", cap=(0.4, None))
    k = smooth(prog(u, 0.6, 1.1))
    panel(ctx, 1220, 190, 600, 330, k)
    text(ctx, "（面板标题）", 1520, 245, 30, "#D9B26A", k, "serif_sb")
    for i, s in enumerate(("（要点一：年份 + 数字）", "（要点二）", "（要点三）")):
        text(ctx, s, 1260, 315 + i * 60, 28, "#F6EEDF", smooth(prog(u, 0.9 + i * 0.4, 1.4 + i * 0.4)), "serif_sb", "l")


# ---------------------------------------------------------------- C：蓝图原理图


def _c(ctx, t):
    u = t - T_C
    blueprint_bg(ctx, W, H, t)
    cx, cy = 720, 560
    # 示意：一个转动的轮 + 流动的光点（换成本章的原理动画）
    ctx.set_line_width(4)
    setc(ctx, "#7FD8FF", 0.8)
    circle(ctx, cx, cy, 220)
    ctx.stroke()
    for i in range(12):
        a = i / 12 * math.tau + u * 0.8
        glow(ctx, cx + math.cos(a) * 220, cy + math.sin(a) * 220, 18, "#BFEFFF", 0.7)
    stroke_pts(ctx, [(cx - 300, cy), (cx + 300, cy)], 3, "#7FD8FF", 0.4)
    text(ctx, "（原理图标题 · 年份）", cx, 200, 32, "#E8F2FF", smooth(prog(u, 0.1, 0.6)), "serif_k")
    panel(ctx, 1240, 260, 580, 420, smooth(prog(u, 0.3, 0.8)), "#7FC8FF")
    for i, s in enumerate(("① （第一步）", "② （第二步）", "③ （结果 / 数字）")):
        k = smooth(prog(u, 0.6 + i * 0.5, 1.1 + i * 0.5))
        text(ctx, s, 1280, 340 + i * 100, 30, "#FFD27A" if i == 2 else "#E8F2FF", k, "serif_sb", "l")


# ---------------------------------------------------------------- D：展品卡片

CARDS = [("gramme", "（年份）", "（名称）", ("（原理一行）", "（应用一行）"), (0.5, 0.5, 1.2)),
         ("edison_bulb", "（年份）", "（名称）", ("（原理一行）", "（应用一行）"), (0.5, 0.45, 1.3)),
         ("bell_phone", "（年份）", "（名称）", ("（原理一行）", "（应用一行）"), (0.5, 0.5, 1.1))]


def _d(ctx, t):
    u = t - T_D
    ctx.set_source(rad(960, 500, 0, 1300, [(0, "#1E1A20"), (1, "#060508")]))
    ctx.paint()
    film.paint_texture(ctx, "stone", 0, 0, W, H, 0.08, scale=0.5)
    z = 1 + 0.04 * ease_io(prog(u, 0, T_E - T_D))
    ctx.save()
    ctx.translate(960, 520)
    ctx.scale(z, z)
    ctx.translate(-960, -520)
    for i, (key, year, title, lines, crop) in enumerate(CARDS):
        k = clamp((u - 0.2 - i * 0.4) / 0.6)
        hot = smooth(prog(u, 0.8 + i * 0.9, 1.2 + i * 0.9)) * (1 - smooth(prog(u, 1.9 + i * 0.9, 2.3 + i * 0.9)))
        card(ctx, key, 420 + i * 540, 520, 480, 620, year, title, lines, 1.0, k, crop, t, hot)
    ctx.restore()
    text(ctx, "（这一排展品的总标题）", 960, 165, 32, "#D9B26A", smooth(prog(u, 0.0, 0.6)), "serif_sb")
    film.vignette(ctx, 0.45)


# ---------------------------------------------------------------- E：卫星地图

MCAM = oldmap.MapCam([(T_E, (60.0, 36.0, 11.0)), (DUR + 0.5, (40.0, 38.0, 9.0), ease_io)])
ROUTE = [(108.9, 34.3), (94.7, 40.1), (66.9, 39.65), (44.4, 33.3), (28.98, 41.0)]


def _e(ctx, t):
    u = t - T_E
    cam = MCAM.at(t)
    oldmap.draw_satellite(ctx, cam, t, 1.0, "day", "warm", coast=0.18, grid=0.05)
    oldmap.route(ctx, cam, ROUTE, ease_io(prog(u, 0.3, 2.6)), "#FFD27A", 1.0, 5, t=t)
    for nm, t0 in (("长安", 0.3), ("敦煌", 0.8), ("撒马尔罕", 1.4), ("巴格达", 1.9), ("君士坦丁堡", 2.4)):
        oldmap.city_sat(ctx, cam, nm, smooth(prog(u, t0, t0 + 0.4)), 1.0, size=26, t=t, pulse=False)
    oldmap.sat_vignette(ctx, 0.6)
    film.grade(ctx, "#FFB070", 0.08)


SHOTS = [(0.0, _a), (T_B, _b), (T_C, _c), (T_D, _d), (T_E, _e)]
TRANS = {2: ("luma", 0.9), 3: ("lightsweep", 0.9, {"color": "#FFE2B0"}), 4: ("dissolve", 1.0)}


def draw(ctx, t):
    sequence(ctx, t, SHOTS, TRANS)


def sfx():
    return [
        (0.0, "ambience_room", {"dur": T_B, "gain": 0.35}),
        (T_B - 1.4, "whoosh", {"dur": 1.4, "gain": 0.15}),
        (T_B, "ambience_room", {"dur": T_C - T_B, "gain": 0.3}), (T_B + 0.3, "shutter", {"gain": 0.3}),
        (T_C, "hum", {"dur": T_D - T_C, "gain": 0.18}), (T_C + 0.2, "zap", {"dur": 0.6, "gain": 0.1}),
        (T_D, "ambience_room", {"dur": T_E - T_D, "gain": 0.3}),
        (T_D + 0.9, "pop", {"gain": 0.18}), (T_D + 1.8, "pop", {"gain": 0.18, "pitch": 1.12}),
        (T_D + 2.7, "pop", {"gain": 0.18, "pitch": 1.24}),
        (T_E, "ambience_wind", {"dur": DUR - T_E + 0.5, "gain": 0.3}), (T_E + 0.3, "caravan", {"dur": 2.4, "gain": 0.25}),
    ]
