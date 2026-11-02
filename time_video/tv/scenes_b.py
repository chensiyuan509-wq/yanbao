"""场景 4–6：测量时间（钟）、感知时间（心理时间与光的延迟）、时空。T 为全局秒数。"""
import math

from .claude import draw_claude, expr_pop, hop, walk_x, wave
from .core import (TAU, H, W, arrow, at, bg_vertical, camera, circle, clamp,
                   dashed, ease_back, ease_in, ease_io, ease_out, ellipse,
                   env, glow, group_alpha, kf, label_pill, lerp, lin, line,
                   pick, prog, rad, rng, rrect, setc, smooth, soft_shadow,
                   star4, text, vignette)
from .props import (Stars, atom, clock, earth, galaxy, moon, pendulum,
                    quartz, space_bg, sun)

INK = "#3B2B26"
ACC = "#E07B53"
GOLD = "#FFC765"
CYAN = "#7FD8FF"


def fmt(n):
    return f"{int(n):,}"


# ======================================================================
# S4 怎么测量时间：数重复 63–80
# ======================================================================
ST = (960, 2560, 4160)


def _clock_cam(T):
    cx = kf(T, [(63.0, 960), (68.9, 960), (70.0, 2560), (71.5, 2560), (72.5, 4160), (76.0, 4160), (77.5, 2560)])
    z = math.exp(kf(T, [(76.0, 0.0), (77.5, math.log(0.42))]))
    cy = kf(T, [(76.0, 540), (77.5, 520)])
    return cx, cy, z


def _w2s(x, y, cam):
    cx, cy, z = cam
    return W / 2 + (x - cx) * z, H / 2 + (y - cy) * z


def station_label(ctx, x, title, rate, a=1.0):
    text(ctx, title, x, 790, 58, INK, a, "black")
    text(ctx, rate, x, 858, 40, ACC, a, "bold")


def s_clocks(ctx, T):
    bg_vertical(ctx, "#F6F0E0", "#E8D2BC", "#F7E6D2", 0.6)
    glow(ctx, W / 2, -100, 900, "#FFFFFF", 0.5)
    cam = _clock_cam(T)
    with camera(ctx, *cam):
        # 地面与点阵（体现镜头移动）
        for gx in range(-400, 5600, 120):
            for gy in range(80, 900, 120):
                setc(ctx, "#C9A88A", 0.25)
                circle(ctx, gx, gy, 3)
                ctx.fill()
        line(ctx, -600, 905, 5800, 905, 3, "#D9B597", 0.8)

        # ---- 1 钟摆
        x = ST[0]
        u = T - 63.0
        ang = 0.36 * math.cos(math.pi * u)
        ctx.set_line_width(3)
        setc(ctx, INK, 0.12)
        ctx.arc(x, 150, 430, math.pi / 2 - 0.36, math.pi / 2 + 0.36)
        ctx.stroke()
        bx, by = pendulum(ctx, x, 150, 430, ang, 1.0, 40)
        k = math.floor(u + 0.0001)
        since = u - k
        if since < 0.45 and k >= 1:
            word = "嘀" if k % 2 else "嗒"
            side = 1 if math.cos(math.pi * k) > 0 else -1
            text(ctx, word, bx + side * 90, by - 40 - since * 60, 48, ACC, 1 - since / 0.45, "black")
        count = max(0, k)
        text(ctx, str(count), x + 420, 380, 170, INK, 1, "black")
        text(ctx, "下 = " + str(count) + " 秒", x + 420, 500, 40, ACC, 1, "bold")
        station_label(ctx, x, "钟摆", "每秒摆 1 次")

        # ---- 2 石英
        x = ST[1]
        a2 = 1.0
        quartz(ctx, x - 230, 690, T, a2, 1.0)
        rrect(ctx, x - 40, 300, 520, 340, 24)
        setc(ctx, "#FFFFFF", 0.6)
        ctx.fill()
        ctx.save()
        rrect(ctx, x - 40, 300, 520, 340, 24)
        ctx.clip()
        ctx.set_line_width(3)
        setc(ctx, "#4F8FE0", 0.9)
        ph = T * 30
        for i in range(0, 1001):
            px = x - 30 + i * 0.5
            py = 568 + math.sin(i * 0.5 * 0.6 + ph) * 52
            if i == 0:
                ctx.move_to(px, py)
            else:
                ctx.line_to(px, py)
        ctx.stroke()
        ctx.restore()
        n2 = max(0.0, T - 69.4) * 32768
        text(ctx, fmt(n2), x + 220, 370, 76, INK, 1, "black")
        text(ctx, "次", x + 220, 440, 32, "#4F8FE0", 1, "bold")
        station_label(ctx, x, "石英晶体（手表里）", "每秒振动 32,768 次")

        # ---- 3 铯原子
        x = ST[2]
        atom(ctx, x - 220, 470, 175, T, 1.0, 1.4)
        rrect(ctx, x - 20, 300, 540, 340, 24)
        setc(ctx, "#18234A", 0.92)
        ctx.fill()
        ctx.save()
        rrect(ctx, x - 20, 300, 540, 340, 24)
        ctx.clip()
        for i in range(140):
            px = x - 10 + i * 3.8
            hgt = 60 + 18 * math.sin(i * 0.9 + T * 50)
            line(ctx, px, 545 - hgt, px, 545 + hgt, 1.6, CYAN, 0.55)
        glow(ctx, x + 250, 545, 260, CYAN, 0.2)
        ctx.restore()
        n3 = 9192631770 * ease_out(prog(T, 72.2, 75.2))
        text(ctx, fmt(n3), x + 250, 368, 62, "#FFFFFF", 1, "black")
        q = ease_back(prog(T, 75.2, 75.7))
        if q > 0:
            label_pill(ctx, "= 精确的 1 秒", x + 250, 440, 34, "#2A1B10", GOLD, q, 0.95)
        station_label(ctx, x, "铯原子钟", "每秒 9,192,631,770 次")

    # 总结（屏幕空间）
    sa = env(T, 77.2, 81, 0.5, 0.3)
    if sa > 0:
        xs = [_w2s(s, 0, cam)[0] for s in ST]
        y = 735
        ctx.set_line_width(4)
        setc(ctx, INK, sa * 0.8)
        ctx.move_to(xs[0] - 140, y - 20)
        ctx.line_to(xs[0] - 140, y)
        ctx.line_to(xs[2] + 140, y)
        ctx.line_to(xs[2] + 140, y - 20)
        ctx.stroke()
        line(ctx, W / 2, y, W / 2, y + 26, 4, INK, sa * 0.8)
        text(ctx, "数满规定的次数 = 1 秒   ·   节奏越快越稳，钟就越准", W / 2, y + 62, 34, INK, sa, "bold")
        label_pill(ctx, "最好的原子钟：上亿年误差不到 1 秒", W / 2, 150, 36, "#2A1B10", GOLD, sa, 0.95)
    expr, since = pick(T, [(0, "think"), (67.2, "curious"), (71.8, "surprised"), (76.2, "proud")])
    bob = math.sin(math.pi * (T - 63)) * 6 if T < 69 else 0
    draw_claude(ctx, 200 + bob, 905, 0.45, expr, T, squash=expr_pop(since), seed=3, look=(6, -4))


# ======================================================================
# S5 感知时间 80–100
# ======================================================================
STARS5 = Stars(500, 13, -100, -100, W + 100, H + 100, 0.4, 2.0)
CONFETTI = [(rng(200 + i).uniform(40, 920), rng(300 + i).uniform(0, 1), rng(400 + i).uniform(0, TAU)) for i in range(26)]


def split_screen(ctx, T):
    # 左：开心
    ctx.save()
    ctx.rectangle(0, 0, W / 2, H)
    ctx.clip()
    ctx.set_source(lin(0, 0, 0, H, [(0, "#FFE8D6"), (1, "#F7B2A0")]))
    ctx.paint()
    glow(ctx, 480, 330, 380, "#FFFFFF", 0.5)
    for i, (cx, ph, rot) in enumerate(CONFETTI):
        y = ((ph + T * 0.25) % 1) * (H + 100) - 50
        star4(ctx, cx + math.sin(T * 2 + i) * 20, y, 10 + (i % 3) * 4, ["#FFD27A", "#FF8A9A", "#8FD3FF"][i % 3], 0.8, T + rot)
    secs = (T - 79.0) * 5400
    for k in range(3):
        ctx.set_line_width(5)
        setc(ctx, ACC, 0.35 - k * 0.1)
        ctx.arc(480, 330, 175 + k * 18, -1.2 + T * 6 + k, -0.2 + T * 6 + k)
        ctx.stroke()
    clock(ctx, 480, 330, 150, secs, accent="#E2483D")
    label_pill(ctx, "开心：时光飞逝", 480, 548, 38, "#FFFFFF", "#E2483D", 1.0, 0.9)
    e, s = pick(T, [(0, "happy"), (81.6, "excited"), (83.0, "happy")])
    jy, jsq = hop(T, 81.6, 50)
    jy2, jsq2 = hop(T, 83.3, 40)
    draw_claude(ctx, 480, 835 + jy + jy2, 0.72, e, T, arm_l=wave(T, 0.9, 0.5), arm_r=wave(T + 0.3, 0.9, 0.5),
                squash=expr_pop(s) + jsq + jsq2)
    ctx.restore()
    # 右：无聊
    ctx.save()
    ctx.rectangle(W / 2, 0, W / 2, H)
    ctx.clip()
    ctx.set_source(lin(0, 0, 0, H, [(0, "#DDE2EC"), (1, "#A9B3C6")]))
    ctx.paint()
    for i in range(18):
        x = 980 + (i * 97) % 940
        y = ((i * 0.37 + T * 0.6) % 1) * H
        line(ctx, x, y, x - 6, y + 26, 2, "#8C98B0", 0.5)
    clock(ctx, 1440, 330, 150, 37 * 60 + (T - 79.0) * 1.5, face="#EEF1F6", accent="#6C7A96")
    label_pill(ctx, "无聊：度日如年", 1440, 548, 38, "#FFFFFF", "#5C6A86", 1.0, 0.9)
    draw_claude(ctx, 1440, 835, 0.72, "tired", T * 0.6, seed=4, squash=0.02 * math.sin(T * 1.2))
    for i in range(3):
        text(ctx, ".", 1580 + i * 26, 600 - i * 6, 60, "#5C6A86", 0.4 + 0.6 * ((T * 1.5 - i * 0.3) % 1), "black")
    ctx.restore()
    ctx.set_source(lin(W / 2 - 8, 0, W / 2 + 8, 0, [(0, "#FFFFFF", 0), (0.5, "#FFFFFF", 0.9), (1, "#FFFFFF", 0)]))
    ctx.rectangle(W / 2 - 8, 0, 16, H)
    ctx.fill()
    label_pill(ctx, "同样的 1 小时", W / 2, 120, 34, "#FFFFFF", "#2A1B4D", 1.0, 0.8)


# 太空部分的世界坐标
EYE = (420 + 0.75 * 90, 820 + 0.75 * (-246 + 68))
OBJ = {
    "flower": (770, 800),
    "moon": (1380, 260),
    "sun": (2800, -760),
    "polaris": (4900, -2300),
    "andromeda": (7900, -4100),
}


def _space_cam(T):
    keys_c = [(84.6, (640, 640)), (88.7, (700, 600)), (89.9, (900, 430)), (90.4, (980, 400)), (91.6, (1650, -40)),
              (92.2, (1800, -120)), (93.5, (2900, -900)), (94.6, (3100, -1000)), (96.6, (4300, -1900)), (100, (4500, -2000))]
    keys_z = [(84.6, 0.0), (88.7, math.log(1.06)), (89.9, math.log(0.78)), (90.4, math.log(0.74)),
              (91.6, math.log(0.36)), (92.2, math.log(0.34)), (93.5, math.log(0.18)), (94.6, math.log(0.17)),
              (96.6, math.log(0.105)), (100, math.log(0.098))]
    cx, cy = kf(T, keys_c)
    z = math.exp(kf(T, keys_z))
    return cx, cy, z


def flower(ctx, x, y, s, t):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    line(ctx, 0, 0, math.sin(t) * 4, -90, 7, "#4FA35A")
    ellipse(ctx, 18, -40, 20, 8)
    setc(ctx, "#5DBB63")
    ctx.fill()
    cx, cy = math.sin(t) * 4, -100
    for k in range(6):
        a = k / 6 * TAU + t * 0.2
        ellipse(ctx, cx + math.cos(a) * 18, cy + math.sin(a) * 18, 15, 15)
        setc(ctx, "#FF8FB0")
        ctx.fill()
    circle(ctx, cx, cy, 13)
    setc(ctx, "#FFD27A")
    ctx.fill()
    ctx.restore()


def light_ray(ctx, p0, p1, T, a=1.0, color=GOLD, n=3, speed=0.7):
    """从 p0（发光物）到 p1（眼睛）的光线，带移动光子。屏幕坐标。"""
    if a <= 0:
        return
    dashed(ctx, p0[0], p0[1], p1[0], p1[1], 2, color, a * 0.6, (10, 10), -T * 40)
    for k in range(n):
        u = (T * speed + k / n) % 1
        x, y = lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u)
        glow(ctx, x, y, 26, color, a * 0.8)
        circle(ctx, x, y, 5)
        setc(ctx, "#FFFFFF", a)
        ctx.fill()


def photo_frame(ctx, x, y, lab, rot, a, seed):
    if a <= 0:
        return
    with at(ctx, x, y, 1.0, rot):
        rrect(ctx, -86, -86, 172, 206, 6)
        setc(ctx, "#FFFFFF", 0.92 * a)
        ctx.fill()
        rrect(ctx, -72, -72, 144, 144, 3)
        setc(ctx, "#0B1030", a)
        ctx.fill()
        r = rng(seed)
        for _ in range(12):
            setc(ctx, "#FFFFFF", a * r.uniform(0.3, 0.9))
            circle(ctx, r.uniform(-65, 65), r.uniform(-65, 65), r.uniform(0.8, 2))
            ctx.fill()
        glow(ctx, 0, 0, 40, "#FFF1D6", a)
        star4(ctx, 0, 0, 16, "#FFFFFF", a)
        text(ctx, lab, 0, 98, 22, "#3B2B26", a, "bold")


def space_journey(ctx, T):
    space_bg(ctx, T, STARS5, neb=0.7, seed=9)
    cam = _space_cam(T)
    cx, cy, z = cam

    def S(p):
        return W / 2 + (p[0] - cx) * z, H / 2 + (p[1] - cy) * z

    with camera(ctx, *cam):
        mx, my = OBJ["moon"]
        moon(ctx, mx, my, 70)
        sx, sy = OBJ["sun"]
        sun(ctx, sx, sy, 280, T)
        earth(ctx, 420, 820 + 1200, 1200, T * 0.3)
        flower(ctx, *OBJ["flower"], 1.0, T)
        e, s = pick(T, [(0, "curious"), (88.8, "surprised"), (91.0, "excited"), (94.6, "proud")])
        draw_claude(ctx, 420, 820, 0.75, e, T, squash=expr_pop(s), look=(8, -6), seed=5)
    # 仙女座星系、北极星：屏幕空间绘制，缩得再小也看得见
    gx, gy = S(OBJ["andromeda"])
    galaxy(ctx, gx, gy, max(1100 * z, 150), T, 1.0, seed=3, tilt=0.4, rot=-0.5)
    px, py = S(OBJ["polaris"])
    glow(ctx, px, py, 70, "#DDE8FF", 0.7)
    star4(ctx, px, py, 34, "#FFFFFF", 1.0, 0.0)
    star4(ctx, px, py, 18, "#FFFFFF", 0.8, math.pi / 4)
    eye = S(EYE)
    rays = [("flower", 85.2, "这朵花 · 约 3 纳秒前", (0, -110)),
            ("moon", 89.4, "月亮 · 1.3 秒前", (0, -95)),
            ("sun", 91.0, "太阳 · 8 分 20 秒前", (0, -120)),
            ("polaris", 92.8, "北极星 · 约 430 年前", (0, -80)),
            ("andromeda", 95.2, "仙女座星系 · 约 250 万年前", (0, -150))]
    for name, t0, lab, off in rays:
        a = env(T, t0, 101, 0.5, 0.3)
        if a <= 0:
            continue
        p0 = S(OBJ[name])
        if name == "flower":
            p0 = (p0[0], p0[1] - 100 * z)
        lab_end = {"flower": 90.4, "moon": 92.6, "sun": 94.8}.get(name, 999)
        fade = 1 - smooth(prog(T, lab_end, lab_end + 0.6))
        light_ray(ctx, p0, eye, T + t0, a * (0.45 + 0.55 * fade), CYAN if name == "andromeda" else GOLD)
        q = ease_back(prog(T, t0 + 0.2, t0 + 0.6))
        lx, ly = p0[0] + off[0], max(p0[1] + off[1], 130)
        label_pill(ctx, lab, lx, ly, 34 if name != "flower" else 30, "#1A1230", GOLD if name != "andromeda" else CYAN, a * q * fade, 0.95)
    # 宇宙相册
    frames = [(330, 300, "约 2,000 年前", -0.12), (1720, 300, "约 4 万年前", 0.1),
              (720, 190, "约 25 万年前", 0.06), (1600, 730, "约 600 年前", -0.08)]
    for i, (x, y, lab, rot) in enumerate(frames):
        a = env(T, 96.6 + i * 0.35, 101, 0.4, 0.3)
        q = ease_back(prog(T, 96.6 + i * 0.35, 97.1 + i * 0.35))
        photo_frame(ctx, x, y + (1 - q) * 40, lab, rot * q, a, i + 40)
    vignette(ctx, 0.45)


def s_perceive(ctx, T):
    if T < 84.4:
        split_screen(ctx, T)
    elif T > 85.4:
        space_journey(ctx, T)
    else:
        u = prog(T, 84.4, 85.4)
        space_journey(ctx, T)
        with group_alpha(ctx, 1 - smooth(u)):
            k = 1 + 0.25 * ease_in(u)
            with at(ctx, W / 2 * (1 - k), H / 2 * (1 - k), k):
                split_screen(ctx, T)


# ======================================================================
# S6 时空 100–118
# ======================================================================


def path_xy(tau):
    return -150 + 22 * tau + 10 * math.sin(1.3 * tau), 120 * math.cos(0.8 * tau) - 30


STAR_XY = (150, -150)
HALF = 280
NFR = 8


def _view(T):
    el = math.radians(kf(T, [(100, 68), (104.2, 68), (105.6, 30), (113.4, 26), (114.8, 0)]))
    yaw = kf(T, [(100, 0.35), (104.2, 0.45), (113.4, 0.78), (114.8, 0.0)])
    ox = kf(T, [(100, 960), (104.2, 960), (113.4, 900), (114.8, 900)])
    oy = kf(T, [(100, 540), (104.2, 560), (105.6, 760), (113.4, 760), (114.8, 820)])
    k = kf(T, [(100, 1.05), (104.2, 1.0), (105.6, 0.85), (113.4, 0.85), (114.8, 1.2)])
    kt = kf(T, [(104.2, 66), (113.4, 66), (114.8, 82)])
    return dict(el=el, yaw=yaw, ox=ox, oy=oy, k=k, kt=kt)


def proj(x, y, tt, v):
    c, s = math.cos(v["yaw"]), math.sin(v["yaw"])
    xr, yr = x * c - y * s, x * s + y * c
    return (v["ox"] + xr * v["k"],
            v["oy"] + yr * v["k"] * math.sin(v["el"]) - tt * v["kt"] * math.cos(v["el"]))


def _frame_tt(i, T):
    t0 = 104.5 + i * 0.42
    if i == 0:
        return 0.0, 1.0
    if T < t0:
        return None, 0.0
    u = ease_out(prog(T, t0, t0 + 0.45))
    return lerp(i - 1, i, u), u


def s_spacetime(ctx, T):
    bg_vertical(ctx, "#0B1130", "#1A2152", "#121A40", 0.6)
    for gx in range(0, W + 1, 60):
        line(ctx, gx, 0, gx, H, 1, "#2B3A78", 0.35)
    for gy in range(0, H + 1, 60):
        line(ctx, 0, gy, W, gy, 1, "#2B3A78", 0.35)
    v = _view(T)
    side = smooth(prog(T, 113.4, 114.8))
    walk_tau = clamp((T - 100.6) * 0.75, 0, 3.0) if T < 104.2 else None

    # 帧（照片）
    fa = 1 - side
    frames_alpha = (1 - 0.55 * smooth(prog(T, 108.6, 109.6))) * fa
    for i in range(NFR):
        tt, u = _frame_tt(i, T)
        if tt is None:
            continue
        corners = [proj(sx * HALF, sy * HALF, tt, v) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        ctx.move_to(*corners[0])
        for c in corners[1:]:
            ctx.line_to(*c)
        ctx.close_path()
        setc(ctx, "#9FC6FF", 0.10 * frames_alpha * u + 0.03 * fa)
        ctx.fill_preserve()
        ctx.set_line_width(2)
        setc(ctx, "#9FC6FF", 0.75 * frames_alpha * u + 0.1 * fa)
        ctx.stroke()
        # 画面中的 Claude 与星星
        tau = i if walk_tau is None else walk_tau
        px, py = proj(*path_xy(tau), tt, v)
        draw_claude(ctx, px, py, 0.17, "neutral" if i < NFR - 1 else "happy", T, shadow=False, blink=False,
                    walk=(tau * 0.8) % 1 if walk_tau is not None and 0 < walk_tau < 3 else None)
        sx, sy = proj(*STAR_XY, tt, v)
        star4(ctx, sx, sy - 14, 14, "#FFE9A8", frames_alpha * u + 0.2 * fa)
        if i == 0 and T < 106:
            a0 = env(T, 100.8, 105.6, 0.5, 0.5)
            e1 = proj(HALF + 60, -HALF, 0, v)
            e0 = proj(-HALF, -HALF, 0, v)
            arrow(ctx, e0[0], e0[1], e1[0], e1[1], 4, CYAN, a0, 22)
            text(ctx, "空间", e1[0] + 50, e1[1], 34, CYAN, a0, "black")
            label_pill(ctx, "一个瞬间的宇宙 = 一张照片", 960, 150, 34, "#FFFFFF", "#2D5E99", a0, 0.85)
        if tt is not None and u > 0 and i > 0 and T < 109:
            cnr = corners[1]
            text(ctx, f"第 {i + 1} 张", cnr[0] + 30, cnr[1], 22, "#CFE0FF", frames_alpha * u * 0.8, "bold", "l")

    # 时间轴
    ta = smooth(prog(T, 104.6, 105.4))
    if ta > 0:
        b0 = proj(-HALF, HALF, 0, v) if side < 1 else proj(-HALF, 0, 0, v)
        b1 = proj(-HALF, HALF, NFR - 0.3, v) if side < 1 else proj(-HALF, 0, NFR - 0.3, v)
        apx = proj(path_xy(0)[0], 0, 0, v)[0]
        bx0 = lerp(b0[0], apx, side)
        bx1 = lerp(b1[0], apx, side)
        arrow(ctx, bx0, b0[1], bx1, b1[1] - 30, 5, GOLD, ta, 26)
        text(ctx, "时间", bx1, b1[1] - 70, 38, GOLD, ta, "black")

    # 世界线
    wa = smooth(prog(T, 108.6, 109.2))
    if wa > 0:
        p = ease_io(prog(T, 108.7, 110.6))
        n = 90
        ctx.new_path()
        for j in range(n + 1):
            tau = (NFR - 1) * p * j / n
            x, y = path_xy(tau)
            if side > 0:
                y = lerp(y, 0, side)
            px, py = proj(x, y, tau, v)
            if j == 0:
                ctx.move_to(px, py)
            else:
                ctx.line_to(px, py)
        ctx.set_line_width(14)
        ctx.set_line_cap(1)
        ctx.set_line_join(1)
        setc(ctx, "#FF9A5C", 0.25 * wa)
        ctx.stroke_preserve()
        ctx.set_line_width(5)
        setc(ctx, "#FFB27A", wa)
        ctx.stroke()
        # 静止星星的世界线
        s0 = proj(STAR_XY[0], lerp(STAR_XY[1], 0, side), 0, v)
        s1 = proj(STAR_XY[0], lerp(STAR_XY[1], 0, side), (NFR - 1) * p, v)
        line(ctx, s0[0], s0[1] - 14, s1[0], s1[1] - 14, 4, "#FFE9A8", wa * 0.8)
        la = env(T, 110.0, 113.6, 0.4, 0.4)
        top = proj(*path_xy(NFR - 1), NFR - 1, v)
        label_pill(ctx, "我的世界线", top[0] - 40, top[1] - 120, 34, "#2A1B10", "#FFB27A", la, 0.95)
        st = proj(STAR_XY[0], STAR_XY[1], NFR - 1, v)
        label_pill(ctx, "静止的星星 → 一条直线", st[0] + 150, st[1] - 70, 28, "#2A1B10", "#FFE9A8", la, 0.9)
        ba = env(T, 110.6, 113.6, 0.4, 0.4)
        label_pill(ctx, "叠起来的“照片” = 时空", 960, 150, 36, "#FFFFFF", "#2D5E99", ba, 0.85)

    # 侧视图：光锥
    if side > 0:
        ox, oy = proj(*path_xy(0), 0, v)
        oy = proj(path_xy(0)[0], 0, 0, v)[1]
        x0, x1 = v["ox"] - HALF * v["k"] - 30, v["ox"] + HALF * v["k"] + 260
        arrow(ctx, x0, oy, x1, oy, 5, CYAN, side, 24)
        text(ctx, "空间", x1 + 10, oy + 44, 34, CYAN, side, "black")
        ca = smooth(prog(T, 114.6, 115.4))
        if ca > 0:
            hgt = 520
            ctx.move_to(ox, oy)
            ctx.line_to(ox - hgt, oy - hgt)
            ctx.line_to(ox + hgt, oy - hgt)
            ctx.close_path()
            ctx.set_source(lin(0, oy, 0, oy - hgt, [(0, GOLD, 0.30 * ca), (1, GOLD, 0.04 * ca)]))
            ctx.fill()
            line(ctx, ox, oy, ox - hgt, oy - hgt, 4, GOLD, ca)
            line(ctx, ox, oy, ox + hgt, oy - hgt, 4, GOLD, ca)
            glow(ctx, ox, oy, 40, GOLD, ca)
            label_pill(ctx, "光锥：光走的路线（45°）", ox - hgt + 170, oy - hgt - 40, 30, "#2A1B10", GOLD, ca, 0.95)
            label_pill(ctx, "我的世界线永远在光锥里", ox + 330, oy - 470, 28, "#2A1B10", "#FFB27A", ca, 0.95)
            fa2 = smooth(prog(T, 115.6, 116.2))
            if fa2 > 0:
                ex, ey = ox + 640, oy - 300
                dashed(ctx, ox, oy, lerp(ox, ex, fa2), lerp(oy, ey, fa2), 4, "#FF5A4E", fa2, (16, 10))
                if fa2 >= 1:
                    label_pill(ctx, "× 超光速：不可能", ex + 20, ey - 40, 30, "#FFFFFF", "#D2453A", 1.0, 0.95)
    expr, since = pick(T, [(0, "curious"), (104.2, "think"), (108.6, "excited"), (113.4, "determined"), (116.0, "proud")])
    draw_claude(ctx, 1720, 900, 0.42, expr, T, squash=expr_pop(since), seed=6, look=(-8, -3), fx=() if expr == "determined" else None)
    vignette(ctx, 0.35)


__all__ = ["s_clocks", "s_perceive", "s_spacetime"]
