"""第二章（2/2）：四年演进时间轴 → 镜头下摇到美国西海岸，领跑公司在地图上落钉。"""
import math

from ..core import (TAU, W, H, Cam, at, circle, clamp, ease_back, ease_in, ease_io, ease_io5,
                    ease_out, fill, glow, kf, lerp, line, lin, pop, poly, prog, rad, rrect, setc,
                    smooth, stars, text, text_w, view, sparkle_burst, ring_burst, bezier_pts,
                    stroke_pts, polyline_partial, bokeh)
from ..icons import (ic_chatgpt, ic_claude_code, ic_codex, ic_muse, ic_openclaw, ic_plug,
                     ic_workbuddy, ic_terminal)
from ..mascot import Puppet
from ..ui import card, pill

DUR = 13.0
CHAPTER = ("02", "什么是 Agent 智能体")

SUBS = [
    (0.6, 5.8, "短短四年，AI 从「{陪你聊}」走到了「{替你干}」。"),
    (6.0, 12.6, "领跑的 OpenAI、Anthropic、Google、Meta……几乎都在{美国}。"),
]

LINE_Y = 700
MS = [  # (x, 年份, 标题, 能力, 图标们, 颜色)
    (420, "2022.11", "ChatGPT 上线", "会聊天", (ic_chatgpt,), "#19C39C"),
    (1020, "2023", "插件 · 函数调用", "会用工具", ("plug",), "#4C8DFF"),
    (1620, "2024.11", "MCP 协议开源", "会连接", ("mcp",), "#8B6CFF"),
    (2220, "2025", "编程智能体", "会写代码", (ic_claude_code, ic_codex), "#FF9F68"),
    (2820, "2026", "个人 / 办公智能体", "替你干活", (ic_openclaw, ic_workbuddy, ic_muse), "#FF6B9A"),
]
T_MS = [0.9 + i * 0.95 for i in range(5)]

# 地图区域
MAP_C = (1650, 1600)
PINS = [  # (公司, 城市, 圆点颜色, 地图钉位置, 名片位置, 出现时间)
    ("Microsoft", "雷德蒙德", "#4C8DFF", (1290, 1270), (1720, 1290), 7.1),
    ("OpenAI", "旧金山", "#19C39C", (1296, 1650), (1720, 1430), 7.5),
    ("Anthropic", "旧金山", "#E88E64", (1306, 1662), (1720, 1530), 7.75),
    ("Meta", "门洛帕克", "#3D7BFF", (1330, 1690), (1720, 1630), 8.0),
    ("Google", "山景城", "#34A853", (1345, 1708), (1720, 1730), 8.25),
    ("NVIDIA", "圣克拉拉", "#76B900", (1362, 1726), (1720, 1830), 8.5),
]

P = Puppet(240, LINE_Y, 0.5, "excited", seed=6.6).look(0, 1.0, -0.2)
for i, (x, *_r) in enumerate(MS):
    t0 = T_MS[i] - 0.55
    P.move(t0, T_MS[i], x, LINE_Y, walk=False, ease=ease_io).hop(t0, 70, 0.55)
    P.expr(T_MS[i], ["happy", "curious", "excited", "proud", "excited"][i])
P.look(5.3, 0.3, 0.8).expr(5.5, "surprised").hop(5.75, 60, 0.4)
P.move(5.9, 7.0, 2400, 1905, walk=False, ease=ease_in).land(7.0).expr(7.05, "excited").look(7.05, -1.0, -0.4)
P.scale(5.9, 0.62, 1.1)
P.expr(9.0, "proud").nod(9.2)

CAM = Cam([
    (0.0, (640, 500, 1.0)),
    (1.0, (740, 500, 1.0)),
    (5.0, (2640, 500, 1.0), lambda u: u),
    (5.5, (2700, 520, 0.96), ease_out),
    (7.0, (MAP_C[0], MAP_C[1] - 20, 1.0), ease_io),
    (13.0, (MAP_C[0] + 20, MAP_C[1], 1.05)),
], drift=6, seed=14.0)


def draw(ctx, t):
    ctx.set_source(lin(0, 0, 0, H, [(0, "#0D1230"), (1, "#271E4D")]))
    ctx.paint()
    cam = CAM.at(t)
    with view(ctx, cam, 0.25):
        stars(ctx, t, 120, 44, area=(-600, -400, W + 1600, H + 1400), a=0.7)
    with view(ctx, cam, 0.5):
        bokeh(ctx, t, 18, 46, ("#8B6CFF", "#FF9F68", "#4C8DFF"), area=(-400, -200, W + 2400, H + 1600),
              r=(40, 110), a=(0.05, 0.12))
    with view(ctx, cam):
        draw_timeline(ctx, t)
        draw_map(ctx, t)
        P.draw(ctx, t)


def _ms_icon(ctx, kind, x, y, s, a, t):
    if kind == "plug":
        ic_plug(ctx, x, y, s, a, t, "#4C8DFF", -0.6)
    elif kind == "mcp":
        rrect(ctx, x - s / 2, y - s / 2, s, s, s * 0.24)
        ctx.set_source(lin(0, y - s / 2, 0, y + s / 2, [(0, "#A58BFF", a), (1, "#6D4FE0", a)]))
        ctx.fill()
        text(ctx, "MCP", x, y, s * 0.32, "#FFFFFF", a, "black")
    else:
        kind(ctx, x, y, s, a, t)


def draw_timeline(ctx, t):
    a = 1 - smooth(prog(t, 7.0, 7.6))
    if a <= 0:
        return
    # 主轴（渐变光带，随小橙推进点亮）
    lit = kf(t, [(0, 260), (T_MS[-1], 2900)], ease_io)
    ctx.set_line_width(8)
    ctx.set_line_cap(1)
    setc(ctx, "#3A3570", a)
    ctx.move_to(150, LINE_Y)
    ctx.line_to(3150, LINE_Y)
    ctx.stroke()
    ctx.set_source(lin(150, 0, 3000, 0, [(0, "#19C39C", a), (0.35, "#4C8DFF", a), (0.55, "#8B6CFF", a),
                                         (0.78, "#FF9F68", a), (1, "#FF6B9A", a)]))
    ctx.move_to(150, LINE_Y)
    ctx.line_to(lit, LINE_Y)
    ctx.stroke()
    glow(ctx, lit, LINE_Y, 60, "#FFFFFF", 0.5 * a)
    # 箭头
    from ..core import arrow_head
    arrow_head(ctx, 3190, LINE_Y, 0, 40, "#FF6B9A", a * smooth(prog(t, 4.6, 5.0)))
    for i, (x, year, title, cap, icons, col) in enumerate(MS):
        k = pop(t, T_MS[i] - 0.05, 0.5)
        circle(ctx, x, LINE_Y, 16)
        fill(ctx, col if t > T_MS[i] else "#3A3570", a)
        if k <= 0:
            continue
        ring_burst(ctx, t, T_MS[i], x, LINE_Y, 16, 110, col, 0.6, 6)
        text(ctx, year, x, LINE_Y + 62, 44, "#FFFFFF", a * min(1, k), "black")
        # 卡片
        cw, ch = 500, 300
        cy = LINE_Y - 230 - ch / 2
        with at(ctx, x, cy + (1 - min(k, 1)) * 40, k):
            card(ctx, -cw / 2, -ch / 2, cw, ch, 30, "#FFFFFF", a, shadow=0.35)
            n = len(icons)
            for j, ic in enumerate(icons):
                _ms_icon(ctx, ic, (j - (n - 1) / 2) * 122, -70, 104, a, t)
            text(ctx, title, 0, 30, 40, "#2B2233", a, "black")
            pill(ctx, cap, 0, 100, 34, "#FFFFFF", col, a, 1.0, weight="black")
        # 连接竖线
        line(ctx, x, LINE_Y - 16, x, cy + ch / 2 * k, 3, col, 0.5 * a * min(1, k))
        sparkle_burst(ctx, t, T_MS[i], x, cy - ch / 2, 7, 140, "#FFE3A3", 0.7, i + 3, 16)
    # 9 亿用户的小注释
    nk = pop(t, 1.6, 0.45)
    if nk > 0:
        with at(ctx, 420, LINE_Y + 136, nk):
            pill(ctx, "2026 年初：每周约 9 亿人在用", 0, 0, 30, "#FFE3B3", "#19C39C", a, 0.35)


def draw_map(ctx, t):
    a = smooth(prog(t, 5.9, 6.8))
    if a <= 0:
        return
    cx, cy = MAP_C
    # 海洋与陆地
    glow(ctx, 1300, 1640, 600, "#4C8DFF", 0.25 * a)
    coast = bezier_pts((1250, 1180), (1310, 1380), (1180, 1520), (1300, 1660), 40)
    coast += bezier_pts((1300, 1660), (1380, 1760), (1420, 1860), (1520, 2050), 40)[1:]
    land = coast + [(2600, 2050), (2600, 1180)]
    poly(ctx, land)
    ctx.set_source(lin(1250, 0, 2600, 0, [(0, "#3B3878", 0.95 * a), (1, "#26244F", 0.5 * a)]))
    ctx.fill()
    # 经纬网格
    ctx.save()
    poly(ctx, land)
    ctx.clip()
    ctx.set_line_width(2)
    setc(ctx, "#8C86D8", 0.16 * a)
    for gx in range(1100, 2700, 120):
        ctx.move_to(gx, 1150)
        ctx.line_to(gx - 60, 2080)
    for gy in range(1180, 2080, 120):
        ctx.move_to(1100, gy)
        ctx.line_to(2650, gy + 30)
    ctx.stroke()
    ctx.restore()
    stroke_pts(ctx, polyline_partial(coast, ease_out(prog(t, 6.0, 7.0))), 6, "#7CC6FF", 0.75 * a)
    # 标题
    tk = pop(t, 6.6, 0.5)
    if tk > 0:
        with at(ctx, 2120, 1180, tk):
            text(ctx, "美国 · 西海岸", 0, 0, 64, "#FFFFFF", a, "black", shadow=(0, 4, "#000000", 0.35))
    # 城市圈
    for (lab, x, y, tt) in (("西雅图", 1150, 1270, 7.0), ("旧金山湾区", 1120, 1690, 7.4)):
        k = smooth(prog(t, tt, tt + 0.4))
        text(ctx, lab, x, y, 30, "#CFE3FF", a * k, "bold", "r")
    gk = smooth(prog(t, 7.4, 8.0))
    if gk > 0:
        glow(ctx, 1330, 1690, 150, "#FFC65C", 0.35 * gk * (0.8 + 0.2 * math.sin(t * 3)))
    # 地图钉 + 名片
    for (name, city, col, (px, py), (bx, by), tt) in PINS:
        k = pop(t, tt, 0.45)
        if k <= 0:
            continue
        drop = (1 - ease_out(prog(t, tt, tt + 0.35))) * -90
        # 引线
        lp = ease_out(prog(t, tt + 0.1, tt + 0.5))
        x1 = lerp(px, bx - 20, lp)
        y1 = lerp(py, by, lp)
        stroke_pts(ctx, [(px, py), ((px + x1) / 2 + 30, (py + y1) / 2), (x1, y1)], 3, col, 0.6 * a)
        # 钉
        with at(ctx, px, py + drop, k):
            circle(ctx, 0, -26, 16)
            fill(ctx, col, a)
            poly(ctx, [(-12, -18), (12, -18), (0, 4)])
            fill(ctx, col, a)
            circle(ctx, 0, -26, 6)
            fill(ctx, "#FFFFFF", a)
        # 名片
        with at(ctx, bx, by, k):
            w = text_w(ctx, name, 36, "black") + text_w(ctx, city, 24, "bold") + 112
            rrect(ctx, 0, -38, w, 76, 38)
            fill(ctx, "#FFFFFF", 0.96 * a)
            circle(ctx, 38, 0, 14)
            fill(ctx, col, a)
            text(ctx, name, 66, 0, 36, "#2B2233", a, "black", "l")
            text(ctx, city, w - 22, 2, 24, "#8A8296", a, "bold", "r")


def sfx():
    out = []
    for i, tt in enumerate(T_MS):
        out.append((tt - 0.55, "hop", {"gain": 0.3, "pitch": 1.0 + i * 0.06}))
        out.append((tt, "pop", {"gain": 0.5, "pitch": 0.9 + i * 0.12}))
    out += [(1.6, "tick", {"gain": 0.3, "pitch": 1.4}),
            (5.5, "surprise", {"gain": 0.3}),
            (5.75, "fall", {"dur": 1.3, "gain": 0.45}),
            (7.0, "thud", {"gain": 0.45}),
            (6.6, "swish", {"gain": 0.3})]
    for (name, city, col, p_, b_, tt) in PINS:
        out.append((tt, "pin", {"gain": 0.45}))
    out.append((8.9, "shimmer", {"dur": 1.4, "gain": 0.3}))
    out.append((0.0, "ambience_night", {"dur": 13.0, "gain": 0.3}))
    return out
