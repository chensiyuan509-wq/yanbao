"""人类知识星图：60 个里程碑按时间顺序排成一条光河。

光河的形状是一只张开的手（和第一章洞壁上的手印呼应）：手腕左侧是史前，绕过拇指、四指，
到手腕右侧是今天的 AI。序章只拍到局部，尾声镜头拉远时才看出是一只手。
"""
import math

from .core import (TAU, circle, clamp, glow, lerp, mix, polyline_partial, rad, rng, setc, smooth, star4,
                   stroke_pts, text)

S = 3000.0            # 星图世界尺寸（手掌宽约 0.8S、高约 1.2S）

_OUT = [(0.32, 1.18), (0.28, 0.98), (0.20, 0.84), (0.08, 0.70), (0.02, 0.58), (0.06, 0.53), (0.13, 0.58),
        (0.24, 0.66), (0.25, 0.50), (0.22, 0.30), (0.21, 0.16), (0.26, 0.12), (0.31, 0.16), (0.34, 0.42),
        (0.36, 0.20), (0.38, 0.04), (0.43, 0.01), (0.48, 0.05), (0.48, 0.40), (0.53, 0.18), (0.57, 0.07),
        (0.62, 0.07), (0.64, 0.14), (0.60, 0.45), (0.69, 0.30), (0.75, 0.22), (0.80, 0.24), (0.80, 0.32),
        (0.70, 0.62), (0.66, 0.80), (0.62, 0.98), (0.60, 1.18)]


def _smooth_path(pts, n=6, it=2):
    """Chaikin 细分，让轮廓圆润。"""
    for _ in range(it):
        out = [pts[0]]
        for a, b in zip(pts, pts[1:]):
            out.append((0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]))
            out.append((0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1]))
        out.append(pts[-1])
        pts = out
    return pts


PATH = [(x * S, y * S) for x, y in _smooth_path(_OUT, it=3)]
_SEG = [math.dist(a, b) for a, b in zip(PATH, PATH[1:])]
LENGTH = sum(_SEG)


def point(u):
    """光河上进度 u (0..1) 处的位置。"""
    d = clamp(u) * LENGTH
    acc = 0.0
    for (a, b), L in zip(zip(PATH, PATH[1:]), _SEG):
        if acc + L >= d:
            f = (d - acc) / L if L else 0
            return (lerp(a[0], b[0], f), lerp(a[1], b[1], f))
        acc += L
    return PATH[-1]


def tangent(u):
    a, b = point(u - 0.002), point(u + 0.002)
    return math.atan2(b[1] - a[1], b[0] - a[0])


# (名称, 年代标签, 年份数值（负数为公元前），是否重要)
STARS = [
    ("石器", "330 万年前", -3.3e6, 1), ("用火", "100 万年前", -1e6, 1), ("智人", "30 万年前", -3e5, 0),
    ("洞穴手印", "4 万年前", -4e4, 1), ("骨上刻痕", "4 万年前", -4.2e4, 0), ("农业", "1 万年前", -1e4, 1),
    ("楔形文字", "前 3200 年", -3200, 1), ("巨石阵", "前 3000 年", -3000, 0), ("365 天历", "古埃及", -2800, 0),
    ("六十进制", "两河流域", -2000, 0), ("勾股数表", "前 1800 年", -1800, 0), ("甲骨文", "前 1250 年", -1250, 0),
    ("泰勒斯", "前 585 年", -585, 0), ("毕达哥拉斯", "前 530 年", -530, 0), ("墨经", "前 4 世纪", -380, 0),
    ("亚里士多德", "前 350 年", -350, 0), ("几何原本", "前 300 年", -300, 1), ("阿基米德", "前 250 年", -250, 0),
    ("地球周长", "前 240 年", -240, 1), ("九章算术", "1 世纪", 50, 0), ("造纸术", "105 年", 105, 1),
    ("割圆术", "263 年", 263, 0), ("祖冲之 π", "约 480 年", 480, 0), ("数字 0", "628 年", 628, 1),
    ("智慧之家", "9 世纪", 830, 0), ("代数", "约 820 年", 820, 1), ("光学之书", "1021 年", 1021, 0),
    ("活字印刷", "1040 年代", 1045, 1), ("指南针", "11 世纪", 1088, 0), ("印刷机", "1450 年", 1450, 1),
    ("日心说", "1543 年", 1543, 1), ("望远镜", "1609 年", 1609, 1), ("行星定律", "1609 年", 1609, 0),
    ("皇家学会", "1660 年", 1660, 0), ("微生物", "1676 年", 1676, 0), ("万有引力", "1687 年", 1687, 1),
    ("蒸汽机", "1769 年", 1769, 1), ("电池", "1800 年", 1800, 0), ("电磁感应", "1831 年", 1831, 0),
    ("进化论", "1859 年", 1859, 1), ("电磁理论", "1865 年", 1865, 0), ("周期表", "1869 年", 1869, 1),
    ("X 射线", "1895 年", 1895, 0), ("相对论", "1905 年", 1905, 1), ("量子力学", "1925 年", 1925, 1),
    ("青霉素", "1928 年", 1928, 0), ("图灵机", "1936 年", 1936, 1), ("计算机", "1946 年", 1946, 0),
    ("晶体管", "1947 年", 1947, 0), ("DNA", "1953 年", 1953, 1), ("人工智能", "1956 年", 1956, 0),
    ("登月", "1969 年", 1969, 1), ("互联网", "1969 年", 1969, 0), ("万维网", "1989 年", 1989, 0),
    ("人类基因组", "2003 年", 2003, 0), ("深度学习", "2012 年", 2012, 0), ("AlphaGo", "2016 年", 2016, 0),
    ("Transformer", "2017 年", 2017, 0), ("AlphaFold", "2020 年", 2020, 1), ("大语言模型", "2022 年", 2022, 1),
]
N = len(STARS)


def star_u(i):
    return 0.012 + 0.976 * i / (N - 1)


STAR_POS = [point(star_u(i)) for i in range(N)]

# 八个"人类学会的方法"，环绕在手的外侧（尾声时亮起），坐标为手的归一化坐标
METHODS = [("观察", (0.10, 1.06)), ("记录", (-0.10, 0.64)), ("证明", (0.04, 0.26)), ("传承", (0.20, -0.04)),
           ("实验", (0.43, -0.12)), ("预言", (0.66, -0.06)), ("协作", (0.93, 0.12)), ("学习", (0.86, 0.92))]


def year_text(y):
    if y <= -10000:
        w = -y / 1e4
        return f"{w:,.0f} 万年前" if w >= 10 else f"{w:.1f} 万年前".replace(".0 ", " ")
    if y < 0:
        return f"公元前 {-y:.0f} 年"
    return f"公元 {y:.0f} 年"


def year_at(u):
    """光河进度 u 对应的（插值）年份，用于倒流计数器（按对数时间插值史前部分）。"""
    us = [star_u(i) for i in range(N)]
    if u <= us[0]:
        return STARS[0][2]
    for i in range(N - 1):
        if us[i] <= u <= us[i + 1]:
            f = (u - us[i]) / (us[i + 1] - us[i])
            a, b = STARS[i][2], STARS[i + 1][2]
            if a < -5000 and b < -5000:
                la, lb = math.log(-a), math.log(-b)
                return -math.exp(lerp(la, lb, f))
            return lerp(a, b, f)
    return 2026


def draw_sky(ctx, t, a=1.0):
    """星图背后的深空（在调用方的镜头坐标里画，范围略大于星图）。"""
    from .film import star_field
    star_field(ctx, t, 420, 77, area=(-1500, -1500, S + 3000, S * 1.3 + 3000), a=0.55 * a, size=(0.8, 2.4))
    R = rng(12)
    for i in range(10):
        x, y = R.uniform(-500, S + 500), R.uniform(-500, S * 1.25 + 500)
        r = R.uniform(500, 1100)
        c = ["#3A2C6B", "#5A2E4E", "#1E3E6B", "#6B4A2E"][i % 4]
        ctx.set_source(rad(x, y, 0, r, [(0, c, 0.22 * a), (1, c, 0)]))
        circle(ctx, x, y, r)
        ctx.fill()


def draw_map(ctx, t, a=1.0, lit=1.0, lit_from=0.0, label_a=1.0, path_a=1.0, zoom=1.0, focus=None,
             hot=None, color="#FFD58A", label_size=26, sub_size=19, methods_a=0.0, pulse_u=None):
    """画光河与星点。lit：已点亮到的进度（0..1）；hot：当前高亮的星序号；zoom 用于调整线宽 / 字号。"""
    if a <= 0.003:
        return
    iz = 1 / max(zoom, 0.05)
    # 光河
    if path_a > 0:
        full = polyline_partial(PATH, 0, 1)
        stroke_pts(ctx, full, 2.2 * iz, "#9FB4FF", 0.18 * a * path_a)
        if lit > lit_from:
            seg = polyline_partial(PATH, lit_from, lit)
            stroke_pts(ctx, seg, 22 * iz, color, 0.06 * a * path_a)
            stroke_pts(ctx, seg, 9 * iz, color, 0.14 * a * path_a)
            stroke_pts(ctx, seg, 3.2 * iz, "#FFF2D0", 0.75 * a * path_a)
            hx, hy = point(lit)
            if lit < 0.999:
                glow(ctx, hx, hy, 80 * iz, color, 0.7 * a)
    if pulse_u is not None:
        px, py = point(pulse_u)
        glow(ctx, px, py, 140 * iz, "#FFFFFF", 0.5 * a)
    # 星点
    for i, (name, sub, yr, big) in enumerate(STARS):
        u = star_u(i)
        x, y = STAR_POS[i]
        on = smooth(clamp((lit - u) / 0.01 + 1)) if lit < 1 else 1.0
        k = 0.25 + 0.75 * on
        r = (7 if big else 5) * iz
        tw = 0.8 + 0.2 * math.sin(t * 1.7 + i * 2.3)
        hot_k = 1.0 if hot == i else 0.0
        glow(ctx, x, y, (60 if big else 38) * iz * (1 + hot_k), color, 0.5 * a * k * tw)
        circle(ctx, x, y, r * (1 + 0.6 * hot_k))
        setc(ctx, mix("#FFFFFF", color, 0.3), a * k)
        ctx.fill()
        if big:
            star4(ctx, x, y, 26 * iz * tw * (0.6 + 0.4 * on), "#FFFFFF", 0.7 * a * k, 0.0)
        if label_a > 0.01:
            ang = tangent(u)
            nx, ny = -math.sin(ang), math.cos(ang)
            side = 1 if i % 2 == 0 else -1
            lx, ly = x + nx * side * 46 * iz, y + ny * side * 46 * iz
            la = label_a * a * (0.35 + 0.65 * on)
            ls = label_size * iz * (1.15 if big else 1.0)
            text(ctx, name, lx, ly - ls * 0.45, ls, "#FFF4DE", la, "serif_sb")
            text(ctx, sub, lx, ly + ls * 0.62, sub_size * iz, "#C9B98F", la * 0.85, "serif_l")
    if methods_a > 0.003:
        for j, (word, (nx_, ny_)) in enumerate(METHODS):
            x, y = nx_ * S, ny_ * S
            ms = 60 * iz
            text(ctx, word, x + 2 * iz, y + 2 * iz, ms, "#000000", 0.4 * methods_a * a, "serif_k")
            text(ctx, word, x, y, ms, "#FFE6B0", methods_a * a, "serif_k")


def hand_outline(ctx, x, y, w):
    """在 (x, y) 处画手的轮廓路径（宽 w，左上角为基准），用于洞壁手印。"""
    k = w / (0.82 * S)
    pts = [(x + px * k, y + py * k) for px, py in PATH]
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    return pts
