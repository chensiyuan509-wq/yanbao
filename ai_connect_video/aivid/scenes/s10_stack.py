"""第五章 · 软硬件底座：显卡 → 驱动 / CUDA → Linux / Ubuntu → PyTorch → 大模型 → 智能体。

六层底座依次砸落叠起，小橙一层层跳上去；两侧齿轮逐层咬合转动。
"""
import math

from ..core import (TAU, W, H, Cam, at, circle, clamp, ease_back, ease_in, ease_io, ease_out,
                    fill, glow, kf, lerp, line, lin, pop, prog, rrect, setc, smooth, text, text_w,
                    view, sparkle_burst, ring_burst, stroke_pts, font)
from ..icons import (ic_brain, ic_chatgpt, ic_claude_code, ic_codex, ic_flame, ic_gear, ic_gpu,
                     ic_muse, ic_openclaw, ic_penguin, ic_ubuntu, ic_terminal)
from ..mascot import Puppet
from ..ui import card, pill, progress

DUR = 24.0
CHAPTER = ("05", "软硬件底座")

SUBS = [
    (0.8, 5.6, "再往下看，大模型跑在一整套软硬件「{底座}」上："),
    (5.8, 12.4, "NVIDIA 显卡 + {CUDA}，跑在 Linux / Ubuntu 上，一条命令就能装好驱动。"),
    (12.6, 18.6, "Ubuntu 宣布内置 CUDA；{PyTorch} 由 Meta 开源，又交给了基金会。"),
    (18.8, 23.6, "不同公司、不同国家，像{齿轮}一样严丝合缝地咬合。"),
]

LX, LW, LH = 690, 1140, 118
LAYERS = [  # (标题, 副标题, 颜色上, 颜色下, 落地时间)
    ("GPU 显卡", "算力的发动机", "#2F4B2A", "#1E331B", 0.5),
    ("驱动 + CUDA", "让软件用上显卡", "#355E2B", "#22421C", 1.2),
    ("Linux / Ubuntu", "AI 服务器最常用的操作系统", "#7A3A23", "#5A2816", 1.9),
    ("PyTorch 框架", "训练模型的工具箱", "#7A3220", "#5B2212", 2.6),
    ("大模型", "GPT · Claude · Gemini …", "#4B3A8C", "#33276A", 3.3),
    ("智能体应用", "Claude Code · Codex · Muse …", "#7A3A6E", "#57264E", 4.0),
]
LY = [905 - i * 130 for i in range(6)]          # 各层中心 y
CHIPS = [
    [("NVIDIA · 美国", "#76B900")],
    [("NVIDIA · 美国", "#76B900")],
    [("Canonical（英国）+ 全球开源社区", "#E95420")],
    [("Meta 开源 → Linux 基金会", "#3D7BFF")],
    [("OpenAI · Anthropic · Google · Meta", "#8B6CFF")],
    [],
]
T_TERM = 6.0
T_B1, T_B2 = 12.9, 14.7
T_WIDE = 18.6

P = Puppet(1100, LY[0] - LH / 2, 0.5, "curious", seed=10.1).look(0, -0.6, -0.8)
for i in range(1, 6):
    t0 = LAYERS[i][4] - 0.12
    P.move(t0, t0 + 0.5, 1100, LY[i] - LH / 2, walk=False, ease=ease_out).hop(t0, 55, 0.5)
P.expr(0.6, "surprised").expr(1.4, "excited").expr(4.6, "proud")
P.expr(6.6, "curious").look(6.6, 1.0, 0.6).expr(9.6, "happy")
P.look(12.8, 1.0, 0.4).expr(13.0, "curious").expr(15.2, "smile")
P.expr(T_WIDE + 0.2, "determined").fx(T_WIDE + 0.2, ("sparkle",)).look(T_WIDE + 0.2, 0, 0)
P.wave(20.6, 22.8, "l")

CAM = Cam([
    (0.0, (830, 800, 1.3)),
    (1.2, (830, 760, 1.25)),
    (4.6, (960, 560, 0.98), ease_io),
    (5.8, (975, 570, 1.0)),
    (7.0, (1000, 680, 1.07), ease_io),
    (12.4, (1010, 680, 1.09)),
    (13.4, (1000, 540, 1.06), ease_io),
    (18.4, (1010, 530, 1.08)),
    (19.6, (960, 545, 0.9), ease_io),
    (24.0, (960, 540, 0.94)),
], drift=5, seed=27.0)


def draw(ctx, t):
    ctx.set_source(lin(0, 0, 0, H, [(0, "#0A1A30"), (1, "#123553")]))
    ctx.paint()
    cam = CAM.at(t)
    with view(ctx, cam, 0.5):
        ctx.set_line_width(1.5)
        setc(ctx, "#5FA8FF", 0.12)
        for i in range(-12, 40):
            ctx.move_to(i * 80 - 400, -600)
            ctx.line_to(i * 80 - 400, 1800)
        for j in range(-8, 24):
            ctx.move_to(-600, j * 80 - 300)
            ctx.line_to(2800, j * 80 - 300)
        ctx.stroke()
        setc(ctx, "#5FA8FF", 0.22)
        for i in range(-3, 10):
            for j in range(-3, 8):
                circle(ctx, i * 320 - 400, j * 320 - 300, 3)
        ctx.fill()
    with view(ctx, cam):
        speed = 1 + 2.5 * smooth(prog(t, T_WIDE, T_WIDE + 1.5))
        draw_gears(ctx, t, speed)
        for i in range(6):
            draw_layer(ctx, i, t)
        callouts(ctx, t)
        P.draw(ctx, t)
    wide_text(ctx, t)


def _land(i, t):
    """第 i 层的落下偏移与可见度。"""
    t0 = LAYERS[i][4]
    if t < t0 - 0.45:
        return None
    u = prog(t, t0 - 0.45, t0)
    dy = -700 * (1 - ease_in(u))
    if t > t0:
        dy += -14 * math.sin((t - t0) * 18) * math.exp(-(t - t0) * 7)
    return dy


def draw_layer(ctx, i, t):
    dy = _land(i, t)
    if dy is None:
        return
    title, sub, c0, c1, t0 = LAYERS[i]
    y = LY[i] + dy
    x0 = LX - LW / 2
    hl = 0.0
    if T_TERM <= t < 12.4 and i in (0, 1, 2):
        hl = 0.5 + 0.5 * math.sin(t * 4 + i)
    if 12.6 <= t < 18.4 and ((i == 2 and t > T_B1) or (i == 3 and t > T_B2)):
        hl = 0.5 + 0.5 * math.sin(t * 4 + i)
    from ..core import box_shadow
    box_shadow(ctx, x0, y - LH / 2, LW, LH, 26, blur=30, a=0.45, dy=14, color="#020814")
    rrect(ctx, x0, y - LH / 2, LW, LH, 26)
    ctx.set_source(lin(0, y - LH / 2, 0, y + LH / 2, [(0, c0), (1, c1)]))
    ctx.fill()
    rrect(ctx, x0 + 3, y - LH / 2 + 3, LW - 6, 14, 7)
    fill(ctx, "#FFFFFF", 0.10)
    if hl > 0:
        rrect(ctx, x0 - 4, y - LH / 2 - 4, LW + 8, LH + 8, 30)
        ctx.set_line_width(5)
        setc(ctx, "#FFD25C", 0.5 + 0.4 * hl)
        ctx.stroke()
    # 图标
    ix = x0 + 90
    if i == 0:
        spin = t * (1.2 if t < T_TERM + 3.6 else 6.0)
        ic_gpu(ctx, ix + 20, y, 150, 1.0, t, spin, glow_a=0.6 * smooth(prog(t, T_TERM + 3.6, T_TERM + 4.2)))
    elif i == 1:
        rrect(ctx, ix - 44, y - 40, 88, 80, 16)
        fill(ctx, "#76B900")
        text(ctx, "CUDA", ix, y, 26, "#FFFFFF", 1, "black")
    elif i == 2:
        ic_penguin(ctx, ix - 20, y + 2, 92, 1.0, t)
        ic_ubuntu(ctx, ix + 46, y, 66, 1.0, t, t * 0.4)
    elif i == 3:
        ic_flame(ctx, ix, y, 90, 1.0, t)
    elif i == 4:
        ic_brain(ctx, ix, y, 92, 1.0, t, glow_a=0.1)
    elif i == 5:
        for j, ic in enumerate((ic_claude_code, ic_codex, ic_chatgpt, ic_muse, ic_openclaw)):
            ic(ctx, LX + 120 + j * 92, y, 74, 1.0, t)
    tx = x0 + (240 if i != 0 else 260)
    text(ctx, title, tx, y - 18, 40, "#FFFFFF", 1, "black", "l")
    text(ctx, sub, tx, y + 28, 24, "#E9E2D6", 0.8, "bold", "l")
    # 公司标签
    cx = x0 + LW - 30
    for (s, col) in reversed(CHIPS[i]):
        tw = text_w(ctx, s, 26, "bold") + 26 * 0.62 * 2 + 26 * 0.8
        pill(ctx, s, cx - tw / 2, y, 26, "#2B2233", "#FFFFFF", 1.0, 0.95, dot=col)
        cx -= tw + 12
    if t < t0 + 0.4:
        ring_burst(ctx, t, t0, LX, y + LH / 2, 60, 700, "#9CD1FF", 0.5, 8, 0.6)


def draw_gears(ctx, t, speed):
    for i in range(5):
        if t <= LAYERS[i + 1][4]:
            continue
        a = smooth(prog(t, LAYERS[i + 1][4], LAYERS[i + 1][4] + 0.3))
        gy = (LY[i] + LY[i + 1]) / 2
        d = 1 if i % 2 == 0 else -1
        for gx, col in ((LX - LW / 2 + 10, "#9FB7D6"), (LX + LW / 2 - 10, "#D6B98F")):
            ic_gear(ctx, gx, gy, 64, 12, d * t * 0.9 * speed + i * 0.13, col, a)
            circle(ctx, gx, gy, 12)
            fill(ctx, "#0E2238", a)


def callouts(ctx, t):
    # 终端：一条命令装驱动
    a = smooth(prog(t, T_TERM, T_TERM + 0.4)) * (1 - smooth(prog(t, 12.4, 12.9)))
    if a > 0:
        x, y, w, h = 1330, 600, 540, 330
        k = ease_back(prog(t, T_TERM, T_TERM + 0.5), 1.4)
        with at(ctx, x + w / 2, y + h / 2, 0.85 + 0.15 * k):
            card(ctx, -w / 2, -h / 2, w, h, 28, "#16141E", a, shadow=0.4)
            ctx.save()
            rrect(ctx, -w / 2, -h / 2, w, h, 28)
            ctx.clip()
            ctx.rectangle(-w / 2, -h / 2, w, 50)
            fill(ctx, "#2A2735", a)
            ctx.restore()
            for k2, c in enumerate(("#FF6159", "#FFBD2E", "#28C941")):
                circle(ctx, -w / 2 + 28 + k2 * 24, -h / 2 + 25, 7.5)
                fill(ctx, c, a)
            text(ctx, "Ubuntu 终端", 0, -h / 2 + 25, 24, "#BDB7CC", a, "medium")
            cmd = "$ sudo ubuntu-drivers install"
            n = int(len(cmd) * prog(t, T_TERM + 0.5, T_TERM + 1.9))
            text(ctx, cmd[:n], -w / 2 + 30, -h / 2 + 100, 28, "#FFFFFF", a, "mono", "l")
            if t > T_TERM + 2.1:
                progress(ctx, -w / 2 + 30, -h / 2 + 150, w - 60, 16, ease_io(prog(t, T_TERM + 2.1, T_TERM + 3.5)),
                         "#76B900", "#34313F", a)
                pct = int(100 * ease_io(prog(t, T_TERM + 2.1, T_TERM + 3.5)))
                text(ctx, f"正在安装 NVIDIA 驱动… {pct}%", -w / 2 + 30, -h / 2 + 200, 26, "#BDB7CC", a, "bold", "l")
            if t > T_TERM + 3.6:
                ok = pop(t, T_TERM + 3.6, 0.4)
                with at(ctx, -w / 2 + 60, -h / 2 + 268, ok):
                    circle(ctx, 0, 0, 22)
                    fill(ctx, "#76B900", a)
                    from ..core import check_mark
                    check_mark(ctx, 0, 1, 26, "#FFFFFF", 1, a)
                text(ctx, "驱动装好了，显卡就绪", -w / 2 + 96, -h / 2 + 268, 30, "#7CFFB2", a * ok, "black", "l")
        # 指向 GPU 层的连线
        stroke_pts(ctx, [(x, y + h - 40), (LX + LW / 2 + 20, LY[0])], 4, "#9CD1FF", 0.5 * a, dash=(12, 10), offset=-t * 40)
    # 两条时间注释
    for (tb, li, y0, head, body, col) in (
        (T_B1, 2, LY[2] - 70, "2025.9  Canonical 宣布", "CUDA 将进入 Ubuntu 官方软件源", "#E95420"),
        (T_B2, 3, LY[3] - 210, "2022  PyTorch 基金会成立", "由 Meta 开源，交给 Linux 基金会托管", "#3D7BFF"),
    ):
        ba = smooth(prog(t, tb, tb + 0.4)) * (1 - smooth(prog(t, T_WIDE, T_WIDE + 0.5)))
        if ba <= 0:
            continue
        k = ease_back(prog(t, tb, tb + 0.5), 1.5)
        x = 1330
        with at(ctx, x + 270, y0 + 70, 0.85 + 0.15 * k):
            card(ctx, -270, -78, 540, 156, 28, "#FFFFFF", ba, shadow=0.35)
            rrect(ctx, -270, -78, 14, 156, 7)
            fill(ctx, col, ba)
            text(ctx, head, -236, -28, 30, col, ba, "black", "l")
            text(ctx, body, -236, 26, 26, "#2B2233", ba, "bold", "l")
        stroke_pts(ctx, [(x, y0 + 70), (LX + LW / 2 + 20, LY[li])], 4, col, 0.6 * ba, dash=(12, 10), offset=-t * 40)


def wide_text(ctx, t):
    a = smooth(prog(t, T_WIDE + 0.8, T_WIDE + 1.4))
    if a <= 0:
        return
    x = 1540
    from ..core import text_reveal
    text_reveal(ctx, "不同公司", x, 360, 64, "#FFFFFF", prog(t, T_WIDE + 0.8, T_WIDE + 1.6), "black")
    text_reveal(ctx, "不同国家", x, 450, 64, "#FFFFFF", prog(t, T_WIDE + 1.2, T_WIDE + 2.0), "black")
    text_reveal(ctx, "严丝合缝", x, 560, 72, "#FFD25C", prog(t, T_WIDE + 1.8, T_WIDE + 2.6), "black")
    ic_gear(ctx, x, 700, 60 * smooth(prog(t, T_WIDE + 2.2, T_WIDE + 2.7)), 12, t * 2.5, "#FFD25C", a)


def sfx():
    out = [(4.2, "gears_run", {"dur": 14.4, "gain": 0.16})]
    for i, L in enumerate(LAYERS):
        out.append((L[4] - 0.4, "fall", {"dur": 0.45, "gain": 0.25}))
        out.append((L[4], "clunk", {"gain": 0.6, "pitch": 1.0 - i * 0.04}))
        if i > 0:
            out.append((L[4] + 0.05, "gear", {"dur": 0.6, "gain": 0.3}))
            out.append((L[4] - 0.12, "hop", {"gain": 0.2}))
    out += [(0.6, "surprise", {"gain": 0.25}),
            (T_TERM, "pop", {"gain": 0.4, "pitch": 0.8}),
            (T_TERM + 0.5, "typing", {"dur": 1.4, "gain": 0.35}),
            (T_TERM + 2.1, "scan", {"dur": 1.4, "gain": 0.25}),
            (T_TERM + 3.6, "success", {"gain": 0.45}),
            (T_TERM + 3.7, "fan", {"dur": 2.6, "gain": 0.35}),
            (T_B1, "pop", {"gain": 0.4, "pitch": 1.0}), (T_B1 + 0.2, "ding", {"gain": 0.3, "pitch": 1.1}),
            (T_B2, "pop", {"gain": 0.4, "pitch": 1.15}), (T_B2 + 0.2, "ding", {"gain": 0.3, "pitch": 1.3}),
            (T_WIDE, "whoosh", {"dur": 1.2, "gain": 0.4}),
            (T_WIDE + 0.4, "gears_run", {"dur": 5.0, "gain": 0.4}),
            (T_WIDE + 1.8, "impact_soft", {"gain": 0.4})]
    return out
