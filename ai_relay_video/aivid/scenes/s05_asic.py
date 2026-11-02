"""02 · 算力接力（中）：通用显卡 vs 专用 ASIC → 博通（谷歌 TPU、OpenAI 10 吉瓦）→ Marvell →
铜线 vs 光纤 → 光模块里的"翻译" → 一盘散沙变成一张光网。"""
import math

from ..core import (TAU, Cam, at, circle, clamp, ease_back, ease_in, ease_io, ease_out, ease_out5, fill,
                    glow, lerp, lin, line, pop, prog, rad, ring_burst, rng, rrect, setc, smooth,
                    sparkle_burst, star4, stroke_pts, text, text_w, view, poly)
from ..icons import ic_gpu
from ..props import (bg_grad, chip_pkg, circuit_traces, copper, fiber, name_card, optical_module, pylon,
                     server_rack, tag, waveform)
from .common import host, mini_icon, talk_lines

DUR = 39.5
CHAPTER = ("02", "算力接力")

VO = [
    (0.7, '显卡是通用的「瑞士军刀」，可巨头们的算力需求太大，于是开始定制专用芯片：{ASIC}。'),
    (8.2, '谷歌的 TPU 由{博通}协助设计；OpenAI 也和博通签下了 10 吉瓦的定制芯片合作。'),
    (15.5, '{Marvell} 也在为云厂商定制芯片，同时还是{光通信}芯片的关键玩家。'),
    (21.2, '一个 AI 集群有成千上万颗芯片，铜线传不远、也不够快，就要把电信号变成光，用光纤连起来；'),
    (29.5, '光模块里负责「翻译」的芯片，很多就来自 Marvell 和博通。'),
    (34.4, '没有这张光网，再多芯片也只是{一盘散沙}。'),
]

G = 900
XA, XB, XC, XD, XE, XF = 960, 3100, 5200, 7300, 9400, 11500
BRCM = "#CC092F"
MRVL = "#B8003F"

P = (host(XA, G, 0.56, "curious", seed=5.5)
     .look(0, -0.9, -0.5).look(1.8, -0.8, -0.7)
     .look(3.6, 0.9, -0.6).expr(3.7, "hmm")
     .expr(6.0, "awe").look(6.0, 0.9, -0.8)
     .expr(7.5, "smile").run_to(7.6, 8.4, XB - 720, G)
     .expr(8.5, "curious").look(8.5, 0.9, -0.6)
     .expr(12.0, "shock").startle(12.0).expr(13.0, "awe")
     .expr(14.8, "smile").run_to(14.9, 15.7, XC - 720, G)
     .expr(15.8, "curious").look(15.8, 0.9, -0.6)
     .expr(20.4, "smile").run_to(20.5, 21.3, XD - 760, G)
     .expr(21.4, "curious").look(21.4, 0.9, -0.4)
     .expr(23.5, "worried").fx(23.5, ("sweat",)).look(23.5, 0.5, -0.2)
     .expr(25.6, "excited").fx(25.6, ()).look(25.6, 0.9, -0.5)
     .expr(28.9, "smile").run_to(29.0, 29.8, XE - 760, G)
     .expr(29.9, "awe").look(29.9, 0.9, -0.6)
     .expr(33.8, "smile").run_to(33.9, 34.7, XF - 760, G)
     .expr(34.8, "worried").look(34.8, 0.9, -0.5)
     .expr(36.4, "starry").hop(36.4, 50, 0.4))
talk_lines(P, VO, [0, 2], smile=0.3)

CAM = Cam([
    (0.0, (XA, 540, 1.04)),
    (7.4, (XA + 20, 540, 1.0)),
    (8.4, (XB, 540, 1.0), ease_io),
    (14.7, (XB + 20, 540, 1.02)),
    (15.7, (XC, 540, 1.0), ease_io),
    (20.3, (XC + 20, 540, 1.02)),
    (21.3, (XD, 540, 1.0), ease_io),
    (28.8, (XD + 20, 540, 1.02)),
    (29.8, (XE, 540, 1.0), ease_io),
    (33.7, (XE + 20, 540, 1.05)),
    (34.7, (XF, 540, 1.0), ease_io),
    (37.0, (XF + 40, 520, 1.08)),
    (39.5, (XF + 80, 500, 1.55), ease_in),
], drift=6, seed=11.0)


def _bg(ctx, t, cam):
    bg_grad(ctx, "#0D1226", "#1A1838", "#121633", 0.6)
    with view(ctx, cam, 0.5):
        circuit_traces(ctx, t, -600, -200, 13000, 1300, seed=33, n=90, color="#8B6CFF", a=0.1, pulse="#D9CCFF")
    with view(ctx, cam, 1.0):
        ctx.rectangle(-1000, G, 14000, 400)
        ctx.set_source(lin(0, G, 0, G + 260, [(0, "#1F2142"), (1, "#0F1024")]))
        ctx.fill()
        ctx.rectangle(-1000, G - 2, 14000, 4)
        fill(ctx, "#8B6CFF", 0.35)


def _knife(ctx, x, y, t, open_k):
    """瑞士军刀：刀身 + 展开的各种工具（每个工具一个标签）。"""
    tools = [("图形", -2.1), ("科学计算", -1.55), ("AI 训练", -1.0), ("视频", -0.45)]
    for i, (lab, ang) in enumerate(tools):
        k = clamp(open_k * 1.4 - i * 0.12)
        a_ = lerp(-0.05, ang, ease_back(k, 1.3))
        ctx.save()
        ctx.translate(x - 160, y)
        ctx.rotate(a_)
        rrect(ctx, 0, -14, 230, 28, 10)
        ctx.set_source(lin(0, -14, 0, 14, [(0, "#E8ECF4"), (1, "#9AA3B5")]))
        ctx.fill()
        ctx.restore()
        if k > 0.6:
            tx = x - 160 + math.cos(a_) * 280
            ty = y + math.sin(a_) * 280
            tag(ctx, lab, tx, ty, 26, "#FFFFFF", "#4A4458", smooth((k - 0.6) / 0.3))
    rrect(ctx, x - 200, y - 46, 400, 92, 46)
    ctx.set_source(lin(0, y - 46, 0, y + 46, [(0, "#FF5A5F"), (1, "#C42A30")]))
    ctx.fill()
    rrect(ctx, x - 30, y - 18, 60, 36, 6)
    fill(ctx, "#FFFFFF")
    text(ctx, "GPU", x + 110, y, 34, "#FFFFFF", 1, "black")


def _part_a(ctx, t):
    _knife(ctx, XA - 420, 560, t, prog(t, 1.0, 2.6))
    tag(ctx, "通用：什么都能干", XA - 420, 760, 30, "#FFFFFF", "#C42A30", smooth(prog(t, 1.6, 2.0)))
    k = pop(t, 3.4, 0.55)
    if k > 0:
        with at(ctx, XA + 450, 480, k):
            chip_pkg(ctx, 0, 0, 280, "ASIC", "专用芯片", "#8B6CFF", 1.0, 0.45, t)
        tag(ctx, "专用：只把一件事做到极致", XA + 450, 760, 30, "#FFFFFF", "#6A4FD8", k)
    # 能效对比条
    e = smooth(prog(t, 4.6, 5.0))
    if e > 0:
        for i, (lab, v, c, x) in enumerate((("能效", 0.45, "#FF5A5F", XA - 420), ("能效", 0.9, "#8B6CFF", XA + 450))):
            q = ease_out5(prog(t, 4.8 + i * 0.3, 5.8 + i * 0.3))
            rrect(ctx, x - 160, 820, 320, 22, 11)
            fill(ctx, "#2B2F45", e)
            rrect(ctx, x - 160, 820, 320 * v * q, 22, 11)
            fill(ctx, c, e)
            text(ctx, lab, x - 190, 831, 24, "#CFC8E6", e, "bold", "r")
    b = pop(t, 6.2, 0.5)
    if b > 0:
        with at(ctx, XA, 200, b):
            glow(ctx, 0, 0, 260, "#8B6CFF", 0.45)
            rrect(ctx, -160, -60, 320, 120, 60)
            fill(ctx, "#8B6CFF")
            text(ctx, "ASIC", 0, 0, 72, "#FFFFFF", 1, "black")


def _part_b(ctx, t):
    a = smooth(prog(t, 7.9, 8.5))
    if a <= 0:
        return
    # 谷歌 TPU × 博通
    k1 = pop(t, 8.4, 0.5)
    if k1 > 0:
        with at(ctx, XB - 330, 420, k1):
            chip_pkg(ctx, 0, 0, 240, "TPU", "谷歌", "#4285F4", a, 0.4, t)
    k2 = pop(t, 9.6, 0.5)
    if k2 > 0:
        name_card(ctx, "博通", XB - 330, 650, BRCM, 36, a, k2, sub="协助设计")
        line(ctx, XB - 330, 545, XB - 330, 600, 5, "#FFFFFF", 0.5 * a * k2)
    # OpenAI × 博通：10 吉瓦
    k3 = pop(t, 11.0, 0.5)
    if k3 > 0:
        with at(ctx, XB + 380, 330, k3):
            rrect(ctx, -300, -120, 600, 240, 30)
            fill(ctx, "#FFFFFF", 0.95 * a)
            text(ctx, "OpenAI × 博通", 0, -66, 40, "#2B2233", a, "black")
            text(ctx, "定制 AI 芯片", 0, -14, 28, "#6B6377", a, "bold")
            text(ctx, "10 吉瓦", 0, 58, 66, BRCM, a, "black")
        tag(ctx, "2025 年 10 月宣布", XB + 380, 490, 26, "#FFFFFF", "#4A4458", a * k3)
    # 10 座"电站"
    for i in range(10):
        q = pop(t, 12.2 + i * 0.1, 0.4)
        if q <= 0:
            continue
        x = XB + 110 + (i % 5) * 135
        y = 640 + (i // 5) * 110
        with at(ctx, x, y, q):
            pylon(ctx, 0, 40, 110, a, "#C9B8FF")
            mini_icon(ctx, "bolt", 0, -40, 50, "#FFD84D")
    if t > 12.2:
        tag(ctx, "≈ 十台大型核电机组的发电功率", XB + 380, 850, 26, "#FFFFFF", "#6A4FD8", a * smooth(prog(t, 13.3, 13.7)))


def _part_c(ctx, t):
    a = smooth(prog(t, 15.2, 15.8))
    if a <= 0:
        return
    name_card(ctx, "Marvell", XC - 120, 200, MRVL, 44, a, pop(t, 15.6, 0.5), sub="美满电子")
    # 定制芯片 → 云
    for i, lab in enumerate(("云厂商 A", "云厂商 B", "云厂商 C")):
        q = pop(t, 16.4 + i * 0.25, 0.45)
        if q <= 0:
            continue
        x = XC - 520 + i * 260
        with at(ctx, x, 470, q):
            for (dx, dy, r) in ((-46, 10, 44), (0, -18, 58), (50, 8, 46)):
                circle(ctx, dx, dy, r)
            rrect(ctx, -96, 8, 192, 54, 27)
            fill(ctx, "#DCE6FF", a)
            text(ctx, lab, 0, 22, 24, "#2B3A66", a, "black")
        with at(ctx, x, 660, q):
            chip_pkg(ctx, 0, 0, 130, "定制", "", "#B8003F", a, 0.3, t)
        line(ctx, x, 590, x, 545, 4, "#FFFFFF", 0.4 * a * q)
    # 光通信
    k = pop(t, 18.6, 0.5)
    if k > 0:
        with at(ctx, XC + 560, 520, k):
            glow(ctx, 0, 0, 240, "#7FE7FF", 0.35)
            rrect(ctx, -150, -150, 300, 300, 40)
            fill(ctx, "#13203A")
            for i in range(5):
                ph = (t * 0.9 + i / 5) % 1
                yy = -60 + i * 30
                ctx.move_to(-110, yy)
                ctx.line_to(110, yy)
                ctx.set_line_width(4)
                setc(ctx, "#7FE7FF", 0.25)
                ctx.stroke()
                glow(ctx, -110 + 220 * ph, yy, 18, "#BFF6FF", 0.9)
            text(ctx, "光通信", 0, 110, 40, "#FFFFFF", 1, "black")
        tag(ctx, "光模块芯片的关键玩家", XC + 560, 760, 28, "#FFFFFF", MRVL, k * a)


def _part_d(ctx, t):
    """铜线传不远、不够快 → 换成光纤。"""
    a = smooth(prog(t, 20.9, 21.5))
    if a <= 0:
        return
    xs = [XD - 500, XD - 120, XD + 260, XD + 640]
    for i, x in enumerate(xs):
        q = pop(t, 21.3 + i * 0.12, 0.45)
        if q > 0:
            with at(ctx, x, G - 20, q):
                server_rack(ctx, 0, 0, 170, 470, t, a, 8, "#7FE7FF", seed=i + 11)
    tag(ctx, "成千上万颗芯片", XD + 70, 220, 30, "#FFFFFF", "#4A4458",
        a * smooth(prog(t, 21.8, 22.2)) * (1 - smooth(prog(t, 25.4, 25.9))))
    # 铜线（热、慢）
    cu = smooth(prog(t, 23.0, 23.5)) * (1 - smooth(prog(t, 26.0, 26.6)))
    if cu > 0:
        pts = [(xs[0] + 85, 560), (xs[0] + 200, 600), (xs[1] - 85, 560)]
        from ..core import bezier_pts
        pts = bezier_pts((xs[0] + 85, 560), (xs[0] + 150, 640), (xs[1] - 150, 640), (xs[1] - 85, 560), 30)
        copper(ctx, pts, t, cu, hot=smooth(prog(t, 23.6, 24.6)))
        pts2 = bezier_pts((xs[1] + 85, 560), (xs[1] + 200, 700), (xs[3] - 200, 700), (xs[3] - 85, 560), 40)
        from ..core import polyline_partial
        seg = polyline_partial(pts2, 0, 0.45)
        copper(ctx, seg, t, cu, hot=1.0)
        cross = smooth(prog(t, 24.2, 24.6))
        if cross > 0:
            from ..core import cross_mark
            cross_mark(ctx, seg[-1][0] + 30, seg[-1][1], 70, "#FF5A5F", cross, cu)
            tag(ctx, "传不远 · 不够快 · 发热", XD + 60, 780, 28, "#FFFFFF", "#C42A30", cu * cross)
    # 光纤（快、远）
    op = smooth(prog(t, 25.8, 26.4))
    if op > 0:
        from ..core import bezier_pts
        for k, (i, j) in enumerate(((0, 1), (1, 2), (2, 3), (0, 3), (1, 3), (0, 2))):
            hgt = 120 + abs(j - i) * 70
            pts = bezier_pts((xs[i], 330), (xs[i], 330 - hgt), (xs[j], 330 - hgt), (xs[j], 330), 40)
            fiber(ctx, pts, t, op, "#7FE7FF", 5, 3, 0.9, prog(t, 25.8 + k * 0.15, 26.8 + k * 0.15))
        tag(ctx, "电 → 光 · 光纤高速互联", XD + 70, 780, 28, "#FFFFFF", "#1F7A9A", op * smooth(prog(t, 26.6, 27.0)))


def _part_e(ctx, t):
    a = smooth(prog(t, 29.2, 29.8))
    if a <= 0:
        return
    lid = smooth(prog(t, 30.4, 31.2))
    optical_module(ctx, XE + 80, 520, 700, 240, a, t, lid, "光模块")
    # 电信号进、光信号出
    waveform(ctx, XE - 720, 520, 360, 70, t, "square", "#FFD36B", a, 1.0)
    tag(ctx, "电信号", XE - 540, 430, 26, "#2B2233", "#FFD36B", a)
    if lid > 0.3:
        waveform(ctx, XE + 470, 520, 380, 70, t, "pulse", "#7FE7FF", a * lid, 1.4)
        tag(ctx, "光信号", XE + 660, 430, 26, "#0E2A3A", "#7FE7FF", a * lid)
        k = pop(t, 31.4, 0.5)
        if k > 0:
            with at(ctx, XE - 120, 700, k):
                rrect(ctx, -170, -40, 340, 80, 40)
                fill(ctx, "#3BAA6B")
                text(ctx, "DSP = 翻译官", 0, 0, 34, "#FFFFFF", 1, "black")
        k2 = pop(t, 32.2, 0.5)
        if k2 > 0:
            name_card(ctx, "Marvell", XE + 160, 820, MRVL, 30, a, k2)
            name_card(ctx, "博通", XE + 440, 820, BRCM, 30, a, k2)


def _part_f(ctx, t):
    a = smooth(prog(t, 34.1, 34.7))
    if a <= 0:
        return
    R = rng(55)
    net = smooth(prog(t, 36.0, 37.2))
    pts = []
    cols, rows = 9, 5
    for i in range(cols * rows):
        gx = XF - 640 + (i % cols) * 160
        gy = 200 + (i // cols) * 130
        sx, sy = gx + R.uniform(-140, 140), gy + R.uniform(-90, 90)
        x, y = lerp(sx, gx, ease_io(net)), lerp(sy, gy, ease_io(net))
        pts.append((x, y))
    if net > 0:
        for i, (x, y) in enumerate(pts):
            for j in (i + 1, i + cols):
                if (j == i + 1 and (i + 1) % cols == 0) or j >= len(pts):
                    continue
                x2, y2 = pts[j]
                q = clamp(net * 1.6 - (i % cols) * 0.05)
                fiber(ctx, [(x, y), (x2, y2)], t + i * 0.13, a * q, "#7FE7FF", 3, 1, 1.2)
    for i, (x, y) in enumerate(pts):
        c = "#9AA0AE" if net < 0.5 else "#B6FF6B"
        rrect(ctx, x - 26, y - 26, 52, 52, 8)
        fill(ctx, "#2B2F45", a)
        rrect(ctx, x - 16, y - 16, 32, 32, 5)
        fill(ctx, c, a)
        if net > 0.8:
            glow(ctx, x, y, 40, "#B6FF6B", 0.25 * a)
    if net < 0.5:
        tag(ctx, "一盘散沙", XF, 860, 32, "#FFFFFF", "#6B6377", a * (1 - net * 2))
    else:
        tag(ctx, "一张光网", XF, 860, 32, "#0E2A3A", "#7FE7FF", a * (net * 2 - 1))


def draw(ctx, t):
    cam = CAM.at(t)
    _bg(ctx, t, cam)
    with view(ctx, cam, 1.0):
        _part_a(ctx, t)
        _part_b(ctx, t)
        _part_c(ctx, t)
        _part_d(ctx, t)
        _part_e(ctx, t)
        _part_f(ctx, t)
        P.draw(ctx, t)


def sfx():
    return [
        (1.0, "ratchet", {"dur": 1.4, "gain": 0.3}),
        (3.4, "pop_big", {"gain": 0.35}),
        (4.8, "rise", {"dur": 1.0, "gain": 0.22}),
        (6.2, "impact_soft", {"gain": 0.4}),
        (7.6, "whoosh_short", {"gain": 0.3}),
        (8.4, "pop", {"gain": 0.3}), (9.6, "connect", {"gain": 0.35}),
        (11.0, "stamp", {"gain": 0.4}),
        (12.2, "zap", {"dur": 1.2, "gain": 0.25}),
        (14.9, "whoosh_short", {"gain": 0.3}),
        (15.6, "pop", {"gain": 0.3}), (16.4, "pop", {"gain": 0.25, "pitch": 1.2}),
        (16.65, "pop", {"gain": 0.25, "pitch": 1.35}), (16.9, "pop", {"gain": 0.25, "pitch": 1.5}),
        (18.6, "shimmer", {"dur": 1.2, "gain": 0.3}),
        (20.5, "whoosh_short", {"gain": 0.3}),
        (21.3, "fan", {"dur": 4.0, "gain": 0.12}),
        (23.6, "buzz", {"gain": 0.3}), (24.2, "error", {"gain": 0.3}),
        (25.8, "zip", {"gain": 0.3}), (26.0, "stream", {"dur": 2.4, "gain": 0.2}),
        (29.0, "whoosh_short", {"gain": 0.3}),
        (30.4, "slide", {"gain": 0.3}), (31.4, "pop_big", {"gain": 0.35}),
        (32.2, "pop", {"gain": 0.3}), (32.3, "pop", {"gain": 0.3, "pitch": 1.2}),
        (33.9, "whoosh_short", {"gain": 0.3}),
        (34.6, "shuffle", {"dur": 1.2, "gain": 0.25}),
        (36.0, "connect", {"gain": 0.35}), (36.2, "stream", {"dur": 2.0, "gain": 0.2}),
        (37.6, "zoom_in", {"dur": 1.8, "gain": 0.35}),
    ]
