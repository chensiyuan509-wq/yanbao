"""第八章 · 孤岛：围墙花园。

A 国产大模型（DeepSeek · Qwen · Kimi …）已是世界第一梯队
B 镜头拉远：微信、淘宝、抖音、小红书、支付宝、美团……一座座岛升起围墙
C WorkBuddy 能连海外的 Gmail / Slack / Notion，却没有抖音、小红书的官方连接器
D 豆包手机助手想替你操作 App：150 多款 App 说"不"
E 理由有安全，也有竞争
F 大脑再聪明，智能体也伸不出手
"""
import math

from ..core import (TAU, W, H, Cam, at, circle, clamp, ease_back, ease_in, ease_io, ease_out,
                    ellipse, fill, glow, kf, lerp, line, lin, pop, poly, prog, rad, rng, rrect, setc,
                    smooth, text, text_w, view, sparkle_burst, ring_burst, stroke_pts, cross_mark,
                    vignette, check_mark)
from ..icons import ic_brain, ic_gmail, ic_notion, ic_slack, ic_trophy, ic_workbuddy
from ..mascot import Puppet
from ..ui import card, pill, stamp

DUR = 35.5
CHAPTER = ("08", "孤岛：围墙花园")

SUBS = [
    (0.8, 7.2, "再看中国：问题不在模型，{DeepSeek} 等国产模型已是世界第一梯队。"),
    (7.4, 12.4, "问题在于，数据和接口被一座座「{围墙花园}」隔开了。"),
    (12.6, 19.6, "腾讯的 WorkBuddy 能连 Gmail、Slack，却没有{抖音、小红书}的官方连接器。"),
    (19.8, 25.6, "字节的豆包手机助手想替你操作 App，{150 多款 App} 说「不」："),
    (25.8, 31.2, "微信、淘宝、支付宝、美团、小红书……理由有安全，也有竞争。"),
    (31.4, 35.3, "结果是：大脑再聪明，智能体也{伸不出手}。"),
]

M = (880, 600)            # 大模型所在的中心岛
ISL = {  # 名称: (位置, 颜色, 围墙升起时间, 印章时间)
    "微信": ((330, 380), "#07C160", 8.0, 20.9),
    "淘宝": ((1430, 330), "#FF5000", 8.3, 21.35),
    "抖音": ((1660, 890), "#161823", 8.6, None),
    "小红书": ((1080, 955), "#FF2442", 8.9, 23.15),
    "支付宝": ((300, 840), "#1677FF", 9.2, 21.8),
    "美团": ((1985, 590), "#FFC300", 9.5, 22.25),
}
HORIZON = 120
_R = rng(77)
FAR = [(_R.uniform(-250, 2550), HORIZON + _R.uniform(10, 90), _R.uniform(18, 34), 21.0 + i * 0.075)
       for i in range(46)]
T_WB = 12.7
T_DB = 19.9
OVERSEAS = [(1780, 130, ic_gmail), (1910, 215, ic_slack), (2040, 130, ic_notion)]

P = (Puppet(M[0] + 130, M[1] + 6, 0.5, "proud", seed=13.9)
     .look(0, -0.6, -0.6).fx(0.0, ("sparkle",))
     .fx(6.9, None).expr(7.5, "curious").look(7.6, -1.0, -0.6).look(8.6, 1.0, -0.4).look(9.4, -1.0, 0.4)
     .expr(10.2, "worried")
     .look(T_WB + 0.5, 1.0, -1.0).expr(T_WB + 1.4, "happy").look(T_WB + 3.0, 1.0, 0.6)
     .expr(T_WB + 4.4, "sad")
     .expr(T_DB + 0.4, "curious").look(T_DB + 0.4, -1.0, 0.4)
     .expr(T_DB + 1.2, "shock").shake(T_DB + 1.2, 0.5, 0.05).expr(T_DB + 2.6, "tired")
     .fx(T_DB + 2.6, ("sweat",))
     .expr(26.4, "worried").fx(26.4, None).look(26.4, 0, -0.8)
     .expr(31.4, "determined").look(31.4, 1.0, 0.5).fx(31.4, None)
     .arm(31.6, "r", 0.35, 0.3).ext(31.6, "r", 95, 0.6).strain(32.2, 33.6, "r")
     .arm(33.7, "r", 0.0, 0.5).ext(33.7, "r", 0, 0.4)
     .expr(33.8, "sad").fx(33.8, ("gloom",)).look(33.8, 0, 0.4))

CAM = Cam([
    (0.0, (M[0] + 60, 560, 1.45)),
    (6.8, (M[0] + 70, 560, 1.52)),
    (8.4, (1130, 600, 0.92), ease_io),
    (12.4, (1140, 605, 0.94)),
    (13.4, (1310, 540, 0.97), ease_io),
    (19.4, (1320, 540, 0.99)),
    (20.4, (1130, 600, 0.92), ease_io),
    (30.8, (1140, 600, 0.94)),
    (32.0, (M[0] + 190, M[1] - 70, 1.55), ease_io),
    (35.5, (M[0] + 200, M[1] - 70, 1.62)),
], drift=6, seed=41.0)


def draw(ctx, t):
    cam = CAM.at(t)
    gloom = smooth(prog(t, 31.0, 33.5))
    # 天空 + 海
    ctx.set_source(lin(0, 0, 0, H, [(0, "#16324A"), (0.35, "#1E4E68"), (1, "#0D2E44")]))
    ctx.paint()
    with view(ctx, cam, 0.85):
        ctx.rectangle(-2000, HORIZON, 7000, 3000)
        ctx.set_source(lin(0, HORIZON, 0, HORIZON + 1400, [(0, "#2B6F86"), (1, "#0E3550")]))
        ctx.fill()
        glow(ctx, 1150, HORIZON, 900, "#FFD9A8", 0.18)
    with view(ctx, cam):
        waves(ctx, t)
        far_islands(ctx, t)
        overseas(ctx, t)
        # 按 y 排序绘制岛屿，近的盖住远的
        items = [(pos[1], name) for name, (pos, *_r) in ISL.items()] + [(M[1], "__M")]
        for _, name in sorted(items):
            if name == "__M":
                model_island(ctx, t)
            else:
                island(ctx, name, t)
        boats(ctx, t)
        tags(ctx, t)
    counter(ctx, t)
    walled_title(ctx, t)
    if gloom > 0:
        vignette(ctx, 0.55 * gloom, "#020814", inner=0.3)


def waves(ctx, t):
    for j in range(16):
        y = HORIZON + 60 + j * 80
        ctx.move_to(-800, y)
        for x in range(-800, 3200, 60):
            ctx.line_to(x, y + math.sin(x * 0.01 + t * 1.2 + j) * 6)
        ctx.set_line_width(2.5)
        setc(ctx, "#8FD3E8", 0.10 + 0.012 * j)
        ctx.stroke()


def _island_base(ctx, x, y, rx, top="#4E8A5E", side="#3B5E44"):
    ry = rx * 0.32
    ellipse(ctx, x, y + 26, rx * 1.18, ry * 1.25)
    fill(ctx, "#8FD3E8", 0.18)
    ctx.move_to(x - rx, y)
    ctx.curve_to(x - rx, y + ry * 1.6, x + rx, y + ry * 1.6, x + rx, y)
    ctx.close_path()
    ctx.set_source(lin(0, y, 0, y + ry * 1.4, [(0, side), (1, "#24382A")]))
    ctx.fill()
    ellipse(ctx, x, y, rx, ry)
    ctx.set_source(lin(0, y - ry, 0, y + ry, [(0, "#E9D9B4"), (0.25, top), (1, top)]))
    ctx.fill()


def _wall(ctx, x, y, rx, h, front, gate=0.0):
    """围墙：front=False 画后半圈，True 画前半圈（含砖纹与大门）。"""
    if h <= 0.5:
        return
    ry = rx * 0.32
    rw = rx * 0.96
    rwy = ry * 0.96
    a0, a1 = (math.pi, TAU) if not front else (0, math.pi)
    pts_bot = [(x + math.cos(a0 + (a1 - a0) * i / 30) * rw, y + math.sin(a0 + (a1 - a0) * i / 30) * rwy) for i in range(31)]
    pts_top = [(px, py - h) for (px, py) in reversed(pts_bot)]
    poly(ctx, pts_bot + pts_top)
    col0, col1 = ("#B9A58A", "#8C7A64") if not front else ("#D9C4A4", "#A8916F")
    ctx.set_source(lin(0, y - h - rwy, 0, y + rwy, [(0, col0), (1, col1)]))
    ctx.fill()
    if front:
        # 墙顶
        stroke_pts(ctx, pts_top[::-1], 6, "#EADBC0", 1.0)
        # 砖纹
        ctx.save()
        poly(ctx, pts_bot + pts_top)
        ctx.clip()
        setc(ctx, "#8A7457", 0.45)
        ctx.set_line_width(2)
        rows = int(h / 22) + 1
        for r_ in range(rows):
            yy = r_ * 22
            ctx.move_to(x - rw, y + rwy - yy)
            ctx.line_to(x + rw, y + rwy - yy)
            for c_ in range(-8, 9):
                bx = x + c_ * 40 + (20 if r_ % 2 else 0)
                ctx.move_to(bx, y + rwy - yy)
                ctx.line_to(bx, y + rwy - yy - 22)
        ctx.stroke()
        ctx.restore()
        # 大门
        gh = min(h * 0.8, 70)
        gw = 54
        gy = y + rwy
        rrect(ctx, x - gw / 2, gy - gh, gw, gh + 4, 22)
        fill(ctx, "#3A2C22")
        if gate > 0:
            for sgn in (-1, 1):
                ctx.rectangle(x + (0 if sgn > 0 else -gw / 2 * gate), gy - gh, gw / 2 * gate, gh)
            fill(ctx, "#6B4E36")


def island(ctx, name, t):
    (x, y), col, tw_, ts = ISL[name]
    k = pop(t, 7.6 + list(ISL).index(name) * 0.12, 0.5)
    if k <= 0:
        return
    rx = 180 * k
    _island_base(ctx, x, y, rx)
    hwall = 92 * ease_out(prog(t, tw_, tw_ + 0.7))
    gate = ease_out(prog(t, tw_ + 0.4, tw_ + 0.9))
    _wall(ctx, x, y, rx, hwall, False)
    # 岛上的 App 牌子
    bob = math.sin(t * 1.5 + x) * 4
    with at(ctx, x, y - 70 + bob, k):
        rrect(ctx, -86, -50, 172, 100, 30)
        fill(ctx, col)
        rrect(ctx, -86, -50, 172, 100, 30)
        ctx.set_line_width(3)
        setc(ctx, "#FFFFFF", 0.55)
        ctx.stroke()
        tsize = 42 if len(name) <= 2 else 36
        text(ctx, name, 0, 0, tsize, "#FFFFFF" if name != "美团" else "#2B2233", 1, "black")
    _wall(ctx, x, y, rx, hwall, True, gate)
    # 被点名时的高亮
    if 25.8 <= t < 31.0 and name != "抖音":
        idx = ["微信", "淘宝", "支付宝", "美团", "小红书"].index(name)
        hk = smooth(prog(t, 25.9 + idx * 0.55, 26.3 + idx * 0.55)) * (1 - smooth(prog(t, 30.4, 31.0)))
        glow(ctx, x, y - 70, 220, "#FFD25C", 0.35 * hk)
    # "拒绝"印章
    if ts is not None and t > ts:
        u = prog(t, ts, ts + 0.22)
        kk = lerp(2.4, 1.0, ease_in(u))
        stamp(ctx, "拒绝", x + 46, y + 18, 50, "#E5484D", min(1, u * 2), -0.2, kk)
        if u >= 1:
            ring_burst(ctx, t, ts + 0.22, x + 40, y + 20, 30, 140, "#F2D7C0", 0.5, 8)


def model_island(ctx, t):
    x, y = M
    _island_base(ctx, x, y, 270, top="#5C7FB8", side="#3C557E")
    gl = 0.6 + 0.2 * math.sin(t * 2)
    glow(ctx, x - 70, y - 130, 260, "#8B6CFF", 0.35 * gl)
    ic_brain(ctx, x - 70, y - 120, 170, 1.0, t, glow_a=0.2)
    ic_trophy(ctx, x - 200, y - 40, 110, 1.0, t)
    la = smooth(prog(t, 0.6, 1.2))
    with at(ctx, x - 70, y - 262, ease_back(prog(t, 0.6, 1.2), 1.5)):
        pill(ctx, "世界第一梯队", 0, 0, 34, "#2B2233", "#FFD25C", la, 1.0, weight="black")
    ck = smooth(prog(t, 1.4, 1.9)) * (1 - smooth(prog(t, 7.4, 8.0)))
    if ck > 0:
        for i, (s, col) in enumerate((("DeepSeek", "#4D6BFE"), ("Qwen", "#615CED"), ("Kimi", "#1E1E1E"))):
            k = pop(t, 1.5 + i * 0.3, 0.45)
            with at(ctx, x - 310 + i * 205, y + 132, k):
                from ..ui import chip
                chip(ctx, s, 0, 0, 34, col, ck)
    tk = pop(t, 2.8, 0.45) * (1 - smooth(prog(t, 7.0, 7.6)))
    if tk > 0:
        with at(ctx, x - 70, y + 205, tk):
            pill(ctx, "国产大模型，开源榜单名列前茅", 0, 0, 28, "#FFFFFF", "#1A1426", 1.0, 0.75)
    P.draw(ctx, t)


def far_islands(ctx, t):
    a = smooth(prog(t, 8.2, 9.0))
    if a <= 0:
        return
    for (x, y, r, ts) in FAR:
        ellipse(ctx, x, y, r * 1.6, r * 0.42)
        fill(ctx, "#4E7D69", 0.8 * a)
        ctx.rectangle(x - r * 1.2, y - r * 0.9, r * 2.4, r * 0.9)
        fill(ctx, "#B9A58A", 0.6 * a)
        if t > ts:
            u = prog(t, ts, ts + 0.15)
            circle(ctx, x, y - r * 1.3, 9 * lerp(1.8, 1.0, u))
            fill(ctx, "#E5484D", 0.95 * a)


def overseas(ctx, t):
    """右上角"海外"的应用：WorkBuddy 能连上它们。"""
    a = smooth(prog(t, T_WB, T_WB + 0.6))
    if a <= 0:
        return
    a *= 1 - smooth(prog(t, 19.6, 20.4))
    for i, (x, y, ic) in enumerate(OVERSEAS):
        k = pop(t, T_WB + 0.3 + i * 0.2, 0.45)
        glow(ctx, x, y, 130, "#7CC6FF", 0.3 * a)
        ic(ctx, x, y, 118 * k, a, t)
    pill(ctx, "海外应用：开放连接器", 1910, 320, 36, "#0E3550", "#CFF0FF", a, 0.95, weight="black")


def _boat(ctx, x, y, s, t, label, col, arm=False, above=False):
    with at(ctx, x, y + math.sin(t * 2 + x) * 5, s, math.sin(t * 1.7) * 0.03):
        poly(ctx, [(-120, 0), (120, 0), (90, 50), (-90, 50)])
        ctx.set_source(lin(0, 0, 0, 50, [(0, "#C9895C"), (1, "#8E5A39")]))
        ctx.fill()
        line(ctx, 0, 0, 0, -150, 7, "#6B4E36")
        poly(ctx, [(4, -150), (110, -110), (4, -70)])
        fill(ctx, col)
        if arm:
            stroke_pts(ctx, [(-60, -4), (-120, -70), (-180, -60)], 12, "#9AA7B8", 1.0)
            circle(ctx, -186, -60, 16)
            fill(ctx, "#C9D3E0")
        w = text_w(ctx, label, 44, "black") + 52
        ly = -245 if above else 62
        rrect(ctx, -w / 2, ly, w, 70, 35)
        fill(ctx, "#FFFFFF", 0.96)
        text(ctx, label, 0, ly + 35, 44, "#2B2233", 1, "black")


def boats(ctx, t):
    # WorkBuddy 小船
    a = smooth(prog(t, T_WB - 0.3, T_WB + 0.3)) * (1 - smooth(prog(t, 19.4, 20.0)))
    if a > 0:
        bx = kf(t, [(T_WB, 1290), (T_WB + 2.4, 1330), (T_WB + 3.6, 1390, ease_io)])
        by = kf(t, [(T_WB, 640), (T_WB + 2.4, 640), (T_WB + 3.6, 720, ease_io)])
        # 连向海外应用（成功）
        for i, (ox, oy, _ic) in enumerate(OVERSEAS):
            lp = ease_out(prog(t, T_WB + 0.7 + i * 0.25, T_WB + 1.3 + i * 0.25))
            if lp > 0:
                stroke_pts(ctx, [(bx + 20, by - 140), (lerp(bx + 20, ox, lp), lerp(by - 140, oy + 50, lp))], 6,
                           "#7CFFB2", 0.8 * a, dash=(16, 10), offset=-t * 50)
            if lp >= 1:
                ck = pop(t, T_WB + 1.3 + i * 0.25, 0.4)
                with at(ctx, ox + 54, oy - 54, ck):
                    circle(ctx, 0, 0, 24)
                    fill(ctx, "#3CCB7F", a)
                    check_mark(ctx, 0, 1, 28, "#FFFFFF", 1, a)
        # 尝试连抖音、小红书（失败）
        for i, name in enumerate(("抖音", "小红书")):
            (ix, iy) = ISL[name][0]
            t0 = T_WB + 3.8 + i * 0.9
            lp = ease_out(prog(t, t0, t0 + 0.5))
            if lp <= 0:
                continue
            ex, ey = lerp(bx, ix, 0.78), lerp(by - 60, iy - 40, 0.78)
            stroke_pts(ctx, [(bx, by - 60), (lerp(bx, ex, lp), lerp(by - 60, ey, lp))], 6, "#FF7A85", 0.8 * a,
                       dash=(16, 10), offset=-t * 50)
            if lp >= 1:
                cross_mark(ctx, ex, ey, 76, "#E5484D", prog(t, t0 + 0.5, t0 + 0.8), a, 14)
                lk = pop(t, t0 + 0.6, 0.4)
                with at(ctx, ex + (60 if name == "抖音" else -150), ey - 78, lk):
                    pill(ctx, "无官方连接器", 0, 0, 38, "#FFFFFF", "#E5484D", a, 1.0, weight="black")
        from ..core import group_alpha
        with group_alpha(ctx, a):
            _boat(ctx, bx, by, 1.0, t, "WorkBuddy（腾讯）", "#2F7BFF", above=True)
    # 豆包手机助手的小船
    a2 = smooth(prog(t, T_DB - 0.2, T_DB + 0.4)) * (1 - smooth(prog(t, 30.6, 31.2)))
    if a2 > 0:
        bx = kf(t, [(T_DB, 560), (T_DB + 3.0, 700, ease_io), (30.0, 760)])
        by = kf(t, [(T_DB, 860), (T_DB + 3.0, 800, ease_io)])
        from ..core import group_alpha
        with group_alpha(ctx, a2):
            _boat(ctx, bx, by, 0.95, t, "豆包手机助手（字节）", "#3C8CFF", arm=True)


def counter(ctx, t):
    a = smooth(prog(t, T_DB + 0.8, T_DB + 1.2)) * (1 - smooth(prog(t, 30.6, 31.2)))
    if a <= 0:
        return
    n = int(150 * ease_io(prog(t, 20.9, 24.6)))
    x, y = 1540, 130
    card(ctx, x, y - 70, 340, 140, 30, "#1A1426", a * 0.9, shadow=0.3)
    text(ctx, "拒绝 AI 代操作的 App", x + 170, y - 32, 26, "#FFB3B8", a, "bold")
    s = f"{n}" + ("+" if n >= 150 else "")
    text(ctx, s, x + 140, y + 28, 64, "#FF5A5F", a, "black")
    text(ctx, "款", x + 140 + text_w(ctx, s, 64, "black") / 2 + 30, y + 34, 30, "#FFFFFF", a, "bold")
    sk = pop(t, 24.7, 0.45)
    if sk > 0:
        with at(ctx, x + 170, y + 108, sk):
            pill(ctx, "2026 年 10 月公布的名单", 0, 0, 22, "#FFFFFF", "#5A4E63", a, 0.9)


def walled_title(ctx, t):
    a = smooth(prog(t, 9.6, 10.2)) * (1 - smooth(prog(t, 12.2, 12.7)))
    if a <= 0:
        return
    k = ease_back(prog(t, 9.6, 10.2), 1.6)
    with at(ctx, 960, 470, k):
        rrect(ctx, -250, -70, 500, 140, 70)
        fill(ctx, "#1A1426", 0.82 * a)
        text(ctx, "围墙花园", 0, 0, 76, "#FFD25C", a, "black")


def tags(ctx, t):
    for (s, x, y, t0, col) in (("安全？", 700, 300, 28.6, "#4C8DFF"), ("竞争？", 1240, 200, 29.2, "#FF7A59")):
        k = pop(t, t0, 0.45) * (1 - smooth(prog(t, 30.8, 31.3)))
        if k > 0:
            bob = math.sin(t * 2.4 + x) * 8
            with at(ctx, x, y + bob, k, math.sin(t * 1.6 + x) * 0.05):
                pill(ctx, s, 0, 0, 46, "#FFFFFF", col, 1.0, 1.0, weight="black")


def sfx():
    out = [(0.0, "ambience_sea", {"dur": 35.5, "gain": 0.55}),
           (0.6, "pop", {"gain": 0.4, "pitch": 1.0}), (0.7, "chime", {"gain": 0.35})]
    for i in range(3):
        out.append((1.5 + i * 0.3, "pop", {"gain": 0.3, "pitch": 1.1 + i * 0.1}))
    out += [(2.8, "pop", {"gain": 0.25, "pitch": 0.9}), (7.0, "whoosh", {"dur": 1.4, "gain": 0.4})]
    for name, (pos, col, tw_, ts) in ISL.items():
        out.append((tw_, "rumble", {"dur": 0.8, "gain": 0.4}))
        out.append((tw_ + 0.8, "gate", {"gain": 0.35}))
        if ts is not None:
            out.append((ts, "stamp", {"gain": 0.6}))
    out += [(9.6, "impact_soft", {"gain": 0.5}),
            (T_WB, "water", {"gain": 0.35})]
    for i in range(3):
        out.append((T_WB + 1.3 + i * 0.25, "connect", {"gain": 0.4, "pitch": 1.0 + i * 0.1}))
    for i in range(2):
        out.append((T_WB + 4.3 + i * 0.9, "error", {"gain": 0.45}))
    out += [(T_DB, "water", {"gain": 0.35}), (T_DB + 1.2, "surprise", {"gain": 0.3})]
    for (x, y, r, ts) in FAR[::3]:
        out.append((ts, "tick", {"gain": 0.18, "pitch": 1.6}))
    out += [(24.6, "impact_soft", {"gain": 0.45})]
    for (s, x, y, t0, col) in (("安全？", 640, 300, 28.6, ""), ("竞争？", 1340, 230, 29.2, "")):
        out.append((t0, "pop", {"gain": 0.4, "pitch": 1.0}))
    out += [(31.2, "whoosh", {"dur": 1.0, "gain": 0.35}),
            (31.7, "stretch", {"dur": 2.0, "gain": 0.4}),
            (33.8, "womp", {"gain": 0.45})]
    return out
