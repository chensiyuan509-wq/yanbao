"""05 · 孤岛与飞轮（上）：反观中国。DeepSeek 算法出色、用更少算力训练出一流模型；
可到了产品层面，各家智能体只在自家岛上畅通无阻，一跨出去就撞墙。"""
import math

from ..core import (TAU, Cam, at, circle, clamp, ease_back, ease_in, ease_io, ease_out, ease_out5, ellipse,
                    fill, glow, lerp, lin, line, pop, prog, rad, ring_burst, rng, rrect, setc, smooth,
                    sparkle_burst, star4, star5, stroke_pts, text, text_w, view, bezier_pts, point_on)
from ..charts import MapView, world_dots
from ..icons import ic_gpu
from ..props import app_tile, bg_grad, name_card, tag, whale
from .common import host, talk_lines

DUR = 24.5
CHAPTER = ("05", "孤岛与飞轮")

VO = [
    (1.2, '反观中国。'),
    (3.0, '{DeepSeek} 在算法上非常出色，用更少的算力训练出一流模型，让全世界刮目相看。'),
    (10.3, '可到了产品层面，问题就来了。'),
    (13.2, 'WorkBuddy、千问办公、钉钉、豆包手机……各家的智能体，大多只在{自家生态}里畅通无阻，'),
    (20.7, '一跨出去，就撞上了{围墙}。'),
]

SEA = 640                     # 海平面
ISLES = [  # (名字, 中心 x, 颜色, 应用们)
    ("腾讯生态", 500, "#1E9BF0", [("WorkBuddy", "#3E8BFF", "WB"), ("微信", "#07C160", "微"), ("QQ", "#12B7F5", "Q")]),
    ("阿里生态", 1180, "#FF6A00", [("千问办公", "#615CED", "千问"), ("钉钉", "#1677FF", "钉"), ("淘宝", "#FF5000", "淘")]),
    ("字节生态", 1860, "#1F1F2E", [("豆包手机", "#4D7CFE", "豆包"), ("抖音", "#161823", "抖"), ("飞书", "#3370FF", "飞")]),
]
OFF = 2200                    # 孤岛群在世界坐标里的偏移

P = (host(-560, 900, 0.6, "curious", seed=11.1)
     .look(0, 0.6, -0.8)
     .expr(3.2, "awe").look(3.2, 0.9, -0.6)
     .expr(6.6, "starry").hop(6.7, 40, 0.38)
     .expr(10.2, "worried").look(10.2, 0.7, -0.4)
     .move(11.6, 12.2, -560, 900).fade(11.6, 0.0, 0.3).place(12.3, OFF + 1520, SEA + 14)
     .fade(12.6, 1.0, 0.4).hop(12.6, 50, 0.4)
     .expr(13.2, "curious").look(13.2, 0.0, -0.8)
     .look(15.0, -0.8, -0.6).look(16.6, 0.0, -0.8).look(18.2, 0.8, -0.6)
     .look(20.4, -1.0, -0.4).expr(20.6, "shock").startle(20.9).expr(21.8, "worried").fx(21.8, ("sweat",)))
talk_lines(P, VO, [0, 2], smile=0.2)

MAPV = MapView(0, 420, 4.0, lon0=-170, lat0=30)

CAM = Cam([
    (0.0, (-500, 470, 1.0)),
    (2.6, (-180, 470, 1.0), ease_io),
    (3.1, (0, 520, 1.0), ease_io),
    (10.0, (20, 520, 1.03)),
    (12.4, (OFF + 1180, 500, 1.0), ease_io),
    (19.8, (OFF + 1180, 500, 1.02)),
    (20.5, (OFF + 1060, 500, 1.1), ease_io),
    (24.5, (OFF + 1040, 500, 1.13)),
], drift=6, seed=23.0)


def _bg(ctx, t, cam):
    dusk = smooth(prog(t, 0.0, 3.0))
    ctx.set_source(lin(0, 0, 0, 1080, [(0, "#1B2340"), (0.55, "#3A2F55"), (1, "#5C3B4E")]))
    ctx.paint()
    ctx.set_source(rad(960, 980, 0, 1100, [(0, "#FF9F68", 0.35 * dusk), (1, "#FF9F68", 0)]))
    ctx.paint()


def _map(ctx, t):
    a = 1 - smooth(prog(t, 2.6, 3.4))
    if a <= 0:
        return
    pan = ease_io(prog(t, 0.0, 2.6))
    MAPV.lon0 = lerp(-150.0, 105.0, pan)
    world_dots(ctx, MAPV, a, "#9FD8FF", 0.4, 3.0,
               hi={(104.0, 35.0, 16.0 * smooth(prog(t, 1.2, 2.2))): "#FFB27A"})
    q = smooth(prog(t, 1.2, 1.8))
    text(ctx, "反观中国", 0, 160, 72, "#FFFFFF", a * q, "black")


def _deepseek(ctx, t):
    a = smooth(prog(t, 2.9, 3.5)) * (1 - smooth(prog(t, 11.6, 12.4)))
    if a <= 0:
        return
    whale(ctx, 80, 420, 1.5, a, t)
    name_card(ctx, "DeepSeek", 80, 190, "#4D6BFE", 40, a, pop(t, 3.2, 0.5), sub="深度求索")
    badges = [("MoE 混合专家", -440, 300, 4.4), ("MLA 注意力压缩", 600, 300, 4.9), ("FP8 低精度训练", -440, 560, 5.4),
              ("强化学习推理", 600, 560, 5.9)]
    for lab, dx, dy, st in badges:
        q = pop(t, st, 0.45)
        if q > 0:
            with at(ctx, 80 + dx, dy, q):
                rrect(ctx, -150, -36, 300, 72, 36)
                fill(ctx, "#FFFFFF", 0.95 * a)
                text(ctx, lab, 0, 0, 28, "#2B3A8C", a, "black")
    # 更少的算力
    c = smooth(prog(t, 6.4, 6.9))
    if c > 0:
        rrect(ctx, -560, 700, 300, 34, 17)
        fill(ctx, "#2B2F45", a * c)
        rrect(ctx, -560, 700, 300 * 0.35, 34, 17)
        fill(ctx, "#7CFFB2", a * c)
        text(ctx, "算力", -600, 717, 26, "#FFFFFF", a * c, "bold", "r")
        tag(ctx, "更少的算力", -410, 770, 26, "#0E2A3A", "#7CFFB2", a * c)
        rrect(ctx, 400, 700, 300, 34, 17)
        fill(ctx, "#2B2F45", a * c)
        rrect(ctx, 400, 700, 300 * 0.92, 34, 17)
        fill(ctx, "#FFD36B", a * c)
        text(ctx, "效果", 360, 717, 26, "#FFFFFF", a * c, "bold", "r")
        tag(ctx, "一流的模型", 550, 770, 26, "#3A2A00", "#FFD36B", a * c)
    # 全世界刮目相看
    w = smooth(prog(t, 7.8, 8.3))
    if w > 0:
        R = rng(6)
        for i in range(14):
            ang = i / 14 * TAU
            x = 80 + math.cos(ang) * 760
            y = 430 + math.sin(ang) * 330
            k = pop(t, 7.8 + i * 0.05, 0.4)
            star5(ctx, x, y, 16 * k, "#FFD36B", 0.9 * a * w, t * 0.5 + i)
        tag(ctx, "全世界刮目相看", 80, 90, 30, "#2B2233", "#FFD36B", a * w)


def _isle(ctx, x, name, color, apps, t, a, idx):
    from ..props import castle
    # 岛
    rx = 250
    ctx.move_to(x - rx, SEA)
    ctx.curve_to(x - rx * 0.9, SEA + 120, x + rx * 0.9, SEA + 120, x + rx, SEA)
    ctx.close_path()
    fill(ctx, "#3B5E44", a)
    ellipse(ctx, x, SEA, rx, 46)
    ctx.set_source(lin(0, SEA - 46, 0, SEA + 46, [(0, "#7CC48A", a), (1, "#4E8A5E", a)]))
    ctx.fill()
    name_card(ctx, name, x, SEA + 140, color, 30, a, 1.0)
    # 岛上的应用 + 自家生态里畅通的路
    pos = [(x - 150, SEA - 120), (x + 5, SEA - 235), (x + 160, SEA - 110)]
    for i in range(3):
        for j in range(i + 1, 3):
            pts = bezier_pts(pos[i], (pos[i][0], pos[i][1] - 80), (pos[j][0], pos[j][1] - 80), pos[j], 24)
            stroke_pts(ctx, pts, 6, "#FFE29A", 0.75 * a)
            ph = (t * 0.6 + i * 0.3 + j * 0.2 + idx * 0.17) % 1
            (px, py), _ = point_on(pts, ph)
            glow(ctx, px, py, 20, "#FFE29A", 0.9 * a)
    for i, (nm, c, short) in enumerate(apps):
        k = pop(t, 13.4 + idx * 0.9 + i * 0.15, 0.45)
        if k > 0:
            app_tile(ctx, pos[i][0], pos[i][1], 96, c, short, a, k=k, text_size=40 if len(short) == 1 else 32)
            text(ctx, nm, pos[i][0], pos[i][1] + 70, 24, "#FFFFFF", a * k, "black")


def _islands(ctx, t):
    a = smooth(prog(t, 11.0, 12.0))
    if a <= 0:
        return
    # 海面
    ctx.save()
    ctx.translate(OFF, 0)
    ctx.rectangle(-1400, SEA, 5000, 900)
    ctx.set_source(lin(0, SEA, 0, SEA + 600, [(0, "#2C6E8E", a), (1, "#123448", a)]))
    ctx.fill()
    for k in range(5):
        y = SEA + 30 + k * 60
        ctx.move_to(-1400, y)
        for xx in range(-1400, 3700, 50):
            ctx.line_to(xx, y + math.sin(xx * 0.01 + t * (1.2 + k * 0.2) + k) * 6)
        ctx.set_line_width(3)
        setc(ctx, "#9FD8FF", 0.15 * a)
        ctx.stroke()
    for idx, (nm, x, c, apps) in enumerate(ISLES):
        q = smooth(prog(t, 11.3 + idx * 0.25, 12.1 + idx * 0.25))
        ctx.save()
        ctx.translate(0, (1 - ease_out(q)) * 200)
        _isle(ctx, x, nm, c, apps, t, a * q, idx)
        ctx.restore()
    # 自家生态标签
    tg = smooth(prog(t, 18.0, 18.4))
    if tg > 0:
        tag(ctx, "自家生态里，畅通无阻", 1180, 120, 34, "#2B2233", "#FFE29A", a * tg)
    # 智能体想去隔壁岛：撞墙
    # Claude 脚下的礁石
    ellipse(ctx, 1520, SEA + 22, 120, 30)
    fill(ctx, "#5A6B78", a)
    ellipse(ctx, 1520, SEA + 14, 110, 22)
    fill(ctx, "#7D909E", a)
    b = prog(t, 20.4, 21.2)
    if b > 0:
        wx = 840
        wall = ease_back(clamp((t - 20.6) / 0.4), 1.5)
        rrect(ctx, wx - 16, SEA - 380 * wall, 32, 380 * wall, 8)
        ctx.set_source(lin(0, SEA - 380, 0, SEA, [(0, "#C9B79C", a), (1, "#8C7A60", a)]))
        ctx.fill()
        for k in range(6):
            line(ctx, wx - 16, SEA - 60 * k * wall, wx + 16, SEA - 60 * k * wall, 2, "#6E5E48", a * wall)
        u = clamp((t - 20.4) / 0.5)
        back = clamp((t - 20.9) / 0.6)
        ax = lerp(600, wx - 70, ease_in(u)) - 90 * ease_out(back)
        ay = SEA - 250 - math.sin(u * math.pi) * 40
        with at(ctx, ax, ay, 1.0, -0.4 * ease_out(back)):
            app_tile(ctx, 0, 0, 90, "#3E8BFF", "智能体", a, text_size=22)
        if t > 20.9:
            ring_burst(ctx, t, 20.9, wx - 30, ay, 10, 120, "#FFFFFF", 0.5, 6)
            for i in range(4):
                ang = t * 4 + i * TAU / 4
                star5(ctx, ax + math.cos(ang) * 60, ay - 70 + math.sin(ang) * 16, 12, "#FFD54A",
                      a * (1 - smooth(prog(t, 23.0, 23.6))), ang)
        tag(ctx, "围墙", wx, SEA - 420, 34, "#FFFFFF", "#C42A30", a * smooth(prog(t, 21.0, 21.4)))
    ctx.restore()


def draw(ctx, t):
    cam = CAM.at(t)
    _bg(ctx, t, cam)
    with view(ctx, cam, 1.0):
        _map(ctx, t)
        _deepseek(ctx, t)
        _islands(ctx, t)
        P.draw(ctx, t)


def sfx():
    return [
        (0.0, "swell", {"dur": 2.0, "gain": 0.3}),
        (0.2, "whoosh", {"dur": 2.4, "gain": 0.3}),
        (3.0, "water", {"gain": 0.35}),
        (4.4, "pop", {"gain": 0.3}), (4.9, "pop", {"gain": 0.3, "pitch": 1.15}),
        (5.4, "pop", {"gain": 0.3, "pitch": 1.3}), (5.9, "pop", {"gain": 0.3, "pitch": 1.45}),
        (6.4, "rise", {"dur": 0.9, "gain": 0.25}),
        (7.8, "sparkle", {"dur": 1.4, "gain": 0.3}),
        (10.3, "womp", {"gain": 0.3}),
        (11.8, "whoosh", {"dur": 1.0, "gain": 0.3}),
        (12.0, "ambience_sea", {"dur": 12.5, "gain": 0.35}),
        (13.4, "pop", {"gain": 0.25}), (14.3, "pop", {"gain": 0.25, "pitch": 1.2}),
        (15.2, "pop", {"gain": 0.25, "pitch": 1.4}),
        (14.0, "stream", {"dur": 4.0, "gain": 0.12}),
        (20.6, "rumble", {"dur": 0.6, "gain": 0.35}),
        (20.9, "knock", {"gain": 0.5}), (21.0, "boing", {"gain": 0.3, "pitch": 0.8}),
    ]
