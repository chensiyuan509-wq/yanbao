"""第六章 · 应用层：数据自由流动（以 Meta 的 Muse 为例）。

A 一句"连上我的 Gmail" → 授权弹窗 → 连接成功
B Google 文档 / 表格 / Tasks / 日历、Instagram 逐个连上
C 一句话下达任务：把上周 Ins 帖子数据做成周报，发给老板，再建跟进任务
D 数据依次流经 Instagram → 表格 → 文档 → 邮件 → 任务
E 连接越多 → 能干越多 → 用户越多 → 数据越好 → 模型越强：飞轮
"""
import math

from ..core import (TAU, W, H, Cam, at, circle, clamp, ease_back, ease_in, ease_io, ease_out,
                    fill, glow, kf, lerp, line, lin, pop, prog, rad, rrect, setc, smooth, text,
                    text_w, view, sparkle_burst, ring_burst, stroke_pts, check_mark, arrow_head,
                    point_on, polyline_partial)
from ..icons import (ic_calendar, ic_docs, ic_gmail, ic_instagram, ic_muse, ic_sheets, ic_tasks)
from ..mascot import Puppet
from ..ui import bubble, button, card, checkbox, pill, table, lines_block
from .common import light_bg

DUR = 30.0
CHAPTER = ("06", "应用层：数据自由流动")

SUBS = [
    (0.8, 6.2, "看 Meta 的 {Muse}：说一句「连上我的 Gmail」，授权就完成。"),
    (6.4, 12.4, "Google 文档、表格、Tasks、日历，再加上 Instagram，统统能连。"),
    (12.6, 18.8, "「把上周 Ins 帖子的数据做成周报，发给老板，再建个跟进任务。」"),
    (19.0, 24.4, "读数据、填表格、写报告、发邮件、建任务，{一气呵成}。"),
    (24.6, 29.6, "连接越多 → 能干越多 → 用户越多 → 数据越好 → 模型越强：这就是{飞轮}。"),
]

OC = (960, 480)
NODES = {  # 名称: (图标, 标签, 位置, 连接时间, 颜色)
    "gmail": (ic_gmail, "Gmail", (1450, 240), 3.6, "#EA4335"),
    "docs": (ic_docs, "Google 文档", (1590, 500), 6.8, "#4285F4"),
    "sheets": (ic_sheets, "Google 表格", (1450, 760), 7.6, "#0F9D58"),
    "tasks": (ic_tasks, "Google Tasks", (470, 760), 8.4, "#1A73E8"),
    "calendar": (ic_calendar, "Google 日历", (330, 500), 9.2, "#4285F4"),
    "instagram": (ic_instagram, "Instagram", (470, 240), 10.0, "#D62976"),
}
T_ALLOW = 3.3
T_REQ = 12.7
FLOW = [("instagram", 19.0, "in"), ("sheets", 19.9, "out"), ("docs", 20.8, "out"),
        ("gmail", 21.7, "out"), ("tasks", 22.6, "out")]
T_FLY = 24.5

P = (Puppet(960, 905, 0.55, "smile", seed=11.3)
     .look(0, 0, -1.0)
     .expr(1.0, "happy").talk(1.0, 2.0)
     .expr(3.4, "excited").look(3.4, 1.0, -1.0)
     .expr(6.6, "curious").look(6.8, 1.0, -0.2).look(7.6, 1.0, 0.4).look(8.4, -1.0, 0.4)
     .look(9.2, -1.0, -0.2).look(10.0, -1.0, -1.0).expr(10.2, "excited")
     .expr(T_REQ, "determined").look(T_REQ, 0, -1.0).talk(T_REQ + 0.1, T_REQ + 2.4)
     .expr(15.4, "curious")
     .expr(19.0, "surprised").look(19.0, -1.0, -1.0).look(19.9, 1.0, 0.3).look(20.8, 1.0, -0.1)
     .look(21.7, 1.0, -1.0).look(22.6, -1.0, 0.3)
     .expr(23.6, "excited").hop(23.7, 50).look(23.7, 0, -0.6)
     .move(T_FLY + 0.1, T_FLY + 0.9, 1610, 905, walk=False).hop(T_FLY + 0.1, 120, 0.8).land(T_FLY + 0.9)
     .expr(T_FLY + 0.95, "determined").fx(T_FLY + 0.95, ("sparkle",)).look(T_FLY + 0.95, -1.0, -0.6)
     .expr(28.0, "excited").hop(28.1, 55))

CAM = Cam([
    (0.0, (960, 520, 1.04)),
    (6.2, (960, 515, 1.0)),
    (12.4, (960, 515, 1.0)),
    (13.4, (960, 500, 1.04), ease_io),
    (18.8, (960, 505, 1.02)),
    (T_FLY, (960, 510, 1.0)),
    (T_FLY + 1.2, (960, 520, 0.94), ease_io),
    (30.0, (960, 520, 0.98)),
], drift=4, seed=31.0)


def draw(ctx, t):
    light_bg(ctx, "#F6F8FF", "#E4EBFB", dots="#8EA3D6", dot_a=0.14, spacing=64, drift=(t * 6, -t * 4))
    cam = CAM.at(t)
    with view(ctx, cam, 0.5):
        glow(ctx, 960, 500, 700, "#FFFFFF", 0.6)
    with view(ctx, cam):
        fly = smooth(prog(t, T_FLY, T_FLY + 0.8))
        draw_links(ctx, t, 1 - 0.75 * fly)
        draw_nodes(ctx, t, 1 - 0.7 * fly)
        draw_orb(ctx, t)
        draw_flow(ctx, t)
        if fly > 0:
            draw_flywheel(ctx, t, fly)
        auth_dialog(ctx, t)
        request(ctx, t)
        P.draw(ctx, t)
        speech(ctx, t)


def _node_k(name, t):
    return pop(t, NODES[name][3], 0.45)


def draw_links(ctx, t, a):
    for name, (ic, lab, (x, y), t0, col) in NODES.items():
        lp = ease_out(prog(t, t0 - 0.25, t0 + 0.2))
        if lp <= 0:
            continue
        x1, y1 = lerp(OC[0], x, lp), lerp(OC[1], y, lp)
        stroke_pts(ctx, [OC, (x1, y1)], 6, col, 0.35 * a, dash=(16, 12), offset=-t * 50)
        if lp >= 1:
            for d in range(2):
                u = ((t - t0) * 0.45 + d * 0.5) % 1
                glow(ctx, lerp(OC[0], x, u), lerp(OC[1], y, u), 16, col, 0.5 * a * math.sin(u * math.pi))


def draw_nodes(ctx, t, a):
    for name, (ic, lab, (x, y), t0, col) in NODES.items():
        k = _node_k(name, t)
        if k <= 0:
            continue
        act = 0.0
        for (n2, ts, _) in FLOW:
            if n2 == name and ts <= t < ts + 0.9:
                act = math.sin(prog(t, ts, ts + 0.9) * math.pi)
        with at(ctx, x, y, k * (1 + 0.12 * act)):
            glow(ctx, 0, 0, 150, col, (0.15 + 0.4 * act) * a)
            ic(ctx, 0, 0, 132, a, t)
            text(ctx, lab, 0, 102, 30, "#3A3F55", a, "black")
        ring_burst(ctx, t, t0, x, y, 60, 160, col, 0.6, 6)
        ck = pop(t, t0 + 0.2, 0.35)
        if ck > 0:
            with at(ctx, x + 56, y - 56, ck):
                circle(ctx, 0, 0, 22)
                fill(ctx, "#3CCB7F", a)
                check_mark(ctx, 0, 1, 26, "#FFFFFF", 1, a)
    # 标注：Google 的开放接口 / Meta 自家
    for (tt, s, x, y, bg) in ((10.9, "Google 的开放接口", 1640, 905, "#4285F4"), (10.6, "Meta 自家：自动连接", 470, 120, "#D62976")):
        k = pop(t, tt, 0.45) * (1 - smooth(prog(t, 12.4, 12.9)))
        if k > 0:
            with at(ctx, x, y, k):
                pill(ctx, s, 0, 0, 28, "#FFFFFF", bg, a, 0.95)


def draw_orb(ctx, t):
    k = ease_back(prog(t, 0.2, 0.8), 1.5)
    if k <= 0:
        return
    thinking = smooth(prog(t, 13.2, 13.6)) * (1 - smooth(prog(t, 18.7, 19.0)))
    pulse = 0.5 + 0.5 * math.sin(t * 3)
    glow(ctx, OC[0], OC[1], 300 * k, "#8B6CFF", 0.35 + 0.1 * pulse)
    if thinking > 0:
        for j in range(3):
            ang = t * (2.5 + j) + j * 2.1
            ctx.set_line_width(6)
            setc(ctx, ["#3D7BFF", "#8B5CF6", "#FF7AC6"][j], 0.8 * thinking)
            ctx.new_sub_path()
            ctx.arc(OC[0], OC[1], 130 + j * 14, ang, ang + 1.4)
            ctx.stroke()
    ic_muse(ctx, OC[0], OC[1], 200 * k, 1.0, t)
    la = smooth(prog(t, 0.6, 1.0)) * (1 - smooth(prog(t, 1.2, 1.6))) + smooth(prog(t, 4.6, 5.0)) * (1 - smooth(prog(t, 12.2, 12.6)))
    if la > 0:
        text(ctx, "Meta 的个人智能体", OC[0], OC[1] + 140, 30, "#5B4E8C", la, "black")


def speech(ctx, t):
    k = pop(t, 1.0, 0.4) * (1 - smooth(prog(t, 3.0, 3.3)))
    if k > 0:
        hx, hy = P.head(t)
        with at(ctx, hx, hy - 60, k):
            bubble(ctx, -170, -50, 340, 84, "#FFFFFF", 1, tail="bottom", r=30)
            text(ctx, "连上我的 Gmail", 0, -8, 34, "#2B2233", 1, "black")


def auth_dialog(ctx, t):
    k = ease_back(prog(t, 1.7, 2.15), 1.5)
    out = prog(t, T_ALLOW + 0.25, T_ALLOW + 0.65)
    if k <= 0 or out >= 1:
        return
    x, y = 960, 240
    e = ease_in(out)
    gx, gy = NODES["gmail"][2]
    cx, cy = lerp(x, gx, e), lerp(y, gy, e)
    s = k * (1 - 0.8 * e)
    with at(ctx, cx, cy, s):
        card(ctx, -300, -130, 600, 260, 34, "#FFFFFF", 1, shadow=0.3)
        ic_gmail(ctx, -200, -40, 90, 1, t)
        text(ctx, "Muse 想访问你的 Gmail", 60, -64, 32, "#2B2233", 1, "black")
        text(ctx, "可读取邮件；发送前会先问你", 60, -16, 24, "#8A8296", 1, "bold")
        press = prog(t, T_ALLOW - 0.1, T_ALLOW + 0.15)
        button(ctx, "允许", 150, 66, 200, 70, "#4285F4", 1, press, 30)
        button(ctx, "取消", -60, 66, 160, 70, "#ECEAF2", 1, 0, 28, "#5A4E63")
    if t < T_ALLOW + 0.3:
        # 手指点击
        u = ease_io(prog(t, 2.5, T_ALLOW - 0.05))
        fx, fy = lerp(1240, 1110, u), lerp(470, 306 + 8, u)
        circle(ctx, fx, fy, 22 + 6 * math.sin(prog(t, T_ALLOW - 0.1, T_ALLOW + 0.2) * math.pi))
        fill(ctx, "#2B2233", 0.25 * smooth(prog(t, 2.5, 2.7)))
        ring_burst(ctx, t, T_ALLOW, 1110, 306, 10, 60, "#4285F4", 0.4, 5)


def request(ctx, t):
    k = ease_back(prog(t, T_REQ, T_REQ + 0.45), 1.4)
    if k <= 0:
        return
    a = 1 - smooth(prog(t, T_FLY, T_FLY + 0.6))
    if a <= 0:
        return
    l1, l2 = "把上周 Ins 帖子的数据做成周报，", "发给老板，再建个跟进任务。"
    full = l1 + l2
    n = int(len(full) * prog(t, T_REQ + 0.2, T_REQ + 2.4))
    s1, s2 = full[:min(n, len(l1))], full[len(l1):n] if n > len(l1) else ""
    with at(ctx, 960, 92, k):
        w = 760
        bubble(ctx, -w / 2, -64, w, 128, "#FFFFFF", a, tail="none", r=34, shadow=0.2)
        circle(ctx, -w / 2 + 56, 0, 30)
        fill(ctx, "#FFB547", a)
        text(ctx, "你", -w / 2 + 56, 0, 28, "#FFFFFF", a, "black")
        text(ctx, s1, -w / 2 + 104, -24, 32, "#2B2233", a, "bold", "l")
        text(ctx, s2, -w / 2 + 104, 24, 32, "#2B2233", a, "bold", "l")
    # 指向 Muse 的虚线
    lp = ease_out(prog(t, T_REQ + 2.4, T_REQ + 2.9))
    if lp > 0:
        stroke_pts(ctx, [(960, 160), (960, lerp(160, OC[1] - 120, lp))], 5, "#8B6CFF", 0.6 * a, dash=(10, 9), offset=-t * 40)


def _mini(ctx, kind, x, y, t, ts, a):
    k = ease_back(prog(t, ts + 0.35, ts + 0.75), 1.6)
    if k <= 0:
        return
    with at(ctx, x, y, k):
        if kind == "instagram":
            card(ctx, -150, -70, 300, 140, 22, "#FFFFFF", a, shadow=0.2)
            text(ctx, "上周帖子", -126, -40, 24, "#D62976", a, "black", "l")
            for j, (lab, v) in enumerate((("点赞", "12,480"), ("评论", "1,036"))):
                text(ctx, lab, -126, 0 + j * 38, 26, "#8A8296", a, "bold", "l")
                text(ctx, v, 126, 0 + j * 38, 28, "#2B2233", a, "black", "r")
        elif kind == "sheets":
            card(ctx, -165, -82, 330, 164, 22, "#FFFFFF", a, shadow=0.2)
            cells = [["周一", "3.2k"], ["周三", "4.1k"], ["周五", "5.2k"]]
            table(ctx, -140, -66, 2, 3, 140, 32, a, "#E6F4EA", "#CFE6D6", prog(t, ts + 0.5, ts + 0.9), 20,
                  ["日期", "点赞"], cells, "#0F9D58")
        elif kind == "docs":
            card(ctx, -150, -82, 300, 164, 22, "#FFFFFF", a, shadow=0.2)
            text(ctx, "周报：点赞 +23%", -124, -48, 26, "#4285F4", a, "black", "l")
            lines_block(ctx, -124, -14, 248, 4, 26, "#D7DEEC", a, prog(t, ts + 0.5, ts + 0.9), 10, seed=3)
        elif kind == "gmail":
            card(ctx, -150, -60, 300, 120, 22, "#FFFFFF", a, shadow=0.2)
            text(ctx, "收件人：老板", -126, -26, 26, "#2B2233", a, "black", "l")
            sent = prog(t, ts + 0.6, ts + 0.8)
            text(ctx, "已发送 ✓" if sent >= 1 else "发送中…", -126, 22, 26, "#3CCB7F" if sent >= 1 else "#8A8296", a, "bold", "l")
        elif kind == "tasks":
            card(ctx, -150, -56, 300, 112, 22, "#FFFFFF", a, shadow=0.2)
            checkbox(ctx, -110, 0, 34, prog(t, ts + 0.55, ts + 0.85), "#1A73E8", a)
            text(ctx, "周一跟进反馈", -80, 0, 28, "#2B2233", a, "black", "l")


def draw_flow(ctx, t):
    if t < 18.9 or t > T_FLY + 0.8:
        return
    a = 1 - smooth(prog(t, T_FLY, T_FLY + 0.6))
    for i, (name, ts, d) in enumerate(FLOW):
        if t < ts:
            continue
        x, y = NODES[name][2]
        col = NODES[name][4]
        u = prog(t, ts, ts + 0.55)
        if 0 < u < 1:
            p0, p1 = ((x, y), OC) if d == "in" else (OC, (x, y))
            for k in range(5):
                v = clamp(ease_io(u) - k * 0.05)
                px, py = lerp(p0[0], p1[0], v), lerp(p0[1], p1[1], v)
                glow(ctx, px, py, 34 - k * 5, col, 0.8 * a * (1 - k / 5))
            circle(ctx, lerp(p0[0], p1[0], ease_io(u)), lerp(p0[1], p1[1], ease_io(u)), 11)
            fill(ctx, "#FFFFFF", a)
        # 步骤编号
        bk = pop(t, ts + 0.3, 0.4)
        if bk > 0:
            with at(ctx, x - 64, y - 62, bk):
                circle(ctx, 0, 0, 26)
                fill(ctx, "#2B2233", a)
                text(ctx, str(i + 1), 0, 0, 30, "#FFFFFF", a, "black")
        mx, my = lerp(x, OC[0], 0.42), lerp(y, OC[1], 0.42)
        _mini(ctx, name, mx, my, t, ts, a)


FLY_LABELS = ["连接更多", "能干更多", "用户更多", "数据更好", "模型更强"]


def draw_flywheel(ctx, t, a):
    cx, cy = OC[0], OC[1] - 10
    R = 345
    u = t - T_FLY
    # 角度随时间加速
    spin = 0.6 * u + 0.35 * u * u
    ctx.set_line_width(26)
    setc(ctx, "#8B6CFF", 0.12 * a)
    circle(ctx, cx, cy, R)
    ctx.stroke()
    for k in range(5):
        a0 = -math.pi / 2 + k * TAU / 5 + 0.2
        a1 = a0 + TAU / 5 - 0.4
        dp = ease_out(prog(t, T_FLY + 0.3 + k * 0.12, T_FLY + 0.8 + k * 0.12))
        if dp <= 0:
            continue
        pts = [(cx + math.cos(lerp(a0, a1, v / 24)) * R, cy + math.sin(lerp(a0, a1, v / 24)) * R) for v in range(25)]
        seg = polyline_partial(pts, dp)
        stroke_pts(ctx, seg, 10, "#8B6CFF", 0.75 * a)
        if dp > 0.95:
            (ex, ey), (qx, qy) = pts[-1], pts[-2]
            arrow_head(ctx, ex, ey, math.atan2(ey - qy, ex - qx), 34, "#8B6CFF", 0.85 * a)
    # 绕圈的彗星
    for j in range(3):
        ang = -math.pi / 2 + spin * TAU / 3 + j * TAU / 3
        for q in range(10):
            aa = ang - q * 0.05 * (1 + u * 0.4)
            glow(ctx, cx + math.cos(aa) * R, cy + math.sin(aa) * R, 30 - q * 2.4, "#FFC65C", 0.8 * a * (1 - q / 10))
    # 标签（位置固定，便于阅读）
    for k, s in enumerate(FLY_LABELS):
        ang = -math.pi / 2 + k * TAU / 5
        lk = pop(t, T_FLY + 0.5 + k * 0.25, 0.45)
        if lk <= 0:
            continue
        lx, ly = cx + math.cos(ang) * (R + 4), cy + math.sin(ang) * (R + 4)
        with at(ctx, lx, ly, lk):
            pill(ctx, s, 0, 0, 34, "#FFFFFF", "#6D4FE0", a, 1.0, weight="black")
    ck = pop(t, T_FLY + 1.9, 0.5)
    if ck > 0:
        with at(ctx, cx, cy + 150, ck):
            pill(ctx, "飞轮效应", 0, 0, 40, "#FFC65C", "#1A1426", a, 0.9, weight="black")
    sparkle_burst(ctx, t, T_FLY + 1.9, cx, cy, 12, 420, "#FFC65C", 1.0, 8, 22)


def sfx():
    out = [(0.2, "pop", {"gain": 0.45, "pitch": 0.8}), (1.0, "bubble", {"gain": 0.4}),
           (1.7, "pop", {"gain": 0.45, "pitch": 1.0}), (T_ALLOW, "click", {"gain": 0.55}),
           (T_ALLOW + 0.3, "whoosh_short", {"gain": 0.35}),
           (4.0, "stream", {"dur": 8.6, "gain": 0.14}), (19.0, "stream", {"dur": 5.0, "gain": 0.12})]
    for name, (_, _, _, t0, _) in NODES.items():
        out.append((t0, "connect", {"gain": 0.45, "pitch": 1.0 + list(NODES).index(name) * 0.07}))
        out.append((t0 + 0.2, "check", {"gain": 0.3}))
    out += [(10.6, "pop", {"gain": 0.3, "pitch": 1.2}), (10.9, "pop", {"gain": 0.3, "pitch": 1.1}),
            (T_REQ, "notify", {"gain": 0.45, "pitch": 1.05}), (T_REQ + 0.2, "typing", {"dur": 2.2, "gain": 0.3}),
            (13.2, "think", {"dur": 5.4, "gain": 0.25})]
    for i, (name, ts, d) in enumerate(FLOW):
        out.append((ts, "zip", {"gain": 0.4, "pitch": 0.9 + i * 0.1}))
        out.append((ts + 0.35, "pop", {"gain": 0.35, "pitch": 1.0 + i * 0.1}))
        if name == "gmail":
            out.append((ts + 0.6, "mail", {"gain": 0.45}))
        if name == "tasks":
            out.append((ts + 0.6, "check", {"gain": 0.45}))
    out += [(23.7, "success", {"gain": 0.45}),
            (T_FLY, "whoosh", {"dur": 1.2, "gain": 0.4}),
            (T_FLY + 0.4, "spinup", {"dur": 5.0, "gain": 0.45})]
    for k in range(5):
        out.append((T_FLY + 0.5 + k * 0.25, "pop", {"gain": 0.3, "pitch": 1.0 + k * 0.12}))
    out += [(T_FLY + 1.9, "impact_soft", {"gain": 0.45}), (T_FLY + 1.95, "shimmer", {"dur": 1.6, "gain": 0.35})]
    return out
