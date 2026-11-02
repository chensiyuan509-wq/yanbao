"""场景 7–10：光钟与双生子、质量弯曲时空与 GPS、黑洞、结尾。T 为全局秒数。"""
import math

from .claude import draw_claude, expr_pop, hop, wave
from .core import (STYLE, TAU, H, W, arrow, at, bg_vertical, camera, circle,
                   clamp, dashed, ease_back, ease_in, ease_io, ease_out,
                   ellipse, env, glow, group_alpha, kf, label_pill, lerp, lin,
                   line, pick, prog, rad, rng, rrect, setc, smooth, star4,
                   text, text_reveal, vignette)
from .props import (Stars, black_hole, clock, earth, rocket, satellite,
                    space_bg, sun)
from .scenes_a import planet

INK = "#3B2B26"
ACC = "#E07B53"
GOLD = "#FFC765"
CYAN = "#7FD8FF"

# ======================================================================
# S7 光钟与双生子 118–138
# ======================================================================
C_PX = 480.0          # “光速”，像素/秒
D_MIR = 240.0         # 两面镜子的距离
V_FRAC = 0.8
T_A0, T_B0 = 118.8, 122.8
TRIP_A = 2 * D_MIR / C_PX
TRIP_B = TRIP_A / math.sqrt(1 - V_FRAC ** 2)
STARS7 = Stars(260, 17)


def _tri(u):
    u = u % 1.0
    return 1 - abs(2 * u - 1)          # 0 底 → 1 顶 → 0 底


def mirror(ctx, cx, y, a=1.0):
    glow(ctx, cx, y, 120, "#BFE8FF", 0.2 * a)
    rrect(ctx, cx - 100, y - 9, 200, 18, 9)
    ctx.set_source(lin(cx - 100, 0, cx + 100, 0, [(0, "#9FB3C8", a), (0.5, "#F4FBFF", a), (1, "#9FB3C8", a)]))
    ctx.fill()


def light_clock(ctx, cx, cy, ph, a=1.0, trail=None):
    top, bot = cy - D_MIR / 2, cy + D_MIR / 2
    for sx in (-1, 1):
        line(ctx, cx + sx * 92, top, cx + sx * 92, bot, 3, "#7F93B8", 0.35 * a)
    mirror(ctx, cx, top - 9, a)
    mirror(ctx, cx, bot + 9, a)
    if trail:
        ctx.new_path()
        for i, (x, y) in enumerate(trail):
            if i == 0:
                ctx.move_to(x, y)
            else:
                ctx.line_to(x, y)
        ctx.set_line_width(10)
        setc(ctx, GOLD, 0.18 * a)
        ctx.stroke_preserve()
        ctx.set_line_width(3)
        setc(ctx, GOLD, 0.85 * a)
        ctx.stroke()
    py = bot - _tri(ph) * D_MIR
    glow(ctx, cx, py, 46, "#FFE9A8", 0.9 * a)
    circle(ctx, cx, py, 9)
    setc(ctx, "#FFFFFF", a)
    ctx.fill()
    return py


def ticks(T, t0, trip):
    return max(0, math.floor((T - t0) / trip + 1e-6)) if T >= t0 else 0


def lab_scene(ctx, T):
    bg_vertical(ctx, "#0E1630", "#1C2350", "#151C40", 0.6)
    sp = smooth(prog(T, 122.6, 123.6))       # 0：一只钟居中；1：左右分屏
    # 右侧：飞行的光钟
    if sp > 0:
        ctx.save()
        ctx.rectangle(W / 2, 0, W / 2, H)
        ctx.clip()
        ctx.set_source(lin(0, 0, 0, H, [(0, "#14123A", sp), (1, "#2A1B4D", sp)]))
        ctx.paint()
        for i, (x, y, r, *_rest) in enumerate(STARS7.s):
            xx = W / 2 + ((x - (T - 120) * 420 * (0.4 + r * 0.4)) % (W / 2 + 200)) - 100
            line(ctx, xx, y, xx + 30 * r, y, r, "#FFFFFF", 0.5 * sp)
        cx, cy = 1440, 470
        vpx = V_FRAC * C_PX
        if T >= T_B0:
            pts = []
            for k in range(80):
                tau = T - k * 0.03
                if tau < T_B0:
                    break
                pts.append((cx - (T - tau) * vpx, cy + D_MIR / 2 - _tri((tau - T_B0) / TRIP_B) * D_MIR))
            ph = (T - T_B0) / TRIP_B
        else:
            pts, ph = None, 0.0
        # 飞行平台 + 小 Claude
        rrect(ctx, cx - 150, cy + D_MIR / 2 + 22, 300, 22, 10)
        setc(ctx, "#E07B53", sp)
        ctx.fill()
        fl = 1 + 0.2 * math.sin(T * 40)
        ctx.move_to(cx - 150, cy + D_MIR / 2 + 26)
        ctx.line_to(cx - 150 - 70 * fl, cy + D_MIR / 2 + 33)
        ctx.line_to(cx - 150, cy + D_MIR / 2 + 40)
        setc(ctx, "#FFB347", sp)
        ctx.fill()
        light_clock(ctx, cx, cy, ph, sp, pts)
        draw_claude(ctx, cx + 175, cy + D_MIR / 2 + 22, 0.28, "excited", T, shadow=False, seed=7)
        label_pill(ctx, "高速飞行的光钟  v = 0.8 c", cx, 140, 32, "#1A1230", GOLD, sp, 0.95)
        n = ticks(T, T_B0, TRIP_B)
        label_pill(ctx, f"跳了 {n} 下", cx, 700, 40, "#FFFFFF", "#8E4FD6", sp * smooth(prog(T, 122.8, 123.4)), 0.9)
        ctx.restore()
    # 左侧（或居中）：静止的光钟
    cx = lerp(960, 480, sp)
    cy = 470
    ph = (T - T_A0) / TRIP_A
    light_clock(ctx, cx, cy, ph, 1.0, [(cx, cy - D_MIR / 2), (cx, cy + D_MIR / 2)])
    label_pill(ctx, "静止的光钟", cx, 140, 32, "#1A1230", CYAN, 1.0, 0.95)
    if sp < 1:
        k = ticks(T, T_A0, TRIP_A)
        u = (T - T_A0) / TRIP_A - k
        if k >= 1 and u < 0.6:
            text(ctx, f"嘀 {k}", cx + 180, cy + D_MIR / 2 - u * 80, 54, GOLD, (1 - u / 0.6) * (1 - sp), "black")
        text(ctx, "光往返一次 = 嘀嗒一下", cx, 700, 34, "#CFE0FF", (1 - sp) * env(T, 118.6, 140, 0.5, 0.1), "bold")
    if T >= T_B0:
        n = ticks(T, T_B0, TRIP_A)
        label_pill(ctx, f"跳了 {n} 下", cx, 700, 40, "#FFFFFF", "#2D7FC0", smooth(prog(T, 122.8, 123.4)), 0.9)
    if sp > 0:
        line(ctx, W / 2, 0, W / 2, H, 3, "#FFFFFF", 0.5 * sp)
    # 三角形解释卡
    ca = env(T, 127.4, 131.6, 0.4, 0.3)
    if ca > 0:
        rrect(ctx, 510, 762, 900, 182, 22)
        setc(ctx, "#0B0F24", 0.88 * ca)
        ctx.fill()
        text(ctx, "光速不变  →  路更长  →  每一下更久", 960, 800, 30, "#FFFFFF", ca, "black")
        by = 922
        line(ctx, 600, by, 600, by - 85, 5, CYAN, ca)
        text(ctx, "静止：直上直下", 626, by - 42, 26, CYAN, ca, "bold", "l")
        line(ctx, 900, by, 1030, by - 85, 5, GOLD, ca)
        line(ctx, 1030, by - 85, 1160, by, 5, GOLD, ca)
        dashed(ctx, 900, by + 4, 1160, by + 4, 2, "#FFFFFF", ca * 0.6, (8, 8))
        text(ctx, "飞行：斜线更长", 1180, by - 42, 26, GOLD, ca, "bold", "l")
    ba = env(T, 127.6, 131.6, 0.4, 0.3)
    if ba > 0:
        q = ease_back(prog(T, 127.6, 128.1))
        rrect(ctx, 960 - 330 * q, 230, 660 * q, 80, 40)
        setc(ctx, GOLD, 0.95 * ba)
        ctx.fill()
        text(ctx, "跑得越快 → 时间走得越慢", 960, 270, 40, "#2A1B10", ba * q, "black")
    expr, since = pick(T, [(0, "curious"), (122.6, "surprised"), (124.6, "think"), (127.4, "determined"), (129.8, "proud")])
    draw_claude(ctx, 230, 905, 0.42, expr, T, squash=expr_pop(since), seed=8, look=(8, -5),
                fx=() if expr == "determined" else None)


EARTH_C, EARTH_R = (360, 800), 230
STAR_T = (1640, 330)


def _rocket_pos(u):
    """u: 0→1 往返。返回位置与朝向角。"""
    p0 = (EARTH_C[0] + 200, EARTH_C[1] - 260)
    p1 = (STAR_T[0] - 140, STAR_T[1] + 30)
    if u < 0.5:
        k = ease_io(u / 0.5)
        x, y = lerp(p0[0], p1[0], k), lerp(p0[1], p1[1], k) - math.sin(k * math.pi) * 120
        ang = math.atan2(p1[1] - p0[1] - math.cos(k * math.pi) * 120 * math.pi, p1[0] - p0[0])
    else:
        k = ease_io((u - 0.5) / 0.5)
        x, y = lerp(p1[0], p0[0], k), lerp(p1[1], p0[1], k) + math.sin(k * math.pi) * 120
        ang = math.atan2(p0[1] - p1[1] + math.cos(k * math.pi) * 120 * math.pi, p0[0] - p1[0])
    return x, y, ang


def _on_earth(ctx, ang, expr, T, seed, s=0.4, **kw):
    with at(ctx, EARTH_C[0], EARTH_C[1], 1.0, ang):
        draw_claude(ctx, 0, -EARTH_R + 4, s, expr, T, seed=seed, **kw)


def twins_scene(ctx, T):
    space_bg(ctx, T, STARS7, neb=0.8, seed=12)
    glow(ctx, *STAR_T, 160, "#BFD8FF", 0.4)
    star4(ctx, *STAR_T, 40, "#FFFFFF", 1.0, T * 0.3)
    text(ctx, "遥远的恒星", STAR_T[0], STAR_T[1] + 80, 28, "#CFE0FF", 0.9, "bold")
    earth(ctx, EARTH_C[0], EARTH_C[1], EARTH_R, T)
    u = prog(T, 131.9, 136.8)
    years_e = 10 * u
    years_s = 5 * u
    # 地球上的双胞胎
    e_expr = "curious" if u < 0.55 else ("tired" if u >= 1 else "neutral")
    _on_earth(ctx, -0.34, e_expr, T, 9, look=(8, -6))
    if u >= 1:
        qa = smooth(prog(T, 136.9, 137.3))
        label_pill(ctx, "老了 10 岁", EARTH_C[0] - 150, EARTH_C[1] - EARTH_R - 170, 26, "#1A1230", CYAN, qa, 0.95)
        label_pill(ctx, "只老了 5 岁", EARTH_C[0] + 190, EARTH_C[1] - EARTH_R - 170, 26, "#1A1230", GOLD, qa, 0.95)
    # 火箭
    if 0 < u < 1:
        x, y, ang = _rocket_pos(u)
        n = 24
        ctx.new_path()
        for i in range(n + 1):
            uu = max(0.0, u - i * 0.012)
            px, py, _ = _rocket_pos(uu)
            if i == 0:
                ctx.move_to(px, py)
            else:
                ctx.line_to(px, py)
        ctx.set_line_width(6)
        setc(ctx, GOLD, 0.35)
        ctx.stroke()
        rocket(ctx, x, y, 0.8, ang, T)
        label_pill(ctx, "0.87 倍光速", x, y - 80, 26, "#1A1230", GOLD, 0.95, 0.95)
    elif u >= 1:
        q = ease_back(prog(T, 136.8, 137.2))
        _on_earth(ctx, 0.38, "excited", T, 10, 0.4 * q)
    else:
        rocket(ctx, EARTH_C[0] + 200, EARTH_C[1] - 260, 0.8, -0.3, T, flame=False)
    # 计时卡
    ca = env(T, 131.7, 140, 0.4, 0.2)
    for cx, title, yrs, col in [(1090, "地球上的双胞胎", years_e, CYAN), (1540, "飞船上的我", years_s, GOLD)]:
        rrect(ctx, cx - 200, 600, 400, 180, 24)
        setc(ctx, "#0B0F24", 0.75 * ca)
        ctx.fill_preserve()
        ctx.set_line_width(3)
        setc(ctx, col, 0.8 * ca)
        ctx.stroke()
        text(ctx, title, cx, 640, 30, col, ca, "bold")
        text(ctx, f"{yrs:.1f} 年", cx, 720, 76, "#FFFFFF", ca, "black")
    if u >= 1:
        text(ctx, "重逢时，我比双胞胎年轻了 5 岁", 1315, 860, 34, GOLD, smooth(prog(T, 137.0, 137.4)), "black")


def s_lightclock(ctx, T):
    if T < 131.3:
        lab_scene(ctx, T)
    elif T > 132.0:
        twins_scene(ctx, T)
    else:
        u = smooth(prog(T, 131.3, 132.0))
        twins_scene(ctx, T)
        with group_alpha(ctx, 1 - u):
            lab_scene(ctx, T)


# ======================================================================
# S8 质量弯曲时空 + GPS 138–155
# ======================================================================
STARS8 = Stars(300, 23)


def well_y(r, depth):
    return -depth / math.sqrt(1 + (r / 1.7) ** 2)


def P3(X, Y, Z, cam):
    yaw, el, dist, f, cx, cy = cam
    x1 = X * math.cos(yaw) - Z * math.sin(yaw)
    z1 = X * math.sin(yaw) + Z * math.cos(yaw)
    y2 = Y * math.cos(el) + z1 * math.sin(el)
    z2 = -Y * math.sin(el) + z1 * math.cos(el) + dist
    return cx + f * x1 / z2, cy - f * y2 / z2, z2


def _depth(T):
    if T < 141.1:
        return 0.0
    u = prog(T, 141.1, 142.3)
    return 4.4 * (1 + 0.12 * math.sin(u * 12) * (1 - u)) * ease_out(u)


def grid_scene(ctx, T, a=1.0):
    space_bg(ctx, T, STARS8, neb=0.7, seed=4)
    dist = kf(T, [(138, 21), (146.2, 22.5), (147.4, 34)])
    cam = (kf(T, [(138, -0.15), (147, 0.25)], ease_io), 0.5, dist, 980, 960, 470)
    depth = _depth(T)
    L, step = 10, 1.0
    for axis in (0, 1):
        for i in range(int(-L / step), int(L / step) + 1):
            c = i * step
            ctx.new_path()
            first = True
            n = 80
            for j in range(n + 1):
                s = -L + 2 * L * j / n
                X, Z = (c, s) if axis == 0 else (s, c)
                r = math.hypot(X, Z)
                sx, sy, _ = P3(X, well_y(r, depth), Z, cam)
                if first:
                    ctx.move_to(sx, sy)
                    first = False
                else:
                    ctx.line_to(sx, sy)
            edge = 1 - abs(c) / (L + 1)
            ctx.set_line_width(1.6)
            setc(ctx, "#7FD8FF", (0.25 + 0.45 * edge) * a)
            ctx.stroke()
    # 深处的蓝紫色光
    cxp, cyp, _ = P3(0, well_y(0, depth), 0, cam)
    glow(ctx, cxp, cyp, 260, "#8E6BFF", 0.3 * a * depth / 4.4)
    # 行星落下
    R = 1.35
    yr = kf(T, [(139.4, 9.0), (141.15, well_y(0, 4.4) + R)], ease_in)
    if T > 141.15:
        yr = well_y(0, depth) + R
    px, py, pz = P3(0, yr, 0, cam)
    pr = 980 * R / pz
    if T > 139.4:
        earth(ctx, px, py, pr, T, a)
    # 两个时钟
    ca = env(T, 142.4, 147.0, 0.5, 0.6) * a
    if ca > 0:
        for (X, Z, rate, lab, col) in [(7.2, -1.5, 1.0, "离得远：走得快", CYAN), (2.3, 0.4, 0.33, "离得近：走得慢", "#B49BFF")]:
            r = math.hypot(X, Z)
            sx, sy, _ = P3(X, well_y(r, depth), Z, cam)
            line(ctx, sx, sy, sx, sy - 80, 3, col, ca)
            circle(ctx, sx, sy, 6)
            setc(ctx, col, ca)
            ctx.fill()
            clock(ctx, sx, sy - 140, 58, (T - 142.4) * 1700 * rate, a=ca, accent=ACC, glow_c=col)
            label_pill(ctx, lab, sx, sy - 228, 28, "#1A1230", col, ca, 0.95)
    la = env(T, 141.6, 147.0, 0.5, 0.5) * a
    label_pill(ctx, "质量把时空“压”出一个坑", 960, 140, 34, "#FFFFFF", "#4B3A9A", la, 0.85)


GPS_E = (620, 560)


def gps_scene(ctx, T, a=1.0):
    space_bg(ctx, T, STARS8, neb=0.6, seed=4)
    ex, ey = GPS_E
    er = 205
    ang = (T - 146) * 0.9
    rx, ry, tilt = 420, 140, -0.18

    def orbit_pt(t):
        x, y = math.cos(t) * rx, math.sin(t) * ry
        return ex + x * math.cos(tilt) - y * math.sin(tilt), ey + x * math.sin(tilt) + y * math.cos(tilt)

    def orbit_half(front):
        ctx.new_path()
        rng_ = (0, math.pi) if front else (math.pi, TAU)
        for k in range(61):
            t = lerp(rng_[0], rng_[1], k / 60)
            x, y = orbit_pt(t)
            if k == 0:
                ctx.move_to(x, y)
            else:
                ctx.line_to(x, y)
        ctx.set_line_width(2.5)
        setc(ctx, GOLD, 0.55 * a)
        ctx.set_dash((10, 8))
        ctx.stroke()
        ctx.set_dash(())

    sat_front = math.sin(ang) > 0
    orbit_half(False)
    sx, sy = orbit_pt(ang)
    if not sat_front:
        satellite(ctx, sx, sy, 0.9, 0.2, a)
    earth(ctx, ex, ey, er, T, a)
    orbit_half(True)
    if sat_front:
        satellite(ctx, sx, sy, 0.9, 0.2, a)
    clock(ctx, sx, sy - 70, 30, (T - 146) * 900 * 1.0, a=a, accent=ACC, show_sec=True)
    gx, gy = ex, ey - er
    clock(ctx, gx, gy - 46, 28, (T - 146) * 900 * 0.995, a=a, accent="#4F8FE0")
    text(ctx, "地面", gx, gy - 92, 22, "#FFFFFF", a * 0.9, "bold")
    # 右侧：账本
    q1 = ease_back(prog(T, 147.2, 147.6))
    q2 = ease_back(prog(T, 147.9, 148.3))
    q3 = ease_back(prog(T, 148.7, 149.2))
    bx = 1180
    label_pill(ctx, "卫星上的钟，每天：", bx, 200, 32, "#FFFFFF", "#2A1B4D", a * q1, 0.0, align="l")
    label_pill(ctx, "+45 微秒   离地球远，引力弱 → 走得快", bx, 270, 28, "#1A1230", CYAN, a * q2, 0.95, align="l")
    label_pill(ctx, "−7 微秒   飞得快 → 走得慢", bx, 335, 28, "#1A1230", "#B49BFF", a * q2, 0.95, align="l")
    if q3 > 0:
        line(ctx, bx, 378, bx + 560, 378, 2, "#FFFFFF", 0.6 * a * q3)
        label_pill(ctx, "= 每天快 38 微秒", bx, 430, 40, "#2A1B10", GOLD, a * q3, 0.95, align="l")
    # 地图卡片：误差累积
    ma = env(T, 151.0, 160, 0.4, 0.1) * a
    if ma > 0:
        mx, my, mw, mh = 1180, 520, 600, 330
        rrect(ctx, mx, my, mw, mh, 22)
        setc(ctx, "#F4EEDF", ma)
        ctx.fill()
        ctx.save()
        rrect(ctx, mx, my, mw, mh, 22)
        ctx.clip()
        for k in range(8):
            line(ctx, mx + k * 85 + 20, my, mx + k * 85 - 40, my + mh, 10, "#FFFFFF", ma)
            line(ctx, mx, my + k * 52 + 10, mx + mw, my + k * 52 + 30, 8, "#FFFFFF", ma)
        ellipse(ctx, mx + 470, my + 90, 90, 50)
        setc(ctx, "#BFE3A8", ma)
        ctx.fill()
        ctx.restore()
        tx, ty = mx + 150, my + 200
        circle(ctx, tx, ty, 12)
        setc(ctx, "#2E8A47", ma)
        ctx.fill()
        text(ctx, "你在这里", tx, ty + 34, 22, "#2E8A47", ma, "bold")
        d = ease_io(prog(T, 151.6, 153.4))
        gx2, gy2 = lerp(tx, mx + 470, d), lerp(ty, my + 120, d)
        dashed(ctx, tx, ty, gx2, gy2, 3, "#D2453A", ma * d, (10, 8))
        ctx.move_to(gx2, gy2)
        ctx.arc(gx2, gy2 - 30, 18, math.pi * 0.75, math.pi * 2.25)
        ctx.close_path()
        setc(ctx, "#E2483D", ma)
        ctx.fill()
        circle(ctx, gx2, gy2 - 30, 7)
        setc(ctx, "#FFFFFF", ma)
        ctx.fill()
        if d > 0.6:
            label_pill(ctx, "导航以为你在这", gx2, gy2 - 76, 22, "#FFFFFF", "#E2483D", ma * smooth(prog(d, 0.6, 1)), 0.95)
        label_pill(ctx, "一天后：偏差约 10 公里", mx + mw / 2, my + mh - 34, 28, "#FFFFFF", "#2A1B4D", ma * smooth(prog(T, 153.0, 153.5)), 0.9)
    text(ctx, "GPS 卫星", sx, sy + 56, 24, GOLD, a, "bold")


def s_gravity(ctx, T):
    if T < 146.4:
        grid_scene(ctx, T)
    elif T > 147.4:
        gps_scene(ctx, T)
    else:
        u = smooth(prog(T, 146.4, 147.4))
        grid_scene(ctx, T)
        with group_alpha(ctx, u):
            gps_scene(ctx, T)
    expr, since = pick(T, [(0, "curious"), (141.2, "surprised"), (142.6, "think"), (146.8, "curious"),
                           (151.2, "surprised"), (153.4, "determined")])
    draw_claude(ctx, 190, 905, 0.42, expr, T, squash=expr_pop(since), seed=11, look=(8, -5),
                fx=() if expr == "determined" else None)
    vignette(ctx, 0.35)


# ======================================================================
# S9 黑洞 155–165
# ======================================================================
STARS9 = Stars(520, 29, -300, -300, W + 300, H + 300, 0.4, 1.8)
BH = (1180, 470)
BH_R = 118


def _approach(T):
    s = max(0.0, T - 155.0)
    u = 1 - math.exp(-s / 2.4)
    tau = 155.0 + 2.4 * u          # Claude 自己的时间：越来越慢，最终几乎停住
    return u, tau


def s_blackhole(ctx, T):
    bg_vertical(ctx, "#020208", "#0A0818", "#06050F", 0.6)
    zoom = kf(T, [(154.4, 0.82), (165.6, 1.12)])
    rot = kf(T, [(154.4, -0.05), (165.6, 0.04)])
    with camera(ctx, 1080, 500, zoom, rot):
        # 被引力“拉弯”的星光
        for x, y, r, ph, b, c, sp in STARS9.s:
            dx, dy = x - BH[0], y - BH[1]
            d = math.hypot(dx, dy) + 1e-3
            push = 9000 / d
            px, py = x + dx / d * push, y + dy / d * push
            setc(ctx, c, b * (0.6 + 0.4 * math.sin(T * sp + ph)))
            circle(ctx, px, py, r)
            ctx.fill()
        # 时间流速圈
        ra = env(T, 156.8, 170, 0.6, 0.1)
        for k, (mul, lab) in enumerate([(4.4, "时间流速 90%"), (2.7, "60%"), (1.7, "20%")]):
            ctx.set_line_width(2)
            ctx.set_dash((8, 10), T * 10)
            setc(ctx, "#B49BFF", ra * (0.35 + k * 0.15))
            circle(ctx, BH[0], BH[1], BH_R * mul)
            ctx.stroke()
            ctx.set_dash(())
            text(ctx, lab, BH[0] + BH_R * mul * 0.71 + 10, BH[1] - BH_R * mul * 0.71 - 10, 24, "#CFC2FF", ra, "bold", "l")
        black_hole(ctx, BH[0], BH[1], BH_R, T)
        # Claude 坠向黑洞
        u, tau = _approach(T)
        cx = lerp(380, BH[0] - BH_R * 1.95, u)
        cy = lerp(640, BH[1] + 40, u)
        s = lerp(0.42, 0.26, u)
        STYLE.update(tint="#FF4A2A", tint_amt=0.85 * u ** 1.5, bright=1 - 0.55 * u ** 2)
        e, since = pick(tau, [(0, "curious"), (155.9, "surprised")])
        glow(ctx, cx, cy - 120 * s, 260 * s, "#BFE8FF", 0.25)
        draw_claude(ctx, cx, cy, s, e, tau, squash=expr_pop(since), seed=12, look=(8, 0),
                    arm_r=wave(tau, 0.9, 0.4) * env(tau, 155.0, 156.4, 0.2, 0.2), shadow=False)
        clock(ctx, cx, cy - 330 * s - 70, 52, (tau - 155) * 1800, a=1.0, accent=ACC)
        STYLE.update(tint=None, tint_amt=0.0, bright=1.0)
        ctx.arc(cx, cy - 120 * s, 230 * s, 0, TAU)
        ctx.set_line_width(3)
        setc(ctx, "#DFF4FF", 0.4)
        ctx.stroke()
        ha = env(T, 156.4, 166, 0.5, 0.1)
        if ha > 0:
            hx, hy = BH[0] + BH_R * 0.8, BH[1] + BH_R * 0.62
            line(ctx, hx, hy, hx + 120, hy + 170, 2.5, "#FFE6A8", ha)
            label_pill(ctx, "事件视界：连光都逃不出", hx + 130, hy + 200, 28, "#1A1230", "#FFE6A8", ha, 0.95)
        ca = env(T, 159.4, 166, 0.5, 0.1)
        if ca > 0:
            label_pill(ctx, "我的钟：几乎停住", cx, cy - 330 * s - 160, 26, "#FFFFFF", "#C2412F", ca, 0.9)
    # 远处的时钟（屏幕空间）
    fa = env(T, 157.2, 166, 0.5, 0.1)
    if fa > 0:
        rrect(ctx, 54, 120, 290, 290, 26)
        setc(ctx, "#0E1230", 0.8 * fa)
        ctx.fill()
        clock(ctx, 199, 245, 88, (T - 155) * 1800, a=fa, accent="#4F8FE0", glow_c="#7FD8FF")
        text(ctx, "远处的时钟：照常走", 199, 375, 26, CYAN, fa, "bold")
    vignette(ctx, 0.55)


# ======================================================================
# S10 结尾 165–180
# ======================================================================
STARS10 = Stars(360, 31, -100, -100, W + 100, 760)


def fabric(ctx, T, a):
    if a <= 0:
        return
    for i in range(15):
        ctx.new_path()
        for j in range(61):
            x = -100 + j * (W + 200) / 60
            y0 = 90 + i * 34
            d = math.sin(x * 0.006 + T * 1.6 + i * 0.3) * 14
            pull = 60 * math.exp(-((x - 960) ** 2) / 90000 - ((y0 - 330) ** 2) / 30000)
            y = y0 + d + pull
            if j == 0:
                ctx.move_to(x, y)
            else:
                ctx.line_to(x, y)
        ctx.set_line_width(1.6)
        setc(ctx, "#FFE2B8", a * 0.45)
        ctx.stroke()
    for j in range(25):
        ctx.new_path()
        x0 = -100 + j * (W + 200) / 24
        for i in range(31):
            y = 90 + i * 15.6
            x = x0 + math.sin(y * 0.01 + T * 1.3 + j * 0.25) * 16
            pull = 60 * math.exp(-((x - 960) ** 2) / 90000 - ((y - 330) ** 2) / 30000)
            if i == 0:
                ctx.move_to(x, y + pull)
            else:
                ctx.line_to(x, y + pull)
        ctx.set_line_width(1.6)
        setc(ctx, "#FFE2B8", a * 0.45)
        ctx.stroke()


def s_ending(ctx, T):
    bg_vertical(ctx, "#1B1640", "#FFC995", "#E98A6A", 0.72)
    STARS10.draw(ctx, T, 1 - 0.7 * prog(T, 165, 176))
    sy = lerp(980, 770, ease_out(prog(T, 165, 176)))
    sun(ctx, 1380, sy, 95, T)
    fa = env(T, 169.4, 174.2, 0.8, 0.8)
    fabric(ctx, T, fa)
    if fa > 0:
        for word, x, y, t0 in [("伸缩", 560, 260, 170.0), ("弯曲", 1360, 230, 171.0)]:
            q = ease_back(prog(T, t0, t0 + 0.5))
            text(ctx, word, x, y, 64, "#FFFFFF", fa * q, "black", outline="#B4583A", outline_w=8)
    planet(ctx, 960, 830, 2600, 1.0, warm=1.0)
    expr, since = pick(T, [(0, "proud"), (169.6, "happy"), (173.8, "excited"), (176.8, "happy"), (178.6, "proud")])
    arms = env(T, 169.6, 173.4, 0.4, 0.4)
    wv = env(T, 176.8, 179.4, 0.3, 0.3)
    jy, jsq = hop(T, 173.9, 50)
    draw_claude(ctx, 960, 830 + jy, 0.95, expr, T, squash=expr_pop(since) + jsq, seed=13,
                arm_l=0.7 * arms, arm_r=0.7 * arms + wave(T, 0.9, 0.5) * wv, look=(0, -4))
    # 你刚刚度过的时间
    ta = env(T, 173.8, 176.7, 0.4, 0.4)
    if ta > 0:
        mm, ss = int(T // 60), int(T % 60)
        text(ctx, f"{mm:02d}:{ss:02d}", 960, 290, 150, "#FFFFFF", ta, "black", outline="#8A4A6E", outline_w=10)
        text(ctx, "你刚刚和我一起度过的时间", 960, 410, 36, "#FFF1DC", ta, "bold")
    ea = env(T, 176.8, 182, 0.6, 0.1)
    if ea > 0:
        glow(ctx, 960, 290, 520, "#FFE2B8", 0.25 * ea)
        text_reveal(ctx, "看见时间", 960, 280, 140, "#FFFFFF", prog(T, 176.9, 178.0), "black",
                    outline="#8A4A6E", outline_w=10)
        text(ctx, "Claude 的宇宙时间课 · 完", 960, 410, 38, "#FFF1DC", env(T, 177.6, 182, 0.6, 0.1), "bold", spacing=0.1)
    vignette(ctx, 0.35)


__all__ = ["s_lightclock", "s_gravity", "s_blackhole", "s_ending"]
