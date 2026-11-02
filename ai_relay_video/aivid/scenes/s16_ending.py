"""结语 · 接力：日出跑道上的接力赛（论文 → 芯片 → 代工 → 开源 → 产品）→ 开放连接 / 好数据 / 健康商业 →
围墙开始松动（淘宝接入微信支付、WorkBuddy 连上飞书）→ 孤岛之间架起光桥 → 片尾。"""
import math

from mascot import draw_mascot, draw_prop

from ..core import (TAU, Cam, at, circle, clamp, ease_back, ease_in, ease_io, ease_out, ease_out5, ellipse, fill,
                    font, glow, lerp, lin, line, pop, prog, rad, ring_burst, rng, rrect, setc, smooth,
                    sparkle_burst, star4, stroke_pts, text, text_reveal, text_w, view, bezier_pts, point_on,
                    polyline_partial)
from ..icons import ic_penguin
from ..props import app_tile, chip_pkg, factory, iphone, name_card, tag, wafer
from .common import host, mini_icon, talk_lines

DUR = 33.0
CHAPTER = ("结语", "接力")

VO = [
    (1.0, '回头看，AI 从来不是一家公司的独奏，而是一场{接力赛}：'),
    (5.8, '论文、芯片、代工、开源、产品，一棒接一棒。'),
    (11.5, '谁能让接力棒传得更顺——更开放的连接、更好的数据、更健康的商业——谁就跑得更快。'),
    (18.6, '好在，围墙已经开始松动：淘宝接入了微信支付，腾讯的 WorkBuddy 也连上了字节的飞书。'),
    (25.6, '愿每一座孤岛，都能架起通往彼此的{桥}。'),
]

TRACK_Y = 820
STATIONS = [("论文", 600, "#FF9F68"), ("芯片", 1500, "#76B900"), ("代工", 2400, "#E60012"), ("开源", 3300, "#2EC4B6"),
            ("产品", 4200, "#8B6CFF")]
T_PASS = [6.0, 7.0, 8.0, 9.0, 10.0]

P = (host(300, TRACK_Y + 60, 0.6, "smile", seed=16.6)
     .look(0, 0.8, -0.5)
     .expr(1.0, "proud")
     .expr(5.6, "excited").hold(5.8, ("baton",), "r", -0.5).arm(5.8, "r", 1.2)
     .run_to(6.0, 10.6, 4300, TRACK_Y + 60)
     .expr(10.8, "fired_up").fx(10.8, ()).run_to(11.0, 17.6, 6400, TRACK_Y + 60)
     .expr(17.8, "smile").drop(17.8).arm(17.8, "r", 0.0)
     .move(18.2, 18.3, 8400, 716).fade(18.0, 0.0, 0.2).fade(18.4, 1.0, 0.3)
     .expr(18.6, "curious").look(18.6, 0.6, -0.6)
     .expr(20.6, "happy").expr(22.6, "starry").hop(22.7, 40, 0.38)
     .expr(25.6, "moved").look(25.6, 0.0, -0.6)
     .expr(28.4, "grin").wave(28.6, 32.6, "r"))
talk_lines(P, VO, [0, 2, 4], smile=0.45)

CAM = Cam([
    (0.0, (900, 520, 0.82)),
    (5.4, (1000, 520, 0.9), ease_io),
    (6.0, (900, 520, 0.95)),
    (10.6, (4300, 520, 0.95), lambda u: u),
    (11.2, (4500, 520, 0.92)),
    (17.6, (6500, 520, 0.92), lambda u: u),
    (18.2, (8400, 560, 0.92), ease_io),
    (24.8, (8410, 560, 0.94)),
    (26.0, (8400, 540, 0.88), ease_io),
    (33.0, (8400, 520, 0.92)),
], drift=5, seed=33.0)


def _bg(ctx, t, cam):
    sun = smooth(prog(t, 0.0, 28.0))
    ctx.set_source(lin(0, 0, 0, 1080, [(0, mix_c("#2A2D5C", "#7FB6FF", sun)), (0.55, mix_c("#7A4F7E", "#FFD1B0", sun)),
                                       (1, mix_c("#FF9F68", "#FFE7C8", sun))]))
    ctx.paint()
    sy = lerp(980, 640, ease_out(sun))
    glow(ctx, 960, sy, 600, "#FFD36B", 0.55)
    circle(ctx, 960, sy, 110)
    fill(ctx, "#FFE29A", 0.9)
    with view(ctx, cam, 0.3):
        R = rng(2)
        for i in range(30):
            x = R.uniform(-1000, 9000)
            y = R.uniform(80, 420)
            for (dx, dy, k) in ((-0.8, 0.1, 0.6), (-0.3, -0.15, 0.8), (0.3, -0.05, 0.7), (0.8, 0.1, 0.55)):
                circle(ctx, x + dx * 90, y + dy * 90, k * 90)
            fill(ctx, "#FFFFFF", 0.35)


def mix_c(a, b, t):
    from ..core import mix
    return mix(a, b, t)


def _track(ctx, t):
    # 跑道
    ctx.rectangle(-1200, TRACK_Y - 40, 9000, 260)
    ctx.set_source(lin(0, TRACK_Y - 40, 0, TRACK_Y + 220, [(0, "#D9654A"), (1, "#B04A34")]))
    ctx.fill()
    for k in range(4):
        y = TRACK_Y - 20 + k * 60
        ctx.set_line_width(4)
        setc(ctx, "#FFFFFF", 0.7)
        ctx.move_to(-1200, y)
        ctx.line_to(7800, y)
        ctx.stroke()
    ctx.rectangle(-1200, TRACK_Y + 220, 9000, 400)
    fill(ctx, "#5FA85A")
    # 接力站
    for i, (lab, x, c) in enumerate(STATIONS):
        q = pop(t, 1.2 + i * 0.25, 0.45)
        if q <= 0:
            continue
        with at(ctx, x, TRACK_Y - 250, q):
            glow(ctx, 0, 0, 160, c, 0.35)
            circle(ctx, 0, 0, 96)
            fill(ctx, "#FFFFFF", 0.95)
            if lab == "论文":
                draw_prop(ctx, ("paper", {"title": "Transformer"}), t)
            elif lab == "芯片":
                chip_pkg(ctx, 0, 0, 120, "GPU", "", "#76B900", 1.0, 0.0, t)
            elif lab == "代工":
                wafer(ctx, 0, 0, 62, 1.0, t, 0.0, lit=0.5)
            elif lab == "开源":
                ic_penguin(ctx, 0, 0, 120, 1.0, t)
            else:
                iphone(ctx, 0, 0, 130, 1.0)
            text(ctx, lab, 0, 140, 40, "#FFFFFF", 1.0, "black", outline="#5A2A1A", outline_w=6)
        # 站上的小队友（交棒时举手）
        k = 1.0 if t < T_PASS[i] else 0.0
        draw_mascot(ctx, x + 60, TRACK_Y + 60, 0.36, "excited" if t > T_PASS[i] - 0.8 else "smile", t, since=2.0,
                    seed=40 + i, arm_r=1.0 if abs(t - T_PASS[i]) < 0.6 else 0.2, look=(-0.8, -0.3), hat=None)
        if abs(t - T_PASS[i]) < 0.6:
            sparkle_burst(ctx, t, T_PASS[i], x + 60, TRACK_Y - 60, 8, 120, "#FFE7A3", 0.7, i, 16)
    # 接力的光轨
    u = prog(t, 6.0, 10.6)
    if u > 0:
        xx = lerp(300, 4300, u)
        ctx.set_source(lin(300, 0, xx, 0, [(0, "#FFD36B", 0.0), (1, "#FFD36B", 0.8)]))
        rrect(ctx, 300, TRACK_Y + 108, xx - 300, 12, 6)
        ctx.fill()


VALUES = [("更开放的连接", "#4C8DFF", 12.4), ("更好的数据", "#2EC4B6", 13.8), ("更健康的商业", "#E0A42B", 15.4)]


def _values(ctx, t):
    a = smooth(prog(t, 11.4, 11.8)) * (1 - smooth(prog(t, 17.6, 18.1)))
    if a <= 0:
        return
    for i, (lab, c, st) in enumerate(VALUES):
        q = pop(t, st, 0.5)
        if q <= 0:
            continue
        x = 4700 + i * 650 + (t - st) * 120
        with at(ctx, x, 300 + i * 40, q):
            rrect(ctx, -200, -50, 400, 100, 50)
            fill(ctx, c, a)
            text(ctx, lab, 0, 0, 40, "#FFFFFF", a, "black")
    # 速度线
    sp = smooth(prog(t, 11.0, 12.0))
    st = P.state(t)
    for k in range(8):
        yy = TRACK_Y - 160 + k * 26
        L = 200 + (k % 3) * 120
        line(ctx, st["x"] - 160 - L, yy, st["x"] - 160, yy, 5, "#FFFFFF", 0.4 * a * sp)


ISL = {"微信": (7600, 600, "#07C160"), "淘宝": (8050, 450, "#FF5000"), "WorkBuddy": (8750, 450, "#3E8BFF"),
       "飞书": (9200, 600, "#3370FF"), "抖音": (7720, 850, "#161823"), "钉钉": (9080, 850, "#1677FF")}
HUB = (8400, 720)
BRIDGES = [("淘宝", "微信", "接入微信支付", 19.6), ("WorkBuddy", "飞书", "官方连接器", 21.8)]
MORE = [("微信", "抖音"), ("抖音", "钉钉"), ("钉钉", "飞书"), ("淘宝", "WorkBuddy"), ("微信", None), ("淘宝", None),
        ("WorkBuddy", None), ("飞书", None), ("抖音", None), ("钉钉", None)]


def _isle(ctx, x, y, a, rx=180):
    ellipse(ctx, x, y + 40, rx + 10, 44)
    fill(ctx, "#3B7A4E", a)
    ellipse(ctx, x, y + 26, rx, 36)
    fill(ctx, "#7CC48A", a)


def _arc(ctx, p0, p1, u, w, c, a, lift=180):
    (x0, y0), (x1, y1) = p0, p1
    mid = ((x0 + x1) / 2, min(y0, y1) - lift)
    pts = bezier_pts((x0, y0), mid, mid, (x1, y1), 40)
    seg = polyline_partial(pts, 0, u)
    stroke_pts(ctx, seg, w * 2.2, "#FFF3C4", 0.3 * a)
    stroke_pts(ctx, seg, w, c, a)
    return pts


def _islands(ctx, t):
    a = smooth(prog(t, 17.8, 18.6))
    if a <= 0:
        return
    ctx.rectangle(6800, 560, 3600, 800)
    ctx.set_source(lin(0, 560, 0, 1200, [(0, "#6FB8D9", a), (1, "#2C6E8E", a)]))
    ctx.fill()
    for k in range(4):
        y = 600 + k * 70
        ctx.move_to(6800, y)
        for xx in range(6800, 10400, 60):
            ctx.line_to(xx, y + math.sin(xx * 0.01 + t * (1.0 + k * 0.2)) * 5)
        ctx.set_line_width(3)
        setc(ctx, "#FFFFFF", 0.15 * a)
        ctx.stroke()
    # 先画"愿每一座孤岛都架起桥"的光桥（在岛的后面）
    all_b = smooth(prog(t, 25.8, 27.6))
    if all_b > 0:
        for k, (s0, s1) in enumerate(MORE):
            q = clamp(all_b * 1.8 - k * 0.08)
            if q <= 0:
                continue
            p0 = ISL[s0][:2]
            p1 = HUB if s1 is None else ISL[s1][:2]
            _arc(ctx, p0, p1, ease_out(q), 6, "#FFE9A8", 0.85 * a, 120 if s1 is None else 160)
    _isle(ctx, HUB[0], HUB[1] - 10, a, 150)
    for nm, (x, y, c) in ISL.items():
        _isle(ctx, x, y, a)
    labels = []
    for (s0, s1, lab, st) in BRIDGES:
        u = ease_out(prog(t, st, st + 1.2))
        if u <= 0:
            continue
        p0 = (ISL[s0][0], ISL[s0][1] + 12)
        p1 = (ISL[s1][0], ISL[s1][1] + 12)
        pts = _arc(ctx, p0, p1, u, 10, "#FFD36B", a, 230)
        if u > 0.6:
            (lx, ly), _ = point_on(pts, 0.5)
            labels.append((lab, lx, ly - 40, a * smooth((u - 0.6) / 0.3)))
    for nm, (x, y, c) in ISL.items():
        app_tile(ctx, x, y - 50, 96, c, nm[:2] if nm != "WorkBuddy" else "WB", a, text_size=34)
        text(ctx, nm, x, y + 28, 26, "#FFFFFF", a, "black", outline="#2B4A3A", outline_w=5)
    for (lab, lx, ly, aa) in labels:
        tag(ctx, lab, lx, ly, 26, "#3A2A00", "#FFE29A", aa)
    yr = smooth(prog(t, 20.2, 20.6)) * (1 - smooth(prog(t, 25.4, 25.9)))
    if yr > 0:
        tag(ctx, "2024：淘宝全面接入微信支付", 7820, 230, 26, "#FFFFFF", "#FF5000", a * yr)
    yr2 = smooth(prog(t, 22.6, 23.0)) * (1 - smooth(prog(t, 25.4, 25.9)))
    if yr2 > 0:
        tag(ctx, "2026：WorkBuddy 上线飞书连接器", 8980, 230, 26, "#FFFFFF", "#3E8BFF", a * yr2)


def _end_title(ctx, t):
    p = prog(t, 28.8, 30.2)
    if p <= 0:
        return
    d = smooth(p)
    ctx.set_source(lin(0, 0, 0, 1080, [(0, "#1A1030", 0.55 * d), (0.6, "#1A1030", 0.25 * d), (1, "#1A1030", 0.0)]))
    ctx.paint()
    glow(ctx, 960, 300, 600, "#FFB27A", 0.3 * d)
    s = "AI 接力赛"
    size = 140
    font(ctx, size, "black")
    tw = ctx.text_extents(s).x_advance
    q = ease_out5(prog(t, 28.8, 29.8))
    text(ctx, s, 964, 286 + (1 - q) * 30, size, "#1A0F2E", 0.35 * q, "black")
    ctx.save()
    font(ctx, size, "black")
    ctx.move_to(960 - tw / 2, 280 + (1 - q) * 30 + size * 0.36)
    ctx.text_path(s)
    ctx.set_source(lin(0, 200, 0, 360, [(0, "#FFF4E6", q), (1, "#FFB27A", q)]))
    ctx.fill()
    ctx.restore()
    text_reveal(ctx, "感谢观看 · 愿每一座孤岛都能架起桥", 960, 420, 44, "#FFE3C8", prog(t, 29.6, 30.8))
    c = smooth(prog(t, 30.8, 31.4))
    if c > 0:
        text(ctx, "数据与事件截至 2026 年 11 月 · 非官方科普作品，图形均为示意", 960, 490, 24, "#E8DCF2", c, "bold")


def draw(ctx, t):
    cam = CAM.at(t)
    _bg(ctx, t, cam)
    with view(ctx, cam, 1.0):
        _track(ctx, t)
        _values(ctx, t)
        _islands(ctx, t)
        P.draw(ctx, t)
    _end_title(ctx, t)


def sfx():
    out = [(0.0, "ambience_dawn", {"dur": 18.0, "gain": 0.3}), (1.0, "shimmer", {"dur": 1.6, "gain": 0.3})]
    for i in range(5):
        out.append((1.2 + i * 0.25, "pop", {"gain": 0.25, "pitch": 1.0 + i * 0.1}))
    out.append((5.8, "powerup", {"gain": 0.3}))
    for i, tp in enumerate(T_PASS):
        out.append((tp, "swish_hi", {"gain": 0.25}))
        out.append((tp + 0.05, "ding", {"gain": 0.22, "pitch": 1.0 + i * 0.12}))
    out += [
        (11.0, "whoosh", {"dur": 1.2, "gain": 0.3}),
        (12.4, "pop", {"gain": 0.3}), (13.8, "pop", {"gain": 0.3, "pitch": 1.2}), (15.4, "pop", {"gain": 0.3, "pitch": 1.4}),
        (17.9, "whoosh", {"dur": 1.0, "gain": 0.3}),
        (18.4, "ambience_sea", {"dur": 10.0, "gain": 0.25}),
        (19.6, "bridge", {"gain": 0.4}), (21.8, "bridge", {"gain": 0.4, "pitch": 1.12}),
        (25.8, "shimmer", {"dur": 2.0, "gain": 0.35}),
        (28.8, "finale", {"gain": 0.5}),
    ]
    return out
