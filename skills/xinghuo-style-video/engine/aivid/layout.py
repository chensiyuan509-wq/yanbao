"""版面与信息层级：把《星火》的排版规律固化成组件，换任何题材（历史、宇宙、编程……）都保持同一套层级。

数值来自对《星火》全部场景代码与成片的统计（见 references/design-system.md）：
  · 信息面板几乎都在右栏 x≈1150–1840、顶 y≈170–220，宽 540–640
  · 字号：镜头标题 34–44（宋体 Black）> 面板标题 30（金）> 正文 26–30（暖白）> 次要 22–26 > 出处 20–22
  · 节奏：面板在镜头开始后 0.4–0.8 秒出现，条目间隔 0.3–0.5 秒逐条浮现，结论最后出现（金 / 橘红）

用法：
    from ..layout import GRID, TYPE, C, reveal, headline, info_panel, stat, tag, pointer, source_note
    info_panel(ctx, t, T0 + 0.6, title="水星近日点进动", rows=[("观测", "574″"), ("牛顿理论", "531″"), ("差", "43″")],
               conclusion="广义相对论算出 43″", theme="blueprint")
"""
import math

from .core import H, W, clamp, ease_out, glow, prog, rrect, setc, smooth, text, text_w

# ---------------------------------------------------------------- 网格（设计坐标 1920×1080）

GRID = dict(
    lb=96,                    # 遮幅黑边；有效画面 y ∈ [96, 984]
    margin=118,               # 左右安全边距（出处字幕、年代字幕的 x）
    info_x=1180, info_w=640,  # 右栏信息面板
    info_y=180,
    hero=(118, 120, 1060, 840),   # 左侧 / 中部主视觉区（x, y, w, h）
    caption_y=900,            # 左下出处字幕
    super_y=160,              # 左上年代 / 地点字幕
    ground_y=905,             # Claude 的脚底线
    title_y=170,              # 镜头标题（居中或在主视觉上方）
)

# ---------------------------------------------------------------- 颜色

C = dict(
    ink="#F6EEDF", ink2="#F2E6CE",          # 暖白正文
    gold="#D9B26A", gold_hi="#FFD27A",       # 面板标题 / 年份；关键数字
    sub="#CFC4B0", source="#9A8C78",         # 次要文字；出处小字
    warn="#FF8A6A",                          # 反例 / 警示
    blue_ink="#E8F2FF", blue_sub="#BFE0FF", blue_line="#7FD8FF", blue_accent="#7FC8FF",   # 蓝图
    panel="#0E0C10",
)

# ---------------------------------------------------------------- 字号层级

TYPE = dict(
    display=(118, "serif_k"),   # 章节 / 片名
    h1=(40, "serif_k"),         # 镜头标题（"1905 · 奇迹年"）
    h2=(30, "serif_sb"),        # 面板标题（金色）
    body=(28, "serif_sb"),      # 面板正文
    value=(34, "serif_k"),      # 正文里的数值
    sub=(24, "serif_r"),        # 次要说明
    source=(20, "serif_r"),     # 出处 / 注释（最小，480p 下约 9 像素）
    label=(28, "serif_sb"),     # 画面上的标注（带投影）
    mono=(26, "mono"),          # 代码 / 终端
)

THEMES = {
    "dark": dict(panel=C["panel"], panel_a=0.78, edge=C["gold"], title=C["gold"], ink=C["ink"], sub=C["sub"],
                 value=C["gold_hi"]),
    "blueprint": dict(panel="#08162A", panel_a=0.80, edge=C["blue_accent"], title=C["blue_ink"], ink=C["blue_ink"],
                      sub=C["blue_sub"], value=C["gold_hi"]),
    "paper": dict(panel="#FBF4E4", panel_a=0.94, edge="#1C1A18", title="#7A2E16", ink="#1C1A18", sub="#5A4A3A",
                  value="#C8372D"),
}


def reveal(t, t0, i=0, step=0.4, dur=0.5):
    """第 i 个元素的入场进度（0..1）：从 t0 起，每个间隔 step 秒，淡入时长 dur。"""
    return smooth(prog(t, t0 + i * step, t0 + i * step + dur))


def _font_for(s, base):
    """含数学符号（″ ≈ − × ÷ ² ₀ ∇）的短数值用 eq 字体，避免宋体缺字。"""
    return "eq" if any(ch in s for ch in "″′≈−×÷²³₀₁₂∇∂√∞±") and not any("一" <= ch <= "鿿" for ch in s) else base


def headline(ctx, s, x, y, a=1.0, level="h1", color=None, align="c"):
    size, font = TYPE[level]
    return text(ctx, s, x, y, size, color or C["ink"], a, font, align)


def info_panel(ctx, t, t0, title=None, rows=(), conclusion=None, x=None, y=None, w=None, theme="dark",
               step=0.4, a=1.0, row_h=None):
    """右栏信息面板：标题（金）→ 条目逐条浮现 → 结论（最后、高亮）。

    rows 的每一项可以是：
      "一行文字"                    正文
      ("左边说明", "右边数值")       说明左对齐、数值右对齐高亮（数值含 ″ ≈ − 等自动用 eq 字体）
      ("说明", "数值", "#色")        指定数值颜色
    返回面板矩形 (x, y, w, h)。
    """
    th = THEMES[theme]
    x = GRID["info_x"] if x is None else x
    y = GRID["info_y"] if y is None else y
    w = GRID["info_w"] if w is None else w
    pad = 40
    rh = row_h or (64 if any(isinstance(r, tuple) for r in rows) else 56)
    h = pad + (56 if title else 0) + rh * len(rows) + (64 if conclusion else 0) + pad - 14
    k = reveal(t, t0, 0, step, 0.5) * a
    if k <= 0.003:
        return (x, y, w, h)
    rrect(ctx, x, y + (1 - ease_out(k)) * 16, w, h, 16)
    setc(ctx, th["panel"], th["panel_a"] * k)
    ctx.fill()
    rrect(ctx, x, y + (1 - ease_out(k)) * 16, w, h, 16)
    ctx.set_line_width(2)
    setc(ctx, th["edge"], 0.45 * k)
    ctx.stroke()
    cy = y + pad
    if title:
        size, font = TYPE["h2"]
        text(ctx, title, x + w / 2, cy + 6, size, th["title"], k, font)
        cy += 56
    for i, r in enumerate(rows):
        kk = reveal(t, t0 + 0.3, i, step) * a
        yy = cy + rh * i + rh / 2 - 8
        if isinstance(r, tuple):
            lab, val = r[0], r[1]
            col = r[2] if len(r) > 2 else th["value"]
            text(ctx, lab, x + 36, yy, TYPE["body"][0], th["ink"], kk, TYPE["body"][1], "l")
            vs, vf = TYPE["value"]
            text(ctx, val, x + w - 36, yy, vs, col, kk, _font_for(val, vf), "r")
        else:
            text(ctx, r, x + 36, yy, TYPE["body"][0], th["ink"], kk, TYPE["body"][1], "l")
    if conclusion:
        kk = reveal(t, t0 + 0.3, len(rows) + 0.6, step) * a
        yy = cy + rh * len(rows) + 30
        ctx.rectangle(x + 36, yy - 32, w - 72, 1.5)
        setc(ctx, th["edge"], 0.35 * kk)
        ctx.fill()
        text(ctx, conclusion, x + w / 2, yy + 4, TYPE["body"][0], th["value"], kk, "serif_sb")
    return (x, y, w, h)


def stat(ctx, t, t0, x, y, value, label, sub=None, color=None, a=1.0, size=84, count_from=None, fmt="{:,.0f}"):
    """大数字：数值（宋体 Black，可从 count_from 数到目标）+ 下方说明。"""
    k = reveal(t, t0, 0, 0.4, 0.6) * a
    if k <= 0.003:
        return
    s = value
    if count_from is not None:
        try:
            target = float(str(value).replace(",", ""))
            v = count_from + (target - count_from) * ease_out(prog(t, t0, t0 + 1.4))
            s = fmt.format(v)
        except ValueError:
            pass
    glow(ctx, x, y, size * 2.2, color or C["gold_hi"], 0.12 * k)
    text(ctx, s, x, y, size, color or C["gold_hi"], k, _font_for(str(s), "serif_k"))
    text(ctx, label, x, y + size * 0.85, 28, C["ink"], k, "serif_sb")
    if sub:
        text(ctx, sub, x, y + size * 0.85 + 40, 22, C["sub"], reveal(t, t0 + 0.4, 0) * a, "serif_r")


def tag(ctx, s, x, y, a=1.0, color=None, align="l", size=24, theme="dark"):
    """小标签（年份、型号、类别）：细边框的胶囊。theme 跟随所在画面：dark / blueprint / paper。"""
    if a <= 0.003:
        return 0
    th = THEMES[theme]
    color = color or (th["value"] if theme == "paper" else C["gold"])
    tw = text_w(ctx, s, size, "serif_sb")
    x0 = x if align == "l" else (x - tw / 2 - 18 if align == "c" else x - tw - 36)
    rrect(ctx, x0, y - size * 0.8, tw + 36, size * 1.6, size * 0.8)
    setc(ctx, th["panel"], (0.9 if theme == "paper" else 0.6) * a)
    ctx.fill()
    rrect(ctx, x0, y - size * 0.8, tw + 36, size * 1.6, size * 0.8)
    ctx.set_line_width(1.5)
    setc(ctx, color, 0.8 * a)
    ctx.stroke()
    text(ctx, s, x0 + 18, y, size, color, a, "serif_sb", "l")
    return tw + 36


def pointer(ctx, t, t0, target, anchor, s, sub=None, a=1.0, color=None):
    """指向画面细节的标注：目标点上的小圆 → 细引线 → 文字（适合"右下角拿圆规的人"、星系里的某个点、代码里的某一行）。"""
    k = smooth(prog(t, t0, t0 + 0.6)) * a
    if k <= 0.003:
        return
    col = color or C["gold_hi"]
    (tx, ty), (ax, ay) = target, anchor
    ph = (t - t0) * 2.2
    ctx.set_line_width(2.5)
    setc(ctx, col, 0.9 * k)
    ctx.arc(tx, ty, 14 + 3 * math.sin(ph), 0, math.tau)
    ctx.stroke()
    p = ease_out(prog(t, t0 + 0.1, t0 + 0.6))
    ctx.move_to(tx + (ax - tx) * 0.08, ty + (ay - ty) * 0.08)
    ctx.line_to(tx + (ax - tx) * p, ty + (ay - ty) * p)
    setc(ctx, col, 0.7 * k)
    ctx.set_line_width(2)
    ctx.stroke()
    align = "l" if ax >= tx else "r"
    dx = 12 if align == "l" else -12
    kk = smooth(prog(t, t0 + 0.4, t0 + 0.9)) * a
    text(ctx, s, ax + dx + 2, ay + 2.5, TYPE["label"][0], "#000000", 0.55 * kk, TYPE["label"][1], align)
    text(ctx, s, ax + dx, ay, TYPE["label"][0], C["ink"], kk, TYPE["label"][1], align)
    if sub:
        text(ctx, sub, ax + dx, ay + 38, 22, C["sub"], kk, "serif_r", align)


def source_note(ctx, s, x=None, y=None, a=1.0, align="l"):
    """不占出处字幕位置的小注（"示意图，角度已夸大"之类）。"""
    text(ctx, s, GRID["margin"] if x is None else x, 950 if y is None else y, TYPE["source"][0], C["source"], a,
         TYPE["source"][1], align)
