"""代码与终端：编程题材里的"主视觉 / 实物"。配色沿用星火的暖白 + 金，冷色只给函数名，保持同一种审美。

    code_panel(ctx, t, T0, CODE, x=140, y=200, w=980, title="search.py", cps=45,
               highlight=[(4, T0 + 3.0, T0 + 5.0)], focus=None)
    terminal(ctx, t, T0, [("cmd", "python search.py"), ("out", "找到 42，比较了 6 次"), ("ok", "✓ 通过 12 个测试")],
             x=1180, y=560, w=640)

逐字打出（cps 字 / 秒）、行高亮（金色底条 + 左侧标记）、聚焦（其余行变暗）、闪烁光标。
"""
import math
import re

from .core import clamp, prog, rrect, setc, smooth, text, text_w

PAL = dict(bg="#0B0A0E", edge="#D9B26A", tab="#CFC4B0", base="#E8E2D6", kw="#E0B26A", str="#A9C99A",
           num="#F0A87A", fn="#BFE0FF", com="#7E766A", punc="#A89E90", lineno="#5E564C", cursor="#FFD27A")

_KW = {
    "python": r"\b(def|return|if|elif|else|for|while|in|not|and|or|import|from|as|class|with|try|except|finally|raise|"
              r"lambda|yield|None|True|False|pass|break|continue|global|async|await|is)\b",
    "js": r"\b(function|return|if|else|for|while|const|let|var|new|class|import|from|export|default|try|catch|throw|"
          r"async|await|null|undefined|true|false|this|of|in)\b",
}
_COMMENT = {"python": r"#.*$", "js": r"//.*$", "sh": r"#.*$"}


def tokenize(line, lang="python"):
    """把一行代码切成 (文字, 颜色) 片段。"""
    pats = [("com", _COMMENT.get(lang, r"#.*$")), ("str", r"\"[^\"]*\"|'[^']*'|`[^`]*`"),
            ("num", r"\b\d+(?:\.\d+)?\b"), ("kw", _KW.get(lang, _KW["python"])), ("fn", r"\b[A-Za-z_]\w*(?=\()"),
            ("punc", r"[()\[\]{}:,.=+\-*/<>%!]")]
    out, i = [], 0
    rx = re.compile("|".join(f"(?P<{n}>{p})" for n, p in pats), re.M)
    for m in rx.finditer(line):
        if m.start() > i:
            out.append((line[i:m.start()], PAL["base"]))
        out.append((m.group(0), PAL[m.lastgroup]))
        i = m.end()
    if i < len(line):
        out.append((line[i:], PAL["base"]))
    return out


def _frame(ctx, x, y, w, h, title, a):
    rrect(ctx, x, y, w, h, 14)
    setc(ctx, PAL["bg"], 0.92 * a)
    ctx.fill()
    rrect(ctx, x, y, w, h, 14)
    ctx.set_line_width(1.5)
    setc(ctx, PAL["edge"], 0.32 * a)
    ctx.stroke()
    if title:
        text(ctx, title, x + 28, y + 30, 20, PAL["tab"], 0.9 * a, "mono", "l")
        tw = text_w(ctx, title, 20, "mono")
        ctx.rectangle(x + 28, y + 46, tw, 2)
        setc(ctx, PAL["edge"], 0.7 * a)
        ctx.fill()
        ctx.rectangle(x, y + 58, w, 1)
        setc(ctx, PAL["edge"], 0.15 * a)
        ctx.fill()


def code_panel(ctx, t, t0, code, x=140, y=200, w=980, h=None, title="main.py", lang="python", cps=45, size=26,
               highlight=(), focus=None, a=1.0, line_nos=True, typed=True):
    """代码面板。highlight=[(行号, 开始秒, 结束秒), …]（行号从 1 开始）；focus=(行a, 行b) 时其余行变暗。"""
    k = smooth(prog(t, t0 - 0.4, t0)) * a
    if k <= 0.003:
        return
    lines = code.strip("\n").split("\n")
    lh = size * 1.55
    top = 58 if title else 18
    h = h or top + 26 + lh * len(lines) + 18
    _frame(ctx, x, y, w, h, title, k)
    n_vis = (t - t0) * cps if typed else 1e9
    gx = x + (78 if line_nos else 30)
    cur = None
    used = 0
    for i, line in enumerate(lines):
        ly = y + top + 26 + lh * i + lh / 2
        hk = 0.0
        for (ln, h0, h1) in highlight:
            if ln == i + 1:
                hk = max(hk, smooth(prog(t, h0, h0 + 0.3)) * (1 - smooth(prog(t, h1, h1 + 0.4))))
        if hk > 0:
            rrect(ctx, x + 8, ly - lh / 2 + 2, w - 16, lh - 4, 6)
            setc(ctx, PAL["edge"], 0.13 * hk * k)
            ctx.fill()
            ctx.rectangle(x + 8, ly - lh / 2 + 4, 4, lh - 8)
            setc(ctx, PAL["cursor"], hk * k)
            ctx.fill()
        dim = 1.0
        if focus and not (focus[0] <= i + 1 <= focus[1]):
            dim = 0.35
        if line_nos:
            text(ctx, str(i + 1), x + 52, ly, size * 0.8, PAL["lineno"], k * dim, "mono", "r")
        if used >= n_vis:
            continue
        cx = gx
        for seg, col in tokenize(line, lang):
            take = seg[:max(0, int(n_vis - used))]
            used += len(seg)
            if take:
                cx += text(ctx, take, cx, ly, size, col, k * dim, "mono", "l")
            if len(take) < len(seg):
                break
        used += 1                                         # 换行也算一个字
        if used <= n_vis + 1:
            cur = (cx, ly)
    if cur and typed and (t - t0) * cps < sum(len(L) + 1 for L in lines) + 20:
        if int((t - t0) * 2.4) % 2 == 0:
            ctx.rectangle(cur[0] + 2, cur[1] - size * 0.55, size * 0.5, size * 1.1)
            setc(ctx, PAL["cursor"], 0.85 * k)
            ctx.fill()


def terminal(ctx, t, t0, lines, x=1180, y=560, w=640, h=None, title="terminal", cps=28, size=24, a=1.0):
    """终端：("cmd", 命令) 逐字打出；("out", 文字) / ("ok", 文字) / ("err", 文字) 在命令打完后逐行出现。"""
    k = smooth(prog(t, t0 - 0.4, t0)) * a
    if k <= 0.003:
        return
    lh = size * 1.6
    top = 58 if title else 18
    h = h or top + 22 + lh * len(lines) + 16
    _frame(ctx, x, y, w, h, title, k)
    col = {"out": "#BFAE8E", "ok": "#A9C99A", "err": "#FF8A6A"}
    tt = t0 + 0.2
    for i, (kind, s) in enumerate(lines):
        ly = y + top + 22 + lh * i + lh / 2
        if kind == "cmd":
            n = int(clamp((t - tt) * cps, 0, len(s)))
            if t >= tt:
                text(ctx, "$", x + 28, ly, size, PAL["cursor"], k, "mono", "l")
                text(ctx, s[:n], x + 28 + size * 1.1, ly, size, PAL["base"], k, "mono", "l")
                if n < len(s) and int((t - t0) * 2.4) % 2 == 0:
                    cx = x + 28 + size * 1.1 + text_w(ctx, s[:n], size, "mono")
                    ctx.rectangle(cx + 2, ly - size * 0.55, size * 0.5, size * 1.1)
                    setc(ctx, PAL["cursor"], 0.85 * k)
                    ctx.fill()
            tt += len(s) / cps + 0.45
        else:
            if t >= tt:
                text(ctx, s, x + 28, ly, size, col.get(kind, "#BFAE8E"), k * smooth(prog(t, tt, tt + 0.15)), "mono", "l")
            tt += 0.18
