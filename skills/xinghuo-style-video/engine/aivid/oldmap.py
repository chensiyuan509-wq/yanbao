"""古地图风格的精确地图：羊皮纸底、墨线海岸、近岸波纹、河流、山脉符号、城市与航线。

坐标为 (经度, 纬度)。MapCam 把地图坐标投影到画面（等距圆柱 + 经度压缩），并可做关键帧运镜。
海岸线、湖泊、河流来自 Natural Earth 1:5000 万数据（公有领域，见 tools/prepare_geo.py），
近景用精细版、全球视角用简化版，只绘制视野内的部分。
"""
import math

import cairo

from .core import (H, W, TAU, circle, clamp, ease_io, ease_out, fill, glow, kf, lerp, lin, mix, poly, rad,
                   rrect, setc, smooth, stroke_pts, text, text_w, polyline_partial)
from .film import paint_texture, tracked
W_, H_ = W, H

MOUNTAINS = {
    "alps": [(6.5, 45.3), (7.5, 45.9), (8.5, 46.3), (10.0, 46.5), (11.5, 46.9), (13.0, 47.0), (14.5, 47.2)],
    "taurus": [(31.5, 37.2), (33.0, 37.2), (34.5, 37.4), (36.0, 37.9), (38.0, 38.2), (40.0, 38.6)],
    "zagros": [(45.5, 35.5), (47.0, 34.3), (48.5, 33.2), (50.0, 32.0), (51.5, 30.5), (53.0, 29.5)],
    "caucasus": [(40.5, 43.3), (42.5, 43.0), (44.5, 42.7), (46.5, 42.0), (48.0, 41.5)],
    "himalaya": [(74.0, 34.5), (76.5, 33.0), (79.0, 31.0), (81.5, 30.0), (84.0, 28.7), (86.5, 28.0), (89.0, 27.8),
                 (91.5, 27.9), (94.0, 28.5)],
    "hindukush": [(67.5, 35.0), (69.5, 35.5), (71.5, 36.0), (73.5, 36.5)],
    "tianshan": [(72.0, 41.0), (75.0, 41.5), (78.0, 42.0), (81.0, 43.0), (84.0, 43.5), (87.0, 43.3)],
    "atlas": [(-8.5, 31.0), (-6.5, 31.8), (-4.5, 32.5), (-2.0, 33.5), (1.0, 34.3), (4.0, 35.0)],
    "pyrenees": [(-1.5, 42.9), (0.0, 42.7), (1.5, 42.6), (2.8, 42.5)],
    "qinling": [(104.5, 34.0), (106.5, 33.8), (108.5, 33.9), (110.5, 33.8)],
}

CITIES = {
    "乌鲁克": (45.6, 31.3), "巴比伦": (44.4, 32.5), "吉萨": (31.1, 30.0), "底比斯": (32.6, 25.7),
    "赛伊尼": (32.9, 24.1), "亚历山大港": (29.9, 31.2), "雅典": (23.7, 38.0), "米利都": (27.3, 37.5),
    "萨摩斯": (26.9, 37.7), "叙拉古": (15.3, 37.1), "巴格达": (44.4, 33.3), "撒马尔罕": (67.0, 39.65),
    "长安": (108.9, 34.3), "洛阳": (112.45, 34.6), "开封": (114.3, 34.8), "安阳": (114.3, 36.1),
    "哈拉帕": (72.9, 30.6), "摩亨佐-达罗": (68.1, 27.3), "君士坦丁堡": (29.0, 41.0), "开罗": (31.2, 30.05),
    "托莱多": (-4.0, 39.9), "科尔多瓦": (-4.8, 37.9), "美因茨": (8.3, 50.0), "帕多瓦": (11.9, 45.4),
    "佛罗伦萨": (11.25, 43.77), "威尼斯": (12.33, 45.44), "弗龙堡": (19.7, 54.4), "布拉格": (14.4, 50.1),
    "伦敦": (-0.1, 51.5), "剑桥": (0.12, 52.2), "巴黎": (2.35, 48.85), "柏林": (13.4, 52.5),
    "哥廷根": (9.9, 51.5), "格拉斯哥": (-4.25, 55.86), "圣彼得堡": (30.3, 59.9), "乌贾因": (75.8, 23.2),
    "巨石阵": (-1.83, 51.18), "大马士革": (36.3, 33.5), "怛罗斯": (72.3, 42.5), "敦煌": (94.7, 40.1),
    "喀什": (76.0, 39.5), "罗马": (12.5, 41.9), "尼尼微": (43.15, 36.36), "孟菲斯": (31.25, 29.85),
}

# 近代科学中心（汤浅光朝的统计）
CENTERS = [("意大利", 11.5, 43.5, "1540–1610"), ("英国", -1.5, 52.5, "1660–1730"), ("法国", 2.3, 47.0, "1770–1830"),
           ("德国", 10.5, 51.0, "1810–1920"), ("美国", -77.0, 39.0, "1920–")]

LAT_K = 0.80            # 纬度方向不压缩，经度方向乘这个系数（中纬度看起来更自然）


class MapCam:
    """地图镜头：keys = [(t, (中心经度, 中心纬度, 每度像素)), ...]。"""

    def __init__(self, keys, cx=W / 2, cy=H / 2):
        self.keys = keys
        self.cx, self.cy = cx, cy
        self.lon, self.lat, self.k = keys[0][1]

    def at(self, t):
        self.lon, self.lat, self.k = kf(t, self.keys)
        return self

    def set(self, lon, lat, k):
        self.lon, self.lat, self.k = lon, lat, k
        return self

    def xy(self, lon, lat):
        return (self.cx + (lon - self.lon) * self.k * LAT_K, self.cy - (lat - self.lat) * self.k)

    def pts(self, ll):
        return [self.xy(*p) for p in ll]


def _path(ctx, pts):
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.close_path()


_GEO = {}


def geo():
    if not _GEO:
        import json
        import os
        p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "geo", "world.json")
        g = json.load(open(p))
        for key in ("land_hi", "land_lo", "lakes"):
            rings = []
            for r in g[key]:
                xs = [q[0] for q in r]
                ys = [q[1] for q in r]
                rings.append((min(xs), min(ys), max(xs), max(ys), r))
            _GEO[key] = rings
        _GEO["rivers"] = g["rivers"]
    return _GEO


def _visible(cam, rings, margin=4.0):
    lon_half = W / 2 / (cam.k * LAT_K) + margin
    lat_half = H / 2 / cam.k + margin
    lo0, lo1 = cam.lon - lon_half, cam.lon + lon_half
    la0, la1 = cam.lat - lat_half, cam.lat + lat_half
    return [r for (x0, y0, x1, y1, r) in rings if x1 >= lo0 and x0 <= lo1 and y1 >= la0 and y0 <= la1]


def _lands(cam):
    return _visible(cam, geo()["land_hi" if cam.k >= 9 else "land_lo"])


INK = "#3B2A1C"
SEA = "#AEB39B"
LAND = "#EEDDB4"


def draw_map(ctx, cam, t=0.0, a=1.0, world=False, rivers=None, river_p=None, mountains=True,
             grid=True, sea_labels=True, ink=INK, land=LAND, sea=SEA, tex=True):
    """画一张古地图（铺满画面）。rivers：要画的河流名；river_p：{河流: 描线进度}。"""
    if a <= 0.003:
        return
    grp = a < 0.999
    if grp:
        ctx.push_group()
    # 海面 / 纸底
    ctx.set_source(lin(0, 0, 0, H, [(0, mix(sea, "#FFFFFF", 0.06)), (1, mix(sea, "#000000", 0.06))]))
    ctx.paint()
    ox, oy = cam.xy(0, 0)
    k = cam.k
    lw = clamp(k / 14, 0.9, 3.2)
    # 经纬网
    if grid:
        step = 10 if k < 40 else 5
        ctx.set_line_width(1.2)
        setc(ctx, ink, 0.12)
        lon0 = math.floor((cam.lon - W / (k * LAT_K)) / step) * step
        lon = lon0
        while lon < cam.lon + W / (k * LAT_K):
            x, _ = cam.xy(lon, 0)
            ctx.move_to(x, -10)
            ctx.line_to(x, H + 10)
            lon += step
        lat = math.floor((cam.lat - H / k) / step) * step
        while lat < cam.lat + H / k:
            _, y = cam.xy(0, lat)
            ctx.move_to(-10, y)
            ctx.line_to(W + 10, y)
            lat += step
        ctx.stroke()
    lands = [cam.pts(L) for L in _lands(cam)]
    # 近岸波纹（在海那一侧）
    for wdt, al in ((44, 0.05), (28, 0.07), (14, 0.1)):
        ctx.set_line_width(wdt * clamp(k / 18, 0.5, 2.0))
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        setc(ctx, ink, al)
        for P in lands:
            _path(ctx, P)
        ctx.stroke()
    # 陆地
    for P in lands:
        _path(ctx, P)
    ctx.set_source(lin(0, 0, W, H, [(0, mix(land, "#FFFFFF", 0.1), 0.92), (1, mix(land, "#8A6A3A", 0.1), 0.92)]))
    ctx.fill()
    # 湖泊（里海、咸海等）
    seas = [cam.pts(S) for S in _visible(cam, geo()["lakes"])]
    for P in seas:
        _path(ctx, P)
    setc(ctx, sea, 0.95)
    ctx.fill()
    ctx.set_line_width(10 * clamp(k / 18, 0.5, 2.0))
    setc(ctx, ink, 0.08)
    for P in seas:
        _path(ctx, P)
    ctx.stroke()
    # 海岸线
    ctx.set_line_width(lw)
    setc(ctx, ink, 0.85)
    for P in lands + seas:
        _path(ctx, P)
    ctx.stroke()
    # 山脉
    if mountains and k > 8:
        ms = clamp(k * 0.55, 6, 26)
        for name, ll in MOUNTAINS.items():
            P = cam.pts(ll)
            for i in range(len(P) - 1):
                for f in (0.0, 0.5):
                    x, y = lerp(P[i][0], P[i + 1][0], f), lerp(P[i][1], P[i + 1][1], f)
                    if -50 < x < W + 50 and -50 < y < H + 50:
                        ctx.move_to(x - ms, y + ms * 0.5)
                        ctx.line_to(x, y - ms * 0.6)
                        ctx.line_to(x + ms, y + ms * 0.5)
                        setc(ctx, "#C8AE7E", 0.9)
                        ctx.fill_preserve()
                        ctx.set_line_width(max(1.0, lw * 0.8))
                        setc(ctx, ink, 0.7)
                        ctx.stroke()
                        ctx.move_to(x, y - ms * 0.6)
                        ctx.line_to(x + ms * 0.35, y + ms * 0.5)
                        setc(ctx, ink, 0.35)
                        ctx.stroke()
    # 河流
    names = rivers if rivers is not None else list(geo()["rivers"])
    for name in names:
        p = 1.0 if river_p is None else river_p.get(name, 1.0)
        if p <= 0.001:
            continue
        for line in river_lines(name):
            seg = polyline_partial(cam.pts(line), p)
            stroke_pts(ctx, seg, max(1.5, lw * 1.3), "#3E5A6B", 0.85)
    if tex:       # 纸纹：正片叠底，保留底色
        ctx.save()
        ctx.set_operator(cairo.OPERATOR_MULTIPLY)
        paint_texture(ctx, "parchment", -200, -200, W + 400, H + 400, 0.85, scale=1.0,
                      ox=-(ox % 2048), oy=-(oy % 1152))
        ctx.restore()
    if sea_labels and k > 6:
        lab = [("地 中 海", 18.0, 34.5), ("红 海", 38.2, 20.5), ("波斯湾", 51.0, 27.2), ("阿 拉 伯 海", 63.0, 16.0),
               ("黑 海", 34.5, 43.3), ("里海", 50.6, 41.8), ("孟加拉湾", 88.5, 15.0), ("大 西 洋", -22.0, 40.0)]
        size = clamp(k * 0.75, 14, 34)
        for s, lo, la in lab:
            x, y = cam.xy(lo, la)
            if -200 < x < W + 200 and -100 < y < H + 100:
                text(ctx, s, x, y, size, "#5B4630", 0.55, "serif_l")
    if grp:
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(clamp(a))


def river_lines(name):
    """某条河的折线（Natural Earth）。"""
    return geo()["rivers"].get(name, [])


def map_vignette(ctx, a=0.6):
    """古地图的焦边暗角。"""
    ctx.set_source(rad(W / 2, H / 2, H * 0.35, H * 1.1, [(0, "#2A1A0C", 0), (0.7, "#2A1A0C", 0.35 * a),
                                                         (1, "#1A0E05", a)]))
    ctx.paint()


def city(ctx, cam, name, a=1.0, k=1.0, size=30, color="#7A2E16", dx=0, dy=-34, t=0.0, pulse=False,
         label=None, align="c"):
    """城市标记：墨点 + 圆圈 + 宋体地名。"""
    if a <= 0.003 or k <= 0.01:
        return
    lon, lat = CITIES[name]
    x, y = cam.xy(lon, lat)
    if pulse:
        ph = (t * 0.7) % 1
        ctx.set_line_width(3)
        setc(ctx, color, a * (1 - ph) * 0.7)
        circle(ctx, x, y, 8 + ph * 40)
        ctx.stroke()
    glow(ctx, x, y, 34 * k, "#FFD98A", 0.45 * a)
    circle(ctx, x, y, 9 * k)
    setc(ctx, "#F5E6C4", a)
    ctx.fill_preserve()
    ctx.set_line_width(3)
    setc(ctx, color, a)
    ctx.stroke()
    circle(ctx, x, y, 4 * k)
    setc(ctx, color, a)
    ctx.fill()
    s = label or name
    if s:
        ax = x + dx
        text(ctx, s, ax + 2, y + dy + 2, size, "#F7EBD0", 0.6 * a * k, "serif_sb", align)
        text(ctx, s, ax, y + dy, size, "#3B2414", a * k, "serif_sb", align)
    return x, y


def route(ctx, cam, ll, p=1.0, color="#B2401E", a=1.0, w=4.0, dash=(14, 10), t=0.0, head=True, glow_a=0.5):
    """沿 ll 的航线 / 商路（描线进度 p），带流动的虚线与光点。"""
    if a <= 0.003 or p <= 0.001:
        return None
    P = cam.pts(ll)
    seg = polyline_partial(P, p)
    if len(seg) < 2:
        return None
    stroke_pts(ctx, seg, w + 6, "#F7E7C2", 0.6 * a)
    stroke_pts(ctx, seg, w, color, a, dash=dash, offset=-t * 40)
    if head:
        x, y = seg[-1]
        glow(ctx, x, y, 30, "#FFD27A", glow_a * a)
        circle(ctx, x, y, w * 1.6)
        setc(ctx, color, a)
        ctx.fill()
    return seg[-1]


def compass_rose(ctx, x, y, r, a=1.0, rot=0.0, ink=INK):
    if a <= 0.003:
        return
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.set_line_width(2)
    setc(ctx, ink, 0.6 * a)
    circle(ctx, 0, 0, r * 0.62)
    ctx.stroke()
    circle(ctx, 0, 0, r * 0.7)
    ctx.stroke()
    for i in range(16):
        ang = i * TAU / 16
        L = r if i % 4 == 0 else (r * 0.72 if i % 2 == 0 else r * 0.5)
        w = r * (0.13 if i % 4 == 0 else 0.08)
        for side, col in ((1, ink), (-1, "#E9D7AE")):
            poly(ctx, [(0, 0), (math.cos(ang) * L, math.sin(ang) * L),
                       (math.cos(ang + side * math.pi / 2) * w, math.sin(ang + side * math.pi / 2) * w)])
            setc(ctx, col, a * (0.85 if col == ink else 0.95))
            ctx.fill()
    text(ctx, "N", 0, -r - 22, r * 0.28, ink, a, "latin_b")
    ctx.restore()


# ---------------------------------------------------------------- 真实卫星底图（NASA 蓝色弹珠 / 夜间灯光，公有领域）


def draw_satellite(ctx, cam, t=0.0, a=1.0, layer="day", tone="warm", rivers=None, river_p=None, coast=0.25, grid=0.06):
    """把 NASA 的等距圆柱投影卫星影像贴到地图镜头上。tone: warm（古代，暖褐）/ natural / cool。"""
    import cairo
    from .archive import _load
    key = "bluemarble" if layer == "day" else "citylights"
    full, _ = _load(key)
    iw, ih = full.get_width(), full.get_height()
    sx = 360.0 / iw * cam.k * LAT_K
    sy = 180.0 / ih * cam.k
    m = ctx.get_matrix()
    dev = sx * math.hypot(m.xx, m.yx)
    level = 0
    while dev < 0.45 and level < 3:
        dev *= 2
        level += 1
    surf, _ = _load(key, level)
    f = 2 ** level
    ctx.save()
    ctx.rectangle(-50, -50, W + 100, H + 100)
    ctx.clip()
    ctx.set_source_rgb(0.02, 0.03, 0.06)
    ctx.paint()
    for wrap in (-360, 0, 360):            # 跨越日期变更线时左右各补一张
        x0 = cam.cx + (-180 + wrap - cam.lon) * cam.k * LAT_K
        if x0 > W + 50 or x0 + 360 * cam.k * LAT_K < -50:
            continue
        ctx.save()
        ctx.translate(x0, cam.cy - (90 - cam.lat) * cam.k)
        ctx.scale(sx * f, sy * f)
        ctx.set_source_surface(surf, 0, 0)
        ctx.get_source().set_filter(cairo.FILTER_GOOD)
        ctx.paint_with_alpha(a)
        ctx.restore()
    ctx.restore()
    if tone == "warm":
        ctx.save()
        ctx.set_operator(cairo.OPERATOR_HSL_SATURATION)
        ctx.set_source_rgba(0.5, 0.5, 0.5, 0.45 * a)
        ctx.paint()
        ctx.set_operator(cairo.OPERATOR_SOFT_LIGHT)
        ctx.set_source_rgba(0.85, 0.6, 0.35, 0.55 * a)
        ctx.paint()
        ctx.restore()
    elif tone == "cool":
        ctx.save()
        ctx.set_operator(cairo.OPERATOR_SOFT_LIGHT)
        ctx.set_source_rgba(0.3, 0.45, 0.8, 0.4 * a)
        ctx.paint()
        ctx.restore()
    # 经纬网
    if grid > 0:
        step = 10 if cam.k < 40 else 5
        ctx.set_line_width(1.2)
        setc(ctx, "#FFFFFF", grid * a)
        lon = math.floor((cam.lon - W / (cam.k * LAT_K)) / step) * step
        while lon < cam.lon + W / (cam.k * LAT_K):
            x, _ = cam.xy(lon, 0)
            ctx.move_to(x, -10)
            ctx.line_to(x, H + 10)
            lon += step
        lat = math.floor((cam.lat - H / cam.k) / step) * step
        while lat < cam.lat + H / cam.k:
            _, y = cam.xy(0, lat)
            ctx.move_to(-10, y)
            ctx.line_to(W + 10, y)
            lat += step
        ctx.stroke()
    # 淡淡的海岸线
    if coast > 0:
        ctx.set_line_width(clamp(cam.k / 16, 0.8, 2.2))
        setc(ctx, "#F2E6CC" if layer == "day" else "#9FC8FF", coast * a)
        for P in [cam.pts(L) for L in _lands(cam)]:
            _path(ctx, P)
        ctx.stroke()
    names = rivers or []
    for name in names:
        p = 1.0 if river_p is None else river_p.get(name, 1.0)
        if p <= 0.001:
            continue
        for line in river_lines(name):
            seg = polyline_partial(cam.pts(line), p)
            stroke_pts(ctx, seg, 10, "#7FD8FF", 0.15 * a)
            stroke_pts(ctx, seg, 3, "#BFEFFF", 0.8 * a)


def sat_vignette(ctx, a=0.55):
    ctx.set_source(rad(W / 2, H / 2, H * 0.4, H * 1.1, [(0, "#000000", 0), (0.7, "#000000", 0.3 * a), (1, "#000000", a)]))
    ctx.paint()


def city_sat(ctx, cam, name, a=1.0, k=1.0, size=28, color="#FFD27A", dy=-34, t=0.0, pulse=True, label=None, lonlat=None):
    """卫星图上的城市标记：发光点 + 白色宋体地名。"""
    if a <= 0.003:
        return None
    lon, lat = lonlat or CITIES[name]
    x, y = cam.xy(lon, lat)
    if pulse:
        ph = (t * 0.7) % 1
        ctx.set_line_width(2.5)
        setc(ctx, color, a * (1 - ph) * 0.8)
        circle(ctx, x, y, 8 + ph * 36)
        ctx.stroke()
    glow(ctx, x, y, 40 * k, color, 0.7 * a)
    circle(ctx, x, y, 6 * k)
    setc(ctx, "#FFFFFF", a)
    ctx.fill()
    s = label or name
    if s:
        text(ctx, s, x + 2, y + dy + 2.5, size, "#000000", 0.7 * a * k, "serif_sb")
        text(ctx, s, x, y + dy, size, "#FFF4E0", a * k, "serif_sb")
    return x, y
