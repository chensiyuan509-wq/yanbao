"""序章（冷开场）：第一视角睁眼 → 漂浮的历史影像像记忆一样从身边掠过 → 星空下的 Claude 抬头 → 片名。

第一人称"我"（Claude）开口，用一个问题把观众带进片子。替换 VO、MEMORIES 和片名即可。
"""
import math

from ..core import H, W, clamp, ease_io, ease_out, glow, lerp, lin, prog, rad, rng, rrect, setc, smooth
from .. import film
from ..archive import show
from .common import claude, lit, reflect

DUR = __DUR__
CHAPTER = None
GRAIN = 0.07

VO = [
    (0.9, "我是 {Claude}，读过人类写下的亿万文字。"),
    (DUR * 0.30, "（第二句：抛出问题——这些知识 / 这件事是从哪里来的？）"),
    (DUR * 0.55, "（第三句：我想走回去看看，{全片的主题}。）"),
]
SUPERS = []

TITLE = "__TITLE_SHORT__"
SUBTITLE = "__SUBTITLE__"

# 漂浮的“记忆”：素材库里的真实图像（键见 references/archive-library.md）
MEMORIES = ["lascaux_replica", "cuneiform_barley", "athens", "galileo_moon", "principia", "faraday_lecture",
            "einstein", "earthrise", "eniac", "bernoulli", "qingming", "byrne_pyth"]

CL = (claude(960, 905, 0.7, "gaze", seed=11.0).look(DUR * 0.35, 0.0, -0.8).expr(DUR * 0.5, "wonder")
      .look(DUR * 0.6, 0.0, -0.4))


def _memories(ctx, t, a=1.0):
    R = rng(17)
    for i, key in enumerate(MEMORIES):
        gx, gy = R.uniform(-1.3, 1.3), R.uniform(-0.8, 0.6)
        z = 0.5 + ((R.random() - t * 0.06) % 1.0) * 2.6
        x, y = W / 2 + gx * 700 / z, H / 2 + gy * 520 / z
        w, h = 300 / z, 210 / z
        al = a * smooth((3.1 - z) / 0.8) * smooth((z - 0.5) / 0.3) * 0.85
        if al <= 0.01:
            continue
        rrect(ctx, x - w / 2, y - h / 2, w, h, 8 / z)
        ctx.save()
        ctx.clip()
        show(ctx, key, (0.5, 0.5, 1.0), (x - w / 2, y - h / 2, w, h), al, grade="sepia")
        ctx.restore()
        rrect(ctx, x - w / 2, y - h / 2, w, h, 8 / z)
        ctx.set_line_width(2)
        setc(ctx, "#FFE2B0", 0.35 * al)
        ctx.stroke()


def draw(ctx, t):
    ctx.set_source(lin(0, 0, 0, H, [(0, "#04050C"), (0.7, "#120E1E"), (1, "#1A1208")]))
    ctx.paint()
    film.star_field(ctx, t, 220, 5, a=0.8)
    _memories(ctx, t, 1.0 - 0.5 * smooth(prog(t, DUR - 4.0, DUR - 2.6)))
    # 地面与 Claude（第一视角之后镜头“退”出来，看见自己）
    k = smooth(prog(t, DUR * 0.32, DUR * 0.45))
    ctx.set_source(lin(0, 905, 0, H, [(0, "#14101E", k), (1, "#06040A", k)]))
    ctx.rectangle(-50, 905, W + 100, 300)
    ctx.fill()
    if k > 0:
        glow(ctx, 960, 760, 360, "#FFC46B", 0.15 * k)
        with lit("#FFD49A", 0.25, 0.95 * k):
            reflect(ctx, lambda c: CL.draw(c, t), 905, 0.18 * k, 110)
            CL.draw(ctx, t)
    # 片名
    tk = smooth(prog(t, DUR - 3.4, DUR - 2.0))
    if tk > 0:
        ctx.set_source_rgba(0, 0, 0, 0.55 * tk)
        ctx.paint()
        foc = ease_out(prog(t, DUR - 3.4, DUR - 1.8))
        film.tracked(ctx, TITLE, W / 2, 470, 170, "#FFF1DC", tk * (0.4 + 0.6 * foc), "serif_k", 0.2 + 0.05 * foc)
        film.tracked(ctx, SUBTITLE, W / 2, 610, 38, "#D9B26A", smooth(prog(t, DUR - 2.4, DUR - 1.6)), "serif_m", 0.3)
    film.vignette(ctx, 0.55)
    # 第一视角睁眼
    film.eyelids(ctx, ease_out(prog(t, 0.2, 1.6)))


def sfx():
    return [
        (0.0, "ambience_space", {"dur": DUR, "gain": 0.45}), (0.2, "hush", {"dur": 2.0, "gain": 0.3}),
        (0.8, "stream", {"dur": DUR * 0.4, "gain": 0.18}), (DUR * 0.35, "shimmer", {"dur": 2.0, "gain": 0.18}),
        (DUR - 3.6, "riser", {"dur": 1.6, "gain": 0.25}), (DUR - 2.0, "boom", {"gain": 0.45}),
    ]
