"""时间轴：把各场景拼成整片，并负责字幕、章节标题、地点年代字幕与 SRT 导出。

每个场景模块提供：
    DUR      场景时长（秒）
    CHAPTER  None 或 dict(num="第一章", title="火与石", era="约 330 万年前 — 5000 年前", key="观察", at=1.0)
    VO       [(本地开始秒, "字幕文案，{高亮}"), ...]   视频没有人声，文案只以字幕出现
    SUPERS   [(本地开始秒, 本地结束秒, "公元前 240 年", "亚历山大港"), ...]   画面左上角的年代 / 地点
    draw(ctx, t)      t 为场景内本地时间（转场时可能略小于 0 或略大于 DUR）
    sfx()    [(本地时间, 音效名, {参数}), ...]
"""
import math

from . import narration
from .core import (H, W, clamp, ease_io, ease_out, ease_out5, glow, lin, parse_marked, rad, rich_text,
                   rich_w, setc, smooth, text, text_w, wrap_marked)
from .scenes import ORDER, TRANSITIONS

STARTS = []
_acc = 0.0
for _m in ORDER:
    STARTS.append(_acc)
    _acc += _m.DUR
DURATION = _acc
NAMES = [m.__name__.split(".")[-1] for m in ORDER]

assert len(TRANSITIONS) == len(ORDER) - 1, "转场数量必须等于场景数 - 1"

LB = 96          # 遮幅黑边高度（设计坐标），画面有效区域 y ∈ [LB, H - LB]


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


# ---------------------------------------------------------------- 文案 → 字幕


def vo_lines():
    """全片文案：[{id, scene, idx, start, slot_end, text}]，slot_end 为这句最晚应结束的时间。"""
    out = []
    for i, m in enumerate(ORDER):
        lines = getattr(m, "VO", [])
        for k, item in enumerate(lines):
            t0, txt = item[0], item[1]
            opts = item[2] if len(item) > 2 else {}
            start = STARTS[i] + t0
            if k + 1 < len(lines):
                end = STARTS[i] + lines[k + 1][0] - 0.12
            else:
                end = STARTS[i] + m.DUR + opts.get("spill", 0.3)
            out.append(dict(id=f"{NAMES[i]}#{k}", scene=NAMES[i], idx=k, start=round(start, 3),
                            slot_end=round(end, 3), text=txt))
    return out


VO = vo_lines()


def _cues():
    cues = []
    for L in VO:
        # 没有配音：比朗读多留一些阅读时间，但不超过下一句开始
        d = min(narration.estimate(L["text"]) * 1.3 + 0.9, L["slot_end"] - L["start"])
        cues += narration.estimate_cues(L["text"], L["start"], d)
    cues.sort(key=lambda c: c[0])
    fixed = []
    for j, (a, b, s) in enumerate(cues):
        if j + 1 < len(cues) and 0 < cues[j + 1][0] - b < 0.4:
            b = cues[j + 1][0] - 0.02          # 小句之间的极短空隙直接连上，避免闪烁
        fixed.append((a, b, s))
    return fixed


SUBS = _cues()


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
            out.append((b - dur / 2 - 0.05, snd, {"dur": dur + 0.25, "gain": params.get("gain", 0.4)}))
    out.sort(key=lambda x: x[0])
    return out


def chapters():
    """[(全片开始秒, 结束秒, 章节信息 dict), ...]"""
    out = []
    for i, m in enumerate(ORDER):
        ch = getattr(m, "CHAPTER", None)
        if ch:
            out.append((STARTS[i], STARTS[i] + m.DUR, ch))
    return out


CHAPTERS = chapters()


def supers():
    out = []
    for i, m in enumerate(ORDER):
        for (a, b, l1, *rest) in getattr(m, "SUPERS", []):
            out.append((STARTS[i] + a, STARTS[i] + b, l1, rest[0] if rest else ""))
    return out


SUPERS = supers()

# ---------------------------------------------------------------- 字幕（放在下方黑边里）

SUB_SIZE = 46
SUB_MAX_W = 1700
SUB_Y = H - LB / 2 + 2
SUB_HI = "#F2C46B"


def draw_subtitle(ctx, T):
    for (a, b, s) in SUBS:
        if a - 0.01 <= T <= b + 0.01:
            al = min(smooth((T - a) / 0.16), smooth((b - T) / 0.16))
            if al <= 0.003:
                continue
            lines = wrap_marked(ctx, s, SUB_SIZE, "medium", SUB_MAX_W)
            lh = SUB_SIZE * 1.18
            y0 = SUB_Y - lh * (len(lines) - 1) / 2 - (lh * 0.5 if len(lines) > 1 else 0)
            for k, L in enumerate(lines):
                yy = y0 + lh * k
                segs = parse_marked(L)
                rich_text(ctx, segs, W / 2 + 2, yy + 2.5, SUB_SIZE, "#000000", "#000000", 0.6 * al, "medium")
                rich_text(ctx, segs, W / 2, yy, SUB_SIZE, "#F3EEE6", SUB_HI, al, "medium")


# ---------------------------------------------------------------- 章节标题（电影片头字卡式）


def _tracked(ctx, s, x, y, size, color, a, weight, track):
    """字距可变的居中文字（track 为字距占字号的比例）。"""
    from .core import font
    font(ctx, size, weight)
    adv = [ctx.text_extents(ch).x_advance for ch in s]
    tw = sum(adv) + track * size * (len(s) - 1)
    cx = x - tw / 2
    for ch, w in zip(s, adv):
        text(ctx, ch, cx, y, size, color, a, weight, "l")
        cx += w + track * size
    return tw


def draw_chapter(ctx, T):
    for (s0, s1, ch) in CHAPTERS:
        at_ = s0 + ch.get("at", 1.0)
        dur = ch.get("dur", 4.6)
        u = T - at_
        if u < 0 or u > dur:
            continue
        a = smooth(u / 0.9) * smooth((dur - u) / 0.8)
        if a <= 0.003:
            continue
        cy = ch.get("y", 500)
        cx = ch.get("x", W / 2)
        # 压暗背景，保证字清楚
        ctx.set_source(rad(cx, cy, 0, 760, [(0, "#000000", 0.55 * a), (0.6, "#000000", 0.25 * a),
                                               (1, "#000000", 0)]))
        ctx.paint()
        tr = 0.10 + 0.08 * ease_io(u / dur)                       # 字距缓慢拉开
        num_a = a * smooth((u - 0.1) / 0.8)
        _tracked(ctx, ch["num"], cx, cy - 112, 34, "#D9B26A", num_a, "serif_m", 0.6)
        # 主标题：先虚后实（几层错位叠加模拟失焦 → 合焦）
        foc = ease_out(clamp((u - 0.2) / 1.1))
        for k, (dx, al) in enumerate(((0, 1.0), (-6, 0.25), (6, 0.25))):
            off = dx * (1 - foc)
            if k > 0 and foc > 0.98:
                continue
            ctx.save()
            ctx.translate(off, 0)
            _tracked(ctx, ch["title"], cx, cy - 18, 118, "#F4ECDF",
                     a * al * (0.35 + 0.65 * foc) if k == 0 else a * al * (1 - foc), "serif_k", tr)
            ctx.restore()
        # 金色细线
        lw = 420 * ease_io(clamp((u - 0.6) / 1.0))
        ctx.rectangle(cx - lw / 2, cy + 62, lw, 2)
        setc(ctx, "#D9B26A", 0.85 * a)
        ctx.fill()
        ea = a * smooth((u - 1.0) / 0.8)
        _tracked(ctx, ch["era"], cx, cy + 108, 32, "#E8DCC8", ea, "serif_l", 0.12)
        if ch.get("key"):
            ka = a * smooth((u - 1.6) / 0.8)
            _tracked(ctx, "关键词 · " + ch["key"], cx, cy + 162, 28, "#D9B26A", ka, "serif_m", 0.3)


# ---------------------------------------------------------------- 年代 / 地点字幕（左上角，打字机效果）


def draw_supers(ctx, T):
    for (a, b, l1, l2) in SUPERS:
        if not (a <= T <= b):
            continue
        al = smooth((T - a) / 0.4) * smooth((b - T) / 0.5)
        x, y = 118, LB + 64
        n1 = len(l1)
        k1 = int(clamp((T - a) / 0.045 / max(n1, 1)) * n1 + 0.999) if T - a < 0.045 * n1 else n1
        ln = 64 * ease_out(clamp((T - a) / 0.5))
        ctx.rectangle(x, y - 24, 3, ln)
        setc(ctx, "#D9B26A", 0.9 * al)
        ctx.fill()
        text(ctx, l1[:k1], x + 22, y - 2, 34, "#000000", 0.5 * al, "serif_sb", "l")
        text(ctx, l1[:k1], x + 20, y - 4, 34, "#F2D79B", al, "serif_sb", "l")
        if l2:
            t2 = T - a - 0.045 * n1 - 0.1
            k2 = int(clamp(t2 / 0.05 / max(len(l2), 1)) * len(l2) + 0.999) if t2 > 0 else 0
            text(ctx, l2[:k2], x + 22, y + 38, 28, "#000000", 0.5 * al, "serif_r", "l")
            text(ctx, l2[:k2], x + 20, y + 36, 28, "#F1EADF", 0.92 * al, "serif_r", "l")


def draw_overlays(ctx, T, subs=True):
    draw_supers(ctx, T)
    draw_chapter(ctx, T)


def draw_bar_overlays(ctx, T, subs=True):
    """画在黑边之上的东西（字幕）。"""
    if subs:
        draw_subtitle(ctx, T)


# ---------------------------------------------------------------- SRT


def _ts(t):
    ms = int(round(max(0.0, t) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def srt_text():
    out = []
    for i, (a, b, s) in enumerate(SUBS, 1):
        out.append(f"{i}\n{_ts(a)} --> {_ts(b)}\n{narration.plain(s)}\n")
    return "\n".join(out)


def script_text():
    """完整文案稿。"""
    out, cur = [], None
    for L in VO:
        if L["scene"] != cur:
            cur = L["scene"]
            out.append(f"\n## {cur}")
        out.append(f"[{L['start']:7.2f}s] {narration.plain(L['text'])}")
    return "\n".join(out).strip() + "\n"
