"""电影质感工具：胶片颗粒、遮幅、调色、光束、尘埃、火焰、月相、山脊、云雾、人物剪影、
第一视角（Claude 的手臂入画、眨眼、望远镜视野）、羊皮纸纹理、字距标题。

所有函数都在 1920×1080 的设计坐标里绘制（颗粒除外，它直接作用在输出像素上）。
"""
import math

import cairo
import numpy as np

from .core import (TAU, H, W, circle, clamp, ease_io, ease_out, ellipse, fbm, font, glow, hexc, lerp,
                   lin, mix, noise, poly, rad, rng, rrect, setc, smooth, star4, styled, text)

# ---------------------------------------------------------------- 胶片颗粒（像素空间）

_GRAIN = {}


def _grain_frames(pw, ph, n=6):
    key = (pw, ph)
    if key in _GRAIN:
        return _GRAIN[key]
    out = []
    r = np.random.default_rng(7)
    for i in range(n):
        g = np.clip(r.normal(128, 46, (ph, pw)), 0, 255).astype(np.uint8)
        arr = np.empty((ph, pw, 4), dtype=np.uint8)
        arr[..., 0] = g
        arr[..., 1] = g
        arr[..., 2] = g
        arr[..., 3] = 255
        s = cairo.ImageSurface.create_for_data(bytearray(arr.tobytes()), cairo.FORMAT_ARGB32, pw, ph, pw * 4)
        out.append(s)
    _GRAIN[key] = out
    return out


def apply_grain(ctx, pw, ph, T, amount=0.09):
    """叠加胶片颗粒（overlay 混合），每帧换一张并随机偏移。"""
    if amount <= 0:
        return
    frames = _grain_frames(pw, ph)
    f = int(T * 30)
    s = frames[f % len(frames)]
    r = rng(f * 7 + 3)
    ox, oy = -r.randint(0, 40), -r.randint(0, 40)
    ctx.save()
    ctx.identity_matrix()
    ctx.set_operator(cairo.OPERATOR_OVERLAY)
    pat = cairo.SurfacePattern(s)
    pat.set_extend(cairo.EXTEND_REPEAT)
    pat.set_filter(cairo.FILTER_NEAREST)
    m = cairo.Matrix()
    m.translate(-ox, -oy)
    pat.set_matrix(m)
    ctx.set_source(pat)
    ctx.paint_with_alpha(amount)
    ctx.restore()


def letterbox(ctx, lb, a=1.0):
    ctx.save()
    ctx.set_source_rgba(0, 0, 0, a)
    ctx.rectangle(-200, -200, W + 400, lb + 200)
    ctx.rectangle(-200, H - lb, W + 400, lb + 200)
    ctx.fill()
    ctx.restore()


def grade(ctx, color, a=0.3, op=cairo.OPERATOR_SOFT_LIGHT):
    """整体调色：用柔光 / 叠加 / 正片叠底铺一层颜色。"""
    if a <= 0.003:
        return
    ctx.save()
    ctx.set_operator(op)
    r, g, b = hexc(color)
    ctx.set_source_rgba(r, g, b, a)
    ctx.paint()
    ctx.restore()


def vignette(ctx, a=0.55, inner=0.38, color="#000000", cx=None, cy=None):
    cx = W / 2 if cx is None else cx
    cy = H / 2 if cy is None else cy
    g = rad(cx, cy, H * inner, H * 1.05, [(0, color, 0), (0.6, color, a * 0.55), (1, color, a)])
    ctx.set_source(g)
    ctx.paint()


def fade_black(ctx, a):
    if a > 0.002:
        ctx.set_source_rgba(0, 0, 0, clamp(a))
        ctx.paint()


def flicker(t, seed=0.0, amt=0.12, speed=7.0):
    """火光 / 烛光的亮度闪烁（约 1-amt .. 1）。"""
    return 1 - amt * 0.5 + amt * 0.5 * fbm(t * speed, seed)


# ---------------------------------------------------------------- 文字


def tracked(ctx, s, x, y, size, color, a=1.0, weight="serif_r", track=0.1, align="c"):
    """字距可调的单行文字。"""
    if a <= 0.003 or not s:
        return 0.0
    font(ctx, size, weight)
    adv = [ctx.text_extents(ch).x_advance for ch in s]
    tw = sum(adv) + track * size * (len(s) - 1)
    cx = x - tw / 2 if align == "c" else (x - tw if align == "r" else x)
    for ch, w in zip(s, adv):
        text(ctx, ch, cx, y, size, color, a, weight, "l")
        cx += w + track * size
    return tw


def type_on(s, t, t0, cps=18):
    """打字机效果：返回 t 时刻应显示的前缀。"""
    n = int(max(0.0, t - t0) * cps)
    return s[:n]


# ---------------------------------------------------------------- 天空 / 地形 / 大气


def sky(ctx, stops, y0=0, y1=H):
    ctx.set_source(lin(0, y0, 0, y1, stops))
    ctx.paint()


def sun(ctx, x, y, r, a=1.0, color="#FFE6B0", halo="#FFB766", halo_r=None):
    if a <= 0.003:
        return
    halo_r = halo_r or r * 9
    glow(ctx, x, y, halo_r, halo, 0.55 * a)
    glow(ctx, x, y, r * 3.2, color, 0.7 * a)
    circle(ctx, x, y, r)
    ctx.set_source(rad(x, y, 0, r, [(0, "#FFFFFF", a), (0.7, color, a), (1, mix(color, halo, 0.5), a)]))
    ctx.fill()


def moon(ctx, x, y, r, phase=0.5, a=1.0, lit="#F2EAD6", dark="#20263A", dark_a=0.55, glow_a=0.25,
         craters=True):
    """月相：phase 0 新月 → 0.25 上弦（右半亮）→ 0.5 满月 → 0.75 下弦 → 1 新月。"""
    if a <= 0.003:
        return
    phase %= 1.0
    lit_frac = 0.5 - 0.5 * math.cos(TAU * phase)
    if glow_a > 0:
        glow(ctx, x, y, r * 3.0, lit, glow_a * a * (0.3 + 0.7 * lit_frac))
    circle(ctx, x, y, r)
    setc(ctx, dark, dark_a * a)
    ctx.fill()
    ctx.save()
    ctx.translate(x, y)
    if phase > 0.5:
        ctx.scale(-1, 1)
        p = 1 - phase
    else:
        p = phase
    rx = r * math.cos(TAU * p)
    ctx.new_path()
    ctx.arc(0, 0, r, -math.pi / 2, math.pi / 2)
    n = 40
    for i in range(n + 1):
        th = math.pi / 2 - math.pi * i / n
        ctx.line_to(rx * math.cos(th), r * math.sin(th))
    ctx.close_path()
    ctx.set_source(rad(-r * 0.2, -r * 0.25, 0, r * 1.2, [(0, "#FFFFFF", a), (0.5, lit, a), (1, mix(lit, "#B9AE98", 0.5), a)]))
    if craters:
        ctx.save()
        ctx.clip_preserve()
        ctx.fill()
        for (cx_, cy_, cr) in ((-0.3, -0.25, 0.18), (0.25, 0.1, 0.24), (-0.1, 0.4, 0.13), (0.35, -0.4, 0.1),
                               (-0.45, 0.15, 0.1)):
            circle(ctx, cx_ * r, cy_ * r, cr * r)
            setc(ctx, "#9C927F", 0.28 * a)
            ctx.fill()
        ctx.restore()
    else:
        ctx.fill()
    ctx.restore()


def ridge(ctx, x0, x1, base_y, amp, freq, seed, color, a=1.0, step=10, bottom=None, sharp=0.0,
          grad=None):
    """山脊剪影：fbm 噪声生成轮廓并填充到底部。grad=(上色, 下色) 时用竖向渐变。"""
    if a <= 0.003:
        return
    bottom = H + 200 if bottom is None else bottom
    ctx.move_to(x0, bottom)
    x = x0
    while x <= x1 + step:
        v = fbm(x * freq, seed)
        if sharp:
            v = (1 - abs(v)) * sharp + v * (1 - sharp)
        ctx.line_to(x, base_y - (v * 0.5 + 0.5) * amp)
        x += step
    ctx.line_to(x1 + step, bottom)
    ctx.close_path()
    if grad:
        ctx.set_source(lin(0, base_y - amp, 0, base_y + amp * 0.6, [(0, grad[0], a), (1, grad[1], a)]))
        ctx.fill()
    else:
        setc(ctx, color, a)
        ctx.fill()


def fog(ctx, y, h, color, a=0.4):
    if a <= 0.003:
        return
    ctx.set_source(lin(0, y - h, 0, y + h, [(0, color, 0), (0.5, color, a), (1, color, 0)]))
    ctx.rectangle(-400, y - h, W + 800, 2 * h)
    ctx.fill()


def cloud(ctx, x, y, w, h, color, a=0.5, seed=1):
    """柔软的云团（几层径向渐变叠加）。"""
    if a <= 0.003:
        return
    R = rng(seed)
    for i in range(6):
        cx = x + R.uniform(-0.45, 0.45) * w
        cy = y + R.uniform(-0.25, 0.2) * h
        rr = R.uniform(0.35, 0.6) * w
        ctx.save()
        ctx.translate(cx, cy)
        ctx.scale(1, h / w * 1.4)
        ctx.set_source(rad(0, 0, 0, rr, [(0, color, a * 0.5), (0.6, color, a * 0.22), (1, color, 0)]))
        circle(ctx, 0, 0, rr)
        ctx.fill()
        ctx.restore()


def beams(ctx, ox, oy, ang, spread, length, n, color, a=0.2, t=0.0, seed=1, width=0.05):
    """放射光束（从光源 (ox, oy) 朝 ang 方向扇形展开），带缓慢闪动。"""
    if a <= 0.003:
        return
    R = rng(seed)
    for i in range(n):
        th = ang + (i / max(n - 1, 1) - 0.5) * spread + R.uniform(-0.02, 0.02)
        w = width * R.uniform(0.5, 1.4)
        k = 0.55 + 0.45 * (0.5 + 0.5 * math.sin(t * R.uniform(0.3, 0.8) + R.random() * TAU))
        L = length * R.uniform(0.7, 1.1)
        ctx.move_to(ox, oy)
        ctx.line_to(ox + math.cos(th - w) * L, oy + math.sin(th - w) * L)
        ctx.line_to(ox + math.cos(th + w) * L, oy + math.sin(th + w) * L)
        ctx.close_path()
        ctx.set_source(rad(ox, oy, 0, L, [(0, color, a * k), (0.5, color, a * k * 0.35), (1, color, 0)]))
        ctx.fill()


def shaft(ctx, x0, y0, x1, y1, w0, w1, color, a=0.2):
    """一束平行光（从窗口斜射进来的光柱）。"""
    if a <= 0.003:
        return
    ang = math.atan2(y1 - y0, x1 - x0) + math.pi / 2
    dx0, dy0 = math.cos(ang) * w0 / 2, math.sin(ang) * w0 / 2
    dx1, dy1 = math.cos(ang) * w1 / 2, math.sin(ang) * w1 / 2
    poly(ctx, [(x0 - dx0, y0 - dy0), (x0 + dx0, y0 + dy0), (x1 + dx1, y1 + dy1), (x1 - dx1, y1 - dy1)])
    ctx.set_source(lin(x0, y0, x1, y1, [(0, color, a), (0.6, color, a * 0.45), (1, color, 0)]))
    ctx.fill()


def dust(ctx, t, n, seed, area=(0, 0, W, H), color="#FFE9C4", a=0.5, size=(1.2, 3.4), speed=8.0):
    """飘浮的微尘（光柱里的灰尘）。"""
    if a <= 0.003:
        return
    R = rng(seed)
    x0, y0, w, h = area
    for i in range(n):
        px, py = R.random(), R.random()
        s = R.uniform(*size)
        ph = R.random() * 100
        sp = R.uniform(0.3, 1.0) * speed
        x = x0 + (px * w + fbm(t * 0.1 + ph, seed) * 60 + t * sp * 0.6) % w
        y = y0 + (py * h + fbm(t * 0.08 + ph, seed + 3) * 50 - t * sp * 0.3) % h
        tw = 0.4 + 0.6 * (0.5 + 0.5 * math.sin(t * R.uniform(0.6, 2.0) + ph))
        setc(ctx, color, a * tw)
        circle(ctx, x, y, s)
        ctx.fill()


def embers(ctx, t, x, y, n, seed, spread=60, height=420, color="#FFB04A", a=1.0, size=3.5, speed=0.55):
    """火星：从 (x, y) 往上飘，忽左忽右，逐渐熄灭。"""
    if a <= 0.003:
        return
    R = rng(seed)
    for i in range(n):
        off = R.random()
        sp = R.uniform(0.6, 1.3) * speed
        u = (t * sp + off) % 1.0
        ph = R.random() * 50
        ex = x + R.uniform(-1, 1) * spread * 0.5 + fbm(u * 3 + ph, seed) * spread * (0.4 + u)
        ey = y - u * height * R.uniform(0.6, 1.1)
        al = a * (1 - u) ** 1.4 * clamp(u * 8)
        s = size * R.uniform(0.5, 1.2) * (1 - u * 0.6)
        glow(ctx, ex, ey, s * 4, color, al * 0.5)
        setc(ctx, "#FFE7A8", al)
        circle(ctx, ex, ey, s * 0.6)
        ctx.fill()


def fire(ctx, x, y, s, t, a=1.0, seed=0.0, glow_a=1.0):
    """篝火：(x, y) 为火堆底部中心，s 为大小（约等于火焰高度）。"""
    if a <= 0.003:
        return
    glow(ctx, x, y - s * 0.35, s * 3.2, "#FF8A2A", 0.35 * glow_a * a * flicker(t, seed))
    glow(ctx, x, y - s * 0.3, s * 1.3, "#FFB347", 0.55 * glow_a * a * flicker(t, seed + 1))
    layers = (("#E8451A", 1.0, 0.85), ("#FF8C1F", 0.78, 0.9), ("#FFC94A", 0.55, 0.95), ("#FFF4C8", 0.3, 1.0))
    R = rng(int(seed * 10) + 5)
    tongues = [(R.uniform(-0.32, 0.32), R.uniform(0.6, 1.0), R.random() * 20) for _ in range(7)]
    for col, k, al in layers:
        for (dx, hk, ph) in tongues:
            hh = s * hk * k * (0.75 + 0.35 * (0.5 + 0.5 * noise(t * 3.1 + ph, seed)))
            sway = noise(t * 2.2 + ph * 1.7, seed + 2) * 0.28 * hh
            bw = s * 0.2 * k * (0.8 + 0.4 * hk)
            bx = x + dx * s * k
            ctx.move_to(bx - bw, y)
            ctx.curve_to(bx - bw * 1.1, y - hh * 0.45, bx + sway * 0.6 - bw * 0.3, y - hh * 0.75, bx + sway, y - hh)
            ctx.curve_to(bx + sway * 0.6 + bw * 0.3, y - hh * 0.75, bx + bw * 1.1, y - hh * 0.45, bx + bw, y)
            ctx.close_path()
        setc(ctx, col, a * al)
        ctx.fill()


def logs(ctx, x, y, s, a=1.0):
    """篝火下的木柴与石圈。"""
    for ang, L in ((-0.25, 1.0), (0.22, 0.95), (0.05, 0.8)):
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(ang)
        rrect(ctx, -s * 0.6 * L, -s * 0.07, s * 1.2 * L, s * 0.14, s * 0.07)
        setc(ctx, "#3A2416", a)
        ctx.fill()
        ctx.restore()
    for i in range(9):
        th = math.pi * (i / 8)
        ellipse(ctx, x + math.cos(th) * s * 0.75, y + 6 + math.sin(th) * s * 0.12 * 0 + 4, s * 0.12, s * 0.07)
        setc(ctx, "#2A221D", a)
        ctx.fill()


def smoke_puffs(ctx, t, x, y, n, seed, color="#D8D2CA", a=0.4, rise=300, size=60, drift=80, speed=0.25):
    """烟 / 蒸汽：一团团往上飘、变大、变淡。"""
    if a <= 0.003:
        return
    R = rng(seed)
    for i in range(n):
        off = R.random()
        u = (t * speed * R.uniform(0.7, 1.3) + off) % 1.0
        px = x + fbm(u * 2 + i, seed) * drift + u * drift * 0.6
        py = y - u * rise
        r = size * (0.4 + u * 1.6) * R.uniform(0.8, 1.2)
        al = a * math.sin(u * math.pi) ** 1.2
        ctx.set_source(rad(px, py, 0, r, [(0, color, al * 0.6), (0.6, color, al * 0.25), (1, color, 0)]))
        circle(ctx, px, py, r)
        ctx.fill()


# ---------------------------------------------------------------- 人物剪影


def _limb(ctx, pts, w):
    ctx.set_line_width(w)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.stroke()


def _seg(p, ang, L):
    """从 p 出发，ang=0 朝下、正值朝前（+x）转。"""
    return (p[0] + math.sin(ang) * L, p[1] + math.cos(ang) * L)


def _human_path(ctx, u, pose, t, phase, robe, hat, arms, lean):
    """在局部坐标（脚底为原点、朝 +x）里画一个人形，返回关键点。"""
    walk = pose in ("walk", "run")
    sw = math.sin(phase * TAU) if walk else 0.0
    if pose == "sit":                    # 盘腿坐地
        hip = (0, -12 * u)
    elif pose == "sit_chair":
        hip = (0, -27 * u)
    elif pose in ("kneel", "crouch"):
        hip = (0, -30 * u)
    else:
        hip = (0, -50 * u + (abs(sw) * 1.5 * u if walk else 0))
    tl = lean + (0.08 if pose == "run" else 0.0) + (0.35 if pose == "crouch" else 0.0)
    shoulder = (hip[0] + math.sin(tl) * 31 * u, hip[1] - math.cos(tl) * 31 * u)
    head = (shoulder[0] + math.sin(tl) * 10 * u, shoulder[1] - math.cos(tl) * 10 * u)
    # 腿
    legs = []
    if pose == "sit":
        legs = [[(-3 * u, hip[1]), (15 * u, -7 * u), (-2 * u, -2 * u)], [(3 * u, hip[1]), (-13 * u, -6 * u), (4 * u, -2 * u)]]
    elif pose == "sit_chair":
        legs = [[(-2 * u, hip[1]), (15 * u, hip[1] + 1 * u), (15 * u, 0)], [(2 * u, hip[1]), (17 * u, hip[1]), (18 * u, 0)]]
    elif pose == "kneel":
        legs = [[(-2 * u, hip[1]), (-2 * u, -4 * u), (-20 * u, -2 * u)], [(3 * u, hip[1]), (16 * u, -26 * u), (16 * u, 0)]]
    elif pose == "crouch":
        legs = [[(-3 * u, hip[1]), (12 * u, -18 * u), (2 * u, 0)], [(3 * u, hip[1]), (18 * u, -14 * u), (12 * u, 0)]]
    else:
        amp = 0.42 if pose == "run" else (0.3 if walk else 0.0)
        for side, sg in ((-1, 1), (1, -1)):
            a1 = sg * sw * amp + (0.06 * side if not walk else 0)
            knee = _seg((side * 2.5 * u, hip[1]), -a1, 25 * u)
            bend = max(0.0, -sg * sw) * (0.6 if pose == "run" else 0.35)
            foot = _seg(knee, -a1 + bend * 0.2 - bend, 25 * u)
            foot = (foot[0], min(foot[1], 0))
            legs.append([(side * 2.5 * u, hip[1]), knee, foot])
    # 手臂（角度：0 朝下，正值朝前）
    default = {"stand": (0.12, -0.12), "walk": (sw * 0.5, -sw * 0.5), "run": (sw * 0.9 + 0.3, -sw * 0.9 + 0.3),
               "sit": (0.5, 0.3), "sit_chair": (0.7, 0.5), "kneel": (0.8, 0.4), "crouch": (1.0, 0.6),
               "point": (2.6, -0.1), "reach": (1.5, 0.2), "raise": (2.9, -2.9), "write": (1.3, 0.9),
               "hold": (1.1, 0.9), "telescope": (2.0, 1.75)}
    a_back, a_front = arms if arms else default.get(pose, (0.1, -0.1))
    arm_pts = []
    for ang, bend in ((a_back, 0.25), (a_front, 0.35)):
        elbow = _seg(shoulder, ang + tl, 16 * u)
        hand = _seg(elbow, ang + tl + bend, 15 * u)
        arm_pts.append([shoulder, elbow, hand])
    # 画：腿 → 身体 → 手臂 → 头
    if robe:
        sw2 = sw * 2 * u
        poly(ctx, [(shoulder[0] - 9 * u, shoulder[1] + 1 * u), (shoulder[0] + 9 * u, shoulder[1] + 1 * u),
                   (hip[0] + 12 * u, hip[1] + 4 * u),
                   (15 * u + sw2 + (8 * u if pose.startswith("sit") else 0), (0 if not pose.startswith("sit") else -2 * u)),
                   (-15 * u + sw2, 0 if not pose.startswith("sit") else -2 * u)])
        ctx.fill()
        if pose.startswith("sit"):
            for L in legs:
                _limb(ctx, L, 7 * u)
    else:
        for L in legs:
            _limb(ctx, L, 6.5 * u)
        poly(ctx, [(shoulder[0] - 9.5 * u, shoulder[1]), (shoulder[0] + 9.5 * u, shoulder[1]),
                   (hip[0] + 7.5 * u, hip[1] + 2 * u), (hip[0] - 7.5 * u, hip[1] + 2 * u)])
        ctx.set_line_width(5 * u)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.stroke_preserve()
        ctx.fill()
    for A in arm_pts:
        _limb(ctx, A, 5.2 * u)
    circle(ctx, head[0], head[1] - 6 * u, 6.6 * u)
    ctx.fill()
    hx, hy = head[0], head[1] - 6 * u
    if hat == "turban":
        ellipse(ctx, hx, hy - 4.5 * u, 8.2 * u, 5.5 * u)
        ctx.fill()
    elif hat == "cap":                       # 幞头 / 小帽
        rrect(ctx, hx - 6 * u, hy - 11 * u, 12 * u, 7 * u, 2 * u)
        ctx.fill()
    elif hat == "hood":
        poly(ctx, [(hx - 8 * u, hy + 4 * u), (hx - 7 * u, hy - 8 * u), (hx + 1 * u, hy - 11 * u), (hx + 8 * u, hy - 3 * u),
                   (hx + 8 * u, hy + 5 * u)])
        ctx.fill()
    elif hat == "tophat":
        ctx.rectangle(hx - 5.5 * u, hy - 17 * u, 11 * u, 12 * u)
        ctx.rectangle(hx - 9 * u, hy - 6.5 * u, 18 * u, 2.2 * u)
        ctx.fill()
    elif hat == "wig":                       # 17 世纪的长卷发
        ellipse(ctx, hx - 2 * u, hy + 2 * u, 8.5 * u, 10 * u)
        ctx.fill()
    elif hat == "hair":
        ellipse(ctx, hx - 1.5 * u, hy + 1 * u, 7.5 * u, 8 * u)
        ctx.fill()
    elif hat == "bun":                       # 发髻
        circle(ctx, hx - 4 * u, hy - 6 * u, 3.6 * u)
        ctx.fill()
    return dict(head=(hx, hy), hand_b=arm_pts[0][2], hand_f=arm_pts[1][2], shoulder=shoulder, hip=hip)


def human(ctx, x, y, h, pose="stand", t=0.0, color="#120C0A", a=1.0, flip=False, rim=None, rim_a=0.7,
          rim_dx=-3.0, rim_dy=-1.5, phase=0.0, robe=False, hat=None, arms=None, lean=0.0):
    """人物剪影。(x, y) 为脚底中心，h 为身高（像素），默认朝右；返回关键点（世界坐标）。"""
    if a <= 0.003:
        return None
    u = h / 100.0
    pts = None
    grp = a < 0.999
    if grp:
        ctx.push_group()
    for layer in ((rim, rim_dx, rim_dy) if rim else None, (color, 0, 0)):
        if layer is None:
            continue
        col, dx, dy = layer
        ctx.save()
        ctx.translate(x + dx * u / 1.6, y + dy * u / 1.6)
        if flip:
            ctx.scale(-1, 1)
        setc(ctx, col, rim_a if col is rim and rim else 1.0)
        pts = _human_path(ctx, u, pose, t, phase, robe, hat, arms, lean)
        ctx.restore()
    if grp:
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(clamp(a))
    sg = -1 if flip else 1
    return {k: (x + v[0] * sg, y + v[1]) for k, v in pts.items()}


# ---------------------------------------------------------------- 第一视角


ARM_T = "#F59A6E"
ARM_B = "#C6664A"
ARM_OUT = "#8A452F"
ARM_RIM = "#FBE9BB"


def pov_arm(ctx, base, tip, thick=150, a=1.0, light=1.0):
    """Claude 的手臂入画（第一视角）：从画外 base 伸到 tip 的橙色圆角长条。"""
    if a <= 0.003:
        return
    (x0, y0), (x1, y1) = base, tip
    L = math.dist(base, tip)
    ang = math.atan2(y1 - y0, x1 - x0)
    ctx.save()
    ctx.translate(x0, y0)
    ctx.rotate(ang)
    # 投影
    rrect(ctx, 0, -thick / 2 + 16, L + 10, thick, thick * 0.16)
    setc(ctx, "#000000", 0.25 * a)
    ctx.fill()
    rrect(ctx, 0, -thick / 2 - 4, L + 4, thick + 8, thick * 0.17)
    setc(ctx, ARM_RIM, 0.9 * a)
    ctx.fill()
    rrect(ctx, 0, -thick / 2, L, thick, thick * 0.15)
    ctx.set_source(lin(0, -thick / 2, 0, thick / 2, [(0, mix(ARM_T, "#FFFFFF", 0.08 * light), a),
                                                     (0.55, mix(ARM_T, ARM_B, 0.45), a), (1, ARM_B, a)]))
    ctx.fill_preserve()
    ctx.set_line_width(5)
    setc(ctx, ARM_OUT, 0.8 * a)
    ctx.stroke()
    rrect(ctx, L * 0.35, -thick / 2 + 14, L * 0.5, 10, 5)
    setc(ctx, "#FFF1DB", 0.45 * a * light)
    ctx.fill()
    ctx.restore()


def eyelids(ctx, open_k, color="#030202", soft=90):
    """眨眼：open_k=0 闭眼，1 完全睁开。上下眼睑带弧度和柔边。"""
    if open_k >= 0.999:
        return
    k = ease_io(clamp(open_k))
    gap = (H / 2 + 260) * k
    r, g, b = hexc(color)
    for sgn in (-1, 1):
        edge = H / 2 + sgn * gap
        bulge = 160 * (1 - k * 0.5)
        ctx.new_path()
        if sgn < 0:
            ctx.move_to(-50, -50)
            ctx.line_to(W + 50, -50)
            ctx.line_to(W + 50, edge + 60)
            ctx.curve_to(W * 0.7, edge + bulge, W * 0.3, edge + bulge, -50, edge + 60)
        else:
            ctx.move_to(-50, H + 50)
            ctx.line_to(W + 50, H + 50)
            ctx.line_to(W + 50, edge - 60)
            ctx.curve_to(W * 0.7, edge - bulge, W * 0.3, edge - bulge, -50, edge - 60)
        ctx.close_path()
        ctx.set_source_rgba(r, g, b, 1)
        ctx.fill()
        # 柔边
        e2 = edge + sgn * -1 * 0
        gpat = cairo.LinearGradient(0, e2 + (bulge * 0.75 if sgn < 0 else -bulge * 0.75),
                                    0, e2 + (bulge * 0.75 + soft if sgn < 0 else -bulge * 0.75 - soft))
        gpat.add_color_stop_rgba(0, r, g, b, 0.85)
        gpat.add_color_stop_rgba(1, r, g, b, 0)
        ctx.set_source(gpat)
        ctx.rectangle(-50, -50, W + 100, H + 100)
        ctx.fill()


def scope_view(ctx, x, y, r, a=1.0, color="#000000", ring="#7A5A2E"):
    """望远镜 / 显微镜视野：圆形之外全黑，边缘柔和暗角 + 一圈色散。"""
    rr, gg, bb = hexc(color)
    ctx.save()
    ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    ctx.rectangle(-100, -100, W + 200, H + 200)
    circle(ctx, x, y, r)
    ctx.set_source_rgba(rr, gg, bb, a)
    ctx.fill()
    ctx.restore()
    ctx.set_source(rad(x, y, r * 0.55, r, [(0, color, 0), (0.8, color, 0.45 * a), (1, color, a)]))
    circle(ctx, x, y, r)
    ctx.fill()
    ctx.set_line_width(5)
    setc(ctx, ring, 0.4 * a)
    circle(ctx, x, y, r - 3)
    ctx.stroke()
    ctx.set_line_width(2)
    setc(ctx, "#7FB6FF", 0.18 * a)
    circle(ctx, x, y, r - 9)
    ctx.stroke()


# ---------------------------------------------------------------- 羊皮纸纹理

_PARCH = {}


def _value_noise_img(w, h, seed, octaves=((8, 0.5), (16, 0.25), (40, 0.15), (120, 0.1))):
    r = np.random.default_rng(seed)
    out = np.zeros((h, w), dtype=np.float32)
    for cells, amp in octaves:
        gw, gh = cells + 2, max(2, int(cells * h / w) + 2)
        g = r.random((gh, gw)).astype(np.float32)
        xs = np.linspace(0, gw - 1.001, w)
        ys = np.linspace(0, gh - 1.001, h)
        x0 = xs.astype(int)
        y0 = ys.astype(int)
        fx = xs - x0
        fy = ys - y0
        fx = fx * fx * (3 - 2 * fx)
        fy = fy * fy * (3 - 2 * fy)
        a = g[np.ix_(y0, x0)]
        b = g[np.ix_(y0, x0 + 1)]
        c = g[np.ix_(y0 + 1, x0)]
        d = g[np.ix_(y0 + 1, x0 + 1)]
        top = a + (b - a) * fx[None, :]
        bot = c + (d - c) * fx[None, :]
        out += (top + (bot - top) * fy[:, None]) * amp
    return out / sum(a for _, a in octaves)


def texture(kind="parchment", w=1024, h=576):
    """预生成纹理（每个进程一次）：parchment 羊皮纸 / clay 泥板 / stone 石面 / paper 纸。"""
    key = (kind, w, h)
    if key in _PARCH:
        return _PARCH[key]
    base = {"parchment": (0.90, 0.82, 0.66), "clay": (0.72, 0.52, 0.36), "stone": (0.55, 0.52, 0.48),
            "paper": (0.95, 0.91, 0.82)}[kind]
    n = _value_noise_img(w, h, {"parchment": 3, "clay": 5, "stone": 9, "paper": 11}[kind])
    fine = np.random.default_rng(4).normal(0, 1, (h, w)).astype(np.float32)
    v = 0.82 + (n - 0.5) * 0.42 + fine * (0.025 if kind != "stone" else 0.05)
    if kind == "parchment":
        # 污渍
        st = _value_noise_img(w, h, 21, ((5, 1.0),))
        v -= np.clip(st - 0.62, 0, 1) * 0.6
    img = np.stack([np.clip(base[2] * v, 0, 1), np.clip(base[1] * v, 0, 1), np.clip(base[0] * v, 0, 1)], -1)
    arr = np.empty((h, w, 4), dtype=np.uint8)
    arr[..., :3] = (img * 255).astype(np.uint8)
    arr[..., 3] = 255
    s = cairo.ImageSurface.create_for_data(bytearray(arr.tobytes()), cairo.FORMAT_ARGB32, w, h, w * 4)
    _PARCH[key] = s
    return s


def paint_texture(ctx, kind, x, y, w, h, a=1.0, scale=1.0, ox=0.0, oy=0.0, clip_path=None):
    """把纹理铺在矩形 (x, y, w, h) 里（可平移 ox/oy 做视差）。"""
    if a <= 0.003:
        return
    s = texture(kind)
    sw, sh = s.get_width(), s.get_height()
    pat = cairo.SurfacePattern(s)
    pat.set_extend(cairo.EXTEND_REFLECT)
    pat.set_filter(cairo.FILTER_GOOD)
    m = cairo.Matrix()
    k = max(w / sw, h / sh) / scale
    m.scale(1 / k, 1 / k)
    m.translate(-(x + ox), -(y + oy))
    pat.set_matrix(m)
    ctx.save()
    if clip_path:
        clip_path(ctx)
        ctx.clip()
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    ctx.set_source(pat)
    ctx.paint_with_alpha(a)
    ctx.restore()


# ---------------------------------------------------------------- 常用小件


def tablet_wedge(ctx, x, y, s, ang=0.0, color="#4A2E1C", a=1.0):
    """楔形笔画（三角头 + 细尾）。"""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    poly(ctx, [(0, -s * 0.32), (s * 0.42, 0), (0, s * 0.32)])
    setc(ctx, color, a)
    ctx.fill()
    ctx.rectangle(s * 0.3, -s * 0.05, s * 0.9, s * 0.1)
    ctx.fill()
    ctx.restore()


def scroll_roll(ctx, x, y, w, h, a=1.0, color="#E7D6AE", rod="#6B4A2B", open_k=1.0):
    """展开的卷轴：两端木轴，中间纸面。返回纸面矩形。"""
    ww = w * open_k
    rrect(ctx, x - ww / 2, y - h / 2, ww, h, 6)
    setc(ctx, color, a)
    ctx.fill()
    for sx in (-1, 1):
        rrect(ctx, x + sx * ww / 2 - 14, y - h / 2 - 22, 28, h + 44, 12)
        setc(ctx, rod, a)
        ctx.fill()
        rrect(ctx, x + sx * ww / 2 - 18, y - h / 2 - 30, 36, 16, 6)
        rrect(ctx, x + sx * ww / 2 - 18, y + h / 2 + 14, 36, 16, 6)
        setc(ctx, mix(rod, "#000000", 0.3), a)
        ctx.fill()
    return (x - ww / 2, y - h / 2, ww, h)


def star_field(ctx, t, n, seed, area=(0, 0, W, H), a=1.0, size=(0.8, 2.6), color="#FFFFFF", tw=1.0):
    R = rng(seed)
    x0, y0, w, h = area
    for i in range(n):
        x, y = x0 + R.random() * w, y0 + R.random() * h
        s = R.uniform(*size)
        ph = R.random() * TAU
        k = 1 - tw * 0.5 + tw * 0.5 * math.sin(t * R.uniform(0.5, 2.0) + ph)
        setc(ctx, color, a * k * R.uniform(0.4, 1.0))
        circle(ctx, x, y, s)
        ctx.fill()
        if s > 2.2:
            star4(ctx, x, y, s * 3.5 * k, color, a * 0.4 * k)
