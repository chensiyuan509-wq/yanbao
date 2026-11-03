"""场景道具：芯片、晶圆、内存、服务器、光纤、光模块、工厂、建筑、城堡、法槌、价签、奖牌……

全部用代码绘制的通用风格图形（不使用任何商标图片）。约定 (x, y) 为中心，除非另有说明。
"""
import math

import cairo

from .core import (TAU, box_shadow, circle, clamp, ease_out, ellipse, fill, glow, lerp, lin, line,
                   mix, poly, rad, rng, rrect, setc, star4, star5, stroke_pts, text, text_w)

# ---------------------------------------------------------------- 背景


def bg_grad(ctx, top, bottom, mid=None, mid_at=0.55, w=1920, h=1080):
    stops = [(0, top), (mid_at, mid), (1, bottom)] if mid else [(0, top), (1, bottom)]
    ctx.set_source(lin(0, 0, 0, h, stops))
    ctx.paint()


def grid_dots(ctx, x0, y0, x1, y1, spacing, color, a=0.1, r=2.4, drift=(0, 0)):
    setc(ctx, color, a)
    ox, oy = drift[0] % spacing, drift[1] % spacing
    nx = int((x1 - x0) / spacing) + 2
    ny = int((y1 - y0) / spacing) + 2
    for i in range(-1, nx):
        for j in range(-1, ny):
            circle(ctx, x0 + i * spacing + ox, y0 + j * spacing + oy, r)
    ctx.fill()


def grid_lines(ctx, x0, y0, x1, y1, spacing, color, a=0.08, w=1.5):
    ctx.set_line_width(w)
    setc(ctx, color, a)
    x = x0
    while x <= x1:
        ctx.move_to(x, y0)
        ctx.line_to(x, y1)
        x += spacing
    y = y0
    while y <= y1:
        ctx.move_to(x0, y)
        ctx.line_to(x1, y)
        y += spacing
    ctx.stroke()


def circuit_traces(ctx, t, x0, y0, x1, y1, seed=3, n=26, color="#3BE0C8", a=0.18, pulse="#9FFFF0"):
    """电路走线背景（直角折线 + 流动的光点）。"""
    R = rng(seed)
    for i in range(n):
        x = R.uniform(x0, x1)
        y = R.uniform(y0, y1)
        pts = [(x, y)]
        for k in range(R.randint(2, 4)):
            if k % 2 == 0:
                x += R.choice((-1, 1)) * R.uniform(80, 260)
            else:
                y += R.choice((-1, 1)) * R.uniform(60, 180)
            pts.append((x, y))
        stroke_pts(ctx, pts, 2.5, color, a)
        circle(ctx, pts[0][0], pts[0][1], 5)
        fill(ctx, color, a * 1.4)
        circle(ctx, pts[-1][0], pts[-1][1], 5)
        fill(ctx, color, a * 1.4)
        # 光点沿线流动
        L = sum(math.dist(p, q) for p, q in zip(pts, pts[1:]))
        ph = (t * 140 / max(L, 1) + R.random()) % 1
        d = ph * L
        for p, q in zip(pts, pts[1:]):
            s = math.dist(p, q)
            if d <= s:
                u = d / max(s, 1e-6)
                px, py = lerp(p[0], q[0], u), lerp(p[1], q[1], u)
                glow(ctx, px, py, 16, pulse, a * 2.2)
                break
            d -= s


def floor(ctx, y, color="#000000", a=0.12, w=1920):
    ctx.set_source(lin(0, y - 6, 0, y + 60, [(0, color, a), (1, color, 0)]))
    ctx.rectangle(-400, y, w + 800, 60)
    ctx.fill()


# ---------------------------------------------------------------- 文字小部件


def tag(ctx, s, x, y, size=26, fg="#FFFFFF", bg="#2B2233", a=1.0, bg_a=0.85, align="c", dot=None,
        weight="bold", border=None):
    """胶囊标签，返回 (宽, 高)。"""
    if a <= 0.003:
        return 0, 0
    tw = text_w(ctx, s, size, weight)
    px, py = size * 0.62, size * 0.36
    dw = size * 0.8 if dot else 0
    w, h = tw + px * 2 + dw, size + py * 2
    x0 = x - w / 2 if align == "c" else (x - w if align == "r" else x)
    rrect(ctx, x0, y - h / 2, w, h, h / 2)
    setc(ctx, bg, a * bg_a)
    ctx.fill()
    if border:
        rrect(ctx, x0, y - h / 2, w, h, h / 2)
        ctx.set_line_width(2.5)
        setc(ctx, border, a)
        ctx.stroke()
    if dot:
        circle(ctx, x0 + px + size * 0.25, y, size * 0.22)
        fill(ctx, dot, a)
    text(ctx, s, x0 + px + dw, y, size, fg, a, weight, "l")
    return w, h


def name_card(ctx, s, x, y, color, size=30, a=1.0, k=1.0, sub=None, w=None):
    """公司 / 产品名片：白底圆角卡 + 左侧色块，(x, y) 为中心。"""
    if a <= 0.003 or k <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, k)
    tw = max(text_w(ctx, s, size, "black"), text_w(ctx, sub, size * 0.6, "bold") if sub else 0)
    w = w or tw + size * 2.2
    h = size * (2.3 if sub else 1.85)
    box_shadow(ctx, -w / 2, -h / 2, w, h, h * 0.3, blur=18, a=0.18 * a, dy=7)
    rrect(ctx, -w / 2, -h / 2, w, h, min(h * 0.3, 18))
    setc(ctx, "#FFFFFF", 0.97 * a)
    ctx.fill()
    rrect(ctx, -w / 2 + size * 0.35, -h / 2 + h * 0.22, size * 0.32, h * 0.56, size * 0.16)
    setc(ctx, color, a)
    ctx.fill()
    tx = -w / 2 + size * 0.95
    if sub:
        text(ctx, s, tx, -size * 0.32, size, "#2B2233", a, "black", "l")
        text(ctx, sub, tx, size * 0.5, size * 0.6, "#7A7186", a, "bold", "l")
    else:
        text(ctx, s, tx, 0, size, "#2B2233", a, "black", "l")
    ctx.restore()


def big_stat(ctx, value, label, x, y, size=96, color="#FF9F68", a=1.0, label_color="#FFFFFF", k=1.0):
    if a <= 0.003:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, k)
    text(ctx, value, 3, 4, size, "#000000", 0.2 * a, "black")
    text(ctx, value, 0, 0, size, color, a, "black")
    if label:
        text(ctx, label, 0, size * 0.78, size * 0.3, label_color, a * 0.9, "bold")
    ctx.restore()


def count_fmt(v, fmt="{:,.0f}"):
    return fmt.format(v)


# ---------------------------------------------------------------- 芯片 / 半导体


def chip_pkg(ctx, x, y, s=200, label="", sub="", color="#76B900", a=1.0, glow_a=0.0, t=0.0, die="#2B3A2B"):
    """芯片封装（俯视）：基板 + 引脚 + 裸片 + 文字。s 为边长。"""
    if a <= 0.003:
        return
    h = s / 2
    if glow_a > 0:
        glow(ctx, x, y, s * 1.1, color, glow_a * a)
    box_shadow(ctx, x - h, y - h, s, s, s * 0.08, blur=s * 0.15, a=0.3 * a, dy=s * 0.05)
    n = 7
    for i in range(n):
        v = -h + s * (i + 1) / (n + 1)
        for (px, py, w_, h_) in ((x + v - s * 0.02, y - h - s * 0.06, s * 0.04, s * 0.07),
                                 (x + v - s * 0.02, y + h - s * 0.01, s * 0.04, s * 0.07),
                                 (x - h - s * 0.06, y + v - s * 0.02, s * 0.07, s * 0.04),
                                 (x + h - s * 0.01, y + v - s * 0.02, s * 0.07, s * 0.04)):
            ctx.rectangle(px, py, w_, h_)
    fill(ctx, "#C9A14A", a)
    rrect(ctx, x - h, y - h, s, s, s * 0.08)
    ctx.set_source(lin(0, y - h, 0, y + h, [(0, "#3A4152", a), (1, "#22262F", a)]))
    ctx.fill()
    d = s * 0.62
    rrect(ctx, x - d / 2, y - d / 2, d, d, s * 0.05)
    ctx.set_source(lin(x - d / 2, y - d / 2, x + d / 2, y + d / 2,
                       [(0, mix(color, "#FFFFFF", 0.25), a), (1, mix(color, "#000000", 0.25), a)]))
    ctx.fill()
    # 裸片上的细纹
    ctx.set_line_width(max(1, s * 0.006))
    setc(ctx, "#FFFFFF", 0.18 * a)
    for i in range(1, 6):
        ctx.move_to(x - d / 2 + d * i / 6, y - d / 2 + 4)
        ctx.line_to(x - d / 2 + d * i / 6, y + d / 2 - 4)
    ctx.stroke()
    if label:
        text(ctx, label, x, y - (s * 0.06 if sub else 0), s * 0.17, "#FFFFFF", a, "black")
    if sub:
        text(ctx, sub, x, y + s * 0.13, s * 0.085, "#FFFFFF", 0.85 * a, "bold")
    # 扫光
    ph = (t * 0.35) % 1
    if a > 0.3:
        ctx.save()
        rrect(ctx, x - d / 2, y - d / 2, d, d, s * 0.05)
        ctx.clip()
        sx = x - d + ph * d * 3
        ctx.set_source(lin(sx - d * 0.25, y - d, sx + d * 0.25, y + d,
                           [(0, "#FFFFFF", 0), (0.5, "#FFFFFF", 0.18 * a), (1, "#FFFFFF", 0)]))
        ctx.paint()
        ctx.restore()


def wafer(ctx, x, y, r, a=1.0, t=0.0, glow_a=0.0, cell=None, lit=None):
    """晶圆：圆形硅片 + 晶粒网格 + 彩虹反光。lit 为点亮晶粒的比例 0..1。"""
    if a <= 0.003:
        return
    if glow_a > 0:
        glow(ctx, x, y, r * 1.5, "#B8E1FF", glow_a * a)
    box_shadow(ctx, x - r, y - r, 2 * r, 2 * r, r, blur=r * 0.2, a=0.25 * a, dy=r * 0.06)
    circle(ctx, x, y, r)
    ctx.set_source(rad(x - r * 0.3, y - r * 0.3, r * 0.1, r * 1.1,
                       [(0, "#E9EEF5", a), (0.5, "#B7C3D6", a), (1, "#8C98AE", a)]))
    ctx.fill()
    cell = cell or r / 6.5
    ctx.save()
    circle(ctx, x, y, r * 0.94)
    ctx.clip()
    n = int(r / cell) + 1
    R = rng(int(r))
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            cx, cy = x + i * cell, y + j * cell
            if math.hypot(cx - x, cy - y) > r * 0.9:
                continue
            on = lit is not None and R.random() < lit
            rrect(ctx, cx - cell * 0.44, cy - cell * 0.44, cell * 0.88, cell * 0.88, cell * 0.12)
            if on:
                setc(ctx, "#7CFFB2", 0.85 * a)
            else:
                setc(ctx, "#6F7C95", 0.35 * a)
            ctx.fill()
    # 彩虹反光
    ang = t * 0.5
    ctx.set_source(lin(x + math.cos(ang) * r, y + math.sin(ang) * r, x - math.cos(ang) * r, y - math.sin(ang) * r,
                       [(0, "#FF9AD5", 0.0), (0.35, "#9AD9FF", 0.22 * a), (0.55, "#B8FFC9", 0.18 * a),
                        (0.75, "#FFE39A", 0.15 * a), (1, "#FF9AD5", 0.0)]))
    ctx.paint()
    ctx.restore()
    ctx.set_line_width(3)
    setc(ctx, "#FFFFFF", 0.5 * a)
    circle(ctx, x, y, r)
    ctx.stroke()
    # 定位缺口
    poly(ctx, [(x - r * 0.08, y + r * 0.99), (x, y + r * 0.9), (x + r * 0.08, y + r * 0.99)])
    fill(ctx, "#3A3646", a)


def hbm_stack(ctx, x, y, w, h, layers=8, a=1.0, color="#5B7CFA", k=1.0):
    """高带宽内存（HBM）：一摞薄片（侧视），(x, y) 为底部中心。k 为堆叠进度。"""
    if a <= 0.003:
        return
    lh = h / layers
    shown = int(math.ceil(layers * k))
    for i in range(shown):
        q = clamp(layers * k - i)
        yy = y - (i + 1) * lh - (1 - ease_out(q)) * 40
        rrect(ctx, x - w / 2, yy, w, lh * 0.82, 3)
        ctx.set_source(lin(0, yy, 0, yy + lh, [(0, mix(color, "#FFFFFF", 0.35), a * q), (1, color, a * q)]))
        ctx.fill()


def server_rack(ctx, x, y, w, h, t=0.0, a=1.0, units=8, accent="#7CFFB2", seed=1):
    """服务器机柜（正视），(x, y) 为底部中心。"""
    if a <= 0.003:
        return
    x0, y0 = x - w / 2, y - h
    box_shadow(ctx, x0, y0, w, h, 10, blur=26, a=0.3 * a, dy=10)
    rrect(ctx, x0, y0, w, h, 10)
    ctx.set_source(lin(0, y0, 0, y, [(0, "#3A3F4E", a), (1, "#23262F", a)]))
    ctx.fill()
    uh = (h - 24) / units
    R = rng(seed)
    for i in range(units):
        uy = y0 + 12 + i * uh
        rrect(ctx, x0 + 10, uy + 3, w - 20, uh - 6, 4)
        fill(ctx, "#2D3240", a)
        for j in range(3):
            on = math.sin(t * R.uniform(3, 9) + R.random() * 6) > -0.2
            circle(ctx, x0 + 24 + j * 14, uy + uh / 2, 3.6)
            fill(ctx, accent if on else "#2E5E46", a)
        rrect(ctx, x0 + w * 0.45, uy + uh / 2 - 3, w * 0.4, 6, 3)
        fill(ctx, "#4A5162", a)


def fiber(ctx, pts, t=0.0, a=1.0, color="#7FE7FF", width=6, pulses=3, speed=0.6, p=1.0, core="#FFFFFF"):
    """光纤：沿折线 / 曲线发光，带流动光脉冲；p 为铺设进度。"""
    if a <= 0.003 or len(pts) < 2 or p <= 0.001:
        return
    from .core import polyline_partial
    seg = polyline_partial(pts, 0.0, p)
    stroke_pts(ctx, seg, width * 3.2, color, 0.12 * a)
    stroke_pts(ctx, seg, width, color, 0.75 * a)
    stroke_pts(ctx, seg, width * 0.35, core, 0.8 * a)
    from .core import point_on
    for i in range(pulses):
        ph = (t * speed + i / pulses) % 1
        if ph > p:
            continue
        (px, py), _ = point_on(pts, ph)
        glow(ctx, px, py, width * 5, color, 0.9 * a)
        circle(ctx, px, py, width * 0.7)
        fill(ctx, "#FFFFFF", a)


def copper(ctx, pts, t=0.0, a=1.0, hot=0.0, width=8):
    """铜线（发热时变红）。"""
    if a <= 0.003:
        return
    c = mix("#C77B3C", "#FF4B3A", hot)
    stroke_pts(ctx, pts, width + 4, "#5A3418", 0.6 * a)
    stroke_pts(ctx, pts, width, c, a)
    if hot > 0.05:
        for (px, py) in pts[1:-1:3]:
            glow(ctx, px, py, 40, "#FF6A3D", 0.25 * hot * a)


def optical_module(ctx, x, y, w=420, h=150, a=1.0, t=0.0, lid=0.0, label="光模块"):
    """光模块（侧视）：外壳 + 金手指 + 内部 DSP + 激光器；lid 为外壳透明程度（看内部）。"""
    if a <= 0.003:
        return
    x0, y0 = x - w / 2, y - h / 2
    box_shadow(ctx, x0, y0, w, h, 16, blur=24, a=0.25 * a, dy=8)
    # 金手指
    for i in range(8):
        ctx.rectangle(x0 - 34, y0 + 18 + i * (h - 36) / 8, 34, (h - 36) / 8 - 4)
    fill(ctx, "#D9B44A", a)
    # 内部
    rrect(ctx, x0, y0, w, h, 16)
    fill(ctx, "#1F2F2A", a)
    rrect(ctx, x0 + 26, y + 6, 104, h * 0.38, 8)
    fill(ctx, "#3BAA6B", a)
    text(ctx, "DSP", x0 + 78, y + 6 + h * 0.19, 26, "#FFFFFF", a, "black")
    rrect(ctx, x0 + w - 150, y - h * 0.32, 66, h * 0.3, 6)
    fill(ctx, "#8E7CFF", a)
    text(ctx, "激光", x0 + w - 117, y - h * 0.17, 20, "#FFFFFF", a, "bold")
    # 外壳（可半透明）
    if lid < 0.99:
        rrect(ctx, x0, y0, w, h, 16)
        ctx.set_source(lin(0, y0, 0, y0 + h, [(0, "#D9DEE8", a * (1 - lid)), (1, "#9AA3B5", a * (1 - lid))]))
        ctx.fill()
        text(ctx, label, x, y, 34, "#3A3F4E", a * (1 - lid), "black")
    ctx.set_line_width(3)
    setc(ctx, "#FFFFFF", 0.45 * a)
    rrect(ctx, x0, y0, w, h, 16)
    ctx.stroke()
    # 光口
    rrect(ctx, x0 + w - 8, y - 26, 30, 52, 6)
    fill(ctx, "#5A6275", a)


def waveform(ctx, x0, y0, w, h, t, kind="square", color="#FFD36B", a=1.0, speed=1.0, p=1.0):
    """电信号（方波）/ 光信号（脉冲）。"""
    if a <= 0.003:
        return
    pts = []
    n = 120
    for i in range(n + 1):
        u = i / n * p
        ph = (u * 6 - t * speed) % 1
        if kind == "square":
            v = 1 if ph < 0.5 else -1
        else:
            v = math.exp(-((ph - 0.5) / 0.08) ** 2) * 2 - 1
        pts.append((x0 + u * w, y0 - v * h / 2))
    stroke_pts(ctx, pts, 5, color, a)


def factory(ctx, x, y, w, h, a=1.0, t=0.0, label="", color="#E9E4F2", accent="#E5484D", lights=True):
    """晶圆厂（无尘车间风格）：(x, y) 为底部中心。"""
    if a <= 0.003:
        return
    x0, y0 = x - w / 2, y - h
    box_shadow(ctx, x0, y0, w, h, 14, blur=30, a=0.28 * a, dy=12)
    rrect(ctx, x0, y0 + h * 0.22, w, h * 0.78, 12)
    ctx.set_source(lin(0, y0, 0, y, [(0, color, a), (1, mix(color, "#9AA0AE", 0.35), a)]))
    ctx.fill()
    # 屋顶的设备
    for i in range(4):
        rrect(ctx, x0 + w * (0.1 + i * 0.22), y0 + h * 0.08, w * 0.14, h * 0.16, 6)
        fill(ctx, mix(color, "#6E7380", 0.35), a)
    # 横向长窗
    for r in range(2):
        yy = y0 + h * (0.36 + r * 0.22)
        rrect(ctx, x0 + w * 0.06, yy, w * 0.88, h * 0.12, 6)
        fill(ctx, "#2B3550", a)
        if lights:
            for i in range(10):
                k = 0.5 + 0.5 * math.sin(t * 2 + i * 1.3 + r)
                rrect(ctx, x0 + w * 0.08 + i * w * 0.086, yy + 6, w * 0.06, h * 0.12 - 12, 3)
                fill(ctx, "#9FD8FF", (0.35 + 0.45 * k) * a)
    rrect(ctx, x - w * 0.08, y - h * 0.22, w * 0.16, h * 0.22, 4)
    fill(ctx, "#3A3646", a)
    if label:
        rrect(ctx, x - w * 0.22, y0 + h * 0.24 - 24, w * 0.44, 48, 10)
        fill(ctx, accent, a)
        text(ctx, label, x, y0 + h * 0.24, 30, "#FFFFFF", a, "black")


def office(ctx, x, y, w, h, color="#4C8DFF", a=1.0, label="", sub="", windows=True, t=0.0, roof=None):
    """公司大楼（正视），(x, y) 为底部中心。"""
    if a <= 0.003:
        return
    x0, y0 = x - w / 2, y - h
    box_shadow(ctx, x0, y0, w, h, 12, blur=26, a=0.25 * a, dy=10)
    rrect(ctx, x0, y0, w, h, 12)
    ctx.set_source(lin(0, y0, 0, y, [(0, mix(color, "#FFFFFF", 0.25), a), (1, color, a)]))
    ctx.fill()
    if windows:
        cols = max(2, int(w / 60))
        rows = max(2, int((h - 90) / 60))
        for i in range(cols):
            for j in range(rows):
                k = 0.5 + 0.5 * math.sin(t * 1.3 + i * 2.1 + j * 1.7)
                rrect(ctx, x0 + 18 + i * (w - 36) / cols, y0 + 70 + j * 58, (w - 36) / cols - 14, 40, 5)
                fill(ctx, "#FFFFFF", (0.28 + 0.25 * k) * a)
    rrect(ctx, x - 26, y - 64, 52, 64, 6)
    fill(ctx, mix(color, "#000000", 0.35), a)
    if label:
        text(ctx, label, x, y0 + 34, min(40, w * 0.16), "#FFFFFF", a, "black")
    if sub:
        text(ctx, sub, x, y + 34, 24, "#FFFFFF", 0.85 * a, "bold")


def garage(ctx, x, y, w, h, a=1.0, color="#F4E6D0", label="", t=0.0, door=0.0, glow_a=0.0):
    """车库（创业公司）。door 为卷帘门打开程度，glow_a 为门里透出的光。"""
    if a <= 0.003:
        return
    x0, y0 = x - w / 2, y - h
    box_shadow(ctx, x0, y0, w, h, 10, blur=22, a=0.22 * a, dy=8)
    poly(ctx, [(x0 - 20, y0 + h * 0.3), (x, y0 - h * 0.05), (x0 + w + 20, y0 + h * 0.3)])
    fill(ctx, "#C4664A", a)
    ctx.rectangle(x0, y0 + h * 0.28, w, h * 0.72)
    fill(ctx, color, a)
    dx0, dy0, dw, dh = x0 + w * 0.15, y0 + h * 0.45, w * 0.7, h * 0.55
    ctx.rectangle(dx0, dy0, dw, dh)
    fill(ctx, "#2B2233", a)
    if glow_a > 0:
        ctx.save()
        ctx.rectangle(dx0, dy0, dw, dh)
        ctx.clip()
        glow(ctx, x, y, dw, "#FFD36B", glow_a * a)
        ctx.restore()
    ctx.rectangle(dx0, dy0, dw, dh * (1 - door))
    fill(ctx, "#B9B2A6", a)
    for i in range(int(6 * (1 - door))):
        ctx.rectangle(dx0, dy0 + i * dh / 6, dw, 3)
        fill(ctx, "#8C857A", a)
    if label:
        text(ctx, label, x, y0 + h * 0.36, min(30, w * 0.12), "#5A3A30", a, "black")


def castle(ctx, x, y, w, h, color="#C9B79C", a=1.0, flag=None, flag_text="", t=0.0, gate=0.0):
    """围墙城堡（互联网"地主"），(x, y) 为底部中心。"""
    if a <= 0.003:
        return
    x0, y0 = x - w / 2, y - h
    box_shadow(ctx, x0, y0, w, h, 6, blur=22, a=0.25 * a, dy=8)
    ctx.rectangle(x0, y0 + h * 0.2, w, h * 0.8)
    ctx.set_source(lin(0, y0, 0, y, [(0, mix(color, "#FFFFFF", 0.15), a), (1, mix(color, "#000000", 0.2), a)]))
    ctx.fill()
    n = max(3, int(w / 46))
    bw = w / (2 * n - 1)
    for i in range(n):
        ctx.rectangle(x0 + i * 2 * bw, y0 + h * 0.08, bw, h * 0.14)
    fill(ctx, color, a)
    ctx.set_line_width(2)
    setc(ctx, mix(color, "#000000", 0.35), 0.4 * a)
    for r in range(4):
        yy = y0 + h * (0.35 + r * 0.16)
        ctx.move_to(x0, yy)
        ctx.line_to(x0 + w, yy)
    ctx.stroke()
    # 城门
    gw, gh = w * 0.24, h * 0.42
    ctx.move_to(x - gw / 2, y)
    ctx.line_to(x - gw / 2, y - gh + gw / 2)
    ctx.arc(x, y - gh + gw / 2, gw / 2, math.pi, 0)
    ctx.line_to(x + gw / 2, y)
    ctx.close_path()
    fill(ctx, "#3A2E28", a)
    if gate > 0:
        ctx.save()
        ctx.move_to(x - gw / 2, y)
        ctx.line_to(x - gw / 2, y - gh + gw / 2)
        ctx.arc(x, y - gh + gw / 2, gw / 2, math.pi, 0)
        ctx.line_to(x + gw / 2, y)
        ctx.close_path()
        ctx.clip()
        glow(ctx, x, y - gh * 0.4, gw, "#FFE29A", 0.8 * gate * a)
        ctx.restore()
    else:
        for i in range(4):
            ctx.rectangle(x - gw / 2 + (i + 0.5) * gw / 4 - 2, y - gh, 4, gh)
        fill(ctx, "#7A6A5E", a)
    if flag:
        fx, fy = x + w * 0.32, y0 + h * 0.08
        ctx.rectangle(fx - 2, fy - 70, 4, 70)
        fill(ctx, "#5A4A40", a)
        wv = [math.sin(t * 5 + i * 0.8) * 4 for i in range(5)]
        ctx.move_to(fx + 2, fy - 70)
        for i in range(5):
            ctx.line_to(fx + 2 + i * 22, fy - 70 + wv[i])
        for i in range(4, -1, -1):
            ctx.line_to(fx + 2 + i * 22, fy - 36 + wv[i])
        ctx.close_path()
        fill(ctx, flag, a)
        if flag_text:
            text(ctx, flag_text, fx + 46, fy - 53 + wv[2], 18, "#FFFFFF", a, "black")


def gavel(ctx, x, y, s=1.0, rot=0.0, a=1.0):
    """法槌，(x, y) 为槌头中心。"""
    if a <= 0.003:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    rrect(ctx, -10, 10, 20, 150, 8)
    fill(ctx, "#8C5A33", a)
    rrect(ctx, -70, -30, 140, 56, 14)
    ctx.set_source(lin(0, -30, 0, 26, [(0, "#B57A45", a), (1, "#7A4A26", a)]))
    ctx.fill()
    for xx in (-56, 44):
        rrect(ctx, xx, -34, 12, 64, 5)
        fill(ctx, "#D9B44A", a)
    ctx.restore()


def price_tag(ctx, x, y, s, label, color="#FFC857", a=1.0, rot=-0.12):
    if a <= 0.003:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    w = text_w(ctx, label, 40 * s, "black") + 90 * s
    h = 70 * s
    box_shadow(ctx, -w / 2, -h / 2, w, h, 10 * s, blur=16, a=0.2 * a, dy=6)
    poly(ctx, [(-w / 2, 0), (-w / 2 + 28 * s, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2 + 28 * s, h / 2)])
    fill(ctx, color, a)
    circle(ctx, -w / 2 + 26 * s, 0, 8 * s)
    fill(ctx, "#FFFFFF", a)
    text(ctx, label, 14 * s, 0, 40 * s, "#2B2233", a, "black")
    ctx.restore()


def medal(ctx, x, y, r, a=1.0, t=0.0, label=""):
    if a <= 0.003:
        return
    for sx, c in ((-1, "#4C8DFF"), (1, "#E5484D")):
        poly(ctx, [(x + sx * r * 0.15, y - r * 0.6), (x + sx * r * 0.75, y - r * 2.2), (x + sx * r * 0.35, y - r * 2.3),
                   (x - sx * r * 0.1, y - r * 0.7)])
        fill(ctx, c, a)
    glow(ctx, x, y, r * 2, "#FFE58A", 0.35 * a)
    circle(ctx, x, y, r)
    ctx.set_source(rad(x - r * 0.3, y - r * 0.3, r * 0.1, r, [(0, "#FFF3B8", a), (1, "#E0A42B", a)]))
    ctx.fill()
    circle(ctx, x, y, r * 0.78)
    ctx.set_line_width(r * 0.06)
    setc(ctx, "#B9771B", a)
    ctx.stroke()
    if label:
        text(ctx, label, x, y, r * 0.5, "#8A5A12", a, "black")
    star4(ctx, x + r * 0.45, y - r * 0.45, r * 0.25, "#FFFFFF", 0.9 * a, t)


def pylon(ctx, x, y, h, a=1.0, color="#9AA3B5"):
    """输电塔，(x, y) 为底部中心。"""
    if a <= 0.003:
        return
    w = h * 0.36
    ctx.set_line_width(max(2, h * 0.025))
    setc(ctx, color, a)
    ctx.move_to(x - w / 2, y)
    ctx.line_to(x - w * 0.08, y - h)
    ctx.line_to(x + w * 0.08, y - h)
    ctx.line_to(x + w / 2, y)
    for k in (0.3, 0.55, 0.8):
        yy = y - h * k
        half = lerp(w / 2, w * 0.08, k)
        ctx.move_to(x - half, yy)
        ctx.line_to(x + half, yy)
    for k in (0.62, 0.86):
        yy = y - h * k
        ctx.move_to(x - w * 0.7, yy)
        ctx.line_to(x + w * 0.7, yy)
    ctx.stroke()


def whale(ctx, x, y, s=1.0, a=1.0, t=0.0, color="#4D6BFE"):
    """小鲸鱼（DeepSeek 风格的通用卡通形象），(x, y) 为中心，s=1 时宽约 220。"""
    if a <= 0.003:
        return
    ctx.save()
    ctx.translate(x, y + math.sin(t * 2) * 6 * s)
    ctx.scale(s, s)
    ctx.rotate(math.sin(t * 1.4) * 0.04)
    # 尾巴
    sw = math.sin(t * 3) * 0.2
    ctx.save()
    ctx.translate(100, -10)
    ctx.rotate(-0.4 + sw)
    ctx.move_to(0, 0)
    ctx.curve_to(30, -20, 60, -50, 70, -40)
    ctx.curve_to(60, -20, 50, 0, 70, 20)
    ctx.curve_to(40, 20, 20, 10, 0, 10)
    ctx.close_path()
    fill(ctx, color, a)
    ctx.restore()
    ctx.move_to(-110, 0)
    ctx.curve_to(-110, -70, 40, -80, 105, -12)
    ctx.curve_to(110, 30, 40, 60, -40, 55)
    ctx.curve_to(-90, 52, -110, 30, -110, 0)
    ctx.close_path()
    ctx.set_source(lin(0, -80, 0, 60, [(0, mix(color, "#FFFFFF", 0.25), a), (1, color, a)]))
    ctx.fill()
    ctx.move_to(-104, 18)
    ctx.curve_to(-60, 40, 20, 48, 80, 22)
    ctx.curve_to(40, 56, -60, 58, -104, 18)
    fill(ctx, "#DCE6FF", 0.9 * a)
    circle(ctx, -60, -10, 8)
    fill(ctx, "#1B1F3A", a)
    circle(ctx, -62, -13, 3)
    fill(ctx, "#FFFFFF", a)
    # 喷水
    for i in range(3):
        ph = (t * 1.2 + i / 3) % 1
        circle(ctx, -30 + (i - 1) * 16 * ph, -78 - ph * 60, 7 * (1 - ph) + 2)
        fill(ctx, "#9FD8FF", a * (1 - ph))
    ctx.restore()


def moon_icon(ctx, x, y, r, a=1.0, color="#FFFFFF", bg="#1E1E2E"):
    circle(ctx, x, y, r)
    fill(ctx, bg, a)
    ctx.save()
    circle(ctx, x, y, r * 0.7)
    ctx.clip()
    circle(ctx, x, y, r * 0.7)
    fill(ctx, color, a)
    circle(ctx, x + r * 0.32, y - r * 0.22, r * 0.62)
    fill(ctx, bg, a)
    ctx.restore()


def smiley(ctx, x, y, r, a=1.0, color="#FFD21E"):
    """黄色笑脸（通用表情，用来代表开源模型社区）。"""
    circle(ctx, x, y, r)
    ctx.set_source(rad(x - r * 0.3, y - r * 0.3, r * 0.1, r, [(0, "#FFE680", a), (1, color, a)]))
    ctx.fill()
    for sx in (-1, 1):
        ellipse(ctx, x + sx * r * 0.33, y - r * 0.18, r * 0.1, r * 0.16)
        fill(ctx, "#3A2E1E", a)
    ctx.move_to(x - r * 0.45, y + r * 0.15)
    ctx.curve_to(x - r * 0.25, y + r * 0.55, x + r * 0.25, y + r * 0.55, x + r * 0.45, y + r * 0.15)
    ctx.set_line_width(r * 0.1)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    setc(ctx, "#3A2E1E", a)
    ctx.stroke()


def gemini_star(ctx, x, y, r, a=1.0, rot=0.0):
    """四角星（通用造型）。"""
    if a <= 0.003:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    k = r * 0.12
    ctx.move_to(0, -r)
    ctx.curve_to(k, -k, k, -k, r, 0)
    ctx.curve_to(k, k, k, k, 0, r)
    ctx.curve_to(-k, k, -k, k, -r, 0)
    ctx.curve_to(-k, -k, -k, -k, 0, -r)
    ctx.set_source(lin(-r, r, r, -r, [(0, "#4C8DFF", a), (0.6, "#8B6CFF", a), (1, "#FF7AC6", a)]))
    ctx.fill()
    ctx.restore()


def iphone(ctx, x, y, h, a=1.0, screen="#F7F5FA"):
    """手机正面，(x, y) 为中心，高 h，返回屏幕区域 (x0, y0, w, h)。"""
    w = h * 0.49
    x0, y0 = x - w / 2, y - h / 2
    box_shadow(ctx, x0, y0, w, h, w * 0.16, blur=h * 0.06, a=0.3 * a, dy=h * 0.02)
    rrect(ctx, x0, y0, w, h, w * 0.16)
    fill(ctx, "#1E1C24", a)
    m = w * 0.045
    rrect(ctx, x0 + m, y0 + m, w - 2 * m, h - 2 * m, w * 0.13)
    fill(ctx, screen, a)
    rrect(ctx, x - w * 0.15, y0 + m * 2.2, w * 0.3, m * 1.6, m * 0.8)
    fill(ctx, "#1E1C24", a)
    return (x0 + m, y0 + m * 4.5, w - 2 * m, h - m * 6)


def app_tile(ctx, x, y, s, color, label="", a=1.0, fg="#FFFFFF", sub=None, k=1.0, text_size=None):
    """通用 App 图标：彩色圆角方块 + 文字（不复刻任何官方 Logo）。"""
    if a <= 0.003 or k <= 0.01:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(k, k)
    box_shadow(ctx, -s / 2, -s / 2, s, s, s * 0.24, blur=s * 0.2, a=0.22 * a, dy=s * 0.06)
    rrect(ctx, -s / 2, -s / 2, s, s, s * 0.24)
    ctx.set_source(lin(0, -s / 2, 0, s / 2, [(0, mix(color, "#FFFFFF", 0.18), a), (1, color, a)]))
    ctx.fill()
    if label:
        n = len(label)
        sz = text_size or (s * (0.42 if n <= 2 else 0.3 if n <= 3 else 0.22))
        text(ctx, label, 0, 0, sz, fg, a, "black")
    ctx.restore()
    if sub:
        text(ctx, sub, x, y + s * 0.5 * k + 22, 22, "#2B2233", a, "bold")


def doc_card(ctx, x, y, w, h, kind="doc", a=1.0, p=1.0, title="", accent=None, t=0.0):
    """办公文档卡片：doc（文档）/ sheet（表格）/ slide（幻灯片）/ mail（邮件）/ chart（图表）。
    p 为内容填充进度。(x, y) 为中心。"""
    if a <= 0.003:
        return
    colors = {"doc": "#4C8DFF", "sheet": "#20A464", "slide": "#F5A623", "mail": "#E5484D", "chart": "#8B6CFF"}
    c = accent or colors.get(kind, "#4C8DFF")
    x0, y0 = x - w / 2, y - h / 2
    box_shadow(ctx, x0, y0, w, h, 14, blur=22, a=0.22 * a, dy=8)
    rrect(ctx, x0, y0, w, h, 14)
    fill(ctx, "#FFFFFF", a)
    ctx.save()
    rrect(ctx, x0, y0, w, h, 14)
    ctx.clip()
    ctx.rectangle(x0, y0, w, 44)
    fill(ctx, c, a)
    ctx.restore()
    if title:
        text(ctx, title, x0 + 18, y0 + 22, 22, "#FFFFFF", a, "black", "l")
    cx0, cy0, cw, ch = x0 + 18, y0 + 62, w - 36, h - 80
    if kind in ("doc", "mail"):
        n = int(ch / 22)
        for i in range(n):
            q = clamp(p * n - i)
            if q <= 0:
                break
            lw = cw * (0.62 if i % 4 == 3 else 0.95) * ease_out(q)
            rrect(ctx, cx0, cy0 + i * 22, lw, 9, 4.5)
            fill(ctx, "#C9C3D3", a)
    elif kind == "sheet":
        rows, cols = int(ch / 28), 4
        cwid = cw / cols
        for r in range(rows):
            for cc in range(cols):
                q = clamp(p * rows * cols - (r * cols + cc))
                ctx.rectangle(cx0 + cc * cwid, cy0 + r * 28, cwid - 3, 25)
                setc(ctx, "#E8F5EC" if r == 0 else "#F4F6F8", a)
                ctx.fill()
                if q > 0 and r > 0:
                    rrect(ctx, cx0 + cc * cwid + 6, cy0 + r * 28 + 9, (cwid - 18) * q, 7, 3.5)
                    fill(ctx, "#20A464" if cc == 3 else "#9AA3B5", a)
    elif kind == "slide":
        rrect(ctx, cx0, cy0, cw, ch, 8)
        fill(ctx, "#FFF6E6", a)
        q = clamp(p * 3)
        rrect(ctx, cx0 + 16, cy0 + 16, (cw - 32) * 0.7 * ease_out(q), 16, 8)
        fill(ctx, c, a)
        for i in range(3):
            q = clamp(p * 3 - 1 - i * 0.5)
            hh = (ch - 70) * (0.4 + 0.2 * i) * ease_out(q)
            rrect(ctx, cx0 + 24 + i * (cw - 48) / 3, cy0 + ch - 16 - hh, (cw - 48) / 3 - 14, hh, 4)
            fill(ctx, mix(c, "#FFFFFF", 0.2 * i), a)
    elif kind == "chart":
        for i in range(6):
            q = clamp(p * 6 - i)
            hh = ch * (0.25 + 0.12 * i) * ease_out(q)
            rrect(ctx, cx0 + i * cw / 6 + 4, cy0 + ch - hh, cw / 6 - 10, hh, 4)
            fill(ctx, c, a * (0.55 + 0.08 * i))


def code_panel(ctx, x0, y0, w, h, lines, t, a=1.0, cps=28, start=0.0, title="", size=22, lh=34,
               theme="dark"):
    """代码面板：lines=[(文字, 颜色, 开始时间)]，逐字打出。"""
    from .ui import term_lines, window
    cx, cy, cw, ch = window(ctx, x0, y0, w, h, title, a, theme)
    ctx.save()
    ctx.rectangle(cx, cy, cw, ch)
    ctx.clip()
    term_lines(ctx, lines, cx + 24, cy + 30, t, a, size=size, lh=lh, cps=cps, max_w=cw - 48)
    ctx.restore()
    return cx, cy, cw, ch
