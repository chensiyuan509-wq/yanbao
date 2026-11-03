"""脸部零件：眼睛、眉毛、嘴巴、腮红。全部在"身体局部坐标"里绘制。"""
import math

import cairo

from .const import (BLUSH_Y, C_BLUSH, C_EYE, C_MOUTH, C_TEAR, C_TEETH, C_TONGUE, C_BROW, EYE_X,
                    MOUTH_Y)
from .gfx import (TAU, circle, clamp, ellipse, fill, heart, lerp, rad, rrect, setc, star4, star5,
                  stroke)

# ---------------------------------------------------------------- 眼睛


def _eye_rect(ctx, x, y, w, h, a=1.0, shine=0):
    if h < 1.2:
        ctx.move_to(x - w / 2, y)
        ctx.line_to(x + w / 2, y)
        stroke(ctx, C_EYE, 5, a)
        return
    rrect(ctx, x - w / 2, y - h / 2, w, h, min(6.5, w / 3, h / 2))
    fill(ctx, C_EYE, a)
    if h > 16:
        rrect(ctx, x - w / 2 + 4, y - h / 2 + 5, w * 0.32, min(13, h * 0.24), 2.6)
        fill(ctx, "#FFFFFF", 0.96 * a)
        circle(ctx, x + w * 0.17, y + h * 0.27, 2.5)
        fill(ctx, "#FFFFFF", 0.9 * a)
        if shine:
            star4(ctx, x + w * 0.12, y - h * 0.05, 7 + 2 * shine, "#FFFFFF", 0.95 * a, 0.3)
            circle(ctx, x - w * 0.18, y + h * 0.18, 3.2)
            fill(ctx, "#FFFFFF", 0.8 * a)


def _caret(ctx, x, y, k=1.0, a=1.0, flip=False):
    if k <= 0.02:
        return
    d = -1 if flip else 1
    ctx.move_to(x - 19, y + 9 * k * d)
    ctx.line_to(x, y - 11 * k * d)
    ctx.line_to(x + 19, y + 9 * k * d)
    stroke(ctx, C_EYE, 7.5, a)


def _closed(ctx, x, y, k=1.0, a=1.0, down=False):
    """闭眼弧线：默认向下弯（放松 / 睡着）；down=True 为向上拱（难过）。"""
    s = -1 if down else 1
    ctx.move_to(x - 18, y - 2 * s)
    ctx.curve_to(x - 9, y - 2 * s + 9 * k * s, x + 9, y - 2 * s + 9 * k * s, x + 18, y - 2 * s)
    stroke(ctx, C_EYE, 6.5, a)


def _half(ctx, x, y, w, h, lid, slant, side, a=1.0):
    """半眯眼：上眼睑盖住 lid 比例，slant>0 时外侧更低（不屑 / 慵懒）。"""
    top = y - h / 2
    ly = top + h * clamp(lid)
    dy = slant * side * (w / 2 + 6)
    x0, x1 = x - w / 2 - 6, x + w / 2 + 6
    ctx.save()
    ctx.move_to(x0, ly - dy)
    ctx.line_to(x1, ly + dy)
    ctx.line_to(x1, y + h)
    ctx.line_to(x0, y + h)
    ctx.close_path()
    ctx.clip()
    _eye_rect(ctx, x, y, w, h, a)
    ctx.restore()
    ctx.move_to(x0 + 2, ly - dy * 0.9)
    ctx.line_to(x1 - 2, ly + dy * 0.9)
    stroke(ctx, C_EYE, 6, a)


def _spiral(ctx, x, y, t, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(t * 5)
    ctx.move_to(0, 0)
    for i in range(1, 60):
        ang = i * 0.28
        r = i * 0.36
        ctx.line_to(math.cos(ang) * r, math.sin(ang) * r)
    stroke(ctx, C_EYE, 4.2, a)
    ctx.restore()


def _teary(ctx, x, y, w, h, a=1.0, t=0.0, side=1):
    _eye_rect(ctx, x, y, w, h, a, shine=1)
    # 下眼眶的泪光
    ctx.save()
    rrect(ctx, x - w / 2, y - h / 2, w, h, min(6.5, w / 3, h / 2))
    ctx.clip()
    wob = math.sin(t * 6 + side) * 2
    ctx.move_to(x - w / 2 - 2, y + h * 0.22 + wob)
    ctx.curve_to(x - w * 0.2, y + h * 0.12 - wob, x + w * 0.2, y + h * 0.3 + wob, x + w / 2 + 2, y + h * 0.18)
    ctx.line_to(x + w / 2 + 2, y + h)
    ctx.line_to(x - w / 2 - 2, y + h)
    ctx.close_path()
    fill(ctx, C_TEAR, 0.55 * a)
    ctx.restore()


def draw_eye(ctx, kind, side, x, y, op, t=0.0, a=1.0):
    """kind 为元组，第一项是种类；op 为睁开度 0..1（眨眼 / 换形）。side=-1 左眼，1 右眼。"""
    k = kind[0]
    if k == "rect":
        _eye_rect(ctx, x, y, kind[1], kind[2] * op, a)
    elif k == "shine":
        _eye_rect(ctx, x, y, kind[1], kind[2] * op, a, shine=1 + 0.5 * math.sin(t * 7 + side))
    elif k == "caret":
        _caret(ctx, x, y + (1 - op) * 4, op, a)
    elif k == "closed":
        _closed(ctx, x, y + 4, 0.3 + 0.7 * op, a)
    elif k == "sad_closed":
        _closed(ctx, x, y + 6, 0.3 + 0.7 * op, a, down=True)
    elif k == "small":
        _eye_rect(ctx, x, y + 7, 26, 24 * op, a)
        circle(ctx, x - 3, y - 17, 3.5)
        fill(ctx, "#FFE9DD", 0.75 * a * op)
    elif k == "think":
        if side < 0:
            _eye_rect(ctx, x, y + 12, 24, 22 * op, a)
        else:
            _eye_rect(ctx, x, y, 24, 50 * op, a)
    elif k == "wink":
        if side < 0:
            _caret(ctx, x, y + 2, op, a)
        else:
            _eye_rect(ctx, x, y, kind[1], kind[2] * op, a)
    elif k == "half":
        w, h, lid, slant = kind[1], kind[2], kind[3], kind[4] if len(kind) > 4 else 0.0
        _half(ctx, x, y, w, h, lerp(1.0, lid, op), slant, side, a)
    elif k == "half_l":          # 只眯左眼（怀疑）
        w, h, lid = kind[1], kind[2], kind[3]
        if side < 0:
            _half(ctx, x, y + 3, w, h, lerp(1.0, lid, op), 0.0, side, a)
        else:
            _eye_rect(ctx, x, y, w, h * op, a)
    elif k == "heart":
        s = 21 * (0.35 + 0.65 * op) * (1 + 0.08 * math.sin(t * 9))
        heart(ctx, x, y, s, "#FF4F78", a)
    elif k == "star":
        s = 25 * (0.35 + 0.65 * op)
        star5(ctx, x, y, s, "#FFC93C", a, math.sin(t * 3) * 0.15)
        star5(ctx, x, y, s * 0.45, "#FFF6C8", a, math.sin(t * 3) * 0.15)
    elif k == "spiral":
        _spiral(ctx, x, y, t * (1 if side > 0 else -1), a)
    elif k == "x":               # >  < （大笑 / 用力）
        d = 1 if side < 0 else -1
        ctx.move_to(x - 16 * d, y - 13 * op)
        ctx.line_to(x + 14 * d, y)
        ctx.line_to(x - 16 * d, y + 13 * op)
        stroke(ctx, C_EYE, 7.5, a)
    elif k == "cross":           # ✕ ✕（晕倒）
        for sx, sy in ((1, 1), (1, -1)):
            ctx.move_to(x - 14 * sx, y - 14 * sy * op)
            ctx.line_to(x + 14 * sx, y + 14 * sy * op)
        stroke(ctx, C_EYE, 7, a)
    elif k == "dot":
        rrect(ctx, x - 7, y - 8 * op, 14, max(1.5, 16 * op), 4)
        fill(ctx, C_EYE, a)
    elif k == "line":
        ctx.move_to(x - 15, y + 4)
        ctx.line_to(x + 15, y + 4)
        stroke(ctx, C_EYE, 6.5, a)
    elif k == "teary":
        _teary(ctx, x, y, kind[1], kind[2] * op, a, t, side)
    elif k == "wide":            # 惊恐：小瞳孔 + 白眼眶
        rrect(ctx, x - 17, y - 30 * op, 34, 60 * op, 12)
        fill(ctx, "#FFFFFF", a)
        ctx.set_line_width(4)
        setc(ctx, C_EYE, a)
        rrect(ctx, x - 17, y - 30 * op, 34, 60 * op, 12)
        ctx.stroke()
        circle(ctx, x, y, 7 * op)
        fill(ctx, C_EYE, a)


# ---------------------------------------------------------------- 眉毛


def draw_brow(ctx, x, y, ang, a, thick=1.0):
    if a <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    h = 8.4 * thick
    rrect(ctx, -19, -h / 2, 38, h, h / 2)
    setc(ctx, C_BROW, 0.93 * a)
    ctx.fill()
    ctx.restore()


# ---------------------------------------------------------------- 嘴巴


def _d_mouth(ctx, w, d):
    ctx.move_to(-w, -6)
    ctx.line_to(w, -6)
    ctx.curve_to(w, d * 0.75, -w, d * 0.75, -w, -6)
    ctx.close_path()


def draw_mouth(ctx, kind, t, k=1.0, talk=0.0, smile=0.0):
    """在 MOUTH_Y 处画嘴。k 为缩放（过渡用），talk 为说话张口度，smile 让说话嘴角上扬。"""
    if kind is None or k <= 0.02:
        return
    ctx.save()
    ctx.translate(0, MOUTH_Y)
    ctx.scale(k, k)
    lw = 5.5
    if kind in ("smile", "smile_big", "laugh", "grin"):
        w, d = {"smile": (19, 20), "smile_big": (23, 27), "laugh": (29, 38), "grin": (27, 24)}[kind]
        if kind == "laugh":
            d += 2 * math.sin(t * 22)
        _d_mouth(ctx, w, d)
        fill(ctx, C_MOUTH)
        if kind == "grin":
            ctx.save()
            _d_mouth(ctx, w, d)
            ctx.clip()
            ctx.rectangle(-w, -7, 2 * w, 9)
            fill(ctx, C_TEETH)
            ctx.restore()
        ellipse(ctx, 0, d * 0.38, w * 0.5, d * 0.19)
        fill(ctx, C_TONGUE)
    elif kind == "talk":
        o = talk
        w = 15 + 4 * o + 4 * smile
        dd = 4 + 20 * o
        lift = 5 * smile
        ctx.move_to(-w, -5 - lift)
        ctx.curve_to(-w * 0.6, -7 + lift * 0.2, w * 0.6, -7 + lift * 0.2, w, -5 - lift)
        ctx.curve_to(w, dd * 0.8, -w, dd * 0.8, -w, -5 - lift)
        ctx.close_path()
        fill(ctx, C_MOUTH)
        if o > 0.35:
            ellipse(ctx, 0, dd * 0.42, w * 0.45, dd * 0.16)
            fill(ctx, C_TONGUE)
    elif kind == "dot":
        ellipse(ctx, 0, 0, 7.5, 5.5)
        fill(ctx, C_MOUTH, 0.85)
    elif kind in ("o", "o_small", "o_big", "o_wide"):
        rx, ry = {"o": (10, 14), "o_small": (8.5, 8.5), "o_big": (15, 21), "o_wide": (22, 25)}[kind]
        if kind == "o_wide":
            ry += 2 * math.sin(t * 20)
        ellipse(ctx, 0, 0, rx, ry)
        fill(ctx, C_MOUTH)
        ellipse(ctx, 0, ry * 0.45, rx * 0.6, ry * 0.4)
        fill(ctx, C_TONGUE)
    elif kind == "yawn":
        q = 1 + 0.15 * math.sin(t * 3)
        ellipse(ctx, 0, 2, 13, 18 * q)
        fill(ctx, C_MOUTH)
        ellipse(ctx, 0, 2 + 18 * q * 0.5, 8, 6)
        fill(ctx, C_TONGUE)
    elif kind == "tiny":
        ellipse(ctx, 0, 0, 8, 3)
        fill(ctx, C_MOUTH, 0.35)
    elif kind == "curve":
        ctx.move_to(-22, -5)
        ctx.curve_to(-10, 9, 10, 9, 22, -5)
        stroke(ctx, C_MOUTH, lw)
    elif kind == "smile_small":
        ctx.move_to(-13, -3)
        ctx.curve_to(-6, 5, 6, 5, 13, -3)
        stroke(ctx, C_MOUTH, 5)
    elif kind == "smirk":
        ctx.move_to(4, 0)
        ctx.curve_to(14, 6, 24, 6, 34, -4)
        stroke(ctx, C_MOUTH, 5)
    elif kind == "side":
        ctx.move_to(-4, 3)
        ctx.curve_to(6, 4, 14, 1, 24, -5)
        stroke(ctx, C_MOUTH, 5)
    elif kind == "frown":
        ctx.move_to(-18, 6)
        ctx.curve_to(-8, -6, 8, -6, 18, 6)
        stroke(ctx, C_MOUTH, lw)
    elif kind == "open_frown":
        w, d = 20, 22
        ctx.move_to(-w, 10)
        ctx.curve_to(-w, -d * 0.7, w, -d * 0.7, w, 10)
        ctx.close_path()
        fill(ctx, C_MOUTH)
        ellipse(ctx, 0, 6, w * 0.45, 4)
        fill(ctx, C_TONGUE)
    elif kind == "wavy":
        ctx.move_to(-20, 2)
        for i in range(1, 9):
            ctx.line_to(-20 + i * 5, 2 + (3.5 if i % 2 else -3.5))
        stroke(ctx, C_MOUTH, 4.5)
    elif kind == "flat":
        ctx.move_to(-16, 0)
        ctx.line_to(16, 0)
        stroke(ctx, C_MOUTH, 5)
    elif kind == "teeth":
        rrect(ctx, -22, -9, 44, 18, 6)
        fill(ctx, C_TEETH)
        ctx.set_line_width(2.4)
        setc(ctx, C_MOUTH)
        ctx.move_to(-22, 0)
        ctx.line_to(22, 0)
        for xx in (-11, 0, 11):
            ctx.move_to(xx, -9)
            ctx.line_to(xx, 9)
        ctx.stroke()
        rrect(ctx, -22, -9, 44, 18, 6)
        stroke(ctx, C_MOUTH, 4)
    elif kind == "cat":
        ctx.move_to(-20, -4)
        ctx.curve_to(-18, 6, -4, 6, 0, -2)
        ctx.curve_to(4, 6, 18, 6, 20, -4)
        stroke(ctx, C_MOUTH, 5)
    elif kind == "pout":
        ellipse(ctx, 0, 0, 9, 7.5)
        fill(ctx, C_MOUTH)
        ellipse(ctx, -2, -2, 3.5, 2)
        fill(ctx, C_TONGUE, 0.8)
    ctx.restore()


# ---------------------------------------------------------------- 腮红


def draw_blush(ctx, k):
    if k <= 0.01:
        return
    for sx in (-1, 1):
        bx, by = sx * (EYE_X + 10), BLUSH_Y
        ctx.save()
        ctx.translate(bx, by)
        ctx.scale(1, 0.5)
        ctx.set_source(rad(0, 0, 0, 26, [(0, C_BLUSH, 0.95 * k), (0.7, C_BLUSH, 0.8 * k), (1, C_BLUSH, 0)]))
        circle(ctx, 0, 0, 26)
        ctx.fill()
        ctx.restore()
