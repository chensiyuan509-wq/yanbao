"""第一章（3/3）：会聊天、写作、翻译、编程的"大脑"——却够不着一张机票。"""
import math

from ..core import (W, H, Cam, at, circle, clamp, ease_back, ease_io, ease_out, fill, glow, lerp,
                    pop, prog, rrect, setc, smooth, text, view, sparkle_burst, star4, line)
from ..icons import ic_chat, ic_code, ic_docs, ic_plane, ic_brain
from ..mascot import Puppet
from ..ui import bubble, card
from .common import light_bg

DUR = 9.0
CHAPTER = ("01", "什么是大语言模型")

SUBS = [
    (0.4, 4.6, "所以它能聊天、写作、翻译、编程，像一个博学的大脑——"),
    (4.8, 8.8, "可大脑只会「说」，不会「做」：它{没有手}。"),
]

MX, MY = 860, 820
BADGES = [  # (时间, 标签, 绘制函数, 位置)
    (0.6, "聊天", "chat", (520, 380)),
    (1.3, "写作", "write", (760, 250)),
    (2.0, "翻译", "trans", (1020, 250)),
    (2.7, "编程", "code", (1240, 380)),
]
T_TICKET = 4.85

P = (Puppet(MX, MY, 0.82, "smile", seed=4.4)
     .look(0, 0, -0.6)
     .expr(0.6, "happy").look(0.6, -0.8, -0.5)
     .look(1.3, -0.3, -1.0).look(2.0, 0.3, -1.0).look(2.7, 0.8, -0.5)
     .expr(3.3, "proud").look(3.3, 0, 0).nod(3.4)
     .expr(5.1, "curious").look(5.1, 1.0, -0.4)
     .expr(5.7, "determined").arm(5.7, "r", 0.55, 0.4).ext(5.7, "r", 70, 0.5)
     .strain(6.2, 7.3, "r").fx(6.3, ("sweat",))
     .expr(7.35, "sad").arm(7.35, "r", 0.0, 0.5).ext(7.35, "r", 0, 0.4)
     .fx(7.35, ("sweat",)).tilt(7.35, -0.04))

CAM = Cam([
    (0.0, (900, 540, 1.0)),
    (4.2, (900, 520, 1.05)),
    (5.3, (1020, 560, 1.02), ease_io),
    (9.0, (1040, 560, 1.08)),
], drift=5, seed=8.0)


def _badge_icon(ctx, kind, x, y, s, t):
    if kind == "chat":
        ic_chat(ctx, x, y, s, 1, t, "#2EC4B6")
    elif kind == "code":
        ic_code(ctx, x, y, s, 1, t)
    elif kind == "write":
        ic_docs(ctx, x, y, s, 1, t)
    else:
        rrect(ctx, x - s / 2, y - s / 2, s, s, s * 0.24)
        fill(ctx, "#8B6CFF")
        text(ctx, "文", x - s * 0.15, y - s * 0.1, s * 0.42, "#FFFFFF", 1, "black")
        text(ctx, "A", x + s * 0.2, y + s * 0.18, s * 0.38, "#FFE3A3", 1, "black")


def draw(ctx, t):
    light_bg(ctx, "#FFF4EA", "#F7DCCB", dots="#D9A88C", dot_a=0.14, spacing=70, drift=(-t * 5, t * 2))
    cam = CAM.at(t)
    with view(ctx, cam, 0.5):
        glow(ctx, 860, 420, 600, "#FFD9B0", 0.45)
    with view(ctx, cam):
        # 头顶的"大脑"光环
        hx, hy = P.head(t)
        ba = smooth(prog(t, 0.1, 0.6))
        dim = 1 - 0.35 * smooth(prog(t, 7.3, 8.0))
        glow(ctx, hx, hy - 120, 240, "#B6A4FF", 0.35 * ba * dim)
        ic_brain(ctx, hx, hy - 120, 130 * ease_back(prog(t, 0.1, 0.6)), ba * dim, t, glow_a=0.2)
        # 技能徽章
        for (t0, lab, kind, (x, y)) in BADGES:
            k = pop(t, t0, 0.45)
            if k <= 0:
                continue
            fy = math.sin(t * 1.6 + x) * 6
            fade = 1 - 0.5 * smooth(prog(t, 4.9, 5.5))
            with at(ctx, x, y + fy, k):
                card(ctx, -80, -80, 160, 160, 34, "#FFFFFF", fade, shadow=0.16)
                _badge_icon(ctx, kind, 0, -14, 76, t)
                text(ctx, lab, 0, 50, 30, "#2B2233", fade, "black")
            line(ctx, hx, hy - 120, x, y + fy, 3, "#B6A4FF", 0.35 * k * fade)
            sparkle_burst(ctx, t, t0, x, y, 7, 110, "#FFC65C", 0.7, int(t0 * 10), 15)
            # 绿色对勾
            ck = pop(t, t0 + 0.25, 0.35)
            if ck > 0:
                with at(ctx, x + 62, y - 62 + fy, ck):
                    circle(ctx, 0, 0, 22)
                    fill(ctx, "#3CCB7F", fade)
                    from ..core import check_mark
                    check_mark(ctx, 0, 1, 26, "#FFFFFF", 1, fade)
        # 机票任务卡
        ta = smooth(prog(t, T_TICKET, T_TICKET + 0.35))
        if ta > 0:
            dx = (1 - ease_out(prog(t, T_TICKET, T_TICKET + 0.6))) * 500
            draw_ticket(ctx, 1560 + dx, 620, ta, t)
        P.draw(ctx, t)
        # 说话气泡
        sa = pop(t, 6.9, 0.4) * (1 - smooth(prog(t, 8.7, 9.0)))
        if sa > 0:
            with at(ctx, hx - 250, hy - 40, sa):
                bubble(ctx, -230, -60, 460, 96, "#FFFFFF", 1, tail="right", r=30)
                text(ctx, "我只能告诉你怎么订……", 0, -12, 30, "#5A4E63", 1, "bold")


def draw_ticket(ctx, x, y, a, t):
    w, h = 420, 230
    tilt = -0.05 + 0.02 * math.sin(t * 2)
    with at(ctx, x, y, 1.0, tilt):
        card(ctx, -w / 2, -h / 2, w, h, 28, "#FFFFFF", a, shadow=0.22)
        ctx.save()
        rrect(ctx, -w / 2, -h / 2, w, h, 28)
        ctx.clip()
        ctx.rectangle(-w / 2, -h / 2, w, 64)
        setc(ctx, "#4C8DFF", a)
        ctx.fill()
        ctx.restore()
        text(ctx, "任务", -w / 2 + 28, -h / 2 + 32, 26, "#FFFFFF", a, "black", "l")
        ic_plane(ctx, w / 2 - 50, -h / 2 + 32, 56, a, t, "#FFFFFF", -0.2)
        text(ctx, "帮我订一张", 0, 2, 32, "#2B2233", a, "bold")
        text(ctx, "去上海的机票", 0, 50, 36, "#2B2233", a, "black")
        # 撕票虚线
        ctx.save()
        ctx.set_dash((8, 8))
        ctx.set_line_width(3)
        setc(ctx, "#D7D0E0", a)
        ctx.move_to(-w / 2 + 20, 82)
        ctx.line_to(w / 2 - 20, 82)
        ctx.stroke()
        ctx.restore()


def sfx():
    out = []
    for i, (t0, *_r) in enumerate(BADGES):
        out.append((t0, "pop", {"gain": 0.45, "pitch": 1.0 + i * 0.14}))
        out.append((t0 + 0.25, "tick", {"gain": 0.25, "pitch": 1.6}))
    out += [
        (3.3, "chime", {"gain": 0.4}),
        (T_TICKET, "swish", {"gain": 0.45}),
        (5.75, "stretch", {"dur": 1.6, "gain": 0.45}),
        (6.9, "bubble", {"gain": 0.35}),
        (7.35, "womp", {"gain": 0.45}),
    ]
    return out
