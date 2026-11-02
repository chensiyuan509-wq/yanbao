"""漫画式特效：睡觉 Z、汗滴、问号、感叹号、怒气、泪水、晕眩、灵光、音符……

全部在身体局部坐标里绘制（随身体一起缩放 / 倾斜），t 为时间，a 为透明度。
"""
import math

from .const import BW, C_OUT, C_TEAR, EYE_X, EYE_Y, TOP
from .gfx import (TAU, circle, clamp, ellipse, fill, glow, heart, lin, rad, rng, rrect, setc,
                  star4, star5, stroke, text)


def _drop(ctx, x, y, s, a, c1="#E8F7FF", c2="#69B9E8"):
    ctx.move_to(x, y - 22 * s)
    ctx.curve_to(x + 4 * s, y - 10 * s, x + 13 * s, y - 2 * s, x + 13 * s, y + 6 * s)
    ctx.curve_to(x + 13 * s, y + 14 * s, x - 13 * s, y + 14 * s, x - 13 * s, y + 6 * s)
    ctx.curve_to(x - 13 * s, y - 2 * s, x - 4 * s, y - 10 * s, x, y - 22 * s)
    ctx.set_source(rad(x - 4 * s, y, 1, 18 * s, [(0, c1, a), (1, c2, a)]))
    ctx.fill()


def fx_zzz(ctx, t, a):
    for i in range(3):
        ph = (t * 0.42 + i / 3) % 1
        k = math.sin(ph * math.pi)
        text(ctx, "Z", 128 + ph * 70 + i * 4, TOP - 6 - ph * 120, 26 + ph * 26, "#FFFFFF", k * 0.95 * a,
             "black", outline=C_OUT, outline_w=4)


def fx_sparkle(ctx, t, a):
    p = 0.75 + 0.25 * math.sin(t * 5)
    glow(ctx, 70, TOP + 106, 70 * p, "#FFF6C8", 0.5 * a)
    star4(ctx, 70, TOP + 106, 28 * p, "#FFF8D8", 0.95 * a, t * 0.6)


def fx_sparkles(ctx, t, a):
    """身体周围一闪一闪的小星星。"""
    pts = ((-175, TOP + 20), (172, TOP + 4), (-150, TOP - 40), (186, TOP + 90), (120, TOP - 52))
    for i, (x, y) in enumerate(pts):
        k = 0.5 + 0.5 * math.sin(t * 4.2 + i * 1.9)
        star4(ctx, x, y, (10 + 8 * k), "#FFF3B0", a * (0.35 + 0.65 * k), t * 0.8 + i)


def fx_bulb(ctx, t, a):
    bx, by = 105, TOP - 50
    glow(ctx, bx, by, 150, "#FFE98A", 0.45 * a)
    for k in range(9):
        ang = k / 9 * TAU + t * 0.4
        r0, r1 = 34, 50 + 6 * math.sin(t * 4 + k)
        ctx.move_to(bx + math.cos(ang) * r0, by + math.sin(ang) * r0)
        ctx.line_to(bx + math.cos(ang) * r1, by + math.sin(ang) * r1)
        stroke(ctx, "#FFE27A", 4, 0.75 * a)
    circle(ctx, bx, by - 3, 20)
    ctx.set_source(rad(bx - 6, by - 9, 2, 22, [(0, "#FFFFFF", a), (1, "#FFE173", a)]))
    ctx.fill()
    rrect(ctx, bx - 9, by + 14, 18, 12, 3)
    fill(ctx, "#B9A68A", a)


def fx_question(ctx, t, a):
    bob = math.sin(t * 3) * 6
    text(ctx, "?", -112, TOP - 44 + bob, 70, "#FFFFFF", a, "black", outline="#5a3a30", outline_w=7)


def fx_question2(ctx, t, a):
    for i, (qx, qy, qs) in enumerate(((-120, -40, 70), (-40, -84, 52), (118, -52, 60))):
        bob = math.sin(t * 3 + i * 1.7) * 6
        text(ctx, "?", qx, TOP + qy + bob, qs, "#FFFFFF", a, "black", outline="#5a3a30", outline_w=6)


def fx_exclaim(ctx, t, a):
    k = 1 + 0.08 * math.sin(t * 12)
    text(ctx, "!", 0, TOP - 58, 86 * k, "#FFD25C", a, "black", outline="#5a3a30", outline_w=7)


def fx_sweat(ctx, t, a):
    _drop(ctx, -170, TOP + 104 + math.sin(t * 2.2) * 4, 1.0, a)


def fx_drops(ctx, t, a):
    """紧张：两侧不断飞出的小汗滴。"""
    for i in range(4):
        ph = (t * 1.3 + i / 4) % 1
        side = -1 if i % 2 == 0 else 1
        x = side * (160 + ph * 60)
        y = TOP + 30 - math.sin(ph * math.pi) * 40 + ph * 30
        _drop(ctx, x, y, 0.55, a * math.sin(ph * math.pi))


def fx_heart(ctx, t, a):
    for i in range(2):
        ph = (t * 0.6 + i * 0.5) % 1
        k = math.sin(ph * math.pi)
        heart(ctx, 120 + i * 40 + ph * 20, TOP - 20 - ph * 90, 18 + i * 6, "#FF6B8B", k * a)


def fx_gloom(ctx, t, a):
    for i in range(3):
        x = -60 + i * 60
        ctx.move_to(x, TOP - 20)
        ctx.line_to(x, TOP - 60 - (i % 2) * 14)
        stroke(ctx, "#6A5ACD", 5, 0.6 * a)


def fx_anger(ctx, t, a):
    """额头的"井"字怒气符号。"""
    k = 1 + 0.12 * abs(math.sin(t * 9))
    ctx.save()
    ctx.translate(118, TOP + 24)
    ctx.scale(k, k)
    for ang in (0.0, math.pi / 2, math.pi, 3 * math.pi / 2):
        ctx.save()
        ctx.rotate(ang + 0.785)
        ctx.move_to(5, -9)
        ctx.curve_to(10, -4, 10, 4, 5, 9)
        stroke(ctx, "#E5303B", 6, a)
        ctx.restore()
    ctx.restore()


def fx_tears(ctx, t, a):
    """两道泪流 + 落下的泪珠。"""
    for side in (-1, 1):
        x = side * EYE_X + side * 4
        ctx.move_to(x - 6, EYE_Y + 12)
        ctx.curve_to(x - 8, EYE_Y + 40, x + 8, EYE_Y + 60, x + 2 * side, EYE_Y + 86)
        ctx.line_to(x + 12 * side + 2, EYE_Y + 86)
        ctx.curve_to(x + 14, EYE_Y + 60, x + 6, EYE_Y + 40, x + 6, EYE_Y + 12)
        ctx.close_path()
        fill(ctx, C_TEAR, 0.75 * a)
        for i in range(2):
            ph = (t * 1.6 + i * 0.5 + (0.25 if side > 0 else 0)) % 1
            _drop(ctx, x + 6 * side, EYE_Y + 92 + ph * 70, 0.45, a * (1 - ph))


def fx_tears_joy(ctx, t, a):
    for side in (-1, 1):
        ph = (t * 1.4 + (0.5 if side > 0 else 0)) % 1
        x = side * (EYE_X + 34 + ph * 40)
        y = EYE_Y - 10 - math.sin(ph * math.pi) * 34 + ph * 40
        _drop(ctx, x, y, 0.55, a * math.sin(ph * math.pi))


def fx_dizzy(ctx, t, a):
    """头顶绕圈的小星星。"""
    for i in range(4):
        ang = t * 3.2 + i * TAU / 4
        x, y = math.cos(ang) * 120, TOP - 26 + math.sin(ang) * 22
        front = math.sin(ang) > 0
        star5(ctx, x, y, 15 if front else 11, "#FFD54A", a * (1.0 if front else 0.6), ang)


def fx_puff(ctx, t, a):
    """叹气时嘴边飘出的一小团气。"""
    ph = (t * 0.55) % 1
    k = math.sin(ph * math.pi)
    for i, (dx, dy, r) in enumerate(((0, 0, 16), (18, -6, 12), (-14, -8, 11))):
        circle(ctx, 70 + ph * 70 + dx, TOP + 118 - ph * 40 + dy, r * (0.6 + 0.6 * ph))
        fill(ctx, "#FFFFFF", 0.7 * k * a)


def fx_music(ctx, t, a):
    for i in range(3):
        ph = (t * 0.5 + i / 3) % 1
        k = math.sin(ph * math.pi)
        x = 130 + ph * 60 + i * 12 - (i == 1) * 260
        y = TOP - 10 - ph * 100
        text(ctx, "♪" if i % 2 == 0 else "♫", x, y, 46, "#FFFFFF", a * k, True, outline="#5a3a30",
             outline_w=5)


def fx_flame(ctx, t, a):
    """背后燃起的斗志之火。"""
    for i, (x, s) in enumerate(((-110, 0.8), (0, 1.15), (110, 0.85))):
        f = 1 + 0.12 * math.sin(t * 13 + i * 2.1)
        ctx.save()
        ctx.translate(x, TOP + 30)
        ctx.scale(s, s * f)
        ctx.move_to(0, -120)
        ctx.curve_to(30, -80, 60, -50, 52, -14)
        ctx.curve_to(46, 18, 20, 30, 0, 30)
        ctx.curve_to(-20, 30, -46, 18, -52, -14)
        ctx.curve_to(-60, -50, -30, -80, 0, -120)
        ctx.set_source(lin(0, -120, 0, 30, [(0, "#FFD34D", 0.0), (0.35, "#FF9F2E", 0.75 * a),
                                            (1, "#FF5B2E", 0.85 * a)]))
        ctx.fill()
        ctx.restore()


def fx_shock(ctx, t, a):
    """头顶的惊吓竖线。"""
    for i, (x, h) in enumerate(((-70, 46), (-24, 62), (24, 62), (70, 46))):
        jit = math.sin(t * 40 + i) * 3
        ctx.move_to(x + jit, TOP - 18)
        ctx.line_to(x + jit * 0.5 + (x * 0.15), TOP - 18 - h)
        stroke(ctx, "#2B2233", 6, 0.85 * a)


def fx_blush_lines(ctx, t, a):
    for side in (-1, 1):
        bx = side * (EYE_X + 10)
        for i in range(3):
            x = bx - 18 + i * 14
            ctx.move_to(x, TOP + 122)
            ctx.line_to(x + 9, TOP + 106)
            stroke(ctx, "#E9616B", 4, 0.8 * a)


def fx_ellipsis(ctx, t, a):
    """"……" 思考气泡。"""
    x0, y0 = 95, TOP - 70
    rrect(ctx, x0 - 62, y0 - 34, 124, 68, 34)
    fill(ctx, "#FFFFFF", 0.95 * a)
    circle(ctx, x0 - 46, y0 + 44, 11)
    fill(ctx, "#FFFFFF", 0.95 * a)
    circle(ctx, x0 - 62, y0 + 64, 7)
    fill(ctx, "#FFFFFF", 0.95 * a)
    for i in range(3):
        k = 0.5 + 0.5 * math.sin(t * 6 - i * 0.9)
        circle(ctx, x0 - 30 + i * 30, y0 - 4 * k, 8 + 2 * k)
        fill(ctx, "#8A8296", a * (0.5 + 0.5 * k))


def fx_confetti(ctx, t, a):
    R = rng(7)
    cols = ("#FF6B9A", "#FFC857", "#4C8DFF", "#3CCB7F", "#8B6CFF")
    for i in range(22):
        ph = (t * R.uniform(0.35, 0.6) + R.random()) % 1
        x = R.uniform(-260, 260) + math.sin(t * 2 + i) * 20
        y = TOP - 220 + ph * 360
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(t * R.uniform(-4, 4) + i)
        ctx.rectangle(-7, -4, 14, 8)
        fill(ctx, cols[i % len(cols)], a * min(1, (1 - ph) * 3))
        ctx.restore()


def fx_steam(ctx, t, a):
    """头顶冒热气（累 / 气）。"""
    for i in range(3):
        ph = (t * 0.8 + i / 3) % 1
        x = -50 + i * 50 + math.sin(t * 3 + i) * 8
        y = TOP - 10 - ph * 80
        circle(ctx, x, y, 12 + ph * 16)
        fill(ctx, "#FFFFFF", 0.55 * a * math.sin(ph * math.pi))


def fx_idea(ctx, t, a):
    """灵光一闪：头顶的小灯泡（比 bulb 小，常用于"想到了"）。"""
    bx, by = 0, TOP - 64
    glow(ctx, bx, by, 90, "#FFE98A", 0.55 * a)
    for k in range(8):
        ang = k / 8 * TAU
        r0, r1 = 30, 42 + 4 * math.sin(t * 6 + k)
        ctx.move_to(bx + math.cos(ang) * r0, by + math.sin(ang) * r0)
        ctx.line_to(bx + math.cos(ang) * r1, by + math.sin(ang) * r1)
        stroke(ctx, "#FFD84D", 4, 0.8 * a)
    circle(ctx, bx, by - 2, 18)
    ctx.set_source(rad(bx - 5, by - 8, 2, 20, [(0, "#FFFFFF", a), (1, "#FFD84D", a)]))
    ctx.fill()
    rrect(ctx, bx - 8, by + 13, 16, 10, 3)
    fill(ctx, "#B9A68A", a)


FX = {
    "zzz": fx_zzz, "sparkle": fx_sparkle, "sparkles": fx_sparkles, "bulb": fx_bulb, "idea": fx_idea,
    "question": fx_question, "question2": fx_question2, "exclaim": fx_exclaim, "sweat": fx_sweat,
    "drops": fx_drops, "heart": fx_heart, "gloom": fx_gloom, "anger": fx_anger, "tears": fx_tears,
    "tears_joy": fx_tears_joy, "dizzy": fx_dizzy, "puff": fx_puff, "music": fx_music, "flame": fx_flame,
    "shock": fx_shock, "blush_lines": fx_blush_lines, "ellipsis": fx_ellipsis, "confetti": fx_confetti,
    "steam": fx_steam,
}

# 画在身体后面的特效（其余画在前面）
BEHIND = {"flame", "confetti"}


def draw_fx(ctx, names, t, a=1.0, behind=False):
    for n in names or ():
        if (n in BEHIND) != behind:
            continue
        fn = FX.get(n)
        if fn and a > 0.003:
            fn(ctx, t, a)
