"""第四章（2/2）：数据授权（Reddit → Google / OpenAI）与"行为数据"喂养下一代模型。"""
import math

from ..core import (TAU, W, H, Cam, at, circle, clamp, ease_back, ease_in, ease_io, ease_out,
                    fill, glow, kf, lerp, line, lin, pop, prog, rrect, setc, smooth, text, text_w,
                    view, sparkle_burst, ring_burst, bezier_pts, point_on, stroke_pts,
                    polyline_partial, font)
from ..icons import ic_brain, ic_coin, ic_reddit, ic_scroll, google_word
from ..mascot import Puppet
from ..ui import card, pill
from .common import light_bg

DUR = 15.0
CHAPTER = ("04", "语料：模型的粮食")

SUBS = [
    (0.6, 7.2, "美国平台还会把数据「{授权}」出去：Reddit 就授权给了 Google 和 OpenAI。"),
    (7.4, 14.6, "更宝贵的新语料是「{行为}」：工具怎么调、结果对不对、用户满不满意。"),
]

RD = (500, 440)
BUYERS = [("google", (1430, 300), 1.3), ("openai", (1430, 600), 2.3)]
CON = (2560, 450)          # 日志面板中心
ORB = (3420, 450)

LOG = [
    ("▶ 调用工具  查询航班(上海, 周五)", "#8AB4FF", 8.0),
    ("✓ 返回 3 个航班", "#7CFFB2", 8.55),
    ("▶ 调用工具  填写订单", "#8AB4FF", 9.0),
    ("× 报错：证件号格式不对", "#FF7A85", 9.5),
    ("◆ 自动修正后重试", "#FFC65C", 10.0),
    ("✓ 下单成功", "#7CFFB2", 10.45),
    ("★ 用户反馈：满意", "#FFC65C", 10.9),
]
T_PACK = 11.6

P = (Puppet(960, 905, 0.6, "curious", seed=9.9)
     .look(0, -0.8, -0.6)
     .expr(1.4, "happy").look(1.4, 1.0, -0.7)
     .expr(3.3, "excited").hop(3.4, 40).hop(3.9, 40).look(3.3, -0.8, -0.4)
     .move(6.95, 7.85, 2010, 905, walk=False).hop(6.95, 160, 0.9).land(7.85)
     .expr(7.9, "curious").look(7.9, 1.0, -0.6)
     .expr(9.5, "worried").expr(10.1, "think").expr(10.5, "happy")
     .expr(T_PACK + 0.6, "surprised").look(T_PACK + 0.6, 1.0, -0.5)
     .expr(13.0, "proud").nod(13.2))

CAM = Cam([
    (0.0, (960, 520, 1.0)),
    (6.9, (990, 520, 1.03)),
    (7.9, (2790, 520, 1.0), ease_io),
    (15.0, (2820, 515, 1.03)),
], drift=5, seed=23.0)


def draw(ctx, t):
    light_bg(ctx, "#F5F2FF", "#E2DAF6", dots="#9C8BD6", dot_a=0.14, spacing=64, drift=(-t * 8, 0))
    cam = CAM.at(t)
    with view(ctx, cam, 0.5):
        glow(ctx, 900, 430, 700, "#FFFFFF", 0.5)
        glow(ctx, 2300, 430, 700, "#FFFFFF", 0.4)
    with view(ctx, cam):
        if cam[0] < 2500:
            part_a(ctx, t)
        if cam[0] > 1300:
            part_b(ctx, t)
        P.draw(ctx, t)


def _buyer(ctx, kind, x, y, a, k):
    with at(ctx, x, y, k):
        card(ctx, -230, -80, 460, 160, 40, "#FFFFFF", a, shadow=0.2)
        if kind == "google":
            google_word(ctx, 0, 0, 70, a)
        else:
            circle(ctx, -120, 0, 40)
            fill(ctx, "#111111", a)
            from ..core import star4
            star4(ctx, -120, 0, 26, "#FFFFFF", a, 0.3)
            text(ctx, "OpenAI", 40, 0, 60, "#111111", a, "black")


def part_a(ctx, t):
    a = 1.0
    # Reddit
    rk = pop(t, 0.2, 0.5)
    if rk > 0:
        glow(ctx, RD[0], RD[1], 260, "#FF4500", 0.18)
        ic_reddit(ctx, RD[0], RD[1], 210 * rk, a, t)
        text(ctx, "Reddit 社区内容", RD[0], RD[1] + 160, 38, "#3A2E4A", min(1, rk), "black")
    for i, (kind, (bx, by), t0) in enumerate(BUYERS):
        k = pop(t, 0.5 + i * 0.25, 0.5)
        if k <= 0:
            continue
        # 数据流（曲线）
        pts = bezier_pts((RD[0] + 110, RD[1]), (900, RD[1] + (by - RD[1]) * 0.2 - 120 + i * 240),
                         (1050, by), (bx - 240, by), 36)
        lp = ease_out(prog(t, t0 - 0.3, t0 + 0.4))
        stroke_pts(ctx, polyline_partial(pts, lp), 6, "#FF8A50", 0.35, dash=(16, 12), offset=-t * 60)
        if t > t0 + 0.5:
            for d in range(5):
                u = ((t - t0) * 0.55 + d / 5) % 1
                (gx, gy), _ = point_on(pts, u)
                glow(ctx, gx, gy, 18, "#FFB27A", 0.85 * math.sin(u * math.pi))
        # 合同卷轴飞过去
        u = prog(t, t0 - 0.4, t0 + 0.5)
        if 0 < u < 1:
            (sx, sy), _ = point_on(pts, ease_io(u))
            ic_scroll(ctx, sx, sy - 40 * math.sin(u * math.pi), 110, 1.0, t)
        _buyer(ctx, kind, bx, by, a, k)
        ck = pop(t, t0 + 0.5, 0.4)
        if ck > 0:
            with at(ctx, bx + 210, by - 70, ck):
                circle(ctx, 0, 0, 30)
                fill(ctx, "#3CCB7F")
                from ..core import check_mark
                check_mark(ctx, 0, 1, 34, "#FFFFFF", prog(t, t0 + 0.6, t0 + 0.9))
            pill(ctx, "数据授权协议", bx, by + 120, 28, "#FFFFFF", "#FF7A45", ck, 1.0)
        # 金币回流
        for c in range(4):
            cu = prog(t, 3.2 + i * 0.3 + c * 0.22, 4.1 + i * 0.3 + c * 0.22)
            if 0 < cu < 1:
                cx = lerp(bx - 200, RD[0] + 80, ease_io(cu))
                cy = lerp(by, RD[1] - 60, ease_io(cu)) - math.sin(cu * math.pi) * 180
                ic_coin(ctx, cx, cy, 56, 1.0, t, spin=t * 2 + c)
    yk = pop(t, 2.9, 0.45)
    if yk > 0:
        with at(ctx, 1000, 150, yk):
            pill(ctx, "2024 年起：内容授权给 AI 公司训练模型", 0, 0, 34, "#FFFFFF", "#3A2E4A", 1.0, 0.85)


def part_b(ctx, t):
    a = smooth(prog(t, 7.2, 7.9))
    if a <= 0:
        return
    x, y = CON
    w, h = 880, 560
    card(ctx, x - w / 2, y - h / 2, w, h, 34, "#1C1A26", a, shadow=0.35)
    ctx.save()
    rrect(ctx, x - w / 2, y - h / 2, w, h, 34)
    ctx.clip()
    ctx.rectangle(x - w / 2, y - h / 2, w, 60)
    fill(ctx, "#2A2735", a)
    ctx.restore()
    for k, c in enumerate(("#FF6159", "#FFBD2E", "#28C941")):
        circle(ctx, x - w / 2 + 32 + k * 26, y - h / 2 + 30, 8)
        fill(ctx, c, a)
    text(ctx, "智能体运行日志", x, y - h / 2 + 30, 28, "#BDB7CC", a, "bold")
    pack = prog(t, T_PACK, T_PACK + 1.2)
    for i, (s, col, t0) in enumerate(LOG):
        if t < t0:
            break
        ly = y - h / 2 + 108 + i * 64
        st = T_PACK + i * 0.1
        u = prog(t, st, st + 0.8)
        if u <= 0:
            n = min(len(s), int((t - t0) * 40))
            text(ctx, s[:n], x - w / 2 + 46, ly, 34, col, a, "bold", "l")
        elif u < 1:
            # 文字收缩成光块飞向模型
            e = ease_in(u)
            sx, sy = x - w / 2 + 280, ly
            px = lerp(sx, ORB[0], e)
            py = lerp(sy, ORB[1], e) - math.sin(u * math.pi) * 120
            sz = lerp(50, 18, e)
            glow(ctx, px, py, sz * 1.8, col, 0.6)
            rrect(ctx, px - sz / 2, py - sz / 2, sz, sz, sz * 0.25)
            fill(ctx, col, 0.95)
    # 模型球
    ok = ease_back(prog(t, 7.6, 8.2), 1.4)
    if ok > 0:
        absorbed = sum(1 for i in range(len(LOG)) if t > T_PACK + i * 0.1 + 0.8)
        grow = 1 + 0.06 * absorbed
        pulse = max([0.0] + [1 - (t - (T_PACK + i * 0.1 + 0.8)) / 0.3 for i in range(len(LOG))
                             if 0 < t - (T_PACK + i * 0.1 + 0.8) < 0.3])
        glow(ctx, ORB[0], ORB[1], 330 * grow, "#8B6CFF", (0.25 + 0.06 * absorbed + 0.25 * pulse) * a)
        ic_brain(ctx, ORB[0], ORB[1], 230 * ok * grow, a, t, glow_a=0.2)
        lab = "下一代模型" if absorbed >= len(LOG) else "模型"
        text(ctx, lab, ORB[0], ORB[1] + 190 * grow, 40, "#3A2E4A", a, "black")
        if absorbed >= len(LOG):
            sparkle_burst(ctx, t, T_PACK + 0.6 + 0.8 + 0.05, ORB[0], ORB[1], 12, 300, "#FFC65C", 0.9, 4, 22)
    tk = pop(t, 12.4, 0.45)
    if tk > 0:
        with at(ctx, (CON[0] + ORB[0]) / 2 + 60, 860, tk):
            pill(ctx, "真实使用中的「行为数据」→ 训练下一代模型", 0, 0, 32, "#FFFFFF", "#6D4FE0", 1.0, 0.95)


def sfx():
    out = [(0.2, "pop", {"gain": 0.4, "pitch": 0.8}), (0.5, "pop", {"gain": 0.3, "pitch": 1.1}),
           (0.75, "pop", {"gain": 0.3, "pitch": 1.2})]
    for (kind, _, t0) in BUYERS:
        out.append((t0 - 0.4, "paper", {"gain": 0.45}))
        out.append((t0 + 0.5, "check", {"gain": 0.4}))
    for i in range(2):
        for c in range(4):
            out.append((4.0 + i * 0.3 + c * 0.22, "coin", {"gain": 0.35, "pitch": 1.0 + c * 0.06}))
    out += [(2.9, "pop", {"gain": 0.3, "pitch": 0.9}), (3.4, "hop", {"gain": 0.2}), (3.9, "hop", {"gain": 0.2}),
            (6.95, "whoosh", {"dur": 1.1, "gain": 0.45}), (7.85, "thud", {"gain": 0.25}),
            (7.6, "pop", {"gain": 0.35, "pitch": 0.8})]
    for (s, col, t0) in LOG:
        snd = "error" if s.startswith("×") else ("ding" if s.startswith("★") else "blip")
        out.append((t0, snd, {"gain": 0.35 if snd != "ding" else 0.3, "pitch": 1.2}))
        out.append((t0, "typing", {"dur": 0.35, "gain": 0.18}))
    for i in range(len(LOG)):
        out.append((T_PACK + i * 0.1 + 0.8, "blip", {"gain": 0.25, "pitch": 1.5 + i * 0.08}))
    out += [(T_PACK, "whoosh", {"dur": 1.0, "gain": 0.4}), (T_PACK + 1.45, "powerup", {"gain": 0.45}),
            (12.4, "pop", {"gain": 0.3, "pitch": 0.9})]
    return out
