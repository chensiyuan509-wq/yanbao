"""历史图像（档案）层：加载 assets/archive 里的公有领域图片，做推拉摇移、调色、蓝图化、画框与出处字幕。

    from .archive import kb, show, caption
    kb(ctx, "athens", t, 0, 8, (0.5, 0.5, 1.0), (0.72, 0.78, 2.2))     # 8 秒内从全景推到右下角的欧几里得
    caption(ctx, "拉斐尔《雅典学院》", "1509—1511 · 梵蒂冈 · 公有领域", a)

裁切坐标 (cx, cy, zoom)：cx, cy 是要放在画面中心的图像归一化坐标，zoom=1 表示刚好铺满目标区域。
"""
import json
import math
import os

import cairo

from .core import H, W, clamp, ease_io, glow, hexc, lin, rad, rrect, setc, smooth, text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, "assets", "archive")
_CACHE = {}
_META = None


def meta(key):
    global _META
    if _META is None:
        p = os.path.join(DIR, "credits.json")
        _META = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    return _META.get(key, {})


def _load(key, level=0):
    ck = (key, level)
    if ck in _CACHE:
        return _CACHE[ck]
    from PIL import Image
    im = Image.open(os.path.join(DIR, key + ".jpg")).convert("RGB")
    if level:
        im = im.resize((max(1, im.width >> level), max(1, im.height >> level)), Image.LANCZOS)
    im = im.convert("RGBA")
    r, g, b, a = im.split()
    data = bytearray(Image.merge("RGBA", (b, g, r, a)).tobytes())
    s = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, im.width, im.height, im.width * 4)
    _CACHE[ck] = (s, data)
    return _CACHE[ck]


def size(key):
    s, _ = _load(key)
    return s.get_width(), s.get_height()


def _surface_for(ctx, key, scale):
    """按实际缩放挑一张合适分辨率的图（避免大幅缩小时的锯齿和开销）。"""
    m = ctx.get_matrix()
    dev = scale * math.hypot(m.xx, m.yx)
    level = 0
    while dev < 0.45 and level < 3:
        dev *= 2
        level += 1
    s, _ = _load(key, level)
    return s, 2 ** level


def show(ctx, key, crop=(0.5, 0.5, 1.0), rect=(0, 0, W, H), a=1.0, grade=None, fit="cover", rot=0.0):
    """把图像的某个区域铺进 rect。fit='cover' 铺满（可能裁切），'contain' 完整显示。"""
    if a <= 0.003:
        return None
    iw, ih = size(key)
    x, y, rw, rh = rect
    cx, cy, z = crop
    base = max(rw / iw, rh / ih) if fit == "cover" else min(rw / iw, rh / ih)
    sc = base * z
    if fit == "cover":           # 不露出边缘
        hx, hy = rw / (2 * iw * sc), rh / (2 * ih * sc)
        cx = clamp(cx, hx, 1 - hx) if hx < 0.5 else 0.5
        cy = clamp(cy, hy, 1 - hy) if hy < 0.5 else 0.5
    surf, k = _surface_for(ctx, key, sc)
    ctx.save()
    ctx.rectangle(x, y, rw, rh)
    ctx.clip()
    ctx.translate(x + rw / 2, y + rh / 2)
    if rot:
        ctx.rotate(rot)
    ctx.scale(sc * k, sc * k)
    ctx.translate(-cx * iw / k, -cy * ih / k)
    ctx.set_source_surface(surf, 0, 0)
    ctx.get_source().set_filter(cairo.FILTER_GOOD)
    if grade == "blueprint":
        _blueprint_paint(ctx, a)
    else:
        ctx.paint_with_alpha(clamp(a))
    ctx.restore()
    if grade and grade != "blueprint":
        _grade(ctx, grade, rect, a)
    # 返回图像坐标 → 画面坐标的映射，方便在图上做标注
    def to_screen(u, v):
        return (x + rw / 2 + (u - cx) * iw * sc, y + rh / 2 + (v - cy) * ih * sc)
    return to_screen


def _blueprint_paint(ctx, a):
    """专利图 / 线描 → 蓝图：反相后染成青色，用"滤色"叠在深蓝底上。"""
    src = ctx.get_source()
    ctx.push_group()
    ctx.set_source(src)
    ctx.paint()
    ctx.set_operator(cairo.OPERATOR_DIFFERENCE)
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    ctx.set_operator(cairo.OPERATOR_MULTIPLY)
    ctx.set_source_rgb(0.55, 0.88, 1.0)
    ctx.paint()
    ctx.pop_group_to_source()
    ctx.set_operator(cairo.OPERATOR_SCREEN)
    ctx.paint_with_alpha(clamp(a))
    ctx.set_operator(cairo.OPERATOR_OVER)


def _grade(ctx, grade, rect, a):
    x, y, rw, rh = rect
    ctx.save()
    ctx.rectangle(x, y, rw, rh)
    ctx.clip()
    if grade in ("mono", "sepia", "cool_mono"):
        ctx.set_operator(cairo.OPERATOR_HSL_SATURATION)
        ctx.set_source_rgba(0.5, 0.5, 0.5, a)
        ctx.paint()
        ctx.set_operator(cairo.OPERATOR_OVER)
    if grade in ("sepia", "warm"):
        ctx.set_operator(cairo.OPERATOR_SOFT_LIGHT)
        ctx.set_source_rgba(*hexc("#C88A4A"), 0.55 * a if grade == "sepia" else 0.35 * a)
        ctx.paint()
    elif grade in ("cool", "cool_mono"):
        ctx.set_operator(cairo.OPERATOR_SOFT_LIGHT)
        ctx.set_source_rgba(*hexc("#4A78C8"), 0.4 * a)
        ctx.paint()
    elif grade == "fire":
        ctx.set_operator(cairo.OPERATOR_SOFT_LIGHT)
        ctx.set_source_rgba(*hexc("#FF7A2A"), 0.55 * a)
        ctx.paint()
    elif grade == "dim":
        ctx.set_source_rgba(0, 0, 0, 0.35 * a)
        ctx.paint()
    ctx.restore()


def kb(ctx, key, t, t0, t1, c0, c1, rect=(0, 0, W, H), a=1.0, grade=None, ease=ease_io, fit="cover"):
    """Ken Burns：在 [t0, t1] 里从裁切 c0 缓缓推 / 摇到 c1。"""
    u = ease(clamp((t - t0) / max(t1 - t0, 1e-3)))
    c = tuple(c0[i] + (c1[i] - c0[i]) * u for i in range(3))
    return show(ctx, key, c, rect, a, grade, fit)


def framed(ctx, key, x, y, h, a=1.0, mat="#EFE6D2", frame="#5A3A1E", shadow=0.5, crop=None, w=None):
    """挂在墙上的画：画框 + 衬纸 + 投影。(x, y) 为画框中心，h 为画心高度。"""
    if a <= 0.003:
        return
    iw, ih = size(key)
    w = w or h * iw / ih
    pad, fr = h * 0.06, h * 0.035
    X, Y = x - w / 2, y - h / 2
    for k in range(6):
        e = (k + 1) * 6
        rrect(ctx, X - pad - fr - e / 2 + 10, Y - pad - fr - e / 2 + 18, w + 2 * (pad + fr) + e,
              h + 2 * (pad + fr) + e, 6 + e / 2)
        setc(ctx, "#000000", shadow * a / 7)
        ctx.fill()
    rrect(ctx, X - pad - fr, Y - pad - fr, w + 2 * (pad + fr), h + 2 * (pad + fr), 4)
    ctx.set_source(lin(X, Y, X + w, Y + h, [(0, "#8A6238", a), (0.5, frame, a), (1, "#2E1E0E", a)]))
    ctx.fill()
    rrect(ctx, X - pad, Y - pad, w + 2 * pad, h + 2 * pad, 2)
    setc(ctx, mat, a)
    ctx.fill()
    show(ctx, key, crop or (0.5, 0.5, 1.0), (X, Y, w, h), a, fit="cover")


def caption(ctx, title, sub="", a=1.0, x=118, y=None, size=36):
    """档案出处字幕（画面左下，黑边之上）。"""
    if a <= 0.003:
        return
    y = y or (H - 96 - 84)
    tw = max(len(title) * size * 0.95, len(sub) * size * 0.6) + 40
    ctx.set_source(lin(x - 30, 0, x + tw + 120, 0, [(0, "#000000", 0.55 * a), (0.7, "#000000", 0.3 * a),
                                                   (1, "#000000", 0)]))
    ctx.rectangle(x - 40, y - size * 1.1, tw + 200, size * 2.9)
    ctx.fill()
    ctx.rectangle(x - 18, y - size * 0.75, 3, size * 2.1)
    setc(ctx, "#D9B26A", 0.9 * a)
    ctx.fill()
    text(ctx, title, x, y, size, "#F4E6C8", a, "serif_sb", "l")
    if sub:
        text(ctx, sub, x, y + size * 1.05, size * 0.72, "#D8C6A0", a * 0.95, "serif_m", "l")


def light_leak(ctx, t, x, y, color="#FFB466", a=0.25):
    """镜头漏光：一团缓慢移动的暖光（叠加模式）。"""
    if a <= 0.003:
        return
    ctx.save()
    ctx.set_operator(cairo.OPERATOR_SCREEN)
    ox = x + math.sin(t * 0.3) * 120
    oy = y + math.cos(t * 0.23) * 60
    ctx.set_source(rad(ox, oy, 0, 900, [(0, color, a), (0.5, color, a * 0.3), (1, color, 0)]))
    ctx.paint()
    ctx.restore()
