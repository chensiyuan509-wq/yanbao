"""第七章 · 竞合：在竞争中合作。

A Google VS Meta → Muse 插进 Google 的开放接口
B 苹果 VS 谷歌 → Gemini 驱动新 Siri（2026.1 宣布）
C 各家接入 Anthropic 的 MCP → 交由 Linux 基金会（AAIF）共同维护
D 竞争与合作首尾相接，蛋糕越做越大
"""
import math

from ..core import (TAU, W, H, Cam, at, circle, clamp, ease_back, ease_in, ease_io, ease_out,
                    fill, glow, kf, lerp, line, lin, pop, poly, prog, rad, rng, rrect, setc, smooth,
                    star4, text, text_w, view, sparkle_burst, ring_burst, stroke_pts, bezier_pts,
                    polyline_partial, point_on, arrow_head)
from ..icons import ic_building, ic_cake, ic_muse, ic_plug, google_word
from ..mascot import Puppet
from ..ui import card, pill

DUR = 26.0
CHAPTER = ("07", "竞合：在竞争中合作")

SUBS = [
    (0.8, 6.6, "有意思的是：Google 和 Meta 是广告市场的老对手，接口却照样对它开放。"),
    (6.8, 12.2, "苹果和谷歌是手机上的对手，新 Siri 却选用了 {Gemini}。"),
    (12.4, 19.6, "Anthropic 发明的 {MCP} 协议，对手们纷纷接入，如今交由 Linux 基金会共同维护。"),
    (19.8, 25.6, "在竞争中合作，在合作中竞争：先把{蛋糕做大}，再各凭本事。"),
]

AX, BX, CX, DX = 960, 2880, 4800, 6720
T_PLUG = 3.1
T_GEM = 8.9
T_LF = 16.5

P = (Puppet(AX, 905, 0.55, "curious", seed=12.7)
     .look(0, -1.0, -0.6).look(1.0, 1.0, -0.6)
     .expr(1.6, "shock").shake(1.7, 0.6, 0.06).look(2.0, -0.5, -0.8)
     .expr(T_PLUG + 0.5, "happy").look(T_PLUG + 0.5, 0, -0.9).nod(T_PLUG + 0.8)
     .move(6.5, 7.3, BX, 905, walk=False).hop(6.5, 150, 0.8).land(7.3)
     .expr(7.4, "curious").look(7.4, -1.0, -0.6).look(8.2, 1.0, -0.6)
     .expr(T_GEM + 0.8, "surprised").look(T_GEM + 0.8, -1.0, -0.9).expr(10.6, "excited")
     .move(12.3, 13.1, CX - 560, 905, walk=False).hop(12.3, 150, 0.8).land(13.1)
     .expr(13.2, "curious").look(13.2, 1.0, -0.7).expr(15.6, "happy")
     .expr(T_LF + 0.6, "proud")
     .move(19.5, 20.3, DX - 520, 905, walk=False).hop(19.5, 150, 0.8).land(20.3)
     .expr(20.4, "excited").look(20.4, 1.0, -0.6).hop(22.6, 50).fx(23.0, ("heart",)))

CAM = Cam([
    (0.0, (AX, 520, 1.0)), (6.4, (AX + 20, 515, 1.04)),
    (7.3, (BX, 520, 1.0), ease_io), (12.2, (BX + 20, 515, 1.04)),
    (13.1, (CX, 520, 1.0), ease_io), (19.4, (CX + 20, 520, 1.03)),
    (20.3, (DX, 520, 1.0), ease_io), (26.0, (DX + 20, 515, 1.05)),
], drift=5, seed=37.0)


def draw(ctx, t):
    cam = CAM.at(t)
    ctx.set_source(lin(0, 0, W, H, [(0, "#FFE9DF"), (0.5, "#F1E8FA"), (1, "#E1EDFF")]))
    ctx.paint()
    with view(ctx, cam, 0.4):
        from ..core import bokeh
        bokeh(ctx, t, 22, 91, ("#FF9F68", "#8B6CFF", "#4C8DFF"), area=(-400, -200, W + 3600, H + 400),
              r=(40, 120), a=(0.06, 0.14))
    with view(ctx, cam):
        lo, hi = cam[0] - 1500, cam[0] + 1500
        if lo < AX < hi:
            part_a(ctx, t)
        if lo < BX < hi:
            part_b(ctx, t)
        if lo < CX < hi:
            part_c(ctx, t)
        if lo < DX < hi:
            part_d(ctx, t)
        P.draw(ctx, t)


def vs_badge(ctx, x, y, t, t0, label):
    k = pop(t, t0, 0.5)
    if k <= 0:
        return
    with at(ctx, x, y, k):
        glow(ctx, 0, 0, 160, "#FF5A5F", 0.35)
        circle(ctx, 0, 0, 74)
        ctx.set_source(lin(0, -74, 0, 74, [(0, "#FF7A59"), (1, "#E5484D")]))
        ctx.fill()
        text(ctx, "VS", 0, 0, 64, "#FFFFFF", 1, "black")
    # 闪电
    R = rng(int(t * 12))
    if t0 + 0.2 < t < t0 + 2.2:
        for side in (-1, 1):
            pts = [(x + side * 90, y)]
            for j in range(1, 6):
                pts.append((x + side * (90 + j * 34), y + R.uniform(-40, 40)))
            stroke_pts(ctx, pts, 6, "#FFC65C", 0.9)
            stroke_pts(ctx, pts, 2, "#FFFFFF", 0.9)
    lk = pop(t, t0 + 0.3, 0.45)
    if lk > 0:
        with at(ctx, x, y + 130, lk):
            pill(ctx, label, 0, 0, 30, "#FFFFFF", "#2B2233", 1.0, 0.85)


def _company(ctx, kind, x, y, k, a=1.0):
    with at(ctx, x, y, k):
        card(ctx, -230, -110, 460, 220, 44, "#FFFFFF", a, shadow=0.22)
        if kind == "google":
            google_word(ctx, 0, 0, 84, a)
        elif kind == "meta":
            text(ctx, "Meta", 0, 0, 84, "#0866FF", a, "black")
        elif kind == "apple":
            text(ctx, "苹果", 0, 0, 80, "#1D1D1F", a, "black")
        elif kind == "google_cn":
            google_word(ctx, 0, 0, 84, a)


def part_a(ctx, t):
    kg = ease_back(prog(t, 0.3, 0.9), 1.3)
    km = ease_back(prog(t, 0.5, 1.1), 1.3)
    gx, mx, y = AX - 470, AX + 470, 360
    _company(ctx, "google", gx - (1 - kg) * 300, y, kg)
    _company(ctx, "meta", mx + (1 - km) * 300, y, km)
    vs_badge(ctx, AX, y, t, 1.4, "广告市场的老对手")
    # 开放接口：插座在 Google 下方，Muse 的插头从 Meta 那边连过来
    pk = pop(t, 2.6, 0.45)
    if pk > 0:
        sx, sy = gx, y + 250
        with at(ctx, sx, sy, pk):
            rrect(ctx, -170, -40, 340, 80, 40)
            fill(ctx, "#4285F4")
            text(ctx, "Gmail · 文档 · 表格 API", 0, 0, 27, "#FFFFFF", 1, "black")
        line(ctx, gx, y + 110, gx, sy - 40, 6, "#4285F4", pk)
        mk = pop(t, 2.8, 0.45)
        ic_muse(ctx, mx, y + 250, 110 * mk, 1.0, t)
        u = ease_io(prog(t, T_PLUG - 0.1, T_PLUG + 0.6))
        pts = bezier_pts((mx - 60, y + 250), (mx - 300, y + 420), (sx + 400, y + 420), (sx + 175, sy), 40)
        seg = polyline_partial(pts, u)
        stroke_pts(ctx, seg, 9, "#8B6CFF", 0.85)
        if u > 0:
            (px, py), ang = point_on(pts, u)
            ic_plug(ctx, px, py, 70, 1.0, t, "#8B6CFF", ang + math.pi / 2)
        if t > T_PLUG + 0.6:
            for d in range(4):
                v = ((t - T_PLUG) * 0.5 + d / 4) % 1
                (qx, qy), _ = point_on(pts, 1 - v)
                glow(ctx, qx, qy, 20, "#B6A4FF", 0.9 * math.sin(v * math.pi))
            ring_burst(ctx, t, T_PLUG + 0.6, sx + 175, sy, 20, 120, "#8B6CFF", 0.5, 7)
            ok = pop(t, T_PLUG + 0.7, 0.45)
            with at(ctx, AX, 150, ok):
                pill(ctx, "对手的智能体，照样能接入", 0, 0, 36, "#FFFFFF", "#3CCB7F", 1.0, 1.0)


def _phone(ctx, x, y, h, kind, t, glow_siri=0.0):
    w = h * 0.5
    from ..core import box_shadow
    box_shadow(ctx, x - w / 2, y - h / 2, w, h, w * 0.2, blur=40, a=0.3, dy=16)
    rrect(ctx, x - w / 2, y - h / 2, w, h, w * 0.2)
    fill(ctx, "#1D1D1F" if kind == "apple" else "#2F3A4A")
    sx, sy, sw, sh = x - w / 2 + 12, y - h / 2 + 12, w - 24, h - 24
    rrect(ctx, sx, sy, sw, sh, w * 0.16)
    ctx.set_source(lin(0, sy, 0, sy + sh, [(0, "#EEF2FF" if kind == "apple" else "#E9F7EE"), (1, "#FFFFFF")]))
    ctx.fill()
    if kind == "apple":
        rrect(ctx, x - 40, sy + 14, 80, 22, 11)
        fill(ctx, "#1D1D1F")
    else:
        circle(ctx, x, sy + 24, 9)
        fill(ctx, "#2F3A4A")
    for j in range(3):
        for i in range(3):
            rrect(ctx, sx + 26 + i * (sw - 52) / 3 + 4, sy + 70 + j * 74, (sw - 52) / 3 - 8, 54, 14)
            fill(ctx, ["#FF9F68", "#4C8DFF", "#3CCB7F", "#8B6CFF", "#FFC65C", "#FF6B9A"][(i + j * 3 + (kind == "apple")) % 6], 0.85)
    if glow_siri > 0:
        cx, cy = x, sy + sh - 90
        glow(ctx, cx, cy, 130, "#8B6CFF", 0.6 * glow_siri)
        circle(ctx, cx, cy, 46 * glow_siri)
        ctx.set_source(lin(cx - 46, cy - 46, cx + 46, cy + 46, [(0, "#3D7BFF"), (0.5, "#B05CFF"), (1, "#FF5FA2")]))
        ctx.fill()
        text(ctx, "Siri", cx, cy + 76, 30, "#2B2233", glow_siri, "black")


def gemini_star(ctx, x, y, r, a=1.0, rot=0.0):
    glow(ctx, x, y, r * 2.4, "#7A8CFF", 0.5 * a)
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    k = r * 0.16
    ctx.move_to(0, -r)
    ctx.curve_to(k * 0.4, -k, k, -k * 0.4, r, 0)
    ctx.curve_to(k, k * 0.4, k * 0.4, k, 0, r)
    ctx.curve_to(-k * 0.4, k, -k, k * 0.4, -r, 0)
    ctx.curve_to(-k, -k * 0.4, -k * 0.4, -k, 0, -r)
    ctx.set_source(lin(-r, -r, r, r, [(0, "#4C8DFF", a), (0.6, "#9B72FF", a), (1, "#FF7AA8", a)]))
    ctx.fill()
    ctx.restore()


def part_b(ctx, t):
    a = smooth(prog(t, 6.3, 7.0))
    if a <= 0:
        return
    ax, gx, y = BX - 460, BX + 460, 400
    ka = ease_back(prog(t, 6.9, 7.5), 1.3)
    kg = ease_back(prog(t, 7.1, 7.7), 1.3)
    siri = smooth(prog(t, T_GEM + 0.9, T_GEM + 1.4))
    if ka > 0:
        with at(ctx, ax, y, ka):
            _phone(ctx, 0, 0, 520, "apple", t, siri)
        pill(ctx, "苹果 iPhone", ax, y + 320, 32, "#FFFFFF", "#1D1D1F", ka, 0.9)
    if kg > 0:
        with at(ctx, gx, y, kg):
            _phone(ctx, 0, 0, 520, "android", t)
        pill(ctx, "谷歌 Android", gx, y + 320, 32, "#FFFFFF", "#34A853", kg, 0.95)
    vs_badge(ctx, BX, y - 40, t, 7.8, "手机市场的对手")
    # Gemini 星光从谷歌飞向 iPhone
    u = prog(t, T_GEM, T_GEM + 1.0)
    if 0 < u < 1:
        e = ease_io(u)
        x = lerp(gx, ax, e)
        yy = lerp(y - 60, y + 120, e) - math.sin(u * math.pi) * 330
        gemini_star(ctx, x, yy, 54, 1.0, u * 3)
        for q in range(8):
            v = clamp(e - q * 0.03)
            gx2 = lerp(gx, ax, v)
            gy2 = lerp(y - 60, y + 120, v) - math.sin(v * math.pi) * 330
            star4(ctx, gx2, gy2, 14 * (1 - q / 8), "#C9B8FF", 0.7 * (1 - q / 8))
    elif u <= 0 and t > 8.3:
        gemini_star(ctx, gx, y - 60, 54 * pop(t, 8.3, 0.45), 1.0, t)
        text(ctx, "Gemini", gx, y - 140, 34, "#5B4E8C", smooth(prog(t, 8.4, 8.7)), "black")
    sparkle_burst(ctx, t, T_GEM + 1.0, ax, y + 160, 12, 220, "#C9B8FF", 0.9, 5, 20)
    nk = pop(t, T_GEM + 1.5, 0.5)
    if nk > 0:
        with at(ctx, BX, 92, nk):
            pill(ctx, "2026 年 1 月：苹果宣布新 Siri 由 Gemini 驱动", 0, 0, 34, "#FFFFFF", "#6D4FE0", 1.0, 1.0)


MCP_PEERS = [("OpenAI", "#19C39C", -150), ("Google", "#4285F4", -30), ("微软", "#00A4EF", 30),
             ("AWS", "#FF9900", 150), ("Anthropic", "#E88E64", 210)]


def part_c(ctx, t):
    a = smooth(prog(t, 12.0, 12.8))
    if a <= 0:
        return
    hx, hy = CX + 40, 440
    lf = smooth(prog(t, T_LF, T_LF + 0.8))
    # 基金会大楼（后景）
    if lf > 0:
        glow(ctx, hx, hy, 640, "#FFE3A3", 0.35 * lf)
        with at(ctx, hx, hy - 20, 0.9 + 0.1 * ease_back(prog(t, T_LF, T_LF + 0.7))):
            ic_building(ctx, 0, 0, 900, lf * 0.9, t, "#CDBFEA")
        pill(ctx, "Linux 基金会 · 智能体 AI 基金会（AAIF）", hx, 860 - 40, 34, "#FFFFFF", "#5B4E8C", lf, 0.95,
             weight="black")
        tk = pop(t, T_LF + 0.6, 0.45)
        with at(ctx, hx, 120, tk):
            pill(ctx, "2025 年 12 月：MCP 捐给 Linux 基金会，多家共同维护", 0, 0, 30, "#FFFFFF", "#2B2233", 1.0, 0.85)
    # 接入的公司
    for i, (name, col, deg) in enumerate(MCP_PEERS):
        ang = math.radians(deg - 90)
        R = 390
        px, py = hx + math.cos(ang) * R * 1.25, hy + math.sin(ang) * R * 0.75 + 30
        if name == "Anthropic":
            px, py = hx - 520, hy + 180
        k = pop(t, 12.9 + i * 0.25, 0.45)
        if k <= 0:
            continue
        t0 = 13.6 + i * 0.35 if name != "Anthropic" else 12.9
        lp = ease_out(prog(t, t0, t0 + 0.45))
        if lp > 0:
            x1, y1 = lerp(px, hx, lp * 0.82), lerp(py, hy, lp * 0.82)
            stroke_pts(ctx, [(px, py), (x1, y1)], 8, col, 0.8)
            ic_plug(ctx, x1, y1, 54, 1.0, t, col, math.atan2(hy - py, hx - px) + math.pi / 2)
            if lp >= 1:
                ring_burst(ctx, t, t0 + 0.45, x1, y1, 10, 70, col, 0.4, 5)
        with at(ctx, px, py, k):
            w = text_w(ctx, name, 38, "black") + 90
            rrect(ctx, -w / 2, -42, w, 84, 42)
            fill(ctx, "#FFFFFF")
            circle(ctx, -w / 2 + 38, 0, 13)
            fill(ctx, col)
            text(ctx, name, 16, 0, 38, "#2B2233", 1, "black")
        if name == "Anthropic":
            ik = pop(t, 13.3, 0.45)
            with at(ctx, px, py + 74, ik):
                pill(ctx, "发明者 · 2024.11 开源", 0, 0, 24, "#FFFFFF", "#E88E64", 1.0, 1.0)
    # MCP 枢纽
    k = ease_back(prog(t, 12.5, 13.1), 1.5)
    if k > 0:
        glow(ctx, hx, hy, 260, "#8B6CFF", 0.4)
        with at(ctx, hx, hy, k):
            rrect(ctx, -120, -120, 240, 240, 60)
            ctx.set_source(lin(0, -120, 0, 120, [(0, "#A58BFF"), (1, "#6D4FE0")]))
            ctx.fill()
            rrect(ctx, -70, 30, 140, 46, 23)
            fill(ctx, "#4B33B5")
            for j in range(5):
                rrect(ctx, -52 + j * 22, 44, 14, 18, 3)
                fill(ctx, "#E8E0FF")
            text(ctx, "MCP", 0, -26, 66, "#FFFFFF", 1, "black")
        lk = smooth(prog(t, 13.1, 13.5)) * (1 - lf)
        text(ctx, "模型上下文协议：AI 的「万能插座」", hx, hy + 175, 30, "#4B3A8C", lk, "black")


def part_d(ctx, t):
    a = smooth(prog(t, 19.4, 20.2))
    if a <= 0:
        return
    cx, cy = DX + 60, 430
    grow = ease_out(prog(t, 20.6, 23.0))
    size = 170 + 200 * grow
    # 竞争 / 合作 两条首尾相接的弧形箭头
    rot = (t - 20.0) * 1.2
    R = 330
    for j, (lab, col) in enumerate((("竞争", "#FF7A59"), ("合作", "#4C8DFF"))):
        a0 = rot + j * math.pi + 0.25
        a1 = a0 + math.pi - 0.5
        dp = ease_out(prog(t, 20.3 + j * 0.2, 21.0 + j * 0.2))
        if dp <= 0:
            continue
        pts = [(cx + math.cos(lerp(a0, a1, v / 30)) * R, cy + math.sin(lerp(a0, a1, v / 30)) * R * 0.85) for v in range(31)]
        seg = polyline_partial(pts, dp)
        stroke_pts(ctx, seg, 22, col, 0.85 * a)
        if dp > 0.95:
            (ex, ey), (qx, qy) = pts[-1], pts[-2]
            arrow_head(ctx, ex, ey, math.atan2(ey - qy, ex - qx), 58, col, 0.9 * a)
        mid = pts[15]
        pill(ctx, lab, mid[0], mid[1], 36, "#FFFFFF", col, a * dp, 1.0, weight="black")
    glow(ctx, cx, cy, size * 1.4, "#FFD7E2", 0.6 * a)
    ic_cake(ctx, cx, cy + 10, size, a, t)
    sparkle_burst(ctx, t, 23.0, cx, cy, 14, 380, "#FFC65C", 1.0, 3, 24)
    # 蛋糕周围的公司
    names = [("Google", "#4285F4"), ("Meta", "#0866FF"), ("苹果", "#1D1D1F"), ("OpenAI", "#19C39C"),
             ("Anthropic", "#E88E64"), ("微软", "#00A4EF")]
    for i, (n, col) in enumerate(names):
        k = pop(t, 23.2 + i * 0.12, 0.45)
        if k <= 0:
            continue
        ang = -math.pi / 2 + i * TAU / 6 + 0.5
        px, py = cx + math.cos(ang) * 520, cy + math.sin(ang) * 330
        with at(ctx, px, py, k):
            from ..ui import chip
            chip(ctx, n, 0, 0, 30, col, a)


def sfx():
    out = [(0.3, "swish", {"gain": 0.35}), (0.5, "swish", {"gain": 0.3}),
           (1.4, "zap", {"dur": 1.6, "gain": 0.45}), (1.45, "impact_soft", {"gain": 0.5}),
           (2.6, "pop", {"gain": 0.35, "pitch": 1.0}), (2.8, "pop", {"gain": 0.35, "pitch": 1.2}),
           (T_PLUG - 0.1, "whoosh_short", {"gain": 0.35}), (T_PLUG + 0.6, "plug", {"gain": 0.6}),
           (T_PLUG + 0.7, "success", {"gain": 0.4}), (T_PLUG + 1.0, "stream", {"dur": 2.4, "gain": 0.15}),
           (6.5, "hop", {"gain": 0.3}), (7.3, "thud", {"gain": 0.25}),
           (6.9, "swish", {"gain": 0.3}), (7.1, "swish", {"gain": 0.3}),
           (7.8, "zap", {"dur": 1.4, "gain": 0.4}), (7.85, "impact_soft", {"gain": 0.4}),
           (8.3, "sparkle", {"dur": 0.8, "gain": 0.3}),
           (T_GEM, "whoosh", {"dur": 1.0, "gain": 0.4}), (T_GEM + 0.95, "shimmer", {"dur": 1.4, "gain": 0.4}),
           (T_GEM + 1.5, "pop", {"gain": 0.35, "pitch": 1.0}),
           (12.3, "hop", {"gain": 0.3}), (13.1, "thud", {"gain": 0.25}),
           (12.5, "pop", {"gain": 0.45, "pitch": 0.8})]
    for i, (name, col, deg) in enumerate(MCP_PEERS):
        t0 = 13.6 + i * 0.35 if name != "Anthropic" else 12.9
        out.append((12.9 + i * 0.25, "pop", {"gain": 0.25, "pitch": 1.0 + i * 0.08}))
        out.append((t0 + 0.45, "plug", {"gain": 0.45, "pitch": 1.0 + i * 0.05}))
    out += [(T_LF, "whoosh", {"dur": 0.9, "gain": 0.35}), (T_LF + 0.3, "impact_soft", {"gain": 0.45}),
            (T_LF + 0.6, "chime", {"gain": 0.35}), (T_LF + 1.2, "sparkle", {"dur": 1.6, "gain": 0.2}),
            (19.5, "hop", {"gain": 0.3}), (20.3, "thud", {"gain": 0.25}),
            (20.3, "swish", {"gain": 0.3}), (20.5, "swish", {"gain": 0.3}),
            (20.6, "rise", {"gain": 0.35, "dur": 2.4}), (23.0, "pop_big", {"gain": 0.5}),
            (23.0, "sparkle", {"dur": 1.4, "gain": 0.35})]
    for i in range(6):
        out.append((23.2 + i * 0.12, "pop", {"gain": 0.22, "pitch": 1.1 + i * 0.08}))
    out.append((22.6, "boing", {"gain": 0.3}))
    return out
