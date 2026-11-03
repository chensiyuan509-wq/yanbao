"""主绘制：把身体、腿、手臂、脸、配件、道具、特效组装起来。

draw_mascot(ctx, x, y, s, **pose) —— (x, y) 为脚底中心（地面），s 为缩放。
pose 的各项含义见 draw_mascot 的文档；通常由 Actor.state(t) 生成，也可以手动传。
"""
import math
import random

from .costume import PALETTES, draw_layers
from .const import (ARM_Y, BH, BLEND, BW, C_BODY_B, C_BODY_M, C_BODY_T, C_HL, C_LEG, C_LEG_D,
                    C_LEG_L, C_OUT, C_RIM, EYE_X, EYE_Y, BROW_Y, LEG_H, LEGS_X, TOP)
from .expressions import BROWS, EXPRESSIONS
from .face import draw_blush, draw_brow, draw_eye, draw_mouth
from .fx import draw_fx
from .gear import GLASSES, HATS, OPAQUE_GLASSES, draw_prop
from .gfx import (TAU, circle, clamp, ease_back, ease_out, fill, lerp, lin, noise, nz, rad, rrect,
                  setc, smooth, soft_shadow, stroke)

# ---------------------------------------------------------------- 自然眨眼

_BLINK_CACHE = {}


_PAL = dict(PALETTES["orange"])


def _blink_times(seed):
    R = random.Random(int(seed * 1000) + 17)
    out, t = [], R.uniform(0.4, 2.5)
    while t < 900:
        out.append(t)
        if R.random() < 0.18:
            out.append(t + 0.26)          # 偶尔连眨两下
        t += R.uniform(2.4, 5.2)
    return out


def blink_open(t, seed=0.0):
    """返回眼睛睁开比例 0..1（确定性的"自然"眨眼）。"""
    bt = _BLINK_CACHE.get(seed)
    if bt is None:
        bt = _BLINK_CACHE[seed] = _blink_times(seed)
    best = 1.0
    lo, hi = 0, len(bt)
    while lo < hi:                         # 二分找到 t 附近
        mid = (lo + hi) // 2
        if bt[mid] < t - 0.3:
            lo = mid + 1
        else:
            hi = mid
    for tb in bt[lo:lo + 4]:
        d = t - tb
        if 0 <= d < 0.17:
            best = min(best, 1 - math.sin(math.pi * d / 0.17) * 0.95)
    return best


# ---------------------------------------------------------------- 表情混合


def _blend_state(expr, since, prev):
    cur = EXPRESSIONS[expr]
    old = EXPRESSIONS.get(prev, cur)
    u = clamp(since / BLEND) if since < BLEND else 1.0
    st = {}
    en, eo = cur["eyes"], old["eyes"]
    if u >= 1 or en == eo:
        st["eyes"], st["eye_op"] = en, 1.0
    elif en[0] == eo[0] and len(en) == len(eo) and len(en) > 1:
        e = ease_out(u)
        st["eyes"] = (en[0],) + tuple(lerp(a, b, e) for a, b in zip(eo[1:], en[1:]))
        st["eye_op"] = 1.0
    elif u < 0.42:
        st["eyes"], st["eye_op"] = eo, 1 - smooth(u / 0.42)
    else:
        st["eyes"], st["eye_op"] = en, ease_back((u - 0.42) / 0.58, 2.2)
    bn, bo = BROWS[cur["brows"]], BROWS[old["brows"]]
    e = smooth(u)
    st["brows"] = tuple(lerp(o, n, e) for o, n in zip(bo, bn))
    st["brow_a"] = lerp(1.0 if old["brows"] else 0.0, 1.0 if cur["brows"] else 0.0, e)
    if u >= 1 or cur["mouth"] == old["mouth"]:
        st["mouth"], st["mouth_k"] = cur["mouth"], 1.0
    elif u < 0.4:
        st["mouth"], st["mouth_k"] = old["mouth"], 1 - smooth(u / 0.4)
    else:
        st["mouth"], st["mouth_k"] = cur["mouth"], ease_back((u - 0.4) / 0.6, 2.4)
    st["blush"] = lerp(old["blush"], cur["blush"], e)
    st["u"] = u
    return st


# ---------------------------------------------------------------- 手臂


def _bar(ctx, cx, cy, length, thick, ang, a=1.0):
    """前置长条手臂。"""
    if length < 4 or a <= 0.01:
        return
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(ang)
    rrect(ctx, -length / 2, -thick / 2, length, thick, 10)
    ctx.set_source(lin(0, -thick / 2, 0, thick / 2, [(0, _PAL["arm"], a), (1, _PAL["b"], a)]))
    ctx.fill_preserve()
    ctx.set_line_width(4)
    setc(ctx, C_OUT, 0.9 * a)
    ctx.stroke()
    rrect(ctx, -length / 2 + 10, -thick / 2 + 5, length * 0.45, 5, 2.5)
    setc(ctx, C_HL, 0.45 * a)
    ctx.fill()
    ctx.restore()


def _bar_from(ctx, x0, y0, ang, length, thick, k=1.0, a=1.0):
    """从肩部 (x0, y0) 沿 ang 方向伸出的手臂，k 控制伸出程度（入场 / 收回）。"""
    L = length * ease_out(k)
    cx, cy = x0 + math.cos(ang) * L / 2, y0 + math.sin(ang) * L / 2
    _bar(ctx, cx, cy, L, thick, ang, a * clamp(k * 2.5))


def stub_geom(side, ang, ext=0.0, length=46):
    """侧臂几何：返回 (根部 x, 根部 y, 旋转角, 手臂总长)。"""
    lift = clamp(ang / 0.9)
    px, py = side * (BW / 2 - 8 + 14 * lift), ARM_Y - 30 * lift
    return px, py, -side * ang, length + 14 * lift + ext


def hand_point(side, ang, ext=0.0):
    """侧臂末端（手）的位置与朝向角（身体局部坐标）。"""
    px, py, rot, L = stub_geom(side, ang, ext)
    d = L + 4
    hx = px + math.cos(rot) * d * side
    hy = py + math.sin(rot) * d * side
    return hx, hy, rot if side > 0 else rot + math.pi


def _stub(ctx, side, ang, ext=0.0):
    px, py, rot, L = stub_geom(side, ang, ext)
    ctx.save()
    ctx.translate(px, py)
    ctx.rotate(rot)
    x0 = -12 if side > 0 else -(L + 8)
    w = L + 20
    rrect(ctx, x0 - 1, -24, w + 2, 47, 8)
    setc(ctx, _PAL["rim"], 0.95)
    ctx.fill()
    rrect(ctx, x0, -21, w, 44, 7)
    ctx.set_source(lin(0, -21, 0, 23, [(0, _PAL["arm"]), (1, _PAL["b"])]))
    ctx.fill()
    ctx.restore()


def _front_pose(ctx, name, k, t, clap=0.0, over=0.0):
    """前置手臂姿势。k 为入场程度 0..1；over 为"举过头顶"时额外抬高的像素（戴帽子时）。"""
    if k <= 0.01:
        return
    if name == "think":          # 手托下巴（素材图 think）
        _bar_from(ctx, -154, TOP + 141, -0.27, 236, 46, k)
    elif name == "fists":        # 双拳举起（素材图 determined）
        _bar_from(ctx, -101, TOP + 211, -2.356, 140, 48, k)
        _bar_from(ctx, 101, TOP + 211, -0.785, 140, 48, k)
    elif name == "cover":        # 捂眼 / 扶额
        _bar_from(ctx, -150, EYE_Y + 14, -0.06, 300, 50, k)
    elif name == "cross":        # 抱臂
        _bar_from(ctx, -150, TOP + 222, -0.30, 250, 44, k)
        _bar_from(ctx, 150, TOP + 222, math.pi + 0.30, 250, 44, k)
    elif name == "hold":         # 双手在身前捧东西
        _bar_from(ctx, -152, HOLD_Y - 8, 0.12, 96, 42, k)
        _bar_from(ctx, 152, HOLD_Y - 8, math.pi - 0.12, 96, 42, k)
    elif name == "carry":        # 举过头顶
        _bar_from(ctx, -120, TOP + 30, -1.75, 150 + over, 42, k)
        _bar_from(ctx, 120, TOP + 30, -1.39, 150 + over, 42, k)
    elif name == "clap":         # 拍手（在身前下方）
        g = 34 * (1 - abs(math.sin(clap * math.pi)))
        _bar_from(ctx, -150, TOP + 190, -0.16, 150 - g, 44, k)
        _bar_from(ctx, 150, TOP + 190, math.pi + 0.16, 150 - g, 44, k)
    elif name == "type":         # 敲键盘
        j = 4 * math.sin(t * 26)
        _bar_from(ctx, -150, TOP + 176, 0.22, 110, 40, k)
        _bar_from(ctx, 150, TOP + 176 + j, math.pi - 0.22, 110, 40, k)
    elif name == "point_up":     # 右手指向天上
        _bar_from(ctx, 130, TOP + 120, -1.05, 170, 42, k)
    elif name == "salute":       # 手搭凉棚眺望（手在额头上）
        _bar_from(ctx, 160, TOP + 60, -2.75, 150, 40, k)
    elif name == "chin":         # 托腮（单手，更放松）
        _bar_from(ctx, 175, TOP + 215, -2.26, 112, 44, k)


HOLD_Y = TOP + 176            # 身前捧东西的高度（嘴巴下方）

FRONT_POSES = ("think", "fists", "cover", "cross", "hold", "carry", "clap", "type", "point_up",
               "salute", "chin")


# ---------------------------------------------------------------- 主绘制


def draw_mascot(ctx, x, y, s=1.0, expr="neutral", t=0.0, since=10.0, prev=None, look=(0.0, 0.0),
                squash=0.0, tilt=0.0, walk=None, stride=1.0, arm_l=0.0, arm_r=0.0, ext_l=0.0,
                ext_r=0.0, front=None, clap=0.0, fx=None, fx_a=1.0, talk=0.0, talk_smile=0.0,
                flip=False, spin=0.0, sit=0.0, lift=0.0, shadow=1.0, alpha=1.0, blink=True,
                eye_open=1.0, seed=0.0, hat=None, hat_dy=0.0, hat_rot=0.0, glasses=None, prop=None,
                prop_at="front", prop_k=1.0, prop_rot=0.0, dust=0.0, brow_lift=0.0, costume=None, palette=None,
                **_):
    """绘制角色。

    expr / since / prev：当前表情、距上次切换的秒数、上一个表情（用于平滑过渡）。
    look：视线 (-1..1, -1..1)，脸会随之轻微平移制造"转头"。
    squash：挤压（正值压扁）。tilt：以脚底为轴倾斜（弧度）。lift：离地高度。
    walk：行走相位（圈数，None 表示不走）；stride：步幅倍数（跑步约 1.8）。
    arm_l / arm_r：侧臂抬起角度；ext_l / ext_r：侧臂伸长像素。
    front：前置手臂姿势，字符串或 {姿势名: 入场程度}（见 FRONT_POSES）；clap 为拍手相位。
    fx：特效名元组（None 表示使用表情默认特效）。talk：说话张口度 0..1。
    flip：左右镜像；spin：绕竖轴旋转角（转身 / 转圈，背面不画脸）；sit：坐下程度 0..1。
    hat / glasses：配件名；prop：道具（见 gear.draw_prop）；prop_at：'front' / 'over' / 'l' / 'r'。
    dust：跑动扬尘强度。eye_open：额外的睁眼系数（强制眨眼用）。brow_lift：眉毛额外上扬像素。
    """
    if alpha <= 0.003 or s <= 0.001:
        return
    if alpha < 0.999:
        ctx.push_group()
    try:
        _draw(ctx, x, y, s, expr, t, since, prev, look, squash, tilt, walk, stride, arm_l, arm_r, ext_l,
              ext_r, front, clap, fx, fx_a, talk, talk_smile, flip, spin, sit, lift, shadow, blink,
              eye_open, seed, hat, hat_dy, hat_rot, glasses, prop, prop_at, prop_k, prop_rot, dust,
              brow_lift, costume, palette)
    finally:
        if alpha < 0.999:
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(clamp(alpha))


def _draw(ctx, x, y, s, expr, t, since, prev, look, squash, tilt, walk, stride, arm_l, arm_r, ext_l,
          ext_r, front, clap, fx, fx_a, talk, talk_smile, flip, spin, sit, lift, shadow, blink,
          eye_open, seed, hat, hat_dy, hat_rot, glasses, prop, prop_at, prop_k, prop_rot, dust,
          brow_lift, costume=None, palette=None):
    _PAL.clear()
    _PAL.update(PALETTES.get(palette or "orange", PALETTES["orange"]))
    if expr not in EXPRESSIONS:
        expr = "neutral"
    st = _blend_state(expr, since, prev if prev in EXPRESSIONS else expr)
    cs = math.cos(spin)
    sx_spin = cs if abs(cs) > 0.12 else (0.12 if cs >= 0 else -0.12)
    show_face = cs > 0.0
    mirror = -1 if flip else 1
    lx = look[0] * mirror
    ly = look[1]

    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # 地面：阴影 + 扬尘 ---------------------------------------------------
    if shadow > 0:
        k = 1 / (1 + max(lift, 0) / 160)
        w = 178 * (0.55 + 0.45 * abs(sx_spin))
        soft_shadow(ctx, 0, 3, w * k, 19 * k, 0.30 * shadow * k)
    if dust > 0.01:
        for i in range(5):
            ph = (t * 2.4 + i / 5) % 1
            dx = -mirror * (60 + ph * 120) + (i - 2) * 22
            r = 10 + ph * 26
            circle(ctx, dx, -6 - ph * 22, r)
            fill(ctx, "#E9D8C8", 0.45 * dust * (1 - ph))

    ctx.translate(0, -max(lift, 0))
    ctx.rotate(tilt)
    ctx.scale(nz(sx_spin * mirror), 1)

    # 腿 ----------------------------------------------------------------
    bob = 0.0
    lifts, swings = [0.0] * 4, [0.0] * 4
    if walk is not None:
        ph = walk * TAU
        bob = -abs(math.sin(ph)) * 7 * stride
        for i in range(4):
            sg = 1 if i in (0, 2) else -1
            lifts[i] = max(0.0, sg * math.sin(ph)) * 16 * stride
            swings[i] = sg * math.cos(ph) * 9 * stride
    air = clamp(lift / 40)
    sit_drop = LEG_H * 0.82 * clamp(sit)
    for i, lx0 in enumerate(LEGS_X):
        lxx = lx0 + swings[i] + (lx0 * 0.12 * sit)
        top = -LEG_H - 10 + bob + sit_drop
        bottom = -lifts[i] - air * 8
        if sit > 0:
            bottom = max(bottom, top + 6)
        h = bottom - top
        if h > 1:
            rrect(ctx, lxx - 10, top, 20, h, 2.5)
            ctx.set_source(lin(0, top, 0, bottom, [(0, C_LEG_D), (0.35, _PAL["leg"]), (1, _PAL["b"])]))
            ctx.fill()
            ctx.rectangle(lxx - 10, top + 12, 5, max(0, h - 13))
            setc(ctx, C_LEG_L, 0.8)
            ctx.fill()

    # 身体组（挤压拉伸以身体底边为基准）---------------------------------
    breathe = 0.013 * math.sin(t * 2.2 + seed * 3)
    sq = squash + breathe
    ctx.translate(0, bob + sit_drop - LEG_H)
    ctx.scale(1 + sq * 0.6, 1 - sq)
    ctx.translate(0, LEG_H)

    names = EXPRESSIONS[expr].get("fx") if fx is None else fx
    fa = (clamp(since / 0.3) if fx is None else 1.0) * fx_a
    if names:
        draw_fx(ctx, names, t, fa, behind=True)

    _stub(ctx, -1, arm_l, ext_l)
    _stub(ctx, 1, arm_r, ext_r)

    rrect(ctx, -BW / 2 + 1, TOP - 5, BW + 5, BH + 4, 13)
    setc(ctx, _PAL["rim"])
    ctx.fill()
    rrect(ctx, -BW / 2, TOP, BW, BH, 12)
    ctx.set_source(lin(0, TOP, 0, TOP + BH, [(0, _PAL["t"]), (0.55, _PAL["m"]), (1, _PAL["b"])]))
    ctx.fill_preserve()
    ctx.set_source(rad(-70, TOP + 30, 10, 270, [(0, "#FFFFFF", 0.12), (1, "#FFFFFF", 0)]))
    ctx.fill()
    rrect(ctx, -BW / 2 + 18, TOP + 8, 92, 11, 5.5)
    setc(ctx, C_HL, 0.8)
    ctx.fill()
    if costume and show_face:
        draw_layers(ctx, costume, t, 1.0, "under")

    # 前置手臂姿势（解析）
    poses = {}
    if isinstance(front, dict):
        poses = {k: v for k, v in front.items() if v > 0.01}
    elif isinstance(front, str):
        poses = {front: 1.0}

    # 脸 ----------------------------------------------------------------
    fx_off, fy_off = lx * 14, ly * 8
    if show_face:
        ctx.save()
        ctx.translate(fx_off * 0.55, fy_off * 0.5)
        draw_blush(ctx, st["blush"])
        op = st["eye_op"] * eye_open * (blink_open(t, seed) if blink else 1.0)
        sac = (noise(t * 1.3, seed + 5) * 1.6, noise(t * 1.1, seed + 8) * 1.2)
        ex, ey = fx_off * 0.55 + sac[0], fy_off * 0.6 + sac[1]
        if glasses not in OPAQUE_GLASSES:
            for sd in (-1, 1):
                draw_eye(ctx, st["eyes"], sd * mirror, sd * EYE_X + ex, EYE_Y + ey, op, t)
        dl, al, dr, ar = st["brows"]
        if st["brow_a"] > 0.01:
            draw_brow(ctx, -EYE_X + ex * 0.5, BROW_Y + dl - brow_lift, al, st["brow_a"])
            draw_brow(ctx, EYE_X + ex * 0.5, BROW_Y + dr - brow_lift, ar, st["brow_a"])
        ctx.translate(fx_off * 0.25, 0)
        if talk > 0.01 and "cover" not in poses:
            draw_mouth(ctx, "talk", t, 1.0, clamp(talk), talk_smile)
        else:
            draw_mouth(ctx, st["mouth"], t, st["mouth_k"])
        ctx.restore()
        if glasses in GLASSES:
            GLASSES[glasses](ctx, t, 1.0, (fx_off * 0.55, fy_off * 0.5))

    # 帽子（有惯性晃动）-------------------------------------------------
    if hat in HATS:
        ctx.save()
        ctx.translate(fx_off * 0.3, hat_dy)
        ctx.translate(0, TOP)
        ctx.rotate(hat_rot)
        ctx.translate(0, -TOP)
        HATS[hat](ctx, t, 1.0)
        ctx.restore()

    if costume:
        draw_layers(ctx, costume, t, 1.0, "over")

    # 道具 + 前置手臂 -----------------------------------------------------
    if prop is not None and prop_k > 0.01:
        pk = ease_back(prop_k, 1.6) if prop_k < 1 else 1.0
        if prop_at in ("l", "r"):
            sd = -1 if prop_at == "l" else 1
            hx, hy, rot = hand_point(sd, arm_l if sd < 0 else arm_r, ext_l if sd < 0 else ext_r)
            ctx.save()
            ctx.translate(hx, hy)
            ctx.rotate(prop_rot)
            ctx.scale(pk, pk)
            draw_prop(ctx, prop, t)
            ctx.restore()
        elif prop_at == "over":
            ctx.save()
            ctx.translate(0, TOP - 110 - (75 if hat else 0))
            ctx.rotate(prop_rot)
            ctx.scale(pk, pk)
            draw_prop(ctx, prop, t)
            ctx.restore()
        else:
            dy = prop[1].get("dy", 0) if isinstance(prop, tuple) and len(prop) > 1 else 0
            ctx.save()
            ctx.translate(0, HOLD_Y + dy)
            ctx.rotate(prop_rot)
            ctx.scale(pk, pk)
            draw_prop(ctx, prop, t)
            ctx.restore()

    if not poses and show_face:
        dflt = EXPRESSIONS[expr].get("front")
        if dflt:
            poses = {dflt: clamp(since / 0.22) if since < 0.22 else 1.0}
    for name, k in poses.items():
        _front_pose(ctx, name, k, t, clap, 75 if hat else 0)

    if names:
        draw_fx(ctx, names, t, fa, behind=False)
    ctx.restore()
