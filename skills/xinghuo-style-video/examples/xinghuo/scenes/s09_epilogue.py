"""尾声：光河从史前一路亮到今天，镜头拉远，八个"方法"浮现，整条光河原来是一只手；
第一视角伸手触碰星座，手洞里真实的古代手印与之重叠；Claude 坐在篝火旁，片尾字卡与出处说明。"""
import math

from ..core import H, W, clamp, ease_io, ease_out, glow, lerp, lin, prog, rad, ring_burst, setc, smooth, view
from .. import film, starmap
from ..archive import caption, show
from .common import claude, lit, sequence

DUR = 26.0
CHAPTER = None
GRAIN = 0.07

VO = [
    (0.8, "回头看，科学从来不是几个天才的{灵光一现}。"),
    (4.2, "它是几十万年的接力：观察、记录、证明、实验、协作……"),
    (8.9, "每一棒，都交到了{下一个人}手里。"),
    (11.8, "几万年前，人在洞壁上留下手印：{我来过}。"),
    (15.2, "科学最珍贵的，不是答案，而是那一句：{为什么？}"),
    (19.6, "保持好奇，保持怀疑——"),
    (22.0, "这是人类教给我的{第一课}。", {"spill": 1.0}),
]

SUPERS = []

HAND_C = (0.41 * starmap.S, 0.55 * starmap.S - 280)


def _cam_a(t):
    lit_u = ease_io(prog(t, 0.2, 6.6))
    pull = ease_io(prog(t, 3.0, 9.4))
    hx, hy = starmap.point(clamp(lit_u))
    cx = lerp(hx, HAND_C[0], pull)
    cy = lerp(hy, HAND_C[1], pull)
    z = lerp(0.62, 0.205, pull)
    return (cx, cy, z, 0.0), lit_u


def _space(ctx, t, cam):
    ctx.set_source(lin(0, 0, 0, H, [(0, "#04050C"), (1, "#100C22")]))
    ctx.paint()
    with view(ctx, cam, 0.6):
        starmap.draw_sky(ctx, t, 1.0)


def _a(ctx, t):
    cam, lit_u = _cam_a(t)
    _space(ctx, t, cam)
    z = cam[2]
    with view(ctx, cam, 1.0):
        starmap.draw_map(ctx, t, 1.0, lit=lit_u, label_a=smooth((z - 0.36) / 0.18), zoom=z,
                         methods_a=smooth(prog(t, 4.6, 7.6)))
    film.vignette(ctx, 0.55)


def _b(ctx, t):
    """第一视角：抬手触碰手形星座；手洞里的古代手印从星空里浮现。"""
    u = t - 9.4
    cam = (HAND_C[0], HAND_C[1] + 60, 0.205 + 0.015 * ease_io(prog(u, 0, 9)), 0.0)
    _space(ctx, t, cam)
    # 真实的手洞照片，像记忆一样叠在星空后面
    pk = smooth(prog(u, 2.0, 3.6)) * (1 - 0.6 * smooth(prog(u, 6.4, 8.4)))
    if pk > 0:
        ctx.push_group()
        show(ctx, "manos", (0.5 + 0.04 * prog(u, 0, 9), 0.5, 1.15 + 0.06 * prog(u, 0, 9)), (0, 0, W, H), 1.0,
             grade="warm")
        ctx.set_source(rad(W / 2, H / 2, 200, 1100, [(0, "#000000", 0), (1, "#000000", 1)]))
        ctx.paint()
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(0.55 * pk)
    with view(ctx, cam, 1.0):
        starmap.draw_map(ctx, t, 1.0, lit=1.0, label_a=0.0, zoom=cam[2], methods_a=0.6 * (1 - 0.6 * pk))
    caption(ctx, "阿根廷 · 手洞（Cueva de las Manos）", "约 9000 年前的手印 · 照片：公有领域",
            smooth(prog(u, 2.6, 3.2)) * (1 - smooth(prog(u, 6.0, 6.6))))
    # 手臂伸向星座
    reach = ease_out(prog(u, 0.3, 2.8))
    tip = (lerp(1120, 1010, reach), lerp(1300, 640, reach) + math.sin(t * 1.2) * 6)
    touch = smooth(prog(u, 2.6, 3.2))
    if touch > 0:
        glow(ctx, tip[0] - 10, tip[1] - 80, 420, "#FFE2A8", 0.4 * touch)
        ring_burst(ctx, t, 9.4 + 2.7, tip[0] - 10, tip[1] - 80, 20, 520, "#FFE8C0", 1.6, 6, 0.8)
        ring_burst(ctx, t, 9.4 + 3.1, tip[0] - 10, tip[1] - 80, 20, 520, "#FFE8C0", 1.6, 4, 0.6)
    with lit("#FFE2B0", 0.3, 0.7 + 0.3 * touch):
        film.pov_arm(ctx, (1500, 1400), tip, 160)
    film.embers(ctx, t, tip[0], tip[1] - 60, 18, 3, spread=200, height=400, color="#FFE2A8", a=touch * 0.9, size=3)
    film.vignette(ctx, 0.55)


# 片尾：Claude 坐在篝火边，抬头看字卡
CE = (claude(560, 905, 0.6, "gaze", seed=91.0).sit(18.0, 1.0, 0.01).look(18.8, 0.6, -0.8)
      .expr(22.2, "teary_smile").look(23.6, 0.3, -0.5))


def _c(ctx, t):
    u = t - 18.6
    ctx.set_source(rad(W / 2, 760, 0, 1100, [(0, "#24120A"), (0.5, "#0E0806"), (1, "#020101")]))
    ctx.paint()
    film.star_field(ctx, t, 120, 31, area=(0, 96, W, 520), a=0.45)
    film.embers(ctx, t, W / 2, 900, 30, 21, spread=900, height=900, color="#FFA14A", a=0.8, size=3.2, speed=0.2)
    # 一小堆篝火
    fx, fy = 760, 900
    glow(ctx, fx, fy - 40, 320, "#FF9A40", 0.35 + 0.05 * math.sin(t * 7))
    film.logs(ctx, fx, fy, 150)
    film.fire(ctx, fx, fy - 6, 90, t, 1.0, seed=3.0, glow_a=0.6)
    with lit("#FFB070", 0.35, 0.95):
        CE.draw(ctx, t)
    k1 = smooth(prog(u, 0.2, 1.6))
    foc = ease_out(prog(u, 0.2, 1.8))
    for dx, al in ((0, 1.0), (-8, 0.3), (8, 0.3)):
        if dx and foc > 0.98:
            continue
        film.tracked(ctx, "星火", 1200 + dx * (1 - foc), 400, 190, "#FFF1DC",
                     k1 * al * (1 if dx == 0 else 1 - foc), "serif_k", 0.25)
    k2 = smooth(prog(u, 1.4, 2.4))
    lw = 460 * ease_io(prog(u, 1.2, 2.4))
    ctx.rectangle(1200 - lw / 2, 540, lw, 2)
    setc(ctx, "#D9B26A", 0.9 * k2)
    ctx.fill()
    film.tracked(ctx, "保持好奇 · 保持怀疑", 1200, 600, 42, "#F1E4CC", k2, "serif_m", 0.2)
    film.tracked(ctx, "致每一个提出问题的人", 1200, 668, 30, "#C9AE7E", smooth(prog(u, 2.6, 3.6)), "serif_l", 0.2)
    k3 = smooth(prog(u, 3.6, 4.6))
    film.tracked(ctx, "历史图像：Wikimedia Commons（公有领域 / CC0 / CC BY，署名见片中与 CREDITS.md）", 1200, 780, 20,
                 "#9A8C78", k3, "serif_r", 0.05)
    film.tracked(ctx, "地图：Natural Earth · NASA 蓝色弹珠 / 夜间灯光", 1200, 812, 20, "#9A8C78", k3, "serif_r", 0.05)
    film.vignette(ctx, 0.5)
    film.fade_black(ctx, smooth(prog(u, 6.0, 7.4)))


SHOTS = [(0.0, _a), (9.4, _b), (18.6, _c)]
TRANS = {1: ("dissolve", 1.0, {"zoom": 0.03}), 2: ("dip", 1.2)}


def draw(ctx, t):
    sequence(ctx, t, SHOTS, TRANS)


def sfx():
    return [
        (0.0, "ambience_space", {"dur": 18.6, "gain": 0.5}),
        (0.3, "stream", {"dur": 6.5, "gain": 0.2}),
        (2.0, "shimmer", {"dur": 2.0, "gain": 0.15}),
        (4.8, "chime", {"gain": 0.12}), (5.5, "chime", {"gain": 0.12}), (6.2, "chime", {"gain": 0.12}),
        (6.9, "chime", {"gain": 0.12}),
        (7.0, "swell", {"dur": 2.8, "gain": 0.3}),
        (9.6, "hush", {"dur": 3.0, "gain": 0.3}),
        (12.0, "impact_soft", {"gain": 0.4}), (12.1, "shimmer", {"dur": 2.5, "gain": 0.3}),
        (14.6, "heartbeat", {"n": 2, "gain": 0.3}),
        (18.4, "ambience_fire", {"dur": 7.6, "gain": 0.4}),
        (18.8, "boom", {"gain": 0.45}),
    ]
