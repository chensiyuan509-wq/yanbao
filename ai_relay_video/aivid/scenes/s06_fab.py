"""02 · 算力接力（下）：谁来造芯片？台积电 → "只代工、不设计" → 先进封装 / 测试 / 组装 →
亚利桑那的晶圆飞回台湾封装 → 跨越太平洋的接力赛。"""
import math

from ..core import (TAU, Cam, at, circle, clamp, ease_back, ease_in, ease_io, ease_out, ease_out5, fill,
                    glow, lerp, lin, line, pop, prog, rad, ring_burst, rng, rrect, setc, smooth,
                    sparkle_burst, star4, stroke_pts, text, text_w, view, polyline_partial, point_on,
                    check_mark)
from ..charts import MapView, arc_pts, map_pin, world_dots
from ..icons import ic_plane
from ..props import (bg_grad, chip_pkg, factory, grid_lines, hbm_stack, name_card, server_rack, tag, wafer)
from mascot import draw_prop
from .common import host, talk_lines

DUR = 43.5
CHAPTER = ("02", "算力接力")

VO = [
    (0.7, '芯片设计好了，谁来造？答案是{台积电}。'),
    (5.1, '1987 年，在美国德州仪器工作了二十多年的张忠谋，在台湾创办台积电，开创了「只代工、不设计」的模式。'),
    (13.5, '从此，英伟达这样的公司不用建工厂，专心设计就行。'),
    (18.5, '造好的芯片还要{封装测试}：用先进封装把 GPU 和高带宽内存封在一起，再测试、组装成服务器。'),
    (27.4, '2025 年，第一片美国造的 Blackwell 晶圆在亚利桑那下线，可它还得{飞回台湾}封装。'),
    (34.8, '美国设计、台湾制造，加上荷兰的光刻机、韩国的内存……这是一场跨越太平洋的{接力赛}。'),
]

G = 900
XA, XB, XC, XD, XM = 960, 3000, 5000, 7100, 9600
TSMC = "#E60012"
MAP = MapView(XM, 560, 5.0, lon0=172, lat0=28)
LOC = {"taiwan": (121.0, 23.7), "arizona": (-112.0, 33.4), "valley": (-122.0, 37.4),
       "texas": (-97.0, 32.8), "nl": (5.5, 51.4), "korea": (127.5, 36.5)}

P = (host(XA - 520, G, 0.58, "curious", seed=6.6, hat="explorer")
     .look(0, 0.9, -0.7)
     .expr(2.2, "hmm").fx(2.2, ("question",))
     .hat(3.2, "hardhat").fx(3.2, ()).expr(3.2, "fired_up").hop(3.15, 40, 0.38).fx(3.3, ())
     .expr(4.4, "smile").run_to(4.6, 5.4, XB - 760, G)
     .expr(5.5, "curious").look(5.5, 0.9, -0.6)
     .expr(11.0, "awe")
     .expr(12.6, "smile").run_to(12.7, 13.5, XC - 780, G)
     .expr(13.6, "happy").look(13.6, 0.9, -0.5).nod(16.2, 2)
     .expr(17.6, "smile").run_to(17.7, 18.5, XD - 760, G)
     .expr(18.6, "focused").look(18.6, 0.9, -0.6)
     .expr(22.6, "awe").expr(24.9, "proud")
     .hat(26.6, "explorer").expr(26.6, "excited").hop(26.6, 40, 0.38)
     .move(26.9, 27.6, XM - 820, G, ease_io).fade(26.9, 0.0, 0.4).fade(27.7, 1.0, 0.5)
     .expr(27.8, "curious").look(27.8, 0.8, -0.8)
     .expr(32.0, "surprised").expr(33.4, "smile")
     .expr(35.0, "excited").hold(35.2, ("baton",), "r", -0.5).arm(35.2, "r", 1.2)
     .expr(39.0, "proud").bounce(39.2, 43.0, 0.035, 1.6))
talk_lines(P, VO, [0, 2], smile=0.3)

CAM = Cam([
    (0.0, (XA, 540, 1.04)),
    (4.4, (XA + 20, 540, 1.0)),
    (5.4, (XB, 540, 1.0), ease_io),
    (12.5, (XB + 20, 540, 1.02)),
    (13.5, (XC, 540, 1.0), ease_io),
    (17.5, (XC + 20, 540, 1.02)),
    (18.5, (XD, 540, 1.0), ease_io),
    (26.5, (XD + 20, 540, 1.03)),
    (27.6, (XM + 30, 470, 1.55), ease_io),
    (33.6, (XM + 40, 470, 1.6)),
    (35.4, (XM, 520, 1.0), ease_io),
    (43.5, (XM, 520, 1.04)),
], drift=6, seed=13.0)


def _bg(ctx, t, cam):
    bg_grad(ctx, "#0E1A2C", "#152238", "#101C30", 0.6)
    with view(ctx, cam, 0.6):
        grid_lines(ctx, -800, -400, 11500, 1600, 90, "#5FA8FF", 0.06)
    with view(ctx, cam, 1.0):
        ctx.rectangle(-1000, G, 9200, 400)
        ctx.set_source(lin(0, G, 0, G + 260, [(0, "#1C2A40"), (1, "#0E1626")]))
        ctx.fill()
        ctx.rectangle(-1000, G - 2, 9200, 4)
        fill(ctx, "#5FA8FF", 0.3)


def _blueprint(ctx, x, y, w, h, a, t):
    rrect(ctx, x - w / 2, y - h / 2, w, h, 16)
    fill(ctx, "#1F4E8C", a)
    ctx.save()
    rrect(ctx, x - w / 2, y - h / 2, w, h, 16)
    ctx.clip()
    grid_lines(ctx, x - w / 2, y - h / 2, x + w / 2, y + h / 2, 24, "#9FD0FF", 0.2 * a)
    R = rng(4)
    ctx.set_line_width(3)
    setc(ctx, "#CFE8FF", 0.7 * a)
    for i in range(16):
        px, py = x - w / 2 + R.uniform(30, w - 30), y - h / 2 + R.uniform(30, h - 30)
        ctx.move_to(px, py)
        ctx.line_to(px + R.choice((-1, 1)) * R.uniform(40, 120), py)
        ctx.line_to(px + R.choice((-1, 1)) * R.uniform(40, 120), py + R.choice((-1, 1)) * R.uniform(30, 80))
    ctx.stroke()
    rrect(ctx, x - w * 0.18, y - h * 0.18, w * 0.36, h * 0.36, 8)
    ctx.set_line_width(4)
    setc(ctx, "#FFFFFF", 0.85 * a)
    ctx.stroke()
    ctx.restore()


def _part_a(ctx, t):
    k = pop(t, 0.2, 0.6)
    if k > 0:
        shrink = smooth(prog(t, 3.0, 3.8))
        with at(ctx, lerp(XA + 40, XA - 80, shrink), 430, k * lerp(1.45, 1.0, shrink), math.sin(t * 1.2) * 0.02):
            _blueprint(ctx, 0, 0, 460, 320, 1.0, t)
            text(ctx, "芯片设计图", 0, 205, 30, "#CFE8FF", 1, "black")
            if 1.6 < t < 3.4:
                q = pop(t, 1.7, 0.5) * (1 - smooth(prog(t, 3.0, 3.4)))
                with at(ctx, 0, -240, q):
                    rrect(ctx, -120, -40, 240, 80, 40)
                    fill(ctx, "#FFFFFF", 0.95)
                    text(ctx, "谁来造？", 0, 0, 40, "#1F4E8C", 1, "black")
    f = smooth(prog(t, 3.2, 4.0))
    if f > 0:
        y = G + (1 - ease_out(f)) * 300
        ctx.save()
        ctx.rectangle(XA + 180, 0, 900, G)
        ctx.clip()
        factory(ctx, XA + 600, y, 680, 460, 1.0, t, "台积电", "#E9E4F2", TSMC)
        ctx.restore()
        sparkle_burst(ctx, t, 3.9, XA + 600, G - 300, 12, 360, "#FFD9D9", 0.9, 7, 20)


def _part_b(ctx, t):
    a = smooth(prog(t, 4.8, 5.4))
    if a <= 0:
        return
    # 年份
    k = pop(t, 5.2, 0.5)
    if k > 0:
        with at(ctx, XB - 110, 200, k):
            text(ctx, "1987", 0, 0, 120, "#FFFFFF", a, "black")
    # 美国 → 台湾 的小航线（与后面的太平洋地图同向：台湾在左，美国在右）
    p0, p1 = (XB + 470, 600), (XB - 600, 600)
    for (x, y), lab, sub, c in ((p0, "美国", "德州仪器 · 二十多年", "#4C8DFF"), (p1, "台湾", "新竹 · 创办台积电", TSMC)):
        q = pop(t, 5.6 if x > XB else 8.4, 0.5)
        if q > 0:
            with at(ctx, x, y, q):
                circle(ctx, 0, 0, 22)
                fill(ctx, c, a)
                circle(ctx, 0, 0, 10)
                fill(ctx, "#FFFFFF", a)
            name_card(ctx, lab, x, y + 90, c, 34, a, q, sub=sub)
    u = prog(t, 6.4, 8.6)
    if u > 0:
        pts = arc_pts(p0, p1, 0.32)
        stroke_pts(ctx, polyline_partial(pts, 0, ease_io(u)), 5, "#FFD36B", 0.8 * a)
        if u < 1:
            (px, py), ang = point_on(pts, ease_io(u))
            ic_plane(ctx, px, py, 90, a, t, "#FFFFFF", ang)
    # "只代工、不设计"
    s = pop(t, 10.4, 0.55)
    if s > 0:
        with at(ctx, XB - 110, 345, s, -0.06):
            glow(ctx, 0, 0, 260, TSMC, 0.35)
            rrect(ctx, -230, -62, 460, 124, 24)
            fill(ctx, TSMC)
            text(ctx, "只代工、不设计", 0, 0, 52, "#FFFFFF", 1, "black")


FABLESS = [("英伟达", "#76B900"), ("AMD", "#ED1C24"), ("苹果", "#A3AAAE"), ("博通", "#CC092F"), ("高通", "#3253DC")]


def _part_c(ctx, t):
    a = smooth(prog(t, 12.9, 13.5))
    if a <= 0:
        return
    factory(ctx, XC + 160, G, 560, 420, a, t, "台积电", "#E9E4F2", TSMC)
    for i, (nm, c) in enumerate(FABLESS):
        q = pop(t, 13.6 + i * 0.18, 0.45)
        if q <= 0:
            continue
        y = 220 + i * 110
        name_card(ctx, nm, XC - 560, y, c, 30, a, q, w=210)
        # 设计图像纸飞机一样飞向工厂
        u = prog(t, 14.4 + i * 0.25, 15.6 + i * 0.25)
        if 0 < u < 1:
            pts = arc_pts((XC - 450, y), (XC + 40, G - 300), 0.18)
            (px, py), ang = point_on(pts, ease_io(u))
            with at(ctx, px, py, 0.32, ang):
                _blueprint(ctx, 0, 0, 200, 140, a, t)
    # 晶圆出炉
    for i in range(3):
        q = pop(t, 15.8 + i * 0.4, 0.5)
        if q > 0:
            wafer(ctx, XC + 560 + i * 34, 520 - i * 150, 64 * q, a, t, 0.4, lit=0.6)
    tag(ctx, "设计（Fabless） + 代工（Foundry）", XC + 40, 140, 30, "#FFFFFF", "#4A4458", a * smooth(prog(t, 15.0, 15.4)))


def _part_d(ctx, t):
    a = smooth(prog(t, 17.9, 18.5))
    if a <= 0:
        return
    # 先进封装：中介层 + GPU 裸片 + 两侧 HBM
    cx, cy = XD - 140, 520
    s1 = smooth(prog(t, 18.8, 19.4))
    if s1 > 0:
        rrect(ctx, cx - 330, cy + 40, 660, 40, 8)
        fill(ctx, "#4E5A6E", a * s1)
        rrect(ctx, cx - 360, cy + 80, 720, 50, 10)
        fill(ctx, "#2E7D4F", a * s1)
        text(ctx, "中介层 + 基板", cx, cy + 105, 24, "#FFFFFF", a * s1, "bold")
    u = prog(t, 19.4, 20.2)
    if u > 0:
        yy = lerp(cy - 400, cy - 90, ease_back(u, 1.2))
        rrect(ctx, cx - 140, yy, 280, 130, 10)
        ctx.set_source(lin(0, yy, 0, yy + 130, [(0, "#9FE870", a), (1, "#4E9A2A", a)]))
        ctx.fill()
        text(ctx, "GPU", cx, yy + 65, 44, "#FFFFFF", a, "black")
    for side in (-1, 1):
        for j in range(2):
            st = 20.3 + j * 0.25 + (0.12 if side > 0 else 0)
            q = clamp((t - st) / 0.5)
            if q > 0:
                hx = cx + side * (205 + j * 90)
                hbm_stack(ctx, hx, cy + 40, 70, 150, 8, a, "#5B7CFA", q)
    if t > 20.3:
        tag(ctx, "高带宽内存 HBM", cx + 260, cy - 190, 26, "#FFFFFF", "#3E5BD8", a * smooth(prog(t, 20.6, 21.0)))
        tag(ctx, "先进封装（如台积电 CoWoS）", cx, cy - 330, 30, "#FFFFFF", TSMC, a * smooth(prog(t, 21.0, 21.4)))
    # 测试
    tst = smooth(prog(t, 22.6, 23.0))
    if tst > 0:
        tx = XD + 470
        for i in range(3):
            q = pop(t, 22.8 + i * 0.3, 0.4)
            if q <= 0:
                continue
            with at(ctx, tx, 300 + i * 170, q):
                chip_pkg(ctx, 0, 0, 120, "", "", "#76B900", a, 0.2, t)
                for k in range(4):
                    line(ctx, -60 + k * 40, -110, -40 + k * 30, -64, 4, "#C9CED8", a)
                check_mark(ctx, 110, 0, 60, "#3CCB7F", clamp((t - 23.2 - i * 0.3) / 0.3), a)
        tag(ctx, "测试（如日月光）", tx, 160, 28, "#FFFFFF", "#4A4458", a * tst)
    # 组装成服务器
    sv = smooth(prog(t, 24.4, 24.9))
    if sv > 0:
        sx = XD + 800
        server_rack(ctx, sx, G - 10, 210, 560, t, a * sv, 9, "#7CFFB2", seed=4)
        tag(ctx, "组装成服务器（如鸿海、广达）", sx - 60, 270, 28, "#FFFFFF", "#4A4458", a * sv)


def _map_part(ctx, t):
    a = smooth(prog(t, 26.8, 27.6))
    if a <= 0:
        return
    hi = {}
    focus = smooth(prog(t, 34.8, 35.6))
    world_dots(ctx, MAP, a, "#7FB6E8", 0.42, 3.0,
               hi={(121.0, 23.7, 3.2): "#FF6B5B", (-108.0, 36.0, 9.0 if focus > 0 else 3.5): "#4C8DFF",
                   (127.5, 36.5, 2.6 if focus > 0 else 0.1): "#B7A6FF",
                   (5.5, 51.4, 4.0 if focus > 0 else 0.1): "#FFC857"})
    tw = MAP.xy(*LOC["taiwan"])
    az = MAP.xy(*LOC["arizona"])
    # 亚利桑那：第一片美国造 Blackwell 晶圆
    k = pop(t, 28.0, 0.5)
    if k > 0 and t < 35.4:
        map_pin(ctx, az[0], az[1], "#4C8DFF", "亚利桑那 · 台积电工厂", a * (1 - focus), k, 20, t=t, below=True)
    w = smooth(prog(t, 28.6, 29.2))
    fly = prog(t, 31.6, 33.6)
    if w > 0 and t < 34.8:
        pts = arc_pts((az[0], az[1] - 16), (tw[0], tw[1] - 10), 0.28)
        if fly <= 0:
            px, py = az[0] - 2, az[1] - 46
        else:
            (px, py), _ = point_on(pts, ease_io(fly))
            stroke_pts(ctx, polyline_partial(pts, 0, ease_io(fly)), 2.2, "#FFD36B", 0.8 * a)
        wafer(ctx, px, py, 16 * w, a, t, 0.6, lit=0.7)
        if fly > 0 and fly < 1:
            (qx, qy), ang = point_on(pts, min(1, ease_io(fly) + 0.04))
            ic_plane(ctx, qx, qy - 12, 26, a, t, "#FFFFFF", ang)
        tag(ctx, "2025.10 · 第一片美国造 Blackwell 晶圆", az[0] - 30, az[1] - 96, 20, "#FFFFFF", "#2B2233",
            a * w * (1 - smooth(prog(t, 31.4, 31.8))))
    k2 = pop(t, 32.6, 0.5)
    if k2 > 0 and t < 35.4:
        map_pin(ctx, tw[0], tw[1], "#FF6B5B", "台湾 · 先进封装", a * (1 - focus), k2, 20, t=t, below=True)
    # 接力：美国设计 → 台湾制造；荷兰光刻机、韩国内存
    if focus > 0:
        nodes = [("valley", "美国：设计", "#4C8DFF", "英伟达 · AMD · 博通 · Marvell"),
                 ("taiwan", "台湾：制造 · 封测 · 组装", "#FF6B5B", "台积电 · 日月光 · 鸿海 · 广达"),
                 ("nl", "荷兰：光刻机", "#FFC857", "ASML"),
                 ("korea", "韩国：内存", "#B7A6FF", "SK 海力士 · 三星")]
        for i, (key, lab, c, sub) in enumerate(nodes):
            q = pop(t, 35.2 + i * 0.5, 0.5)
            if q <= 0:
                continue
            x, y = MAP.xy(*LOC[key])
            map_pin(ctx, x, y, c, "", a, q, t=t)
            dy = {"valley": -150, "taiwan": 120, "nl": -150, "korea": -170}[key]
            dx = {"valley": 40, "taiwan": -60, "nl": 60, "korea": 40}[key]
            with at(ctx, x + dx, y + dy, q):
                tw_ = max(text_w(ctx, lab, 34, "black"), text_w(ctx, sub, 25, "bold")) + 44
                rrect(ctx, -tw_ / 2, -50, tw_, 100, 24)
                fill(ctx, "#1A1426", 0.85 * a)
                text(ctx, lab, 0, -16, 34, c, a, "black")
                text(ctx, sub, 0, 25, 25, "#FFFFFF", 0.9 * a, "bold")
        # 接力路线：硅谷 → 台湾，荷兰 → 台湾，韩国 → 台湾
        for i, (src, dst, c, st) in enumerate((("valley", "taiwan", "#FFD36B", 36.0), ("nl", "taiwan", "#FFC857", 36.8),
                                                ("korea", "taiwan", "#B7A6FF", 37.4), ("taiwan", "valley", "#7FE7FF", 38.2))):
            u = prog(t, st, st + 1.4)
            if u <= 0:
                continue
            p0, p1 = MAP.xy(*LOC[src]), MAP.xy(*LOC[dst])
            bend = 0.2 if src != "nl" else -0.12
            pts = arc_pts(p0, p1, bend)
            stroke_pts(ctx, polyline_partial(pts, 0, ease_io(u)), 5, c, 0.85 * a)
            if u < 1:
                (px, py), ang = point_on(pts, ease_io(u))
                with at(ctx, px, py, 0.42, ang):
                    draw_prop(ctx, ("baton",), t)
        ttl = pop(t, 39.0, 0.6)
        if ttl > 0:
            with at(ctx, XM, 150, ttl):
                glow(ctx, 0, 0, 380, "#FFB27A", 0.35)
                rrect(ctx, -330, -58, 660, 116, 58)
                fill(ctx, "#FF9F68")
                text(ctx, "跨越太平洋的接力赛", 0, 0, 54, "#FFFFFF", 1, "black")


def draw(ctx, t):
    cam = CAM.at(t)
    _bg(ctx, t, cam)
    with view(ctx, cam, 1.0):
        _part_a(ctx, t)
        _part_b(ctx, t)
        _part_c(ctx, t)
        _part_d(ctx, t)
        _map_part(ctx, t)
        P.draw(ctx, t)


def sfx():
    return [
        (0.4, "paper", {"gain": 0.35}),
        (2.2, "think", {"dur": 1.0, "gain": 0.25}),
        (3.15, "pop_big", {"gain": 0.35}), (3.2, "rumble", {"dur": 0.8, "gain": 0.35}),
        (3.9, "shimmer", {"dur": 1.0, "gain": 0.3}),
        (4.6, "whoosh_short", {"gain": 0.3}),
        (5.2, "impact_soft", {"gain": 0.35}),
        (6.4, "whoosh", {"dur": 2.2, "gain": 0.3}),
        (10.4, "stamp", {"gain": 0.45}),
        (12.7, "whoosh_short", {"gain": 0.3}),
        (14.4, "swish", {"gain": 0.22}), (14.65, "swish", {"gain": 0.22}), (14.9, "swish", {"gain": 0.22}),
        (15.8, "pop", {"gain": 0.3}), (16.2, "pop", {"gain": 0.3, "pitch": 1.2}), (16.6, "pop", {"gain": 0.3, "pitch": 1.4}),
        (17.7, "whoosh_short", {"gain": 0.3}),
        (18.8, "slide", {"gain": 0.3}), (20.0, "clunk", {"gain": 0.35}),
        (20.4, "click", {"gain": 0.3}), (20.65, "click", {"gain": 0.3}), (20.9, "click", {"gain": 0.3}),
        (23.2, "check", {"gain": 0.3}), (23.5, "check", {"gain": 0.3, "pitch": 1.1}),
        (23.8, "check", {"gain": 0.3, "pitch": 1.2}),
        (24.4, "slide", {"gain": 0.3}), (24.6, "fan", {"dur": 2.0, "gain": 0.12}),
        (26.9, "whoosh", {"dur": 1.0, "gain": 0.35}),
        (28.0, "pin", {"gain": 0.35}), (28.6, "shimmer", {"dur": 1.0, "gain": 0.3}),
        (31.6, "whoosh", {"dur": 2.0, "gain": 0.3}),
        (32.6, "pin", {"gain": 0.35}),
        (34.6, "zoom_in", {"dur": 1.0, "gain": 0.25}),
        (35.2, "pin", {"gain": 0.3}), (35.7, "pin", {"gain": 0.3}), (36.2, "pin", {"gain": 0.3}),
        (36.7, "pin", {"gain": 0.3}),
        (36.0, "stream", {"dur": 3.4, "gain": 0.18}),
        (39.0, "impact_soft", {"gain": 0.45}), (39.05, "shimmer", {"dur": 1.6, "gain": 0.35}),
    ]
