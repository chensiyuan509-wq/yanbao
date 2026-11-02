"""第一章 · 什么是大语言模型（1/3）：文字接龙。

「床前明月 __」→ 候选字概率条 → 选中"光"飞入 → 继续一字一字生成"，疑是地上霜"。
"""
import math

from ..core import (W, H, Cam, at, circle, clamp, ease_back, ease_in, ease_io, ease_out, fill,
                    glow, kf, lerp, pop, prog, rrect, setc, smooth, text, text_w, view, font,
                    sparkle_burst, ring_burst, bezier_pts, point_on, dashed, line)
from ..mascot import Puppet
from ..ui import card, progress
from .common import light_bg

DUR = 13.0
CHAPTER = ("01", "什么是大语言模型")

SUBS = [
    (1.0, 6.3, "{大语言模型}（LLM），本质上是一个「文字接龙」高手。"),
    (6.5, 12.6, "给它半句话，它就能算出{下一个字}最可能是什么。"),
]

PROMPT = "床前明月"
CANDS = [("光", 0.92), ("亮", 0.03), ("夜", 0.02), ("色", 0.01)]
GEN = [("，", [("，", .97), ("。", .02), ("下", .01)]),
       ("疑", [("疑", .90), ("照", .04), ("洒", .03)]),
       ("是", [("是", .95), ("似", .03), ("在", .01)]),
       ("地", [("地", .93), ("天", .03), ("窗", .02)]),
       ("上", [("上", .96), ("面", .02), ("下", .01)]),
       ("霜", [("霜", .94), ("雪", .03), ("光", .02)])]
T_TYPE = [0.9 + i * 0.36 for i in range(4)]
T_SLOT = 2.45
T_PANEL = 6.5
T_ROWS = [6.85 + i * 0.3 for i in range(4)]
T_PICK = 8.55
T_LAND = 9.35
T_GEN = [10.0 + i * 0.36 for i in range(len(GEN))]

CARD_X, CARD_Y, CARD_W, CARD_H = 330, 250, 1180, 190
TXT_X, TXT_Y, TXT_S = 410, 345, 92
PANEL_X, PANEL_Y, PANEL_W, PANEL_H = 330, 520, 760, 360

P = (Puppet(1530, 905, 0.62, "curious", seed=2.1, flip=True)
     .look(0, -0.8, -0.6)
     .expr(2.5, "think").bar(2.5, "think").fx(2.5, ("question",))
     .bar(6.4, None).fx(6.4, None).expr(6.4, "curious").look(6.4, -0.9, 0.0)
     .expr(8.5, "surprised")
     .expr(9.35, "excited").hop(9.35, 55).look(9.35, -0.6, -0.8)
     .expr(10.4, "happy").look(10.4, -0.7, -0.6).nod(11.0).nod(12.0))

CAM = Cam([
    (0.0, (920, 470, 1.04)),
    (5.8, (900, 450, 1.08)),
    (7.0, (900, 560, 1.0), ease_io),
    (9.5, (890, 540, 1.04)),
    (13.0, (900, 470, 1.1), ease_io),
], drift=5, seed=4.0)


def _char_pos(i):
    """第 i 个字（含生成部分）的左边 x。"""
    return TXT_X + i * (TXT_S + 4)


def draw(ctx, t):
    light_bg(ctx, "#FFF8EE", "#F6E3CF", dots="#C9A98C", dot_a=0.16, spacing=64, drift=(t * 6, t * 3))
    cam = CAM.at(t)
    with view(ctx, cam, 0.4):
        glow(ctx, 300, 200, 520, "#FFD7B0", 0.35)
        glow(ctx, 1650, 800, 600, "#FFC7D6", 0.25)

    with view(ctx, cam):
        # 输入卡片
        k = ease_back(prog(t, 0.0, 0.55), 1.4)
        a = smooth(prog(t, 0.0, 0.3))
        with at(ctx, CARD_X + CARD_W / 2, CARD_Y + CARD_H / 2, 0.92 + 0.08 * k):
            card(ctx, -CARD_W / 2, -CARD_H / 2, CARD_W, CARD_H, 40, "#FFFFFF", a, shadow=0.18)
            text(ctx, "输入", -CARD_W / 2 + 40, -CARD_H / 2 + 34, 24, "#B39C88", a, "bold", "l")
        # 已输入的字
        for i, ch in enumerate(PROMPT):
            q = pop(t, T_TYPE[i], 0.3)
            if q > 0:
                with at(ctx, _char_pos(i) + TXT_S / 2, TXT_Y, q):
                    text(ctx, ch, 0, 0, TXT_S, "#2B2233", 1, "black")
        # 光标
        n_typed = sum(1 for tt in T_TYPE if t >= tt)
        if t < T_SLOT and (t * 2.2) % 1 < 0.6 and t > 0.4:
            cx = _char_pos(n_typed) + 6
            rrect(ctx, cx, TXT_Y - 46, 6, 92, 3)
            fill(ctx, "#E07A4F")
        # 空槽
        slot_x = _char_pos(4)
        sk = pop(t, T_SLOT, 0.4)
        filled = t >= T_LAND
        if sk > 0 and not filled:
            pulse = 1 + 0.04 * math.sin(t * 6)
            with at(ctx, slot_x + TXT_S / 2, TXT_Y, sk * pulse):
                rrect(ctx, -TXT_S / 2 - 6, -TXT_S / 2 - 8, TXT_S + 12, TXT_S + 16, 18)
                setc(ctx, "#FFF1E6", 1)
                ctx.fill()
                ctx.save()
                ctx.set_dash((12, 9), t * 20)
                rrect(ctx, -TXT_S / 2 - 6, -TXT_S / 2 - 8, TXT_S + 12, TXT_S + 16, 18)
                ctx.set_line_width(4)
                setc(ctx, "#E07A4F", 0.9)
                ctx.stroke()
                ctx.restore()
                text(ctx, "?", 0, 0, 70, "#E07A4F", 0.8 + 0.2 * math.sin(t * 5), "black")
        if filled:
            q = ease_back(prog(t, T_LAND, T_LAND + 0.35), 2.5)
            with at(ctx, slot_x + TXT_S / 2, TXT_Y, 0.6 + 0.4 * q):
                text(ctx, "光", 0, 0, TXT_S, "#E07A4F", 1, "black")
            ring_burst(ctx, t, T_LAND, slot_x + TXT_S / 2, TXT_Y, 30, 150, "#FFB27A", 0.6, 8)
            sparkle_burst(ctx, t, T_LAND, slot_x + TXT_S / 2, TXT_Y, 9, 140, "#FFC65C", 0.8, 5, 18)
        # 继续生成的字
        for i, (ch, _) in enumerate(GEN):
            q = pop(t, T_GEN[i], 0.3)
            if q > 0:
                hi = 1 - smooth(prog(t, T_GEN[i] + 0.25, T_GEN[i] + 0.9))
                with at(ctx, _char_pos(5 + i) + TXT_S / 2, TXT_Y, q):
                    col = "#E07A4F" if hi > 0.5 else "#2B2233"
                    text(ctx, ch, 0, 0, TXT_S, col, 1, "black")
                if hi > 0:
                    rrect(ctx, _char_pos(5 + i) + 8, TXT_Y + 52, TXT_S - 16, 6, 3)
                    fill(ctx, "#FFB27A", hi)

        # 概率面板
        pa = smooth(prog(t, T_PANEL, T_PANEL + 0.4))
        if pa > 0:
            dy = (1 - ease_out(prog(t, T_PANEL, T_PANEL + 0.5))) * 60
            draw_panel(ctx, t, pa, dy)

        # "光"字从面板飞向空槽
        if T_PICK <= t < T_LAND:
            u = ease_io(prog(t, T_PICK, T_LAND))
            p0 = (PANEL_X + 120, PANEL_Y + 130)
            p3 = (slot_x + TXT_S / 2, TXT_Y)
            pts = bezier_pts(p0, (p0[0] - 160, p0[1] - 260), (p3[0] - 40, p3[1] + 250), p3, 40)
            (x, y), ang = point_on(pts, u)
            glow(ctx, x, y, 90, "#FFB27A", 0.5)
            with at(ctx, x, y, 0.8 + 0.4 * math.sin(u * math.pi), 0.3 * math.sin(u * math.pi * 2)):
                text(ctx, "光", 0, 0, 86, "#E07A4F", 1, "black")

        P.draw(ctx, t)


def draw_panel(ctx, t, a, dy):
    x, y, w, h = PANEL_X, PANEL_Y + dy, PANEL_W, PANEL_H
    card(ctx, x, y, w, h, 34, "#FFFFFF", a, shadow=0.16)
    # 当前展示哪一步的候选
    stage = -1
    for i, tt in enumerate(T_GEN):
        if t >= tt - 0.12:
            stage = i
    if stage < 0:
        title, cands, row_ts = "下一个字是什么？", CANDS, T_ROWS
    else:
        title, cands = "继续接龙…", GEN[stage][1]
        row_ts = [T_GEN[stage] - 0.12 + j * 0.04 for j in range(len(cands))]
    text(ctx, title, x + 40, y + 46, 30, "#8A7766", a, "bold", "l")
    text(ctx, "概率", x + w - 40, y + 46, 24, "#B9A797", a, "medium", "r")
    for j, (ch, pr) in enumerate(cands):
        q = ease_out(prog(t, row_ts[j], row_ts[j] + 0.45))
        if q <= 0:
            continue
        ry = y + 118 + j * 62
        top = j == 0
        hl = top and (stage >= 0 or t >= T_PICK - 0.5)
        if hl:
            rrect(ctx, x + 22, ry - 28, w - 44, 56, 18)
            setc(ctx, "#FFF1E6", a * q)
            ctx.fill()
        hidden = (stage < 0 and top and T_PICK <= t)  # "光"已飞出
        if not hidden:
            text(ctx, ch, x + 90, ry, 44, "#E07A4F" if top else "#5A4E63", a * q, "black")
        bw = (w - 330) * pr * q
        rrect(ctx, x + 150, ry - 13, w - 330, 26, 13)
        setc(ctx, "#F1E9E0", a * q)
        ctx.fill()
        rrect(ctx, x + 150, ry - 13, max(26, bw), 26, 13)
        setc(ctx, "#FF9F68" if top else "#CDBFB2", a * q)
        ctx.fill()
        text(ctx, f"{pr * 100 * q:.0f}%", x + w - 40, ry, 32, "#2B2233" if top else "#8A7F92", a * q,
             "black" if top else "bold", "r")


def sfx():
    out = [(0.05, "pop", {"gain": 0.4, "pitch": 0.8})]
    for i, tt in enumerate(T_TYPE):
        out.append((tt, "key", {"gain": 0.55, "seed": i}))
    out.append((T_SLOT, "tick", {"gain": 0.4, "pitch": 1.3}))
    out.append((2.5, "bubble", {"gain": 0.3}))
    out.append((2.9, "think", {"dur": 3.4, "gain": 0.22}))
    out.append((T_PANEL, "swish", {"gain": 0.35}))
    for i, tt in enumerate(T_ROWS):
        out.append((tt, "pop", {"gain": 0.38, "pitch": 1.0 + i * 0.12}))
    out.append((T_PICK, "whoosh_short", {"gain": 0.45}))
    out.append((T_LAND, "ding", {"gain": 0.6, "pitch": 1.0}))
    out.append((T_LAND + 0.02, "sparkle", {"dur": 0.9, "gain": 0.3}))
    out.append((T_LAND + 0.05, "boing", {"gain": 0.35}))
    for i, tt in enumerate(T_GEN):
        out.append((tt, "tick", {"gain": 0.32, "pitch": 1.1 + 0.06 * i}))
    return out
