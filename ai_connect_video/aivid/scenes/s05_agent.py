"""第二章 · 什么是 Agent 智能体。

A 大脑 + 工具 = 智能体（工具飞来环绕小橙）
B 拆解任务 → 调用工具 → 检查结果 的循环
C 订机票：查航班 → 比价格 → 填信息 → 付款前找你确认
"""
import math

from ..core import (TAU, W, H, Cam, at, check_mark, circle, clamp, ease_back, ease_in, ease_io,
                    ease_io5, ease_out, fill, glow, kf, lerp, line, lin, pop, prog, rrect, setc,
                    smooth, text, text_w, view, sparkle_burst, ring_burst, arrow_head, dashed,
                    bezier_pts, point_on, stroke_pts)
from ..icons import (ic_brain, ic_browser, ic_calendar, ic_code, ic_folder, ic_mail, ic_terminal,
                     ic_plane)
from ..mascot import Puppet
from ..ui import bubble, button, card, checkbox, pill, progress, window, typing_dots
from .common import light_bg

DUR = 21.0
CHAPTER = ("02", "什么是 Agent 智能体")

SUBS = [
    (0.8, 5.9, "{Agent}（智能体）＝ 大模型大脑 ＋ 能动手的工具。"),
    (6.1, 11.4, "它会{拆解任务}、{调用工具}、{检查结果}，直到把事办完。"),
    (11.6, 15.4, "比如你说：「帮我订周五去上海的机票。」"),
    (15.6, 20.7, "它会查航班、比价格、填信息，{付款前再找你确认}。"),
]

MX, MY = 1460, 610                 # A/B 段小橙位置
BRAIN = (300, 410)
TOOLS = [ic_browser, ic_terminal, ic_folder, ic_mail, ic_calendar, ic_code]
TOOL_C = (830, 410)
T_TOOL = [1.5 + i * 0.15 for i in range(6)]
T_FLY = 3.2                        # 工具飞向小橙
T_POWER = 4.3

LOOP_C = (MX, 470)
LOOP_R = 330
NODES = [(-90, "拆解任务", "#8B6CFF"), (30, "调用工具", "#2EC4B6"), (150, "检查结果", "#FF9F68")]
T_LOOP0, LOOP_PERIOD, LOOPS = 6.7, 1.9, 2

# C 段（右侧世界区域）
CX0 = 1920
WIN = (2600, 130, 1150, 790)       # 浏览器窗口 x, y, w, h
CHK = (1975, 265, 540, 410)        # 步骤清单
T_REQ = 11.7
T_STEPS = [16.3, 17.5, 18.8, 20.5]
T_CLICK = 20.25

P = (Puppet(MX, MY, 0.92, "curious", seed=5.5)
     .look(0, -1.0, -0.5)
     .expr(T_FLY, "surprised").look(T_FLY, -0.6, -0.3)
     .expr(T_POWER, "determined").bar(T_POWER, "fists").hop(T_POWER, 50)
     .bar(5.6, None).expr(5.6, "smile")
     .expr(6.6, "think")
     .expr(10.7, "happy")
     .move(11.3, 12.6, 2230, 915).scale(11.3, 0.52, 1.3)
     .expr(12.6, "determined").nod(12.7)
     .type(12.9, 18.9)
     .expr(19.0, "curious").look(19.0, 0.0, 0.0).talk(19.2, 19.9)
     .expr(20.5, "excited").hop(20.5, 45).look(20.5, 0.7, -0.3))

CAM = Cam([
    (0.0, (960, 520, 1.0)),
    (5.6, (990, 520, 1.03)),
    (6.6, (MX - 80, 500, 1.04), ease_io),
    (11.2, (MX - 60, 500, 1.07)),
    (12.4, (2880, 520, 1.0), ease_io5),
    (21.0, (2900, 525, 1.03)),
], drift=5, seed=12.0)


def draw(ctx, t):
    light_bg(ctx, "#EEF9F6", "#D3EDE7", dots="#7FBFB2", dot_a=0.16, spacing=66, drift=(-t * 8, 0))
    cam = CAM.at(t)
    with view(ctx, cam, 0.5):
        glow(ctx, 700, 300, 600, "#FFFFFF", 0.5)
        glow(ctx, 2700, 500, 800, "#FFFFFF", 0.4)
    with view(ctx, cam):
        if t < 12.6:
            draw_equation(ctx, t)
        if 5.9 < t < 12.4:
            draw_loop(ctx, t)
        if t > 11.0:
            draw_booking(ctx, t)
        orbit_tools(ctx, t, back=True)
        st = P.state(t)
        look = None
        if T_LOOP0 <= t < T_LOOP0 + LOOP_PERIOD * LOOPS:
            ang = math.radians(-90) + TAU * (t - T_LOOP0) / LOOP_PERIOD
            dx, dy = math.cos(ang), math.sin(ang)
            look = (dx * 0.9, dy * 0.8)
        if look:
            P.draw(ctx, t, look=look)
        else:
            P.draw(ctx, t)
        orbit_tools(ctx, t, back=False)
        # 付款前的确认气泡
        sa = pop(t, 19.15, 0.4) * (1 - smooth(prog(t, 20.4, 20.7)))
        if sa > 0:
            hx, hy = P.head(t)
            with at(ctx, hx + 40, hy - 70, sa):
                bubble(ctx, -10, -66, 300, 84, "#FFFFFF", 1, tail="left", r=28)
                text(ctx, "确认付款吗？", 140, -24, 32, "#2B2233", 1, "black")


# ---------------------------------------------------------------- A：等式

def _lab(ctx, s1, s2, x, y, a):
    text(ctx, s1, x, y, 46, "#21423C", a, "black")
    text(ctx, s2, x, y + 52, 30, "#4E7F75", a, "bold")


def draw_equation(ctx, t):
    fade = 1 - smooth(prog(t, 5.6, 6.3))
    if fade <= 0:
        return
    # 大脑
    fly = ease_io(prog(t, T_FLY, T_FLY + 0.9))
    bk = pop(t, 0.6, 0.5)
    if bk > 0 and fly < 1:
        bx = lerp(BRAIN[0], MX, fly)
        by = lerp(BRAIN[1], MY - 140 * 0.7, fly) - math.sin(fly * math.pi) * 160
        ic_brain(ctx, bx, by, 230 * bk * (1 - 0.75 * fly), 1.0, t, glow_a=0.35)
    la = smooth(prog(t, 0.9, 1.3)) * fade
    _lab(ctx, "大模型", "（大脑）", BRAIN[0], BRAIN[1] + 175, la)
    # + 和 =
    for (tt, s, x) in ((1.2, "+", 560), (2.8, "=", 1120)):
        k = pop(t, tt, 0.4)
        if k > 0:
            with at(ctx, x, 410, k):
                text(ctx, s, 0, 0, 140, "#2E8B7A", fade, "black")
    # 工具
    for i, fn in enumerate(TOOLS):
        k = pop(t, T_TOOL[i], 0.4)
        if k <= 0:
            continue
        gx, gy = TOOL_C[0] + (i % 3 - 1) * 128, TOOL_C[1] + (i // 3 - 0.5) * 128
        u = ease_io(prog(t, T_FLY + i * 0.06, T_FLY + 0.85 + i * 0.06))
        if u >= 1:
            continue
        ox, oy, _, _ = _orbit_pos(t, i)
        x = lerp(gx, ox, u)
        y = lerp(gy, oy, u) - math.sin(u * math.pi) * 120
        fn(ctx, x, y, 112 * k * (1 - 0.5 * u), 1.0, t)
    _lab(ctx, "工具", "（手和脚）", TOOL_C[0], TOOL_C[1] + 175, smooth(prog(t, 2.4, 2.8)) * fade)
    # 结果标签
    rk = pop(t, T_POWER + 0.15, 0.45)
    if rk > 0:
        ring_burst(ctx, t, T_POWER, MX, MY - 130, 40, 360, "#FFD25C", 0.7, 10)
        sparkle_burst(ctx, t, T_POWER, MX, MY - 140, 10, 300, "#FFC65C", 0.9, 4, 22)
        with at(ctx, MX, MY + 80, rk):
            pill(ctx, "智能体 Agent", 0, 0, 46, "#FFFFFF", "#2E8B7A", fade, 1.0, weight="black")


def _orbit_pos(t, i):
    """工具绕小橙旋转的位置 (x, y, 缩放, 是否在后面)。"""
    ang = t * 1.1 + i * TAU / 6
    st = P.state(t)
    cx, cy = st["x"], st["y"] - 120 * st["s"]
    rx, ry = 260 * st["s"] / 0.92, 66 * st["s"] / 0.92
    x, y = cx + math.cos(ang) * rx, cy + math.sin(ang) * ry
    depth = math.sin(ang)
    return x, y, 0.75 + 0.25 * depth, depth < 0


def orbit_tools(ctx, t, back):
    if t < T_FLY + 0.85:
        return
    a = smooth(prog(t, T_FLY + 0.8, T_FLY + 1.0)) * (1 - smooth(prog(t, 12.4, 12.9)))
    if a <= 0:
        return
    st = P.state(t)
    for i, fn in enumerate(TOOLS):
        x, y, k, is_back = _orbit_pos(t, i)
        if is_back != back:
            continue
        fn(ctx, x, y, 66 * k * st["s"] / 0.92, a * (0.65 + 0.35 * k), t)


# ---------------------------------------------------------------- B：循环

def draw_loop(ctx, t):
    a = smooth(prog(t, 6.0, 6.5)) * (1 - smooth(prog(t, 11.4, 12.0)))
    if a <= 0:
        return
    cx, cy = LOOP_C
    draw_p = ease_out(prog(t, 6.0, 6.9))
    # 圆环（分三段箭头）
    for k in range(3):
        a0 = math.radians(NODES[k][0]) + 0.32
        a1 = math.radians(NODES[(k + 1) % 3][0]) - 0.32
        if a1 < a0:
            a1 += TAU
        pts = [(cx + math.cos(lerp(a0, a1, u / 30)) * LOOP_R, cy + math.sin(lerp(a0, a1, u / 30)) * LOOP_R)
               for u in range(31)]
        from ..core import polyline_partial
        seg = polyline_partial(pts, draw_p)
        stroke_pts(ctx, seg, 7, "#2E8B7A", 0.35 * a)
        if draw_p > 0.95:
            (ex, ey), (px, py) = pts[-1], pts[-2]
            arrow_head(ctx, ex, ey, math.atan2(ey - py, ex - px), 26, "#2E8B7A", 0.6 * a)
    # 流动的光点
    if T_LOOP0 <= t < T_LOOP0 + LOOP_PERIOD * LOOPS:
        u = (t - T_LOOP0) / LOOP_PERIOD
        ang = math.radians(-90) + TAU * u
        x, y = cx + math.cos(ang) * LOOP_R, cy + math.sin(ang) * LOOP_R
        for k in range(8):
            a2 = ang - k * 0.06
            glow(ctx, cx + math.cos(a2) * LOOP_R, cy + math.sin(a2) * LOOP_R, 34 - k * 3, "#FFD25C", 0.5 * a * (1 - k / 8))
        circle(ctx, x, y, 12)
        fill(ctx, "#FFFFFF", a)
    # 出口 → 完成
    ex = prog(t, T_LOOP0 + LOOP_PERIOD * LOOPS, T_LOOP0 + LOOP_PERIOD * LOOPS + 0.6)
    done_x, done_y = cx - 560, cy - 60
    if ex > 0:
        p0 = (cx, cy - LOOP_R)
        pts = bezier_pts(p0, (cx - 260, cy - LOOP_R - 60), (done_x + 120, done_y - 120), (done_x + 70, done_y), 30)
        from ..core import polyline_partial
        seg = polyline_partial(pts, ease_out(ex))
        stroke_pts(ctx, seg, 6, "#3CCB7F", 0.8 * a, dash=(14, 10), offset=-t * 40)
        (gx, gy), _ = point_on(pts, ease_out(ex))
        glow(ctx, gx, gy, 30, "#FFD25C", 0.7 * a * (1 - ex))
    dk = pop(t, T_LOOP0 + LOOP_PERIOD * LOOPS + 0.5, 0.45)
    if dk > 0:
        with at(ctx, done_x, done_y, dk):
            circle(ctx, 0, 0, 62)
            fill(ctx, "#3CCB7F", a)
            check_mark(ctx, 0, 2, 70, "#FFFFFF", prog(t, T_LOOP0 + LOOP_PERIOD * LOOPS + 0.6, T_LOOP0 + LOOP_PERIOD * LOOPS + 0.9), a)
            text(ctx, "办完", 0, 98, 34, "#21423C", a, "black")
    # 节点
    for k, (deg, lab, col) in enumerate(NODES):
        ang = math.radians(deg)
        x, y = cx + math.cos(ang) * LOOP_R, cy + math.sin(ang) * LOOP_R
        nk = pop(t, 6.2 + k * 0.18, 0.45)
        if nk <= 0:
            continue
        hit = 0.0
        if T_LOOP0 <= t < T_LOOP0 + LOOP_PERIOD * LOOPS + 0.3:
            u = (t - T_LOOP0) / LOOP_PERIOD
            pos = ((deg + 90) / 360.0)
            d = (u - pos) % 1.0
            if d < 0.12 and u >= pos - 0.001:
                hit = 1 - d / 0.12
        with at(ctx, x, y, nk * (1 + 0.12 * hit)):
            glow(ctx, 0, 0, 120, col, 0.35 * hit * a)
            w = text_w(ctx, lab, 40, "black") + 64
            rrect(ctx, -w / 2, -38, w, 76, 38)
            fill(ctx, "#FFFFFF", a)
            ctx.set_line_width(4)
            setc(ctx, col, a)
            rrect(ctx, -w / 2, -38, w, 76, 38)
            ctx.stroke()
            text(ctx, lab, 0, 0, 40, col, a, "black")


# ---------------------------------------------------------------- C：订机票

FLIGHTS = [("07:50 → 10:05", "¥1,180"), ("10:30 → 12:40", "¥960"), ("14:15 → 16:25", "¥1,050")]


def draw_booking(ctx, t):
    a = smooth(prog(t, 11.2, 11.8))
    # 用户请求气泡
    rk = pop(t, T_REQ, 0.45)
    if rk > 0:
        with at(ctx, 2060, 175, rk):
            circle(ctx, 0, 0, 44)
            fill(ctx, "#FFB547")
            circle(ctx, 0, -10, 15)
            fill(ctx, "#FFFFFF")
            ctx.new_sub_path()
            ctx.arc(0, 26, 26, math.pi, TAU)
            fill(ctx, "#FFFFFF")
            text(ctx, "你", 0, 70, 24, "#4E7F75", 1, "bold")
            bubble(ctx, 80, -54, 520, 100, "#FFFFFF", 1, tail="left", r=32)
            text(ctx, "帮我订周五去上海的机票", 340, -4, 36, "#2B2233", 1, "black")
    # 步骤清单
    ck = ease_out(prog(t, 12.5, 13.0))
    if ck > 0:
        x, y, w, h = CHK
        dx = (1 - ck) * -60
        card(ctx, x + dx, y, w, h, 30, "#FFFFFF", ck, shadow=0.16)
        text(ctx, "智能体的步骤", x + dx + 36, y + 52, 34, "#2E8B7A", ck, "black", "l")
        items = ["查航班", "比价格", "填信息", "找你确认"]
        for i, s in enumerate(items):
            iy = y + 125 + i * 74
            done = prog(t, T_STEPS[i], T_STEPS[i] + 0.35)
            active = (i == 0 and t > 13.2) or (i > 0 and t > T_STEPS[i - 1])
            if active and done < 1:
                rrect(ctx, x + dx + 18, iy - 30, w - 36, 60, 18)
                fill(ctx, "#E6F6F1", ck)
            checkbox(ctx, x + dx + 60, iy, 40, done, "#3CCB7F", ck)
            text(ctx, f"{i + 1}. {s}", x + dx + 102, iy, 37, "#2B2233" if active else "#9AA7A3", ck, "bold", "l")
            if i == 3 and 19.0 < t < T_STEPS[3]:
                typing_dots(ctx, x + dx + w - 70, iy, t, "#2E8B7A", ck, 7)
    # 浏览器窗口
    wk = ease_back(prog(t, 12.8, 13.35), 1.3)
    if wk <= 0:
        return
    x, y, w, h = WIN
    with at(ctx, x + w / 2, y + h / 2, 0.85 + 0.15 * wk):
        cx0, cy0 = -w / 2, -h / 2
        content = window(ctx, cx0, cy0, w, h, "机票预订", min(1, wk * 1.5))
        bx, by, bw, bh = content
        # 搜索栏
        rrect(ctx, bx + 40, by + 34, bw - 80, 84, 42)
        fill(ctx, "#F2F0F6")
        q = "目的地：上海    日期：周五"
        n = int(len(q) * prog(t, 13.3, 14.4))
        text(ctx, q[:n], bx + 84, by + 76, 36, "#2B2233", 1, "bold", "l")
        ic_plane(ctx, bx + bw - 96, by + 76, 58, 1, t, "#4C8DFF", -0.3)
        # 搜索进度
        if 14.5 < t < 15.7:
            progress(ctx, bx + 40, by + 160, bw - 80, 14, ease_io(prog(t, 14.5, 15.5)), "#4C8DFF")
            text(ctx, "正在查询航班…", bx + bw / 2, by + 220, 34, "#8A8296", 1, "bold")
        # 航班列表 / 表单
        form = smooth(prog(t, 17.95, 18.25))
        lst = 1 - smooth(prog(t, 17.7, 17.95))
        if t > 15.6 and lst > 0:
            for i, (tm, price) in enumerate(FLIGHTS):
                k = ease_out(prog(t, 15.6 + i * 0.2, 16.0 + i * 0.2))
                if k <= 0:
                    continue
                ry = by + 160 + i * 140
                best = i == 1 and t > 16.8
                dim = 0.45 if (t > 16.8 and i != 1) else 1.0
                aa = k * lst * dim
                rrect(ctx, bx + 40, ry, bw - 80, 116, 26)
                fill(ctx, "#FFFFFF", aa)
                ctx.set_line_width(6 if best else 2.5)
                setc(ctx, "#3CCB7F" if best else "#E3DEEA", lst * k)
                rrect(ctx, bx + 40, ry, bw - 80, 116, 26)
                ctx.stroke()
                ic_plane(ctx, bx + 108, ry + 58, 58, aa, t, "#4C8DFF")
                text(ctx, tm, bx + 175, ry + 58, 42, "#2B2233", aa, "bold", "l")
                text(ctx, price, bx + bw - 80, ry + 58, 46, "#E5484D" if best else "#2B2233", aa, "black", "r")
                if best:
                    bk = pop(t, 16.85, 0.4)
                    with at(ctx, bx + bw - 330, ry + 58, bk):
                        pill(ctx, "最低价", 0, 0, 30, "#FFFFFF", "#3CCB7F", lst, 1.0)
        if form > 0:
            rows = [("乘机人", "小橙"), ("证件号", "**** **** 1234"), ("航班", "10:30 → 12:40  ¥960")]
            for i, (k_, v) in enumerate(rows):
                ry = by + 170 + i * 130
                text(ctx, k_, bx + 70, ry + 44, 36, "#8A8296", form, "bold", "l")
                rrect(ctx, bx + 250, ry, bw - 320, 88, 20)
                fill(ctx, "#F6F4FA", form)
                n = int(len(v) * prog(t, 18.05 + i * 0.28, 18.35 + i * 0.28))
                text(ctx, v[:n], bx + 284, ry + 44, 40, "#2B2233", form, "bold", "l")
        # 确认对话框
        mk = ease_back(prog(t, 19.0, 19.4), 1.6)
        if mk > 0:
            ctx.rectangle(bx, by, bw, bh)
            setc(ctx, "#1A1426", 0.28 * min(1, mk))
            ctx.fill()
            ok = t >= T_CLICK + 0.1
            with at(ctx, 0, by + bh / 2 - 20, mk):
                card(ctx, -330, -165, 660, 330, 36, "#FFFFFF", 1, shadow=0.3)
                if not ok:
                    text(ctx, "确认支付 ¥960？", 0, -70, 48, "#2B2233", 1, "black")
                    button(ctx, "取消", -140, 64, 220, 86, "#E3DEEA", 1, 0, 34, "#5A4E63")
                    press = prog(t, T_CLICK - 0.05, T_CLICK + 0.2)
                    button(ctx, "确认", 140, 64, 220, 86, "#3CCB7F", 1, press, 34)
                else:
                    sk = pop(t, T_CLICK + 0.1, 0.4)
                    with at(ctx, 0, -30, sk):
                        circle(ctx, 0, 0, 56)
                        fill(ctx, "#3CCB7F")
                        check_mark(ctx, 0, 2, 64, "#FFFFFF", prog(t, T_CLICK + 0.15, T_CLICK + 0.45))
                    text(ctx, "出票成功", 0, 78, 40, "#2B2233", 1, "black")
        # 鼠标指针
        if 19.5 < t < 20.9:
            u = ease_io(prog(t, 19.5, T_CLICK - 0.05))
            px, py = lerp(420, 150, u), lerp(420, by + bh / 2 + 60, u)
            draw_cursor(ctx, px, py, 1 - smooth(prog(t, 20.6, 20.9)))
            ring_burst(ctx, t, T_CLICK, 140, by + bh / 2 + 44, 10, 100, "#3CCB7F", 0.5, 6)
    sparkle_burst(ctx, t, T_CLICK + 0.1, x + w / 2, y + h / 2 - 20, 12, 320, "#FFC65C", 0.9, 9, 22)


def draw_cursor(ctx, x, y, a):
    if a <= 0:
        return
    pts = [(x, y), (x, y + 46), (x + 12, y + 34), (x + 22, y + 56), (x + 30, y + 52), (x + 20, y + 31), (x + 36, y + 31)]
    from ..core import poly
    poly(ctx, pts)
    fill(ctx, "#FFFFFF", a)
    poly(ctx, pts)
    ctx.set_line_width(3)
    setc(ctx, "#2B2233", a)
    ctx.stroke()


def sfx():
    out = [(0.6, "pop", {"gain": 0.45, "pitch": 0.9}), (1.2, "pop", {"gain": 0.35, "pitch": 1.2})]
    for i, tt in enumerate(T_TOOL):
        out.append((tt, "pop", {"gain": 0.3, "pitch": 1.1 + i * 0.08}))
    out += [(2.8, "pop", {"gain": 0.35, "pitch": 1.2}),
            (T_FLY, "whoosh", {"dur": 1.0, "gain": 0.45}),
            (T_POWER, "powerup", {"gain": 0.6}),
            (T_POWER + 0.05, "boing", {"gain": 0.3}),
            (6.0, "swish", {"gain": 0.3})]
    for k in range(LOOPS * 3):
        out.append((T_LOOP0 + k * LOOP_PERIOD / 3, "blip", {"gain": 0.32, "pitch": [1.0, 1.25, 1.5][k % 3]}))
    out += [(T_LOOP0 + LOOP_PERIOD * LOOPS + 0.55, "ding", {"gain": 0.5, "pitch": 1.2}),
            (11.3, "whoosh", {"dur": 1.2, "gain": 0.5}),
            (T_REQ, "notify", {"gain": 0.5, "pitch": 1.0}),
            (12.6, "swish", {"gain": 0.3}),
            (12.85, "pop", {"gain": 0.35, "pitch": 0.8})]
    out.append((13.3, "typing", {"dur": 1.1, "gain": 0.35}))
    out.append((14.5, "scan", {"dur": 1.0, "gain": 0.3}))
    for i in range(3):
        out.append((15.6 + i * 0.2, "tick", {"gain": 0.35, "pitch": 1.0 + i * 0.1}))
    out.append((16.85, "pop", {"gain": 0.4, "pitch": 1.4}))
    out.append((18.0, "typing", {"dur": 0.9, "gain": 0.35}))
    for tt in T_STEPS[:3]:
        out.append((tt, "check", {"gain": 0.4}))
    out += [(19.0, "pop", {"gain": 0.45, "pitch": 0.9}), (19.15, "bubble", {"gain": 0.35}),
            (T_CLICK, "click", {"gain": 0.6}), (T_CLICK + 0.15, "success", {"gain": 0.55}),
            (T_STEPS[3], "check", {"gain": 0.4}), (20.5, "boing", {"gain": 0.3})]
    return out
