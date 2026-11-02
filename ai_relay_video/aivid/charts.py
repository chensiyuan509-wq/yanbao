"""图表与地图：飞轮、柱状图、甜甜圈图、J 曲线、点阵世界地图、飞行弧线。"""
import math

from .core import (TAU, arrow_head, circle, clamp, ease_out, ease_out5, fill, glow, lerp, lin, mix,
                   poly, rad, rrect, setc, smooth, stroke_pts, text, text_w)

# ---------------------------------------------------------------- 飞轮


def flywheel(ctx, x, y, r, labels, rot=0.0, colors=None, a=1.0, lit=None, size=30, jam=0.0, t=0.0,
             thick=None, label_r=None, center=None, center_color="#2B2233"):
    """飞轮：环形分段 + 段间箭头 + 段上标签。lit[i] 为第 i 段点亮程度；jam>0 时生锈卡住（发灰、抖动）。"""
    if a <= 0.003:
        return
    n = len(labels)
    colors = colors or ["#FF9F68", "#8B6CFF", "#2EC4B6", "#4C8DFF", "#FF6B9A"][:n]
    thick = thick or r * 0.34
    if jam > 0:
        rot += math.sin(t * 40) * 0.01 * jam
    gap = 0.08
    for i in range(n):
        a0 = rot + i * TAU / n + gap / 2 - math.pi / 2
        a1 = rot + (i + 1) * TAU / n - gap / 2 - math.pi / 2
        k = 1.0 if lit is None else clamp(lit[i])
        c = mix(colors[i % len(colors)], "#9AA0AE", jam * 0.85)
        ctx.new_path()
        ctx.arc(x, y, r, a0, a1)
        ctx.arc_negative(x, y, r - thick, a1, a0)
        ctx.close_path()
        setc(ctx, c, a * (0.28 + 0.72 * k))
        ctx.fill()
        # 段末的箭头
        am = a1 + gap * 0.1
        ax, ay = x + math.cos(am) * (r - thick / 2), y + math.sin(am) * (r - thick / 2)
        arrow_head(ctx, ax + math.cos(am + math.pi / 2) * 10, ay + math.sin(am + math.pi / 2) * 10,
                   am + math.pi / 2, thick * 0.55, c, a * (0.28 + 0.72 * k))
        # 标签
        mid = (a0 + a1) / 2
        lr = label_r or (r - thick / 2)
        lx, ly = x + math.cos(mid) * lr, y + math.sin(mid) * lr
        text(ctx, labels[i], lx, ly, size, "#FFFFFF", a * (0.45 + 0.55 * k), "black")
    if center:
        circle(ctx, x, y, r - thick - 14)
        fill(ctx, "#FFFFFF", 0.92 * a)
        text(ctx, center, x, y, size * 1.1, center_color, a, "black")
    if jam > 0.05:
        for i in range(5):
            ang = i * 1.3 + 0.4
            px, py = x + math.cos(ang) * (r - thick / 2), y + math.sin(ang) * (r - thick / 2)
            circle(ctx, px, py, 10 + 6 * (i % 2))
            fill(ctx, "#8A5A3A", 0.6 * jam * a)


# ---------------------------------------------------------------- 柱状图


def hbars(ctx, items, x, y, w, row_h, p=1.0, a=1.0, size=28, vmax=None, label_w=230, value_fmt=None,
          stagger=0.18, bar_h=None):
    """水平柱状图。items = [(标签, 数值, 颜色[, 数值文字])]。"""
    vmax = vmax or max(v for _, v, *_ in items)
    bh = bar_h or row_h * 0.62
    for i, it in enumerate(items):
        lab, v, c = it[0], it[1], it[2]
        vt = it[3] if len(it) > 3 else (value_fmt(v) if value_fmt else f"{v}")
        q = ease_out5(clamp((p - i * stagger) / max(1e-3, 1 - stagger * (len(items) - 1)))) if len(items) > 1 \
            else ease_out5(p)
        yy = y + i * row_h
        text(ctx, lab, x + label_w - 20, yy, size, "#2B2233", a, "black", "r")
        bw = max(bh, (w - label_w) * v / vmax * q)
        rrect(ctx, x + label_w, yy - bh / 2, bw, bh, bh / 2)
        ctx.set_source(lin(x + label_w, 0, x + label_w + bw, 0, [(0, mix(c, "#FFFFFF", 0.2), a), (1, c, a)]))
        ctx.fill()
        if q > 0.2:
            text(ctx, vt, x + label_w + bw + 16, yy, size * 0.9, c, a * smooth((q - 0.2) / 0.5), "black", "l")


def vbars(ctx, items, x, base_y, bw, gap, hmax, p=1.0, a=1.0, size=26, vmax=None, log=False, stagger=0.2,
          value_color=None, label_color="#2B2233"):
    """竖直柱状图，items = [(标签, 数值, 颜色, 数值文字)]。log=True 用对数刻度。"""
    vals = [it[1] for it in items]
    if log:
        lo = math.log10(min(vals)) - 0.6
        hi = math.log10(vmax or max(vals))
        hv = [(math.log10(v) - lo) / (hi - lo) for v in vals]
    else:
        m = vmax or max(vals)
        hv = [v / m for v in vals]
    for i, it in enumerate(items):
        lab, v, c, vt = it[0], it[1], it[2], it[3]
        q = ease_out5(clamp((p - i * stagger) / max(1e-3, 1 - stagger * (len(items) - 1))))
        xx = x + i * (bw + gap)
        h = max(6, hmax * hv[i] * q)
        rrect(ctx, xx, base_y - h, bw, h, min(14, bw / 4))
        ctx.set_source(lin(0, base_y - h, 0, base_y, [(0, mix(c, "#FFFFFF", 0.25), a), (1, c, a)]))
        ctx.fill()
        text(ctx, lab, xx + bw / 2, base_y + size * 0.95, size, label_color, a, "bold")
        if q > 0.3:
            text(ctx, vt, xx + bw / 2, base_y - h - size * 0.8, size * 1.05, value_color or c,
                 a * smooth((q - 0.3) / 0.4), "black")


def donut(ctx, x, y, r, parts, p=1.0, a=1.0, thick=None, rot=-math.pi / 2, gap=0.02):
    """甜甜圈图，parts = [(比例, 颜色)]。"""
    thick = thick or r * 0.36
    acc = 0.0
    for frac, c in parts:
        a0 = rot + acc * TAU
        a1 = rot + min(acc + frac, p) * TAU
        if a1 > a0 + gap:
            ctx.new_path()
            ctx.arc(x, y, r, a0 + gap / 2, a1 - gap / 2)
            ctx.arc_negative(x, y, r - thick, a1 - gap / 2, a0 + gap / 2)
            ctx.close_path()
            setc(ctx, c, a)
            ctx.fill()
        acc += frac
        if acc >= p:
            break


def j_curve(ctx, x0, y0, w, h, p=1.0, a=1.0, color="#FF9F68", dip=0.55):
    """J 曲线：先投入（向下）后收获（向上）。(x0, y0) 为零线左端，h 为纵向尺度。"""
    from .core import bezier_pts, polyline_partial
    seg1 = bezier_pts((0, 0), (0.12, -1.2 * dip), (0.4, -1.2 * dip), (0.6, 0), 40)
    seg2 = bezier_pts((0.6, 0), (0.72, 0.72 * dip), (0.85, 0.85), (1.0, 1.0), 40)
    pts = [(x0 + u * w, y0 - v * h * 0.5) for (u, v) in seg1 + seg2[1:]]
    ctx.set_line_width(3)
    setc(ctx, "#2B2233", 0.35 * a)
    ctx.move_to(x0, y0)
    ctx.line_to(x0 + w, y0)
    ctx.stroke()
    seg = polyline_partial(pts, 0, p)
    if len(seg) > 1:
        ctx.save()
        poly(ctx, seg + [(seg[-1][0], y0), (x0, y0)])
        ctx.clip()
        ctx.rectangle(x0, y0, w, h)
        setc(ctx, "#E5484D", 0.18 * a)
        ctx.fill()
        ctx.rectangle(x0, y0 - h, w, h)
        setc(ctx, "#3CCB7F", 0.2 * a)
        ctx.fill()
        ctx.restore()
        stroke_pts(ctx, seg, 7, color, a)
        glow(ctx, seg[-1][0], seg[-1][1], 26, color, 0.7 * a)
    return pts


# ---------------------------------------------------------------- 点阵世界地图

# 粗略的大陆轮廓（经度, 纬度），只用于点阵风格的示意地图
_CONT = {
    "na": [(-168, 66), (-160, 70), (-150, 71), (-140, 70), (-128, 70), (-118, 70), (-105, 69), (-95, 72),
           (-85, 70), (-80, 64), (-77, 60), (-79, 54), (-82, 52), (-88, 56), (-94, 59), (-94, 64), (-88, 66),
           (-82, 66), (-72, 62), (-64, 60), (-56, 52), (-60, 47), (-67, 45), (-70, 42), (-75, 38), (-76, 35),
           (-81, 31), (-80, 25), (-83, 29), (-89, 30), (-95, 29), (-97, 26), (-97, 21), (-95, 18), (-90, 16),
           (-87, 15), (-83, 10), (-78, 8), (-80, 8), (-84, 10), (-86, 12), (-92, 15), (-97, 16), (-105, 20),
           (-106, 23), (-110, 24), (-112, 29), (-115, 30), (-117, 33), (-121, 35), (-124, 40), (-124, 46),
           (-125, 49), (-130, 54), (-136, 58), (-145, 60), (-152, 59), (-158, 57), (-164, 55), (-160, 59),
           (-165, 62)],
    "gl": [(-73, 78), (-60, 82), (-30, 83), (-20, 80), (-18, 75), (-22, 70), (-30, 68), (-40, 65), (-43, 60),
           (-50, 62), (-53, 66), (-55, 70), (-60, 76)],
    "sa": [(-80, 9), (-75, 11), (-70, 12), (-62, 11), (-55, 6), (-50, 2), (-45, -1), (-38, -4), (-35, -7),
           (-37, -12), (-39, -17), (-41, -22), (-45, -24), (-48, -28), (-53, -34), (-58, -38), (-62, -40),
           (-65, -45), (-68, -50), (-70, -54), (-74, -52), (-75, -46), (-73, -40), (-72, -33), (-71, -25),
           (-70, -18), (-75, -15), (-77, -12), (-80, -6), (-81, -3), (-80, 1), (-78, 4), (-77, 7)],
    "eu_as": [(-9.5, 37), (-9, 43.5), (-1.5, 43.5), (-1, 46), (-4.5, 48), (-1, 49.5), (2, 51), (5, 53),
              (8.5, 54), (8, 57), (10.5, 57.5), (12, 56), (5, 59), (5, 62), (10, 64), (14, 67), (18, 69.5),
              (25, 71), (30, 70), (40, 68), (50, 68), (60, 69), (68, 70), (70, 73), (80, 73), (90, 76),
              (100, 78), (110, 77), (120, 73), (130, 72), (140, 72), (150, 71), (160, 70), (170, 70),
              (180, 68), (178, 64), (170, 60), (163, 58), (160, 52), (156, 51), (156, 57), (150, 59),
              (142, 59), (137, 54), (140, 52), (141, 48), (135, 44), (130, 42), (129, 35), (126, 34.5),
              (126, 37), (125, 39.5), (122, 40), (118, 38), (120, 37), (122, 37), (120, 34), (121, 31),
              (122, 30), (120, 26), (117, 24), (113, 22), (110, 21), (108, 21.5), (106, 19), (108, 16),
              (109, 12), (107, 10.5), (105, 9), (104.5, 10.5), (100, 13.5), (99, 10), (100, 7), (103, 4),
              (104, 1.5), (101, 3), (98, 8), (98, 16), (94, 18), (92, 22), (90, 22), (87, 21), (85, 19.5),
              (81, 16), (80, 13), (79.5, 10), (77.5, 8), (76, 10), (74, 15), (73, 19), (72.5, 21), (69, 22.5),
              (67, 24.5), (62, 25), (57, 26), (59, 23), (57, 19), (52, 16), (45, 13), (43, 13), (42.5, 16),
              (39, 21), (35, 28), (34.5, 29.5), (32.5, 30), (34, 31.5), (35.5, 33.5), (36, 36), (32, 36.5),
              (28, 36.5), (26, 38), (26, 40), (23, 40.5), (22, 37), (20, 40), (19, 42), (13.5, 45.5),
              (12.5, 44), (14, 42), (16, 40), (16, 38), (15.5, 40), (12, 42), (10, 44), (8, 44), (5, 43),
              (3, 43), (3, 41.5), (0, 39.5), (-0.5, 38), (-2, 36.7), (-5, 36), (-6, 36)],
    "gb": [(-5.5, 50), (1.5, 51), (1.5, 53), (-0.5, 54.5), (-2, 56), (-2, 57.6), (-4, 58.6), (-5.5, 57),
           (-5, 55), (-3, 54.5), (-3, 53.4), (-4.5, 52)],
    "af": [(-17, 21), (-17, 15), (-15, 11), (-13, 8), (-8, 4.5), (-4, 5), (2, 6), (5, 4.5), (8.5, 4.5), (9.5, 3),
           (9, -1), (11.5, -5), (12, -8), (13.5, -12), (12, -17), (14, -22), (15, -27), (17, -29), (18.5, -34),
           (20, -35), (22, -34), (26, -34), (30, -31), (33, -27), (35, -24), (35.5, -21), (40, -16),
           (40.5, -11), (39.5, -6), (39, -4), (41, -1.5), (43, 0), (47, 4), (51, 11), (43.5, 11.5), (42, 14.5),
           (40, 16), (38, 18), (37, 22), (35.5, 24), (34, 27), (32.5, 30), (30, 31), (25, 31.5), (20, 31.5),
           (19, 30.5), (15, 32.5), (11, 33.5), (10, 37), (5, 36.8), (0, 35.8), (-2, 35), (-5.5, 35.8), (-6, 34),
           (-9, 32), (-10, 29), (-13, 27)],
    "mg": [(44, -25), (47, -25), (50, -15), (49.5, -12), (44.5, -16), (43.5, -22)],
    "au": [(114, -22), (114, -26), (115, -34), (118, -35), (123, -33.8), (129, -31.6), (135, -34.5),
           (138, -35.6), (140, -38), (144, -38), (147, -38), (150, -37), (152, -32), (153, -28), (153, -25),
           (149, -20), (146, -18.5), (145.5, -15), (143.5, -14), (142, -10.7), (141.5, -13), (141, -17),
           (140, -17.5), (137.5, -16), (136, -12), (132, -11.3), (130, -13), (129, -15), (126, -14), (122, -17),
           (121, -19.5), (117, -20.7)],
    "jp": [(129.5, 33), (131.5, 31), (135, 33.5), (139, 34.6), (141, 36), (142, 39.5), (141.5, 41.3),
           (145.5, 43.3), (141.8, 45.5), (139.8, 42.3), (140, 40), (139.5, 38), (137, 37), (135.5, 35.6),
           (132, 35.4), (130.8, 34)],
    "bo": [(109, 1), (111, -3), (116, -4), (119, 1), (117, 7), (113, 3)],
    "ng": [(131, -1), (141, -2.5), (150, -6), (147, -8), (141, -9), (138, -8), (132, -4)],
    "is": [(-24, 64), (-14, 64.5), (-15, 66.5), (-22, 66.5)],
}
_ISLES = [(96, 4), (99, 1), (102, -2), (105, -5), (107, -7), (111, -7.5), (114, -8), (120, -2), (121, 17),
          (122, 13), (124, 9), (125, 7), (81, 8), (109.5, 19), (121, 23.6), (-84, 22), (-79, 22), (-75, 20),
          (174, -37), (172, -42), (170, -45), (-8, 53), (-7, 54.5)]


def _inside(px, py, pts):
    c = False
    n = len(pts)
    j = n - 1
    for i in range(n):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi + 1e-12) + xi:
            c = not c
        j = i
    return c


_DOTS = {}


def land_dots(step=3.0):
    """返回陆地点阵 [(经度, 纬度)]（缓存）。"""
    if step in _DOTS:
        return _DOTS[step]
    out = []
    lat = 80.0
    while lat > -58:
        lon = -180.0 + step / 2
        while lon < 180:
            for pts in _CONT.values():
                if _inside(lon, lat, pts):
                    out.append((lon, lat))
                    break
            lon += step
        lat -= step
    for (lo, la) in _ISLES:
        out.append((round((lo - step / 2) / step) * step + step / 2, round(la / step) * step))
    _DOTS[step] = sorted(set(out))
    return _DOTS[step]


class MapView:
    """等距圆柱投影：把 (经度, 纬度) 映射到画面坐标。lon0 为画面中心经度（太平洋居中可设 160）。"""

    def __init__(self, cx, cy, scale, lon0=0.0, lat0=20.0):
        self.cx, self.cy, self.k, self.lon0, self.lat0 = cx, cy, scale, lon0, lat0

    def xy(self, lon, lat):
        d = (lon - self.lon0 + 540) % 360 - 180
        return self.cx + d * self.k, self.cy - (lat - self.lat0) * self.k


def world_dots(ctx, view, a=1.0, color="#FFFFFF", dot_a=0.35, step=3.0, r=None, hi=None, t=0.0,
               clip=None):
    """点阵世界地图。hi = {(经度, 纬度, 半径度数): 颜色} 高亮某些区域。"""
    if a <= 0.003:
        return
    r = r or view.k * step * 0.32
    hi = hi or {}
    norm_pts = []
    for (lon, lat) in land_dots(step):
        x, y = view.xy(lon, lat)
        if clip and not (clip[0] - 20 < x < clip[2] + 20 and clip[1] - 20 < y < clip[3] + 20):
            continue
        col = None
        for (hlon, hlat, hr), c in hi.items():
            d = math.hypot(((lon - hlon + 540) % 360 - 180), lat - hlat)
            if d < hr:
                col = c
                break
        if col:
            circle(ctx, x, y, r * 1.15)
            fill(ctx, col, a)
        else:
            norm_pts.append((x, y))
    setc(ctx, color, dot_a * a)
    for (x, y) in norm_pts:
        circle(ctx, x, y, r)
    ctx.fill()


def arc_pts(p0, p1, bend=0.25, n=60):
    """两点间的抛物线弧（飞行航线）。bend>0 向上拱。"""
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    d = math.dist(p0, p1)
    nx, ny = -(y1 - y0) / max(d, 1e-6), (x1 - x0) / max(d, 1e-6)
    if ny > 0:
        nx, ny = -nx, -ny
    cx, cy = mx + nx * d * bend, my + ny * d * bend
    out = []
    for i in range(n + 1):
        u = i / n
        v = 1 - u
        out.append((v * v * x0 + 2 * v * u * cx + u * u * x1, v * v * y0 + 2 * v * u * cy + u * u * y1))
    return out


def map_pin(ctx, x, y, color, label="", a=1.0, k=1.0, size=26, below=False, t=0.0, pulse=True):
    if a <= 0.003 or k <= 0.01:
        return
    if pulse:
        ph = (t * 0.8) % 1
        ctx.set_line_width(3)
        setc(ctx, color, a * (1 - ph) * 0.8)
        circle(ctx, x, y, 10 + ph * 34)
        ctx.stroke()
    glow(ctx, x, y, 40 * k, color, 0.5 * a)
    circle(ctx, x, y, 11 * k)
    fill(ctx, "#FFFFFF", a)
    circle(ctx, x, y, 7 * k)
    fill(ctx, color, a)
    if label:
        tw = text_w(ctx, label, size, "black")
        ly = y + (34 if below else -34) * k
        rrect(ctx, x - tw / 2 - 14, ly - size * 0.8, tw + 28, size * 1.6, size * 0.8)
        setc(ctx, "#1A1426", 0.78 * a)
        ctx.fill()
        text(ctx, label, x, ly, size, "#FFFFFF", a, "black")
