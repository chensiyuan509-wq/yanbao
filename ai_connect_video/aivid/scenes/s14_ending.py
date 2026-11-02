"""结语 · 开放的力量。

A 算力与算法的"军备竞赛"
B 底座互通、协议互联：一张生态网络
C 开放协同的土壤里长出产品之树（根 = 连接）
D 日出，孤岛之间架起光桥；片名收尾
"""
import math

from ..core import (TAU, W, H, Cam, at, circle, clamp, ease_back, ease_in, ease_io, ease_out,
                    ellipse, fill, glow, kf, lerp, line, lin, pop, poly, prog, rad, rng, rrect, setc,
                    smooth, text, text_w, view, sparkle_burst, ring_burst, stroke_pts, bezier_pts,
                    polyline_partial, point_on, font, light_rays, text_reveal, star4)
from ..icons import (ic_chatgpt, ic_claude_code, ic_codex, ic_docs, ic_github, ic_gmail, ic_gpu,
                     ic_muse, ic_openclaw, ic_opencode, ic_penguin, ic_ubuntu, ic_workbuddy, ic_sheets,
                     ic_slack, ic_instagram)
from ..mascot import Puppet
from ..ui import pill

DUR = 20.0
CHAPTER = ("结语", "开放的力量")

SUBS = [
    (0.8, 5.4, "AI 的下半场，不只是算力和算法的军备竞赛，"),
    (5.6, 9.8, "更是{底座互通}、{协议互联}的生态之战。"),
    (10.0, 14.4, "开放协同的土壤，才是先发优势真正的{根}。"),
    (14.6, 18.8, "愿每一座孤岛，都能架起通往彼此的桥。"),
]

T_NET, T_TREE, T_BRIDGE = 5.4, 9.8, 14.3

P = (Puppet(960, 905, 0.55, "determined", seed=14.4)
     .look(0, -0.8, -0.8).look(1.5, 0.8, -0.8)
     .expr(3.4, "worried").look(3.4, 0, -1.0)
     .expr(T_NET + 0.6, "curious").look(T_NET + 0.6, 0, -0.8).expr(7.6, "excited")
     .move(T_TREE - 0.3, T_TREE + 0.5, 1590, 905, walk=False).hop(T_TREE - 0.3, 110, 0.8).land(T_TREE + 0.5)
     .expr(T_TREE + 1.2, "smile").look(T_TREE + 1.2, -1.0, -0.8).expr(12.6, "proud")
     .fade(T_BRIDGE - 0.6, 0.0, 0.4))

P2 = (Puppet(960, 676, 0.5, "happy", seed=15.1)
      .fade(-1, 0.0, 0.01).fade(T_BRIDGE + 0.1, 1.0, 0.3)
      .hop(T_BRIDGE + 1.3, 70).expr(T_BRIDGE + 1.3, "excited").hop(T_BRIDGE + 2.2, 70)
      .wave(16.4, 19.2, "r").expr(16.6, "happy"))

CAM = Cam([
    (0.0, (960, 540, 1.0)), (5.2, (960, 530, 1.05)),
    (5.9, (960, 540, 1.0), ease_io), (9.6, (960, 540, 1.05)),
    (10.2, (960, 560, 1.0), ease_io), (14.1, (960, 520, 1.06)),
    (14.8, (960, 560, 0.98), ease_io), (20.0, (960, 545, 1.04)),
], drift=4, seed=53.0)


def draw(ctx, t):
    dawn = smooth(prog(t, 0, 18))
    ctx.set_source(lin(0, 0, 0, H, [(0, mixc("#14244A", "#3B5A9A", dawn)), (0.55, mixc("#3A3770", "#F2A27C", dawn)),
                                     (1, mixc("#6B4B7A", "#FFD7A6", dawn))]))
    ctx.paint()
    cam = CAM.at(t)
    with view(ctx, cam, 0.4):
        sun_y = lerp(1100, 700, dawn)
        glow(ctx, 960, sun_y, 900, "#FFE2B0", 0.35 + 0.35 * dawn)
        light_rays(ctx, 960, sun_y, 16, 1500, "#FFF1D6", 0.12 * dawn, t * 0.03, 0.12)
    with view(ctx, cam):
        part_a(ctx, t)
        part_b(ctx, t)
        part_c(ctx, t)
        part_d(ctx, t)
        P.draw(ctx, t)
    end_title(ctx, t)
    fo = smooth(prog(t, 19.2, 20.0))
    if fo > 0:
        ctx.set_source_rgba(0, 0, 0, fo)
        ctx.paint()


def mixc(a, b, t):
    from ..core import mix
    return mix(a, b, t)


# ---------------------------------------------------------------- A 军备竞赛

def part_a(ctx, t):
    a = smooth(prog(t, 0.0, 0.5)) * (1 - smooth(prog(t, T_NET - 0.4, T_NET + 0.2)))
    if a <= 0:
        return
    grow = ease_out(prog(t, 0.4, 3.6))
    # 左：算力塔（显卡越堆越高）
    n = int(1 + grow * 6)
    for i in range(n):
        k = pop(t, 0.4 + i * 0.45, 0.35)
        ic_gpu(ctx, 520, 820 - i * 92, 260 * k, a, t, t * 3 + i)
    pill(ctx, "算力", 520, 900, 44, "#FFFFFF", "#76B900", a, 1.0, weight="black")
    # 右：算法塔（公式方块越堆越高）
    syms = ["∑", "∫", "∂", "λ", "∇", "π", "θ"]
    for i in range(n):
        k = pop(t, 0.6 + i * 0.45, 0.35)
        with at(ctx, 1400, 820 - i * 92, k):
            rrect(ctx, -110, -40, 220, 80, 18)
            ctx.set_source(lin(0, -40, 0, 40, [(0, "#9B85FF", a), (1, "#6D4FE0", a)]))
            ctx.fill()
            text(ctx, syms[i % len(syms)], 0, 0, 54, "#FFFFFF", a, "serif")
    pill(ctx, "算法", 1400, 900, 44, "#FFFFFF", "#6D4FE0", a, 1.0, weight="black")
    # 向上的竞赛箭头
    for x in (720, 1200):
        for j in range(3):
            ph = (t * 0.8 + j / 3) % 1
            from ..core import arrow
            arrow(ctx, x, 800 - ph * 500, x, 760 - ph * 500 - 60, 8, "#FFD25C", a * math.sin(ph * math.pi))
    vk = pop(t, 1.6, 0.45)
    if vk > 0:
        with at(ctx, 960, 300, vk):
            pill(ctx, "军备竞赛？", 0, 0, 52, "#FFFFFF", "#E5484D", a, 0.95, weight="black")


# ---------------------------------------------------------------- B 生态网络

NODES = [
    (ic_chatgpt, (520, 300)), (ic_claude_code, (820, 220)), (ic_codex, (1110, 230)), (ic_muse, (1400, 310)),
    (ic_openclaw, (400, 560)), (ic_workbuddy, (1520, 560)), (ic_gmail, (560, 790)), (ic_docs, (820, 860)),
    (ic_github, (1100, 860)), (ic_ubuntu, (1360, 790)), (ic_gpu, (960, 560)),
]
EDGES = [(0, 10, "API"), (1, 10, "CUDA"), (2, 10, "Linux"), (3, 6, "MCP"), (3, 7, "MCP"), (1, 8, "开源"),
         (4, 6, "API"), (5, 7, "MCP"), (0, 1, ""), (1, 2, ""), (2, 3, ""), (9, 10, "CUDA"), (4, 10, ""),
         (5, 10, ""), (6, 7, ""), (7, 8, ""), (8, 9, ""), (0, 4, ""), (3, 5, "")]


def part_b(ctx, t):
    a = smooth(prog(t, T_NET - 0.2, T_NET + 0.4)) * (1 - smooth(prog(t, T_TREE - 0.3, T_TREE + 0.3)))
    if a <= 0:
        return
    for k, (i, j, lab) in enumerate(EDGES):
        t0 = T_NET + 0.5 + k * 0.12
        lp = ease_out(prog(t, t0, t0 + 0.5))
        if lp <= 0:
            continue
        (x0, y0), (x1, y1) = NODES[i][1], NODES[j][1]
        stroke_pts(ctx, [(x0, y0), (lerp(x0, x1, lp), lerp(y0, y1, lp))], 5, "#FFE3A3", 0.55 * a)
        if lp >= 1:
            u = ((t - t0) * 0.7 + k * 0.17) % 1
            glow(ctx, lerp(x0, x1, u), lerp(y0, y1, u), 18, "#FFFFFF", 0.8 * a)
            if lab:
                lk = pop(t, t0 + 0.5, 0.4)
                with at(ctx, (x0 + x1) / 2, (y0 + y1) / 2, lk):
                    pill(ctx, lab, 0, 0, 24, "#2B2233", "#FFE3A3", a, 0.95, weight="black")
    for k, (ic, (x, y)) in enumerate(NODES):
        kk = pop(t, T_NET + 0.2 + k * 0.08, 0.45)
        if kk <= 0:
            continue
        glow(ctx, x, y, 110, "#FFFFFF", 0.25 * a)
        if ic is ic_gpu:
            ic(ctx, x, y, 200 * kk, a, t, t * 2)
        else:
            ic(ctx, x, y, 104 * kk, a, t)


# ---------------------------------------------------------------- C 产品之树

_R = rng(5)


def _branches():
    """生成树枝：[(起点, 终点, 生长开始比例, 粗细, 层级)]。"""
    out = []

    def rec(x, y, ang, length, width, depth, start):
        x1, y1 = x + math.cos(ang) * length, y + math.sin(ang) * length
        out.append(((x, y), (x1, y1), start, width, depth))
        if depth >= 4:
            return
        for d in (-1, 1):
            rec(x1, y1, ang + d * _R.uniform(0.32, 0.6), length * _R.uniform(0.66, 0.78), width * 0.68,
                depth + 1, start + 0.18)

    rec(960, 770, -math.pi / 2, 215, 44, 0, 0.0)
    return out


BRANCHES = _branches()
LEAF_ICONS = [ic_chatgpt, ic_claude_code, ic_codex, ic_muse, ic_openclaw, ic_workbuddy, ic_opencode,
              ic_gmail, ic_docs, ic_sheets, ic_slack, ic_github, ic_instagram]
TIPS = [b for b in BRANCHES if b[4] == 4]


def part_c(ctx, t):
    a = smooth(prog(t, T_TREE - 0.2, T_TREE + 0.4)) * (1 - smooth(prog(t, T_BRIDGE - 0.4, T_BRIDGE + 0.2)))
    if a <= 0:
        return
    g = prog(t, T_TREE + 0.2, T_TREE + 3.0)
    # 土壤
    rrect(ctx, 300, 760, 1320, 160, 60)
    ctx.set_source(lin(0, 760, 0, 920, [(0, "#7A4E33", a), (1, "#4A2E1E", a)]))
    ctx.fill()
    text(ctx, "开放协同的土壤", 960, 886, 34, "#FFE3B3", a * smooth(prog(t, T_TREE, T_TREE + 0.4)), "black")
    # 根（连接线）
    for k in range(9):
        rp = ease_out(prog(t, T_TREE + 0.1 + k * 0.05, T_TREE + 1.3 + k * 0.05))
        if rp <= 0:
            continue
        ex = 960 + (k - 4) * 150
        pts = bezier_pts((960, 776), (960 + (k - 4) * 30, 810), (ex, 820), (ex + (k - 4) * 20, 850), 20)
        stroke_pts(ctx, polyline_partial(pts, rp), 6 - abs(k - 4) * 0.6, "#FFC65C", 0.85 * a)
        (gx, gy), _ = point_on(pts, ((t * 0.5 + k * 0.13) % 1))
        glow(ctx, gx, gy, 16, "#FFE3A3", 0.7 * a * rp)
    rk = pop(t, T_TREE + 2.4, 0.45)
    if rk > 0:
        with at(ctx, 470, 700, rk):
            pill(ctx, "根 = 连接", 0, 0, 38, "#4A2E1E", "#FFC65C", a, 1.0, weight="black")
    # 树干与枝条
    for (p0, p1, st, wdt, dep) in BRANCHES:
        u = clamp((g - st) / 0.28)
        if u <= 0:
            continue
        x1, y1 = lerp(p0[0], p1[0], ease_out(u)), lerp(p0[1], p1[1], ease_out(u))
        line(ctx, p0[0], p0[1], x1, y1, wdt, "#8A5A3C", a)
        line(ctx, p0[0] - wdt * 0.15, p0[1], x1 - wdt * 0.15, y1, wdt * 0.35, "#B07A55", 0.6 * a)
    # 叶子 = 产品
    for k, (p0, p1, st, wdt, dep) in enumerate(TIPS):
        lk = pop(t, T_TREE + 2.0 + k * 0.1, 0.45)
        if lk <= 0:
            continue
        glow(ctx, p1[0], p1[1], 90, "#B8F5C8", 0.35 * a)
        LEAF_ICONS[k % len(LEAF_ICONS)](ctx, p1[0], p1[1], 62 * lk, a, t)


# ---------------------------------------------------------------- D 光桥

ISLES = [(260, 690, "微信"), (610, 640, "淘宝"), (960, 690, ""), (1310, 640, "抖音"), (1660, 690, "小红书")]


def part_d(ctx, t):
    a = smooth(prog(t, T_BRIDGE - 0.2, T_BRIDGE + 0.5))
    if a <= 0:
        return
    # 海面
    ctx.rectangle(-400, 720, 2800, 600)
    ctx.set_source(lin(0, 720, 0, 1200, [(0, "#F7B98F", 0.9 * a), (1, "#8A6A9A", a)]))
    ctx.fill()
    for j in range(6):
        y = 760 + j * 50
        ctx.move_to(-400, y)
        for x in range(-400, 2400, 60):
            ctx.line_to(x, y + math.sin(x * 0.012 + t * 1.3 + j) * 5)
        ctx.set_line_width(2.5)
        setc(ctx, "#FFFFFF", 0.18 * a)
        ctx.stroke()
    # 光桥
    for k in range(4):
        (x0, y0, _), (x1, y1, _) = ISLES[k], ISLES[k + 1]
        t0 = T_BRIDGE + 0.6 + k * 0.35
        bp = ease_out(prog(t, t0, t0 + 0.7))
        if bp <= 0:
            continue
        pts = bezier_pts((x0 + 60, y0 - 10), (x0 + 120, y0 - 170), (x1 - 120, y1 - 170), (x1 - 60, y1 - 10), 30)
        seg = polyline_partial(pts, bp)
        stroke_pts(ctx, seg, 14, "#FFE3A3", 0.5 * a)
        stroke_pts(ctx, seg, 5, "#FFFFFF", 0.95 * a)
        if bp >= 1:
            u = ((t - t0) * 0.6 + k * 0.25) % 1
            (gx, gy), _ = point_on(pts, u)
            glow(ctx, gx, gy, 24, "#FFFFFF", 0.9 * a)
    # 岛屿
    for (x, y, name) in ISLES:
        ellipse(ctx, x, y + 20, 170, 40)
        fill(ctx, "#FFFFFF", 0.15 * a)
        ctx.move_to(x - 140, y)
        ctx.curve_to(x - 140, y + 70, x + 140, y + 70, x + 140, y)
        ctx.close_path()
        fill(ctx, "#6A5A4A", a)
        ellipse(ctx, x, y, 140, 42)
        ctx.set_source(lin(0, y - 42, 0, y + 42, [(0, "#9FE0A6", a), (1, "#5FAE6E", a)]))
        ctx.fill()
        if name:
            with at(ctx, x, y - 70 + math.sin(t * 1.5 + x) * 4, 1):
                pill(ctx, name, 0, 0, 34, "#FFFFFF", "#2B2233", a, 0.75, weight="black")
    P2.draw(ctx, t)
    sparkle_burst(ctx, t, T_BRIDGE + 2.0, 960, 560, 14, 420, "#FFE3A3", 1.2, 6, 22)


def end_title(ctx, t):
    a = smooth(prog(t, 16.2, 17.0)) * (1 - smooth(prog(t, 19.3, 19.9)))
    if a <= 0:
        return
    glow(ctx, 960, 250, 520, "#FFFFFF", 0.25 * a)
    p = prog(t, 16.2, 17.2)
    text_reveal(ctx, "连接的力量", 960, 230, 120, "#FFFFFF", p, "black", rise=30)
    text(ctx, "开放，才是 AI 时代最深的护城河", 960, 340, 42, "#4A2E50", a * smooth(prog(t, 16.9, 17.5)), "black")


def sfx():
    out = [(0.0, "ambience_dawn", {"dur": 20.0, "gain": 0.4})]
    for i in range(7):
        out.append((0.4 + i * 0.45, "clunk", {"gain": 0.3, "pitch": 1.2 + i * 0.05}))
    out += [(1.6, "alert", {"gain": 0.35}), (T_NET - 0.3, "whoosh", {"dur": 1.0, "gain": 0.4})]
    for k in range(len(NODES)):
        out.append((T_NET + 0.2 + k * 0.08, "pop", {"gain": 0.2, "pitch": 1.0 + k * 0.05}))
    for k, (i, j, lab) in enumerate(EDGES):
        if lab:
            out.append((T_NET + 1.0 + k * 0.12, "blip", {"gain": 0.25, "pitch": 1.2 + (k % 4) * 0.1}))
    out += [(T_TREE - 0.3, "whoosh", {"dur": 1.0, "gain": 0.4}), (T_TREE + 0.2, "grow", {"dur": 2.8, "gain": 0.4})]
    for k in range(len(TIPS)):
        out.append((T_TREE + 2.0 + k * 0.1, "pop", {"gain": 0.2, "pitch": 1.2 + (k % 6) * 0.08}))
    out += [(T_TREE + 2.4, "chime", {"gain": 0.35}),
            (T_BRIDGE - 0.3, "whoosh", {"dur": 1.0, "gain": 0.4})]
    for k in range(4):
        out.append((T_BRIDGE + 0.6 + k * 0.35, "bridge", {"gain": 0.4, "pitch": 1.0 + k * 0.12}))
    out += [(T_BRIDGE + 1.3, "boing", {"gain": 0.3}), (T_BRIDGE + 2.0, "shimmer", {"dur": 2.0, "gain": 0.4}),
            (T_BRIDGE + 2.2, "boing", {"gain": 0.3}), (16.2, "finale", {"gain": 0.55})]
    return out
