"""05 · 孤岛与飞轮（中）：围墙。微信里淘宝 / 抖音只能复制口令 → 豆包手机助手被 150 多款 App 拒绝 →
互联网地主的城堡 → 美国的反垄断法 → 开放语料：英文约一半、中文不到 6% → 数据碎片化，飞轮转不起来。"""
import math

from ..core import (TAU, Cam, at, box_shadow, circle, clamp, ease_back, ease_in, ease_io, ease_out, ease_out5,
                    ellipse, fill, glow, lerp, lin, line, pop, prog, rad, ring_burst, rng, rrect, setc, smooth,
                    sparkle_burst, star4, star5, stroke_pts, text, text_w, view, cross_mark, arrow)
from ..charts import flywheel, hbars
from ..icons import ic_building, ic_lock
from ..props import app_tile, bg_grad, castle, gavel, iphone, name_card, tag
from ..ui import bubble, stamp, window
from .common import host, talk_lines

DUR = 43.5
CHAPTER = ("05", "孤岛与飞轮")

VO = [
    (0.7, '在微信里，淘宝、抖音的链接长期打不开，只能复制一串{口令}，再跳回对应的 App。'),
    (7.8, '豆包手机助手想替你操作 App，结果 150 多款 App 说「不」。'),
    (12.9, '每家都把用户和数据当成自己的{私域流量}，像一个个{互联网地主}，守着自己的地。'),
    (19.8, '而在美国，iPhone 上能自由安装谷歌的 App，背后是{反垄断法}在盯着：谁敢封杀对手，就可能被告上法庭。'),
    (28.9, '语料也是一样：开放网页里，英文约占一半，中文不到 6%，大量优质中文内容锁在 App 里。'),
    (37.0, '数据被切成碎片，智能体伸不出手，数据飞轮自然{转不起来}。'),
]

G = 900
XA, XB, XC, XD, XE, XF = 960, 3100, 5300, 7500, 9700, 11900

P = (host(XA - 640, G, 0.6, "curious", seed=12.2)
     .look(0, 0.9, -0.6)
     .expr(2.6, "confused").fx(2.6, ("question",))
     .expr(5.0, "skeptical").fx(5.0, ()).shrug(5.6, 1.2)
     .expr(7.0, "smile").run_to(7.1, 7.9, XB - 700, G)
     .expr(8.0, "curious").look(8.0, 0.9, -0.6)
     .expr(9.6, "shock").startle(9.6).expr(10.6, "sad")
     .expr(12.2, "smile").run_to(12.3, 13.1, XC - 120, G)
     .expr(13.2, "worried").look(13.2, 0.0, -1.0).look(15.0, -0.8, -0.8).look(16.6, 0.8, -0.8)
     .expr(17.4, "gloomy")
     .expr(19.0, "smile").fx(19.0, ()).run_to(19.1, 19.9, XD - 760, G)
     .expr(20.0, "curious").look(20.0, 0.9, -0.6)
     .expr(23.4, "surprised").expr(24.2, "smug").front(24.6, "cross").front(27.6, None)
     .expr(28.1, "smile").run_to(28.2, 29.0, XE - 760, G)
     .expr(29.1, "focused").look(29.1, 0.9, -0.5)
     .expr(33.4, "sad").look(33.4, 0.9, -0.2)
     .expr(36.2, "smile").run_to(36.3, 37.1, XF - 420, G)
     .expr(37.2, "determined").fx(37.2, ()).look(37.2, 1.0, -0.4)
     .point(37.6, "r", 0.3, 120).strain(37.9, 39.6, "r").arms_down(39.8)
     .expr(39.8, "sad").fx(39.8, ("gloom",)))
talk_lines(P, VO, [0, 2], smile=0.2)

CAM = Cam([
    (0.0, (XA, 540, 1.04)),
    (7.0, (XA + 20, 540, 1.0)),
    (7.9, (XB, 540, 1.0), ease_io),
    (12.2, (XB + 20, 540, 1.02)),
    (13.1, (XC, 520, 0.9), ease_io),
    (18.9, (XC + 20, 520, 0.92)),
    (19.9, (XD, 540, 1.0), ease_io),
    (28.1, (XD + 20, 540, 1.02)),
    (29.0, (XE, 540, 1.0), ease_io),
    (36.2, (XE + 20, 540, 1.02)),
    (37.1, (XF, 540, 1.0), ease_io),
    (43.5, (XF + 20, 540, 1.05)),
], drift=6, seed=25.0)


def _bg(ctx, t, cam):
    bg_grad(ctx, "#1E2440", "#4A3550", "#30304E", 0.6)
    ctx.set_source(rad(960, 1100, 0, 1000, [(0, "#FF9F68", 0.22), (1, "#FF9F68", 0)]))
    ctx.paint()
    with view(ctx, cam, 1.0):
        ctx.rectangle(-1000, G, 14000, 400)
        ctx.set_source(lin(0, G, 0, G + 260, [(0, "#3A3A5A"), (1, "#1E1E30")]))
        ctx.fill()
        ctx.rectangle(-1000, G - 2, 14000, 4)
        fill(ctx, "#FFB27A", 0.25)


def _chat_msg(ctx, x, y, w, h, who, a):
    bubble(ctx, x, y, w, h, "#FFFFFF" if who == "l" else "#95EC69", a, "left" if who == "l" else "right",
           shadow=0.12)


def _part_a(ctx, t):
    """聊天窗口：链接打不开，只能复制口令。"""
    cx, cy, cw, ch = window(ctx, XA - 300, 120, 720, 720, "聊天", 1.0, accent="#EDEDED")
    ctx.save()
    rrect(ctx, cx, cy, cw, ch, 0)
    ctx.clip()
    ctx.set_source(lin(0, cy, 0, cy + ch, [(0, "#F5F5F5"), (1, "#EDEDED")]))
    ctx.paint()
    # 1) 朋友发来淘宝链接 → 打不开
    q1 = pop(t, 1.0, 0.45)
    if q1 > 0:
        with at(ctx, cx + 40, cy + 40, q1):
            _chat_msg(ctx, 0, 0, 420, 110, "l", 1.0)
            app_tile(ctx, 55, 55, 70, "#FF5000", "淘", 1.0, text_size=34)
            text(ctx, "好物推荐 · 淘宝商品", 105, 38, 24, "#2B2233", 1, "bold", "l")
            text(ctx, "https://…taobao…", 105, 74, 20, "#9A9AA0", 1, "mono", "l")
        if t > 2.0:
            k = pop(t, 2.0, 0.4)
            with at(ctx, cx + 470, cy + 95, k):
                rrect(ctx, -10, -26, 210, 52, 26)
                fill(ctx, "#E5484D")
                text(ctx, "链接打不开", 95, 0, 24, "#FFFFFF", 1, "black")
    # 2) 只能复制口令
    q2 = pop(t, 3.4, 0.45)
    if q2 > 0:
        with at(ctx, cx + cw - 40, cy + 230, q2):
            _chat_msg(ctx, -560, 0, 560, 120, "r", 1.0)
            text(ctx, "¥ 8Kq2Xy7 ¥ 复制这段话", -540, 40, 26, "#2B2233", 1, "bold", "l")
            text(ctx, "打开淘宝查看", -540, 82, 26, "#2B2233", 1, "bold", "l")
        if t > 4.1:
            k = pop(t, 4.1, 0.4)
            with at(ctx, cx + 140, cy + 420, k):
                rrect(ctx, -110, -30, 220, 60, 30)
                fill(ctx, "#2B2233")
                text(ctx, "长按 → 复制", 0, 0, 26, "#FFFFFF", 1, "black")
    # 3) 抖音同理
    q3 = pop(t, 4.8, 0.45)
    if q3 > 0:
        with at(ctx, cx + 40, cy + 510, q3):
            _chat_msg(ctx, 0, 0, 470, 110, "l", 1.0)
            app_tile(ctx, 55, 55, 70, "#161823", "抖", 1.0, text_size=34)
            text(ctx, "8.97 复制口令，打开抖音", 105, 38, 24, "#2B2233", 1, "bold", "l")
            text(ctx, "看看这条视频", 105, 74, 20, "#9A9AA0", 1, "bold", "l")
    ctx.restore()
    # 跳回对应 App
    if t > 5.6:
        u = ease_io(prog(t, 5.6, 6.6))
        for i, (lab, c, y) in enumerate((("淘", "#FF5000", 330), ("抖", "#161823", 660))):
            x = XA + 580
            arrow(ctx, XA + 440, y, lerp(XA + 440, x - 60, u), y, 7, "#FFB27A", 1.0)
            if u > 0.9:
                app_tile(ctx, x, y, 96, c, lab, 1.0, k=pop(t, 6.5 + i * 0.1, 0.4), text_size=46)
        tag(ctx, "再跳回对应的 App", XA + 580, 500, 26, "#FFFFFF", "#7A5A3A", smooth(prog(t, 6.2, 6.6)))


APPS_NO = [("微信", "#07C160"), ("淘宝", "#FF5000"), ("支付宝", "#1677FF"), ("美团", "#FFC300"),
           ("小红书", "#FF2442"), ("App", "#9AA0AE"), ("App", "#8C93A3"), ("App", "#9AA0AE"),
           ("App", "#8C93A3")]   # 只列公开报道里点名的几家，其余用通用图标


def _part_b(ctx, t):
    a = smooth(prog(t, 7.4, 8.0))
    if a <= 0:
        return
    px, py = XB - 80, 470
    sx, sy, sw, sh = iphone(ctx, px, py, 740, a, "#F1EEF6")
    text(ctx, "豆包手机助手", px, sy + 20, 24, "#4D7CFE", a, "black")
    for i, (nm, c) in enumerate(APPS_NO):
        x = sx + 58 + (i % 3) * 100
        y = sy + 110 + (i // 3) * 150
        q = pop(t, 8.0 + i * 0.05, 0.4)
        app_tile(ctx, x, y, 78, c, nm[:2], a, k=q, text_size=24)
        st = 9.6 + i * 0.18
        k = clamp((t - st) / 0.25)
        if k > 0:
            sc = lerp(2.2, 1.0, ease_out(k))
            stamp(ctx, "不", x + 6, y + 6, 30, "#E5484D", a * min(1, k * 2), -0.2, sc)
    # 智能体的手指想点开 App
    u = prog(t, 8.4, 9.6)
    if 0 < u < 1:
        fx = sx + 58 + 100 * math.sin(u * 6)
        fy = sy + 110 + 120 * u * 2
        glow(ctx, fx, fy, 40, "#4D7CFE", 0.6 * a)
        circle(ctx, fx, fy, 16)
        fill(ctx, "#4D7CFE", a)
    # 计数器
    c = smooth(prog(t, 9.6, 10.0))
    if c > 0:
        n = int(lerp(0, 150, ease_out(prog(t, 9.6, 11.6))))
        with at(ctx, XB + 520, 380, 1.0):
            rrect(ctx, -230, -110, 460, 220, 32)
            fill(ctx, "#2B2233", 0.92 * a * c)
            text(ctx, f"{n} 多款", 0, -20, 78, "#FF6B6B", a * c, "black")
            text(ctx, "App 拒绝 AI 代操作", 0, 60, 30, "#FFFFFF", a * c, "bold")
        tag(ctx, "2026 年 10 月的公开统计", XB + 520, 540, 24, "#FFFFFF", "#4A4458", a * c)


LORDS = [("微信", "#07C160", -620, 0.9), ("淘宝", "#FF5000", -210, 1.05), ("抖音", "#161823", 210, 1.0),
         ("支付宝", "#1677FF", 620, 0.9)]


def _part_c(ctx, t):
    a = smooth(prog(t, 12.4, 13.2))
    if a <= 0:
        return
    for i, (nm, c, dx, s) in enumerate(LORDS):
        rise = ease_back(clamp((t - 13.2 - i * 0.25) / 0.6), 1.3)
        if rise <= 0:
            continue
        x = XC + dx
        h = 430 * s * rise
        ctx.save()
        ctx.rectangle(x - 300, 0, 600, G)
        ctx.clip()
        castle(ctx, x, G + (1 - rise) * 120, 330 * s, 430 * s, "#B9A58A", a, flag=c, flag_text=nm, t=t)
        ctx.restore()
        # 城里的"用户"
        for k in range(5):
            ph = (t * 0.4 + k / 5 + i * 0.2) % 1
            ux = x - 90 * s + (k % 5) * 45 * s
            circle(ctx, ux, G - 30 - abs(math.sin(ph * math.pi)) * 6, 10)
            fill(ctx, "#FFE29A", 0.8 * a * rise)
    l1 = smooth(prog(t, 15.0, 15.4))
    if l1 > 0:
        tag(ctx, "私域流量", XC - 420, 200, 36, "#FFFFFF", "#C42A30", a * l1)
    l2 = smooth(prog(t, 16.4, 16.8))
    if l2 > 0:
        tag(ctx, "互联网地主", XC + 420, 200, 36, "#3A2A00", "#FFD36B", a * l2)


def _part_d(ctx, t):
    a = smooth(prog(t, 19.4, 20.0))
    if a <= 0:
        return
    px, py = XD - 300, 470
    sx, sy, sw, sh = iphone(ctx, px, py, 640, a)
    ctx.save()
    rrect(ctx, sx, sy, sw, sh, 24)
    ctx.clip()
    ctx.set_source(lin(0, sy, 0, sy + sh, [(0, "#E9F1FF", a), (1, "#FCEFFF", a)]))
    ctx.paint()
    for i, (nm, c, ch) in enumerate((("Gmail", "#EA4335", "M"), ("地图", "#34A853", "图"), ("浏览器", "#FBBC05", "C"),
                                     ("视频", "#FF0000", "▶"), ("文档", "#4285F4", "文"), ("Gemini", "#6A4FD8", "G"))):
        q = pop(t, 20.4 + i * 0.12, 0.4)
        x = sx + 58 + (i % 3) * 90
        y = sy + 80 + (i // 3) * 120
        with at(ctx, x, y, q):
            rrect(ctx, -32, -32, 64, 64, 16)
            fill(ctx, c, a)
            text(ctx, ch, 0, 1, 30, "#FFFFFF", a, "black")
        text(ctx, nm, x, y + 50, 16, "#2B2233", a * q, "bold")
    ctx.restore()
    tag(ctx, "iPhone 上随便装谷歌 App", px, py - 380, 28, "#FFFFFF", "#4285F4", a * smooth(prog(t, 20.6, 21.0)))
    # 法院 + 法槌
    cx = XD + 360
    b = smooth(prog(t, 22.6, 23.2))
    if b > 0:
        ic_building(ctx, cx, 420, 420, a * b, t, "#E9E4F2")
        tag(ctx, "反垄断法", cx, 160, 40, "#FFFFFF", "#6A4FD8", a * b)
        hit = clamp((t - 23.3) / 0.35)
        rot = lerp(-0.9, 0.15, ease_in(hit)) if hit < 1 else 0.15 + 0.06 * math.exp(-(t - 23.65) * 6) * math.sin((t - 23.65) * 30)
        gavel(ctx, cx + 230, 560, 0.9, rot, a)
        if t > 23.65:
            ring_burst(ctx, t, 23.65, cx + 170, 640, 20, 160, "#FFFFFF", 0.5, 6)
    e = smooth(prog(t, 25.4, 25.8))
    if e > 0:
        with at(ctx, cx, 760, 1.0):
            rrect(ctx, -330, -40, 660, 80, 40)
            fill(ctx, "#2B2233", 0.9 * a * e)
            text(ctx, "封杀对手 → 可能被告上法庭", 0, 0, 32, "#FFD36B", a * e, "black")
    f = smooth(prog(t, 26.4, 26.8))
    if f > 0:
        tag(ctx, "微软反垄断案（2000 年前后）· 谷歌搜索垄断案（2024 年判决）", cx - 40, 850, 22, "#FFFFFF", "#4A4458",
            a * f)


def _part_e(ctx, t):
    a = smooth(prog(t, 28.6, 29.2))
    if a <= 0:
        return
    x0, y0 = XE - 640, 160
    rrect(ctx, x0 - 40, y0 - 50, 800, 380, 30)
    fill(ctx, "#FFFFFF", 0.92 * a)
    text(ctx, "开放网页语料里的语言占比", x0 + 360, y0, 30, "#2B2233", a, "black")
    items = [("英文", 46, "#4C8DFF", "≈ 46%"), ("中文", 5.5, "#FF6B6B", "< 6%"), ("其他语言", 48.5, "#B9B2C8", "其余")]
    hbars(ctx, items, x0, y0 + 90, 680, 78, prog(t, 29.4, 31.8), a, 30, vmax=50, label_w=160, stagger=0.25)
    text(ctx, "数据：Common Crawl 网页抓取的语言统计", x0 + 360, y0 + 310, 20, "#9A8FA8", a, "bold")
    # 锁在 App 里的中文内容
    b = smooth(prog(t, 33.0, 33.5))
    if b > 0:
        for i, (nm, c) in enumerate((("公众号文章", "#07C160"), ("短视频", "#161823"), ("种草笔记", "#FF2442"),
                                     ("问答", "#0084FF"))):
            q = pop(t, 33.2 + i * 0.25, 0.45)
            if q <= 0:
                continue
            x = XE - 520 + i * 300
            y = 690
            with at(ctx, x, y, q):
                rrect(ctx, -120, -70, 240, 140, 24)
                fill(ctx, c, a)
                text(ctx, nm, 0, -14, 30, "#FFFFFF", a, "black")
                ic_lock(ctx, 70, 30, 70, a, t)
        tag(ctx, "锁在 App 里：搜不到，也难以用来训练", XE - 70, 820, 26, "#FFFFFF", "#C42A30", a * b)


def _part_f(ctx, t):
    a = smooth(prog(t, 36.6, 37.2))
    if a <= 0:
        return
    # 碎片化的数据
    R = rng(31)
    for i in range(18):
        x = XF - 520 + R.uniform(-160, 1000)
        y = R.uniform(170, 520)
        rot = R.uniform(-0.6, 0.6) + math.sin(t + i) * 0.1
        with at(ctx, x, y + math.sin(t * 1.3 + i) * 8, 1.0, rot):
            rrect(ctx, -30, -22, 60, 44, 8)
            fill(ctx, ["#FF9F68", "#8B6CFF", "#2EC4B6", "#4C8DFF"][i % 4], 0.55 * a)
            circle(ctx, 30, 0, 9)
            fill(ctx, ["#FF9F68", "#8B6CFF", "#2EC4B6", "#4C8DFF"][i % 4], 0.55 * a)
    tag(ctx, "数据被切成碎片", XF + 40, 120, 30, "#FFFFFF", "#4A4458", a * smooth(prog(t, 37.2, 37.6)))
    # 卡住的飞轮
    j = smooth(prog(t, 39.6, 40.2))
    if j > 0:
        flywheel(ctx, XF + 420, 620, 200, ["用户", "反馈", "模型"], 0.3, ["#FF9F68", "#8B6CFF", "#2EC4B6"], a * j, None,
                 28, jam=1.0, t=t, center="转不起来", thick=80)
        # 锁链
        ctx.set_line_width(10)
        setc(ctx, "#9AA0AE", a * j)
        for k in range(6):
            ang = k * 0.9
            circle(ctx, XF + 420 + math.cos(ang) * 230, 620 + math.sin(ang) * 230, 18)
            ctx.stroke()


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
    out = [
        (1.0, "bubble", {"gain": 0.3}), (2.0, "error", {"gain": 0.3}),
        (3.4, "bubble", {"gain": 0.3, "pitch": 1.1}), (4.1, "click", {"gain": 0.3}),
        (4.8, "bubble", {"gain": 0.3, "pitch": 1.2}),
        (5.6, "whoosh_short", {"gain": 0.25}), (6.5, "pop", {"gain": 0.25}),
        (7.1, "whoosh_short", {"gain": 0.3}),
        (8.0, "shuffle", {"dur": 0.6, "gain": 0.2}), (8.4, "tick", {"gain": 0.2}), (8.9, "tick", {"gain": 0.2}),
    ]
    for i in range(9):
        out.append((9.6 + i * 0.18, "stamp", {"gain": 0.28}))
    out += [
        (9.6, "spinup", {"dur": 2.0, "gain": 0.18}),
        (12.3, "whoosh_short", {"gain": 0.3}),
        (13.2, "rumble", {"dur": 1.2, "gain": 0.35}), (13.3, "gate", {"gain": 0.3}),
        (15.0, "lock", {"gain": 0.35}), (16.4, "lock", {"gain": 0.35}),
        (19.1, "whoosh_short", {"gain": 0.3}),
        (20.4, "pop", {"gain": 0.25}), (20.6, "pop", {"gain": 0.25, "pitch": 1.2}),
        (22.6, "chime", {"gain": 0.3}), (23.65, "knock", {"gain": 0.6}), (23.7, "thud", {"gain": 0.4}),
        (25.4, "stamp", {"gain": 0.3}),
        (28.2, "whoosh_short", {"gain": 0.3}),
        (29.4, "rise", {"dur": 2.0, "gain": 0.2}),
        (33.2, "lock", {"gain": 0.3}), (33.45, "lock", {"gain": 0.3}), (33.7, "lock", {"gain": 0.3}),
        (33.95, "lock", {"gain": 0.3}),
        (36.3, "whoosh_short", {"gain": 0.3}),
        (37.0, "shuffle", {"dur": 1.4, "gain": 0.22}),
        (37.9, "stretch", {"dur": 1.6, "gain": 0.3}),
        (39.6, "ratchet", {"dur": 1.4, "gain": 0.3}), (40.4, "womp", {"gain": 0.35}),
    ]
    return out
