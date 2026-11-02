"""02 · 算力接力（上）：显卡 + CUDA → AlexNet 起飞 → CUDA 护城河 → Linux / Ubuntu → 层层咬合的技术栈。"""
import math

from ..core import (TAU, Cam, at, circle, clamp, ease_back, ease_in, ease_io, ease_out, ease_out5, fill,
                    glow, lerp, lin, line, pop, prog, rad, ring_burst, rng, rrect, setc, smooth,
                    sparkle_burst, star4, stroke_pts, text, text_w, view)
from ..icons import ic_brain, ic_gear, ic_gpu, ic_penguin, ic_trophy, ic_server
from ..props import bg_grad, castle, circuit_traces, server_rack, tag
from .common import host, talk_lines

DUR = 43.5
CHAPTER = ("02", "算力接力")

VO = [
    (1.0, '大模型要跑起来，离不开{算力}。'),
    (4.0, '显卡原本是给游戏画画面的，2006 年，英伟达推出 {CUDA}，让显卡也能做通用计算。'),
    (12.3, '2012 年，一个叫 AlexNet 的模型用两块游戏显卡训练，拿下图像识别比赛冠军，深度学习从此起飞。'),
    (21.3, '二十年下来，CUDA 攒下了几百万开发者和海量软件库，这才是英伟达真正的{护城河}。'),
    (29.1, '这些显卡大多跑在 {Linux} 上，Ubuntu 是 AI 开发者最常用的系统之一；'),
    (35.6, '芯片、驱动、系统、框架、模型，一层层咬合，才撑起了大模型。'),
]

G = 900                      # 地面
XA, XB, XC, XD, XE, XF = 960, 3000, 5100, 7200, 9300, 11400
NV = "#76B900"

P = (host(XA - 330, G, 0.6, "determined", seed=4.4)
     .fx(0, ()).look(0, 1.0, -0.2)
     .push(0.6, 2.9, "r").expr(2.9, "tired").fx(2.9, ("sweat",))
     .expr(3.3, "surprised").fx(3.3, ()).look(3.3, 0.6, -0.9).hop(3.35, 30, 0.35)
     .expr(3.9, "smile").run_to(4.0, 4.9, XB - 700, G)
     .expr(5.0, "happy").look(5.0, 0.9, -0.6)
     .expr(7.3, "awe").look(7.3, 0.7, -0.8)
     .expr(11.4, "smile").run_to(11.5, 12.4, XC - 760, G)
     .expr(12.5, "curious").look(12.5, 0.9, -0.5)
     .expr(16.6, "excited").cheer(16.7, 17.9)
     .expr(18.6, "starry").look(18.6, 0.9, -0.9)
     .expr(20.4, "smile").run_to(20.5, 21.4, XD - 800, G)
     .expr(21.5, "curious").look(21.5, 0.9, -0.6)
     .expr(25.6, "smug").front(25.6, "cross")
     .front(28.3, None).expr(28.3, "smile").run_to(28.4, 29.3, XE - 720, G)
     .expr(29.4, "happy").look(29.4, 0.9, -0.5).wave(30.6, 31.6, "r")
     .expr(34.6, "smile").run_to(34.7, 35.6, XF - 520, G)
     .expr(35.7, "curious").look(35.7, 0.7, -0.9)
     .move(39.4, 40.3, XF - 30, G - 805, ease_io).hop(39.4, 140, 0.9).land(40.3, 0.2)
     .expr(40.4, "proud").look(40.4, 0.0, 0.2).wave(41.0, 42.4, "r"))
talk_lines(P, VO, [0, 5], smile=0.3)

CAM = Cam([
    (0.0, (XA, 560, 1.06)),
    (3.6, (XA, 560, 1.0)),
    (4.8, (XB, 540, 1.0), ease_io),
    (11.2, (XB + 30, 540, 1.02)),
    (12.4, (XC, 540, 1.0), ease_io),
    (20.2, (XC + 40, 540, 1.02)),
    (21.4, (XD, 540, 1.0), ease_io),
    (28.2, (XD + 30, 540, 1.04)),
    (29.3, (XE, 540, 1.0), ease_io),
    (34.5, (XE + 30, 540, 1.02)),
    (35.6, (XF, 540, 1.0), ease_io),
    (38.6, (XF, 470, 0.9), ease_io),
    (43.5, (XF, 380, 0.94)),
], drift=6, seed=9.0)


def _bg(ctx, t, cam):
    bg_grad(ctx, "#0B1424", "#16213A", "#0F1A30", 0.6)
    with view(ctx, cam, 0.5):
        circuit_traces(ctx, t, -600, -200, 13000, 1300, seed=21, n=90, color="#2EC4B6", a=0.12)
    with view(ctx, cam, 1.0):
        ctx.rectangle(-1000, G, 14000, 400)
        ctx.set_source(lin(0, G, 0, G + 260, [(0, "#1D2A44"), (1, "#0E1626")]))
        ctx.fill()
        ctx.rectangle(-1000, G - 2, 14000, 4)
        fill(ctx, "#2EC4B6", 0.35)


def _part_a(ctx, t):
    """推不动的大模型 → 显卡落下供上算力。"""
    bx, by = XA + 180, G - 230
    power = smooth(prog(t, 3.2, 3.9))
    glow(ctx, bx, by, 320, "#8B6CFF", 0.15 + 0.35 * power)
    rrect(ctx, bx - 230, by - 220, 460, 440, 40)
    ctx.set_source(lin(0, by - 220, 0, by + 220, [(0, "#3A2E66"), (1, "#22193F")]))
    ctx.fill()
    ic_brain(ctx, bx, by - 30, 230, 0.4 + 0.6 * power, t, "#8B6CFF", 0.3 + 0.4 * power)
    text(ctx, "大模型", bx, by + 160, 44, "#FFFFFF", 0.9, "black")
    # 算力表
    mx, my = bx + 360, by - 120
    rrect(ctx, mx - 34, my - 160, 68, 320, 34)
    fill(ctx, "#1A2236")
    lv = power
    rrect(ctx, mx - 24, my + 150 - 300 * lv, 48, 300 * lv, 24)
    fill(ctx, NV)
    text(ctx, "算力", mx, my + 200, 30, "#CFE7C0", 1, "black")
    # 显卡从天而降
    u = prog(t, 2.6, 3.2)
    if u > 0:
        gy = lerp(-200, by + 300, ease_in(u))
        ic_gpu(ctx, bx, min(gy, by + 300), 300, 1.0, t, t * 3 * power, 0.6 * power)
        if t > 3.2:
            ring_burst(ctx, t, 3.2, bx, by + 300, 30, 300, NV, 0.7, 10)
            sparkle_burst(ctx, t, 3.22, bx, by + 300, 12, 260, "#C8FF6B", 0.8, 3, 20)


def _part_b(ctx, t):
    """游戏画面 → CUDA 打开通用计算的大门。"""
    a = smooth(prog(t, 3.9, 4.6))
    if a <= 0:
        return
    x0, y0, w, h = XB - 560, 170, 700, 430
    rrect(ctx, x0 - 16, y0 - 16, w + 32, h + 32, 24)
    fill(ctx, "#2A2F3E", a)
    ctx.save()
    rrect(ctx, x0, y0, w, h, 12)
    ctx.clip()
    gm = 1 - smooth(prog(t, 8.2, 9.2))           # 游戏画面 → 矩阵
    ctx.set_source(lin(0, y0, 0, y0 + h, [(0, "#6EC6FF", a), (1, "#B9E8FF", a)]))
    ctx.paint()
    off = (t * 120) % 140
    for i in range(8):
        hx = x0 + i * 140 - off
        hh = 90 + (i * 37) % 70
        ctx.rectangle(hx, y0 + h - 90 - hh, 120, hh)
        fill(ctx, "#4E8F5A", a)
    ctx.rectangle(x0, y0 + h - 90, w, 90)
    fill(ctx, "#8B5E3C", a)
    for i in range(6):
        cx = x0 + ((i * 160 - t * 200) % (w + 100)) - 50
        circle(ctx, cx, y0 + 200 + (i % 2) * 40, 16)
        fill(ctx, "#FFD84D", a)
    jy = abs(math.sin(t * 5)) * 60
    rrect(ctx, x0 + 170, y0 + h - 160 - jy, 70, 70, 10)
    fill(ctx, "#E88E64", a)
    rrect(ctx, x0 + 180, y0 + h - 148 - jy, 12, 22, 3)
    fill(ctx, "#24130E", a)
    rrect(ctx, x0 + 214, y0 + h - 148 - jy, 12, 22, 3)
    fill(ctx, "#24130E", a)
    if gm < 1:
        ctx.set_source_rgba(0.04, 0.07, 0.13, (1 - gm))
        ctx.paint()
        R = rng(3)
        for r in range(9):
            for c in range(7):
                v = R.uniform(-1, 1)
                k = clamp((t - 8.5 - (r + c) * 0.04) / 0.4)
                text(ctx, f"{v:+.2f}", x0 + 60 + c * 96, y0 + 40 + r * 46, 26, "#7CFFB2" if v > 0 else "#7CC6FF",
                     a * (1 - gm) * k, "mono")
    ctx.restore()
    text(ctx, "游戏画面" if gm > 0.5 else "通用计算：矩阵运算", XB - 210, y0 + h + 60, 34, "#FFFFFF", a, "black")
    # 显卡
    ic_gpu(ctx, XB - 210, G - 120, 330, a, t, t * 2.2, 0.3)
    # CUDA 大门
    k = pop(t, 7.2, 0.6)
    if k > 0:
        cx, cy = XB + 480, 430
        with at(ctx, cx, cy, k):
            glow(ctx, 0, 0, 330, NV, 0.35)
            rrect(ctx, -170, -230, 340, 460, 30)
            fill(ctx, "#1C2B1A")
            op = smooth(prog(t, 8.0, 9.0))
            rrect(ctx, -140, -200, 280, 400, 22)
            ctx.set_source(lin(0, -200, 0, 200, [(0, "#C8FF6B", 0.2 + 0.7 * op), (1, NV, 0.2 + 0.7 * op)]))
            ctx.fill()
            text(ctx, "CUDA", 0, -120, 64, "#FFFFFF", 1, "black")
            text(ctx, "2006", 0, -60, 36, "#E8FFD0", 1, "black")
            for i, lab in enumerate(("科学计算", "物理模拟", "神经网络")):
                q = pop(t, 9.4 + i * 0.35, 0.4)
                if q > 0:
                    with at(ctx, 0, 30 + i * 62, q):
                        rrect(ctx, -110, -24, 220, 48, 24)
                        fill(ctx, "#FFFFFF", 0.92)
                        text(ctx, lab, 0, 0, 26, "#2B5A12", 1, "black")
        # 从显卡流向大门的光流
        if t > 8.0:
            for i in range(6):
                ph = ((t - 8.0) * 0.8 + i / 6) % 1
                px = lerp(XB - 40, cx - 170, ph)
                py = lerp(G - 140, cy + 60, ph) - math.sin(ph * math.pi) * 80
                glow(ctx, px, py, 26, "#C8FF6B", 0.7 * smooth(prog(t, 8.0, 8.4)))


def _part_c(ctx, t):
    """AlexNet：两块 GTX 580 → ImageNet 冠军 → 深度学习起飞。"""
    a = smooth(prog(t, 11.9, 12.6))
    if a <= 0:
        return
    for i in range(2):
        q = pop(t, 12.8 + i * 0.25, 0.45)
        if q > 0:
            with at(ctx, XC - 300 + i * 300, G - 110, q):
                ic_gpu(ctx, 0, 0, 260, a, t, t * 3, 0.5)
    tag(ctx, "GTX 580 × 2", XC - 150, G - 245, 30, "#FFFFFF", "#3C9D4A", a * smooth(prog(t, 13.2, 13.6)))
    tag(ctx, "AlexNet · 2012", XC - 150, G - 315, 34, "#FFFFFF", "#2B2233", a * smooth(prog(t, 12.5, 12.9)))
    # 比赛成绩
    b = smooth(prog(t, 14.8, 15.3))
    if b > 0:
        x0, y0 = XC + 120, 170
        rrect(ctx, x0, y0, 620, 330, 26)
        fill(ctx, "#FFFFFF", 0.92 * b)
        text(ctx, "ImageNet 图像识别比赛 · 错误率", x0 + 310, y0 + 44, 28, "#2B2233", b, "black")
        rows = [("第二名", 26.2, "#9AA0AE"), ("AlexNet", 15.3, NV)]
        for i, (lab, v, c) in enumerate(rows):
            q = ease_out5(prog(t, 15.2 + i * 0.4, 16.2 + i * 0.4))
            yy = y0 + 125 + i * 100
            text(ctx, lab, x0 + 140, yy, 30, "#2B2233", b, "black", "r")
            rrect(ctx, x0 + 160, yy - 26, 380 * v / 30 * q, 52, 26)
            fill(ctx, c, b)
            text(ctx, f"{v}%", x0 + 175 + 380 * v / 30 * q, yy, 28, c, b * q, "black", "l")
        k = pop(t, 16.6, 0.5)
        if k > 0:
            with at(ctx, x0 + 560, y0 + 230, k * 0.8):
                ic_trophy(ctx, 0, 0, 150, b, t)
    # 起飞曲线
    c = smooth(prog(t, 18.0, 18.5))
    if c > 0:
        x0, y0, w, h = XC + 140, 560, 600, 260
        ctx.set_line_width(3)
        setc(ctx, "#FFFFFF", 0.3 * c)
        ctx.move_to(x0, y0 + h)
        ctx.line_to(x0 + w, y0 + h)
        ctx.stroke()
        pts = []
        for i in range(61):
            u = i / 60
            v = 0.05 * u if u < 0.35 else 0.0175 + (u - 0.35) ** 2.2 * 2.2
            pts.append((x0 + u * w, y0 + h - min(1.0, v) * h))
        from ..core import polyline_partial
        seg = polyline_partial(pts, 0, prog(t, 18.2, 20.0))
        stroke_pts(ctx, seg, 7, "#FFB27A", c)
        if len(seg) > 1:
            glow(ctx, seg[-1][0], seg[-1][1], 40, "#FFB27A", 0.8 * c)
        text(ctx, "2012", x0 + w * 0.35, y0 + h + 34, 24, "#FFFFFF", 0.8 * c, "bold")
        tag(ctx, "深度学习起飞", x0 + w * 0.7, y0 + 10, 30, "#FFFFFF", "#FF9F68", c * smooth(prog(t, 19.0, 19.4)))


LIBS = ["cuDNN", "cuBLAS", "NCCL", "TensorRT", "cuFFT", "Thrust", "CUTLASS", "RAPIDS"]


def _part_d(ctx, t):
    """CUDA 护城河：城堡 + 软件库砖块 + 涌来的开发者。"""
    a = smooth(prog(t, 20.9, 21.6))
    if a <= 0:
        return
    cx, cy = XD + 220, G - 60
    # 护城河
    from ..core import ellipse
    ellipse(ctx, cx, cy, 760, 120)
    ctx.set_source(lin(0, cy - 120, 0, cy + 120, [(0, "#2E7FBF", 0.7 * a), (1, "#1B4E7A", 0.7 * a)]))
    ctx.fill()
    for i in range(5):
        ph = (t * 0.3 + i / 5) % 1
        ellipse(ctx, cx, cy, 300 + ph * 440, 46 + ph * 70)
        ctx.set_line_width(3)
        setc(ctx, "#9FD8FF", 0.35 * a * (1 - ph))
        ctx.stroke()
    ellipse(ctx, cx, cy - 4, 300, 46)
    fill(ctx, "#3C4A2E", a)
    castle(ctx, cx, cy - 10, 470, 460, "#5E8C3A", a, flag=NV, flag_text="NV", t=t)
    # 软件库砖块
    for i, lib in enumerate(LIBS):
        q = pop(t, 22.4 + i * 0.28, 0.45)
        if q <= 0:
            continue
        bx = cx - 330 + (i % 4) * 220
        by = 210 + (i // 4) * 80
        with at(ctx, bx, by, q):
            rrect(ctx, -100, -30, 200, 60, 10)
            fill(ctx, "#E9F7D8", a)
            text(ctx, lib, 0, 0, 28, "#2B5A12", a, "mono")
    # 开发者
    R = rng(9)
    dv = smooth(prog(t, 24.0, 25.0))
    for i in range(70):
        side = -1 if i % 2 == 0 else 1
        ph = ((t - 24.0) * R.uniform(0.15, 0.3) + R.random()) % 1
        x = cx + side * lerp(980, 520, ph)
        y = cy - 20 + R.uniform(-60, 70)
        circle(ctx, x, y, 7)
        fill(ctx, ["#FFB27A", "#9CC2FF", "#B7A6FF", "#FFE58A"][i % 4], dv * a * (1 - ph * 0.3))
    n = int(lerp(0, 500, ease_out(prog(t, 24.0, 26.0))))
    if dv > 0:
        tag(ctx, f"开发者 {n} 万+", cx - 640, 520, 30, "#FFFFFF", "#2B2233", dv * a)
    m = pop(t, 26.6, 0.5)
    if m > 0:
        with at(ctx, cx + 600, 470, m, 0.08):
            glow(ctx, 0, 0, 180, "#2E7FBF", 0.4)
            rrect(ctx, -130, -46, 260, 92, 46)
            fill(ctx, "#2E7FBF")
            text(ctx, "护城河", 0, 0, 46, "#FFFFFF", 1, "black")


def _part_e(ctx, t):
    """Linux / Ubuntu：成排的服务器里，跑的是开源系统。"""
    a = smooth(prog(t, 28.9, 29.6))
    if a <= 0:
        return
    for i in range(6):
        q = pop(t, 29.3 + i * 0.12, 0.45)
        if q <= 0:
            continue
        x = XE - 470 + i * 190
        with at(ctx, x, G, q):
            server_rack(ctx, 0, 0, 160, 430, t, a, 7, NV, seed=i + 3)
        k = pop(t, 30.2 + i * 0.12, 0.4)
        if k > 0:
            ic_penguin(ctx, x, G - 470, 80 * k, a, t)
    # Linux / Ubuntu 标牌
    k1 = pop(t, 29.5, 0.5)
    if k1 > 0:
        with at(ctx, XE - 250, 150, k1):
            rrect(ctx, -150, -50, 300, 100, 50)
            fill(ctx, "#2B2233", 0.95 * a)
            text(ctx, "Linux", 0, 0, 50, "#FFFFFF", a, "black")
    k2 = pop(t, 31.0, 0.5)
    if k2 > 0:
        with at(ctx, XE + 250, 150, k2):
            rrect(ctx, -170, -50, 340, 100, 50)
            fill(ctx, "#E95420", a)
            text(ctx, "Ubuntu", 0, 0, 50, "#FFFFFF", a, "black")
        tag(ctx, "AI 开发者最常用的系统之一", XE + 250, 232, 26, "#FFFFFF", "#7A3A20", a * k2)
    # 终端里一条命令
    tm = smooth(prog(t, 32.0, 32.4))
    if tm > 0:
        from ..ui import term_lines
        rrect(ctx, XE - 280, 286, 560, 104, 18)
        fill(ctx, "#14171F", 0.95 * a * tm)
        term_lines(ctx, [("$ nvidia-smi", "#7CFFB2", 32.2), ("GPU 0-7 · 正常运行", "#CFE7C0", 33.0)], XE - 250, 318,
                   t, a * tm, size=26, lh=42, cps=22)


LAYERS = [("芯片", "GPU", "#3C6E1F", "#76B900"), ("驱动", "Driver", "#26507A", "#4C8DFF"),
          ("CUDA", "并行计算平台", "#2E5A16", "#8FD14F"), ("系统", "Linux · Ubuntu", "#7A3A20", "#E95420"),
          ("框架", "PyTorch 等", "#7A2E1A", "#EE4C2C"), ("大模型", "GPT · Claude · Gemini…", "#3E2C78", "#8B6CFF")]
LY = [G - 60 - i * 132 for i in range(6)]


def _part_f(ctx, t):
    a = smooth(prog(t, 35.2, 35.9))
    if a <= 0:
        return
    W_ = 860
    for i, (name, sub, c0, c1) in enumerate(LAYERS):
        st = 35.8 + i * 0.55
        u = prog(t, st, st + 0.5)
        if u <= 0:
            continue
        y = lerp(LY[i] - 500, LY[i], ease_in(u))
        sq = 0.0
        if t > st + 0.5:
            v = (t - st - 0.5) / 0.6
            if v < 1:
                sq = 0.08 * math.sin(v * math.pi * 2.5) * (1 - v)
        hh = 112 * (1 - sq)
        rrect(ctx, XF - W_ / 2, y - hh / 2, W_, hh, 22)
        ctx.set_source(lin(0, y - hh / 2, 0, y + hh / 2, [(0, c1, a), (1, c0, a)]))
        ctx.fill()
        text(ctx, name, XF - W_ / 2 + 140, y, 44, "#FFFFFF", a, "black")
        text(ctx, sub, XF + 120, y, 32, "#FFFFFF", 0.88 * a, "bold")
        if u >= 1 and t < st + 1.0:
            sparkle_burst(ctx, t, st + 0.5, XF - W_ / 2 + 20, y, 5, 90, "#FFFFFF", 0.5, i * 3 + 1, 12)
            sparkle_burst(ctx, t, st + 0.5, XF + W_ / 2 - 20, y, 5, 90, "#FFFFFF", 0.5, i * 3 + 2, 12)
    # 两侧咬合的齿轮
    run = smooth(prog(t, 39.0, 39.8))
    if run > 0:
        for i in range(5):
            y = (LY[i] + LY[i + 1]) / 2
            for side in (-1, 1):
                rot = (t - 39) * (0.9 if (i + (side > 0)) % 2 else -0.9) * run
                ic_gear(ctx, XF + side * (W_ / 2 + 50), y, 46, 10, rot, "#9FB2C9", a * run)
        tag(ctx, "层层咬合", XF + W_ / 2 + 200, LY[3], 34, "#FFFFFF", "#FF9F68", a * run)


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
    out = [
        (0.6, "stretch", {"dur": 2.2, "gain": 0.3}),
        (2.6, "fall", {"dur": 0.6, "gain": 0.35}),
        (3.2, "clunk", {"gain": 0.5}), (3.25, "powerup", {"gain": 0.4}),
        (4.0, "whoosh_short", {"gain": 0.3}),
        (4.6, "fan", {"dur": 3.0, "gain": 0.12}),
        (7.2, "gate", {"gain": 0.4}), (8.0, "shimmer", {"dur": 1.4, "gain": 0.3}),
        (9.4, "pop", {"gain": 0.25, "pitch": 1.2}), (9.75, "pop", {"gain": 0.25, "pitch": 1.35}),
        (10.1, "pop", {"gain": 0.25, "pitch": 1.5}),
        (11.5, "whoosh_short", {"gain": 0.3}),
        (12.8, "clunk", {"gain": 0.3}), (13.05, "clunk", {"gain": 0.3, "pitch": 1.1}),
        (15.2, "rise", {"dur": 0.8, "gain": 0.25}),
        (16.6, "success", {"gain": 0.45}),
        (18.2, "zoom_in", {"dur": 1.8, "gain": 0.3}),
        (20.5, "whoosh_short", {"gain": 0.3}),
        (21.5, "water", {"gain": 0.3}),
        (22.4, "stream", {"dur": 2.4, "gain": 0.15}),
        (24.0, "shuffle", {"dur": 2.0, "gain": 0.2}),
        (26.6, "pop_big", {"gain": 0.4}),
        (28.4, "whoosh_short", {"gain": 0.3}),
        (29.3, "fan", {"dur": 5.0, "gain": 0.12}),
        (32.2, "typing", {"dur": 0.6, "gain": 0.2}),
        (34.7, "whoosh_short", {"gain": 0.3}),
    ]
    for i in range(6):
        out.append((35.8 + i * 0.55 + 0.5, "thud", {"gain": 0.35, "pitch": 1.0 + i * 0.06}))
    out += [(39.0, "gears_run", {"dur": 4.0, "gain": 0.25}), (39.4, "boing", {"gain": 0.3}),
            (40.4, "chime", {"gain": 0.3})]
    return out
