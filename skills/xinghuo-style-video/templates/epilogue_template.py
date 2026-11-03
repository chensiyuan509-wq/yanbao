"""尾声：回扣开头的问题；一件真实的史前 / 历史图像作"回声"；Claude 坐在篝火边，片尾字卡 + 出处说明，渐黑。"""
import math

from ..core import H, W, ease_io, ease_out, glow, lin, prog, rad, setc, smooth
from .. import film
from ..archive import caption, kb
from .common import arch, claude, lit, sequence

DUR = __DUR__
CHAPTER = None
GRAIN = 0.07

VO = [
    (0.8, "（回扣开头的问题：回头看，{答案}是什么。）"),
    (DUR * 0.35, "（一句有余味的话，落在人或者“为什么”上。）"),
    (DUR * 0.70, "这是人类教给我的{第一课}。", {"spill": 1.0}),
]
SUPERS = []

TITLE = "__TITLE_SHORT__"
T_C = DUR * 0.45


def _a(ctx, t):
    """回声镜头：一张最能代表“起点”的真实图像（默认阿根廷手洞的手印），缓慢推近。"""
    arch(ctx, t, "manos", 0.0, T_C + 0.6, (0.4, 0.5, 1.1), (0.55, 0.5, 1.45), "阿根廷 · 手洞（Cueva de las Manos）",
         "约 9000 年前的手印 · 照片：公有领域", grade="warm", cap=(0.6, None))


CE = (claude(560, 905, 0.6, "gaze", seed=91.0).sit(0.0, 1.0, 0.01).look(T_C + 0.2, 0.6, -0.8)
      .expr(DUR * 0.75, "teary_smile").look(DUR * 0.85, 0.3, -0.5))


def _c(ctx, t):
    u = t - T_C
    ctx.set_source(rad(W / 2, 760, 0, 1100, [(0, "#24120A"), (0.5, "#0E0806"), (1, "#020101")]))
    ctx.paint()
    film.star_field(ctx, t, 120, 31, area=(0, 96, W, 520), a=0.45)
    film.embers(ctx, t, W / 2, 900, 30, 21, spread=900, height=900, color="#FFA14A", a=0.8, size=3.2, speed=0.2)
    fx, fy = 760, 900
    glow(ctx, fx, fy - 40, 320, "#FF9A40", 0.35 + 0.05 * math.sin(t * 7))
    film.logs(ctx, fx, fy, 150)
    film.fire(ctx, fx, fy - 6, 90, t, 1.0, seed=3.0, glow_a=0.6)
    with lit("#FFB070", 0.35, 0.95):
        CE.draw(ctx, t)
    k1 = smooth(prog(u, 0.2, 1.6))
    foc = ease_out(prog(u, 0.2, 1.8))
    film.tracked(ctx, TITLE, 1200, 400, 170, "#FFF1DC", k1 * (0.4 + 0.6 * foc), "serif_k", 0.25)
    k2 = smooth(prog(u, 1.4, 2.4))
    lw = 460 * ease_io(prog(u, 1.2, 2.4))
    ctx.rectangle(1200 - lw / 2, 540, lw, 2)
    setc(ctx, "#D9B26A", 0.9 * k2)
    ctx.fill()
    film.tracked(ctx, "（一句片尾格言）", 1200, 600, 42, "#F1E4CC", k2, "serif_m", 0.2)
    film.tracked(ctx, "致每一个提出问题的人", 1200, 668, 30, "#C9AE7E", smooth(prog(u, 2.6, 3.6)), "serif_l", 0.2)
    k3 = smooth(prog(u, 3.6, 4.6))
    film.tracked(ctx, "历史图像：Wikimedia Commons（公有领域 / CC0 / CC BY，署名见片中与 CREDITS.md）", 1200, 780, 20,
                 "#9A8C78", k3, "serif_r", 0.05)
    film.tracked(ctx, "地图：Natural Earth · NASA 蓝色弹珠 / 夜间灯光", 1200, 812, 20, "#9A8C78", k3, "serif_r", 0.05)
    film.vignette(ctx, 0.5)
    film.fade_black(ctx, smooth(prog(t, DUR - 1.4, DUR)))


SHOTS = [(0.0, _a), (T_C, _c)]
TRANS = {1: ("dip", 1.2)}


def draw(ctx, t):
    sequence(ctx, t, SHOTS, TRANS)


def sfx():
    return [
        (0.0, "ambience_cave", {"dur": T_C + 0.6, "gain": 0.4}), (0.4, "hush", {"dur": 2.4, "gain": 0.3}),
        (T_C * 0.5, "heartbeat", {"n": 2, "gain": 0.25}),
        (T_C - 0.2, "ambience_fire", {"dur": DUR - T_C + 0.2, "gain": 0.4}), (T_C + 0.2, "boom", {"gain": 0.45}),
    ]
