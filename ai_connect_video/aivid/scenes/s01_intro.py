"""开场：深夜浮岛上熟睡的小橙被 AI 新闻推送吵醒 → 弹幕刷屏 → 星星连成网络 → 片名。"""
import math

from ..core import (TAU, W, H, Cam, at, circle, clamp, ease_back, ease_in, ease_io, ease_out,
                    ease_out5, glow, kf, lerp, lin, pop, prog, rng, setc, smooth, star4, stars,
                    bokeh, text, text_reveal, text_w, view, sparkle_burst, ring_burst, fill, rrect,
                    font, line)
from ..icons import (ic_chatgpt, ic_claude_code, ic_codex, ic_muse, ic_openclaw, ic_workbuddy)
from ..mascot import Puppet
from .common import danmaku, floating_island, night_sky, notif

DUR = 17.0
CHAPTER = None

SUBS = [
    (3.3, 5.9, "嗨，我是{小橙}。"),
    (6.1, 10.2, "最近，「{大模型}」「{智能体}」天天刷屏。"),
    (10.4, 14.4, "它们到底是什么？AI 为什么偏偏在{美国}先爆发？"),
]

MX, MY = 960, 712

P = (Puppet(MX, MY, 0.75, "sleep", seed=1.3)
     .shake(1.9, 0.35, 0.03)
     .expr(2.6, "surprised").hop(2.6, 70, 0.45).fx(2.6, ("exclaim",)).fx(3.3, None)
     .expr(3.35, "happy").wave(3.4, 5.6, "r").talk(3.45, 4.4)
     .expr(6.0, "curious").look(6.0, -0.9, -0.4).tilt(6.0, -0.06)
     .look(7.4, 0.9, -0.5).tilt(7.4, 0.06)
     .look(8.8, 0.0, -1.0).tilt(8.8, 0.0)
     .expr(10.4, "think").bar(10.4, "think").fx(10.4, ("question2",)).look(10.4, 0.6, -0.6)
     .bar(13.2, None).fx(13.2, None)
     .expr(13.25, "excited").hop(13.3, 60, 0.42).look(13.25, 0.0, -0.3)
     .expr(14.3, "determined").fx(14.3, ("sparkle",)).bar(14.3, "fists")
     .look(14.3, 0.0, 0.0))

NOTIFS = [
    (0.9, ic_chatgpt, "ChatGPT", "每周约 9 亿人在用", (520, 340)),
    (1.4, ic_openclaw, "OpenClaw", "GitHub 星标突破 10 万", (1410, 310)),
    (1.9, ic_muse, "Meta Muse", "个人智能体正式发布", (500, 570)),
    (2.3, ic_workbuddy, "WorkBuddy", "腾讯办公智能体上线", (1430, 550)),
    (2.75, ic_claude_code, "Claude Code", "AI 编程智能体火出圈", (960, 215)),
    (6.4, ic_codex, "Codex", "一句话，交给 AI 写代码", (1400, 760)),
]

DANMAKU = [
    (6.3, "大模型到底是啥？", 0), (6.7, "Agent 又是什么？", 2), (7.0, "又出新模型了！", 4),
    (7.4, "智能体来了", 1), (7.9, "AI 会替我上班吗", 3), (8.3, "MCP 是什么？", 0),
    (8.7, "token 是啥", 2), (9.1, "算力！算力！", 4), (9.5, "OpenClaw 好火", 1),
    (9.9, "求科普", 3), (10.3, "为什么都在美国？", 0),
]

# 片头星座网络节点（世界坐标）
_R = rng(11)
NET = [(_R.uniform(140, 1780), _R.uniform(90, 470)) for _ in range(16)]
EDGES = []
for i, a in enumerate(NET):
    d = sorted(range(len(NET)), key=lambda j: (NET[j][0] - a[0]) ** 2 + (NET[j][1] - a[1]) ** 2)
    for j in d[1:3]:
        if (j, i) not in EDGES:
            EDGES.append((i, j))

CAM = Cam([
    (0.0, (960, 622, 1.62)),
    (2.4, (960, 630, 1.56)),
    (4.2, (960, 575, 1.12), ease_io),
    (10.0, (960, 548, 1.0)),
    (13.0, (960, 515, 0.84), ease_io),
    (17.0, (960, 512, 0.9, 0.012)),
], drift=7, seed=2.0)


def draw(ctx, t):
    warm = smooth(prog(t, 11.5, 15.5))
    night_sky(ctx, t, warm=0.6 * warm)
    cam = CAM.at(t)

    # 远景：星星（视差 0.3）
    with view(ctx, cam, 0.3):
        stars(ctx, t, 140, 5, area=(-300, -300, W + 600, H * 0.8 + 300), a=0.85)
        bokeh(ctx, t, 16, 9, ("#FF9F68", "#8B6CFF", "#4C8DFF"), area=(-200, 0, W + 400, H), r=(30, 90),
              a=(0.05, 0.12), speed=(3, 8))

    # 中景：星座网络（12.4s 起逐条连线）
    with view(ctx, cam, 0.55):
        for k, (i, j) in enumerate(EDGES):
            st = 12.2 + k * 0.07
            q = ease_out(prog(t, st, st + 0.6))
            if q > 0:
                (x0, y0), (x1, y1) = NET[i], NET[j]
                line(ctx, x0, y0, lerp(x0, x1, q), lerp(y0, y1, q), 2.5, "#FFD9B8", 0.5 * q)
        for k, (x, y) in enumerate(NET):
            st = 12.0 + k * 0.08
            q = pop(t, st, 0.4)
            if q > 0:
                glow(ctx, x, y, 34 * q, "#FFC58A", 0.6)
                circle(ctx, x, y, 5 * q)
                fill(ctx, "#FFF3E0")

    with view(ctx, cam, 1.0):
        # 浮岛 + 光晕
        glow(ctx, MX, MY + 30, 520, "#FF9F68", 0.18 + 0.12 * warm)
        floating_island(ctx, MX, MY + 4, 330, t, seed=0.5)
        P.draw(ctx, t)

    with view(ctx, cam, 0.45):
        # 推送通知（中景层，镜头推拉时变化较小，不会被裁出画面）
        for (t0, icon, app, msg, (x, y)) in NOTIFS:
            out = ease_in(prog(t, 10.35 + (x - 960) / 4000, 11.0 + (x - 960) / 4000))
            k = pop(t, t0, 0.5)
            if k <= 0 or out >= 1:
                continue
            fy = math.sin(t * 1.3 + x * 0.01) * 6
            dx = (x - MX) * out * 1.6
            dy = (y - 600) * out * 1.6 - 60 * (1 - ease_out(prog(t, t0, t0 + 0.4)))
            dim = 1 - 0.5 * smooth(prog(t, 6.1, 6.7))      # 弹幕出现时卡片退后变淡
            notif(ctx, x + dx, y + fy + dy, icon, app, msg, a=(1 - out) * dim,
                  k=k * (1 - 0.3 * out) * (1 - 0.07 * (1 - dim) / 0.5), t=t)
            sparkle_burst(ctx, t, t0, x - 190, y, n=6, radius=70, color="#FFE7A3", dur=0.6, seed=int(t0 * 10))

    # 弹幕（近乎屏幕空间，画在卡片之上）
    with view(ctx, cam, 0.12):
        fade = 1 - smooth(prog(t, 10.6, 11.4))
        danmaku(ctx, t, DANMAKU, y0=78, rows=5, row_h=52, speed=320, a=fade, size=31,
                colors=("#FFFFFF", "#FFE3B3", "#CFE3FF"))

    with view(ctx, cam, 1.0):
        # 名字牌
        nk = pop(t, 3.55, 0.45) * (1 - smooth(prog(t, 5.8, 6.2)))
        if nk > 0:
            hx, hy = P.head(t)
            with at(ctx, hx, hy - 62, nk, -0.04):
                rrect(ctx, -70, -30, 140, 60, 30)
                setc(ctx, "#FFFFFF", 0.95)
                ctx.fill()
                text(ctx, "小橙", 0, 0, 32, "#E07A4F", 1, "black")

    # 片名（屏幕空间）
    draw_title(ctx, t)


def draw_title(ctx, t):
    p = prog(t, 13.5, 15.0)
    if p <= 0:
        return
    cx, cy = 960, 250
    glow(ctx, cx, cy, 520, "#FF9F68", 0.22 * smooth(p))
    # 主标题：渐变填充的逐字弹出
    s = "连接的力量"
    size = 138
    font(ctx, size, "black")
    adv = [ctx.text_extents(ch).x_advance + 10 for ch in s]
    tw = sum(adv) - 10
    x = cx - tw / 2
    for i, ch in enumerate(s):
        q = prog(t, 13.5 + i * 0.09, 13.5 + i * 0.09 + 0.55)
        if q <= 0:
            x += adv[i]
            continue
        k = ease_back(q, 2.0)
        ctx.save()
        ctx.translate(x + adv[i] / 2 - 5, cy + (1 - ease_out(q)) * 40)
        ctx.scale(k, k)
        font(ctx, size, "black")
        ext = ctx.text_extents(ch)
        ctx.move_to(-ext.x_advance / 2 + 3, size * 0.36 + 5)
        ctx.text_path(ch)
        setc(ctx, "#1A0F2E", 0.35 * min(1, q * 2))
        ctx.fill()
        ctx.move_to(-ext.x_advance / 2, size * 0.36)
        ctx.text_path(ch)
        ctx.set_source(lin(0, -size * 0.5, 0, size * 0.5,
                           [(0, "#FFF4E6", min(1, q * 2)), (1, "#FFC08A", min(1, q * 2))]))
        ctx.fill()
        ctx.restore()
        x += adv[i]
    # 扫光
    sp = prog(t, 15.3, 16.2)
    if 0 < sp < 1:
        ctx.save()
        font(ctx, size, "black")
        x = cx - tw / 2
        for i, ch in enumerate(s):
            ctx.move_to(x, cy + size * 0.36)
            ctx.text_path(ch)
            x += adv[i]
        ctx.clip()
        sx = lerp(cx - tw / 2 - 200, cx + tw / 2 + 200, ease_io(sp))
        ctx.set_source(lin(sx - 90, 0, sx + 90, 0, [(0, "#FFFFFF", 0), (0.5, "#FFFFFF", 0.85), (1, "#FFFFFF", 0)]))
        ctx.paint()
        ctx.restore()
    # 下划线 + 副标题
    lp = ease_out5(prog(t, 14.2, 15.0))
    if lp > 0:
        rrect(ctx, cx - 260 * lp, cy + 104, 520 * lp, 6, 3)
        setc(ctx, "#FF9F68", 0.9)
        ctx.fill()
    text_reveal(ctx, "AI 为什么先在美国爆发？", cx, cy + 160, 50, "#FFE3C8",
                prog(t, 14.4, 15.4), weight="bold")
    tp = smooth(prog(t, 15.0, 15.8))
    if tp > 0:
        text(ctx, "大模型  ·  智能体  ·  开放互联", cx, cy + 228, 30, "#CDBFE6", tp, "medium", spacing=0.08)


def sfx():
    out = [(0.0, "ambience_night", {"dur": 17.5, "gain": 0.5})]
    for i, (t0, *_rest) in enumerate(NOTIFS):
        out.append((t0, "notify", {"pitch": [1.0, 1.12, 0.94, 1.19, 1.06, 1.0][i], "gain": 0.55}))
    out += [
        (1.9, "snore_twitch", {"gain": 0.35}),
        (2.45, "surprise", {"gain": 0.6}),
        (2.62, "boing", {"gain": 0.45}),
        (3.4, "pop", {"gain": 0.35, "pitch": 1.3}),
        (3.55, "pop", {"gain": 0.4, "pitch": 1.5}),
    ]
    for (ts, s, row) in DANMAKU:
        out.append((ts, "tick", {"gain": 0.18, "pitch": 1.0 + (row % 3) * 0.15}))
    out += [
        (10.3, "whoosh", {"dur": 0.9, "gain": 0.55}),
        (10.45, "bubble", {"gain": 0.4}),
        (11.95, "sparkle", {"dur": 2.2, "gain": 0.35}),
        (13.25, "boing", {"gain": 0.4}),
        (13.5, "impact_soft", {"gain": 0.6}),
        (13.55, "shimmer", {"dur": 1.6, "gain": 0.4}),
        (15.3, "swish_hi", {"gain": 0.35}),
    ]
    return out
