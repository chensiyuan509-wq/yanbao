"""04 · 为什么是美国（上）：竞合与互通。Muse 和 Gemini 是对手，却能连上 Gmail / 谷歌日历 / 文档 / Outlook /
Instagram；苹果和谷歌斗了十几年，Siri 用上 Gemini；投资关系网；竞争、合作、投资拧成一股绳。
镜头在天空的几层云台之间上下移动。"""
import math

from ..core import (TAU, Cam, at, box_shadow, circle, clamp, ease_back, ease_in, ease_io, ease_out,
                    ease_out5, ellipse, fill, glow, lerp, lin, line, pop, prog, rad, ring_burst, rng, rrect,
                    setc, smooth, sparkle_burst, star4, stroke_pts, text, text_w, view, bezier_pts,
                    polyline_partial, point_on, check_mark, dashed)
from ..charts import MapView, world_dots
from ..icons import ic_calendar, ic_docs, ic_gmail, ic_instagram, ic_muse, ic_mail
from ..props import app_tile, gemini_star, iphone, name_card, tag
from .common import host, talk_lines

DUR = 44.5
CHAPTER = ("04", "为什么是美国")

VO = [
    (1.0, '那么，为什么 AI 先在美国引爆？'),
    (4.7, '先看一个细节：Meta 的个人智能体 {Muse}，和谷歌的 Gemini 是直接对手；'),
    (10.3, '可 Muse 照样能连上 Gmail、谷歌日历、谷歌文档，还有微软的 Outlook、自家的 Instagram。'),
    (17.6, '苹果和谷歌斗了十几年，iPhone 上照样能装谷歌全家桶，新版 Siri 干脆用上了 {Gemini}。'),
    (25.2, '微软投资了 OpenAI，也用 Anthropic 的模型；亚马逊和谷歌都投资了 Anthropic；Meta 入股 Scale AI，把创始人请来领导 AI 团队。'),
    (36.5, '{竞争、合作、投资}，三条线缠在一起，大公司和小公司，谁也离不开谁。'),
]

Y1, Y2, Y3 = 880, 2060, 3260         # 三层云台的地面
XB, XD = 1000, 3080

P = (host(560, Y1, 0.6, "think", seed=8.8)
     .fx(0, ("question2",)).look(0, 0.6, -0.8)
     .expr(3.6, "determined").fx(3.6, ())
     # 跳到下一层云台
     .hop(4.0, 70, 0.4).move(4.3, 5.1, 420, Y2, ease_in).land(5.1, 0.22)
     .expr(5.2, "curious").look(5.2, 0.9, -0.6)
     .expr(8.0, "worried").look(8.0, 1.0, -0.6)
     .expr(10.5, "surprised").expr(11.6, "awe").look(11.6, 0.9, -0.7)
     .expr(16.4, "smile").run_to(16.6, 17.5, XD - 680, Y2)
     .expr(17.6, "curious").look(17.6, 0.9, -0.6)
     .expr(21.8, "shock").startle(21.8).expr(22.9, "starry")
     # 再跳到下一层
     .expr(24.4, "determined").hop(24.4, 60, 0.4).move(24.7, 25.5, XD - 820, Y3, ease_in).land(25.5, 0.22)
     .expr(25.6, "focused").look(25.6, 0.9, -0.7)
     .look(28.0, 0.5, -0.9).look(31.0, 1.0, -0.4).expr(33.0, "awe")
     .expr(36.4, "grin").look(36.4, 0.8, -0.6).nod(40.0, 2).expr(41.0, "proud"))
talk_lines(P, VO, [0, 1, 3, 5], smile=0.3)

CAM = Cam([
    (0.0, (960, 560, 1.06)),
    (3.8, (960, 560, 1.0)),
    (5.0, (XB, Y2 - 360, 1.0), ease_io),
    (10.0, (XB + 20, Y2 - 360, 1.04)),
    (10.8, (XB + 60, Y2 - 380, 0.96), ease_io),
    (16.4, (XB + 80, Y2 - 380, 0.98)),
    (17.4, (XD, Y2 - 360, 1.0), ease_io),
    (24.4, (XD + 20, Y2 - 360, 1.02)),
    (25.4, (XD, Y3 - 380, 0.98), ease_io),
    (35.6, (XD + 20, Y3 - 380, 1.0)),
    (37.2, (XD, Y3 - 420, 0.9), ease_io),
    (44.5, (XD + 20, Y3 - 420, 0.94)),
], drift=6, seed=17.0)


def _bg(ctx, t, cam):
    ctx.set_source(lin(0, 0, 0, 1080, [(0, "#7FC4FF"), (0.6, "#CDE9FF"), (1, "#FFF1E3")]))
    ctx.paint()
    with view(ctx, cam, 0.3):
        R = rng(3)
        for i in range(26):
            x = R.uniform(-800, 4800)
            y = R.uniform(-600, 3600)
            s = R.uniform(0.6, 1.6)
            _cloud(ctx, x + math.sin(t * 0.2 + i) * 20, y, 160 * s, 0.55)
    with view(ctx, cam, 1.0):
        for (x0, x1, y) in ((-300, 2300, Y1), (-300, 4400, Y2), (1200, 4800, Y3)):
            _deck(ctx, x0, x1, y)


def _cloud(ctx, x, y, r, a):
    for (dx, dy, k) in ((-0.9, 0.15, 0.62), (-0.35, -0.2, 0.85), (0.3, -0.1, 0.75), (0.85, 0.18, 0.55),
                        (0.0, 0.25, 0.7)):
        circle(ctx, x + dx * r, y + dy * r, k * r)
    setc(ctx, "#FFFFFF", a)
    ctx.fill()


def _deck(ctx, x0, x1, y):
    """云台：一条蓬松的云地面。"""
    ctx.rectangle(x0, y, x1 - x0, 60)
    fill(ctx, "#FFFFFF", 0.92)
    n = int((x1 - x0) / 110)
    for i in range(n + 1):
        circle(ctx, x0 + i * 110, y + 8, 62 + (i % 3) * 10)
    fill(ctx, "#FFFFFF", 0.95)
    ctx.rectangle(x0 - 60, y + 40, x1 - x0 + 120, 40)
    ctx.set_source(lin(0, y + 40, 0, y + 80, [(0, "#E3EEFF", 0.9), (1, "#E3EEFF", 0)]))
    ctx.fill()


def _part_a(ctx, t):
    a = 1 - smooth(prog(t, 4.6, 5.2))
    if a <= 0:
        return
    v = MapView(1240, 470, 9.0, lon0=-98, lat0=40)
    world_dots(ctx, v, a * smooth(prog(t, 0.3, 1.0)), "#3B6FB6", 0.35, 2.0,
               hi={(-98.0, 39.0, 24.0): "#FF9F68"}, clip=(700, 120, 1800, 820))
    q = smooth(prog(t, 1.0, 1.6))
    glow(ctx, 1240, 470, 420, "#FFB27A", 0.4 * q * a)
    for k in range(3):
        ring_burst(ctx, t, 1.4 + k * 0.6, 1240, 470, 40, 360, "#FFFFFF", 1.0, 6, 0.6 * a)
    text(ctx, "为什么是美国？", 1240, 170, 76, "#1E2B4A", a * q, "black")


def _part_bc(ctx, t):
    a = smooth(prog(t, 4.6, 5.3))
    if a <= 0:
        return
    mx, my = XB + 260, Y2 - 440
    vs = 1 - smooth(prog(t, 10.2, 10.9))
    # 对手：Gemini（右侧，VS 后淡出到一边）
    mv = smooth(prog(t, 10.2, 10.9))
    gx, gy = lerp(mx + 380, mx + 700, mv), lerp(my, my + 300, mv)
    gk = pop(t, 6.6, 0.5)
    if gk > 0:
        with at(ctx, gx, gy, gk * (1 - 0.45 * mv)):
            glow(ctx, 0, 0, 200, "#7A8CFF", 0.35)
            gemini_star(ctx, 0, 0, 110, a, t * 0.3)
            name_card(ctx, "Gemini", 0, 170, "#4C8DFF", 30, a, 1.0, sub="谷歌 · 对手")
    mxx = lerp(mx - 380, mx, smooth(prog(t, 10.2, 10.9)))
    mk = pop(t, 5.4, 0.5)
    if mk > 0:
        with at(ctx, mxx, my, mk):
            glow(ctx, 0, 0, 230, "#8B6CFF", 0.35)
            ic_muse(ctx, 0, 0, 200, a, t)
        name_card(ctx, "Muse", mxx, my + 170, "#0866FF", 30, a, mk, sub="Meta 的个人智能体")
    if vs > 0 and t > 7.3:
        q = pop(t, 7.3, 0.5)
        with at(ctx, mx, my, q * vs):
            for i in range(8):
                ang = i / 8 * TAU + t
                line(ctx, math.cos(ang) * 60, math.sin(ang) * 60, math.cos(ang) * 110, math.sin(ang) * 110, 6,
                     "#FFD84D", vs)
            text(ctx, "VS", 0, 0, 90, "#E5484D", vs, "black", outline="#FFFFFF", outline_w=8)
        tag(ctx, "直接对手", mx, my - 150, 30, "#FFFFFF", "#E5484D", vs * q)
    # Muse 连上各家服务
    apps = [("Gmail", ic_gmail, "谷歌"), ("谷歌日历", ic_calendar, "谷歌"), ("谷歌文档", ic_docs, "谷歌"),
            ("Outlook", None, "微软"), ("Instagram", ic_instagram, "Meta 自家")]
    for i, (nm, fn, owner) in enumerate(apps):
        st = 10.8 + i * 1.05
        q = pop(t, st, 0.5)
        if q <= 0:
            continue
        ang = math.pi + (i + 0.5) / len(apps) * math.pi
        ang = -math.pi * 0.95 + i * (math.pi * 0.9 / (len(apps) - 1))
        r = 420
        ax, ay = mx + math.cos(ang) * r * 1.25, my + math.sin(ang) * r * 0.62 + 40
        u = ease_out(prog(t, st + 0.1, st + 0.6))
        stroke_pts(ctx, [(mx, my), (lerp(mx, ax, u), lerp(my, ay, u))], 6, "#FF9F68", 0.85 * a)
        with at(ctx, ax, ay, q):
            if fn is None:
                app_tile(ctx, 0, 0, 110, "#0F6CBD", "O")
            else:
                fn(ctx, 0, 0, 110, 1.0, t)
        text(ctx, nm, ax, ay + 84, 28, "#1E2B4A", q * a, "black")
        text(ctx, owner, ax, ay + 116, 22, "#E5484D" if owner != "Meta 自家" else "#0866FF", q * a, "bold")
        c = clamp((t - st - 0.6) / 0.3)
        if c > 0:
            circle(ctx, ax + 46, ay - 46, 20)
            fill(ctx, "#3CCB7F", c)
            check_mark(ctx, ax + 46, ay - 46, 24, "#FFFFFF", c)
    if t > 15.6:
        tag(ctx, "对手家的服务，照样能连", mx, my + 330, 32, "#FFFFFF", "#FF9F68", smooth(prog(t, 15.6, 16.0)))


GAPPS = [("Gmail", "#EA4335", "M"), ("地图", "#34A853", "图"), ("浏览器", "#FBBC05", "C"), ("视频", "#FF0000", "▶"),
         ("文档", "#4285F4", "文"), ("翻译", "#4C8DFF", "译"), ("相册", "#F4B400", "相"), ("硬盘", "#0F9D58", "盘")]


def _part_d(ctx, t):
    a = smooth(prog(t, 16.6, 17.4))
    if a <= 0:
        return
    px, py = XD + 160, Y2 - 400
    sx, sy, sw, sh = iphone(ctx, px, py, 640, a)
    # 主屏幕上的谷歌全家桶
    ctx.save()
    rrect(ctx, sx, sy, sw, sh, 24)
    ctx.clip()
    ctx.set_source(lin(0, sy, 0, sy + sh, [(0, "#E9F1FF", a), (1, "#FCEFFF", a)]))
    ctx.paint()
    for i, (nm, c, ch) in enumerate(GAPPS):
        q = pop(t, 18.6 + i * 0.16, 0.4)
        if q <= 0:
            continue
        x = sx + 58 + (i % 3) * 90
        y = sy + 70 + (i // 3) * 120
        with at(ctx, x, y, q):
            rrect(ctx, -32, -32, 64, 64, 16)
            fill(ctx, c, a)
            text(ctx, ch, 0, 1, 30, "#FFFFFF", a, "black")
        text(ctx, nm, x, y + 50, 16, "#2B2233", a * q, "bold")
    # Siri 光球
    sk = smooth(prog(t, 22.0, 22.6))
    if sk > 0:
        cx, cy = sx + sw / 2, sy + sh - 90
        glow(ctx, cx, cy, 120, "#B98CFF", 0.7 * sk)
        circle(ctx, cx, cy, 46 * sk)
        ctx.set_source(rad(cx - 12, cy - 12, 4, 50, [(0, "#FFFFFF", sk), (0.5, "#C3A3FF", sk), (1, "#5F7CFF", sk)]))
        ctx.fill()
        gemini_star(ctx, cx, cy, 26 * sk, sk, t)
    ctx.restore()
    # 苹果 VS 谷歌
    for i, (nm, c, dx) in enumerate((("苹果", "#8E8E93", -420), ("谷歌", "#4285F4", 420))):
        q = pop(t, 17.8 + i * 0.3, 0.5)
        if q > 0:
            name_card(ctx, nm, px + dx, py - 230, c, 34, a, q)
    if t > 18.2:
        q = pop(t, 18.2, 0.5) * (1 - smooth(prog(t, 20.6, 21.0)))
        if q > 0:
            tag(ctx, "斗了十几年", px, py - 380, 30, "#FFFFFF", "#E5484D", q)
    if t > 19.6:
        tag(ctx, "iPhone 上照样装谷歌全家桶", px - 420, py + 40, 26, "#1E2B4A", "#FFFFFF",
            smooth(prog(t, 19.6, 20.0)), 0.95)
    if sk > 0:
        tag(ctx, "2026.1 宣布：新 Siri 由 Gemini 驱动", px + 420, py + 160, 26, "#FFFFFF", "#6A4FD8", sk)


NODES = {"微软": ("#00A4EF", -560, -250), "OpenAI": ("#10A37F", -560, 70), "Anthropic": ("#D97757", 0, 220),
         "亚马逊": ("#FF9900", 560, -250), "谷歌": ("#4285F4", 560, 70), "Meta": ("#0866FF", -170, -330),
         "Scale AI": ("#6A4FD8", 330, -400)}
EDGES = [  # (起, 终, 标签, 种类, 出现时间)
    ("微软", "OpenAI", "投资", "inv", 25.6), ("微软", "Anthropic", "用它的模型", "co", 27.0),
    ("亚马逊", "Anthropic", "投资", "inv", 28.6), ("谷歌", "Anthropic", "投资", "inv", 29.6),
    ("Meta", "Scale AI", "入股 143 亿美元", "inv", 31.4), ("Scale AI", "Meta", "创始人加盟", "co", 33.0),
    ("OpenAI", "Anthropic", "竞争", "comp", 27.6), ("谷歌", "OpenAI", "竞争", "comp", 30.4),
    ("Meta", "谷歌", "竞争", "comp", 32.2),
]
EC = {"inv": "#F5B83D", "co": "#3CCB7F", "comp": "#E5484D"}


def _part_e(ctx, t):
    a = smooth(prog(t, 24.8, 25.6)) * (1 - 0.72 * smooth(prog(t, 36.4, 37.2)))
    if a <= 0:
        return
    cx, cy = XD + 120, Y3 - 470
    for (s0, s1, lab, kind, st) in EDGES:
        u = ease_out(prog(t, st, st + 0.7))
        if u <= 0:
            continue
        c0, x0, y0 = NODES[s0]
        c1, x1, y1 = NODES[s1]
        p0, p1 = (cx + x0, cy + y0), (cx + x1, cy + y1)
        bend = 0.18 if kind != "comp" else -0.12
        mx_, my_ = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        d = math.dist(p0, p1)
        nx, ny = -(p1[1] - p0[1]) / d, (p1[0] - p0[0]) / d
        ctrl = (mx_ + nx * d * bend, my_ + ny * d * bend)
        pts = bezier_pts(p0, ctrl, ctrl, p1, 40)
        seg = polyline_partial(pts, 0, u)
        if kind == "comp":
            ctx.save()
            ctx.set_dash((16, 12))
            stroke_pts(ctx, seg, 5, EC[kind], 0.85 * a)
            ctx.restore()
        else:
            stroke_pts(ctx, seg, 7, EC[kind], 0.9 * a)
        if u > 0.6:
            (lx, ly), _ = point_on(pts, 0.5)
            tag(ctx, lab, lx, ly, 28, "#FFFFFF", EC[kind], a * smooth((u - 0.6) / 0.3))
    for nm, (c, x, y) in NODES.items():
        q = pop(t, 25.4 + list(NODES).index(nm) * 0.1, 0.45)
        if q > 0:
            name_card(ctx, nm, cx + x, cy + y, c, 32, a, q, w=230 if len(nm) > 4 else 190)
    lg = smooth(prog(t, 26.0, 26.5))
    if lg > 0:
        for i, (k, lab) in enumerate((("inv", "投资"), ("co", "合作"), ("comp", "竞争"))):
            x = cx - 420 + i * 220
            y = cy + 400
            line(ctx, x - 70, y, x - 20, y, 7, EC[k], lg * a)
            text(ctx, lab, x + 10, y, 26, "#1E2B4A", lg * a, "black", "l")


def _part_f(ctx, t):
    a = smooth(prog(t, 36.4, 37.2))
    if a <= 0:
        return
    cx, cy = XD + 120, Y3 - 470
    # 三股线拧成一股绳（画面正中）
    x0, x1 = cx - 700, cx + 700
    ry = cy + 60
    ctx.rectangle(x0 - 80, ry - 150, x1 - x0 + 160, 300)
    ctx.set_source(lin(0, ry - 150, 0, ry + 150, [(0, "#FFFFFF", 0), (0.5, "#FFFFFF", 0.65 * a), (1, "#FFFFFF", 0)]))
    ctx.fill()
    for k, (c, ph) in enumerate((("#E5484D", 0.0), ("#3CCB7F", TAU / 3), ("#F5B83D", 2 * TAU / 3))):
        pts = []
        for i in range(121):
            u = i / 120
            x = lerp(x0, x1, u)
            y = ry + math.sin(u * TAU * 3 + ph + t * 1.5) * 40
            pts.append((x, y))
        stroke_pts(ctx, polyline_partial(pts, 0, ease_io(prog(t, 36.8, 38.6))), 16, c, a)
    labels = [("竞争", "#E5484D"), ("合作", "#3CCB7F"), ("投资", "#F5B83D")]
    for i, (lab, c) in enumerate(labels):
        q = pop(t, 37.0 + i * 0.35, 0.45)
        if q > 0:
            with at(ctx, cx - 300 + i * 300, ry - 110, q):
                rrect(ctx, -90, -38, 180, 76, 38)
                fill(ctx, c)
                text(ctx, lab, 0, 0, 40, "#FFFFFF", 1, "black")


def draw(ctx, t):
    cam = CAM.at(t)
    _bg(ctx, t, cam)
    with view(ctx, cam, 1.0):
        _part_a(ctx, t)
        _part_bc(ctx, t)
        _part_d(ctx, t)
        _part_e(ctx, t)
        _part_f(ctx, t)
        P.draw(ctx, t)


def sfx():
    out = [
        (1.0, "impact_soft", {"gain": 0.4}), (1.1, "shimmer", {"dur": 1.2, "gain": 0.3}),
        (4.0, "boing", {"gain": 0.3}), (4.3, "fall", {"dur": 0.8, "gain": 0.3}), (5.1, "thud", {"gain": 0.3}),
        (5.4, "pop", {"gain": 0.3}), (6.6, "pop", {"gain": 0.3, "pitch": 1.2}),
        (7.3, "zap", {"dur": 0.8, "gain": 0.3}),
        (10.2, "whoosh_short", {"gain": 0.3}),
    ]
    for i in range(5):
        out += [(10.8 + i * 1.05, "connect", {"gain": 0.3, "pitch": 1.0 + i * 0.08}),
                (11.45 + i * 1.05, "check", {"gain": 0.22, "pitch": 1.0 + i * 0.08})]
    out += [
        (16.6, "whoosh_short", {"gain": 0.3}),
        (17.8, "pop", {"gain": 0.3}), (18.1, "pop", {"gain": 0.3, "pitch": 1.2}),
        (18.6, "shuffle", {"dur": 1.3, "gain": 0.2}),
        (21.8, "surprise", {"gain": 0.35}), (22.0, "powerup", {"gain": 0.35}),
        (24.4, "boing", {"gain": 0.3}), (24.7, "fall", {"dur": 0.8, "gain": 0.3}), (25.5, "thud", {"gain": 0.3}),
    ]
    for (_, _, _, kind, st) in EDGES:
        out.append((st, "zip" if kind != "comp" else "swish", {"gain": 0.22}))
    out += [(36.8, "stretch", {"dur": 1.8, "gain": 0.25}), (37.0, "pop", {"gain": 0.3}),
            (37.35, "pop", {"gain": 0.3, "pitch": 1.2}), (37.7, "pop", {"gain": 0.3, "pitch": 1.4}),
            (40.0, "chime", {"gain": 0.3})]
    return out
