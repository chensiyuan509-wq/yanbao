"""03 · 从聊天到智能体：产品井喷 → 聊天机器人 → 编程助手 → MCP 万能插头 → 各家支持、捐给 Linux 基金会 →
会干活的编程智能体 → 开源社区（OpenCode、OpenClaw）。Claude 站在左边讲解，右侧面板轮播滑入。"""
import math

from ..core import (TAU, Cam, at, box_shadow, circle, clamp, ease_back, ease_in, ease_io, ease_out,
                    ease_out5, fill, glow, lerp, lin, line, pop, prog, rad, ring_burst, rng, rrect, setc,
                    smooth, sparkle_burst, star4, stroke_pts, text, text_w, view, check_mark, bezier_pts,
                    polyline_partial)
from ..icons import (ic_brain, ic_building, ic_chatgpt, ic_docs, ic_github, ic_notion, ic_openclaw, ic_plug,
                     ic_slack, ic_calendar, ic_server)
from ..props import app_tile, bg_grad, gemini_star, grid_dots, name_card, tag
from ..ui import bubble, window, term_lines
from .common import host, mini_icon, talk_lines

DUR = 44.5
CHAPTER = ("03", "从聊天到智能体")

VO = [
    (1.0, '有了模型和算力，产品开始{井喷}。'),
    (4.2, '先是聊天机器人：ChatGPT、Claude、Gemini、Grok；'),
    (9.2, '再是编程助手：GitHub Copilot、Cursor。'),
    (13.1, '2024 年底，Anthropic 开源了 {MCP} 协议，像给 AI 装上「万能插头」，一插就能连上各种软件和数据。'),
    (22.6, 'OpenAI、谷歌、微软纷纷支持，后来 MCP 又被捐给了 {Linux 基金会}。'),
    (29.8, 'AI 从「会聊天」变成了「会干活」：Claude Code、Codex 能自己写代码、跑测试；'),
    (36.6, '开源社区更热闹：OpenCode 能随意切换模型，OpenClaw 让人人都能拥有{私人智能体}。'),
]

MX, MY = 330, 930              # 主持人位置
PCX, PCY = 1140, 500           # 面板中心
PANELS = [(3.9, 8.9), (8.9, 12.8), (12.8, 22.4), (22.4, 29.5), (29.5, 36.3), (36.3, 44.5)]

P = (host(MX, MY, 0.62, "excited", seed=7.7)
     .look(0, 0.5, -0.9).hop(1.2, 50, 0.42).hop(2.3, 40, 0.38)
     .expr(4.1, "smile").look(4.2, 0.9, -0.6).point(4.3, "r", 0.55, 50).arms_down(6.0)
     .expr(9.1, "curious").look(9.1, 1.0, -0.5)
     .expr(13.0, "awe").look(13.0, 1.0, -0.6).point(15.5, "r", 0.5, 60).arms_down(17.5)
     .expr(19.6, "starry")
     .expr(22.5, "happy").look(22.5, 1.0, -0.5).nod(24.6, 2)
     .expr(27.0, "proud")
     .expr(29.7, "excited").look(29.7, 1.0, -0.5).expr(30.3, "focused").type(30.4, 35.5)
     .expr(35.9, "grin")
     .expr(36.5, "starry").look(36.5, 1.0, -0.6).cheer(40.8, 42.4).expr(42.5, "proud"))
talk_lines(P, VO, [0, 1, 2, 3, 4, 6], smile=0.35)

CAM = Cam([
    (0.0, (960, 560, 1.08)),
    (3.6, (960, 545, 1.0)),
    (12.8, (980, 545, 1.02)),
    (13.6, (1000, 540, 1.04), ease_io),
    (22.0, (1010, 540, 1.06)),
    (22.8, (990, 540, 1.0), ease_io),
    (29.5, (1000, 545, 1.03)),
    (36.3, (980, 545, 1.0), ease_io),
    (44.5, (990, 540, 1.04)),
], drift=5, seed=15.0)


def _panel_xform(t, i):
    """面板进出：从右边滑入，向左边滑出。返回 (x 偏移, 透明度, 缩放)。"""
    t0, t1 = PANELS[i]
    if t < t0 - 0.05 or t > t1 + 0.6:
        return None
    ui = ease_out5(clamp((t - t0) / 0.65))
    uo = ease_in(clamp((t - t1) / 0.55)) if i < len(PANELS) - 1 else 0.0
    dx = (1 - ui) * 900 - uo * 1100
    a = min(clamp((t - t0) / 0.35), 1 - clamp((t - t1) / 0.45)) if i < len(PANELS) - 1 else clamp((t - t0) / 0.35)
    return dx, a, 0.94 + 0.06 * ui


def _bg(ctx, t, cam):
    bg_grad(ctx, "#F3EEFF", "#FFE7DA", "#FBEFF6", 0.55)
    with view(ctx, cam, 0.4):
        grid_dots(ctx, -400, -300, 2400, 1400, 64, "#8B6CFF", 0.08, 2.6, drift=(t * 8, 0))
    ctx.set_source(rad(1200, 500, 50, 900, [(0, "#FFFFFF", 0.55), (1, "#FFFFFF", 0)]))
    ctx.paint()


def _fountain(ctx, t):
    """开场：产品图标从地面喷涌而出。"""
    a = 1 - smooth(prog(t, 3.7, 4.3))
    if a <= 0:
        return
    cx, cy = 1150, 860
    glow(ctx, cx, cy, 420, "#FFB27A", 0.5 * a)
    R = rng(12)
    cols = ["#10A37F", "#D97757", "#4C8DFF", "#2B2233", "#8B6CFF", "#FF6B9A", "#2EC4B6", "#FFC857"]
    labels = ["Chat", "Code", "Agent", "MCP", "Search", "Office", "Image", "Voice"]
    for i in range(16):
        st = 1.0 + i * 0.12
        u = clamp((t - st) / 1.6)
        if u <= 0:
            continue
        ang = -math.pi / 2 + R.uniform(-0.9, 0.9)
        sp = R.uniform(560, 860)
        x = cx + math.cos(ang) * sp * u
        y = cy + math.sin(ang) * sp * u + 420 * u * u
        k = pop(t, st, 0.4)
        with at(ctx, x, y, k * 0.9, (u - 0.5) * R.uniform(-0.6, 0.6)):
            app_tile(ctx, 0, 0, 100, cols[i % 8], labels[i % 8], a)
    text(ctx, "产品井喷", cx, 200, 80, "#2B2233", a * smooth(prog(t, 1.4, 1.9)), "black")


CHATS = [("ChatGPT", "#10A37F", "OpenAI"), ("Claude", "#D97757", "Anthropic"), ("Gemini", "#5B6CFF", "谷歌"),
         ("Grok", "#1D1D24", "xAI")]


def _p_chat(ctx, t):
    tag(ctx, "第一站 · 聊天机器人", 0, -330, 32, "#FFFFFF", "#8B6CFF")
    for i, (nm, c, mk) in enumerate(CHATS):
        q = pop(t, 4.3 + i * 0.85, 0.5)
        if q <= 0:
            continue
        x = -480 + (i % 2) * 520 + 220
        y = -150 + (i // 2) * 270
        with at(ctx, x - 220, y, q):
            box_shadow(ctx, -230, -100, 460, 200, 26, blur=24, a=0.18, dy=10)
            rrect(ctx, -230, -100, 460, 200, 26)
            fill(ctx, "#FFFFFF")
            if nm == "Gemini":
                gemini_star(ctx, -160, -30, 44, 1.0, t * 0.5)
            elif nm == "ChatGPT":
                ic_chatgpt(ctx, -160, -30, 86, 1.0, t)
            else:
                app_tile(ctx, -160, -30, 86, c, nm[0])
            text(ctx, nm, -98, -48, 40, "#2B2233", 1, "black", "l")
            text(ctx, mk, -98, -6, 24, "#7A7186", 1, "bold", "l")
            bubble(ctx, -200, 34, 400, 48, mix_hex(c), 1.0, "none", shadow=0)
            n = int(clamp((t - 4.6 - i * 0.85) * 14, 0, 12))
            text(ctx, "你好！有什么可以帮你？"[:n], -184, 58, 24, "#2B2233", 1, "bold", "l")


def mix_hex(c):
    from ..core import mix
    return mix(c, "#FFFFFF", 0.85)


def _p_code(ctx, t):
    tag(ctx, "第二站 · 编程助手", 0, -330, 32, "#FFFFFF", "#8B6CFF")
    cx, cy, cw, ch = window(ctx, -420, -260, 840, 420, "main.py", 1.0, "dark")
    lines = [("def total_price(items):", "#7CC6FF"), ("    sum = 0", "#FFFFFF"), ("    for it in items:", "#FFC857")]
    for i, (s, c) in enumerate(lines):
        text(ctx, s, cx + 30, cy + 40 + i * 46, 28, c, 1, "mono", "l")
    # 灰色的"幽灵建议" → Tab 接受
    ghost = ["        sum += it.price * it.qty", "    return sum"]
    acc = smooth(prog(t, 11.2, 11.5))
    gk = clamp((t - 9.9) / 0.6)
    for i, s in enumerate(ghost):
        n = int(len(s) * gk)
        col = "#8A8496" if acc < 0.5 else "#B6FF6B"
        text(ctx, s[:n], cx + 30, cy + 40 + (3 + i) * 46, 28, col, 1, "mono", "l")
    if 10.4 < t < 11.4:
        tag(ctx, "按 Tab 接受建议", cx + cw - 150, cy + ch - 40, 24, "#2B2233", "#FFD36B")
    name_card(ctx, "GitHub Copilot", -230, 250, "#2B3137", 30, 1.0, pop(t, 9.6, 0.5))
    name_card(ctx, "Cursor", 210, 250, "#3A3A48", 30, 1.0, pop(t, 10.6, 0.5))


APPS = [("GitHub", ic_github), ("Slack", ic_slack), ("文档", ic_docs), ("日历", ic_calendar), ("Notion", ic_notion),
        ("数据库", ic_server)]


def _hub(ctx, t, hx, hy, k, lit):
    """MCP 枢纽：圆角底座 + 一圈插口 + 连向各个应用。"""
    for i, (nm, fn) in enumerate(APPS):
        ax, ay = hx + 380, hy - 240 + i * 96
        q = pop(t, 15.2 + i * 0.15, 0.45) * k
        if q <= 0:
            continue
        lv = clamp(lit * 6 - i * 0.6)
        pts = bezier_pts((hx + 90, hy), (hx + 220, hy), (ax - 160, ay), (ax - 50, ay), 30)
        stroke_pts(ctx, pts, 6, "#FF9F68" if lv > 0.5 else "#D9D2E6", q)
        if lv > 0.5:
            ph = (t * 1.2 + i * 0.17) % 1
            from ..core import point_on
            (px, py), _ = point_on(pts, ph)
            glow(ctx, px, py, 18, "#FFB27A", 0.9 * q)
        with at(ctx, ax, ay, q * 0.62):
            fn(ctx, 0, 0, 120, 1.0, t)
        text(ctx, nm, ax + 60, ay, 24, "#2B2233", q, "bold", "l")
    rrect(ctx, hx - 110, hy - 120, 220, 240, 40)
    ctx.set_source(lin(0, hy - 120, 0, hy + 120, [(0, "#FFB27A", k), (1, "#E07A4F", k)]))
    ctx.fill()
    text(ctx, "MCP", hx, hy - 20, 64, "#FFFFFF", k, "black")
    text(ctx, "万能插头", hx, hy + 50, 28, "#FFFFFF", k, "bold")


def _p_mcp(ctx, t):
    tag(ctx, "第三站 · MCP：AI 的万能插头", 0, -360, 32, "#FFFFFF", "#E07A4F")
    tag(ctx, "2024.11 · Anthropic 开源", 0, -300, 26, "#2B2233", "#FFE3C8", 1.0)
    # 左：AI 大脑 + 插头
    bx, by = -470, 40
    glow(ctx, bx, by, 220, "#8B6CFF", 0.3)
    ic_brain(ctx, bx, by, 220, 1.0, t, "#8B6CFF", 0.4)
    u = ease_out5(prog(t, 14.4, 15.2))
    hx = -20
    px = lerp(bx + 100, hx - 170, u)
    stroke_pts(ctx, [(bx + 100, by), (px, by)], 14, "#6C63FF", 1.0)
    ic_plug(ctx, px + 40, by, 110, 1.0, t, "#6C63FF", math.pi / 2)
    if t > 15.2:
        sparkle_burst(ctx, t, 15.2, hx - 120, by, 10, 140, "#FFE7A3", 0.7, 3, 18)
    _hub(ctx, t, hx, by, smooth(prog(t, 13.4, 14.0)), smooth(prog(t, 15.4, 17.6)))
    if t > 19.4:
        tag(ctx, "一插就能连上各种软件和数据", 0, 330, 30, "#FFFFFF", "#8B6CFF", smooth(prog(t, 19.4, 19.8)))


def _p_support(ctx, t):
    tag(ctx, "各家都来支持", 0, -360, 32, "#FFFFFF", "#E07A4F")
    hx, hy = 0, 120
    lf = smooth(prog(t, 25.8, 26.6))
    # Linux 基金会的大楼罩住 MCP
    if lf > 0:
        with at(ctx, hx, hy - 40, 0.9 + 0.1 * lf):
            glow(ctx, 0, 0, 520, "#4C8DFF", 0.25 * lf)
            ic_building(ctx, 0, -40, 620, lf, t, "#DCE6FF")
        tag(ctx, "Linux 基金会 · 智能体 AI 基金会（AAIF）", hx, hy - 330, 30, "#FFFFFF", "#2B3A66", lf)
        tag(ctx, "2025.12 · MCP 捐赠", hx, hy - 270, 24, "#2B3A66", "#DCE6FF", lf)
    rrect(ctx, hx - 110, hy - 100, 220, 200, 36)
    ctx.set_source(lin(0, hy - 100, 0, hy + 100, [(0, "#FFB27A"), (1, "#E07A4F")]))
    ctx.fill()
    text(ctx, "MCP", hx, hy, 60, "#FFFFFF", 1, "black")
    peers = [("OpenAI", "#10A37F", -520, -60), ("谷歌", "#4285F4", -520, 170), ("微软", "#00A4EF", 520, -60),
             ("更多公司…", "#8B6CFF", 520, 170)]
    for i, (nm, c, dx, dy) in enumerate(peers):
        q = pop(t, 22.9 + i * 0.5, 0.5)
        if q <= 0:
            continue
        u = ease_out(prog(t, 23.2 + i * 0.5, 23.9 + i * 0.5))
        ex = hx + (-110 if dx < 0 else 110)
        sx = hx + dx * 0.62
        stroke_pts(ctx, [(sx, hy + dy * 0.5), (lerp(sx, ex, u), lerp(hy + dy * 0.5, hy + dy * 0.18, u))], 8, c, q)
        if u >= 1:
            circle(ctx, ex, hy + dy * 0.18, 9)
            fill(ctx, c)
        name_card(ctx, nm, hx + dx, hy + dy * 0.5, c, 32, 1.0, q, w=230)


def _p_agent(ctx, t):
    tag(ctx, "从「会聊天」到「会干活」", 0, -360, 32, "#FFFFFF", "#2B2233")
    cx, cy, cw, ch = window(ctx, -470, -290, 940, 520, "终端 · 编程智能体", 1.0, "dark")
    steps = [("> 帮我修好登录页的 bug，并跑一遍测试", "#FFD36B", 30.4),
             ("读取 12 个相关文件", "#CFE7C0", 31.3), ("定位问题：会话过期时间写错", "#CFE7C0", 32.0),
             ("修改 auth.py（+6 −2）", "#CFE7C0", 32.7), ("运行测试：48 / 48 通过", "#7CFFB2", 33.5),
             ("提交代码，等你审阅", "#7CFFB2", 34.3)]
    for i, (s, c, t0) in enumerate(steps):
        if t < t0:
            break
        y = cy + 52 + i * 70
        n = int(clamp((t - t0) * 30, 0, len(s)))
        x = cx + 40
        if i > 0:
            q = clamp((t - t0 - 0.3) / 0.25)
            circle(ctx, x + 14, y, 15)
            fill(ctx, "#3CCB7F", q)
            check_mark(ctx, x + 14, y, 18, "#FFFFFF", q)
            x += 46
        text(ctx, s[:n], x, y, 30, c, 1, "bold" if i else "mono", "l")
    name_card(ctx, "Claude Code", -240, 300, "#D97757", 30, 1.0, pop(t, 30.6, 0.5), w=280)
    name_card(ctx, "Codex", 200, 300, "#10A37F", 30, 1.0, pop(t, 31.4, 0.5), w=200)


MODELS = ["Claude", "GPT", "Gemini", "Qwen", "DeepSeek", "Kimi", "GLM"]


def _p_open(ctx, t):
    tag(ctx, "开源社区", 0, -360, 32, "#FFFFFF", "#2B2233")
    # OpenCode：随意切换模型
    lx = -300
    box_shadow(ctx, lx - 260, -270, 520, 420, 28, blur=26, a=0.18, dy=10)
    rrect(ctx, lx - 260, -270, 520, 420, 28)
    fill(ctx, "#1E1C26")
    text(ctx, "OpenCode", lx, -220, 40, "#FFFFFF", 1, "black")
    text(ctx, "开源编程智能体 · 换模型就像换电池", lx, -170, 22, "#B9B2C8", 1, "bold")
    sel = int(max(0, t - 37.2) / 0.55) % len(MODELS)
    for i, m in enumerate(MODELS):
        y = -110 + i * 36
        if i == sel:
            rrect(ctx, lx - 200, y - 17, 400, 34, 10)
            fill(ctx, "#3CCB7F", 0.9)
        text(ctx, ("▶ " if i == sel else "   ") + m, lx - 180, y, 26, "#FFFFFF", 1, "mono", "l")
    # OpenClaw：人人都有私人智能体
    rx = 330
    q = pop(t, 39.2, 0.55)
    if q > 0:
        with at(ctx, rx, -60, q):
            glow(ctx, 0, 0, 260, "#FF6B5B", 0.25)
            ic_openclaw(ctx, 0, -60, 170, 1.0, t)
            text(ctx, "OpenClaw", 0, 70, 44, "#2B2233", 1, "black")
            text(ctx, "开源的私人智能体", 0, 118, 24, "#7A7186", 1, "bold")
            for i, (nm, c) in enumerate((("聊天", "#25D366"), ("邮箱", "#E5484D"), ("日程", "#4C8DFF"),
                                         ("文件", "#FFB547"))):
                k = pop(t, 40.0 + i * 0.2, 0.4)
                if k > 0:
                    app_tile(ctx, -150 + i * 100, 200, 76 * k, c, nm, 1.0)
        stars = int(lerp(0, 10, ease_out(prog(t, 39.6, 41.8))))
        tag(ctx, f"GitHub 星标 {stars} 万+", rx, 310, 28, "#FFFFFF", "#2B2233", q)


DRAW = [_p_chat, _p_code, _p_mcp, _p_support, _p_agent, _p_open]


def draw(ctx, t):
    cam = CAM.at(t)
    _bg(ctx, t, cam)
    with view(ctx, cam, 1.0):
        _fountain(ctx, t)
        for i, fn in enumerate(DRAW):
            xf = _panel_xform(t, i)
            if not xf:
                continue
            dx, a, k = xf
            if a <= 0.003:
                continue
            ctx.push_group()
            with at(ctx, PCX + dx, PCY, k * 1.08):
                fn(ctx, t)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(a)
        P.draw(ctx, t)


def sfx():
    out = [(1.0, "rumble", {"dur": 0.8, "gain": 0.3}), (1.1, "sparkle", {"dur": 2.0, "gain": 0.3})]
    for i in range(10):
        out.append((1.0 + i * 0.2, "pop", {"gain": 0.18, "pitch": 1.0 + (i % 5) * 0.12}))
    for st in (3.9, 8.9, 12.8, 22.4, 29.5, 36.3):
        out.append((st - 0.05, "swish", {"gain": 0.3}))
    out += [
        (4.3, "bubble", {"gain": 0.25}), (5.15, "bubble", {"gain": 0.25}), (6.0, "bubble", {"gain": 0.25}),
        (6.85, "bubble", {"gain": 0.25}),
        (9.9, "typing", {"dur": 0.8, "gain": 0.2}), (11.2, "ding", {"gain": 0.35}),
        (14.4, "slide", {"gain": 0.3}), (15.2, "plug", {"gain": 0.45}), (15.25, "sparkle", {"dur": 1.0, "gain": 0.25}),
        (15.4, "stream", {"dur": 2.4, "gain": 0.18}),
        (22.9, "connect", {"gain": 0.3}), (23.4, "connect", {"gain": 0.3, "pitch": 1.1}),
        (23.9, "connect", {"gain": 0.3, "pitch": 1.2}), (24.4, "connect", {"gain": 0.3, "pitch": 1.3}),
        (25.8, "chime", {"gain": 0.35}),
        (30.4, "typing", {"dur": 1.2, "gain": 0.2}),
        (31.6, "check", {"gain": 0.25}), (32.3, "check", {"gain": 0.25, "pitch": 1.1}),
        (33.0, "check", {"gain": 0.25, "pitch": 1.2}), (33.8, "success", {"gain": 0.35}),
        (34.6, "check", {"gain": 0.25, "pitch": 1.3}),
        (37.2, "click", {"gain": 0.2}), (37.75, "click", {"gain": 0.2}), (38.3, "click", {"gain": 0.2}),
        (38.85, "click", {"gain": 0.2}),
        (39.2, "pop_big", {"gain": 0.35}),
        (40.0, "pop", {"gain": 0.25}), (40.2, "pop", {"gain": 0.25, "pitch": 1.2}),
        (40.4, "pop", {"gain": 0.25, "pitch": 1.35}), (40.6, "pop", {"gain": 0.25, "pitch": 1.5}),
        (40.8, "success", {"gain": 0.3}),
    ]
    return out
