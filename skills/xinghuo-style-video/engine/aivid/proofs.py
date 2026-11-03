"""经典推导的动画（拜恩 1847 年彩色版《几何原本》的配色：红、黄、蓝 + 黑线）。

每个函数 draw_xxx(ctx, u, a) 里的 u 是这一段开始后的秒数，内部自带节奏。
- angle_sum      三角形内角和 = 180°（《几何原本》卷一命题 32）
- pythagoras     勾股定理：同一个大正方形里移动 4 个直角三角形
- primes         质数有无穷多个（卷九命题 20）
- gcd            辗转相除法（卷七命题 2）：1071 与 462
- complete_square 花拉子米配方法：x² + 10x = 39
- moon_test      牛顿的"月球检验"
"""
import math

from .core import (TAU, H, W, arrow, circle, clamp, dashed, ease_io, ease_out, lerp, lin, poly, polyline_partial,
                   prog, rrect, setc, smooth, stroke_pts, text)
from .film import paint_texture

RED, YEL, BLU, INK, PAPER = "#C8372D", "#EDB12C", "#2457A8", "#1C1A18", "#F2E8D2"


def paper(ctx, a=1.0, dark=0.0):
    ctx.set_source(lin(0, 0, 0, H, [(0, "#F4EBD6"), (1, "#E2D3B2")]))
    ctx.paint()
    paint_texture(ctx, "paper", 0, 0, W, H, 0.55)
    paint_texture(ctx, "parchment", 0, 0, W, H, 0.25, scale=0.8)


def _wedge(ctx, cx, cy, r, a0, a1, color, alpha=1.0):
    ctx.move_to(cx, cy)
    ctx.arc(cx, cy, r, a0, a1) if a1 > a0 else ctx.arc_negative(cx, cy, r, a0, a1)
    ctx.close_path()
    setc(ctx, color, alpha)
    ctx.fill()


def _line(ctx, p, q, w=6, color=INK, a=1.0, k=1.0):
    if k <= 0:
        return
    stroke_pts(ctx, [p, (lerp(p[0], q[0], k), lerp(p[1], q[1], k))], w, color, a)


def _lbl(ctx, s, x, y, size=40, color=INK, a=1.0, weight="latin_i"):
    text(ctx, s, x, y, size, color, a, weight)


def eq(ctx, s, x, y, size=44, color=INK, a=1.0, align="c", weight="serif_sb"):
    text(ctx, s, x, y, size, color, a, weight, align)


# ---------------------------------------------------------------- 1. 三角形内角和


def angle_sum(ctx, u, a=1.0, ox=0, oy=0):
    A, B, C = (560 + ox, 760 + oy), (1300 + ox, 760 + oy), (820 + ox, 380 + oy)
    k = ease_io(prog(u, 0.0, 1.0))
    _line(ctx, A, B, k=k)
    _line(ctx, B, C, k=k)
    _line(ctx, C, A, k=k)
    for p, s, dx, dy in ((A, "A", -30, 30), (B, "B", 30, 30), (C, "C", 0, -40)):
        _lbl(ctx, s, p[0] + dx, p[1] + dy, 40, INK, smooth(prog(u, 0.6, 1.0)))
    angA = (math.atan2(C[1] - A[1], C[0] - A[0]), 0.0)
    angB = (-math.pi, math.atan2(C[1] - B[1], C[0] - B[0]))
    angC = (math.atan2(B[1] - C[1], B[0] - C[0]), math.atan2(A[1] - C[1], A[0] - C[0]))
    wk = smooth(prog(u, 1.0, 1.8))
    move = ease_io(prog(u, 3.2, 4.8))
    _wedge(ctx, *C, 80, angC[0], angC[1], YEL, wk)
    # α（红）、β（蓝）：平移到 C，同时转 180°，就是内错角
    for P0, (a0, a1), col in ((A, angA, RED), (B, angB, BLU)):
        cx, cy = lerp(P0[0], C[0], move), lerp(P0[1], C[1], move)
        _wedge(ctx, cx, cy, lerp(90, 80, move), a0 + math.pi * move, a1 + math.pi * move, col, wk)
    _lbl(ctx, "γ", C[0], C[1] + 110, 40, INK, wk)
    # 过 C 的平行线
    pk = ease_io(prog(u, 2.2, 3.0))
    if pk > 0:
        dashed(ctx, C[0] - 420 * pk, C[1], C[0] + 420 * pk, C[1], 5, INK, 0.9 * a, (18, 12))
        eq(ctx, "过 C 作 AB 的平行线", 1480 + ox, 300 + oy, 30, INK, smooth(prog(u, 2.4, 3.0)), "l")
    ek = smooth(prog(u, 3.4, 4.2))
    eq(ctx, "内错角相等：红 = 红，蓝 = 蓝", 1480 + ox, 360 + oy, 30, INK, ek, "l")
    fk = smooth(prog(u, 5.0, 5.8))
    eq(ctx, "三个角拼成一条直线", 1480 + ox, 450 + oy, 34, INK, fk, "l")
    eq(ctx, "α + β + γ = 180°", 1480 + ox, 520 + oy, 52, RED, fk, "l", "latin_b")


# ---------------------------------------------------------------- 2. 勾股定理


def pythagoras(ctx, u, a=1.0, ox=0, oy=0):
    aa, bb = 150.0, 260.0
    S = aa + bb
    X0, Y0 = 520 + ox - S / 2, 560 + oy - S / 2
    P = lambda x, y: (X0 + x, Y0 + y)
    # 每个三角形：(直角顶点 R, a 边端点, b 边端点)；两种摆法朝向一致，可以刚体移动
    c1 = [((0, 0), (aa, 0), (0, bb)), ((S, 0), (S, aa), (aa, 0)), ((S, S), (bb, S), (S, aa)), ((0, S), (0, bb), (bb, S))]
    c2 = [((aa, aa), (aa, 0), (S, aa)), ((S, 0), (S, aa), (aa, 0)), ((aa, S), (0, S), (aa, aa)), ((0, aa), (aa, aa), (0, S))]
    k = ease_io(prog(u, 3.2, 5.2))
    # 大正方形
    rrect(ctx, X0, Y0, S, S, 2)
    setc(ctx, PAPER, a)
    ctx.fill()
    # 空白处的颜色：先是 c²（黄），三角形移动前淡出；就位后露出 a²（红）+ b²（蓝）
    ya = smooth(prog(u, 0.6, 1.2)) * (1 - smooth(prog(u, 2.8, 3.2)))
    if ya > 0:
        poly(ctx, [P(aa, 0), P(S, aa), P(bb, S), P(0, bb)])
        setc(ctx, YEL, a * ya)
        ctx.fill()
    q = smooth(prog(u, 5.3, 5.8))
    if q > 0:
        ctx.rectangle(*P(0, 0), aa, aa)
        setc(ctx, RED, a * q)
        ctx.fill()
        ctx.rectangle(*P(aa, aa), bb, bb)
        setc(ctx, BLU, a * q)
        ctx.fill()
    for i, (t1, t2) in enumerate(zip(c1, c2)):
        kk = ease_io(clamp((prog(u, 3.2, 5.2) - i * 0.12) / 0.64))
        (r1, pa1, pb1), (r2, pa2, _) = t1, t2
        th1 = math.atan2(pa1[1] - r1[1], pa1[0] - r1[0])
        th2 = math.atan2(pa2[1] - r2[1], pa2[0] - r2[0])
        d = (th2 - th1 + math.pi) % TAU - math.pi
        th = th1 + d * kk
        R = (lerp(r1[0], r2[0], kk), lerp(r1[1], r2[1], kk))
        va = (aa * math.cos(th), aa * math.sin(th))
        vb = (-bb * math.sin(th), bb * math.cos(th))
        pts = [P(*R), P(R[0] + va[0], R[1] + va[1]), P(R[0] + vb[0], R[1] + vb[1])]
        poly(ctx, pts)
        setc(ctx, "#D9CDB0", a)
        ctx.fill_preserve()
        ctx.set_line_width(4)
        setc(ctx, INK, a)
        ctx.stroke()
    rrect(ctx, X0, Y0, S, S, 2)
    ctx.set_line_width(6)
    setc(ctx, INK, a)
    ctx.stroke()
    lk = smooth(prog(u, 0.8, 1.4)) * (1 - smooth(prog(u, 3.0, 3.4)))
    _lbl(ctx, "c²", *P(S / 2, S / 2), 64, INK, lk * a)
    _lbl(ctx, "a", *P(aa / 2, -26), 34, INK, a)
    _lbl(ctx, "b", *P(aa + bb / 2, -26), 34, INK, a)
    k2 = smooth(prog(u, 5.0, 5.6))
    _lbl(ctx, "a²", *P(aa / 2, aa / 2), 54, "#FFFFFF", k2 * a)
    _lbl(ctx, "b²", *P(aa + bb / 2, aa + bb / 2), 64, "#FFFFFF", k2 * a)
    x = 1060 + ox
    eq(ctx, "大正方形 =（a + b）²", x, 340 + oy, 34, INK, smooth(prog(u, 0.4, 1.0)), "l")
    eq(ctx, "= c² + 4 个三角形", x, 410 + oy, 36, INK, smooth(prog(u, 1.4, 2.0)), "l")
    eq(ctx, "= a² + b² + 4 个三角形", x, 480 + oy, 36, INK, smooth(prog(u, 5.2, 5.8)), "l")
    fk = smooth(prog(u, 6.0, 6.8))
    eq(ctx, "a² + b² = c²", x, 590 + oy, 72, RED, fk, "l", "latin_b")


# ---------------------------------------------------------------- 3. 质数无穷


def primes(ctx, u, a=1.0, ox=0, oy=0):
    x = 260 + ox
    rows = [("假设质数只有有限个：2, 3, 5, 7, …, p", 0.2),
            ("令 N = 2 × 3 × 5 × 7 × … × p + 1", 1.2),
            ("N 除以名单里任何一个质数，都余 1", 2.4),
            ("所以 N 的质因数不在名单里——矛盾！", 3.6)]
    for i, (s, t0) in enumerate(rows):
        eq(ctx, s, x, 270 + i * 82 + oy, 40, INK, smooth(prog(u, t0, t0 + 0.6)), "l")
    fk = smooth(prog(u, 4.6, 5.2))
    eq(ctx, "质数有无穷多个", x, 640 + oy, 60, RED, fk, "l", "serif_k")
    # 右侧的例子
    ex = 1320 + ox
    k1 = smooth(prog(u, 1.6, 2.2))
    rrect(ctx, ex - 40, 230 + oy, 560, 330, 14)
    setc(ctx, "#E6D9BA", 0.9 * k1)
    ctx.fill()
    eq(ctx, "例：", ex, 280 + oy, 32, INK, k1, "l")
    eq(ctx, "2×3×5×7 + 1 = 211", ex, 340 + oy, 38, INK, k1, "l", "latin")
    eq(ctx, "→ 211 本身是新质数", ex, 395 + oy, 30, BLU, smooth(prog(u, 2.4, 3.0)), "l")
    eq(ctx, "2×3×5×7×11×13 + 1", ex, 460 + oy, 38, INK, smooth(prog(u, 3.0, 3.6)), "l", "latin")
    eq(ctx, "= 30031 = 59 × 509", ex, 515 + oy, 38, RED, smooth(prog(u, 3.6, 4.2)), "l", "latin")


# ---------------------------------------------------------------- 4. 辗转相除


def gcd(ctx, u, a=1.0, ox=0, oy=0):
    sc = 0.86
    Wd, Ht = 1071 * sc, 462 * sc
    X0, Y0 = 200 + ox, 300 + oy
    rrect(ctx, X0, Y0, Wd, Ht, 2)
    setc(ctx, PAPER, a)
    ctx.fill()
    cols = [RED, BLU, YEL]
    # 第一步：两个 462 的正方形
    k1 = prog(u, 0.4, 1.6)
    for i in range(2):
        q = smooth(clamp(k1 * 2 - i))
        ctx.rectangle(X0 + i * Ht, Y0, Ht, Ht)
        setc(ctx, RED, 0.85 * q * a)
        ctx.fill_preserve()
        ctx.set_line_width(3)
        setc(ctx, INK, q * a)
        ctx.stroke()
    rx = X0 + 2 * Ht
    rw = Wd - 2 * Ht               # 147
    k2 = prog(u, 1.8, 3.0)
    for i in range(3):
        q = smooth(clamp(k2 * 3 - i))
        ctx.rectangle(rx, Y0 + i * rw, rw, rw)
        setc(ctx, BLU, 0.85 * q * a)
        ctx.fill_preserve()
        ctx.set_line_width(2)
        setc(ctx, INK, q * a)
        ctx.stroke()
    ry = Y0 + 3 * rw
    rh = Ht - 3 * rw               # 21
    k3 = prog(u, 3.2, 4.2)
    for i in range(7):
        q = smooth(clamp(k3 * 7 - i))
        ctx.rectangle(rx + i * rh, ry, rh, rh)
        setc(ctx, YEL, 0.95 * q * a)
        ctx.fill_preserve()
        ctx.set_line_width(1.5)
        setc(ctx, INK, q * a)
        ctx.stroke()
    rrect(ctx, X0, Y0, Wd, Ht, 2)
    ctx.set_line_width(5)
    setc(ctx, INK, a)
    ctx.stroke()
    eq(ctx, "1071", X0 + Wd / 2, Y0 - 34, 32, INK, a, "c", "latin")
    eq(ctx, "462", X0 - 50, Y0 + Ht / 2, 32, INK, a, "c", "latin")
    x = 1200 + ox
    steps = [("1071 = 2 × 462 + 147", RED, 0.6), ("462 = 3 × 147 + 21", BLU, 2.0), ("147 = 7 × 21 + 0", "#9A6A10", 3.4)]
    for i, (s, c, t0) in enumerate(steps):
        eq(ctx, s, x, 330 + i * 76 + oy, 42, c, smooth(prog(u, t0, t0 + 0.5)), "l", "latin")
    fk = smooth(prog(u, 4.4, 5.0))
    eq(ctx, "最大公约数 = 21", x, 580 + oy, 52, INK, fk, "l", "serif_k")
    eq(ctx, "大的减去小的，一直除到没有余数", x, 650 + oy, 28, INK, fk * 0.85, "l")


# ---------------------------------------------------------------- 5. 花拉子米配方法


def complete_square(ctx, u, a=1.0, ox=0, oy=0):
    xs, five = 300.0, 150.0          # x 的长度（x = 3 → 示意比例），5 的长度
    X0, Y0 = 380 + ox, 260 + oy
    k1 = smooth(prog(u, 0.2, 0.8))
    ctx.rectangle(X0, Y0, xs, xs)
    setc(ctx, BLU, 0.85 * k1 * a)
    ctx.fill()
    _lbl(ctx, "x²", X0 + xs / 2, Y0 + xs / 2, 60, "#FFFFFF", k1 * a)
    k2 = smooth(prog(u, 0.8, 1.6))
    ctx.rectangle(X0 + xs, Y0, five, xs)
    ctx.rectangle(X0, Y0 + xs, xs, five)
    setc(ctx, RED, 0.85 * k2 * a)
    ctx.fill()
    _lbl(ctx, "5x", X0 + xs + five / 2, Y0 + xs / 2, 40, "#FFFFFF", k2 * a)
    _lbl(ctx, "5x", X0 + xs / 2, Y0 + xs + five / 2, 40, "#FFFFFF", k2 * a)
    k3 = smooth(prog(u, 2.6, 3.2))
    ctx.rectangle(X0 + xs, Y0 + xs, five, five)
    setc(ctx, YEL, k3 * a)
    ctx.fill()
    _lbl(ctx, "25", X0 + xs + five / 2, Y0 + xs + five / 2, 40, INK, k3 * a)
    ctx.set_line_width(4)
    setc(ctx, INK, a)
    ctx.rectangle(X0, Y0, xs + five, xs + five)
    ctx.stroke()
    _lbl(ctx, "x", X0 + xs / 2, Y0 - 28, 36, INK, a)
    _lbl(ctx, "5", X0 + xs + five / 2, Y0 - 28, 36, INK, a)
    x = 1060 + ox
    lines = [("x² + 10x = 39", INK, 0.2), ("把 10x 拆成两块 5x", INK, 1.0), ("补上一个 5 × 5 的角", "#9A6A10", 2.6),
             ("(x + 5)² = 39 + 25 = 64", INK, 3.4), ("x + 5 = 8　→　x = 3", RED, 4.4)]
    for i, (s, c, t0) in enumerate(lines):
        eq(ctx, s, x, 300 + i * 78 + oy, 44 if i in (0, 3, 4) else 34, c, smooth(prog(u, t0, t0 + 0.5)), "l",
           "latin" if i in (0, 3) else "serif_sb")


# ---------------------------------------------------------------- 6. 牛顿的月球检验


def moon_test(ctx, u, a=1.0, ox=0, oy=0):
    ex, ey = 360 + ox, 560 + oy
    circle(ctx, ex, ey, 60)
    setc(ctx, BLU, a)
    ctx.fill()
    _lbl(ctx, "地球", ex, ey + 100, 30, INK, a, "serif_sb")
    mk = ease_io(prog(u, 0.3, 1.4))
    mx = ex + 900 * mk
    circle(ctx, mx, ey, 22)
    setc(ctx, "#8A8A8A", a)
    ctx.fill()
    _lbl(ctx, "月球", mx, ey + 60, 30, INK, a * mk, "serif_sb")
    if mk > 0.2:
        for i in range(1, 60):
            xx = ex + i * 15
            if xx < mx - 24:
                ctx.rectangle(xx, ey - 3, 2, 6)
        setc(ctx, INK, 0.5 * a)
        ctx.fill()
        _lbl(ctx, "≈ 60 个地球半径", (ex + mx) / 2, ey - 50, 34, INK, smooth(prog(u, 1.0, 1.6)), "serif_sb")
    x = 1340 + ox
    rows = [("地面：g = 9.8 米/秒²", INK, 1.6, "serif_sb"), ("引力 ∝ 1/距离²", INK, 2.4, "serif_sb"),
            ("预测：9.8 ÷ 60² ≈ 0.0027", RED, 3.2, "serif_sb"),
            ("实测：4π²r / T² ≈ 0.0027", BLU, 4.6, "serif_sb"),
            ("（r = 38.4 万公里，T = 27.3 天）", INK, 5.0, "serif_r")]
    for i, (s, c, t0, w) in enumerate(rows):
        eq(ctx, s, x, 260 + i * 70 + oy, 36 if i < 4 else 26, c, smooth(prog(u, t0, t0 + 0.5)), "l", w)
    fk = smooth(prog(u, 5.8, 6.4))
    eq(ctx, "吻合！", x, 640 + oy, 60, RED, fk, "l", "serif_k")
