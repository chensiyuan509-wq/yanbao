"""原理图 / 结构图：节点、连线（描出 + 流动光点）、分组框、轨道。适用于任何题材的"机制镜头"：
蒸汽机的气路、干涉仪的光路、程序的数据流、系统架构、行星轨道……

    node(ctx, 500, 400, 260, 110, "请求", "HTTP GET", k=reveal(t, T0, 0), theme="blueprint", hot=h)
    edge(ctx, (630, 400), (900, 400), p=ease_io(prog(t, T0 + 0.5, T0 + 1.2)), flow_t=t)
    orbit(ctx, 960, 540, 330, 250, rot=0.3, body=t * 0.8)
"""
import math

from .core import bezier_pts, glow, polyline_partial, rrect, setc, stroke_pts, text, arrow_head

THEME = {
    "blueprint": dict(fill="#08162A", fill_a=0.88, edge="#7FC8FF", title="#E8F2FF", sub="#BFE0FF", line="#7FD8FF",
                      dot="#BFEFFF", hot="#FFD27A"),
    "dark": dict(fill="#0E0C10", fill_a=0.85, edge="#D9B26A", title="#F6EEDF", sub="#CFC4B0", line="#D9B26A",
                 dot="#FFE2B0", hot="#FFD27A"),
    # 纸面（拜恩《几何原本》配色）：亮场，用在 proofs.paper(ctx) 背景上；hot 用拜恩红
    "paper": dict(fill="#FBF4E4", fill_a=0.95, edge="#1C1A18", title="#1C1A18", sub="#5A4A3A", line="#1C1A18",
                  dot="#C8372D", hot="#C8372D"),
}
BYRNE = dict(red="#C8372D", yellow="#EDB12C", blue="#2457A8", ink="#1C1A18", paper="#F2E8D2")


def node(ctx, x, y, w, h, title, sub=None, a=1.0, k=1.0, theme="blueprint", hot=0.0, title_size=28,
         fill_color=None, fill_a=0.85):
    """(x, y) 为中心。k：入场（淡入 + 轻微放大）；hot：高亮（辉光 + 粗边）；fill_color：色块填充（如拜恩红黄蓝）。"""
    th = THEME[theme]
    a = a * k
    if a <= 0.003:
        return
    s = 0.94 + 0.06 * k
    ww, hh = w * s, h * s
    if hot > 0 and theme != "paper":
        glow(ctx, x, y, max(w, h) * 0.9, th["hot"], 0.18 * hot * a)
    rrect(ctx, x - ww / 2, y - hh / 2, ww, hh, 12)
    setc(ctx, th["fill"], th["fill_a"] * a)
    ctx.fill()
    if fill_color:
        rrect(ctx, x - ww / 2, y - hh / 2, ww, hh, 12)
        setc(ctx, fill_color, fill_a * a)
        ctx.fill()
    rrect(ctx, x - ww / 2, y - hh / 2, ww, hh, 12)
    ctx.set_line_width(2 + 2 * hot)
    setc(ctx, th["hot"] if hot > 0.5 else th["edge"], (0.55 + 0.45 * hot) * a)
    ctx.stroke()
    if sub:
        text(ctx, title, x, y - 14, title_size, th["title"], a, "serif_sb")
        text(ctx, sub, x, y + 22, 20, th["sub"], a, "serif_r")
    else:
        text(ctx, title, x, y, title_size, th["title"], a, "serif_sb")


def edge(ctx, p0, p1, p=1.0, a=1.0, theme="blueprint", curve=0.0, flow_t=None, flow_n=3, flow_speed=0.6,
         arrow=True, dashed=False, label=None, width=3.0, color=None):
    """连线：p 为描出进度；curve 为弯曲量（相对长度，正负决定方向）；flow_t 给时间则有光点沿线流动。"""
    th = THEME[theme]
    col = color or th["line"]
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    c = curve * L
    pts = bezier_pts(p0, (x0 + dx * 0.33 + nx * c, y0 + dy * 0.33 + ny * c),
                     (x0 + dx * 0.67 + nx * c, y0 + dy * 0.67 + ny * c), p1, 40)
    part = polyline_partial(pts, p)
    if len(part) < 2 or a <= 0.003:
        return pts
    stroke_pts(ctx, part, width, col, 0.85 * a, dash=(10, 8) if dashed else None)
    if arrow and p > 0.97:
        (ax, ay), (bx, by) = pts[-2], pts[-1]
        arrow_head(ctx, bx, by, math.atan2(by - ay, bx - ax), 16, col, a)
    if flow_t is not None and p >= 1.0:
        for i in range(flow_n):
            f = (flow_t * flow_speed + i / flow_n) % 1
            idx = f * (len(pts) - 1)
            j = int(idx)
            q = idx - j
            px = pts[j][0] + (pts[min(j + 1, len(pts) - 1)][0] - pts[j][0]) * q
            py = pts[j][1] + (pts[min(j + 1, len(pts) - 1)][1] - pts[j][1]) * q
            glow(ctx, px, py, 16, th["dot"], 0.75 * a)
    if label:
        mx, my = pts[len(pts) // 2]
        text(ctx, label, mx + nx * 26, my + ny * 26, 20, th["sub"], a * min(1.0, p * 1.5), "serif_r")
    return pts


def group(ctx, x, y, w, h, label=None, a=1.0, theme="blueprint"):
    """虚线分组框（"浏览器""服务器""太阳系内侧"）。"""
    th = THEME[theme]
    if a <= 0.003:
        return
    rrect(ctx, x, y, w, h, 18)
    ctx.set_line_width(1.5)
    ctx.set_dash((8, 8))
    setc(ctx, th["edge"], 0.45 * a)
    ctx.stroke()
    ctx.set_dash(())
    if label:
        text(ctx, label, x + 20, y + 26, 20, th["sub"], a, "serif_r", "l")


def orbit(ctx, cx, cy, rx, ry, rot=0.0, a=1.0, theme="blueprint", body=None, body_r=10, body_color=None, trail=0.0,
          width=2.5):
    """椭圆轨道；body 为天体所在的角度（弧度），trail>0 画一段渐隐尾迹。返回天体坐标。"""
    th = THEME[theme]
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(rot)
    ctx.scale(1, ry / rx)
    ctx.arc(0, 0, rx, 0, math.tau)
    ctx.restore()
    ctx.set_line_width(width)
    setc(ctx, th["line"], 0.45 * a)
    ctx.stroke()
    if body is None:
        return None
    def pos(ang):
        px, py = rx * math.cos(ang), ry * math.sin(ang)
        return cx + px * math.cos(rot) - py * math.sin(rot), cy + px * math.sin(rot) + py * math.cos(rot)
    if trail > 0:
        pts = [pos(body - trail * i / 20) for i in range(21)]
        for i, (p, q) in enumerate(zip(pts, pts[1:])):
            stroke_pts(ctx, [p, q], width + 1.5, body_color or th["dot"], a * (1 - i / 20) * 0.8)
    bx, by = pos(body)
    glow(ctx, bx, by, body_r * 3, body_color or th["dot"], 0.7 * a)
    ctx.arc(bx, by, body_r, 0, math.tau)
    setc(ctx, body_color or "#FFFFFF", a)
    ctx.fill()
    return bx, by
