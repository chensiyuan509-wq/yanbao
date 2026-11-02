"""配件与道具：帽子、眼镜、手持道具。

- 帽子 / 眼镜画在身体局部坐标里（随身体缩放倾斜），帽子有惯性晃动（hat_dy / hat_rot）。
- 道具函数签名 prop_xxx(ctx, t, a, **kw)，以 (0, 0) 为握点 / 中心绘制；
  也可以直接传一个可调用对象 fn(ctx, t, a) 作为自定义道具（比如项目里的图标）。
"""
import math

import cairo

from .const import EYE_X, EYE_Y, MOUTH_Y, TOP, BW
from .gfx import (TAU, circle, clamp, ellipse, fill, glow, lin, poly, rad, rrect, setc, star4,
                  stroke, text, text_w)

# ---------------------------------------------------------------- 帽子


def hat_explorer(ctx, t, a=1.0):
    """探险家遮阳帽（木髓盔）。"""
    y = TOP + 6
    ellipse(ctx, 0, y, 150, 22)
    ctx.set_source(lin(0, y - 22, 0, y + 22, [(0, "#F1DFB4", a), (1, "#C9AE78", a)]))
    ctx.fill()
    ctx.move_to(-98, y - 2)
    ctx.curve_to(-96, y - 112, 96, y - 112, 98, y - 2)
    ctx.close_path()
    ctx.set_source(lin(-60, y - 100, 60, y, [(0, "#F6E8C3", a), (1, "#D7BC85", a)]))
    ctx.fill()
    ctx.save()
    ctx.move_to(-98, y - 2)
    ctx.curve_to(-96, y - 112, 96, y - 112, 98, y - 2)
    ctx.close_path()
    ctx.clip()
    ctx.rectangle(-110, y - 34, 220, 22)
    fill(ctx, "#8C6A3E", a)
    ctx.restore()
    ellipse(ctx, -34, y - 70, 24, 12)
    fill(ctx, "#FFFFFF", 0.35 * a)
    circle(ctx, 0, y - 86, 7)
    fill(ctx, "#B99A62", a)


def hat_hardhat(ctx, t, a=1.0):
    y = TOP + 4
    rrect(ctx, -124, y - 14, 248, 20, 10)
    fill(ctx, "#E8A90E", a)
    ctx.move_to(-100, y - 8)
    ctx.curve_to(-98, y - 104, 98, y - 104, 100, y - 8)
    ctx.close_path()
    ctx.set_source(lin(0, y - 100, 0, y, [(0, "#FFE36B", a), (1, "#F5B915", a)]))
    ctx.fill()
    rrect(ctx, -14, y - 98, 28, 90, 12)
    fill(ctx, "#F0AE0C", a)
    ellipse(ctx, -46, y - 62, 22, 12)
    fill(ctx, "#FFFFFF", 0.4 * a)


def hat_grad(ctx, t, a=1.0):
    """学士帽（流苏会摆）。"""
    y = TOP + 2
    rrect(ctx, -70, y - 46, 140, 46, 10)
    fill(ctx, "#2B2735", a)
    poly(ctx, [(0, y - 96), (150, y - 62), (0, y - 30), (-150, y - 62)])
    ctx.set_source(lin(0, y - 96, 0, y - 30, [(0, "#4A4458", a), (1, "#2B2735", a)]))
    ctx.fill()
    sw = math.sin(t * 2.6) * 0.25
    ctx.save()
    ctx.translate(0, y - 63)
    ctx.move_to(0, 0)
    ctx.line_to(96, 4)
    ctx.rotate(0)
    stroke(ctx, "#F5C04A", 4, a)
    ctx.translate(96, 4)
    ctx.rotate(sw)
    ctx.move_to(0, 0)
    ctx.line_to(0, 54)
    stroke(ctx, "#F5C04A", 4, a)
    rrect(ctx, -8, 48, 16, 26, 6)
    fill(ctx, "#F5C04A", a)
    ctx.restore()
    circle(ctx, 0, y - 63, 7)
    fill(ctx, "#F5C04A", a)


def hat_headset(ctx, t, a=1.0):
    y = TOP
    ctx.new_sub_path()
    ctx.arc(0, y + 70, 160, math.pi * 1.08, math.pi * 1.92)
    stroke(ctx, "#3A3646", 14, a)
    for sx in (-1, 1):
        rrect(ctx, sx * 150 - 18, y + 40, 36, 64, 14)
        fill(ctx, "#2E2B38", a)
        rrect(ctx, sx * 150 - 10, y + 50, 20, 44, 8)
        fill(ctx, "#6C63FF", a)
    ctx.move_to(-150, y + 92)
    ctx.curve_to(-150, MOUTH_Y + 30, -90, MOUTH_Y + 20, -40, MOUTH_Y + 8)
    stroke(ctx, "#3A3646", 6, a)
    circle(ctx, -36, MOUTH_Y + 7, 9)
    fill(ctx, "#2E2B38", a)


def hat_crown(ctx, t, a=1.0):
    y = TOP + 4
    pts = [(-80, y), (-80, y - 70), (-44, y - 34), (0, y - 86), (44, y - 34), (80, y - 70), (80, y)]
    poly(ctx, pts)
    ctx.set_source(lin(0, y - 86, 0, y, [(0, "#FFE58A", a), (1, "#E9A93A", a)]))
    ctx.fill()
    for x, c in ((-46, "#FF5A7A"), (0, "#4C8DFF"), (46, "#3CCB7F")):
        circle(ctx, x, y - 18, 9)
        fill(ctx, c, a)
    star4(ctx, 0, y - 86, 14 + 4 * math.sin(t * 5), "#FFFFFF", 0.9 * a, t)


def hat_party(ctx, t, a=1.0):
    y = TOP + 4
    ctx.save()
    ctx.translate(30, y)
    ctx.rotate(0.18)
    poly(ctx, [(-50, 0), (0, -150), (50, 0)])
    ctx.set_source(lin(-50, 0, 50, 0, [(0, "#8B6CFF", a), (1, "#FF6B9A", a)]))
    ctx.fill()
    for i in range(3):
        k = (i + 1) / 4
        ctx.move_to(-50 * (1 - k), -150 * k)
        ctx.line_to(50 * (1 - k), -150 * k)
        stroke(ctx, "#FFE58A", 6, a)
    circle(ctx, 0, -152, 14)
    fill(ctx, "#FFE58A", a)
    ctx.restore()


HATS = {"explorer": hat_explorer, "hardhat": hat_hardhat, "grad": hat_grad, "headset": hat_headset,
        "crown": hat_crown, "party": hat_party}

# ---------------------------------------------------------------- 眼镜


def glasses_round(ctx, t, a=1.0, look=(0, 0)):
    for sx in (-1, 1):
        circle(ctx, sx * EYE_X + look[0], EYE_Y + look[1], 40)
        fill(ctx, "#FFFFFF", 0.14 * a)
        circle(ctx, sx * EYE_X + look[0], EYE_Y + look[1], 40)
        stroke(ctx, "#2B2233", 6, a)
    ctx.move_to(-EYE_X + 40 + look[0], EYE_Y - 4 + look[1])
    ctx.curve_to(-20 + look[0], EYE_Y - 20 + look[1], 20 + look[0], EYE_Y - 20 + look[1],
                 EYE_X - 40 + look[0], EYE_Y - 4 + look[1])
    stroke(ctx, "#2B2233", 6, a)


def glasses_goggles(ctx, t, a=1.0, look=(0, 0)):
    rrect(ctx, -BW / 2 - 2, EYE_Y - 16, BW + 4, 30, 10)
    fill(ctx, "#3A3646", a)
    for sx in (-1, 1):
        rrect(ctx, sx * EYE_X - 44, EYE_Y - 38, 88, 76, 26)
        fill(ctx, "#56607A", a)
        rrect(ctx, sx * EYE_X - 36, EYE_Y - 30, 72, 60, 20)
        fill(ctx, "#BFE8FF", 0.35 * a)
        ctx.move_to(sx * EYE_X - 20, EYE_Y - 20)
        ctx.line_to(sx * EYE_X - 4, EYE_Y - 24)
        stroke(ctx, "#FFFFFF", 5, 0.7 * a)


def glasses_sun(ctx, t, a=1.0, look=(0, 0)):
    for sx in (-1, 1):
        rrect(ctx, sx * EYE_X - 42, EYE_Y - 26, 84, 50, 16)
        ctx.set_source(lin(0, EYE_Y - 26, 0, EYE_Y + 24, [(0, "#3B3550", a), (1, "#14111C", a)]))
        ctx.fill()
        ctx.move_to(sx * EYE_X - 26, EYE_Y - 14)
        ctx.line_to(sx * EYE_X - 6, EYE_Y - 18)
        stroke(ctx, "#FFFFFF", 5, 0.5 * a)
    ctx.move_to(-EYE_X + 42, EYE_Y - 12)
    ctx.line_to(EYE_X - 42, EYE_Y - 12)
    stroke(ctx, "#14111C", 7, a)


GLASSES = {"round": glasses_round, "goggles": glasses_goggles, "sun": glasses_sun}
# 会把眼睛挡住的眼镜（画了它就不画眼睛）
OPAQUE_GLASSES = {"sun"}

# ---------------------------------------------------------------- 手持道具


def prop_baton(ctx, t, a=1.0, glow_a=1.0, **_):
    """接力棒：金色发光圆筒，(0,0) 为中心，长 110。"""
    glow(ctx, 0, 0, 110, "#FFD36B", 0.45 * glow_a * a)
    rrect(ctx, -55, -13, 110, 26, 13)
    ctx.set_source(lin(0, -13, 0, 13, [(0, "#FFF0B8", a), (0.5, "#FFC23D", a), (1, "#D98B12", a)]))
    ctx.fill()
    for x in (-34, 34):
        ctx.rectangle(x - 4, -13, 8, 26)
        fill(ctx, "#FFFFFF", 0.35 * a)
    star4(ctx, 40, -16, 10 + 4 * math.sin(t * 6), "#FFFFFF", 0.9 * a, t * 1.5)


def prop_magnifier(ctx, t, a=1.0, **_):
    """放大镜：握把在 (0,0)，镜片在上方。"""
    rrect(ctx, -9, -10, 18, 70, 8)
    fill(ctx, "#7A4E2C", a)
    circle(ctx, 0, -50, 40)
    fill(ctx, "#CFEFFF", 0.35 * a)
    circle(ctx, 0, -50, 40)
    stroke(ctx, "#5A5F6B", 9, a)
    ctx.new_sub_path()
    ctx.arc(0, -50, 28, math.pi * 1.1, math.pi * 1.5)
    stroke(ctx, "#FFFFFF", 6, 0.8 * a)


def prop_flag(ctx, t, a=1.0, label="", color="#FF6B5B", **_):
    rrect(ctx, -5, -160, 10, 170, 5)
    fill(ctx, "#8C6A3E", a)
    wave = [math.sin(t * 5 + i * 0.7) * 6 for i in range(6)]
    ctx.move_to(5, -156)
    for i in range(6):
        ctx.line_to(5 + i * 26, -156 + wave[i])
    for i in range(5, -1, -1):
        ctx.line_to(5 + i * 26, -86 + wave[i])
    ctx.close_path()
    fill(ctx, color, a)
    if label:
        text(ctx, label, 72, -121 + wave[3], 30, "#FFFFFF", a, True)


def prop_sign(ctx, t, a=1.0, label="", color="#FFFFFF", fg="#2B2233", size=40, **_):
    """举牌：(0,0) 为握点，牌子在上方。"""
    w = max(180, text_w(ctx, label, size) + 60) if label else 200
    rrect(ctx, -6, -150, 12, 160, 5)
    fill(ctx, "#8C6A3E", a)
    rrect(ctx, -w / 2, -250, w, 110, 16)
    fill(ctx, color, a)
    rrect(ctx, -w / 2, -250, w, 110, 16)
    stroke(ctx, "#2B2233", 5, 0.85 * a)
    if label:
        text(ctx, label, 0, -195, size, fg, a, "black")


def prop_laptop(ctx, t, a=1.0, **_):
    """笔记本电脑（正对观众），(0,0) 为键盘中心。"""
    rrect(ctx, -110, -150, 220, 140, 10)
    fill(ctx, "#3A3646", a)
    rrect(ctx, -100, -140, 200, 120, 6)
    fill(ctx, "#1E1B26", a)
    cols = ("#FF7AA2", "#7CC6FF", "#FFC857", "#7CFFB2")
    for i in range(5):
        w = 50 + (i * 37) % 90
        rrect(ctx, -86 + (i % 2) * 14, -126 + i * 20, w, 8, 4)
        fill(ctx, cols[i % 4], a)
    rrect(ctx, -126, -12, 252, 18, 6)
    fill(ctx, "#C9C5D3", a)


def prop_phone(ctx, t, a=1.0, screen="#FFFFFF", **_):
    rrect(ctx, -40, -76, 80, 152, 14)
    fill(ctx, "#25222D", a)
    rrect(ctx, -34, -68, 68, 136, 10)
    fill(ctx, screen, a)
    rrect(ctx, -12, -64, 24, 6, 3)
    fill(ctx, "#25222D", a)


def prop_book(ctx, t, a=1.0, color="#4C8DFF", **_):
    for sx in (-1, 1):
        ctx.move_to(0, -60)
        ctx.curve_to(sx * 40, -72, sx * 80, -66, sx * 100, -58)
        ctx.line_to(sx * 100, 40)
        ctx.curve_to(sx * 80, 32, sx * 40, 28, 0, 40)
        ctx.close_path()
        fill(ctx, "#FFFDF6", a)
        for i in range(5):
            ctx.move_to(sx * 18, -40 + i * 16)
            ctx.line_to(sx * (80 - (i == 4) * 30), -40 + i * 16 - 4)
            stroke(ctx, "#C9C1BA", 4, a)
    rrect(ctx, -104, 34, 208, 14, 6)
    fill(ctx, color, a)


def prop_paper(ctx, t, a=1.0, title="", **_):
    rrect(ctx, -70, -95, 140, 190, 8)
    fill(ctx, "#FFFFFF", a)
    rrect(ctx, -70, -95, 140, 190, 8)
    stroke(ctx, "#D9D2CC", 3, a)
    if title:
        text(ctx, title, 0, -66, 20, "#2B2233", a, True)
    for i in range(7):
        rrect(ctx, -52, -40 + i * 18, 104 if i % 3 else 80, 6, 3)
        fill(ctx, "#C9C1BA", a)


def prop_coffee(ctx, t, a=1.0, **_):
    rrect(ctx, -34, -40, 68, 74, 14)
    fill(ctx, "#FFFFFF", a)
    ctx.new_sub_path()
    ctx.arc(34, -4, 16, -math.pi / 2, math.pi / 2)
    stroke(ctx, "#FFFFFF", 9, a)
    rrect(ctx, -34, -18, 68, 18, 0)
    fill(ctx, "#E88E64", a)
    for i in range(2):
        ph = (t * 0.7 + i * 0.5) % 1
        ctx.move_to(-10 + i * 18, -50 - ph * 40)
        ctx.curve_to(-20 + i * 18, -60 - ph * 40, 0 + i * 18, -70 - ph * 40, -10 + i * 18, -82 - ph * 40)
        stroke(ctx, "#FFFFFF", 5, 0.6 * a * math.sin(ph * math.pi))


def prop_wrench(ctx, t, a=1.0, **_):
    rrect(ctx, -10, -30, 20, 120, 8)
    fill(ctx, "#9AA3B5", a)
    circle(ctx, 0, -48, 30)
    fill(ctx, "#9AA3B5", a)
    rrect(ctx, -11, -84, 22, 40, 4)          # 扳手开口
    fill(ctx, "#5B6475", a)


def prop_pointer(ctx, t, a=1.0, **_):
    rrect(ctx, -5, -220, 10, 230, 5)
    fill(ctx, "#8C6A3E", a)
    circle(ctx, 0, -222, 9)
    fill(ctx, "#FF5A5F", a)


def prop_chip(ctx, t, a=1.0, label="", **_):
    rrect(ctx, -60, -60, 120, 120, 14)
    fill(ctx, "#2F3442", a)
    for i in range(6):
        v = -46 + i * 18
        ctx.rectangle(-68, v, 8, 6)
        ctx.rectangle(60, v, 8, 6)
        ctx.rectangle(v, -68, 6, 8)
        ctx.rectangle(v, 60, 6, 8)
    fill(ctx, "#C9A14A", a)
    rrect(ctx, -40, -40, 80, 80, 8)
    ctx.set_source(lin(0, -40, 0, 40, [(0, "#7DD87D", a), (1, "#3C9D4A", a)]))
    ctx.fill()
    if label:
        text(ctx, label, 0, 0, 22, "#FFFFFF", a, "black")


PROPS = {"baton": prop_baton, "magnifier": prop_magnifier, "flag": prop_flag, "sign": prop_sign,
         "laptop": prop_laptop, "phone": prop_phone, "book": prop_book, "paper": prop_paper,
         "coffee": prop_coffee, "wrench": prop_wrench, "pointer": prop_pointer, "chip": prop_chip}


def draw_prop(ctx, prop, t, a=1.0):
    """prop 可以是 ('名称', {参数}) / '名称' / 可调用对象 fn(ctx, t, a)。"""
    if prop is None or a <= 0.003:
        return
    if callable(prop):
        prop(ctx, t, a)
        return
    if isinstance(prop, str):
        name, kw = prop, {}
    else:
        name, kw = prop[0], (prop[1] if len(prop) > 1 else {})
    fn = PROPS.get(name)
    if fn:
        fn(ctx, t, a, **kw)
