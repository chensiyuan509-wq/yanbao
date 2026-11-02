"""05 · 孤岛与飞轮（下）：付费飞轮也转不动 → 一步跨进移动互联网，免费 / 广告 / 补贴成了常态；
2017 年未授权软件比例 66% → 软件公司收入对比 → 芯片受限，月之暗面 / 深度求索 / 智谱选择开放权重 →
既是无奈也是聪明的打法（下载量超过美国）→ 下载 ≠ 反馈，免费 ≠ 收入。"""
import math

from ..core import (TAU, Cam, at, box_shadow, circle, clamp, ease_back, ease_in, ease_io, ease_out, ease_out5,
                    ellipse, fill, glow, lerp, lin, line, pop, prog, rad, ring_burst, rng, rrect, setc, smooth,
                    sparkle_burst, star4, star5, stroke_pts, text, text_w, view, arrow,
                    bezier_pts, point_on, polyline_partial, poly)
from ..charts import MapView, arc_pts, flywheel, hbars, world_dots
from ..icons import ic_lock
from ..props import bg_grad, chip_pkg, moon_icon, name_card, smiley, tag, whale
from ..ui import stamp
from .common import host, mini_icon, talk_lines

DUR = 57.0
CHAPTER = ("05", "孤岛与飞轮")

VO = [
    (0.7, '另一个飞轮，{付费}，在中国也转得很吃力。'),
    (4.8, '中国几乎是一步跨进了移动互联网，免费、广告、补贴成了常态，个人和企业都没养成为软件付费的习惯；2017 年，中国电脑上未授权软件的比例高达 66%。'),
    (18.8, '拥有 6.78 亿月活设备的金山办公，2025 年收入约 59 亿元；金蝶约 70 亿元，都不到 ServiceNow 的十分之一。'),
    (28.0, '再加上高端芯片受限，月之暗面、深度求索、智谱们纷纷选择了{开放权重}：Kimi K2.6、DeepSeek V4、GLM-5，都免费开放下载。'),
    (40.0, '这既是无奈，也是聪明的打法：换来全球开发者、影响力和人才，Hugging Face 上中国模型的下载量已经超过美国。'),
    (49.2, '但{下载不等于反馈}，{免费也不等于收入}，没有数据和付费的闭环，就很难跑出最强的模型。'),
]

G = 900
XA, XB, XC, XD, XE, XF = 960, 3100, 5300, 7500, 9700, 11900

P = (host(XA - 520, G, 0.6, "determined", seed=13.3)
     .fx(0, ()).look(0, 1.0, -0.4)
     .push(0.8, 3.6, "r").expr(3.6, "tired").fx(3.6, ("sweat",))
     .expr(4.5, "smile").fx(4.5, ()).run_to(4.6, 5.4, XB - 780, G)
     .expr(5.5, "curious").look(5.5, 0.9, -0.6)
     .expr(8.6, "hmm").fx(8.6, ())
     .expr(13.6, "shock").startle(14.0).expr(15.0, "worried")
     .expr(18.0, "smile").run_to(18.1, 18.9, XC - 800, G)
     .expr(19.0, "curious").look(19.0, 0.9, -0.6)
     .expr(24.0, "surprised").expr(25.4, "sad")
     .expr(27.2, "smile").run_to(27.3, 28.1, XD - 780, G)
     .expr(28.2, "worried").look(28.2, 0.9, -0.5)
     .expr(32.0, "curious").expr(35.6, "awe").look(35.6, 0.9, -0.8)
     .expr(39.2, "smile").run_to(39.3, 40.1, XE - 760, G)
     .expr(40.2, "think").expr(41.4, "smile").fx(41.4, ("idea",)).fx(42.6, ())
     .expr(45.4, "starry").look(45.4, 0.9, -0.6)
     .expr(48.4, "smile").run_to(48.5, 49.3, XF - 640, G)
     .expr(49.4, "hmm").look(49.4, 0.9, -0.8)
     .expr(53.0, "focused").look(53.0, 0.8, -1.0))
talk_lines(P, VO, [0, 3, 5], smile=0.25)

CAM = Cam([
    (0.0, (XA, 540, 1.06)),
    (4.4, (XA + 20, 540, 1.0)),
    (5.4, (XB, 540, 1.0), ease_io),
    (11.2, (XB + 20, 540, 1.02)),
    (11.9, (XB + 380, 540, 1.04), ease_io),
    (17.9, (XB + 400, 540, 1.05)),
    (18.9, (XC, 540, 1.0), ease_io),
    (27.2, (XC + 20, 540, 1.02)),
    (28.1, (XD, 540, 1.0), ease_io),
    (39.2, (XD + 20, 540, 1.02)),
    (40.1, (XE, 540, 1.0), ease_io),
    (48.4, (XE + 20, 540, 1.02)),
    (49.3, (XF, 540, 1.0), ease_io),
    (57.0, (XF + 20, 520, 1.08)),
], drift=6, seed=27.0)


def _bg(ctx, t, cam):
    warm = smooth(prog(t, 39.5, 41.0)) * (1 - smooth(prog(t, 48.6, 50.0)))
    bg_grad(ctx, "#1F2A44", "#3C3352", "#2A2F4C", 0.6)
    ctx.set_source(rad(960, 1100, 0, 1100, [(0, "#FFB27A", 0.18 + 0.25 * warm), (1, "#FFB27A", 0)]))
    ctx.paint()
    with view(ctx, cam, 1.0):
        ctx.rectangle(-1000, G, 14000, 400)
        ctx.set_source(lin(0, G, 0, G + 260, [(0, "#353A58"), (1, "#1C1F32")]))
        ctx.fill()
        ctx.rectangle(-1000, G - 2, 14000, 4)
        fill(ctx, "#FFB27A", 0.25)


def _part_a(ctx, t):
    a = 1.0
    rot = 0.25 * math.sin(clamp(t / 4.0) * math.pi) * smooth(prog(t, 0.8, 3.6))
    flywheel(ctx, XA + 260, 470, 290, ["收入", "研发", "好产品"], rot, ["#E0A42B", "#8B6CFF", "#3CCB7F"], a, None, 38,
             jam=0.65, t=t, center="付费飞轮", thick=110)
    if t > 2.0:
        tag(ctx, "转得很吃力", XA + 260, 110, 32, "#FFFFFF", "#C42A30", smooth(prog(t, 2.0, 2.4)))


def _part_b(ctx, t):
    a = smooth(prog(t, 4.4, 5.0)) * (1 - smooth(prog(t, 18.2, 18.8)))
    if a <= 0:
        return
    # 一步跨进移动互联网
    x0 = XB - 420
    stages = [("PC 时代", x0, "#7A8CA8"), ("移动互联网", x0 + 640, "#FF9F68")]
    for i, (lab, x, c) in enumerate(stages):
        q = pop(t, 5.0 + i * 1.0, 0.45)
        if q > 0:
            with at(ctx, x, 560, q):
                rrect(ctx, -170, -60, 340, 120, 30)
                fill(ctx, c, a)
                text(ctx, lab, 0, 0, 40, "#FFFFFF", a, "black")
    u = prog(t, 5.4, 6.4)
    if u > 0:
        pts = arc_pts((x0 + 60, 480), (x0 + 580, 480), 0.55)
        stroke_pts(ctx, polyline_partial(pts, 0, ease_io(u)), 7, "#FFD36B", a)
        if u < 1:
            (px, py), _ = point_on(pts, ease_io(u))
            star4(ctx, px, py, 26, "#FFFFFF", a, t * 4)
        text(ctx, "一步跨过去", x0 + 320, 290, 30, "#FFD36B", a * smooth(prog(t, 6.0, 6.4)), "black")
    for i, (lab, c) in enumerate((("免费", "#3CCB7F"), ("广告", "#4C8DFF"), ("补贴", "#E5484D"))):
        q = pop(t, 7.0 + i * 0.45, 0.45)
        if q > 0:
            with at(ctx, x0 + 320 + (i - 1) * 220, 760, q, (i - 1) * 0.08):
                rrect(ctx, -90, -42, 180, 84, 42)
                fill(ctx, c, a)
                text(ctx, lab, 0, 0, 40, "#FFFFFF", a, "black")
    if t > 9.0:
        tag(ctx, "没养成为软件付费的习惯", x0 + 320, 870, 26, "#FFFFFF", "#4A4458", smooth(prog(t, 9.4, 9.8)) * a)
    # 盗版：未授权软件比例
    b = smooth(prog(t, 11.6, 12.2)) * a
    if b > 0:
        cx = XB + 780
        with at(ctx, cx - 160, 430, 1.0, -0.08):
            box_shadow(ctx, -130, -170, 260, 340, 16, blur=24, a=0.3 * b, dy=10)
            rrect(ctx, -130, -170, 260, 340, 16)
            ctx.set_source(lin(0, -170, 0, 170, [(0, "#6C8CD5", b), (1, "#3D5AA8", b)]))
            ctx.fill()
            circle(ctx, 0, -20, 70)
            fill(ctx, "#DCE6FF", b)
            circle(ctx, 0, -20, 18)
            fill(ctx, "#3D5AA8", b)
            text(ctx, "办公软件", 0, 110, 30, "#FFFFFF", b, "black")
        sk = clamp((t - 13.2) / 0.3)
        if sk > 0:
            stamp(ctx, "盗版", cx - 160, 420, 56, "#E5484D", b * min(1, sk * 2), -0.2, lerp(2.0, 1.0, ease_out(sk)))
        n = int(lerp(0, 66, ease_out(prog(t, 14.4, 16.2))))
        if t > 14.2:
            with at(ctx, cx + 240, 400, 1.0):
                rrect(ctx, -220, -150, 440, 300, 30)
                fill(ctx, "#FFFFFF", 0.95 * b)
                text(ctx, "2017 年 · 中国电脑", 0, -100, 26, "#7A7186", b, "bold")
                text(ctx, "未授权软件比例", 0, -60, 30, "#2B2233", b, "black")
                text(ctx, f"{n}%", 0, 30, 104, "#E5484D", b, "black")
                text(ctx, "同期美国不到 20%", 0, 112, 24, "#7A7186", b * smooth(prog(t, 16.2, 16.6)), "bold")
            tag(ctx, "数据：BSA 全球软件调查", cx + 240, 590, 22, "#FFFFFF", "#4A4458", b)


REV = [("ServiceNow", 943, "#62D84E", "≈ 940 亿元（133 亿美元）"), ("金蝶", 70, "#2F7BF6", "≈ 70 亿元"),
       ("金山办公", 59, "#E5484D", "≈ 59 亿元")]


def _part_c(ctx, t):
    a = smooth(prog(t, 18.4, 19.0)) * (1 - smooth(prog(t, 27.6, 28.2)))
    if a <= 0:
        return
    x0, y0 = XC - 520, 200
    rrect(ctx, x0 - 50, y0 - 70, 1160, 520, 32)
    fill(ctx, "#FFFFFF", 0.93 * a)
    text(ctx, "2025 年收入对比（人民币）", x0 + 530, y0 - 18, 32, "#2B2233", a, "black")
    order = [REV[2], REV[1], REV[0]]
    hbars(ctx, order, x0, y0 + 80, 1000, 120, prog(t, 19.6, 25.6), a, 32, vmax=1260, label_w=220,
          stagger=0.38, bar_h=64)
    k = pop(t, 19.6, 0.5)
    if k > 0:
        with at(ctx, x0 + 640, y0 + 30 + 60, k * 0.95):
            rrect(ctx, -190, -30, 380, 60, 30)
            fill(ctx, "#E5484D")
            text(ctx, "WPS 月活设备 6.78 亿", 0, 0, 28, "#FFFFFF", 1, "black")
    r = pop(t, 25.6, 0.5)
    if r > 0:
        with at(ctx, x0 + 760, y0 + 400, r, -0.05):
            rrect(ctx, -230, -42, 460, 84, 42)
            fill(ctx, "#2B2233")
            text(ctx, "都不到 ServiceNow 的十分之一", 0, 0, 30, "#FFD36B", 1, "black")
    text(ctx, "数据：各公司 2025 年年报，按 1 美元 ≈ 7.1 元折算", x0 + 530, y0 + 500, 20, "#9A8FA8", a, "bold")


LABS = [("Kimi K2.6", "月之暗面", "#1E1E2E", "moon"), ("DeepSeek V4", "深度求索", "#4D6BFE", "whale"),
        ("GLM-5", "智谱", "#3A62F0", "z")]


def _part_d(ctx, t):
    a = smooth(prog(t, 27.6, 28.2)) * (1 - smooth(prog(t, 39.6, 40.2)))
    if a <= 0:
        return
    # 高端芯片受限
    lk = smooth(prog(t, 28.4, 28.9)) * (1 - smooth(prog(t, 31.6, 32.2)))
    if lk > 0:
        with at(ctx, XD - 120, 420, 1.0):
            chip_pkg(ctx, 0, 0, 260, "GPU", "高端芯片", "#76B900", a * lk, 0.2, t)
            ctx.set_line_width(14)
            setc(ctx, "#9AA0AE", a * lk)
            for k in range(-3, 4):
                circle(ctx, k * 46, k * 46 * 0.9, 20)
                ctx.stroke()
            ic_lock(ctx, 0, 30, 130, a * lk, t)
        tag(ctx, "高端芯片受限", XD - 120, 650, 32, "#FFFFFF", "#C42A30", a * lk)
    # 三家开源实验室
    for i, (model, lab, c, icon) in enumerate(LABS):
        st = 32.2 + i * 1.1
        q = pop(t, st, 0.5)
        if q <= 0:
            continue
        x = XD - 560 + i * 560
        y = 420
        with at(ctx, x, y, q):
            box_shadow(ctx, -200, -170, 400, 340, 28, blur=26, a=0.3, dy=10)
            rrect(ctx, -200, -170, 400, 340, 28)
            fill(ctx, "#FFFFFF", 0.96 * a)
            if icon == "moon":
                moon_icon(ctx, 0, -60, 70, a, "#FFFFFF", c)
            elif icon == "whale":
                whale(ctx, 0, -60, 0.55, a, t)
            else:
                rrect(ctx, -60, -120, 120, 120, 28)
                fill(ctx, c, a)
                text(ctx, "Z", 0, -60, 80, "#FFFFFF", a, "black")
            text(ctx, model, 0, 60, 40, "#2B2233", a, "black")
            text(ctx, lab, 0, 112, 28, "#7A7186", a, "bold")
        # 权重像光块一样飞向全球
        for k in range(5):
            u = clamp((t - st - 0.6 - k * 0.18) / 1.6)
            if 0 < u < 1:
                pts = bezier_pts((x, y + 120), (x, y + 360), (XD + (k - 2) * 300, 980), (XD + (k - 2) * 420, 1200), 30)
                (px, py), _ = point_on(pts, ease_in(u))
                rrect(ctx, px - 14, py - 14, 28, 28, 6)
                fill(ctx, c, a * (1 - u))
                glow(ctx, px, py, 30, "#9FD8FF", 0.5 * a * (1 - u))
    if t > 36.0:
        with at(ctx, XD, 760, pop(t, 36.0, 0.5)):
            rrect(ctx, -300, -46, 600, 92, 46)
            fill(ctx, "#3CCB7F")
            text(ctx, "开放权重 · 免费下载", 0, 0, 40, "#FFFFFF", 1, "black")


def _part_e(ctx, t):
    a = smooth(prog(t, 39.6, 40.2)) * (1 - smooth(prog(t, 48.8, 49.4)))
    if a <= 0:
        return
    # 无奈 / 聪明
    for i, (lab, c, ic) in enumerate((("无奈", "#6B6377", "lock"), ("聪明的打法", "#E0A42B", "idea"))):
        q = pop(t, 40.4 + i * 0.9, 0.5) * (1 - smooth(prog(t, 42.8, 43.3)))
        if q > 0:
            with at(ctx, XE - 330 + i * 660, 300, q):
                rrect(ctx, -200, -80, 400, 160, 40)
                fill(ctx, c, a)
                text(ctx, lab, 0, 0, 52, "#FFFFFF", a, "black")
    # 收获：开发者 · 影响力 · 人才
    for i, (lab, c) in enumerate((("全球开发者", "#4C8DFF"), ("影响力", "#FF9F68"), ("人才", "#8B6CFF"))):
        q = pop(t, 43.2 + i * 0.5, 0.5)
        if q > 0:
            with at(ctx, XE - 560 + i * 380, 230, q):
                circle(ctx, 0, 0, 90)
                fill(ctx, c, a)
                text(ctx, lab, 0, 0, 34 if len(lab) <= 3 else 28, "#FFFFFF", a, "black")
    # Hugging Face 下载量
    b = smooth(prog(t, 45.0, 45.5))
    if b > 0:
        x0, y0 = XE - 420, 420
        rrect(ctx, x0 - 60, y0 - 50, 960, 330, 30)
        fill(ctx, "#FFFFFF", 0.94 * a * b)
        smiley(ctx, x0 - 10, y0 - 4, 30, a * b)
        text(ctx, "Hugging Face 模型下载量占比", x0 + 40, y0 - 4, 30, "#2B2233", a * b, "black", "l")
        hbars(ctx, [("中国模型", 41, "#E5484D", "41%"), ("美国模型", 36.5, "#4C8DFF", "36.5%")], x0, y0 + 80,
              820, 90, prog(t, 45.4, 47.4), a * b, 32, vmax=45, label_w=180, stagger=0.3)
        text(ctx, "统计区间：2025.2 – 2026.2 · 来源：Hugging Face 报告", x0 + 420, y0 + 255, 20, "#9A8FA8", a * b, "bold")


def _part_f(ctx, t):
    a = smooth(prog(t, 48.8, 49.4))
    if a <= 0:
        return
    for i, (l, r, st) in enumerate((("下载", "反馈", 49.6), ("免费", "收入", 51.4))):
        q = pop(t, st, 0.5)
        if q <= 0:
            continue
        with at(ctx, XF - 360, 260 + i * 190, q):
            rrect(ctx, -300, -66, 600, 132, 40)
            fill(ctx, "#FFFFFF", 0.95 * a)
            text(ctx, l, -150, 0, 56, "#2B2233", a, "black")
            text(ctx, "≠", 0, 0, 72, "#E5484D", a, "black")
            text(ctx, r, 150, 0, 56, "#2B2233", a, "black")
    # 断开的闭环 + 够不着的山顶
    c = smooth(prog(t, 52.6, 53.2))
    if c > 0:
        mx, my = XF + 400, 520
        poly(ctx, [(mx - 330, G), (mx - 40, my - 260), (mx + 60, my - 180), (mx + 330, G)])
        ctx.set_source(lin(0, my - 260, 0, G, [(0, "#8E9BB8", a * c), (1, "#4A5270", a * c)]))
        ctx.fill()
        poly(ctx, [(mx - 40, my - 260), (mx - 100, my - 180), (mx + 10, my - 200), (mx + 60, my - 180)])
        fill(ctx, "#FFFFFF", 0.9 * a * c)
        line(ctx, mx - 40, my - 260, mx - 40, my - 360, 5, "#5A4A40", a * c)
        poly(ctx, [(mx - 38, my - 360), (mx + 40, my - 340), (mx - 38, my - 318)])
        fill(ctx, "#FFD36B", a * c)
        tag(ctx, "最强的模型", mx - 40, my - 410, 30, "#3A2A00", "#FFD36B", a * c)
        # 断开的环
        for k in range(4):
            a0 = k * TAU / 4 + 0.25
            ctx.new_path()
            ctx.arc(XF - 360, 720, 110, a0, a0 + TAU / 4 - 0.5)
            ctx.set_line_width(22)
            ctx.set_line_cap(1)
            setc(ctx, ["#FF9F68", "#8B6CFF", "#2EC4B6", "#E0A42B"][k], a * c)
            ctx.stroke()
        text(ctx, "闭环断了", XF - 360, 720, 30, "#FFFFFF", a * c, "black")


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
        (0.8, "ratchet", {"dur": 2.4, "gain": 0.3}), (2.0, "womp", {"gain": 0.3}),
        (4.6, "whoosh_short", {"gain": 0.3}),
        (5.0, "pop", {"gain": 0.3}), (5.4, "whoosh", {"dur": 1.0, "gain": 0.3}), (6.0, "pop", {"gain": 0.3, "pitch": 1.2}),
        (7.0, "pop", {"gain": 0.28, "pitch": 1.1}), (7.45, "pop", {"gain": 0.28, "pitch": 1.25}),
        (7.9, "pop", {"gain": 0.28, "pitch": 1.4}),
        (11.6, "whoosh_short", {"gain": 0.25}), (13.2, "stamp", {"gain": 0.5}),
        (14.4, "rise", {"dur": 1.8, "gain": 0.25}),
        (18.1, "whoosh_short", {"gain": 0.3}),
        (19.6, "pop", {"gain": 0.3}), (19.8, "rise", {"dur": 1.0, "gain": 0.2}),
        (22.0, "rise", {"dur": 1.0, "gain": 0.2, "pitch": 1.1}), (24.2, "rise", {"dur": 1.4, "gain": 0.25, "pitch": 1.3}),
        (25.6, "stamp", {"gain": 0.35}),
        (27.3, "whoosh_short", {"gain": 0.3}),
        (28.4, "lock", {"gain": 0.45}), (28.5, "clunk", {"gain": 0.3}),
        (31.6, "zap", {"dur": 0.6, "gain": 0.3}),
        (32.2, "pop_big", {"gain": 0.35}), (33.3, "pop_big", {"gain": 0.35, "pitch": 1.1}),
        (34.4, "pop_big", {"gain": 0.35, "pitch": 1.2}),
        (32.8, "stream", {"dur": 4.0, "gain": 0.18}),
        (36.0, "success", {"gain": 0.35}),
        (39.3, "whoosh_short", {"gain": 0.3}),
        (40.4, "womp", {"gain": 0.25}), (41.3, "ding", {"gain": 0.35}),
        (43.2, "pop", {"gain": 0.3}), (43.7, "pop", {"gain": 0.3, "pitch": 1.2}), (44.2, "pop", {"gain": 0.3, "pitch": 1.4}),
        (45.4, "rise", {"dur": 2.0, "gain": 0.25}), (47.4, "chime", {"gain": 0.3}),
        (48.5, "whoosh_short", {"gain": 0.3}),
        (49.6, "error", {"gain": 0.3}), (51.4, "error", {"gain": 0.3, "pitch": 0.9}),
        (52.6, "rumble", {"dur": 0.8, "gain": 0.25}), (54.0, "womp", {"gain": 0.3}),
    ]
