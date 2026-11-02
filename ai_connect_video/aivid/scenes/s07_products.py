"""第三章 · 产品形态巡礼：ChatGPT → Codex / Claude Code → OpenCode → OpenClaw → WorkBuddy → Muse。

镜头逐站平移，小橙一路跳着当导游；最后所有产品连向工具与数据，点出"连接 = 能力"。
"""
import math

from ..core import (TAU, W, H, Cam, at, circle, clamp, ease_back, ease_in, ease_io, ease_out,
                    fill, glow, kf, lerp, line, lin, pop, poly, prog, rad, rrect, setc, smooth,
                    text, text_w, view, sparkle_burst, ring_burst, bokeh, check_mark, stroke_pts,
                    bezier_pts, polyline_partial, font)
from ..icons import (ic_browser, ic_calendar, ic_chatgpt, ic_claude_code, ic_codex, ic_docs,
                     ic_folder, ic_github, ic_gmail, ic_instagram, ic_laptop, ic_muse, ic_notion,
                     ic_openclaw, ic_opencode, ic_phone, ic_sheets, ic_slack, ic_terminal,
                     ic_workbuddy, ic_tasks)
from ..mascot import Puppet
from ..ui import bubble, card, pill, typing_dots, window, table, lines_block

DUR = 40.5
CHAPTER = ("03", "产品形态巡礼")

SUBS = [
    (1.0, 6.2, "{ChatGPT}：一个对话框，让全世界第一次认识了大模型。"),
    (6.4, 13.0, "{Codex}、{Claude Code}：住在终端里的编程智能体，自己读项目、写代码、跑测试。"),
    (13.2, 18.4, "{OpenCode}：开源的编程智能体，Claude、GPT、Gemini 等模型随意切换。"),
    (18.6, 24.4, "{OpenClaw}：开源的个人智能体，装在自己电脑上，用聊天软件指挥它干活。"),
    (24.6, 29.8, "{WorkBuddy}（腾讯）：桌面办公智能体，帮你整理文档、处理表格。"),
    (30.0, 35.4, "{Muse}（Meta）：个人智能体，连上你的邮箱、文档和日程，替你跑腿。"),
    (35.6, 40.3, "形态在变，核心不变：{能连多少工具和数据，就能干多少活}。"),
]

GAP = 1500
SX = [960 + i * GAP for i in range(6)]
WRAP_X = 960 + 6 * GAP
PANS = [(5.9, 6.9), (12.8, 13.8), (18.1, 19.1), (24.1, 25.1), (29.5, 30.5), (35.1, 36.2)]
T_ARR = [0.0] + [b for (a, b) in PANS]
CY = 450
MASCOT_Y = 905

P = Puppet(SX[0] - 720, MASCOT_Y, 0.56, "curious", seed=7.7).look(0, 1.0, -0.5)
P.expr(3.3, "happy").nod(3.6)
for i, (a, b) in enumerate(PANS[:5]):
    P.move(a + 0.05, b - 0.05, SX[i + 1] - 720, MASCOT_Y, walk=False, ease=ease_io).hop(a + 0.05, 170, b - a - 0.1)
    P.land(b - 0.05, 0.12)
P.expr(6.9, "excited").look(6.9, 1.0, -0.6)
P.expr(10.6, "wink").fx(10.6, ("heart",)).fx(12.4, None)
P.expr(13.8, "think").look(13.8, 1.0, -0.3).expr(15.6, "surprised").expr(16.6, "excited")
P.expr(19.1, "excited").expr(21.5, "proud")
P.expr(25.1, "smile").nod(27.5).expr(28.0, "happy")
P.expr(30.5, "excited")
P.move(35.15, 36.15, WRAP_X - 760, MASCOT_Y + 10, walk=False, ease=ease_io).hop(35.15, 170, 1.0).land(36.15, 0.12)
P.expr(36.2, "curious").look(36.2, 1.0, -0.8).expr(38.0, "determined").fx(38.0, ("sparkle",))

_cam = [(0.0, (SX[0] + 40, 500, 1.0))]
for i, (a, b) in enumerate(PANS):
    tgt = SX[i + 1] if i < 5 else WRAP_X
    hold_z = 1.035
    _cam.append((a, (_cam[-1][1][0] + 20, 500, hold_z)))
    _cam.append((b, (tgt + 40, 500, 1.0), ease_io))
_cam.append((DUR, (WRAP_X + 50, 495, 1.04)))
CAM = Cam(_cam, drift=5, seed=17.0)


def draw(ctx, t):
    ctx.set_source(lin(0, 0, 0, H, [(0, "#120E22"), (0.6, "#221A38"), (1, "#2E2142")]))
    ctx.paint()
    cam = CAM.at(t)
    with view(ctx, cam, 0.35):
        bokeh(ctx, t, 30, 71, ("#8B6CFF", "#FF9F68", "#4C8DFF", "#2EC4B6"),
              area=(-600, -200, W + GAP * 6 * 0.35 + 1200, H + 400), r=(30, 100), a=(0.05, 0.14))
    # 舞台地面（屏幕空间的透视线 + 世界空间移动）
    floor(ctx, cam)
    with view(ctx, cam):
        lo, hi = cam[0] - 1400, cam[0] + 1400
        for i, x in enumerate(SX):
            if lo < x < hi:
                station(ctx, i, x, t)
        if t > 34.0:
            draw_wrap(ctx, t)
        P.draw(ctx, t)
    # 顶部聚光
    ctx.set_source(rad(W / 2, -200, 0, 1100, [(0, "#FFF2D9", 0.16), (1, "#FFF2D9", 0)]))
    ctx.paint()


def floor(ctx, cam):
    y0 = 790
    ctx.set_source(lin(0, y0, 0, H, [(0, "#2C2245", 0.0), (0.2, "#2C2245", 0.85), (1, "#18122A", 1)]))
    ctx.rectangle(0, y0, W, H - y0)
    ctx.fill()
    off = (cam[0] * 0.9) % 160
    ctx.set_line_width(2)
    for k in range(-14, 16):
        xb = W / 2 + (k * 160 - off) * 2.4
        xt = W / 2 + (k * 160 - off) * 0.9
        setc(ctx, "#8B6CFF", 0.10)
        ctx.move_to(xt, y0 + 30)
        ctx.line_to(xb, H)
        ctx.stroke()


# ---------------------------------------------------------------- 卡片外壳

def shell(ctx, x, y, w, h, a, icon, name, maker, tags, t, accent):
    card(ctx, x - w / 2, y - h / 2, w, h, 40, "#FFFFFF", a, shadow=0.45, blur=50, dy=24)
    # 顶部彩条
    ctx.save()
    rrect(ctx, x - w / 2, y - h / 2, w, h, 40)
    ctx.clip()
    ctx.rectangle(x - w / 2, y - h / 2, w, 12)
    setc(ctx, accent, a)
    ctx.fill()
    ctx.restore()
    lx = x - w / 2 + 230
    glow(ctx, lx, y - 150, 170, accent, 0.25 * a)
    icon(ctx, lx, y - 150, 170, a, t)
    text(ctx, name, lx, y + 0, 56 if text_w(ctx, name, 56, "black") < 400 else 46, "#2B2233", a, "black")
    text(ctx, maker, lx, y + 60, 32, "#8A8296", a, "bold")
    for j, tg in enumerate(tags):
        pill(ctx, tg, lx, y + 130 + j * 62, 28, accent, accent, a, 0.14, weight="bold")


def station(ctx, i, x, t):
    lt = t - T_ARR[i] + 0.2      # 本站本地时间
    a = smooth(prog(lt, -0.6, 0.0)) if i > 0 else smooth(prog(t, 0.0, 0.5))
    if a <= 0:
        a = 0.25
    k = ease_back(prog(lt, -0.4, 0.3), 1.2) if i > 0 else ease_back(prog(t, 0.0, 0.6), 1.2)
    with at(ctx, x, CY, 0.9 + 0.1 * k):
        if i == 0:
            st_chatgpt(ctx, 0, 0, lt, a, t)
        elif i == 1:
            st_code(ctx, 0, 0, lt, a, t)
        elif i == 2:
            st_opencode(ctx, 0, 0, lt, a, t)
        elif i == 3:
            st_openclaw(ctx, 0, 0, lt, a, t)
        elif i == 4:
            st_workbuddy(ctx, 0, 0, lt, a, t)
        elif i == 5:
            st_muse(ctx, 0, 0, lt, a, t)


CW, CH = 1180, 640


def _panel(ctx, x, y, w, h, a, dark=False):
    rrect(ctx, x, y, w, h, 28)
    fill(ctx, "#1E1B26" if dark else "#F5F2F9", a)


# ---------------------------------------------------------------- 各站

def st_chatgpt(ctx, x, y, lt, a, t):
    shell(ctx, x, y, CW, CH, a, ic_chatgpt, "ChatGPT", "OpenAI · 2022.11", ["对话助手", "每周约 9 亿人在用"], t, "#19C39C")
    px, py, pw, ph = x - 130, y - 270, 680, 540
    _panel(ctx, px, py, pw, ph, a)
    # 用户提问
    k = pop(lt, 1.4, 0.4)
    if k > 0:
        with at(ctx, px + pw - 40, py + 90, k):
            bw = text_w(ctx, "什么是大模型？", 34, "bold") + 64
            bubble(ctx, -bw, -40, bw, 80, "#19C39C", a, tail="right", r=30, shadow=0.1)
            text(ctx, "什么是大模型？", -bw / 2, 0, 34, "#FFFFFF", a, "bold")
    if 2.1 < lt < 3.0:
        bubble(ctx, px + 40, py + 190, 150, 72, "#FFFFFF", a, tail="left", r=30, shadow=0.1)
        typing_dots(ctx, px + 115, py + 226, t, "#9AA0AE", a, 9)
    ak = ease_out(prog(lt, 3.0, 3.4))
    if ak > 0:
        bubble(ctx, px + 40, py + 190, pw - 120, 290, "#FFFFFF", a * ak, tail="left", r=30, shadow=0.1)
        lines = ["大模型就像一个读过海量", "文字的「接龙高手」，", "能聊天、写作、翻译……"]
        for j, s in enumerate(lines):
            n = int(len(s) * prog(lt, 3.2 + j * 0.55, 3.75 + j * 0.55))
            text(ctx, s[:n], px + 80, py + 250 + j * 72, 36, "#2B2233", a, "bold", "l")


def _term(ctx, x, y, w, h, title, lines, lt, a, t, accent):
    rrect(ctx, x, y, w, h, 26)
    fill(ctx, "#1C1A24", a)
    ctx.save()
    rrect(ctx, x, y, w, h, 26)
    ctx.clip()
    ctx.rectangle(x, y, w, 52)
    fill(ctx, "#2A2735", a)
    ctx.restore()
    for k, c in enumerate(("#FF6159", "#FFBD2E", "#28C941")):
        circle(ctx, x + 30 + k * 24, y + 26, 7.5)
        fill(ctx, c, a)
    text(ctx, title, x + w / 2, y + 26, 24, "#A9A4B8", a, "medium")
    for j, (s, col, t0) in enumerate(lines):
        if lt < t0:
            break
        n = min(len(s), int((lt - t0) * 34))
        yy = y + 100 + j * 56
        text(ctx, s[:n], x + 34, yy, 30, col, a, "mono", "l")
        if n < len(s):
            cw = text_w(ctx, s[:n], 30, "mono")
            rrect(ctx, x + 36 + cw, yy - 16, 16, 32, 2)
            fill(ctx, col, a)


def st_code(ctx, x, y, lt, a, t):
    w2, h2 = 700, 660
    for side, (icon, name, maker, accent, lines) in enumerate((
        (ic_codex, "Codex", "OpenAI", "#6C8CFF",
         [("$ codex", "#C9C4D6", 0.5), ("> 给登录页补上单元测试", "#FFFFFF", 0.9),
          ("✓ 读取了 12 个文件", "#7CFFB2", 2.0), ("+ tests/login.test.js", "#7CFFB2", 2.7),
          ("✓ 18 个测试全部通过", "#7CFFB2", 3.6)]),
        (ic_claude_code, "Claude Code", "Anthropic", "#E88E64",
         [("$ claude", "#C9C4D6", 0.8), ("> 修好支付页的金额 bug", "#FFFFFF", 1.2),
          ("● 正在阅读整个项目…", "#FFC65C", 2.2), ("- if (total = 0)", "#FF7A85", 3.0),
          ("+ if (total === 0)", "#7CFFB2", 3.5), ("✓ 测试通过，已提交", "#7CFFB2", 4.3)]),
    )):
        cx = x + 60 + (side - 0.5) * (w2 + 40)
        card(ctx, cx - w2 / 2, y - h2 / 2, w2, h2, 40, "#FFFFFF", a, shadow=0.45, blur=50, dy=24)
        ctx.save()
        rrect(ctx, cx - w2 / 2, y - h2 / 2, w2, h2, 40)
        ctx.clip()
        ctx.rectangle(cx - w2 / 2, y - h2 / 2, w2, 12)
        fill(ctx, accent, a)
        ctx.restore()
        icon(ctx, cx - w2 / 2 + 90, y - h2 / 2 + 92, 104, a, t)
        text(ctx, name, cx - w2 / 2 + 166, y - h2 / 2 + 74, 48, "#2B2233", a, "black", "l")
        text(ctx, maker + " · 编程智能体", cx - w2 / 2 + 168, y - h2 / 2 + 122, 28, "#8A8296", a, "bold", "l")
        _term(ctx, cx - w2 / 2 + 30, y - h2 / 2 + 170, w2 - 60, h2 - 200, "终端", lines, lt - side * 0.3, a, t, accent)
        if side == 1 and lt > 4.0:
            hk = pop(lt, 4.3, 0.4)
            with at(ctx, cx + w2 / 2 - 60, y - h2 / 2 + 70, hk):
                circle(ctx, 0, 0, 34)
                fill(ctx, "#3CCB7F", a)
                check_mark(ctx, 0, 2, 40, "#FFFFFF", prog(lt, 4.4, 4.7), a)


MODELS = ["Claude", "GPT", "Gemini", "Qwen", "DeepSeek", "Llama", "……"]


def st_opencode(ctx, x, y, lt, a, t):
    shell(ctx, x, y, CW, CH, a, ic_opencode, "OpenCode", "开源社区 · MIT 协议", ["开源免费", "75+ 模型服务商"], t, "#3A3A46")
    px, py, pw, ph = x - 130, y - 270, 680, 540
    _panel(ctx, px, py, pw, ph, a, dark=True)
    text(ctx, "$ opencode", px + 40, py + 60, 30, "#C9C4D6", a, "mono", "l")
    text(ctx, "切换模型：", px + 40, py + 120, 32, "#FFFFFF", a, "bold", "l")
    sel_f = clamp((lt - 1.2) / 0.62, 0, 99)
    sel = int(sel_f) % 5
    e = ease_io(clamp((sel_f - math.floor(sel_f)) * 3 - 2))
    pos = sel + e if sel < 4 else 4 - 4 * e
    hy = py + 180 + pos * 50
    rrect(ctx, px + 30, hy - 23, pw - 60, 46, 14)
    fill(ctx, "#7CFFB2", 0.18 * a)
    for j, m in enumerate(MODELS):
        yy = py + 180 + j * 50
        on = abs(yy - hy) < 25
        text(ctx, ("▶ " if on else "  ") + m, px + 50, yy, 30, "#7CFFB2" if on else "#BDB7CC", a, "mono", "l")
    if lt > 1.2:
        text(ctx, f"当前：{MODELS[sel]}", px + pw - 40, py + 60, 28, "#FFC65C", a, "bold", "r")


def st_openclaw(ctx, x, y, lt, a, t):
    shell(ctx, x, y, CW, CH, a, ic_openclaw, "OpenClaw", "开源 · 个人智能体", ["跑在你自己的电脑上", "聊天软件里下指令"], t, "#E5484D")
    px, py, pw, ph = x - 130, y - 270, 680, 540
    _panel(ctx, px, py, pw, ph, a)
    # 左：聊天软件
    ic_phone(ctx, px + 70, py + 72, 84, a, t, "#ECF7EF")
    text(ctx, "聊天软件", px + 112, py + 72, 28, "#5A4E63", a, "bold", "l")
    msgs = [(0.9, "把下载文件夹整理一下", True), (2.0, "好的，马上处理", False), (4.0, "已整理 128 个文件 ✓", False)]
    for j, (t0, s_, me) in enumerate(msgs):
        k = pop(lt, t0, 0.35)
        if k <= 0:
            continue
        bw = text_w(ctx, s_, 28, "bold") + 44
        by = py + 160 + j * 112
        bx = px + 30 if not me else px + 380 - bw
        with at(ctx, bx + bw / 2, by + 36, k):
            bubble(ctx, -bw / 2, -36, bw, 72, "#5BD27A" if me else "#FFFFFF", a,
                   tail="right" if me else "left", r=26, shadow=0.08)
            text(ctx, s_, 0, 0, 28, "#14361F" if me else "#2B2233", a, "bold")
    # 箭头 → 电脑
    ap = ease_out(prog(lt, 2.3, 2.9))
    if ap > 0:
        from ..core import arrow
        arrow(ctx, px + 400, py + 290, px + 470, py + 290, 7, "#E5484D", a, p=ap)
    lk = smooth(prog(lt, 2.6, 3.0))
    if lk > 0:
        ic_laptop(ctx, px + 575, py + 280, 190, a * lk, t, "#1E1B26")
        text(ctx, "你的电脑", px + 575, py + 400, 26, "#5A4E63", a * lk, "bold")
        for f in range(6):
            u = ease_io(prog(lt, 2.9 + f * 0.15, 3.6 + f * 0.15))
            sx0, sy0 = px + 520 + (f % 3) * 40, py + 240 + (f // 3) * 34
            tx, ty = px + 610, py + 272
            fx, fy = lerp(sx0, tx, u), lerp(sy0, ty, u) - math.sin(u * math.pi) * 24
            if u < 1:
                rrect(ctx, fx - 10, fy - 13, 20, 26, 4)
                fill(ctx, ["#FFB547", "#7CC6FF", "#FF9F68"][f % 3], a * lk)
        ic_folder(ctx, px + 610, py + 268, 48, a * lk, t)


def st_workbuddy(ctx, x, y, lt, a, t):
    shell(ctx, x, y, CW, CH, a, ic_workbuddy, "WorkBuddy", "腾讯 · 2026.3 上线", ["桌面办公智能体", "支持 MCP 连接器"], t, "#2F7BFF")
    px, py, pw, ph = x - 130, y - 270, 680, 540
    content = window(ctx, px, py, pw, ph, "WorkBuddy", a, r=28, shadow=0.0)
    bx, by, bw, bh = content
    task = "整理本周会议纪要，生成待办表格"
    n = int(len(task) * prog(lt, 0.8, 1.9))
    rrect(ctx, bx + 30, by + 26, bw - 60, 64, 20)
    fill(ctx, "#EEF4FF", a)
    text(ctx, task[:n], bx + 54, by + 58, 28, "#2B2233", a, "bold", "l")
    lines_block(ctx, bx + 36, by + 122, 230, 7, 34, "#D7DEEC", a, prog(lt, 2.0, 3.0), 13, seed=5)
    tk = ease_out(prog(lt, 2.8, 3.2))
    if tk > 0:
        cells = [["发布会", "小李", "周三"], ["预算表", "小王", "周四"], ["复盘", "小张", "周五"]]
        table(ctx, bx + 300, by + 116, 3, 3, 112, 62, a * tk, "#E6F0FF", "#C9D8F2",
              prog(lt, 3.0, 4.2), 27, ["事项", "负责人", "截止"], cells, "#2F7BFF")
    sk = pop(lt, 4.4, 0.4)
    if sk > 0:
        with at(ctx, bx + bw / 2, by + bh - 50, sk):
            pill(ctx, "✓ 已保存到腾讯文档", 0, 0, 28, "#FFFFFF", "#2F7BFF", a, 1.0)


def st_muse(ctx, x, y, lt, a, t):
    shell(ctx, x, y, CW, CH, a, ic_muse, "Muse", "Meta · 2026.9 发布", ["个人智能体", "几十种连接器"], t, "#7B5CFF")
    px, py, pw, ph = x - 130, y - 270, 680, 540
    _panel(ctx, px, py, pw, ph, a)
    cx, cy = px + pw / 2, py + ph / 2
    nodes = [(ic_gmail, "Gmail", -2.4), (ic_docs, "文档", -0.75), (ic_calendar, "日历", 0.75), (ic_instagram, "Instagram", 2.4)]
    for j, (ic, lab, ang) in enumerate(nodes):
        t0 = 0.9 + j * 0.55
        k = pop(lt, t0, 0.4)
        nx, ny = cx + math.cos(ang - math.pi / 2) * 210, cy + math.sin(ang - math.pi / 2) * 175 + 10
        lp = ease_out(prog(lt, t0 + 0.2, t0 + 0.6))
        if lp > 0:
            stroke_pts(ctx, [(cx, cy), (lerp(cx, nx, lp), lerp(cy, ny, lp))], 6, "#8B6CFF", 0.5 * a,
                       dash=(14, 10), offset=-t * 40)
        if k > 0:
            with at(ctx, nx, ny, k):
                ic(ctx, 0, 0, 96, a, t)
                text(ctx, lab, 0, 76, 26, "#5A4E63", a, "bold")
    ic_muse(ctx, cx, cy, 150, a, t)


# ---------------------------------------------------------------- 收束：连接 = 能力

PRODS = [ic_chatgpt, ic_codex, ic_claude_code, ic_opencode, ic_openclaw, ic_workbuddy, ic_muse]
TOOLS2 = [ic_gmail, ic_docs, ic_sheets, ic_calendar, ic_github, ic_slack, ic_notion, ic_browser, ic_terminal, ic_folder]
_LINKS = [(p, (p * 3 + k * 4) % len(TOOLS2)) for k in range(4) for p in range(len(PRODS))]


def draw_wrap(ctx, t):
    x0 = WRAP_X
    a = smooth(prog(t, 35.0, 35.8))
    if a <= 0:
        return
    py, ty = 300, 690
    pxs = [x0 - 690 + i * 230 for i in range(len(PRODS))]
    txs = [x0 - 765 + i * 170 for i in range(len(TOOLS2))]
    for n, (pi_, ti) in enumerate(_LINKS):
        t0 = 36.3 + n * 0.09
        lp = ease_out(prog(t, t0, t0 + 0.5))
        if lp <= 0:
            continue
        pts = bezier_pts((pxs[pi_], py + 70), (pxs[pi_], py + 230), (txs[ti], ty - 230), (txs[ti], ty - 60), 24)
        seg = polyline_partial(pts, lp)
        stroke_pts(ctx, seg, 4, "#FFC65C", 0.35 * a)
        if lp >= 1:
            u = ((t - t0) * 0.6 + n * 0.13) % 1
            from ..core import point_on
            (gx, gy), _ = point_on(pts, u)
            glow(ctx, gx, gy, 16, "#FFE3A3", 0.7 * a)
    nconn = sum(1 for n in range(len(_LINKS)) if t > 36.3 + n * 0.09 + 0.3)
    for i, ic in enumerate(PRODS):
        k = pop(t, 35.5 + i * 0.08, 0.45)
        deg = sum(1 for (p, _) in _LINKS[:nconn] if p == i)
        glow(ctx, pxs[i], py, 120, "#FFC65C", 0.1 * deg * a)
        ic(ctx, pxs[i], py, 128 * k, a, t)
    for i, ic in enumerate(TOOLS2):
        k = pop(t, 35.7 + i * 0.06, 0.45)
        ic(ctx, txs[i], ty, 100 * k, a, t)
    ck = pop(t, 37.6, 0.5)
    if ck > 0:
        with at(ctx, x0, (py + ty) / 2, ck):
            rrect(ctx, -270, -58, 540, 116, 58)
            fill(ctx, "#1A1426", 0.85 * a)
            text(ctx, "连接 = 能力", 0, 0, 64, "#FFC65C", a, "black")


def sfx():
    out = [(0.1, "pop", {"gain": 0.4, "pitch": 0.8}),
           (1.4, "bubble", {"gain": 0.4}), (3.0, "pop", {"gain": 0.35, "pitch": 1.2}),
           (2.1, "think", {"dur": 0.9, "gain": 0.2}), (3.2, "typing", {"dur": 1.6, "gain": 0.25})]
    for (a, b) in PANS:
        out.append((a, "whoosh", {"dur": b - a + 0.2, "gain": 0.45}))
        out.append((a + 0.05, "hop", {"gain": 0.3}))
        out.append((b - 0.05, "thud", {"gain": 0.25}))
    s1 = T_ARR[1] - 0.2
    for k, lt0 in enumerate((0.5, 0.9, 2.0, 2.7, 3.6, 1.1, 1.5, 2.5, 3.3, 3.8, 4.6)):
        out.append((s1 + lt0, "typing", {"dur": 0.45, "gain": 0.22, "seed": 500 + k}))
    out += [
            (s1 + 3.6, "check", {"gain": 0.35}), (s1 + 4.3, "success", {"gain": 0.4}),
            (10.6, "wink", {"gain": 0.4})]
    s2 = T_ARR[2] - 0.2
    for k in range(7):
        out.append((s2 + 1.2 + k * 0.62 + 0.4, "tick", {"gain": 0.32, "pitch": 1.0 + (k % 5) * 0.1}))
    s3 = T_ARR[3] - 0.2
    out += [(s3 + 0.9, "bubble", {"gain": 0.4}), (s3 + 2.0, "bubble", {"gain": 0.35}),
            (s3 + 2.9, "shuffle", {"dur": 1.2, "gain": 0.35}), (s3 + 4.0, "success", {"gain": 0.4})]
    s4 = T_ARR[4] - 0.2
    out += [(s4 + 0.8, "typing", {"dur": 1.1, "gain": 0.3}), (s4 + 3.0, "scan", {"dur": 1.2, "gain": 0.25}),
            (s4 + 4.4, "ding", {"gain": 0.45, "pitch": 1.1})]
    s5 = T_ARR[5] - 0.2
    for j in range(4):
        out.append((s5 + 0.9 + j * 0.55, "connect", {"gain": 0.4, "pitch": 1.0 + j * 0.1}))
    out.append((s5 + 2.6, "stream", {"dur": 2.6, "gain": 0.16}))
    out.append((35.5, "pop", {"gain": 0.35, "pitch": 0.9}))
    out.append((36.3, "sparkle", {"dur": 2.6, "gain": 0.35}))
    out.append((37.6, "impact_soft", {"gain": 0.45}))
    out.append((38.0, "powerup", {"gain": 0.35}))
    return out
