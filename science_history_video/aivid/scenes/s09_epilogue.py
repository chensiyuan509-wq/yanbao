"""尾声：光河从史前一路亮到今天；镜头拉远，八个"方法"浮现，整条光河原来是一只手；
第一视角伸手触碰星座，洞壁手印与之重叠；片尾字卡。"""
import math

from ..core import (TAU, H, W, circle, clamp, ease_in, ease_io, ease_out, glow, lerp, lin, prog, rad, ring_burst,
                    setc, smooth, view)
from .. import film, starmap
from .common import fade_io, label, lit

DUR = 32.0
CHAPTER = None
GRAIN = 0.07

VO = [
    (0.9, "回头看，科学从来不是几个天才的{灵光一现}。"),
    (4.4, "它是一场几十万年的接力：观察、记录、证明、传承、实验、预言、协作、学习……"),
    (9.6, "每一棒，都交到了{下一个人}的手里。"),
    (14.2, "几万年前，人在洞壁上留下手印，像是在说：{我来过}。"),
    (18.6, "而科学最珍贵的，不是答案，是那一句：{为什么？}"),
    (24.3, "保持好奇，保持怀疑——"),
    (26.9, "这是人类教给我的{第一课}。", {"spill": 1.0}),
]

SUPERS = []

HAND_C = (0.41 * starmap.S, 0.55 * starmap.S)


def _cam_a(t):
    lit_u = ease_io(prog(t, 0.2, 9.0))
    pull = ease_io(prog(t, 4.5, 12.5))
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


def _shot_a(ctx, t):
    cam, lit_u = _cam_a(t)
    _space(ctx, t, cam)
    z = cam[2]
    with view(ctx, cam, 1.0):
        starmap.draw_map(ctx, t, 1.0, lit=lit_u, label_a=smooth((z - 0.36) / 0.18), zoom=z,
                         methods_a=smooth(prog(t, 6.0, 9.5)))
    film.vignette(ctx, 0.55)


def _shot_b(ctx, t):
    """第一视角：抬手触碰手形星座。"""
    u = t - 14.0
    cam = (HAND_C[0], HAND_C[1] + 40, 0.2 + 0.015 * ease_io(prog(u, 0, 10)), 0.0)
    _space(ctx, t, cam)
    with view(ctx, cam, 1.0):
        starmap.draw_map(ctx, t, 1.0, lit=1.0, label_a=0.0, zoom=cam[2], methods_a=0.6)
        # 洞壁手印的影子与星座重叠
        sk = smooth(prog(u, 1.4, 3.4)) * (1 - 0.5 * smooth(prog(u, 7.0, 9.5)))
        if sk > 0:
            ctx.save()
            starmap.hand_outline(ctx, 0, 0, 0.82 * starmap.S)
            ctx.set_source(rad(HAND_C[0], HAND_C[1], 0, 2000, [(0, "#C2502E", 0.35 * sk), (1, "#C2502E", 0)]))
            ctx.fill()
            ctx.restore()
    # 手臂伸向星座
    reach = ease_out(prog(u, 0.4, 3.2))
    tip = (lerp(1120, 1010, reach), lerp(1300, 640, reach) + math.sin(t * 1.2) * 6)
    touch = smooth(prog(u, 3.0, 3.6))
    if touch > 0:
        glow(ctx, tip[0] - 10, tip[1] - 80, 420, "#FFE2A8", 0.4 * touch)
        ring_burst(ctx, t, 14.0 + 3.1, tip[0] - 10, tip[1] - 80, 20, 520, "#FFE8C0", 1.6, 6, 0.8)
        ring_burst(ctx, t, 14.0 + 3.5, tip[0] - 10, tip[1] - 80, 20, 520, "#FFE8C0", 1.6, 4, 0.6)
    with lit("#FFE2B0", 0.3, 0.7 + 0.3 * touch):
        film.pov_arm(ctx, (1500, 1400), tip, 160)
    film.embers(ctx, t, tip[0], tip[1] - 60, 18, 3, spread=200, height=400, color="#FFE2A8", a=touch * 0.9, size=3)
    film.vignette(ctx, 0.55)
    # 片尾前慢慢变暗
    film.fade_black(ctx, smooth(prog(u, 8.6, 10.0)))


def _shot_c(ctx, t):
    u = t - 24.0
    ctx.set_source(rad(W / 2, 760, 0, 1100, [(0, "#24120A"), (0.5, "#0E0806"), (1, "#020101")]))
    ctx.paint()
    film.embers(ctx, t, W / 2, 900, 30, 21, spread=900, height=900, color="#FFA14A", a=0.8, size=3.2, speed=0.2)
    k1 = smooth(prog(u, 0.2, 1.6))
    foc = ease_out(prog(u, 0.2, 1.8))
    for dx, al in ((0, 1.0), (-8, 0.3), (8, 0.3)):
        if dx and foc > 0.98:
            continue
        film.tracked(ctx, "星火", W / 2 + dx * (1 - foc), 420, 200, "#FFF1DC",
                     k1 * al * (1 if dx == 0 else 1 - foc), "serif_k", 0.25)
    k2 = smooth(prog(u, 1.4, 2.4))
    lw = 480 * ease_io(prog(u, 1.2, 2.4))
    ctx.rectangle(W / 2 - lw / 2, 560, lw, 2)
    setc(ctx, "#D9B26A", 0.9 * k2)
    ctx.fill()
    film.tracked(ctx, "保持好奇 · 保持怀疑", W / 2, 620, 44, "#F1E4CC", k2, "serif_m", 0.2)
    film.tracked(ctx, "致每一个提出问题的人", W / 2, 690, 30, "#C9AE7E", smooth(prog(u, 2.6, 3.6)), "serif_l", 0.2)
    film.vignette(ctx, 0.5)
    film.fade_black(ctx, smooth(prog(u, 6.6, 8.0)))


def draw(ctx, t):
    if t < 14.0:
        _shot_a(ctx, t)
    elif t < 24.0:
        _shot_b(ctx, t)
    else:
        _shot_c(ctx, t)


def sfx():
    return [
        (0.0, "ambience_space", {"dur": 24.0, "gain": 0.5}),
        (0.3, "stream", {"dur": 8.5, "gain": 0.2}),
        (2.0, "shimmer", {"dur": 2.0, "gain": 0.15}),
        (6.2, "chime", {"gain": 0.12}), (7.0, "chime", {"gain": 0.12}), (7.8, "chime", {"gain": 0.12}),
        (8.6, "chime", {"gain": 0.12}),
        (9.0, "swell", {"dur": 3.5, "gain": 0.3}),
        (12.4, "boom", {"gain": 0.45}),
        (14.4, "hush", {"dur": 3.0, "gain": 0.3}),
        (16.9, "impact_soft", {"gain": 0.4}), (17.0, "shimmer", {"dur": 2.5, "gain": 0.3}),
        (19.0, "heartbeat", {"n": 2, "gain": 0.3}),
        (24.0, "ambience_fire", {"dur": 8.0, "gain": 0.35}),
        (24.2, "boom", {"gain": 0.5}),
    ]
