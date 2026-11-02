"""01 · 一篇论文（下）：接力棒从谷歌传到 OpenAI → GPT 参数暴涨 → ChatGPT 两个月破亿 →
八位作者各奔东西 → 硅谷里的接力。"""
import math

from ..core import (TAU, Cam, at, circle, clamp, ease_in, ease_io, ease_out, ease_out5, fill, glow,
                    kf, lerp, lin, pop, prog, rad, ring_burst, rrect, setc, smooth, sparkle_burst,
                    star4, stroke_pts, text, text_w, view, polyline_partial, point_on)
from ..charts import arc_pts, vbars
from ..props import bg_grad, garage, name_card, office, tag
from ..ui import bubble, typing_dots, window
from mascot import draw_prop
from mascot.fx import fx_confetti
from .common import host, talk_lines

DUR = 29.5
CHAPTER = ("01", "一篇论文")

VO = [
    (0.7, '可最先把它推向极致的，不是谷歌，而是一家创业公司：{OpenAI}。'),
    (6.3, '从 2018 年的 GPT，到 2020 年的 GPT-3，参数涨了一千多倍；'),
    (12.2, '2022 年底，{ChatGPT} 上线，两个月用户破亿。'),
    (16.8, '有意思的是，论文的八位作者后来陆续离开谷歌，有的创业，有的加入别家。'),
    (23.3, '{论文公开、人才流动}，一个好点子，就这样在硅谷接力奔跑。'),
]

GROUND = 900
XA, XB, XC, XD, XE = 960, 3200, 5440, 7680, 9920     # 五段画面的中心
GOO = (XA - 430, GROUND)
OAI = (XA + 470, GROUND)

P = (host(XA, GROUND, 0.58, "curious", seed=3.3)
     .look(0, -0.8, -0.6)
     .look(1.3, -0.5, -0.9).look(2.3, 0.6, -0.6).look(3.2, 0.9, -0.2)
     .expr(3.5, "excited").hop(3.6, 40, 0.38)
     .expr(5.6, "determined").run_to(5.65, 6.6, XB - 760, GROUND)
     .expr(6.7, "awe").look(6.7, 0.8, -0.8)
     .expr(10.0, "shock").startle(10.0)
     .expr(11.4, "smile").run_to(11.5, 12.4, XC - 760, GROUND)
     .expr(12.5, "excited").look(12.5, 0.8, -0.5)
     .cheer(14.6, 16.0)
     .expr(16.1, "smile").run_to(16.2, 17.1, XD - 760, GROUND)
     .expr(17.2, "curious").look(17.2, 0.7, -0.7)
     .look(18.2, 0.3, -0.9).look(19.4, 1.0, -0.4).expr(20.6, "hmm")
     .expr(22.6, "fired_up").fx(22.6, ()).hold(22.7, ("baton",), "r", -0.5).arm(22.7, "r", 1.15)
     .run_to(22.8, 27.6, XE + 760, GROUND).arm(27.7, "r", 0.6)
     .expr(27.8, "proud"))
talk_lines(P, VO, [0, 3], smile=0.3)

CAM = Cam([
    (0.0, (XA, 560, 1.05)),
    (5.4, (XA + 20, 555, 1.0)),
    (6.5, (XB, 540, 1.0), ease_io),
    (11.3, (XB + 20, 540, 1.02)),
    (12.4, (XC, 540, 1.0), ease_io),
    (16.0, (XC + 20, 540, 1.02)),
    (17.1, (XD, 540, 1.0), ease_io),
    (22.4, (XD + 40, 540, 1.0)),
    (23.6, (XE - 300, 560, 0.86), ease_io),
    (27.4, (XE + 380, 560, 0.86)),
    (29.5, (XE + 560, 560, 0.9)),
], drift=6, seed=7.0)


def _bg(ctx, t, cam):
    bg_grad(ctx, "#DCEBFF", "#FFE9D6", "#F2EDFF", 0.55)
    with view(ctx, cam, 0.35):
        # 远山
        for i in range(14):
            x = -600 + i * 820
            ctx.move_to(x - 520, 900)
            ctx.curve_to(x - 240, 620 - (i % 3) * 40, x + 240, 620 - (i % 3) * 40, x + 520, 900)
            ctx.close_path()
            fill(ctx, "#C9D6F2", 0.55)
    with view(ctx, cam, 1.0):
        ctx.rectangle(-1000, GROUND, 13000, 400)
        ctx.set_source(lin(0, GROUND, 0, GROUND + 300, [(0, "#E8D9C8"), (1, "#D9C3AE")]))
        ctx.fill()
        ctx.rectangle(-1000, GROUND - 4, 13000, 8)
        fill(ctx, "#C4A98E", 0.6)


def _part_a(ctx, t):
    office(ctx, GOO[0], GOO[1], 420, 560, "#4C8DFF", 1.0, "", windows=True, t=t)
    name_card(ctx, "谷歌", GOO[0], GOO[1] - 610, "#4285F4", 34, 1.0, sub="发表论文")
    k = smooth(prog(t, 3.3, 4.2))
    garage(ctx, OAI[0], OAI[1], 380, 320, 1.0, label="", t=t, door=k, glow_a=k)
    name_card(ctx, "OpenAI", OAI[0], OAI[1] - 380, "#10A37F", 34, 1.0, sub="2015 年成立的创业公司")
    # 论文像接力棒一样飞过去
    u = prog(t, 1.2, 3.4)
    if 0 < u < 1:
        pts = arc_pts((GOO[0] + 60, GOO[1] - 420), (OAI[0], OAI[1] - 160), 0.35)
        (px, py), ang = point_on(pts, ease_io(u))
        for k2 in range(6):
            (qx, qy), _ = point_on(pts, max(0, ease_io(u) - k2 * 0.03))
            glow(ctx, qx, qy, 40 - k2 * 5, "#FFD36B", 0.35)
        with at(ctx, px, py, 0.9, ang * 0.3):
            draw_prop(ctx, ("paper", {"title": "Transformer"}), t)
        if u > 0.2:
            tag(ctx, "公开发表", px, py - 130, 26, "#FFFFFF", "#FF9F68", smooth((u - 0.2) / 0.2) * (1 - smooth((u - 0.85) / 0.15)))
    if t >= 3.4:
        q = pop(t, 3.4, 0.5)
        sparkle_burst(ctx, t, 3.45, OAI[0], OAI[1] - 160, 10, 200, "#FFE7A3", 0.9, 5, 18)
        if q > 0 and t < 6.5:
            with at(ctx, OAI[0], OAI[1] - 170, q * 0.8):
                draw_prop(ctx, ("paper", {"title": "GPT"}), t)


def _part_b(ctx, t):
    a = smooth(prog(t, 5.9, 6.6))
    if a <= 0:
        return
    x0 = XB - 520
    rrect(ctx, x0 - 80, 160, 1200, 640, 34)
    fill(ctx, "#FFFFFF", 0.82 * a)
    text(ctx, "参数量（对数刻度）", XB + 60, 215, 32, "#6B6377", a, "black")
    items = [("GPT · 2018", 1.17e8, "#9CC2FF", "1.17 亿"), ("GPT-2 · 2019", 1.5e9, "#7AA8FF", "15 亿"),
             ("GPT-3 · 2020", 1.75e11, "#4C8DFF", "1750 亿")]
    vbars(ctx, items, x0 + 40, 720, 230, 120, 400, prog(t, 6.6, 10.6), a, 30, log=True, stagger=0.3)
    b = pop(t, 10.0, 0.5)
    if b > 0:
        with at(ctx, XB + 600, 250, b, -0.12):
            glow(ctx, 0, 0, 160, "#FF9F68", 0.4)
            rrect(ctx, -140, -52, 280, 104, 52)
            fill(ctx, "#FF9F68")
            text(ctx, "× 1500", 0, 0, 56, "#FFFFFF", 1, "black")
        sparkle_burst(ctx, t, 10.05, XB + 600, 250, 9, 200, "#FFC57A", 0.8, 6, 18)


def _part_c(ctx, t):
    a = smooth(prog(t, 11.7, 12.4))
    if a <= 0:
        return
    wx, wy, ww, wh = XC - 640, 170, 760, 600
    cx, cy, cw, ch = window(ctx, wx, wy, ww, wh, "ChatGPT", a, accent="#10A37F", title_size=26)
    ctx.save()
    ctx.rectangle(cx, cy, cw, ch)
    ctx.clip()
    q1 = pop(t, 12.6, 0.4)
    if q1 > 0:
        with at(ctx, cx + cw - 30, cy + 60, q1):
            bubble(ctx, -420, -36, 420, 72, "#E9F7F1", a, "right")
            text(ctx, "帮我写一首关于春天的诗", -210, 0, 28, "#2B2233", a, "bold")
    if t > 13.3:
        bubble(ctx, cx + 30, cy + 140, cw - 120, 290, "#F4F2F8", a, "left")
        lines = ["春风翻开了一页书，", "柳枝在水面写字，", "燕子把天空折成信，", "寄给每一个醒来的人。"]
        n = (t - 13.5) * 9
        for i, L in enumerate(lines):
            k = int(clamp(n - i * 9, 0, len(L)))
            if k > 0:
                text(ctx, L[:k], cx + 60, cy + 190 + i * 58, 30, "#2B2233", a, "bold", "l")
        if n < 36:
            typing_dots(ctx, cx + 90, cy + 400, t, a=a)
    ctx.restore()
    tag(ctx, "2022.11.30 上线", wx + ww / 2, wy - 40, 28, "#FFFFFF", "#10A37F", a)
    # 用户数计数器
    gx = XC + 470
    u = ease_in(prog(t, 12.8, 15.0)) ** 0.8
    users = 1e8 * u
    rrect(ctx, gx - 230, 260, 460, 330, 34)
    fill(ctx, "#2B2233", 0.92 * a)
    text(ctx, "用户数", gx, 315, 30, "#CDBFE6", a, "bold")
    val = f"{users / 1e4:,.0f} 万" if users < 1e8 else "1 亿"
    text(ctx, val, gx, 420, 74 if users >= 1e8 else 62, "#FFD36B", a, "black")
    from ..ui import progress
    progress(ctx, gx - 180, 500, 360, 18, u, "#FFD36B", "#4A4458", a)
    rb = pop(t, 15.0, 0.5)
    if rb > 0:
        with at(ctx, gx, 620, rb, -0.06):
            rrect(ctx, -150, -36, 300, 72, 36)
            fill(ctx, "#FF6B9A")
            text(ctx, "只用 2 个月", 0, 0, 34, "#FFFFFF", 1, "black")
        ctx.save()
        ctx.translate(gx, 600)
        fx_confetti(ctx, t, smooth(prog(t, 15.0, 15.4)) * (1 - smooth(prog(t, 16.6, 17.2))))
        ctx.restore()


AUTH = ["A.V.", "N.S.", "N.P.", "J.U.", "L.J.", "A.G.", "L.K.", "I.P."]
DEST = ["Essential AI", "Character.AI", "Essential AI", "Inceptive", "Sakana AI", "Cohere", "OpenAI", "NEAR"]
DEST_POS = {"Essential AI": (XD + 60, 380), "Character.AI": (XD + 340, 250), "Inceptive": (XD + 600, 400),
            "Sakana AI": (XD + 720, 640), "Cohere": (XD + 380, 760), "OpenAI": (XD - 120, 760),
            "NEAR": (XD + 120, 560)}


def _part_d(ctx, t):
    a = smooth(prog(t, 16.4, 17.1))
    if a <= 0:
        return
    gx, gy = XD - 520, GROUND
    office(ctx, gx, gy, 360, 500, "#4C8DFF", a, "", windows=True, t=t)
    name_card(ctx, "谷歌", gx, gy - 550, "#4285F4", 32, a)
    for name, (x, y) in DEST_POS.items():
        q = pop(t, 17.6 + list(DEST_POS).index(name) * 0.15, 0.45)
        if q > 0:
            with at(ctx, x, y, q):
                rrect(ctx, -110, -34, 220, 68, 34)
                fill(ctx, "#FFFFFF", 0.95 * a)
                text(ctx, name, 0, 0, 26, "#2B2233", a, "black")
    for i, (au, dst) in enumerate(zip(AUTH, DEST)):
        st = 17.3 + i * 0.32
        u = ease_io(prog(t, st, st + 1.1))
        if u <= 0:
            continue
        dx, dy = DEST_POS[dst]
        off = (-40 if i == 0 else 40) if dst == "Essential AI" else 0
        pts = arc_pts((gx + 60, gy - 380), (dx + off, dy - 70), 0.3)
        (px, py), _ = point_on(pts, u)
        if u < 1:
            stroke_pts(ctx, polyline_partial(pts, max(0, u - 0.25), u), 4, "#FF9F68", 0.5 * a)
        circle(ctx, px, py, 30)
        fill(ctx, ["#FFB27A", "#B7A6FF", "#7FE0D4", "#9CC2FF"][i % 4], a)
        text(ctx, au, px, py + 1, 17, "#2B2233", a, "black")
    tg = smooth(prog(t, 20.4, 20.9))
    tag(ctx, "到 2023 年，八位作者已全部离开谷歌", XD + 300, 150, 30, "#FFFFFF", "#2B2233", a * tg)


VALLEY = [("谷歌", "#4285F4", -1250), ("OpenAI", "#10A37F", -750), ("Anthropic", "#D97757", -250),
          ("英伟达", "#76B900", 250), ("Meta", "#0866FF", 750), ("斯坦福", "#B1040E", 1250)]


def _part_e(ctx, t):
    a = smooth(prog(t, 22.6, 23.4))
    if a <= 0:
        return
    road_y = GROUND - 40
    pts = [(XE + dx, road_y - 140 - 90 * math.sin(i * 1.3)) for i, (_, _, dx) in enumerate(VALLEY)]
    # 公路
    ctx.set_line_width(26)
    ctx.set_line_cap(1)
    ctx.set_line_join(1)
    setc(ctx, "#B9A68A", 0.5 * a)
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.stroke()
    for i, (name, c, dx) in enumerate(VALLEY):
        q = pop(t, 23.0 + i * 0.12, 0.45)
        if q <= 0:
            continue
        x, y = pts[i]
        with at(ctx, x, y - 120, q):
            office(ctx, 0, 100, 150, 180, c, a, "", windows=True, t=t)
            name_card(ctx, name, 0, -130, c, 26, a)
    # 接力棒的光沿着公路传递
    u = prog(t, 23.6, 27.4)
    if u > 0:
        seg = polyline_partial(pts, 0, ease_io(u))
        stroke_pts(ctx, seg, 8, "#FFD36B", 0.9 * a)
        (px, py), _ = point_on(pts, ease_io(u))
        glow(ctx, px, py, 70, "#FFD36B", 0.8 * a)
        with at(ctx, px, py - 18, 0.7, -0.2):
            draw_prop(ctx, ("baton",), t)
    for i, lab in enumerate(("论文公开", "人才流动")):
        q = pop(t, 23.6 + i * 0.7, 0.45)
        if q > 0:
            with at(ctx, XE - 520 + i * 1040, 180, q):
                rrect(ctx, -150, -44, 300, 88, 44)
                fill(ctx, "#FF9F68" if i == 0 else "#8B6CFF", a)
                text(ctx, lab, 0, 0, 40, "#FFFFFF", a, "black")


def draw(ctx, t):
    cam = CAM.at(t)
    _bg(ctx, t, cam)
    with view(ctx, cam, 1.0):
        _part_a(ctx, t)
        _part_b(ctx, t)
        _part_c(ctx, t)
        _part_d(ctx, t)
        _part_e(ctx, t)
        P.draw(ctx, t)


def sfx():
    return [
        (1.2, "whoosh", {"dur": 2.0, "gain": 0.3}),
        (3.4, "gate", {"gain": 0.35}), (3.45, "shimmer", {"dur": 1.0, "gain": 0.3}),
        (5.65, "whoosh_short", {"gain": 0.3}),
        (6.6, "rise", {"dur": 0.8, "gain": 0.25}), (7.8, "rise", {"dur": 0.8, "gain": 0.25, "pitch": 1.2}),
        (9.0, "rise", {"dur": 0.9, "gain": 0.28, "pitch": 1.45}),
        (10.0, "pop_big", {"gain": 0.45}),
        (11.5, "whoosh_short", {"gain": 0.3}),
        (12.6, "bubble", {"gain": 0.3}), (13.4, "typing", {"dur": 2.4, "gain": 0.18}),
        (12.8, "spinup", {"dur": 2.2, "gain": 0.25}),
        (15.0, "success", {"gain": 0.4}), (15.05, "sparkle", {"dur": 1.2, "gain": 0.3}),
        (16.2, "whoosh_short", {"gain": 0.3}),
        (17.3, "swish", {"gain": 0.25}), (17.9, "swish", {"gain": 0.25}), (18.6, "swish", {"gain": 0.25}),
        (19.2, "swish", {"gain": 0.25}),
        (22.7, "powerup", {"gain": 0.3}),
        (23.6, "zip", {"gain": 0.25}), (24.3, "pop", {"gain": 0.3}),
        (24.6, "stream", {"dur": 2.8, "gain": 0.2}),
    ]
