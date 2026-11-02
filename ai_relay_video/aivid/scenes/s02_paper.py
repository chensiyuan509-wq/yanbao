"""01 · 一篇论文：2017 年谷歌八位研究员的 Transformer；排队过安检 vs 一眼看全；天生适合并行。"""
import math

from ..core import (TAU, Cam, at, circle, clamp, curve_arrow, ease_back, ease_in, ease_io, ease_out,
                    ease_out5, fill, glow, kf, lerp, lin, line, pop, prog, rad, ring_burst, rrect, setc,
                    smooth, sparkle_burst, star4, stroke_pts, text, text_w, view, bezier_pts)
from ..icons import ic_brain
from ..props import bg_grad, chip_pkg, grid_lines, tag
from .common import host, talk_lines

DUR = 28.5
CHAPTER = ("01", "一篇论文")

VO = [
    (0.8, '故事要从 {2017 年}说起。'),
    (3.1, '谷歌的八位研究员发表了一篇论文：《注意力就是你所需要的一切》，提出了一种新架构——{Transformer}。'),
    (10.4, '以前的模型读句子，像过安检，只能一个字一个字地排队；'),
    (15.2, 'Transformer 让每个字同时看向所有字，谁和谁关系近，{一眼}就知道。'),
    (21.0, '更妙的是，它天生适合{并行计算}：显卡越多，模型就能做得越大。'),
]

PX, PY = 1180, 560              # 论文中心
BX = 3200                       # 第二段舞台中心 x
TOK = ["小猫", "追着", "它的", "尾巴", "转圈"]
TOK_C = ["#FF9F68", "#8B6CFF", "#2EC4B6", "#4C8DFF", "#FF6B9A"]
AUTH = ["A.V.", "N.S.", "N.P.", "J.U.", "L.J.", "A.G.", "L.K.", "I.P."]

P = (host(480, 930, 0.62, "curious", seed=2.2, hat="grad")
     .look(0, 0.4, -0.8)
     .expr(3.3, "awe").look(3.3, 1.0, -0.4)
     .expr(7.9, "starry").hop(8.6, 45, 0.4)
     # 去第二段舞台
     .expr(9.7, "smile").walk_to(9.75, 10.9, BX - 760, 930, 1.2)
     .expr(11.6, "sleepy").look(11.6, 0.8, -0.2)
     .sigh(13.4, 1.2)
     .expr(15.2, "surprised").look(15.2, 0.8, -0.5)
     .expr(17.0, "awe")
     .expr(19.2, "excited").hop(19.25, 40, 0.38)
     .expr(21.2, "smile").look(21.2, 0.9, 0.2)
     .expr(24.0, "starry").look(24.0, 0.8, -0.7)
     .jump(25.0, 110, 0.7))
talk_lines(P, VO, [0, 4], smile=0.3)

CAM = Cam([
    (0.0, (960, 540, 1.08)),
    (2.6, (1000, 545, 1.0)),
    (8.3, (1060, 540, 1.04)),
    (10.6, (BX - 120, 540, 1.0), ease_io),
    (14.8, (BX - 100, 540, 1.02)),
    (15.6, (BX - 40, 520, 1.06), ease_io),
    (20.6, (BX - 20, 520, 1.08)),
    (21.6, (BX - 60, 520, 0.96), ease_io),
    (26.3, (BX - 40, 500, 1.0)),
    (28.5, (BX + 60, 470, 1.18), ease_in),
], drift=5, seed=5.0)


def _bg(ctx, t, cam):
    bg_grad(ctx, "#FFF6E8", "#F4DFC8")
    with view(ctx, cam, 0.6):
        grid_lines(ctx, -800, -400, 5200, 1600, 80, "#C9A27E", 0.12)
    ctx.set_source(rad(960, 540, 300, 1100, [(0, "#FFFFFF", 0), (1, "#C98F6A", 0.22)]))
    ctx.paint()


def _year(ctx, t):
    """2012 → 2017 的翻页数字。"""
    a = smooth(prog(t, 0.2, 0.6)) * (1 - smooth(prog(t, 3.0, 3.6)))
    if a <= 0:
        return
    x, y = PX, PY - 40
    v = 2012 + 5 * ease_out5(prog(t, 0.6, 2.2))
    yr = int(v)
    frac = v - yr
    ctx.save()
    rrect(ctx, x - 300, y - 120, 600, 240, 40)
    ctx.clip()
    for k, dy in ((yr, -frac), (yr + 1, 1 - frac)):
        if k > 2017:
            continue
        text(ctx, str(k), x, y + dy * 230, 210, "#2B2233", a * (1 - abs(dy)) ** 0.5, "black")
    ctx.restore()
    ring_burst(ctx, t, 2.25, x, y, 60, 320, "#FF9F68", 0.9, 8)


def _paper(ctx, t):
    k = ease_out5(prog(t, 3.0, 3.8))
    if k <= 0:
        return
    w, h = 720, 860
    x0 = PX - w / 2
    y0 = PY - h / 2 + (1 - k) * 700
    ctx.save()
    ctx.translate(PX, y0 + h / 2)
    ctx.rotate((1 - k) * 0.2 - 0.025)
    ctx.translate(-PX, -(y0 + h / 2))
    from ..core import box_shadow
    box_shadow(ctx, x0, y0, w, h, 10, blur=36, a=0.25, dy=16)
    rrect(ctx, x0, y0, w, h, 10)
    fill(ctx, "#FFFFFF")
    text(ctx, "Google · 2017", PX, y0 + 52, 24, "#9A8FA8", 1, "bold")
    text(ctx, "Attention Is All You Need", PX, y0 + 112, 44, "#1E1A26", 1, "serif")
    # 八位作者
    for i, au in enumerate(AUTH):
        q = pop(t, 4.0 + i * 0.12, 0.4)
        if q <= 0:
            continue
        ax = PX - 287 + i * 82
        with at(ctx, ax, y0 + 190, q):
            circle(ctx, 0, 0, 30)
            fill(ctx, ["#FFB27A", "#B7A6FF", "#7FE0D4", "#9CC2FF"][i % 4])
            text(ctx, au, 0, 1, 17, "#2B2233", 1, "black")
    text(ctx, "八位作者", PX, y0 + 242, 20, "#9A8FA8", smooth(prog(t, 4.9, 5.4)), "bold")
    # Transformer 结构示意
    bx, by = PX, y0 + 300
    d = clamp((t - 5.4) / 2.4)
    blocks = [("输入的每个词", "#E9E4F2", 0.0), ("多头注意力", "#FFD9B8", 0.25), ("前馈网络", "#CFE6FF", 0.5),
              ("输出下一个词", "#E9E4F2", 0.75)]
    for i, (lab, c, st) in enumerate(blocks):
        q = ease_out(clamp((d - st) / 0.25))
        if q <= 0:
            continue
        yy = by + 470 - i * 135
        rrect(ctx, bx - 190, yy - 42, 380 * q, 84, 16)
        fill(ctx, c)
        text(ctx, lab, bx, yy, 30, "#2B2233", q, "black")
        if i < 3 and q > 0.8:
            from ..core import arrow
            arrow(ctx, bx, yy - 46, bx, yy - 88, 5, "#9A8FA8", 1.0)
    if d > 0.5:
        q = smooth((d - 0.5) / 0.3)
        rrect(ctx, bx + 210, by + 155, 16, 290, 8)
        fill(ctx, "#FF9F68", q)
        text(ctx, "× N", bx + 262, by + 300, 30, "#FF9F68", q, "black")
    ctx.restore()
    # "Transformer" 标题印章
    s = pop(t, 8.4, 0.5)
    if s > 0:
        a = 1 - smooth(prog(t, 9.8, 10.4))
        with at(ctx, PX, PY + 300, s, -0.06):
            glow(ctx, 0, 0, 360, "#FFB27A", 0.4 * a)
            rrect(ctx, -270, -62, 540, 124, 30)
            fill(ctx, "#2B2233", 0.92 * a)
            text(ctx, "Transformer", 0, 0, 74, "#FFC08A", a, "black")
        sparkle_burst(ctx, t, 8.45, PX, PY + 300, 10, 340, "#FFC57A", 0.9, 9, 22)


GATE = BX - 120
SP = 160


def _queue_xy(i, t):
    """排队过安检：没轮到的在闸门左边排队，轮到的跳过闸门，按原顺序排到右边。"""
    n_done = sum(1 for k in range(5) if t >= 11.3 + k * 0.75 + 0.75)
    t0 = 11.3 + i * 0.75
    u = clamp((t - t0) / 0.75)
    if u <= 0:
        waiting_rank = i - min(i, n_done)
        return GATE - 200 - waiting_rank * SP, 640
    x = lerp(GATE - 200, GATE + 200 + i * SP, ease_io(u))
    return x, 640 - math.sin(u * math.pi) * (40 + i * 12)


def _tokens(ctx, t):
    a_in = smooth(prog(t, 10.4, 10.9))
    if a_in <= 0:
        return
    queue = 1 - smooth(prog(t, 14.8, 15.5))
    att = smooth(prog(t, 14.9, 15.6))
    par = smooth(prog(t, 21.0, 21.6))
    if queue > 0.01:
        ga = a_in * queue
        rrect(ctx, GATE - 70, 470, 22, 230, 8)
        fill(ctx, "#6B6377", ga)
        rrect(ctx, GATE + 48, 470, 22, 230, 8)
        fill(ctx, "#6B6377", ga)
        rrect(ctx, GATE - 80, 450, 160, 34, 12)
        fill(ctx, "#4A4458", ga)
        busy = any(0 < (t - (11.3 + i * 0.75)) < 0.75 for i in range(5))
        circle(ctx, GATE, 467, 9)
        fill(ctx, "#FF5A5F" if busy else "#3CCB7F", ga)
        tag(ctx, "一个一个来", GATE, 400, 28, "#FFFFFF", "#6B6377", ga, 0.95)
        n = sum(1 for i in range(5) if t > 11.3 + i * 0.75 + 0.75)
        text(ctx, f"已处理 {n}/5", GATE, 770, 28, "#6B6377", ga, "bold")
    row_x = [BX - 420 + i * 210 for i in range(5)]
    for i, w in enumerate(TOK):
        qx, qy = _queue_xy(i, t)
        x, y = lerp(qx, row_x[i], att), lerp(qy, 600, att)
        if par > 0:
            gx, gy = _gpu_slot(i)
            dropu = clamp((t - 21.6) / 0.7)
            x = lerp(x, gx, ease_in(dropu))
            y = lerp(y, gy - 70, ease_in(dropu))
            if dropu >= 1:
                continue
        _token(ctx, x, y, w, TOK_C[i], a_in, hi=(i in (0, 2)) and 18.6 < t < 21.6)


def _token(ctx, x, y, w, c, a, hi=False):
    if hi:
        glow(ctx, x, y, 110, c, 0.5 * a)
    rrect(ctx, x - 75, y - 40, 150, 80, 22)
    fill(ctx, "#FFFFFF", a)
    rrect(ctx, x - 75, y - 40, 150, 80, 22)
    ctx.set_line_width(5)
    setc(ctx, c, a)
    ctx.stroke()
    text(ctx, w, x, y, 40, "#2B2233", a, "black")


def _attention(ctx, t):
    a = smooth(prog(t, 15.4, 15.9)) * (1 - smooth(prog(t, 21.0, 21.5)))
    if a <= 0:
        return
    xs = [BX - 420 + i * 210 for i in range(5)]
    y = 600
    pairs = [(i, j) for i in range(5) for j in range(i + 1, 5)]
    for k, (i, j) in enumerate(pairs):
        st = 15.6 + k * 0.06
        q = ease_out(clamp((t - st) / 0.6))
        if q <= 0:
            continue
        x0, x1 = xs[i], xs[j]
        hgt = 70 + (j - i) * 62
        strong = (i, j) == (0, 2)
        boost = smooth(prog(t, 18.6, 19.2)) if strong else 0
        dim = 1 - 0.55 * smooth(prog(t, 18.6, 19.2)) if not strong else 1
        pts = bezier_pts((x0, y - 46), (x0, y - 46 - hgt), (x1, y - 46 - hgt), (x1, y - 46), 40)
        from ..core import polyline_partial
        seg = polyline_partial(pts, 0, q)
        stroke_pts(ctx, seg, 4 + 10 * boost, "#FF9F68" if strong and boost > 0 else "#8B6CFF",
                   a * (0.55 + 0.45 * boost) * dim)
        if strong and boost > 0:
            mx = (x0 + x1) / 2
            glow(ctx, mx, y - 46 - hgt * 0.75, 90, "#FFB27A", 0.5 * boost * a)
            tag(ctx, "「它的」指的是「小猫」", mx, y - 46 - hgt * 0.75 - 56, 30, "#FFFFFF", "#FF9F68", a * boost)
    # 每个词同时"看向"所有词的小光点
    if t < 18.6:
        for i in range(5):
            for j in range(5):
                if i == j:
                    continue
                ph = ((t - 15.6) * 0.9 + (i * 5 + j) * 0.137) % 1
                x = lerp(xs[i], xs[j], ph)
                yy = y - 46 - math.sin(ph * math.pi) * (70 + abs(j - i) * 62) * 0.75
                circle(ctx, x, yy, 5)
                fill(ctx, "#FFFFFF", 0.7 * a * smooth(prog(t, 15.8, 16.3)))
    tag(ctx, "所有词同时互相「看」", BX - 0, 200, 32, "#FFFFFF", "#8B6CFF", a * (1 - smooth(prog(t, 18.4, 18.8))))


def _gpu_slot(i):
    cols = 5
    return BX - 440 + (i % cols) * 220, 790


def _parallel(ctx, t):
    a = smooth(prog(t, 21.1, 21.6))
    if a <= 0:
        return
    grow = smooth(prog(t, 23.6, 25.6))
    # 显卡：先 5 块，再扩成 3 排 × 9 块
    n1 = 5
    for i in range(n1):
        gx, gy = _gpu_slot(i)
        lit = smooth(prog(t, 22.2, 22.5))
        sx = lerp(1.0, 0.62, grow)
        with at(ctx, lerp(gx, BX - 560 + i * 140, grow), lerp(gy, 800, grow), sx):
            chip_pkg(ctx, 0, 0, 150, "GPU", "", "#76B900", a, 0.5 * lit, t)
    if grow > 0:
        for r in range(2):
            for c in range(9):
                st = 23.8 + (r * 9 + c) * 0.04
                q = pop(t, st, 0.35)
                if q <= 0 or (r == 0 and c < 5):
                    continue
                gx = BX - 560 + c * 140
                gy = 800 if r == 0 else 690
                with at(ctx, gx, gy, 0.62 * q):
                    chip_pkg(ctx, 0, 0, 150, "GPU", "", "#76B900", a, 0.4, t)
    # 并行的光束：每个词同时进入一块显卡
    if 21.5 < t < 22.6:
        for i in range(5):
            gx, gy = _gpu_slot(i)
            ring_burst(ctx, t, 22.25, gx, gy, 20, 120, "#B6FF6B", 0.5, 6, 0.8)
    # 模型越来越大
    m = smooth(prog(t, 22.6, 23.2))
    if m > 0:
        r = lerp(60, 165, grow) * m
        bx, by = BX + 0, 330 - 30 * grow
        glow(ctx, bx, by, r * 2.2, "#8B6CFF", 0.35 * m)
        ic_brain(ctx, bx, by, r * 2, m, t, "#8B6CFF", 0.5)
        tag(ctx, "模型越来越大", bx, by - r - 46, 30, "#FFFFFF", "#8B6CFF", m)
    lab = smooth(prog(t, 22.4, 22.9))
    if lab > 0:
        n = int(lerp(5, 23, grow))
        tag(ctx, f"显卡 × {n}", BX - 760, 790 - 40 * grow, 30, "#FFFFFF", "#3C9D4A", lab * a)
        tag(ctx, "同时开工", BX + 640, 790, 30, "#FFFFFF", "#3C9D4A", lab * a * (1 - grow))


def draw(ctx, t):
    cam = CAM.at(t)
    _bg(ctx, t, cam)
    with view(ctx, cam, 1.0):
        _year(ctx, t)
        _paper(ctx, t)
        _tokens(ctx, t)
        _attention(ctx, t)
        _parallel(ctx, t)
        P.draw(ctx, t)


def sfx():
    return [
        (0.6, "shuffle", {"dur": 1.6, "gain": 0.3}),
        (2.25, "pop_big", {"gain": 0.4}),
        (3.0, "paper", {"gain": 0.45}),
        (4.0, "pop", {"gain": 0.25, "pitch": 1.1}), (4.36, "pop", {"gain": 0.25, "pitch": 1.25}),
        (4.72, "pop", {"gain": 0.25, "pitch": 1.4}),
        (5.5, "slide", {"gain": 0.3}), (6.1, "slide", {"gain": 0.25}), (6.7, "slide", {"gain": 0.25}),
        (8.4, "stamp", {"gain": 0.5}), (8.45, "shimmer", {"dur": 1.2, "gain": 0.35}),
        (9.8, "whoosh", {"dur": 0.9, "gain": 0.3}),
        (11.3, "blip", {"gain": 0.25}), (12.05, "blip", {"gain": 0.25}), (12.8, "blip", {"gain": 0.25}),
        (13.55, "blip", {"gain": 0.25}), (14.3, "blip", {"gain": 0.25}),
        (13.4, "womp", {"gain": 0.25}),
        (15.6, "sparkle", {"dur": 2.0, "gain": 0.3}),
        (18.6, "ding", {"gain": 0.4}),
        (21.6, "whoosh_short", {"gain": 0.35}),
        (22.25, "powerup", {"gain": 0.35}),
        (23.8, "spinup", {"dur": 2.4, "gain": 0.3}),
        (25.0, "boing", {"gain": 0.3}),
    ]
