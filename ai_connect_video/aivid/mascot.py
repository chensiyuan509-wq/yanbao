"""小橙：按素材 assets/image.jpg 的造型与 11 种表情用矢量重绘，并扩展了动作系统。

坐标约定：(x, y) 为脚底中心（地面），s=1 时身体宽 300、总高约 250。

- 表情切换不是硬切：眼型不同则"眨眼换形"，眉毛 / 腮红平滑插值，嘴巴缩放交替；
- 自然随机眨眼、视线（带头部转向的视差）、呼吸、待机微摆；
- 跳跃有预备下蹲、腾空拉伸、落地挤压回弹；走路时四条腿交替、身体起伏；
- 手臂可挥手、抬起、伸长（"够不着"）、打字；还可以"说话"（口型随机开合）。
"""
import math

from .core import (TAU, circle, clamp, ease_back, ease_io, ease_out, ellipse, fill, glow,
                   group_alpha, kf, lerp, lin, noise, rad, rrect, setc, smooth, soft_shadow,
                   star4, text)

# ---------------------------------------------------------------- 造型常量
C_BODY_T = "#EE9669"
C_BODY_M = "#DE7C56"
C_BODY_B = "#C6664A"
C_RIM = "#FBE9BB"
C_LEG = "#A85B40"
C_LEG_D = "#6E3828"
C_LEG_L = "#F3C9A0"
C_EYE = "#24130E"
C_BROW = "#6B4436"
C_BLUSH = "#F8A396"
C_MOUTH = "#561918"
C_TONGUE = "#EF7E84"
C_HL = "#FFF1DB"
C_OUT = "#8A452F"

BW, BH = 300, 196
LEG_H = 50
TOP = -(LEG_H + BH)          # 身体顶部 y = -246
EYE_X = 90
EYE_Y = TOP + 70
MOUTH_Y = TOP + 120
LEGS_X = (-117, -67, 63, 113)
BLEND = 0.26                 # 表情过渡时长

EXPR = {
    "neutral":    dict(eyes=("rect", 24, 50), brows=None, mouth=None, blush=0.0),
    "happy":      dict(eyes=("caret",), brows=None, mouth="smile", blush=1.0),
    "curious":    dict(eyes=("rect", 25, 54), brows="curious", mouth="dot", blush=0.0),
    "think":      dict(eyes=("think",), brows="think", mouth=None, blush=0.0),
    "surprised":  dict(eyes=("rect", 29, 66), brows="up", mouth="o", blush=0.0),
    "determined": dict(eyes=("rect", 25, 42), brows="v", mouth="smirk", blush=0.0),
    "tired":      dict(eyes=("small",), brows="worried", mouth="o_small", blush=0.0),
    "sleep":      dict(eyes=("closed",), brows=None, mouth="tiny", blush=1.0),
    "yawn":       dict(eyes=("closed",), brows="flat", mouth="yawn", blush=1.0),
    "proud":      dict(eyes=("caret",), brows="flat", mouth="curve", blush=1.0),
    "excited":    dict(eyes=("rect", 29, 66), brows="up", mouth="smile_big", blush=1.0),
    # 扩展表情
    "sad":        dict(eyes=("rect", 24, 38), brows="worried", mouth="frown", blush=0.0),
    "worried":    dict(eyes=("rect", 23, 46), brows="worried", mouth="wavy", blush=0.0),
    "wink":       dict(eyes=("wink", 25, 54), brows="curious", mouth="smile", blush=1.0),
    "smile":      dict(eyes=("rect", 25, 52), brows=None, mouth="curve", blush=0.6),
    "shock":      dict(eyes=("rect", 30, 70), brows="up", mouth="o_big", blush=0.0),
}

# (左眉 dy, 左眉角度, 右眉 dy, 右眉角度)
BROWS = {
    None:      (0, 0.0, 0, 0.0),
    "curious": (-7, -0.16, -12, 0.12),
    "up":      (-13, -0.06, -13, 0.06),
    "v":       (6, 0.38, 6, -0.38),
    "worried": (1, -0.32, 1, 0.32),
    "flat":    (0, -0.05, 0, 0.05),
    "think":   (10, 0.38, -9, -0.10),
}

DEFAULT_FX = {"sleep": ("zzz",), "determined": ("sparkle",)}


# ---------------------------------------------------------------- 眨眼


def _blink_times(seed):
    """生成确定性的"自然"眨眼时刻（间隔 2.4–5.2 秒，偶尔连眨两下）。"""
    import random
    R = random.Random(int(seed * 1000) + 17)
    out, t = [], R.uniform(0.4, 2.5)
    while t < 400:
        out.append(t)
        if R.random() < 0.18:
            out.append(t + 0.26)
        t += R.uniform(2.4, 5.2)
    return out


_BLINK_CACHE = {}


def blink_open(t, seed=0.0):
    """返回眼睛睁开比例 0..1。"""
    bt = _BLINK_CACHE.get(seed)
    if bt is None:
        bt = _BLINK_CACHE[seed] = _blink_times(seed)
    best = 1.0
    for tb in bt:
        if tb > t + 0.01:
            break
        d = t - tb
        if 0 <= d < 0.17:
            best = min(best, 1 - math.sin(math.pi * d / 0.17) * 0.95)
    return best


# ---------------------------------------------------------------- 脸部零件


def _eye_rect(ctx, x, y, w, h, a=1.0):
    if h < 1.2:
        ctx.set_line_width(5)
        ctx.set_line_cap(1)
        setc(ctx, C_EYE, a)
        ctx.move_to(x - w / 2, y)
        ctx.line_to(x + w / 2, y)
        ctx.stroke()
        return
    rrect(ctx, x - w / 2, y - h / 2, w, h, min(6.5, w / 3, h / 2))
    fill(ctx, C_EYE, a)
    if h > 16:
        rrect(ctx, x - w / 2 + 4, y - h / 2 + 5, w * 0.32, min(13, h * 0.24), 2.6)
        fill(ctx, "#FFFFFF", 0.96 * a)
        circle(ctx, x + w * 0.17, y + h * 0.27, 2.5)
        fill(ctx, "#FFFFFF", 0.9 * a)


def _caret(ctx, x, y, k=1.0, a=1.0):
    if k <= 0.02:
        return
    ctx.set_line_width(7.5)
    ctx.set_line_cap(1)
    ctx.set_line_join(1)
    setc(ctx, C_EYE, a)
    ctx.move_to(x - 19, y + 9 * k)
    ctx.line_to(x, y - 11 * k)
    ctx.line_to(x + 19, y + 9 * k)
    ctx.stroke()


def _closed(ctx, x, y, k=1.0, a=1.0):
    ctx.set_line_width(6.5)
    ctx.set_line_cap(1)
    setc(ctx, C_EYE, a)
    ctx.move_to(x - 18, y - 2)
    ctx.curve_to(x - 9, y - 2 + 9 * k, x + 9, y - 2 + 9 * k, x + 18, y - 2)
    ctx.stroke()


def _draw_eye(ctx, kind, side, x, y, op, look, a=1.0):
    """op: 0..1 睁开度（也用于换形过渡）。"""
    x += look[0]
    y += look[1]
    k = kind[0]
    if k == "rect":
        _eye_rect(ctx, x, y, kind[1], kind[2] * op, a)
    elif k == "caret":
        _caret(ctx, x, y + (1 - op) * 4, op, a)
    elif k == "closed":
        _closed(ctx, x, y + 4, 0.3 + 0.7 * op, a)
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


def _brow(ctx, x, y, ang, a):
    if a <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    rrect(ctx, -19, -4.2, 38, 8.4, 4.2)
    setc(ctx, C_BROW, 0.93 * a)
    ctx.fill()
    ctx.restore()


def _mouth(ctx, kind, t, k=1.0, talk=0.0):
    """k: 0..1 缩放（过渡）。"""
    if kind is None or k <= 0.02:
        return
    y = MOUTH_Y
    ctx.save()
    ctx.translate(0, y)
    ctx.scale(k, k)
    if kind in ("smile", "smile_big"):
        w = 19 if kind == "smile" else 23
        d = 20 if kind == "smile" else 27
        ctx.move_to(-w, -6)
        ctx.line_to(w, -6)
        ctx.curve_to(w, d * 0.75, -w, d * 0.75, -w, -6)
        ctx.close_path()
        fill(ctx, C_MOUTH)
        ellipse(ctx, 0, d * 0.36, w * 0.5, d * 0.19)
        fill(ctx, C_TONGUE)
    elif kind == "talk":
        o = talk
        w = 15 + 4 * o
        d = 4 + 20 * o
        ctx.move_to(-w, -5)
        ctx.curve_to(-w * 0.6, -7, w * 0.6, -7, w, -5)
        ctx.curve_to(w, d * 0.8, -w, d * 0.8, -w, -5)
        ctx.close_path()
        fill(ctx, C_MOUTH)
        if o > 0.35:
            ellipse(ctx, 0, d * 0.42, w * 0.45, d * 0.16)
            fill(ctx, C_TONGUE)
    elif kind == "dot":
        ellipse(ctx, 0, 0, 7.5, 5.5)
        fill(ctx, C_MOUTH, 0.85)
    elif kind in ("o", "o_small", "o_big"):
        rx, ry = {"o": (10, 14), "o_small": (8.5, 8.5), "o_big": (15, 21)}[kind]
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
        ctx.set_line_width(5.5)
        ctx.set_line_cap(1)
        setc(ctx, C_MOUTH)
        ctx.move_to(-22, -5)
        ctx.curve_to(-10, 9, 10, 9, 22, -5)
        ctx.stroke()
    elif kind == "smirk":
        ctx.set_line_width(5)
        ctx.set_line_cap(1)
        setc(ctx, C_MOUTH)
        ctx.move_to(4, 0)
        ctx.curve_to(14, 6, 24, 6, 34, -4)
        ctx.stroke()
    elif kind == "frown":
        ctx.set_line_width(5.5)
        ctx.set_line_cap(1)
        setc(ctx, C_MOUTH)
        ctx.move_to(-18, 6)
        ctx.curve_to(-8, -6, 8, -6, 18, 6)
        ctx.stroke()
    elif kind == "wavy":
        ctx.set_line_width(4.5)
        ctx.set_line_cap(1)
        setc(ctx, C_MOUTH)
        ctx.move_to(-20, 2)
        for i in range(1, 9):
            ctx.line_to(-20 + i * 5, 2 + (3.5 if i % 2 else -3.5))
        ctx.stroke()
    ctx.restore()


def _front_bar(ctx, cx, cy, length, thick, ang):
    """前置长条手臂（思考 / 握拳时）。"""
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


def _stub(ctx, side, ang, ext=0.0, length=46):
    """侧面短手臂（画在身体后面）。side=-1 左 / 1 右；ang>0 抬起；ext 伸长像素。"""
    lift = clamp(ang / 0.9)
    px, py = side * (BW / 2 - 8 + 14 * lift), TOP + 120 - 30 * lift
    length += 14 * lift + ext
    ctx.save()
    ctx.translate(px, py)
    ctx.rotate(-side * ang)
    x0 = -12 if side > 0 else -(length + 8)
    w = length + 20
    rrect(ctx, x0 - 1, -24, w + 2, 47, 8)
    setc(ctx, C_RIM, 0.95)
    ctx.fill()
    rrect(ctx, x0, -21, w, 44, 7)
    ctx.set_source(lin(0, -21, 0, 23, [(0, "#EE8C62"), (1, C_BODY_B)]))
    ctx.fill()
    ctx.restore()


def _fx(ctx, names, t, a=1.0):
    for n in names:
        if n == "zzz":
            for i in range(3):
                ph = (t * 0.42 + i / 3) % 1
                k = math.sin(ph * math.pi)
                text(ctx, "Z", 128 + ph * 70 + i * 4, TOP - 6 - ph * 120, 26 + ph * 26,
                     "#FFFFFF", k * 0.95 * a, "black", outline=C_OUT, outline_w=4)
        elif n == "sparkle":
            p = 0.75 + 0.25 * math.sin(t * 5)
            glow(ctx, 70, TOP + 106, 70 * p, "#FFF6C8", 0.5 * a)
            star4(ctx, 70, TOP + 106, 28 * p, "#FFF8D8", 0.95 * a, t * 0.6)
        elif n == "bulb":
            bx, by = 105, TOP - 50
            glow(ctx, bx, by, 150, "#FFE98A", 0.45 * a)
            for k in range(9):
                ang = k / 9 * TAU + t * 0.4
                r0, r1 = 34, 50 + 6 * math.sin(t * 4 + k)
                ctx.set_line_width(4)
                ctx.set_line_cap(1)
                setc(ctx, "#FFE27A", 0.75 * a)
                ctx.move_to(bx + math.cos(ang) * r0, by + math.sin(ang) * r0)
                ctx.line_to(bx + math.cos(ang) * r1, by + math.sin(ang) * r1)
                ctx.stroke()
            circle(ctx, bx, by - 3, 20)
            ctx.set_source(rad(bx - 6, by - 9, 2, 22, [(0, "#FFFFFF", a), (1, "#FFE173", a)]))
            ctx.fill()
            rrect(ctx, bx - 9, by + 14, 18, 12, 3)
            fill(ctx, "#B9A68A", a)
        elif n == "question":
            bob = math.sin(t * 3) * 6
            text(ctx, "?", -112, TOP - 44 + bob, 70, "#FFFFFF", a, "black", outline="#5a3a30", outline_w=7)
        elif n == "question2":
            for i, (qx, qy, qs) in enumerate(((-120, -40, 70), (-40, -84, 52), (118, -52, 60))):
                bob = math.sin(t * 3 + i * 1.7) * 6
                text(ctx, "?", qx, TOP + qy + bob, qs, "#FFFFFF", a, "black", outline="#5a3a30", outline_w=6)
        elif n == "exclaim":
            k = 1 + 0.08 * math.sin(t * 12)
            text(ctx, "!", 0, TOP - 58, 86 * k, "#FFD25C", a, "black", outline="#5a3a30", outline_w=7)
        elif n == "sweat":
            x, y = -170, TOP + 104 + math.sin(t * 2.2) * 4
            ctx.move_to(x, y - 22)
            ctx.curve_to(x + 4, y - 10, x + 13, y - 2, x + 13, y + 6)
            ctx.curve_to(x + 13, y + 14, x - 13, y + 14, x - 13, y + 6)
            ctx.curve_to(x - 13, y - 2, x - 4, y - 10, x, y - 22)
            ctx.set_source(rad(x - 4, y, 1, 18, [(0, "#E8F7FF", a), (1, "#69B9E8", a)]))
            ctx.fill()
        elif n == "heart":
            for i in range(2):
                ph = (t * 0.6 + i * 0.5) % 1
                k = math.sin(ph * math.pi)
                _heart(ctx, 120 + i * 40 + ph * 20, TOP - 20 - ph * 90, 18 + i * 6, "#FF6B8B", k * a)
        elif n == "gloom":
            for i in range(3):
                x = -60 + i * 60
                ctx.set_line_width(5)
                ctx.set_line_cap(1)
                setc(ctx, "#6A5ACD", 0.6 * a)
                ctx.move_to(x, TOP - 20)
                ctx.line_to(x, TOP - 60 - (i % 2) * 14)
                ctx.stroke()


def _heart(ctx, x, y, s, color, a):
    if a <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s / 20, s / 20)
    ctx.move_to(0, 6)
    ctx.curve_to(-22, -8, -10, -24, 0, -12)
    ctx.curve_to(10, -24, 22, -8, 0, 6)
    ctx.close_path()
    fill(ctx, color, a)
    ctx.restore()


# ---------------------------------------------------------------- 主绘制


def _blend_state(expr, since, prev):
    """返回当前表情的混合参数。"""
    cur = EXPR[expr]
    old = EXPR[prev] if prev in EXPR else cur
    u = clamp(since / BLEND) if since < BLEND else 1.0
    st = {}
    # 眼睛
    ek_new, ek_old = cur["eyes"], old["eyes"]
    if u >= 1 or ek_new == ek_old:
        st["eyes"], st["eye_op"] = ek_new, 1.0
    elif ek_new[0] == ek_old[0] and ek_new[0] in ("rect", "wink"):
        e = ease_out(u)
        st["eyes"] = (ek_new[0], lerp(ek_old[1], ek_new[1], e), lerp(ek_old[2], ek_new[2], e))
        st["eye_op"] = 1.0
    else:
        if u < 0.42:
            st["eyes"], st["eye_op"] = ek_old, 1 - smooth(u / 0.42)
        else:
            st["eyes"], st["eye_op"] = ek_new, ease_back((u - 0.42) / 0.58, 2.2)
    # 眉毛
    bn, bo = BROWS[cur["brows"]], BROWS[old["brows"]]
    e = smooth(u)
    st["brows"] = tuple(lerp(o, n, e) for o, n in zip(bo, bn))
    an = 1.0 if cur["brows"] else 0.0
    ao = 1.0 if old["brows"] else 0.0
    st["brow_a"] = lerp(ao, an, e)
    # 嘴
    if u >= 1 or cur["mouth"] == old["mouth"]:
        st["mouth"], st["mouth_k"] = cur["mouth"], 1.0
    elif u < 0.4:
        st["mouth"], st["mouth_k"] = old["mouth"], 1 - smooth(u / 0.4)
    else:
        st["mouth"], st["mouth_k"] = cur["mouth"], ease_back((u - 0.4) / 0.6, 2.4)
    st["blush"] = lerp(old["blush"], cur["blush"], e)
    return st


def draw_mascot(ctx, x, y, s=1.0, expr="neutral", t=0.0, since=10.0, prev=None,
                look=(0.0, 0.0), squash=0.0, tilt=0.0, walk=None, arm_l=0.0, arm_r=0.0,
                ext_l=0.0, ext_r=0.0, bar=None, fx=None, talk=0.0, flip=False, seed=0.0,
                shadow=1.0, alpha=1.0, blink=True, lift=0.0, ground=None):
    """绘制小橙。

    since/prev: 距上次表情切换的时间与上一个表情（用于平滑过渡）。
    look: 视线方向 (-1..1, -1..1)（屏幕坐标）。walk: 行走相位（圈数）或 None。
    arm_l / arm_r: 侧臂抬起角度；ext_*: 手臂伸长量；bar: 'think' / 'fists' 前置手臂。
    talk: 0..1 说话强度。lift: 离地高度（跳跃，正值向上）。
    """
    if alpha <= 0.003 or s <= 0.001:
        return
    with group_alpha(ctx, alpha):
        _draw(ctx, x, y, s, expr, t, since, prev, look, squash, tilt, walk, arm_l, arm_r,
              ext_l, ext_r, bar, fx, talk, flip, seed, shadow, blink, lift, ground)


def _draw(ctx, x, y, s, expr, t, since, prev, look, squash, tilt, walk, arm_l, arm_r,
          ext_l, ext_r, bar, fx, talk, flip, seed, shadow, blink, lift, ground):
    st = _blend_state(expr, since, prev or expr)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(-s if flip else s, s)
    lx = -look[0] if flip else look[0]
    ly = look[1]

    if shadow > 0:
        k = 1 / (1 + max(lift, 0) / 160)
        soft_shadow(ctx, 0, 3, 178 * k, 19 * k, 0.30 * shadow * k)

    ctx.translate(0, -max(lift, 0))
    ctx.rotate(tilt)

    # 腿 ----------------------------------------------------------------
    bob = 0.0
    lifts, swings = [0.0] * 4, [0.0] * 4
    if walk is not None:
        ph = walk * TAU
        bob = -abs(math.sin(ph)) * 7
        for i in range(4):
            sgn = 1 if i in (0, 2) else -1
            lifts[i] = max(0.0, sgn * math.sin(ph)) * 16
            swings[i] = sgn * math.cos(ph) * 9
    air = clamp(lift / 40)
    for i, lx0 in enumerate(LEGS_X):
        lxx = lx0 + swings[i]
        top = -LEG_H - 10 + bob
        bottom = -lifts[i] - air * 8
        h = bottom - top
        rrect(ctx, lxx - 10, top, 20, h, 2.5)
        ctx.set_source(lin(0, top, 0, bottom, [(0, C_LEG_D), (0.35, C_LEG), (1, "#B8664A")]))
        ctx.fill()
        ctx.rectangle(lxx - 10, top + 12, 5, max(0, h - 13))
        setc(ctx, C_LEG_L, 0.8)
        ctx.fill()

    # 身体组（挤压拉伸以脚底为基准）-------------------------------------
    breathe = 0.013 * math.sin(t * 2.2 + seed * 3)
    sq = squash + breathe
    ctx.translate(0, bob - LEG_H)
    ctx.scale(1 + sq * 0.6, 1 - sq)
    ctx.translate(0, LEG_H)

    _stub(ctx, -1, arm_l, ext_l)
    _stub(ctx, 1, arm_r, ext_r)

    rrect(ctx, -BW / 2 + 1, TOP - 5, BW + 5, BH + 4, 13)
    setc(ctx, C_RIM)
    ctx.fill()
    rrect(ctx, -BW / 2, TOP, BW, BH, 12)
    ctx.set_source(lin(0, TOP, 0, TOP + BH, [(0, C_BODY_T), (0.55, C_BODY_M), (1, C_BODY_B)]))
    ctx.fill_preserve()
    ctx.set_source(rad(-70, TOP + 30, 10, 270, [(0, "#FFFFFF", 0.12), (1, "#FFFFFF", 0)]))
    ctx.fill()
    rrect(ctx, -BW / 2 + 18, TOP + 8, 92, 11, 5.5)
    setc(ctx, C_HL, 0.8)
    ctx.fill()

    # 脸（随视线整体轻微偏移，制造"转头"的视差）------------------------
    fx_off = lx * 14
    fy_off = ly * 8
    ctx.save()
    ctx.translate(fx_off * 0.55, fy_off * 0.5)
    if st["blush"] > 0.01:
        for sx in (-1, 1):
            bx, by = sx * (EYE_X + 10), TOP + 114
            ctx.save()
            ctx.translate(bx, by)
            ctx.scale(1, 0.5)
            ctx.set_source(rad(0, 0, 0, 26, [(0, C_BLUSH, 0.95 * st["blush"]),
                                             (0.7, C_BLUSH, 0.8 * st["blush"]), (1, C_BLUSH, 0)]))
            circle(ctx, 0, 0, 26)
            ctx.fill()
            ctx.restore()

    op = st["eye_op"] * (blink_open(t, seed) if blink else 1.0)
    sac = (noise(t * 1.3, seed + 5) * 1.6, noise(t * 1.1, seed + 8) * 1.2)
    eye_look = (fx_off * 0.55 + sac[0], fy_off * 0.6 + sac[1])
    for sx in (-1, 1):
        _draw_eye(ctx, st["eyes"], sx, sx * EYE_X, EYE_Y, op, eye_look)

    dl, al, dr, ar = st["brows"]
    if st["brow_a"] > 0.01:
        _brow(ctx, -EYE_X + eye_look[0] * 0.5, TOP + 20 + dl, al, st["brow_a"])
        _brow(ctx, EYE_X + eye_look[0] * 0.5, TOP + 20 + dr, ar, st["brow_a"])

    ctx.translate(fx_off * 0.25, 0)
    if talk > 0.01:
        o = clamp(0.5 + 0.5 * noise(t * 9.0, seed + 2) + 0.3 * math.sin(t * 17))
        _mouth(ctx, "talk", t, 1.0, o * talk)
    else:
        _mouth(ctx, st["mouth"], t, st["mouth_k"])
    ctx.restore()

    if bar == "think":
        _front_bar(ctx, -40, TOP + 110, 236, 46, -0.27)
    elif bar == "fists":
        _front_bar(ctx, -150, TOP + 162, 140, 48, 0.78)
        _front_bar(ctx, 150, TOP + 162, 140, 48, -0.78)

    names = DEFAULT_FX.get(expr, ()) if fx is None else fx
    if names:
        fa = clamp(since / 0.3) if fx is None else 1.0
        _fx(ctx, names, t, fa)
    ctx.restore()


# ---------------------------------------------------------------- 时间轴驱动的"演员"


class Puppet:
    """把小橙的动作写成时间轴。所有方法返回 self，便于链式调用。

    例：
        p = Puppet(960, 800, 0.8).expr(0, 'sleep').expr(2.6, 'surprised').hop(2.6)
        p.draw(ctx, t)
    """

    def __init__(self, x, y, s=1.0, expr="neutral", seed=0.0, flip=False):
        self.pos = [(-99.0, (x, y))]
        self.walk_segs = []        # (t0, t1)
        self.sc = [(-99.0, s)]
        self.ex = [(-99.0, expr)]
        self.lk = [(-99.0, (0.0, 0.0))]
        self.tl = [(-99.0, 0.0)]
        self.al = [(-99.0, 0.0)]
        self.ar = [(-99.0, 0.0)]
        self.el = [(-99.0, 0.0)]
        self.er = [(-99.0, 0.0)]
        self.alpha_k = [(-99.0, 1.0)]
        self.hops = []             # (t0, height, dur)
        self.waves = []            # (t0, t1, side)
        self.typing = []           # (t0, t1)
        self.talks = []            # (t0, t1)
        self.shakes = []           # (t0, dur, amp)
        self.strains = []          # (t0, t1, side)
        self.nods = []             # (t0,)
        self.lands = []            # 落地挤压 (t0, 强度)
        self.fx_k = [(-99.0, None)]
        self.bar_k = [(-99.0, None)]
        self.flip_k = [(-99.0, flip)]
        self.seed = seed

    # -- 构建 --------------------------------------------------------------
    def _add(self, lst, t, v, dur, ease):
        cur = kf(t, lst) if lst else v
        lst.append((t, cur))
        lst.append((t + dur, v, ease))
        lst.sort(key=lambda k: k[0])
        return self

    def move(self, t0, t1, x, y, walk=True, ease=ease_io):
        cur = kf(t0, self.pos)
        self.pos += [(t0, cur), (t1, (x, y), ease)]
        self.pos.sort(key=lambda k: k[0])
        if walk:
            self.walk_segs.append((t0, t1))
        return self

    def place(self, t, x, y):
        self.pos.append((t, (x, y), lambda u: 1.0 if u > 0 else 0.0))
        self.pos.sort(key=lambda k: k[0])
        return self

    def scale(self, t, s, dur=0.6, ease=ease_io):
        return self._add(self.sc, t, s, dur, ease)

    def expr(self, t, name):
        self.ex.append((t, name))
        self.ex.sort(key=lambda k: k[0])
        return self

    def look(self, t, lx, ly=0.0, dur=0.28):
        return self._add(self.lk, t, (lx, ly), dur, ease_io)

    def tilt(self, t, ang, dur=0.4):
        return self._add(self.tl, t, ang, dur, ease_io)

    def arm(self, t, side, ang, dur=0.3, ease=ease_back):
        return self._add(self.al if side == "l" else self.ar, t, ang, dur, ease)

    def ext(self, t, side, amount, dur=0.4, ease=ease_out):
        return self._add(self.el if side == "l" else self.er, t, amount, dur, ease)

    def fade(self, t, a, dur=0.4):
        return self._add(self.alpha_k, t, a, dur, ease_io)

    def hop(self, t, height=60, dur=0.48):
        self.hops.append((t, height, dur))
        return self

    def wave(self, t0, t1, side="r"):
        self.waves.append((t0, t1, side))
        return self

    def type(self, t0, t1):
        self.typing.append((t0, t1))
        return self

    def talk(self, t0, t1):
        self.talks.append((t0, t1))
        return self

    def shake(self, t, dur=0.5, amp=0.05):
        self.shakes.append((t, dur, amp))
        return self

    def strain(self, t0, t1, side="r"):
        self.strains.append((t0, t1, side))
        return self

    def nod(self, t):
        self.nods.append(t)
        return self

    def land(self, t, amp=0.16):
        self.lands.append((t, amp))
        return self

    def fx(self, t, names):
        self.fx_k.append((t, names))
        self.fx_k.sort(key=lambda k: k[0])
        return self

    def bar(self, t, kind):
        self.bar_k.append((t, kind))
        self.bar_k.sort(key=lambda k: k[0])
        return self

    def face(self, t, flip):
        self.flip_k.append((t, flip))
        self.flip_k.sort(key=lambda k: k[0])
        return self

    # -- 求值 --------------------------------------------------------------
    @staticmethod
    def _step(lst, t):
        cur, since, prev = lst[0][1], t - lst[0][0], lst[0][1]
        for i, k in enumerate(lst):
            if t >= k[0]:
                prev = lst[i - 1][1] if i > 0 else k[1]
                cur, since = k[1], t - k[0]
        return cur, since, prev

    def state(self, t):
        x, y = kf(t, self.pos)
        s = kf(t, self.sc)
        expr, since, prev = self._step(self.ex, t)
        look = kf(t, self.lk)
        tilt = kf(t, self.tl)
        arm_l, arm_r = kf(t, self.al), kf(t, self.ar)
        ext_l, ext_r = kf(t, self.el), kf(t, self.er)
        squash, lift = 0.0, 0.0
        walk = None
        for (t0, t1) in self.walk_segs:
            if t0 <= t <= t1:
                x0 = kf(t0, self.pos)[0]
                walk = (abs(x - x0) / (95.0 * max(s, 0.2))) % 1.0
                tilt += math.sin(walk * TAU * 2) * 0.012
        for (t0, h, d) in self.hops:
            u = (t - t0) / d
            if -0.3 < u < 0:            # 预备下蹲
                squash += 0.09 * math.sin((u + 0.3) / 0.3 * math.pi / 2)
            elif 0 <= u <= 1:
                lift += math.sin(u * math.pi) * h
                squash += -0.07 * math.sin(u * math.pi) + (0.09 * (1 - u * 4) if u < 0.25 else 0)
            elif 1 < u < 1.9:           # 落地回弹
                v = (u - 1) / 0.9
                squash += 0.12 * math.sin(v * math.pi * 2.2) * math.exp(-v * 3.2)
        if since < 0.6:                 # 表情切换的小弹跳
            squash += 0.05 * math.sin(since * 20) * math.exp(-since * 8)
        for (t0, t1, side) in self.waves:
            if t0 <= t <= t1:
                k = smooth(min((t - t0) / 0.25, (t1 - t) / 0.25, 1.0))
                ang = 1.0 + 0.42 * math.sin((t - t0) * 11)
                if side in ("r", "both"):
                    arm_r = lerp(arm_r, ang, k)
                if side in ("l", "both"):
                    arm_l = lerp(arm_l, 1.0 + 0.42 * math.sin((t - t0) * 11 + 1.3), k)
                tilt += 0.03 * math.sin((t - t0) * 5.5) * k
        for (t0, t1) in self.typing:
            if t0 <= t <= t1:
                k = smooth(min((t - t0) / 0.2, (t1 - t) / 0.2, 1.0))
                arm_l += k * (0.25 + 0.2 * abs(math.sin((t - t0) * 15)))
                arm_r += k * (0.25 + 0.2 * abs(math.sin((t - t0) * 15 + 1.6)))
                squash += 0.012 * math.sin((t - t0) * 30) * k
        for (t0, t1, side) in self.strains:
            if t0 <= t <= t1:
                k = smooth(min((t - t0) / 0.3, (t1 - t) / 0.3, 1.0))
                q = 0.08 * math.sin((t - t0) * 40) * k
                if side in ("r", "both"):
                    arm_r += q
                    ext_r += 6 * math.sin((t - t0) * 33) * k
                if side in ("l", "both"):
                    arm_l += q
                    ext_l += 6 * math.sin((t - t0) * 33) * k
                tilt += (0.05 if side == "r" else -0.05) * k
        for (t0, d, amp) in self.shakes:
            if t0 <= t <= t0 + d:
                u = (t - t0) / d
                tilt += amp * math.sin(u * TAU * 3) * (1 - u)
        for t0 in self.nods:
            u = (t - t0) / 0.5
            if 0 <= u <= 1:
                squash += 0.06 * math.sin(u * TAU) * (1 - u)
        for (t0, amp) in self.lands:
            v = (t - t0) / 0.7
            if 0 <= v <= 1:
                squash += amp * math.sin(v * math.pi * 2.4) * math.exp(-v * 3.5)
        talk = 0.0
        for (t0, t1) in self.talks:
            if t0 <= t <= t1:
                talk = max(talk, smooth(min((t - t0) / 0.12, (t1 - t) / 0.12, 1.0)))
        fx, _, _ = self._step(self.fx_k, t)
        bar, _, _ = self._step(self.bar_k, t)
        flip, _, _ = self._step(self.flip_k, t)
        alpha = kf(t, self.alpha_k)
        return dict(x=x, y=y, s=s, expr=expr, since=since, prev=prev, look=look, tilt=tilt,
                    arm_l=arm_l, arm_r=arm_r, ext_l=ext_l, ext_r=ext_r, squash=squash,
                    lift=lift, walk=walk, talk=talk, fx=fx, bar=bar, flip=flip, alpha=alpha)

    def head(self, t):
        """头顶位置（世界坐标），便于在头上放气泡 / 道具。"""
        st = self.state(t)
        return st["x"], st["y"] - (250 + st["lift"]) * st["s"]

    def draw(self, ctx, t, **override):
        st = self.state(t)
        st.update(override)
        draw_mascot(ctx, st["x"], st["y"], st["s"], st["expr"], t, st["since"], st["prev"],
                    st["look"], st["squash"], st["tilt"], st["walk"], st["arm_l"], st["arm_r"],
                    st["ext_l"], st["ext_r"], st["bar"], st["fx"], st["talk"], st["flip"],
                    self.seed, 1.0, st["alpha"], True, st["lift"])
        return st
