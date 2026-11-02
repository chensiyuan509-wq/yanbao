"""Claude 小人：按素材图（image.jpg）的造型与 11 种表情用矢量重绘。

坐标约定：(x, y) 是小人脚底中心（地面），s=1 时身体宽 300、总高约 250。
"""
import math

from .core import (TAU, clamp, ease_out, ellipse, glow, lerp, lin, rad,
                   rrect, setc, soft_shadow, star4, text)

C_BODY_T = "#E88E64"
C_BODY_B = "#C7694A"
C_RIM = "#F9E8B8"
C_LEG = "#A85B40"
C_LEG_D = "#7E412D"
C_LEG_L = "#F3C9A0"
C_EYE = "#26150F"
C_BROW = "#6E4739"
C_BLUSH = "#F7A595"
C_MOUTH = "#561918"
C_TONGUE = "#EF7E84"
C_HL = "#FCEED8"
C_OUT = "#8A452F"

BW, BH = 300, 196
LEG_H = 50
TOP = -(LEG_H + BH)          # 身体顶部 y = -246
EYE_X = 90
EYE_Y = TOP + 68
MOUTH_Y = TOP + 116
LEGS_X = (-115, -65, 65, 115)

EXPR = {
    "neutral":    dict(eyes="rect", ew=24, eh=50, brows=None, mouth=None, blush=False),
    "happy":      dict(eyes="caret", brows=None, mouth="smile", blush=True),
    "curious":    dict(eyes="rect", ew=25, eh=54, brows="curious", mouth="dot", blush=False),
    "think":      dict(eyes="think", ew=24, eh=50, brows="think", mouth=None, blush=False, bar="think"),
    "surprised":  dict(eyes="rect", ew=28, eh=64, brows="up", mouth="o", blush=False),
    "determined": dict(eyes="rect", ew=25, eh=44, brows="v", mouth="smirk", blush=False,
                       bar="fists", fx=("sparkle", "bulb")),
    "tired":      dict(eyes="small", brows="worried", mouth="o_small", blush=False),
    "sleep":      dict(eyes="closed", brows=None, mouth="tiny", blush=True, fx=("zzz",)),
    "yawn":       dict(eyes="closed", brows="flat", mouth="yawn", blush=True),
    "proud":      dict(eyes="caret", brows="flat", mouth="curve", blush=True),
    "excited":    dict(eyes="rect", ew=28, eh=64, brows="up", mouth="smile_big", blush=True),
}

# (左眉 dy, 左眉角度, 右眉 dy, 右眉角度)；角度为屏幕顺时针弧度
BROWS = {
    "curious": (-6, -0.16, -10, 0.12),
    "up":      (-12, -0.06, -12, 0.06),
    "v":       (6, 0.36, 6, -0.36),
    "worried": (2, -0.30, 2, 0.30),
    "flat":    (0, -0.05, 0, 0.05),
    "think":   (10, 0.38, -8, -0.10),
}


def blink_amount(t, seed=0.0, period=3.7):
    """返回 0..1 的眼睛睁开比例。"""
    ph = (t + seed * 1.37) % period
    if ph < 0.16:
        return 1 - math.sin(math.pi * ph / 0.16) * 0.92
    return 1.0


def _eye_rect(ctx, x, y, w, h, look):
    x += look[0]
    y += look[1]
    rrect(ctx, x - w / 2, y - h / 2, w, h, min(6, w / 3, h / 2))
    setc(ctx, C_EYE)
    ctx.fill()
    if h > 14:
        rrect(ctx, x - w / 2 + 4, y - h / 2 + 5, w * 0.3, min(13, h * 0.24), 2.5)
        setc(ctx, "#ffffff", 0.95)
        ctx.fill()
        ctx.arc(x + w * 0.18, y + h * 0.28, 2.4, 0, TAU)
        setc(ctx, "#ffffff", 0.9)
        ctx.fill()


def _caret(ctx, x, y, look):
    x += look[0]
    y += look[1]
    ctx.set_line_width(7.5)
    ctx.set_line_cap(1)
    ctx.set_line_join(1)
    setc(ctx, C_EYE)
    ctx.move_to(x - 19, y + 9)
    ctx.line_to(x, y - 11)
    ctx.line_to(x + 19, y + 9)
    ctx.stroke()


def _closed(ctx, x, y, look):
    x += look[0]
    y += look[1]
    ctx.set_line_width(6.5)
    ctx.set_line_cap(1)
    setc(ctx, C_EYE)
    ctx.move_to(x - 18, y - 2)
    ctx.curve_to(x - 9, y + 7, x + 9, y + 7, x + 18, y - 2)
    ctx.stroke()


def _brow(ctx, x, y, ang):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    rrect(ctx, -19, -4, 38, 8, 4)
    setc(ctx, C_BROW, 0.92)
    ctx.fill()
    ctx.restore()


def _mouth(ctx, kind, t):
    y = MOUTH_Y
    if kind is None:
        return
    if kind in ("smile", "smile_big"):
        w = 19 if kind == "smile" else 22
        d = 20 if kind == "smile" else 26
        ctx.move_to(-w, y - 6)
        ctx.line_to(w, y - 6)
        ctx.curve_to(w, y + d * 0.7, -w, y + d * 0.7, -w, y - 6)
        ctx.close_path()
        setc(ctx, C_MOUTH)
        ctx.fill()
        ellipse(ctx, 0, y + d * 0.38, w * 0.52, d * 0.2)
        setc(ctx, C_TONGUE)
        ctx.fill()
    elif kind == "dot":
        ellipse(ctx, 0, y, 7.5, 5.5)
        setc(ctx, C_MOUTH, 0.85)
        ctx.fill()
    elif kind in ("o", "o_small"):
        rx, ry = (10, 14) if kind == "o" else (9, 9)
        ellipse(ctx, 0, y, rx, ry)
        setc(ctx, C_MOUTH)
        ctx.fill()
        ellipse(ctx, 0, y + ry * 0.45, rx * 0.6, ry * 0.4)
        setc(ctx, C_TONGUE)
        ctx.fill()
    elif kind == "yawn":
        k = 1 + 0.15 * math.sin(t * 3)
        ellipse(ctx, 0, y + 2, 13, 18 * k)
        setc(ctx, C_MOUTH)
        ctx.fill()
        ellipse(ctx, 0, y + 2 + 18 * k * 0.5, 8, 6)
        setc(ctx, C_TONGUE)
        ctx.fill()
    elif kind == "tiny":
        ellipse(ctx, 0, y, 8, 3)
        setc(ctx, C_MOUTH, 0.35)
        ctx.fill()
    elif kind == "curve":
        ctx.set_line_width(5.5)
        ctx.set_line_cap(1)
        setc(ctx, C_MOUTH)
        ctx.move_to(-22, y - 5)
        ctx.curve_to(-10, y + 9, 10, y + 9, 22, y - 5)
        ctx.stroke()
    elif kind == "smirk":
        ctx.set_line_width(5)
        ctx.set_line_cap(1)
        setc(ctx, C_MOUTH)
        ctx.move_to(4, y)
        ctx.curve_to(14, y + 6, 24, y + 6, 34, y - 4)
        ctx.stroke()


def _bar(ctx, cx, cy, length, thick, ang):
    """前置手臂（思考/握拳时的长条手臂，带描边）。"""
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(ang)
    rrect(ctx, -length / 2, -thick / 2, length, thick, 10)
    ctx.set_source(lin(0, -thick / 2, 0, thick / 2, [(0, "#F59A6E"), (1, C_BODY_B)]))
    ctx.fill_preserve()
    ctx.set_line_width(4)
    setc(ctx, C_OUT, 0.9)
    ctx.stroke()
    rrect(ctx, -length / 2 + 10, -thick / 2 + 5, length * 0.45, 5, 2.5)
    setc(ctx, C_HL, 0.45)
    ctx.fill()
    ctx.restore()


def _stub(ctx, side, ang, length=46):
    """侧面短手臂（在身体后面），side=-1 左 / 1 右，ang>0 抬起。"""
    lift = clamp(ang / 0.9)
    px, py = side * (BW / 2 - 8 + 14 * lift), TOP + 118 - 30 * lift
    length += 14 * lift
    ctx.save()
    ctx.translate(px, py)
    ctx.rotate(-side * ang)
    x0 = -12 if side > 0 else -(length + 8)
    w = length + 20
    rrect(ctx, x0, -21 - 3, w, 44 + 3, 7)
    setc(ctx, C_RIM, 0.95)
    ctx.fill()
    rrect(ctx, x0, -21, w, 44, 7)
    ctx.set_source(lin(0, -21, 0, 23, [(0, "#EE8C62"), (1, C_BODY_B)]))
    ctx.fill()
    ctx.restore()


def _fx(ctx, names, t):
    for n in names:
        if n == "zzz":
            for i in range(3):
                ph = (t * 0.45 + i / 3) % 1
                a = math.sin(ph * math.pi)
                text(ctx, "Z", 120 + ph * 70 + i * 6, TOP - 10 - ph * 120, 26 + ph * 26,
                     "#FFFFFF", a * 0.95, "black", outline=C_OUT, outline_w=4)
        elif n == "sparkle":
            p = 0.75 + 0.25 * math.sin(t * 5)
            glow(ctx, 62, TOP + 104, 70 * p, "#FFF6C8", 0.55)
            star4(ctx, 62, TOP + 104, 30 * p, "#FFF8D8", 0.95, t * 0.6)
        elif n == "bulb":
            bx, by = 105, TOP - 46
            glow(ctx, bx, by, 150, "#FFE98A", 0.45)
            for k in range(9):
                a = k / 9 * TAU + t * 0.4
                r0, r1 = 34, 50 + 6 * math.sin(t * 4 + k)
                ctx.set_line_width(4)
                ctx.set_line_cap(1)
                setc(ctx, "#FFE27A", 0.75)
                ctx.move_to(bx + math.cos(a) * r0, by + math.sin(a) * r0)
                ctx.line_to(bx + math.cos(a) * r1, by + math.sin(a) * r1)
                ctx.stroke()
            ctx.arc(bx, by - 3, 20, 0, TAU)
            ctx.set_source(rad(bx - 6, by - 9, 2, 22, [(0, "#FFFFFF"), (1, "#FFE173")]))
            ctx.fill()
            rrect(ctx, bx - 9, by + 14, 18, 12, 3)
            setc(ctx, "#B9A68A")
            ctx.fill()
        elif n == "question":
            bob = math.sin(t * 3) * 5
            text(ctx, "?", -100, TOP - 40 + bob, 64, "#FFFFFF", 1, "black",
                 outline="#5a3a30", outline_w=6)
        elif n == "sweat":
            x, y = -168, TOP + 108 + math.sin(t * 2) * 3
            ctx.move_to(x, y - 22)
            ctx.curve_to(x + 4, y - 10, x + 13, y - 2, x + 13, y + 6)
            ctx.curve_to(x + 13, y + 14, x - 13, y + 14, x - 13, y + 6)
            ctx.curve_to(x - 13, y - 2, x - 4, y - 10, x, y - 22)
            ctx.set_source(rad(x - 4, y, 1, 18, [(0, "#E8F7FF"), (1, "#69B9E8")]))
            ctx.fill()


def draw_claude(ctx, x, y, s=1.0, expr="neutral", t=0.0, walk=None,
                arm_l=0.0, arm_r=0.0, look=(0, 0), seed=0.0, squash=0.0,
                fx=None, shadow=True, flip=False, bar=True, blink=True):
    """绘制 Claude。

    walk: 行走相位（圈数，None=站立）；arm_l/arm_r: 侧手臂抬起角度（弧度）；
    squash: 挤压拉伸（正值压扁）；fx: 额外特效，None=按表情默认。
    """
    e = EXPR[expr]
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(-s if flip else s, s)

    if shadow:
        soft_shadow(ctx, 0, 2, 175, 18, 0.30)

    # 腿 ---------------------------------------------------------------
    bob = 0.0
    lifts, swings = [0, 0, 0, 0], [0, 0, 0, 0]
    if walk is not None:
        ph = walk * TAU
        bob = -abs(math.sin(ph)) * 6
        for i in range(4):
            sgn = 1 if i in (0, 2) else -1
            lifts[i] = max(0.0, sgn * math.sin(ph)) * 15
            swings[i] = sgn * math.cos(ph) * 8
    for i, lx in enumerate(LEGS_X):
        lx += swings[i]
        top = -LEG_H - 10 + bob
        h = (-lifts[i]) - top
        rrect(ctx, lx - 10, top, 20, h, 2)
        ctx.set_source(lin(0, top, 0, -lifts[i], [(0, C_LEG_D), (0.35, C_LEG), (1, "#B8664A")]))
        ctx.fill()
        ctx.rectangle(lx - 10, top + 12, 5, h - 12)
        setc(ctx, C_LEG_L, 0.85)
        ctx.fill()

    # 身体组 -------------------------------------------------------------
    breathe = 0.012 * math.sin(t * 2.3)
    sq = squash + breathe
    ctx.translate(0, bob - LEG_H)
    ctx.scale(1 + sq * 0.6, 1 - sq)
    ctx.translate(0, LEG_H)

    _stub(ctx, -1, arm_l)
    _stub(ctx, 1, arm_r)

    rrect(ctx, -BW / 2 + 1, TOP - 5, BW + 5, BH + 4, 13)
    setc(ctx, C_RIM)
    ctx.fill()
    rrect(ctx, -BW / 2, TOP, BW, BH, 12)
    ctx.set_source(lin(0, TOP, 0, TOP + BH, [(0, C_BODY_T), (0.55, "#DB7A55"), (1, C_BODY_B)]))
    ctx.fill_preserve()
    ctx.set_source(rad(-60, TOP + 40, 10, 260, [(0, "#FFFFFF", 0.10), (1, "#FFFFFF", 0)]))
    ctx.fill()
    rrect(ctx, -BW / 2 + 18, TOP + 8, 92, 11, 5.5)
    setc(ctx, C_HL, 0.80)
    ctx.fill()

    # 脸 ---------------------------------------------------------------
    if e.get("blush"):
        for sx in (-1, 1):
            bx, by = sx * (EYE_X + 10), TOP + 112
            ctx.save()
            ctx.translate(bx, by)
            ctx.scale(1, 0.5)
            ctx.set_source(rad(0, 0, 0, 25, [(0, C_BLUSH, 0.95), (0.7, C_BLUSH, 0.8), (1, C_BLUSH, 0)]))
            ctx.arc(0, 0, 25, 0, TAU)
            ctx.fill()
            ctx.restore()

    op = blink_amount(t, seed) if blink else 1.0
    kind = e["eyes"]
    for sx in (-1, 1):
        ex = sx * EYE_X
        if kind == "rect":
            _eye_rect(ctx, ex, EYE_Y, e["ew"], e["eh"] * op, look)
        elif kind == "caret":
            _caret(ctx, ex, EYE_Y, look)
        elif kind == "closed":
            _closed(ctx, ex, EYE_Y + 4, look)
        elif kind == "small":
            _eye_rect(ctx, ex, EYE_Y + 6, 26, 24 * op, look)
            ctx.arc(ex - 2 + look[0], EYE_Y - 18, 3.5, 0, TAU)
            setc(ctx, "#FFE9DD", 0.8)
            ctx.fill()
        elif kind == "think":
            if sx < 0:
                _eye_rect(ctx, ex, EYE_Y + 12, 24, 22 * op, look)
            else:
                _eye_rect(ctx, ex, EYE_Y, 24, 50 * op, look)

    b = e.get("brows")
    if b:
        dl, al, dr, ar = BROWS[b]
        _brow(ctx, -EYE_X, TOP + 18 + dl, al)
        _brow(ctx, EYE_X, TOP + 18 + dr, ar)

    _mouth(ctx, e.get("mouth"), t)

    if bar and e.get("bar") == "think":
        _bar(ctx, -40, TOP + 108, 236, 46, -0.27)
    elif bar and e.get("bar") == "fists":
        _bar(ctx, -150, TOP + 160, 140, 48, 0.78)
        _bar(ctx, 150, TOP + 160, 140, 48, -0.78)

    names = e.get("fx", ()) if fx is None else fx
    if names:
        _fx(ctx, names, t)
    ctx.restore()


def expr_pop(since, amp=0.07):
    """表情切换时的弹性挤压。"""
    if since < 0 or since > 0.6:
        return 0.0
    return amp * math.sin(since * 18) * math.exp(-since * 7)


def wave(t, base=0.9, amp=0.45, speed=9.0):
    """挥手角度。"""
    return base + amp * math.sin(t * speed)


def hop(t, t0, height=40, dur=0.45):
    """在 t0 时刻跳一下，返回 y 偏移（负数向上）与挤压值。"""
    u = (t - t0) / dur
    if u < 0 or u > 1:
        if 1 < u < 1.4:
            return 0.0, 0.08 * math.sin((u - 1) / 0.4 * math.pi)
        return 0.0, 0.0
    return -math.sin(u * math.pi) * height, -0.05 * math.sin(u * math.pi)


def walk_x(t, t0, t1, x0, x1):
    """在 [t0, t1] 内从 x0 走到 x1，返回 (x, 行走相位或 None)。"""
    if t <= t0:
        return x0, None
    if t >= t1:
        return x1, None
    u = (t - t0) / (t1 - t0)
    # 头尾稍微减速
    k = clamp(u * 1.0)
    x = lerp(x0, x1, k)
    dist = abs(x1 - x0)
    return x, (abs(x - x0) / 95.0) % 1.0 if dist else None


__all__ = ["draw_claude", "expr_pop", "wave", "hop", "walk_x", "EXPR", "TOP",
           "blink_amount", "ease_out"]
