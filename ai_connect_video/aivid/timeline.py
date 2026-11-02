"""时间轴：把各场景拼成整片，并负责字幕、章节标签、进度条与 SRT 导出。

每个场景模块提供：
    DUR      场景时长（秒）
    CHAPTER  None 或 ("01", "章节名")
    SUBS     [(本地开始, 本地结束, "字幕，{高亮}"), ...]
    draw(ctx, t)      t 为场景内本地时间（转场时可能略小于 0 或略大于 DUR）
    sfx()    [(本地时间, 音效名, {参数}), ...]
"""
import math

from .core import (H, W, clamp, ease_out, ease_out5, font, lerp, parse_marked, rich_text,
                   rich_w, rrect, setc, smooth, text, text_w, wrap_marked)
from .scenes import ORDER, TRANSITIONS

STARTS = []
_acc = 0.0
for _m in ORDER:
    STARTS.append(_acc)
    _acc += _m.DUR
DURATION = _acc

assert len(TRANSITIONS) == len(ORDER) - 1, "转场数量必须等于场景数 - 1"


def scene_index(T):
    for i in range(len(ORDER) - 1, -1, -1):
        if T >= STARTS[i]:
            return i
    return 0


def transition_at(T):
    """若 T 处于某个转场窗口内，返回 (前场景序号, 后场景序号, 种类, 进度, 参数)。"""
    for i, tr in enumerate(TRANSITIONS):
        kind, dur = tr[0], tr[1]
        params = tr[2] if len(tr) > 2 else {}
        b = STARTS[i + 1]
        if b - dur / 2 <= T < b + dur / 2:
            return i, i + 1, kind, (T - (b - dur / 2)) / dur, params
    return None


def all_subs():
    out = []
    for i, m in enumerate(ORDER):
        for (a, b, s) in m.SUBS:
            out.append((STARTS[i] + a, STARTS[i] + b, s))
    out.sort(key=lambda x: x[0])
    return out


def all_sfx():
    out = []
    for i, m in enumerate(ORDER):
        for cue in m.sfx():
            t, name = cue[0], cue[1]
            kw = cue[2] if len(cue) > 2 else {}
            out.append((STARTS[i] + t, name, kw))
    for i, tr in enumerate(TRANSITIONS):
        b = STARTS[i + 1]
        kind, dur = tr[0], tr[1]
        params = tr[2] if len(tr) > 2 else {}
        snd = params.get("sound", "whoosh")
        if snd:
            out.append((b - dur / 2 - 0.05, snd, {"dur": dur + 0.25, "gain": params.get("gain", 0.5)}))
    out.sort(key=lambda x: x[0])
    return out


def chapters():
    """[(开始, 结束, 编号, 标题), ...]，相邻同章节场景合并。"""
    out = []
    for i, m in enumerate(ORDER):
        ch = getattr(m, "CHAPTER", None)
        end = STARTS[i] + m.DUR
        if ch is None:
            continue
        if out and out[-1][2] == ch[0] and abs(out[-1][1] - STARTS[i]) < 1e-6:
            out[-1] = (out[-1][0], end, ch[0], ch[1])
        else:
            out.append((STARTS[i], end, ch[0], ch[1]))
    return out


SUBS = all_subs()
CHAPTERS = chapters()

# ---------------------------------------------------------------- 字幕

SUB_SIZE = 44
SUB_MAX_W = 1560
SUB_BOTTOM = 1046
SUB_HI = "#FFC65C"


def draw_subtitle(ctx, T):
    for (a, b, s) in SUBS:
        if a - 0.01 <= T <= b + 0.01:
            fin = smooth((T - a) / 0.2)
            fout = smooth((b - T) / 0.18)
            al = min(fin, fout)
            if al <= 0.003:
                continue
            rise = (1 - ease_out(clamp((T - a) / 0.3))) * 10
            lines = wrap_marked(ctx, s, SUB_SIZE, "bold", SUB_MAX_W)
            lh = SUB_SIZE * 1.42
            ws = [rich_w(ctx, parse_marked(L), SUB_SIZE, "bold") for L in lines]
            bw = max(ws) + SUB_SIZE * 1.3
            bh = lh * len(lines) + SUB_SIZE * 0.5
            x0, y0 = W / 2 - bw / 2, SUB_BOTTOM - bh + rise
            rrect(ctx, x0, y0, bw, bh, min(26, bh / 2))
            setc(ctx, "#120E18", 0.62 * al)
            ctx.fill()
            for k, L in enumerate(lines):
                yy = y0 + SUB_SIZE * 0.25 + lh * (k + 0.5)
                # 细描边阴影，提升可读性
                rich_text(ctx, parse_marked(L), W / 2 + 1.5, yy + 2, SUB_SIZE, "#000000", "#000000",
                          0.35 * al, "bold")
                rich_text(ctx, parse_marked(L), W / 2, yy, SUB_SIZE, "#FFFFFF", SUB_HI, al, "bold")


# ---------------------------------------------------------------- 章节标签 / 进度条


def draw_chapter(ctx, T):
    for (a, b, num, title) in CHAPTERS:
        if not (a - 0.1 <= T <= b + 0.1):
            continue
        u = T - a
        # 大标签：0.35s 进入，停留到 3.1s，然后收缩成角标
        big_in = ease_out5(clamp((u - 0.35) / 0.55))
        big_out = smooth(clamp((u - 3.0) / 0.5))
        fade_end = smooth(clamp((b - T) / 0.4))
        if big_in > 0 and big_out < 1:
            k = big_in * (1 - big_out)
            x0, y0 = 70, 64
            # 深色底板（保证在浅色背景上也清晰）
            nw0 = text_w(ctx, num, 104, "black")
            tw0 = text_w(ctx, title, 50, "black")
            pw_ = (nw0 + 46 + max(tw0, 160) + 70) * ease_out5(clamp((u - 0.3) / 0.6))
            rrect(ctx, x0 - 34 - 30 * big_out, y0 - 14, pw_, 136, 30)
            setc(ctx, "#1A1426", 0.72 * k)
            ctx.fill()
            # 编号
            ctx.save()
            ctx.rectangle(0, 0, W, H)
            ctx.clip()
            nx = x0 - 60 * (1 - big_in) - 30 * big_out
            text(ctx, num, nx, y0 + 52, 104, "#FF9F68", k, "black", "l",
                 shadow=(3, 4, "#000000", 0.25))
            nw = text_w(ctx, num, 104, "black")
            bar_h = 92 * big_in
            ctx.rectangle(nx + nw + 20, y0 + 52 - bar_h / 2, 6, bar_h)
            setc(ctx, "#FFFFFF", 0.85 * k)
            ctx.fill()
            tx = nx + nw + 46
            reveal = clamp((u - 0.55) / 0.6)
            tw = text_w(ctx, title, 50, "black")
            ctx.rectangle(tx - 6, y0, (tw + 30) * ease_out(reveal), 120)
            ctx.clip()
            text(ctx, title, tx + 2, y0 + 30 + 3, 50, "#000000", 0.25 * k, "black", "l")
            text(ctx, title, tx, y0 + 30, 50, "#FFFFFF", k, "black", "l")
            sub = ("CHAPTER " + num) if num.isdigit() else "EPILOGUE"
            text(ctx, sub, tx, y0 + 82, 22, "#FFD9B8", 0.9 * k, "bold", "l", spacing=0.3)
            ctx.restore()
        # 角标
        small = smooth(clamp((u - 3.1) / 0.45)) * fade_end
        if small > 0.003:
            s = f"{num} · {title}"
            sz = 24
            w = text_w(ctx, s, sz, "bold") + 40
            x, y = 40 - 20 * (1 - small), 34
            rrect(ctx, x, y, w, 42, 21)
            setc(ctx, "#120E18", 0.45 * small)
            ctx.fill()
            ctx.arc(x + 20, y + 21, 5, 0, math.tau)
            setc(ctx, "#FF9F68", small)
            ctx.fill()
            text(ctx, s, x + 32, y + 21, sz, "#FFFFFF", 0.92 * small, "bold", "l")


def draw_progress(ctx, T):
    y, h = H - 7, 7
    a = 0.55
    for (s0, s1, num, title) in CHAPTERS:
        x0 = s0 / DURATION * W + 2
        x1 = s1 / DURATION * W - 2
        ctx.rectangle(x0, y, x1 - x0, h)
        setc(ctx, "#FFFFFF", 0.16 * a)
        ctx.fill()
        if T > s0:
            xf = min(x1, T / DURATION * W)
            ctx.rectangle(x0, y, xf - x0, h)
            setc(ctx, "#FF9F68", 0.9 * a)
            ctx.fill()


def draw_overlays(ctx, T):
    draw_chapter(ctx, T)
    draw_subtitle(ctx, T)
    draw_progress(ctx, T)


# ---------------------------------------------------------------- SRT


def _ts(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def srt_text():
    out = []
    for i, (a, b, s) in enumerate(SUBS, 1):
        plain = s.replace("{", "").replace("}", "")
        out.append(f"{i}\n{_ts(a)} --> {_ts(b)}\n{plain}\n")
    return "\n".join(out)
