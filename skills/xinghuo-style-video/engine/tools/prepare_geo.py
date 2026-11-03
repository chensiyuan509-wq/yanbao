#!/usr/bin/env python3
"""把 Natural Earth（公有领域，1:5000 万）的陆地、湖泊、河流转成渲染用的紧凑 JSON。

  python tools/prepare_geo.py 下载目录      # 目录里放 ne_50m_land / lakes / rivers_lake_centerlines 的 geojson

数据来源：https://github.com/nvkelso/natural-earth-vector （Natural Earth，公有领域）
"""
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "geo")

RIVERS = {"Nile": "nile", "Euphrates": "euphrates", "Tigris": "tigris", "Indus": "indus", "Ganges": "ganges",
          "Huang": "yellow", "Yangtze": "yangtze", "Chang Jiang": "yangtze", "Danube": "danube", "Rhine": "rhine",
          "Volga": "volga", "Thames": "thames", "Po": "po", "Mississippi": "mississippi", "Amazon": "amazon",
          "Blue Nile": "blue_nile", "White Nile": "nile"}


def dp(pts, tol):
    """Douglas–Peucker 简化（迭代版）。"""
    if len(pts) < 4:
        return pts
    keep = np.zeros(len(pts), dtype=bool)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        if b <= a + 1:
            continue
        p, q = pts[a], pts[b]
        seg = pts[a + 1:b]
        d = q - p
        n = np.hypot(*d)
        if n < 1e-12:
            dist = np.hypot(*(seg - p).T)
        else:
            dist = np.abs(d[0] * (seg[:, 1] - p[1]) - d[1] * (seg[:, 0] - p[0])) / n
        i = int(np.argmax(dist))
        if dist[i] > tol:
            k = a + 1 + i
            keep[k] = True
            stack += [(a, k), (k, b)]
    return pts[keep]


def rings_of(geom):
    if geom["type"] == "Polygon":
        return geom["coordinates"]
    if geom["type"] == "MultiPolygon":
        return [r for poly in geom["coordinates"] for r in poly]
    return []


def lines_of(geom):
    if geom["type"] == "LineString":
        return [geom["coordinates"]]
    if geom["type"] == "MultiLineString":
        return geom["coordinates"]
    return []


def area(r):
    x, y = r[:, 0], r[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def polys(path, tol, min_area):
    out = []
    for f in json.load(open(path, encoding="utf-8"))["features"]:
        for ring in rings_of(f["geometry"]):
            r = np.array(ring, dtype=float)
            if area(r) < min_area:
                continue
            s = dp(r, tol)
            if len(s) >= 4:
                out.append(np.round(s, 2).tolist())
    return out


def main():
    src = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    geo = {}
    geo["land_hi"] = polys(os.path.join(src, "ne_50m_land.geojson"), 0.04, 0.02)
    geo["land_lo"] = polys(os.path.join(src, "ne_50m_land.geojson"), 0.25, 0.6)
    lakes = []
    for f in json.load(open(os.path.join(src, "ne_50m_lakes.geojson"), encoding="utf-8"))["features"]:
        nm = f["properties"].get("name") or ""
        for ring in rings_of(f["geometry"]):
            r = np.array(ring, dtype=float)
            if area(r) > 0.3 or nm in ("Caspian Sea", "Aral Sea", "Lake Victoria", "Lake Baikal"):
                lakes.append(np.round(dp(r, 0.04), 2).tolist())
    geo["lakes"] = lakes
    rivers = {}
    for f in json.load(open(os.path.join(src, "ne_50m_rivers_lake_centerlines.geojson"), encoding="utf-8"))["features"]:
        nm = f["properties"].get("name") or f["properties"].get("name_en") or ""
        key = None
        for k, v in RIVERS.items():
            if nm == k or nm.startswith(k + " ") or nm.endswith(" " + k):
                key = v
                break
        if not key:
            continue
        for ln in lines_of(f["geometry"]):
            rivers.setdefault(key, []).append(np.round(dp(np.array(ln, dtype=float), 0.03), 2).tolist())
    geo["rivers"] = rivers
    json.dump(geo, open(os.path.join(OUT, "world.json"), "w"), separators=(",", ":"))
    n_hi = sum(len(r) for r in geo["land_hi"])
    n_lo = sum(len(r) for r in geo["land_lo"])
    print(f"陆地 {len(geo['land_hi'])} 块 / {n_hi} 点（精细），{len(geo['land_lo'])} 块 / {n_lo} 点（全球）；"
          f"湖泊 {len(lakes)}；河流 {sorted(rivers)}")
    print("大小", os.path.getsize(os.path.join(OUT, "world.json")) // 1024, "KB")


if __name__ == "__main__":
    main()
