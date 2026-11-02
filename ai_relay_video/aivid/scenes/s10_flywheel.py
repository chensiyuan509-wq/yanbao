"""04 · 为什么是美国（下）：数据飞轮。Claude 推动飞轮 → 用户 / 反馈 / 模型依次点亮 →
编程反馈（采纳、修改、跑测试）流进飞轮 → 一骑绝尘 → 2025 年底企业编程市场份额。"""
import math

from ..core import (TAU, Cam, at, circle, clamp, ease_in, ease_io, ease_out, ease_out5, fill, glow, lerp,
                    lin, line, pop, prog, rad, ring_burst, rng, rrect, setc, smooth, sparkle_burst, star4,
                    stroke_pts, text, view, bezier_pts, point_on, check_mark)
from ..charts import donut, flywheel
from ..props import bg_grad, grid_dots, name_card, tag
from ..ui import window
from .common import host, talk_lines

DUR = 26.5
CHAPTER = ("04", "为什么是美国")

VO = [
    (0.7, '第三，是{数据飞轮}。'),
    (3.0, '用户越多，反馈越多；反馈越多，模型越强；模型越强，用户又更多。'),
    (10.3, 'Claude 在编程上就是这样：开发者每一次采纳、修改、跑测试，都在帮它变得更好。'),
    (17.2, '飞轮一旦转起来，就{一骑绝尘}：到 2025 年底，企业编程市场里，Claude 拿下了一半以上的份额。'),
]

FX_, FY = 1180, 520           # 飞轮中心
R = 285

P = (host(700, 900, 0.62, "determined", seed=10.1)
     .fx(0, ()).look(0, 0.9, -0.5)
     .push(0.9, 2.6, "r").expr(2.7, "excited").hop(2.8, 40, 0.38)
     .expr(3.4, "smile").look(3.4, 0.6, -0.9)
     .expr(6.0, "awe").expr(8.2, "starry")
     .walk_to(9.4, 10.4, 330, 900).expr(10.4, "focused").look(10.4, 0.4, -0.9)
     .expr(13.6, "happy").look(13.6, 1.0, -0.6)
     .expr(17.0, "excited").cheer(17.6, 19.0)
     .expr(19.2, "starry").look(19.2, 1.0, -0.5)
     .expr(22.6, "proud"))
talk_lines(P, VO, [0, 2], smile=0.35)

CAM = Cam([
    (0.0, (1000, 540, 1.08)),
    (2.8, (1020, 540, 1.0)),
    (9.8, (1000, 540, 1.0)),
    (10.6, (960, 540, 1.0), ease_io),
    (16.8, (980, 540, 1.02)),
    (18.2, (1120, 540, 0.92), ease_io),
    (26.5, (1160, 540, 0.96)),
], drift=6, seed=21.0)


def _speed(t):
    """飞轮转速：被推起来 → 越转越快。"""
    return 0.15 * smooth(prog(t, 0.9, 2.6)) + 0.9 * smooth(prog(t, 3.0, 9.0)) + 2.4 * smooth(prog(t, 16.6, 19.5))


def _angle(t):
    # 数值积分转角（逐帧独立计算，确定性）
    n = 80
    dt = max(t, 0) / n
    return sum(_speed(i * dt) * dt for i in range(n))


def _bg(ctx, t, cam):
    bg_grad(ctx, "#F2F6FF", "#FFE9DD", "#F6EEFF", 0.55)
    with view(ctx, cam, 0.5):
        grid_dots(ctx, -600, -300, 2600, 1400, 70, "#4C8DFF", 0.07, 2.5, drift=(-t * 30 * _speed(t), 0))
    with view(ctx, cam, 1.0):
        ctx.rectangle(-800, 900, 3600, 400)
        ctx.set_source(lin(0, 900, 0, 1200, [(0, "#E9DCCB"), (1, "#D9C3AE")]))
        ctx.fill()


def _wheel(ctx, t):
    ang = _angle(t)
    roll = smooth(prog(t, 18.6, 21.0))
    x = FX_ + roll * 420
    lit = [clamp((t - 3.0) / 0.5), clamp((t - 4.4) / 0.5), clamp((t - 6.0) / 0.5)]
    glow_a = 0.25 + 0.5 * smooth(prog(t, 16.6, 19.0))
    glow(ctx, x, FY, R * 1.6, "#FFB27A", glow_a)
    # 速度线 / 扬尘（一骑绝尘）
    if roll > 0:
        for i in range(10):
            yy = FY - R + i * (2 * R / 9)
            L = 220 + (i % 3) * 90
            line(ctx, x - R - 40 - L, yy, x - R - 40, yy, 6, "#FFB27A", 0.4 * roll)
        for i in range(8):
            ph = (t * 1.4 + i / 8) % 1
            circle(ctx, x - R - ph * 420, 880 - ph * 80 + (i % 3) * 10, 22 + ph * 50)
            fill(ctx, "#E9D8C8", 0.55 * roll * (1 - ph))
    flywheel(ctx, x, FY, R, ["用户", "反馈", "模型"], ang, ["#FF9F68", "#8B6CFF", "#2EC4B6"], 1.0, lit, 44,
             center="数据飞轮", thick=118)
    # 每句话对应的放大标签
    marks = [("用户越多", 3.0, 4.3, -1.6), ("反馈越多", 4.4, 5.9, 0.6), ("模型越强", 6.0, 7.9, 2.5),
             ("用户又更多", 8.0, 9.6, -1.6)]
    for lab, a0, a1, angp in marks:
        k = pop(t, a0, 0.45) * (1 - smooth(prog(t, a1, a1 + 0.3)))
        if k > 0:
            px, py = x + math.cos(angp) * (R + 120), FY + math.sin(angp) * (R + 90)
            with at(ctx, px, py, k):
                rrect(ctx, -130, -40, 260, 80, 40)
                fill(ctx, "#2B2233", 0.92)
                text(ctx, lab, 0, 0, 36, "#FFD36B", 1, "black")


SIG = [("采纳", "#3CCB7F"), ("修改", "#FFC857"), ("跑测试", "#4C8DFF")]


def _editor(ctx, t):
    a = smooth(prog(t, 10.0, 10.6)) * (1 - smooth(prog(t, 17.6, 18.4)))
    if a <= 0:
        return
    x0, y0, w, h = 120, 150, 560, 470
    cx, cy, cw, ch = window(ctx, x0, y0, w, h, "Claude Code", a, "dark", accent="#3A2F2A")
    rows = [("+ def parse(token):", "#7CFFB2"), ("+     return jwt.decode(token)", "#7CFFB2"),
            ("-     return token.split('.')", "#FF7A85"), ("  # 测试：12 / 12 通过", "#9AA0AE")]
    for i, (s, c) in enumerate(rows):
        n = int(clamp((t - 10.6 - i * 0.35) * 40, 0, len(s)))
        text(ctx, s[:n], cx + 24, cy + 46 + i * 50, 24, c, a, "mono", "l")
    for i, (lab, c) in enumerate(SIG):
        st = 12.0 + i * 1.0
        q = pop(t, st, 0.4)
        if q <= 0:
            continue
        bx, by = cx + 70 + i * 165, cy + ch - 60
        with at(ctx, bx, by, q):
            rrect(ctx, -70, -30, 140, 60, 30)
            fill(ctx, c, a)
            text(ctx, lab, 0, 0, 28, "#FFFFFF", a, "black")
        # 化作数据光点飞进飞轮
        for k in range(3):
            u = clamp((t - st - 0.3 - k * 0.25) / 1.2)
            if 0 < u < 1:
                pts = bezier_pts((bx, by), (bx + 200, by - 360), (FX_ - 420, FY - 380), (FX_ - R + 40, FY - 60), 30)
                (px, py), _ = point_on(pts, ease_io(u))
                glow(ctx, px, py, 26, c, 0.9 * a)
                circle(ctx, px, py, 7)
                fill(ctx, "#FFFFFF", a)
    tag(ctx, "每一次反馈，都是新的训练信号", x0 + w / 2, y0 + h + 60, 28, "#FFFFFF", "#D97757",
        a * smooth(prog(t, 14.6, 15.0)))


def _share(ctx, t):
    a = smooth(prog(t, 20.6, 21.2))
    if a <= 0:
        return
    cx, cy = 560, 400
    rrect(ctx, cx - 280, cy - 270, 560, 560, 36)
    fill(ctx, "#FFFFFF", 0.93 * a)
    text(ctx, "企业编程市场份额", cx, cy - 215, 32, "#2B2233", a, "black")
    p = prog(t, 21.0, 22.6)
    donut(ctx, cx, cy + 10, 150, [(0.54, "#D97757"), (0.21, "#10A37F"), (0.25, "#C9C3D3")], p, a, 58)
    q = smooth(prog(t, 22.2, 22.6))
    text(ctx, "54%", cx, cy - 6, 64, "#D97757", a * q, "black")
    text(ctx, "Claude", cx, cy + 50, 26, "#2B2233", a * q, "bold")
    for i, (lab, c) in enumerate((("Anthropic 54%", "#D97757"), ("OpenAI 21%", "#10A37F"), ("其他 25%", "#C9C3D3"))):
        x = cx - 236 + i * 178
        circle(ctx, x, cy + 200, 9)
        fill(ctx, c, a * q)
        text(ctx, lab, x + 16, cy + 200, 20, "#2B2233", a * q, "bold", "l")
    text(ctx, "Menlo Ventures · 2025 年 12 月报告", cx, cy + 252, 20, "#9A8FA8", a, "bold")


def draw(ctx, t):
    cam = CAM.at(t)
    _bg(ctx, t, cam)
    with view(ctx, cam, 1.0):
        _wheel(ctx, t)
        _editor(ctx, t)
        _share(ctx, t)
        P.draw(ctx, t)


def sfx():
    return [
        (0.7, "pop_big", {"gain": 0.35}),
        (0.9, "stretch", {"dur": 1.6, "gain": 0.3}), (2.4, "gear", {"gain": 0.35}),
        (2.8, "spinup", {"dur": 6.0, "gain": 0.22}),
        (3.0, "ding", {"gain": 0.3}), (4.4, "ding", {"gain": 0.3, "pitch": 1.12}),
        (6.0, "ding", {"gain": 0.3, "pitch": 1.25}), (8.0, "chime", {"gain": 0.3}),
        (9.4, "whoosh_short", {"gain": 0.25}),
        (10.6, "typing", {"dur": 1.4, "gain": 0.2}),
        (12.0, "check", {"gain": 0.3}), (13.0, "pop", {"gain": 0.3}), (14.0, "success", {"gain": 0.3}),
        (12.3, "stream", {"dur": 3.6, "gain": 0.15}),
        (16.6, "spinup", {"dur": 3.0, "gain": 0.3}),
        (18.6, "whoosh", {"dur": 1.6, "gain": 0.4}), (19.0, "rumble", {"dur": 1.0, "gain": 0.3}),
        (20.8, "pop", {"gain": 0.3}), (21.0, "rise", {"dur": 1.6, "gain": 0.25}),
        (22.6, "impact_soft", {"gain": 0.4}), (22.65, "shimmer", {"dur": 1.2, "gain": 0.3}),
    ]
