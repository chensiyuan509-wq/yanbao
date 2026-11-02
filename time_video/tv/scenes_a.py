"""场景 0–3：开场、什么是时间、宇宙日历、时间之箭。函数参数 T 为全局秒数。"""
import math

from .claude import draw_claude, expr_pop, hop, walk_x, wave
from .core import (STYLE, TAU, H, W, arrow, at, bg_vertical, camera, circle,
                   clamp, dashed, ease_back, ease_in, ease_io, ease_out,
                   ellipse, env, glow, group_alpha, kf, label_pill, lerp, lin,
                   line, pick, prog, rad, rng, rrect, setc, smooth,
                   soft_shadow, star4, text, text_reveal, vignette)
from .props import (Stars, big_bang, candle, clock, clock_ring, cup, dino,
                    earth, galaxy, human, leaf, space_bg, sun, tree)

INK = "#3B2B26"
ACC = "#E07B53"
GOLD = "#FFC765"


def warm_bg(ctx, t=0.0, horizon=790):
    bg_vertical(ctx, "#EDEAD0", "#E6B79E", "#FFE3C6", 0.62)
    glow(ctx, W * 0.5, -120, 900, "#FFF8DC", 0.55)
    # 远山
    for i, (cx, r, c) in enumerate([(300, 520, "#F3CDB0"), (1000, 640, "#EFC2A3"), (1700, 560, "#F3CDB0")]):
        ellipse(ctx, cx, horizon + 40, r, 150)
        setc(ctx, c, 0.65)
        ctx.fill()
    ctx.rectangle(0, horizon, W, H - horizon)
    ctx.set_source(lin(0, horizon, 0, H, [(0, "#F1C7A6"), (1, "#DDA185")]))
    ctx.fill()
    line(ctx, 0, horizon, W, horizon, 2, "#FFF1DC", 0.6)


def planet(ctx, cx, top, R, a=1.0, warm=0.0):
    cy = top + R
    glow(ctx, cx, top, 900, "#8C78E8" if warm < 0.5 else "#FFB27A", 0.18 * a)
    circle(ctx, cx, cy, R)
    c0 = "#4A3A78" if warm < 0.5 else "#6A4A6E"
    ctx.set_source(rad(cx, top + 200, 50, 1400, [(0, c0, a), (1, "#140F28", a)]))
    ctx.fill()
    ctx.set_line_width(5)
    ctx.set_source(lin(cx - 1400, 0, cx + 1400, 0, [(0, "#B7A4FF", 0), (0.5, "#D8CCFF" if warm < 0.5 else "#FFD7A8", 0.85 * a), (1, "#B7A4FF", 0)]))
    ctx.arc(cx, cy, R, math.pi * 1.2, math.pi * 1.8)
    ctx.stroke()
    r = rng(4)
    for i in range(10):
        dx = r.uniform(-1300, 1300)
        yy = cy - math.sqrt(max(R * R - dx * dx, 0)) + r.uniform(25, 120)
        ellipse(ctx, cx + dx, yy, r.uniform(30, 90), r.uniform(6, 14))
        setc(ctx, "#2A2050", 0.5 * a)
        ctx.fill()


# ======================================================================
# S0 开场 0–12
# ======================================================================
STARS0 = Stars(420, 1, -600, -800, W + 600, H + 300)
GHOSTS = [(330, 300, 70), (1600, 250, 92), (650, 150, 48), (1330, 470, 52), (190, 600, 44), (1760, 590, 60)]


def ghost_clock(ctx, x, y, r, t, a, speed=1.0):
    if a <= 0.01:
        return
    glow(ctx, x, y, r * 1.6, "#9FB8FF", 0.12 * a)
    ctx.set_line_width(2.5)
    setc(ctx, "#CFE0FF", 0.7 * a)
    circle(ctx, x, y, r)
    ctx.stroke()
    for i in range(12):
        ang = i / 12 * TAU
        line(ctx, x + math.cos(ang) * r * 0.82, y + math.sin(ang) * r * 0.82,
             x + math.cos(ang) * r * 0.95, y + math.sin(ang) * r * 0.95, 2, "#CFE0FF", 0.6 * a)
    m = t * speed * 2.0 - math.pi / 2
    h = t * speed * 0.17 - math.pi / 2
    line(ctx, x, y, x + math.cos(m) * r * 0.75, y + math.sin(m) * r * 0.75, 3, "#E8F0FF", 0.8 * a)
    line(ctx, x, y, x + math.cos(h) * r * 0.5, y + math.sin(h) * r * 0.5, 4, "#E8F0FF", 0.8 * a)


def s_opening(ctx, T):
    t = T
    space_bg(ctx, t, None)
    cy = kf(t, [(0, 120), (4.6, 540)])
    zoom = kf(t, [(0, 1.3), (4.6, 1.0), (12.5, 1.06)])
    with camera(ctx, 960, cy, zoom):
        STARS0.draw(ctx, t)
        p = prog(t, 1.4, 2.3)
        if 0 < p < 1:
            x, y = lerp(1700, 900, p), lerp(-420, -60, p)
            ctx.set_line_width(3)
            ctx.set_source(lin(x, y, x + 260, y - 120, [(0, "#FFFFFF", 0.9), (1, "#FFFFFF", 0)]))
            ctx.move_to(x, y)
            ctx.line_to(x + 260, y - 120)
            ctx.stroke()
            glow(ctx, x, y, 22, "#FFFFFF", 0.9)
        for i, (gx, gy, gr) in enumerate(GHOSTS):
            a = env(t, 4.5 + i * 0.32, 9.0, 0.7, 0.8) * 0.75
            ghost_clock(ctx, gx, gy + math.sin(t * 0.8 + i) * 8, gr, t + i * 3, a, 1 + i * 0.4)
        planet(ctx, 960, 830, 2600)
        x, ph = walk_x(t, 0.5, 4.0, -260, 960)
        expr, since = pick(t, [(0, "neutral"), (4.2, "happy"), (6.3, "curious"), (8.7, "excited")])
        arm_r = wave(t) * env(t, 4.2, 6.1, 0.25, 0.3)
        lx = kf(t, [(6.3, 0), (6.9, -7), (7.7, 7), (8.5, 0)]) if expr == "curious" else 0
        jy, jsq = hop(t, 8.75, 46)
        draw_claude(ctx, x, 830 + jy, 1.0, expr, t, walk=ph, arm_r=arm_r,
                    look=(lx, -5 if expr == "curious" else 0), squash=expr_pop(since) + jsq)
    # 标题
    pa = env(t, 8.7, 13.0, 0.6, 0.5)
    if pa > 0:
        glow(ctx, 960, 290, 520, "#FFB86B", 0.20 * pa)
        clock_ring(ctx, 960, 290, 230 * ease_out(prog(t, 8.6, 9.8)), t * 1.5, pa)
        text_reveal(ctx, "时间是什么？", 960, 282, 132, "#FFFFFF", prog(t, 8.75, 9.9),
                    "black", outline="#2A1B4D", outline_w=10)
        text(ctx, "跟着 Claude，看见看不见的时间", 960, 400, 38, "#FFD2A6",
             env(t, 9.6, 13, 0.6, 0.4), "medium", spacing=0.08)
    vignette(ctx, 0.5)


# ======================================================================
# S1 什么是时间 12–30
# ======================================================================
FREEZE_END = 20.4


def _leaf_specs():
    r = rng(21)
    out = [(18.85, 1470, 470, 0.9)]  # 这片叶子在“冻结”时悬在半空
    for i in range(16):
        out.append((r.uniform(20.6, 29.5), 1530 + r.uniform(-160, 160), 790 - r.uniform(260, 400), r.uniform(0.7, 1.1)))
    return out


LEAVES = _leaf_specs()
DUST = [(rng(31 + i).uniform(100, 1820), rng(61 + i).uniform(200, 760), rng(91 + i).uniform(1.5, 4)) for i in range(40)]


def mini_scene(ctx, x, y, w, h, a):
    """“之前/之后”卡片里的小场景（完全一样）。"""
    rrect(ctx, x - w / 2, y - h / 2, w, h, 16)
    setc(ctx, "#FFFFFF", 0.95 * a)
    ctx.fill()
    ctx.save()
    rrect(ctx, x - w / 2 + 10, y - h / 2 + 10, w - 20, h - 20, 10)
    ctx.clip()
    ctx.set_source(lin(0, y - h / 2, 0, y + h / 2, [(0, "#EDEAD0", a), (1, "#F1C7A6", a)]))
    ctx.paint()
    s = h / 900
    with at(ctx, x - w / 2, y - h / 2 + 30, s):
        candle(ctx, 430 * w / h * 0.55, 790, 160, 0, True, a, flicker=False)
        draw_claude(ctx, 960 * w / h * 0.55, 790, 0.85, "neutral", 20.4, walk=0.25, blink=False)
    ctx.restore()


def s_change(ctx, T):
    un = smooth(prog(T, FREEZE_END, FREEZE_END + 0.9))
    STYLE["desat"] = (1 - un) * 0.9
    tm = max(T, FREEZE_END)
    warm_bg(ctx, tm)
    # 太阳
    sx = lerp(230, 760, prog(tm, 20.4, 30.5))
    sy = lerp(560, 380, ease_out(prog(tm, 20.4, 30.5)))
    sun(ctx, sx, sy, 62, tm)
    # 灰尘
    for i, (dx, dy, r) in enumerate(DUST):
        px = dx + (tm - FREEZE_END) * 14 + math.sin(tm * 0.7 + i) * 10
        py = dy + math.sin(tm * 0.5 + i * 1.3) * 16
        setc(ctx, "#FFFFFF", 0.55)
        circle(ctx, (px % 1960) - 20, py, r)
        ctx.fill()
    tree(ctx, 1530, 790, tm)
    for i, (t0, lx, ly, s) in enumerate(LEAVES):
        if tm < t0:
            continue
        u = tm - t0
        fall = min(u * 95, 790 - ly - 6)
        px = lx + math.sin(u * 2.2 + i) * 40 + u * 18
        rot = math.sin(u * 3 + i) * 1.2 if fall < 790 - ly - 6 else 0.2
        leaf(ctx, px, ly + fall, s * 1.1, rot, ["#E07B39", "#F4B04C", "#FFD27A"][i % 3])
    h = lerp(165, 64, prog(tm, 20.4, 30.0))
    candle(ctx, 430, 790, h, tm, True, flicker=T >= FREEZE_END)

    # Claude
    expr, since = pick(T, [(0, "neutral"), (20.5, "determined"), (22.9, "curious"),
                           (25.2, "happy"), (27.5, "yawn"), (29.0, "happy")])
    if T < FREEZE_END:
        draw_claude(ctx, 960, 790, 0.85, "neutral", FREEZE_END, walk=0.25, blink=False)
    else:
        draw_claude(ctx, 960, 790, 0.85, expr, T, squash=expr_pop(since),
                    look=(0, -6) if expr == "curious" else (0, 0))
    STYLE["desat"] = 0.0

    # 冻结效果：冰蓝暗角 + 暂停标记
    fr = 1 - un
    if fr > 0.01:
        g = rad(W / 2, H / 2, H * 0.3, H, [(0, "#9CC6FF", 0), (1, "#5A86C8", 0.45 * fr)])
        ctx.set_source(g)
        ctx.paint()
        pa = fr * env(T, 12.6, 30, 0.6, 0.1)
        rrect(ctx, 1640, 60, 210, 70, 35)
        setc(ctx, "#1C2E52", 0.55 * pa)
        ctx.fill()
        for k in (0, 1):
            rrect(ctx, 1676 + k * 22, 78, 12, 34, 3)
            setc(ctx, "#CFE6FF", pa)
            ctx.fill()
        text(ctx, "静止", 1780, 95, 32, "#CFE6FF", pa, "bold")
    # 解冻涟漪
    rp = prog(T, FREEZE_END, FREEZE_END + 1.2)
    if 0 < rp < 1:
        ctx.set_line_width(26 * (1 - rp) + 2)
        setc(ctx, "#FFE2A8", (1 - rp) * 0.8)
        circle(ctx, 960, 650, ease_out(rp) * 1500)
        ctx.stroke()

    # “之前/之后”卡片
    ca = env(T, 16.6, 20.6, 0.5, 0.35)
    if ca > 0:
        for i, (cx, lab) in enumerate([(700, "之前？"), (1220, "之后？")]):
            yy = 240 - (1 - ease_back(prog(T, 16.6 + i * 0.25, 17.3 + i * 0.25))) * 300
            soft_shadow(ctx, cx, yy + 135, 170, 14, 0.25 * ca)
            mini_scene(ctx, cx, yy, 360, 220, ca)
            label_pill(ctx, lab, cx, yy + 150, 30, "#FFFFFF", "#1C2E52", ca, 0.7)
        text(ctx, "=", 960, 236, 90, "#1C2E52", ca * env(T, 17.6, 21, 0.4, 0.2), "black")
        text(ctx, "一模一样，分不出先后", 960, 440, 34, "#1C2E52", ca * env(T, 18.2, 21, 0.5, 0.2), "bold")

    # 时间尺子
    ra = env(T, 20.7, 31, 0.6, 0.3)
    if ra > 0:
        x0, x1, y = 300, 1640, 165
        xe = lerp(x0, x1, ease_io(prog(T, 20.7, 21.7)))
        rrect(ctx, x0 - 30, y - 50, x1 - x0 + 80, 160, 24)
        setc(ctx, "#FFFFFF", 0.35 * ra)
        ctx.fill()
        arrow(ctx, x0, y, xe + 20, y, 7, INK, ra, 30)
        for k in range(21):
            tx = x0 + k * (x1 - x0) / 20
            if tx < xe:
                line(ctx, tx, y - (14 if k % 5 == 0 else 8), tx, y, 3, INK, ra * 0.8)
        text(ctx, "先", x0, y + 36, 28, INK, ra, "bold")
        text(ctx, "后", x1 - 20, y + 36, 28, INK, ra, "bold")
        text(ctx, "时间", x1 + 10, y - 34, 30, ACC, ra * smooth(prog(T, 21.4, 22)), "black")
        nx = lerp(x0 + 20, x1 - 40, prog(T, 20.9, 30.0))
        if T > 21.0:
            glow(ctx, nx, y, 40, "#FFB347", 0.6 * ra)
            circle(ctx, nx, y, 10)
            setc(ctx, ACC, ra)
            ctx.fill()
        evs = [(22.4, "太阳升高"), (25.4, "蜡烛变短"), (26.4, "叶子飘落"), (27.8, "打哈欠")]
        for i, (te, lab) in enumerate(evs):
            if T < te:
                continue
            ex = lerp(x0 + 20, x1 - 40, prog(te, 20.9, 30.0))
            q = ease_back(prog(T, te, te + 0.4))
            ly = y + (40 if i % 2 == 0 else 82)
            line(ctx, ex, y, ex, ly - 18, 2, ACC, ra * q)
            star4(ctx, ex, y, 16 * q, GOLD, ra)
            label_pill(ctx, lab, ex, ly, 24, "#FFFFFF", ACC, ra * q, 0.92)


# ======================================================================
# S2 宇宙日历 30–51
# ======================================================================
STARS2 = Stars(320, 8)
PANEL = (250, 125, 1260, 690)
RIBBON_Y = 480


def _ribbon_x(ago):
    return 230 + (1 - ago / 13.8) * 1460


def ribbon(ctx, T):
    bb = prog(T, 30.25, 31.8)
    xe = lerp(230, 1690, ease_io(prog(T, 30.6, 33.2)))
    if T > 30.5:
        ctx.rectangle(230, RIBBON_Y - 9, xe - 230, 18)
        ctx.set_source(lin(230, 0, 1690, 0, [(0, "#FFFFFF"), (0.15, "#FFD27A"), (0.6, "#A98BFF"), (1, "#5FD0FF")]))
        ctx.fill()
        glow(ctx, xe, RIBBON_Y, 60, "#FFFFFF", 0.6)
    big_bang(ctx, 230, RIBBON_Y, bb)
    events = [(12.5, "星系形成", "gal", -1), (4.6, "太阳和地球", "sun", -1), (3.8, "生命", "life", 1),
              (0.23, "恐龙", "dino", -1), (0.0003, "人类", "human", 1)]
    for ago, lab, icon, side in events:
        x = _ribbon_x(ago)
        if x > xe:
            continue
        q = ease_back(prog(T, 30.6 + (x - 230) / 1460 * 2.6, 30.9 + (x - 230) / 1460 * 2.6 + 0.3))
        y = RIBBON_Y + side * 120
        line(ctx, x, RIBBON_Y, x, y - side * 40, 2, "#FFFFFF", 0.6 * q)
        circle(ctx, x, RIBBON_Y, 8 * q)
        setc(ctx, "#FFFFFF", q)
        ctx.fill()
        with at(ctx, x, y, q):
            if icon == "gal":
                galaxy(ctx, 0, 0, 60, T, 1, rot=0.4)
            elif icon == "sun":
                sun(ctx, -26, 0, 26, T)
                earth(ctx, 32, 6, 16, T)
            elif icon == "life":
                circle(ctx, 0, 0, 22)
                setc(ctx, "#7EE08A", 0.9)
                ctx.fill()
                circle(ctx, 4, -3, 8)
                setc(ctx, "#2E8A47")
                ctx.fill()
            elif icon == "dino":
                dino(ctx, 0, 30, 0.45)
            elif icon == "human":
                human(ctx, 0, 40, 0.7)
        text(ctx, lab, x, y + side * 62, 28, "#FFFFFF", q, "bold")
    n = 138 * ease_out(prog(T, 30.6, 33.2))
    a = env(T, 30.6, 34.5, 0.4, 0.4)
    text(ctx, f"{n:.0f} 亿年", 960, 215, 96, GOLD, a, "black")
    text(ctx, "宇宙从诞生到今天", 960, 290, 32, "#FFFFFF", a * 0.85, "medium")


def _cell(m):
    x, y, w, h = PANEL
    cw, ch = w / 4, h / 3
    return (x + (m % 4) * cw + 6, y + (m // 4) * ch + 6, cw - 12, ch - 12)


def _day(d):
    x, y, w, h = PANEL
    cw, ch = w / 7, h / 5
    i = d - 1
    return (x + (i % 7) * cw + 5, y + (i // 7) * ch + 5, cw - 10, ch - 10)


def cell_box(ctx, r, lit, a, hi=0.0, color="#FFFFFF"):
    x, y, w, h = r
    rrect(ctx, x, y, w, h, 14)
    setc(ctx, "#FFFFFF", (0.05 + 0.10 * lit) * a)
    ctx.fill_preserve()
    ctx.set_line_width(2 + 3 * hi)
    setc(ctx, GOLD if hi > 0 else color, (0.25 + 0.5 * lit + 0.25 * hi) * a)
    ctx.stroke()
    if hi > 0:
        glow(ctx, x + w / 2, y + h / 2, w * 0.7, GOLD, 0.15 * hi * a)


def cal_year(ctx, T, a=1.0):
    text(ctx, "宇宙日历：把 138 亿年压缩成 1 年", 880, 82, 40, "#FFFFFF", a, "bold")
    lit_t = [34.9, 35.5, 35.65, 35.8, 35.95, 36.1, 36.25, 36.4, 36.8, 37.5, 37.9, 38.4]
    for m in range(12):
        r = _cell(m)
        lit = smooth(prog(T, lit_t[m], lit_t[m] + 0.3))
        hi = 0.0
        if m == 11:
            hi = smooth(prog(T, 38.4, 38.8)) * (0.75 + 0.25 * math.sin(T * 8))
        cell_box(ctx, r, lit, a, hi)
        x, y, w, h = r
        text(ctx, f"{m + 1}月", x + 22, y + 36, 34, "#FFFFFF", a * (0.55 + 0.45 * lit), "black", "l")
        if 0 < m < 8 and lit > 0:
            rr = rng(m)
            for k in range(6):
                star4(ctx, x + rr.uniform(40, w - 40), y + rr.uniform(70, h - 30), rr.uniform(5, 10),
                      "#CFC3FF", a * lit * 0.7, T * 0.5)
            if m == 2:
                galaxy(ctx, x + w * 0.62, y + h * 0.58, 55, T, a * lit * 0.8, rot=0.3)
    # 1 月：大爆炸
    x, y, w, h = _cell(0)
    q = prog(T, 34.9, 36.2)
    if q > 0:
        big_bang(ctx, x + w * 0.5, y + h * 0.58, min(q, 0.55) / 0.8, a)
        glow(ctx, x + w * 0.5, y + h * 0.58, 50, "#FFF3C4", a * 0.8)
        label_pill(ctx, "1日 大爆炸", x + w * 0.5, y + h - 30, 24, "#2A1B4D", GOLD, a * smooth(prog(T, 35.1, 35.5)), 0.95)
    # 9 月：太阳与地球
    x, y, w, h = _cell(8)
    q = ease_back(prog(T, 36.8, 37.3))
    if q > 0:
        with at(ctx, x + w * 0.5, y + h * 0.5, q):
            sun(ctx, -40, 0, 34, T)
            earth(ctx, 50, 8, 22, T)
        label_pill(ctx, "初 太阳和地球", x + w * 0.5, y + h - 30, 24, "#2A1B4D", GOLD, a * q, 0.95)


def cal_dec(ctx, T, a=1.0):
    text(ctx, "12 月", 880, 82, 44, GOLD, a, "black")
    for d in range(1, 32):
        r = _day(d)
        lit = 1.0 if d < 25 else smooth(prog(T, 39.4 + (d - 25) * 0.5, 39.7 + (d - 25) * 0.5))
        hi = smooth(prog(T, 42.3, 42.7)) * (0.75 + 0.25 * math.sin(T * 8)) if d == 31 else 0
        cell_box(ctx, r, lit * 0.6, a, hi)
        x, y, w, h = r
        text(ctx, str(d), x + 14, y + 24, 24, "#FFFFFF", a * 0.75, "bold", "l")
    x, y, w, h = _day(25)
    q = ease_back(prog(T, 39.6, 40.1))
    if q > 0:
        dino(ctx, x + w / 2, y + h - 22, 0.42 * q, a)
        label_pill(ctx, "恐龙登场", x + w / 2, y - 20, 24, "#14301C", "#7EE08A", a * q, 0.95)
    for d in range(26, 30):
        x, y, w, h = _day(d)
        dino(ctx, x + w / 2, y + h - 22, 0.32, a * 0.55 * smooth(prog(T, 40.0 + (d - 26) * 0.2, 40.4 + (d - 26) * 0.2)))
    x, y, w, h = _day(30)
    q = prog(T, 41.0, 41.8)
    if q > 0:
        mx, my = lerp(x + w + 80, x + w * 0.55, ease_in(q)), lerp(y - 140, y + h * 0.45, ease_in(q))
        line(ctx, mx, my, mx + 70, my - 90, 8, "#FFB347", a * (1 - q * 0.5))
        circle(ctx, mx, my, 12)
        setc(ctx, "#FFE2A8", a)
        ctx.fill()
        if q >= 1:
            glow(ctx, x + w * 0.55, y + h * 0.45, 90, "#FF8A3D", a * env(T, 41.8, 43.5, 0.05, 1.0))
        label_pill(ctx, "恐龙谢幕", x + w / 2, y - 20, 24, "#FFFFFF", "#D2552A", a * smooth(prog(T, 41.8, 42.1)), 0.95)


CLOCK_C = (610, 470)


def cal_31(ctx, T, a=1.0):
    text(ctx, "12 月 31 日 · 除夕", 880, 82, 44, GOLD, a, "black")
    secs = (23 * 3600 + 48 * 60) * ease_io(prog(T, 43.3, 44.8))
    clock(ctx, CLOCK_C[0], CLOCK_C[1], 240, secs, a=a, show_sec=False)
    hh, mm = int(secs // 3600), int(secs % 3600 // 60)
    text(ctx, f"{hh:02d}:{mm:02d}", 1190, 360, 150, "#FFFFFF", a, "black")
    q = ease_back(prog(T, 44.9, 45.4))
    if q > 0:
        human(ctx, 1060, 600, 1.2 * q, a)
        human(ctx, 1130, 605, 1.0 * q, a * 0.8)
        text(ctx, "人类出现", 1250, 540, 56, GOLD, a * q, "black", "l")
        text(ctx, "距离新年只剩 12 分钟", 1250, 610, 32, "#FFFFFF", a * q * 0.85, "medium", "l")


def cal_minute(ctx, T, a=1.0):
    text(ctx, "23:59 → 24:00 · 最后一分钟", 880, 82, 44, GOLD, a, "black")
    x0, x1, y = 300, 1460, 430
    rrect(ctx, x0, y - 30, x1 - x0, 60, 30)
    setc(ctx, "#FFFFFF", 0.1 * a)
    ctx.fill()
    for k in range(61):
        tx = lerp(x0 + 20, x1 - 20, k / 60)
        big = k % 10 == 0
        line(ctx, tx, y - (22 if big else 12), tx, y + (22 if big else 12), 3 if big else 1.5, "#FFFFFF", a * (0.8 if big else 0.4))
        if big:
            text(ctx, f"{k}秒", tx, y + 60, 24, "#FFFFFF", a * 0.7, "medium")
    cur = lerp(x0 + 20, x1 - 20, ease_io(prog(T, 47.3, 48.6)))
    line(ctx, cur, y - 50, cur, y + 50, 4, "#7FD8FF", a * env(T, 47.2, 48.9, 0.2, 0.4))
    hs = lerp(x0 + 20, x1 - 20, 48 / 60)
    he = x1 - 20
    q = smooth(prog(T, 48.4, 49.0))
    if q > 0:
        rrect(ctx, hs, y - 30, (he - hs) * q, 60, 12)
        setc(ctx, GOLD, 0.85 * a)
        ctx.fill()
        glow(ctx, (hs + he) / 2, y, 220, GOLD, 0.25 * a * q)
        line(ctx, (hs + he) / 2, y - 38, (hs + he) / 2, y - 78, 3, GOLD, a * q)
        text(ctx, "有文字记载的全部历史", (hs + he) / 2 - 40, y - 168, 40, "#FFFFFF", a * q, "black")
        text(ctx, "≈ 最后 12 秒", (hs + he) / 2 - 40, y - 116, 32, GOLD, a * q, "bold")
    q2 = smooth(prog(T, 49.4, 49.9))
    if q2 > 0:
        line(ctx, he - 1, y + 36, he - 60, y + 150, 3, "#7FD8FF", a * q2)
        circle(ctx, he - 2, y, 7)
        setc(ctx, "#7FD8FF", a * q2)
        ctx.fill()
        text(ctx, "你的一生 ≈ 0.2 秒", he - 60, y + 180, 34, "#7FD8FF", a * q2, "bold", "c")


def _zoom_mats(R):
    px, py, pw, ph = PANEL
    rx, ry, rw, rh = R
    s1 = min(pw / rw, ph / rh)
    return (px + pw / 2, py + ph / 2), (rx + rw / 2, ry + rh / 2), s1


def zoom_between(ctx, T, t0, dur, R, draw_a, draw_b):
    u = ease_io(prog(T, t0, t0 + dur))
    pc, rc, s1 = _zoom_mats(R)
    s = s1 ** u
    fx, fy = lerp(pc[0], rc[0], u), lerp(pc[1], rc[1], u)
    ctx.save()
    ctx.translate(pc[0], pc[1])
    ctx.scale(s, s)
    ctx.translate(-fx, -fy)
    aa = 1 - smooth(prog(u, 0.35, 0.95))
    if aa > 0:
        draw_a(ctx, T, aa)
    ab = smooth(prog(u, 0.2, 0.8))
    if ab > 0:
        ctx.translate(rc[0], rc[1])
        ctx.scale(1 / s1, 1 / s1)
        ctx.translate(-pc[0], -pc[1])
        draw_b(ctx, T, ab)
    ctx.restore()


def s_calendar(ctx, T):
    space_bg(ctx, T, STARS2, neb=0.8, seed=5)
    aA = 1 - smooth(prog(T, 33.8, 34.8))
    if aA > 0:
        with group_alpha(ctx, aA):
            k = 1 - 0.3 * ease_in(prog(T, 33.8, 34.8))
            with at(ctx, 960 * (1 - k), RIBBON_Y * (1 - k), k):
                ribbon(ctx, T)
    aB = smooth(prog(T, 34.0, 34.9))
    if aB > 0:
        k = lerp(1.25, 1.0, ease_out(prog(T, 34.0, 35.0)))
        cx, cy = 880, 470
        with at(ctx, cx * (1 - k), cy * (1 - k), k), group_alpha(ctx, aB):
            if T < 39.0:
                cal_year(ctx, T)
            elif T < 39.9:
                zoom_between(ctx, T, 39.0, 0.9, _cell(11), cal_year, cal_dec)
            elif T < 43.0:
                cal_dec(ctx, T)
            elif T < 43.9:
                zoom_between(ctx, T, 43.0, 0.9, _day(31), cal_dec, cal_31)
            elif T < 47.0:
                cal_31(ctx, T)
            elif T < 47.9:
                zoom_between(ctx, T, 47.0, 0.9, (CLOCK_C[0] - 240, CLOCK_C[1] - 240, 480, 480), cal_31, cal_minute)
            else:
                cal_minute(ctx, T)
    expr, since = pick(T, [(0, "surprised"), (31.8, "curious"), (34.8, "think"), (36.8, "happy"),
                           (39.0, "curious"), (41.0, "surprised"), (42.0, "curious"), (43.0, "surprised"),
                           (45.0, "excited"), (47.0, "surprised"), (49.4, "excited")])
    glow(ctx, 1730, 880, 160, "#7F6BFF", 0.25)
    ellipse(ctx, 1730, 884, 150, 18)
    setc(ctx, "#3A2E6A", 0.8)
    ctx.fill()
    draw_claude(ctx, 1730, 880, 0.48, expr, T, squash=expr_pop(since), seed=2,
                look=(-6, -3), arm_l=wave(T, 0.8, 0.4) * env(T, 45.0, 46.6, 0.2, 0.3))
    vignette(ctx, 0.4)


# ======================================================================
# S3 时间之箭 51–63
# ======================================================================
TABLE = (200, 600, 640)    # 左, 桌面 y, 右
FLOOR = 860
CUP_X0 = 585
T_TIP, T_HIT = 51.95, 52.7
G = 1250.0


def _shards():
    r = rng(77)
    out = []
    for i in range(16):
        ang = r.uniform(math.pi * 1.05, math.pi * 1.95)
        sp = r.uniform(250, 620)
        k = 2.6 if i < 6 else 1.7
        pts = [(math.cos(a_) * r.uniform(10, 18) * k, math.sin(a_) * r.uniform(10, 18) * k)
               for a_ in sorted(r.uniform(0, TAU) for _ in range(r.choice([3, 4, 5])))]
        out.append(dict(vx=math.cos(ang) * sp, vy=math.sin(ang) * sp, w=r.uniform(-14, 14),
                        pts=pts, c=r.choice(["#5AA0E8", "#8CC4FF", "#3B78C0", "#2D5E99"])))
    return out


SHARDS = _shards()


def _shard_pos(sh, u):
    """碎片在撞击后 u 秒的位置（落地弹一次后停住）。"""
    x0, y0 = 655, FLOOR - 20
    vx, vy = sh["vx"], sh["vy"]
    t1 = (-vy + math.sqrt(vy * vy + 2 * G * 20)) / G   # 第一次落地
    if u <= t1:
        return x0 + vx * u, y0 + vy * u + 0.5 * G * u * u, sh["w"] * u
    x1 = x0 + vx * t1
    vy2 = -abs(vy + G * t1) * 0.3
    t2 = -2 * vy2 / G
    v = u - t1
    if v <= t2:
        return x1 + vx * 0.5 * v, FLOOR + vy2 * v + 0.5 * G * v * v, sh["w"] * (t1 + v * 0.5)
    x2 = x1 + vx * 0.5 * t2
    w = v - t2
    slide = vx * 0.25 * (1 - math.exp(-w * 4)) / 4
    return x2 + slide, FLOOR, sh["w"] * (t1 + t2 * 0.5)


def _draw_shard(ctx, sh, x, y, rot, a=1.0, ghost=False):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    pts = sh["pts"]
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    if ghost:
        ctx.set_line_width(2)
        setc(ctx, "#7FD8FF", a)
        ctx.stroke_preserve()
        setc(ctx, "#7FD8FF", a * 0.25)
        ctx.fill()
    else:
        setc(ctx, sh["c"], a)
        ctx.fill()
    ctx.restore()


R_PART = rng(5)
PARTS = [dict(x=R_PART.uniform(0, 1), y=R_PART.uniform(0, 1), vx=R_PART.uniform(-1, 1), vy=R_PART.uniform(-1, 1),
              c=0 if i < 70 else 1) for i in range(140)]
BOX = (1130, 270, 520, 330)
T_LIFT = 56.0


def _fold(v, L):
    v = v % (2 * L)
    return v if v < L else 2 * L - v


def _part_pos(p, T):
    bx, by, bw, bh = BOX
    rpad = 8
    half = bw / 2 - rpad * 2
    t = max(T, 55.0) - 55.0
    sp = 170
    if p["c"] == 0:
        x0 = rpad + p["x"] * half
    else:
        x0 = bw / 2 + rpad + p["x"] * half
    y = _fold(p["y"] * (bh - 2 * rpad) + p["vy"] * sp * t, bh - 2 * rpad) + rpad
    tl = min(t, T_LIFT - 55.0)
    if p["c"] == 0:
        x = _fold(x0 - rpad + p["vx"] * sp * tl, half) + rpad
    else:
        x = _fold(x0 - bw / 2 - rpad + p["vx"] * sp * tl, half) + bw / 2 + rpad
    if t > tl:
        x = _fold(x - rpad + p["vx"] * sp * (t - tl), bw - 2 * rpad) + rpad
    return bx + x, by + y


def s_arrow(ctx, T):
    warm_bg(ctx, T, 860)
    # 桌子
    l, ty, r = TABLE
    soft_shadow(ctx, (l + r) / 2, FLOOR + 4, 260, 18, 0.25)
    for lx in (l + 30, r - 40):
        rrect(ctx, lx, ty + 20, 22, FLOOR - ty - 20, 4)
        setc(ctx, "#9A6A48")
        ctx.fill()
    rrect(ctx, l, ty, r - l, 28, 8)
    ctx.set_source(lin(0, ty, 0, ty + 28, [(0, "#C9935F"), (1, "#9A6A48")]))
    ctx.fill()
    # 杯子
    if T < T_HIT:
        if T < T_TIP:
            wob = math.sin(T * 30) * 0.04 * prog(T, 51.4, T_TIP)
            cup(ctx, CUP_X0, ty, 0.85, wob)
        else:
            u = T - T_TIP
            y = ty + 0.5 * G * 0.66 * u * u
            cup(ctx, CUP_X0 + u * 95, min(y, FLOOR), 0.85, u * 2.4)
    else:
        u = T - T_HIT
        if u < 0.5:
            glow(ctx, 655, FLOOR - 10, 120, "#FFFFFF", (1 - u / 0.5) * 0.7)
        for sh in SHARDS:
            x, y, rot = _shard_pos(sh, u)
            _draw_shard(ctx, sh, x, y, rot, 1.0)
        # 倒放的幽灵
        rw = env(T, 53.7, 55.3, 0.2, 0.3)
        if rw > 0:
            k = ease_io(prog(T, 53.8, 54.6))
            for sh in SHARDS:
                x, y, rot = _shard_pos(sh, 1.5)
                tx, ty2 = 655 + sh["pts"][0][0] * 2, ty - 50 + sh["pts"][0][1] * 2
                _draw_shard(ctx, sh, lerp(x, tx, k), lerp(y, ty2, k), rot * (1 - k), rw * 0.9, ghost=True)
            if k >= 1:
                with group_alpha(ctx, rw * 0.6):
                    cup(ctx, 655, ty, 0.85)
            label_pill(ctx, "◀◀ 倒放", 420, 470, 30, "#FFFFFF", "#2D5E99", rw, 0.9)
            xq = ease_back(prog(T, 54.5, 54.9))
            if xq > 0:
                for sgn in (-1, 1):
                    line(ctx, 655 - 70 * xq, ty - 110 - sgn * 70 * xq, 655 + 70 * xq, ty - 110 + sgn * 70 * xq, 18, "#E2483D", rw)
                text(ctx, "现实中从不发生", 655, ty - 220, 34, "#E2483D", rw * xq, "black")
    # 粒子盒
    ba = 0.45 + 0.55 * smooth(prog(T, 55.0, 55.5))
    bx, by, bw, bh = BOX
    rrect(ctx, bx - 10, by - 10, bw + 20, bh + 20, 18)
    setc(ctx, "#FFFFFF", 0.55 * ba)
    ctx.fill_preserve()
    ctx.set_line_width(4)
    setc(ctx, INK, 0.7 * ba)
    ctx.stroke()
    for p in PARTS:
        x, y = _part_pos(p, T)
        circle(ctx, x, y, 7)
        setc(ctx, "#F08A4B" if p["c"] == 0 else "#4F8FE0", ba)
        ctx.fill()
    lift = ease_io(prog(T, T_LIFT - 0.3, T_LIFT + 0.3))
    if lift < 1:
        rrect(ctx, bx + bw / 2 - 5, by - lift * (bh + 30), 10, bh, 4)
        setc(ctx, INK, 0.85 * ba * (1 - lift))
        ctx.fill()
    ent = 0.12 if T < T_LIFT else 0.12 + 0.83 * (1 - math.exp(-(T - T_LIFT) / 1.4))
    ex0, ey = bx, by + bh + 52
    text(ctx, "熵（混乱度）", ex0, ey, 28, INK, ba, "bold", "l")
    rrect(ctx, ex0 + 180, ey - 13, bw - 180, 26, 13)
    setc(ctx, INK, 0.15 * ba)
    ctx.fill()
    rrect(ctx, ex0 + 180, ey - 13, (bw - 180) * ent, 26, 13)
    ctx.set_source(lin(ex0 + 180, 0, ex0 + bw, 0, [(0, "#4F8FE0", ba), (1, "#E2483D", ba)]))
    ctx.fill()
    oa = env(T, 55.2, 57.4, 0.3, 0.4)
    ca = env(T, 57.3, 64, 0.4, 0.3)
    label_pill(ctx, "有序", bx + bw / 2, by - 40, 28, "#FFFFFF", "#4F8FE0", oa, 0.9)
    label_pill(ctx, "混乱", bx + bw / 2, by - 40, 28, "#FFFFFF", "#E2483D", ca, 0.9)
    # 时间之箭
    aa = env(T, 59.2, 64, 0.3, 0.2)
    if aa > 0:
        p = ease_io(prog(T, 59.2, 60.3))
        x0, x1, y = 250, 1670, 140
        xe = lerp(x0, x1, p)
        ctx.set_line_width(18)
        ctx.set_line_cap(1)
        ctx.set_source(lin(x0, 0, x1, 0, [(0, "#4F8FE0", aa), (1, "#E2483D", aa)]))
        ctx.move_to(x0, y)
        ctx.line_to(xe - 20, y)
        ctx.stroke()
        hx = xe
        ctx.move_to(hx + 10, y)
        ctx.line_to(hx - 40, y - 34)
        ctx.line_to(hx - 40, y + 34)
        ctx.close_path()
        setc(ctx, "#E2483D" if p > 0.9 else mix_hex(p), aa)
        ctx.fill()
        text(ctx, "过去", x0, y + 52, 32, "#2D5E99", aa, "black")
        text(ctx, "未来", x1 - 20, y + 52, 32, "#B83A30", aa * smooth(prog(T, 60.0, 60.4)), "black")
        text(ctx, "时间之箭  ·  熵总在增加", 960, y + 52, 32, INK, aa * smooth(prog(T, 60.3, 60.8)), "bold")
    expr, since = pick(T, [(0, "neutral"), (52.75, "surprised"), (53.8, "think"), (55.4, "curious"),
                           (57.4, "surprised"), (59.3, "determined"), (61.4, "proud")])
    draw_claude(ctx, 930, 880, 0.55, expr, T, squash=expr_pop(since), seed=1,
                look=(-8, 0) if T < 55.3 else (8, -2))


def mix_hex(p):
    from .core import mix
    return mix("#4F8FE0", "#E2483D", p)


SCENES_A = [s_opening, s_change, s_calendar, s_arrow]
