"""第一章（2/3）：海量文字飞进模型 → 镜头推进到模型内部 → 千亿个"参数旋钮"被拧准。"""
import math

from ..core import (TAU, W, H, Cam, at, bezier_pts, circle, clamp, ease_in, ease_io, ease_out,
                    fill, glow, kf, lerp, line, lin, point_on, pop, prog, rad, rng, rrect, setc,
                    smooth, stars, text, view, ring_burst, sparkle_burst)
from ..icons import (ic_book, ic_brain, ic_code, ic_paper, ic_qa, ic_web, ic_wiki, ic_chat)
from ..mascot import Puppet

DUR = 11.0
CHAPTER = ("01", "什么是大语言模型")

SUBS = [
    (0.5, 5.9, "为了接得准，它读过海量文字：网页、书籍、论文、代码……"),
    (6.1, 10.7, "{数十万亿}个字词里的规律，被「压缩」进了千亿个{参数}里。"),
]

OX, OY = 960, 470          # 模型球心（世界坐标）
OR = 165                   # 模型球半径
ICONS = [ic_web, ic_book, ic_paper, ic_code, ic_wiki, ic_qa, ic_chat]

_R = rng(21)
FLY = []                   # (开始时间, 图标, 起点, 控制点1, 控制点2, 大小)
for i in range(54):
    t0 = -0.4 + i * 0.105 + _R.uniform(-0.04, 0.04)
    ang = _R.uniform(0, TAU)
    r0 = _R.uniform(820, 1000)
    sx, sy = OX + math.cos(ang) * r0, OY + math.sin(ang) * r0 * 0.62
    c1 = (lerp(sx, OX, 0.35) + _R.uniform(-260, 260), lerp(sy, OY, 0.35) + _R.uniform(-200, 200))
    c2 = (lerp(sx, OX, 0.75) + _R.uniform(-120, 120), lerp(sy, OY, 0.75) + _R.uniform(-90, 90))
    FLY.append((t0, ICONS[i % len(ICONS)], (sx, sy), c1, c2, _R.uniform(96, 130)))
FLY_DUR = 1.7

# 参数旋钮网格（在模型球内部，放大后才看得清）
KN = []
for gy in range(-9, 10):
    for gx in range(-9, 10):
        if gx * gx + gy * gy <= 80:
            KN.append((gx, gy, _R.uniform(0, TAU), _R.uniform(-1.2, 1.2)))

P = (Puppet(330, 930, 0.52, "curious", seed=3.3)
     .look(0, 0.9, -0.7)
     .expr(1.4, "surprised").hop(1.5, 35)
     .expr(3.6, "excited").look(3.6, 0.8, -0.8))

CAM = Cam([
    (0.0, (960, 520, 0.98)),
    (5.6, (960, 500, 1.06)),
    (7.4, (OX, OY, 3.1, 0.05), ease_io),
    (11.0, (OX, OY, 3.35, 0.07)),
], drift=4, seed=6.0)


def draw(ctx, t):
    ctx.set_source(lin(0, 0, 0, H, [(0, "#0B1430"), (1, "#1B2B57")]))
    ctx.paint()
    cam = CAM.at(t)
    with view(ctx, cam, 0.25):
        stars(ctx, t, 90, 33, area=(-400, -300, W + 800, H + 600), a=0.6, size=(1, 2.4))
    with view(ctx, cam, 0.6):
        # 背景网格
        ctx.set_line_width(1.5)
        setc(ctx, "#5B7BD6", 0.12)
        for i in range(-10, 30):
            ctx.move_to(i * 100 - 500, -600)
            ctx.line_to(i * 100 - 500, 1700)
        for j in range(-6, 18):
            ctx.move_to(-600, j * 100)
            ctx.line_to(2500, j * 100)
        ctx.stroke()

    with view(ctx, cam):
        # 吸入的光带
        for (t0, icon, p0, c1, c2, sz) in FLY:
            u = (t - t0) / FLY_DUR
            if 0 < u < 1:
                pts = bezier_pts(p0, c1, c2, (OX, OY), 30)
                e = ease_in(u)
                (x, y), _ = point_on(pts, e)
                (xt, yt), _ = point_on(pts, max(0, e - 0.12))
                line(ctx, xt, yt, x, y, 6 * (1 - u * 0.6), "#9CC3FF", 0.35 * (1 - u))
        # 模型球
        n_in = sum(1 for f in FLY if t > f[0] + FLY_DUR)
        pulse = 0
        for f in FLY:
            d = t - (f[0] + FLY_DUR)
            if 0 < d < 0.3:
                pulse = max(pulse, 1 - d / 0.3)
        inside = smooth(prog(t, 6.3, 7.6))
        draw_orb(ctx, t, pulse, inside)
        for (t0, icon, p0, c1, c2, sz) in FLY:
            u = (t - t0) / FLY_DUR
            if 0 < u < 1:
                pts = bezier_pts(p0, c1, c2, (OX, OY), 30)
                (x, y), _ = point_on(pts, ease_in(u))
                k = (1 - ease_in(u) * 0.75) * min(1, u * 5)
                icon(ctx, x, y, sz * k, min(1, (1 - u) * 4), t)
        # 计数器
        ca = smooth(prog(t, 0.4, 0.9)) * (1 - smooth(prog(t, 5.8, 6.4)))
        if ca > 0:
            val = 30e12 * ease_io(prog(t, 0.5, 5.4)) ** 1.4
            s = f"{int(val):,}"
            text(ctx, "已读字词（token）", 960, 120, 30, "#9FB8F0", ca, "bold")
            text(ctx, s, 960, 180, 64, "#FFFFFF", ca, "black", shadow=(0, 4, "#000000", 0.3))
            if t > 5.3:
                text(ctx, "≈ 数十万亿", 960, 236, 30, "#FFC65C", ca * smooth(prog(t, 5.3, 5.6)), "black")
        P.draw(ctx, t)
        if inside > 0:
            draw_knobs(ctx, t, inside)
    knob_labels(ctx, t)


def draw_orb(ctx, t, pulse, inside):
    r = OR * (1 + 0.06 * pulse)
    glow(ctx, OX, OY, r * 2.6, "#7C9DFF", 0.35 + 0.2 * pulse)
    glow(ctx, OX, OY, r * 1.5, "#B6A4FF", 0.25 + 0.25 * pulse)
    # 外壳（进入内部时变透明）
    shell = 1 - inside
    circle(ctx, OX, OY, r)
    ctx.set_source(rad(OX, OY, 0, r, [(0, "#F4F0FF", 0.95 * shell + 0.15),
                                      (0.7, "#BFAFFF", 0.95 * shell + 0.1),
                                      (1, "#8B6CFF", 0.95 * shell + 0.2)],
                       fx=OX - r * 0.3, fy=OY - r * 0.35))
    ctx.fill()
    if shell > 0.02:
        ic_brain(ctx, OX, OY, r * 1.35, shell, t * 1.6, glow_a=0.0)
    # 赤道光环
    ctx.save()
    ctx.translate(OX, OY)
    ctx.scale(1, 0.28)
    ctx.set_line_width(5)
    setc(ctx, "#CFE0FF", 0.5 * shell)
    circle(ctx, 0, 0, r * 1.35)
    ctx.stroke()
    ctx.restore()
    ang = t * 1.4
    gx, gy = OX + math.cos(ang) * r * 1.35, OY + math.sin(ang) * r * 1.35 * 0.28
    glow(ctx, gx, gy, 24, "#FFFFFF", 0.8 * shell)
    if shell > 0.3:
        text(ctx, "大模型", OX, OY + r + 54, 38, "#FFFFFF", shell, "black")


def draw_knobs(ctx, t, a):
    """模型内部：一格格的小旋钮（参数）。"""
    step = 15.5
    rr = 5.6
    settle = smooth(prog(t, 8.4, 9.6))
    for (gx, gy, ph, sp) in KN:
        x, y = OX + gx * step, OY + gy * step
        wob = math.sin(t * (2.0 + sp) + ph) * 1.6 * (1 - settle)
        ang = ph + t * sp * (1 - settle) + wob
        target = -math.pi / 2 + (gx - gy) * 0.1
        ang = lerp(ang, target, settle)
        circle(ctx, x, y, rr)
        setc(ctx, "#2A2350", a)
        ctx.fill()
        ctx.set_line_width(1.1)
        setc(ctx, "#9F8CFF", a)
        circle(ctx, x, y, rr)
        ctx.stroke()
        line(ctx, x, y, x + math.cos(ang) * rr * 0.85, y + math.sin(ang) * rr * 0.85, 1.4,
             "#FFE3A3", a)
    sh = prog(t, 9.0, 10.2)
    if 0 < sh < 1:
        sx = lerp(OX - 170, OX + 170, sh)
        ctx.save()
        circle(ctx, OX, OY, OR * 1.02)
        ctx.clip()
        ctx.set_source(lin(sx - 30, 0, sx + 30, 0, [(0, "#FFFFFF", 0), (0.5, "#FFFFFF", 0.35 * a), (1, "#FFFFFF", 0)]))
        ctx.paint()
        ctx.restore()


def knob_labels(ctx, t):
    """屏幕空间的说明标签（不受镜头缩放影响）。"""
    from ..ui import pill
    la = smooth(prog(t, 7.5, 8.0))
    if la > 0:
        dy = (1 - ease_out(prog(t, 7.5, 8.1))) * -30
        pill(ctx, "参数 ≈ 千亿个小旋钮", 960, 130 + dy, 46, "#FFE3A3", "#120E18", la, 0.78, weight="black")
    ta = smooth(prog(t, 9.1, 9.6))
    if ta > 0:
        dy = (1 - ease_out(prog(t, 9.1, 9.7))) * 30
        pill(ctx, "训练，就是把这些旋钮一点点拧准", 960, 872 + dy, 36, "#FFFFFF", "#120E18", ta, 0.78)


def sfx():
    out = [(0.1, "stream", {"dur": 5.8, "gain": 0.32})]
    for i, f in enumerate(FLY):
        if i % 3 == 0:
            out.append((f[0] + FLY_DUR, "blip", {"gain": 0.16, "pitch": 0.9 + (i % 7) * 0.08}))
    out += [
        (1.45, "surprise", {"gain": 0.35}),
        (1.5, "boing", {"gain": 0.25}),
        (5.75, "zoom_in", {"gain": 0.55, "dur": 1.6}),
        (7.6, "ratchet", {"dur": 1.4, "gain": 0.35}),
        (9.0, "shimmer", {"dur": 1.3, "gain": 0.35}),
    ]
    return out
