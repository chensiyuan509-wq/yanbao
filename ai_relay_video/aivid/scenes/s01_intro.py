"""片头：三座浮岛（写代码 → 办公 → 生活），镜头钻进手机里的世界地图，美国亮起；最后出片名《AI 接力赛》。"""
import math

from ..core import (TAU, Cam, at, bokeh, circle, clamp, ease_in, ease_io, ease_out, ease_out5, fill,
                    font, glow, kf, lerp, lin, pop, prog, rad, ring_burst, rrect, setc, smooth,
                    sparkle_burst, star4, stars, text, text_reveal, view)
from ..charts import MapView, world_dots
from ..icons import ic_calendar, ic_plane
from ..props import code_panel, doc_card, iphone, tag
from mascot import draw_prop
from .common import host, mini_icon, talk_lines

DUR = 31.0
CHAPTER = None

VO = [
    (1.0, '这两年，AI 先学会了{写代码}，'),
    (4.0, '接着走进办公室，替我们写周报、做表格、回邮件；'),
    (8.6, '现在，它还想帮你订机票、管日程，打理{生活}。'),
    (13.4, 'AI 是怎么一步步走到今天的？'),
    (15.9, '为什么偏偏在{美国}先引爆？'),
    (18.1, '它又会怎样改变我们的{工作和生活}？'),
    (21.2, '走，我带你逛一逛 AI 世界。'),
]

IA, IB, IC = (960, 760), (2900, 760), (4840, 760)       # 三座浮岛顶面中心
PHONE = (IC[0] + 320, 490)                               # 生活岛上的大手机
PH_H = 600
SCR = None                                               # 手机屏幕区域（绘制时更新）

P = (host(IA[0] - 240, IA[1], 0.62, "awe", seed=1.1, hat=None)
     .look(0, 0.9, -0.5)
     .expr(1.0, "excited").point(1.3, "r", 0.5, 70).look(1.3, 1.0, -0.6)
     .arms_down(3.0)
     # 跳到办公岛
     .expr(3.55, "determined").move(3.6, 4.75, IB[0] - 260, IB[1], ease_io).hop(3.6, 300, 1.15)
     .land(4.75, 0.2).expr(4.8, "happy").look(4.8, 0.8, -0.6)
     .wave(6.2, 7.3, "r")
     # 跳到生活岛
     .expr(8.1, "determined").move(8.15, 9.3, IC[0] - 300, IC[1], ease_io).hop(8.15, 300, 1.15)
     .land(9.3, 0.2).expr(9.35, "smile").look(9.35, 1.0, -0.5)
     .point(9.8, "r", 0.55, 60).arms_down(12.0)
     # 提问
     .expr(13.3, "think").fx(13.3, ("question2",)).look(13.3, 0.4, -0.8)
     .expr(15.2, "curious").fx(15.2, ()).look(15.2, 1.0, -0.7)
     .expr(18.0, "hmm").fx(18.0, ()).look(18.2, -0.6, -0.6).look(19.2, 0.6, -0.6).look(20.1, 0.0, -0.3)
     # 出发！
     .expr(20.9, "fired_up").fx(20.9, ()).hat(21.05, "explorer").hop(21.0, 50, 0.4)
     .walk_to(21.7, 22.9, IC[0] - 120, IC[1]).wave(22.9, 23.5, "r").look(22.9, 0.0, 0.1)
     .expr(23.5, "grin").hold(23.6, ("baton",), "r", -0.5).arm(23.6, "r", 1.25, 0.35).fx(24.2, ("sparkles",))
     .bounce(25.0, 30.5, 0.035, 1.6))
talk_lines(P, VO, [0, 1, 2, 3, 5, 6], smile=0.35)

CAM = Cam([
    (0.0, (IA[0] + 40, 600, 1.16)),
    (3.3, (IA[0] + 40, 590, 1.02)),
    (4.7, (IB[0], 590, 1.0), ease_io),
    (8.0, (IB[0] + 20, 590, 1.0)),
    (9.3, (IC[0] + 40, 590, 1.0), ease_io),
    (12.9, (IC[0] + 60, 585, 1.04)),
    (14.6, (IC[0] + 120, 575, 0.92), ease_io),
    (15.25, (PHONE[0], PHONE[1] + 20, 1.0), ease_in),
    (16.25, (PHONE[0], PHONE[1] + 20, 8.6), ease_io),
    (17.65, (PHONE[0], PHONE[1] + 20, 8.9)),
    (18.55, (IC[0] + 80, 590, 0.98), ease_io),
    (20.8, (IC[0] + 40, 600, 1.05)),
    (23.2, (IC[0] - 120, 470, 1.1), ease_io),
    (31.0, (IC[0] - 120, 462, 1.15)),
], drift=6, seed=3.0)

US = (-100.0, 38.0)


def _island(ctx, x, y, rx, t, seed, glow_c="#FFB27A"):
    ry = rx * 0.15
    y += math.sin(t * 1.1 + seed) * 4
    ctx.move_to(x - rx, y)
    ctx.curve_to(x - rx * 0.9, y + rx * 0.35, x - rx * 0.35, y + rx * 0.62, x, y + rx * 0.8)
    ctx.curve_to(x + rx * 0.35, y + rx * 0.62, x + rx * 0.9, y + rx * 0.35, x + rx, y)
    ctx.close_path()
    ctx.set_source(lin(0, y, 0, y + rx * 0.8, [(0, "#5A4B86"), (1, "#1E1838")]))
    ctx.fill()
    from ..core import ellipse
    ellipse(ctx, x, y, rx, ry)
    ctx.set_source(lin(0, y - ry, 0, y + ry, [(0, "#8A7CC0"), (1, "#5E5196")]))
    ctx.fill()
    ellipse(ctx, x, y - 2, rx * 0.98, ry * 0.88)
    ctx.set_line_width(3)
    setc(ctx, glow_c, 0.45)
    ctx.stroke()
    glow(ctx, x, y + rx * 0.4, rx * 0.9, glow_c, 0.08)


def _bg(ctx, t, cam):
    warm = smooth(prog(t, 20.5, 25.0))
    ctx.set_source(lin(0, 0, 0, 1080, [(0, "#141A3A"), (0.6, "#2A2357"), (1, "#4A2F5E")]))
    ctx.paint()
    if warm > 0:
        ctx.set_source(rad(960, 1180, 0, 1100, [(0, "#FFB27A", 0.65 * warm), (0.5, "#FF7A9A", 0.22 * warm),
                                                (1, "#FF7A9A", 0)]))
        ctx.paint()
    with view(ctx, cam, 0.25):
        stars(ctx, t, 150, 4, area=(-600, -400, 6400, 1300), a=0.75)
    with view(ctx, cam, 0.45):
        bokeh(ctx, t, 26, 8, ("#FF9F68", "#8B6CFF", "#4C8DFF"), area=(-400, 0, 6200, 1080), r=(30, 100),
              a=(0.04, 0.11), speed=(3, 8))


def _station_code(ctx, t):
    x, y = IA[0] + 120, IA[1]
    # 显示器 + 支架
    rrect(ctx, x - 14, y - 150, 28, 150, 6)
    fill(ctx, "#3A3646")
    lines = [
        ("def ship_feature(spec):", "#7CC6FF", 0.2),
        ("    plan = agent.plan(spec)", "#FFFFFF", 0.9),
        ("    for step in plan:", "#FFC857", 1.6),
        ("        code = agent.write(step)", "#FFFFFF", 2.2),
        ("        assert tests.pass(code)", "#7CFFB2", 2.9),
        ("    return pr.open()   # 完成！", "#FF9F68", 3.5),
    ]
    cx, cy, cw, ch = code_panel(ctx, x - 300, y - 520, 600, 370, lines, t, 1.0, cps=34, title="ai_agent.py",
                                size=24, lh=46)
    # AI 光标的小星星
    k = clamp((t - 0.3) / 0.3)
    if k > 0 and t < 4.5:
        row = min(5, int(max(0, t - 0.2) / 0.62))
        star4(ctx, cx + cw - 50, cy + 30 + row * 46, 16 + 5 * math.sin(t * 9), "#FFE7A3", k, t * 2)
    tag(ctx, "写代码", x, y - 575, 30, "#FFFFFF", "#FF9F68", 1.0, 1.0)


def _station_office(ctx, t):
    x, y = IB[0] + 110, IB[1]
    cards = [("doc", "周报", -250, -330, 4.5), ("sheet", "表格", 30, -420, 5.3), ("mail", "邮件", 300, -300, 6.1)]
    for i, (kind, title, dx, dy, t0) in enumerate(cards):
        k = pop(t, t0 - 0.55, 0.5)
        if k <= 0:
            continue
        p = clamp((t - t0 + 0.3) / 1.4)
        fy = math.sin(t * 1.3 + i * 2) * 8
        with at(ctx, x + dx, y + dy + fy, k, (i - 1) * 0.05):
            doc_card(ctx, 0, 0, 250, 300, kind, 1.0, p, title)
            if p >= 1:
                q = pop(t, t0 + 1.1, 0.4)
                circle(ctx, 105, -130, 26 * q)
                fill(ctx, "#3CCB7F")
                from ..core import check_mark
                check_mark(ctx, 105, -130, 30 * q, "#FFFFFF", clamp((t - t0 - 1.1) / 0.3))
    tag(ctx, "办公", x, y - 600, 30, "#FFFFFF", "#4C8DFF", 1.0, 1.0)


def _phone_screen(ctx, t, sx, sy, sw, sh):
    """手机屏幕内容：先是订票 / 日程卡片，然后切到世界地图。"""
    mp = smooth(prog(t, 14.9, 15.5))
    if mp < 1:
        ctx.save()
        rrect(ctx, sx, sy, sw, sh, 18)
        ctx.clip()
        ctx.set_source(lin(0, sy, 0, sy + sh, [(0, "#F7F5FA"), (1, "#ECE7F5")]))
        ctx.paint()
        text(ctx, "AI 助理", sx + sw / 2, sy + 30, 22, "#6B6377", 1, "black")
        items = [("上海 → 东京", "机票已订好 · 周五 09:20", 9.6, "#4C8DFF", "plane"),
                 ("周一 10:00", "日程：项目复盘会", 10.4, "#8B6CFF", "cal"),
                 ("比价完成", "帮你省了 128 元", 11.2, "#FF9F68", "bag")]
        for i, (a, b, t0, c, ic) in enumerate(items):
            k = pop(t, t0, 0.45)
            if k <= 0:
                continue
            with at(ctx, sx + sw / 2, sy + 110 + i * 110, k):
                rrect(ctx, -sw / 2 + 16, -44, sw - 32, 88, 16)
                fill(ctx, "#FFFFFF")
                rrect(ctx, -sw / 2 + 16, -44, 10, 88, 5)
                fill(ctx, c)
                mini_icon(ctx, ic, -sw / 2 + 62, 0, 44, c)
                text(ctx, a, -sw / 2 + 96, -14, 22, "#2B2233", 1, "black", "l")
                text(ctx, b, -sw / 2 + 96, 18, 17, "#7A7186", 1, "bold", "l")
        ctx.restore()
    if mp > 0:
        ctx.save()
        rrect(ctx, sx, sy, sw, sh, 18)
        ctx.clip()
        ctx.set_source(lin(0, sy, 0, sy + sh, [(0, "#0E1530", mp), (1, "#1A1440", mp)]))
        ctx.paint()
        cxm, cym = PHONE[0], PHONE[1] + 20
        v = MapView(cxm, cym, sw / 360 * 1.05, lon0=-28, lat0=18)
        us = smooth(prog(t, 15.95, 16.6))
        world_dots(ctx, v, mp, "#9FD8FF", 0.5, 4.0, hi={(US[0], US[1], 26): "#FF9F68"} if us > 0 else None)
        if us > 0:
            ux, uy = v.xy(*US)
            glow(ctx, ux, uy, 60 * us, "#FFB27A", 0.8 * us)
            ring_burst(ctx, t, 16.0, ux, uy, 2, 34, "#FFD9B8", 0.9, 1.6)
            ring_burst(ctx, t, 16.4, ux, uy, 2, 34, "#FFD9B8", 0.9, 1.6)
            sparkle_burst(ctx, t, 16.05, ux, uy, 8, 22, "#FFE7A3", 0.9, 4, 4)
            text(ctx, "USA", ux, uy - 9, 4.2, "#FFFFFF", us, "black")
        text(ctx, "AI 世界地图", cxm, sy + 26, 20, "#FFFFFF", mp * (1 - smooth(prog(t, 15.4, 15.8))), "black")
        ctx.restore()


def _station_life(ctx, t):
    gone = smooth(prog(t, 22.3, 23.3))          # 出片名前清场：手机沉入岛里，图标飞走
    if gone >= 1:
        return
    px, py = PHONE
    if gone > 0:
        ctx.push_group()
    ctx.save()
    ctx.translate(0, 160 * ease_in(gone))
    sx, sy, sw, sh = iphone(ctx, px, py, PH_H, 1.0)
    _phone_screen(ctx, t, sx, sy, sw, sh)
    ctx.restore()
    k = pop(t, 10.0, 0.5)
    if k > 0:
        fy = math.sin(t * 1.6) * 8 - 200 * ease_in(gone)
        ic_calendar(ctx, px - 290, py - 230 + fy, 110 * k, 1.0, t, "15")
        ic_plane(ctx, px + 270, py - 260 - fy, 130 * k, 1.0, t, "#4C8DFF", -0.35)
    tag(ctx, "生活", px, py - PH_H / 2 - 50, 30, "#FFFFFF", "#3CCB7F", 1.0, 1.0)
    if gone > 0:
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(1 - gone)


def _questions(ctx, t):
    """"工作和生活会怎样？"：三个小图标绕着 Claude。"""
    a = smooth(prog(t, 18.2, 18.7)) * (1 - smooth(prog(t, 20.8, 21.3)))
    if a <= 0:
        return
    hx, hy = P.head(t)
    icons = [("laptop", -170, -60, 18.3), ("case", 0, -150, 18.6), ("house", 170, -60, 18.9)]
    for (s, dx, dy, t0) in icons:
        k = pop(t, t0, 0.45)
        if k <= 0:
            continue
        bob = math.sin(t * 3 + dx) * 6
        with at(ctx, hx + dx, hy + dy + bob, k * a):
            circle(ctx, 0, 0, 52)
            fill(ctx, "#FFFFFF", 0.95)
            mini_icon(ctx, s, 0, 2, 58, "#FF9F68")
            text(ctx, "?", 40, -40, 36, "#FF9F68", 1, "black", outline="#FFFFFF", outline_w=6)


def _title(ctx, t):
    p = prog(t, 23.8, 25.2)
    if p <= 0:
        return
    cx, cy = 960, 250
    # 底板光晕
    glow(ctx, cx, cy + 20, 640, "#FF9F68", 0.28 * smooth(p))
    s = "AI 接力赛"
    size = 150
    font(ctx, size, "black")
    adv = [ctx.text_extents(ch).x_advance + 8 for ch in s]
    tw = sum(adv) - 8
    x = cx - tw / 2
    for i, ch in enumerate(s):
        q = prog(t, 23.8 + i * 0.08, 23.8 + i * 0.08 + 0.55)
        if q > 0 and ch.strip():
            k = ease_out5(q) if i < 2 else min(1.25, 0.2 + q * 1.4) if q < 0.7 else 1 + 0.25 * (1 - (q - 0.7) / 0.3)
            ctx.save()
            ctx.translate(x + adv[i] / 2 - 4, cy + (1 - ease_out(q)) * 50)
            ctx.scale(k, k)
            font(ctx, size, "black")
            ext = ctx.text_extents(ch)
            ctx.move_to(-ext.x_advance / 2 + 4, size * 0.36 + 6)
            ctx.text_path(ch)
            setc(ctx, "#1A0F2E", 0.35 * min(1, q * 2))
            ctx.fill()
            ctx.move_to(-ext.x_advance / 2, size * 0.36)
            ctx.text_path(ch)
            ctx.set_source(lin(0, -size * 0.5, 0, size * 0.5,
                               [(0, "#FFF4E6", min(1, q * 2)), (1, "#FFB27A", min(1, q * 2))]))
            ctx.fill()
            ctx.restore()
        x += adv[i]
    # 接力棒划过的光轨
    sp = prog(t, 24.6, 25.6)
    if sp > 0:
        y = cy + 104
        x0, x1 = cx - 330, cx + 330
        xe = lerp(x0, x1, ease_io(sp))
        ctx.set_source(lin(x0, 0, xe, 0, [(0, "#FFD36B", 0), (1, "#FFD36B", 0.9)]))
        rrect(ctx, x0, y - 5, xe - x0, 10, 5)
        ctx.fill()
        if sp < 1:
            with at(ctx, xe, y, 0.6, -0.15):
                draw_prop(ctx, ("baton",), t)
    text_reveal(ctx, "从一篇论文，到你的工作和生活", cx, cy + 168, 48, "#FFE3C8", prog(t, 25.3, 26.4))
    tp = smooth(prog(t, 26.2, 27.0))
    if tp > 0:
        text(ctx, "Transformer · 算力 · 智能体 · 竞合 · 孤岛 · 未来", cx, cy + 230, 28, "#CDBFE6", tp,
             "medium", spacing=0.06)


def draw(ctx, t):
    cam = CAM.at(t)
    _bg(ctx, t, cam)
    with view(ctx, cam, 1.0):
        for (ix, iy), rx, sd in ((IA, 420, 0.3), (IB, 470, 1.4), (IC, 520, 2.2)):
            _island(ctx, ix, iy + 4, rx, t, sd)
        _station_code(ctx, t)
        _station_office(ctx, t)
        _station_life(ctx, t)
        P.draw(ctx, t)
        _questions(ctx, t)
        # 跳跃时的光尘
        for t0, (x0, x1) in ((3.6, (IA[0] - 240, IB[0] - 260)), (8.15, (IB[0] - 260, IC[0] - 300))):
            u = (t - t0) / 1.15
            if 0 < u < 1:
                for k in range(6):
                    v = max(0, u - k * 0.05)
                    px = lerp(x0, x1, ease_io(v))
                    py = IA[1] - 150 - math.sin(v * math.pi) * 300
                    glow(ctx, px, py, 26 - k * 3, "#FFE7A3", 0.35 * (1 - k / 6))
    # 片名期间背景压暗一点，字更清楚
    d = smooth(prog(t, 23.4, 24.4))
    if d > 0:
        ctx.set_source(lin(0, 0, 0, 1080, [(0, "#0E0A1E", 0.55 * d), (0.55, "#0E0A1E", 0.15 * d),
                                           (1, "#0E0A1E", 0.0)]))
        ctx.paint()
    _title(ctx, t)
    # 开场淡入
    if t < 0.8:
        ctx.set_source_rgba(0, 0, 0, 1 - smooth(t / 0.8))
        ctx.paint()


def sfx():
    return [
        (0.0, "ambience_night", {"dur": 16.0, "gain": 0.35}),
        (0.25, "typing", {"dur": 3.4, "gain": 0.28}),
        (1.3, "sparkle", {"dur": 1.2, "gain": 0.25}),
        (3.6, "boing", {"gain": 0.4}),
        (3.65, "whoosh", {"dur": 1.0, "gain": 0.35}),
        (4.75, "thud", {"gain": 0.3}),
        (5.55, "check", {"gain": 0.32}), (6.35, "check", {"gain": 0.32, "pitch": 1.12}),
        (7.15, "check", {"gain": 0.32, "pitch": 1.25}),
        (8.15, "boing", {"gain": 0.4, "pitch": 1.1}),
        (8.2, "whoosh", {"dur": 1.0, "gain": 0.35}),
        (9.3, "thud", {"gain": 0.3}),
        (9.6, "notify", {"gain": 0.32}), (10.4, "notify", {"gain": 0.3, "pitch": 1.12}),
        (11.2, "coin", {"gain": 0.3}),
        (13.4, "think", {"dur": 1.8, "gain": 0.3}),
        (15.2, "zoom_in", {"dur": 1.2, "gain": 0.4}),
        (16.0, "impact_soft", {"gain": 0.45}),
        (16.05, "sparkle", {"dur": 1.2, "gain": 0.3}),
        (17.65, "whoosh", {"dur": 0.9, "gain": 0.35}),
        (18.3, "pop", {"gain": 0.3, "pitch": 1.2}), (18.6, "pop", {"gain": 0.3, "pitch": 1.35}),
        (18.9, "pop", {"gain": 0.3, "pitch": 1.5}),
        (21.05, "pop_big", {"gain": 0.4}),
        (23.6, "powerup", {"gain": 0.35}),
        (23.8, "impact_soft", {"gain": 0.5}),
        (23.85, "shimmer", {"dur": 1.6, "gain": 0.35}),
        (24.6, "swish_hi", {"gain": 0.35}),
    ]
