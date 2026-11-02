"""道具与图标：星空、星云、时钟、蜡烛、树、地球、月亮、卫星、火箭、黑洞等。"""
import math

from .core import (TAU, W, H, arrow, circle, clamp, ease_out, ellipse, glow,
                   hexc, lerp, lin, line, rad, rng, rrect, setc, soft_shadow,
                   star4, text)

# ---------------------------------------------------------------- 星空


class Stars:
    def __init__(self, n, seed, x0=-200, y0=-200, x1=W + 200, y1=H + 200,
                 rmin=0.5, rmax=2.2):
        r = rng(seed)
        pal = ["#FFFFFF", "#FFF4E0", "#DCE8FF", "#FFE2C4", "#E8E0FF"]
        self.s = []
        for _ in range(n):
            rr = lerp(rmin, rmax, r.random() ** 2.6)
            self.s.append((r.uniform(x0, x1), r.uniform(y0, y1), rr,
                           r.uniform(0, TAU), r.uniform(0.35, 1.0),
                           r.choice(pal), r.uniform(1.2, 3.2)))

    def draw(self, ctx, t, a=1.0, ox=0.0, oy=0.0, bright_glow=True):
        for x, y, r, ph, b, c, sp in self.s:
            tw = 0.6 + 0.4 * math.sin(t * sp + ph)
            al = a * b * tw
            if al < 0.02:
                continue
            px, py = x + ox, y + oy
            if bright_glow and r > 1.5:
                glow(ctx, px, py, r * 6, c, al * 0.35)
            setc(ctx, c, al)
            circle(ctx, px, py, r)
            ctx.fill()


def nebula(ctx, t, a=1.0, palette=None, seed=3, n=6, area=(0, 0, W, H)):
    r = rng(seed)
    pal = palette or ["#6A4BC4", "#2D5DB8", "#C0508A", "#E0884A", "#3A8FB0"]
    x0, y0, x1, y1 = area
    for i in range(n):
        x = r.uniform(x0, x1) + math.sin(t * 0.07 + i) * 30
        y = r.uniform(y0, y1) + math.cos(t * 0.05 + i) * 20
        rr = r.uniform(260, 620)
        glow(ctx, x, y, rr, pal[i % len(pal)], a * r.uniform(0.10, 0.22))


def space_bg(ctx, t, stars=None, a=1.0, top="#070B1E", mid="#121433", bot="#241A42", neb=1.0, seed=3):
    g = lin(0, 0, 0, H, [(0, top), (0.55, mid), (1, bot)])
    ctx.set_source(g)
    ctx.paint()
    if neb > 0:
        nebula(ctx, t, neb, seed=seed)
    if stars is not None:
        stars.draw(ctx, t, a)


# ---------------------------------------------------------------- 时钟


def clock(ctx, x, y, r, secs, face="#FFF8EE", rim="#3B2B26", ink="#3B2B26",
          accent="#E07B53", a=1.0, show_sec=True, rim_w=None, glow_c=None):
    """secs: 时钟显示的总秒数（决定三根指针位置）。"""
    if a <= 0.01:
        return
    if glow_c:
        glow(ctx, x, y, r * 1.8, glow_c, 0.35 * a)
    soft_shadow(ctx, x, y + r * 1.02, r * 0.9, r * 0.12, 0.18 * a)
    circle(ctx, x, y, r)
    ctx.set_source(rad(x - r * 0.3, y - r * 0.3, r * 0.1, r * 1.2,
                       [(0, "#FFFFFF", a), (1, face, a)]))
    ctx.fill_preserve()
    ctx.set_line_width(rim_w or max(3, r * 0.09))
    setc(ctx, rim, a)
    ctx.stroke()
    for i in range(60):
        ang = i / 60 * TAU
        big = i % 5 == 0
        r0 = r * (0.78 if big else 0.85)
        line(ctx, x + math.cos(ang) * r0, y + math.sin(ang) * r0,
             x + math.cos(ang) * r * 0.9, y + math.sin(ang) * r * 0.9,
             max(1, r * (0.035 if big else 0.012)), ink, a * (0.9 if big else 0.45))
    hr = (secs / 43200.0) % 1 * TAU - math.pi / 2
    mn = (secs / 3600.0) % 1 * TAU - math.pi / 2
    sc = (secs / 60.0) % 1 * TAU - math.pi / 2
    line(ctx, x, y, x + math.cos(hr) * r * 0.48, y + math.sin(hr) * r * 0.48, r * 0.075, ink, a)
    line(ctx, x, y, x + math.cos(mn) * r * 0.7, y + math.sin(mn) * r * 0.7, r * 0.05, ink, a)
    if show_sec:
        line(ctx, x - math.cos(sc) * r * 0.15, y - math.sin(sc) * r * 0.15,
             x + math.cos(sc) * r * 0.8, y + math.sin(sc) * r * 0.8, max(1.5, r * 0.022), accent, a)
    circle(ctx, x, y, r * 0.07)
    setc(ctx, accent, a)
    ctx.fill()


def clock_ring(ctx, x, y, r, t, a=1.0, color="#FFD9A8"):
    """开场用的发光表盘环。"""
    if a <= 0.01:
        return
    glow(ctx, x, y, r * 1.5, color, 0.12 * a)
    ctx.set_line_width(3)
    setc(ctx, color, 0.55 * a)
    circle(ctx, x, y, r)
    ctx.stroke()
    ctx.set_line_width(1.5)
    setc(ctx, color, 0.25 * a)
    circle(ctx, x, y, r * 1.12)
    ctx.stroke()
    for i in range(12):
        ang = i / 12 * TAU + t * 0.05
        line(ctx, x + math.cos(ang) * r * 0.9, y + math.sin(ang) * r * 0.9,
             x + math.cos(ang) * r * 1.0, y + math.sin(ang) * r * 1.0, 4, color, 0.7 * a)
    for i in range(60):
        ang = i / 60 * TAU - t * 0.03
        rr = r * 1.12
        setc(ctx, color, 0.35 * a)
        circle(ctx, x + math.cos(ang) * rr, y + math.sin(ang) * rr, 1.6)
        ctx.fill()
    mn = t * 0.9 - math.pi / 2
    hr = t * 0.075 - math.pi / 2
    line(ctx, x, y, x + math.cos(mn) * r * 0.78, y + math.sin(mn) * r * 0.78, 5, color, 0.6 * a)
    line(ctx, x, y, x + math.cos(hr) * r * 0.5, y + math.sin(hr) * r * 0.5, 7, color, 0.6 * a)


# ---------------------------------------------------------------- 自然物


def sun(ctx, x, y, r, t, a=1.0):
    glow(ctx, x, y, r * 4.0, "#FFD27A", 0.35 * a)
    glow(ctx, x, y, r * 2.0, "#FFE7A8", 0.5 * a)
    for i in range(12):
        ang = i / 12 * TAU + t * 0.15
        l = r * (1.35 + 0.12 * math.sin(t * 3 + i))
        line(ctx, x + math.cos(ang) * r * 1.15, y + math.sin(ang) * r * 1.15,
             x + math.cos(ang) * l, y + math.sin(ang) * l, r * 0.12, "#FFD36E", 0.8 * a)
    circle(ctx, x, y, r)
    ctx.set_source(rad(x - r * 0.3, y - r * 0.3, r * 0.1, r * 1.1,
                       [(0, "#FFFBE6", a), (0.6, "#FFD866", a), (1, "#FFB347", a)]))
    ctx.fill()


def candle(ctx, x, y, h, t, lit=True, a=1.0, flicker=True):
    """(x, y) 为烛台底部中心；h 为蜡烛剩余高度。"""
    soft_shadow(ctx, x, y + 4, 80, 10, 0.25 * a)
    # 烛台
    ellipse(ctx, x, y - 6, 74, 14)
    ctx.set_source(lin(x - 74, 0, x + 74, 0, [(0, "#B98A4C", a), (0.5, "#F2D08A", a), (1, "#A57536", a)]))
    ctx.fill()
    rrect(ctx, x - 22, y - 34, 44, 28, 6)
    ctx.set_source(lin(x - 22, 0, x + 22, 0, [(0, "#B98A4C", a), (0.5, "#F2D08A", a), (1, "#A57536", a)]))
    ctx.fill()
    top = y - 34 - h
    # 蜡烛体
    rrect(ctx, x - 30, top, 60, h + 4, 8)
    ctx.set_source(lin(x - 30, 0, x + 30, 0, [(0, "#EFE2CF", a), (0.4, "#FFF8EE", a), (1, "#E2CDB2", a)]))
    ctx.fill()
    # 熔蜡滴
    ellipse(ctx, x, top + 3, 30, 7)
    setc(ctx, "#FFF3DE", a)
    ctx.fill()
    ctx.move_to(x + 10, top + 4)
    ctx.curve_to(x + 14, top + 22, x + 22, top + 26, x + 18, top + 34)
    ctx.curve_to(x + 14, top + 40, x + 8, top + 28, x + 10, top + 4)
    setc(ctx, "#FFF6E6", a)
    ctx.fill()
    line(ctx, x, top + 2, x, top - 12, 3, "#3A2A22", a)
    if lit:
        f = 1 + (0.08 * math.sin(t * 17) + 0.05 * math.sin(t * 29) if flicker else 0)
        sway = (math.sin(t * 7) * 3) if flicker else 0
        fy = top - 14
        glow(ctx, x, fy - 20, 120, "#FFC766", 0.35 * a)
        ctx.save()
        ctx.translate(x, fy)
        ctx.scale(1, f)
        ctx.move_to(0, 0)
        ctx.curve_to(16, -6, 12 + sway * 0.3, -34, sway, -50)
        ctx.curve_to(-12 + sway * 0.3, -34, -16, -6, 0, 0)
        ctx.set_source(rad(0, -14, 1, 40, [(0, "#FFFFFF", a), (0.35, "#FFE08A", a), (1, "#FF9A3C", a)]))
        ctx.fill()
        ctx.restore()


def leaf(ctx, x, y, s, rot, color="#E99A3B", a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    ctx.move_to(-14, 0)
    ctx.curve_to(-6, -10, 8, -10, 14, 0)
    ctx.curve_to(8, 10, -6, 10, -14, 0)
    setc(ctx, color, a)
    ctx.fill()
    line(ctx, -14, 0, 12, 0, 1.4, "#9A5A22", a * 0.6)
    ctx.restore()


def tree(ctx, x, y, t, a=1.0, seed=7):
    """一棵秋天的小树；(x, y) 为树根。"""
    soft_shadow(ctx, x, y + 3, 140, 14, 0.22 * a)
    ctx.move_to(x - 22, y)
    ctx.curve_to(x - 14, y - 120, x - 18, y - 200, x - 8, y - 260)
    ctx.line_to(x + 10, y - 260)
    ctx.curve_to(x + 16, y - 200, x + 14, y - 120, x + 24, y)
    ctx.close_path()
    ctx.set_source(lin(x - 22, 0, x + 24, 0, [(0, "#7A4A30", a), (1, "#A8704A", a)]))
    ctx.fill()
    line(ctx, x, y - 170, x + 70, y - 240, 12, "#8E5A3A", a)
    line(ctx, x, y - 150, x - 60, y - 220, 10, "#8E5A3A", a)
    r = rng(seed)
    blobs = [(0, -300, 120), (-80, -260, 90), (85, -265, 95), (-30, -360, 85), (50, -350, 80)]
    for i, (bx, by, br) in enumerate(blobs):
        sway = math.sin(t * 1.3 + i) * 3
        circle(ctx, x + bx + sway, y + by, br)
        ctx.set_source(rad(x + bx - br * 0.3, y + by - br * 0.4, br * 0.1, br * 1.1,
                           [(0, "#FFC062", a), (0.6, "#F09A3E", a), (1, "#D9742E", a)]))
        ctx.fill()
    for i in range(18):
        lx = x + r.uniform(-170, 170)
        ly = y + r.uniform(-400, -200)
        leaf(ctx, lx, ly, r.uniform(0.6, 1.0), r.uniform(0, TAU),
             r.choice(["#FFD27A", "#E07B39", "#F4B04C"]), a * 0.9)


def earth(ctx, x, y, r, t, a=1.0, seed=11):
    glow(ctx, x, y, r * 1.5, "#7FC4FF", 0.35 * a)
    circle(ctx, x, y, r)
    ctx.set_source(rad(x - r * 0.35, y - r * 0.35, r * 0.1, r * 1.1,
                       [(0, "#7CD0FF", a), (0.6, "#2F7FD0", a), (1, "#1A4E96", a)]))
    ctx.fill()
    ctx.save()
    circle(ctx, x, y, r)
    ctx.clip()
    rr = rng(seed)
    shift = (t * 0.04 * r) % (r * 4)
    for i in range(9):
        cx = x - r * 2 + rr.uniform(0, r * 4) + shift
        if cx > x + r * 2:
            cx -= r * 4
        cy = y + rr.uniform(-r * 0.8, r * 0.8)
        ellipse(ctx, cx, cy, r * rr.uniform(0.18, 0.4), r * rr.uniform(0.12, 0.3))
        setc(ctx, rr.choice(["#5DBB63", "#7CC46A", "#4FA35A"]), 0.95 * a)
        ctx.fill()
    for i in range(5):
        cx = x + rr.uniform(-r, r) - shift * 0.6
        cy = y + rr.uniform(-r, r)
        ellipse(ctx, cx, cy, r * rr.uniform(0.2, 0.45), r * 0.06)
        setc(ctx, "#FFFFFF", 0.55 * a)
        ctx.fill()
    ctx.set_source(rad(x + r * 0.4, y + r * 0.4, r * 0.2, r * 1.3,
                       [(0, "#000020", 0), (1, "#000020", 0.55 * a)]))
    circle(ctx, x, y, r)
    ctx.fill()
    ctx.restore()


def moon(ctx, x, y, r, a=1.0):
    glow(ctx, x, y, r * 1.8, "#E8EEFF", 0.25 * a)
    circle(ctx, x, y, r)
    ctx.set_source(rad(x - r * 0.3, y - r * 0.3, r * 0.1, r * 1.1,
                       [(0, "#FFFFFF", a), (1, "#B9BFCC", a)]))
    ctx.fill()
    for dx, dy, cr in [(-0.3, -0.2, 0.18), (0.35, 0.1, 0.13), (0.0, 0.45, 0.1), (0.2, -0.45, 0.08)]:
        circle(ctx, x + dx * r, y + dy * r, cr * r)
        setc(ctx, "#9EA5B5", 0.6 * a)
        ctx.fill()


def galaxy(ctx, x, y, r, t, a=1.0, seed=5, tilt=0.45, rot=0.0):
    glow(ctx, x, y, r * 1.3, "#B8A2FF", 0.25 * a)
    glow(ctx, x, y, r * 0.35, "#FFF1D6", 0.9 * a)
    rr = rng(seed)
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(1, tilt)
    for i in range(420):
        arm = i % 2
        u = rr.random()
        ang = u * 3.2 + arm * math.pi + t * 0.05
        dist = u * r
        jx, jy = rr.gauss(0, r * 0.06), rr.gauss(0, r * 0.06)
        px = math.cos(ang) * dist + jx
        py = math.sin(ang) * dist + jy
        setc(ctx, rr.choice(["#FFFFFF", "#D6CCFF", "#FFE4C8", "#AFC8FF"]), a * (1 - u * 0.6) * 0.8)
        circle(ctx, px, py, rr.uniform(0.8, 2.2))
        ctx.fill()
    ctx.restore()


# ---------------------------------------------------------------- 人造物


def satellite(ctx, x, y, s=1.0, rot=0.0, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    for sx in (-1, 1):
        rrect(ctx, sx * 30 - (34 if sx < 0 else 0) + (0 if sx < 0 else 4), -14, 30, 28, 3)
        ctx.set_source(lin(0, -14, 0, 14, [(0, "#4F7FD6", a), (1, "#2A4C9A", a)]))
        ctx.fill()
        for k in range(3):
            xx = sx * (34 + k * 9) - (0 if sx > 0 else 0)
            line(ctx, xx, -14, xx, 14, 1, "#9CC0FF", 0.6 * a)
    rrect(ctx, -18, -16, 36, 32, 5)
    ctx.set_source(lin(0, -16, 0, 16, [(0, "#F2E4C6", a), (1, "#C9A867", a)]))
    ctx.fill()
    line(ctx, 0, -16, 0, -30, 2, "#C0C6D0", a)
    circle(ctx, 0, -32, 4)
    setc(ctx, "#FF8A65", a)
    ctx.fill()
    ctx.restore()


def rocket(ctx, x, y, s=1.0, rot=0.0, t=0.0, a=1.0, flame=True, window_face=True):
    """火箭，默认朝右。"""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    if flame:
        fl = 1 + 0.2 * math.sin(t * 40)
        glow(ctx, -95, 0, 70, "#FFB347", 0.5 * a)
        ctx.move_to(-70, -16)
        ctx.curve_to(-100 * fl, -14, -130 * fl, -4, -150 * fl, 0)
        ctx.curve_to(-130 * fl, 4, -100 * fl, 14, -70, 16)
        ctx.set_source(lin(-150, 0, -70, 0, [(0, "#FF6A3D", 0), (0.5, "#FFB347", a), (1, "#FFF2C0", a)]))
        ctx.fill()
    # 尾翼
    for sy in (-1, 1):
        ctx.move_to(-50, sy * 22)
        ctx.line_to(-80, sy * 50)
        ctx.line_to(-30, sy * 26)
        ctx.close_path()
        setc(ctx, "#E07B53", a)
        ctx.fill()
    ctx.move_to(-70, -26)
    ctx.line_to(30, -26)
    ctx.curve_to(70, -26, 95, -10, 105, 0)
    ctx.curve_to(95, 10, 70, 26, 30, 26)
    ctx.line_to(-70, 26)
    ctx.close_path()
    ctx.set_source(lin(0, -26, 0, 26, [(0, "#FFFFFF", a), (0.6, "#E4E8F0", a), (1, "#B9C0CE", a)]))
    ctx.fill()
    ctx.move_to(60, -19)
    ctx.curve_to(80, -14, 95, -6, 105, 0)
    ctx.curve_to(95, 6, 80, 14, 60, 19)
    ctx.close_path()
    setc(ctx, "#E07B53", a)
    ctx.fill()
    circle(ctx, 10, 0, 15)
    setc(ctx, "#2B3E66", a)
    ctx.fill()
    circle(ctx, 10, 0, 11)
    ctx.set_source(rad(6, -4, 1, 12, [(0, "#9AD7FF", a), (1, "#3D78C2", a)]))
    ctx.fill()
    if window_face:
        rrect(ctx, 2, -6, 16, 12, 3)
        setc(ctx, "#E88E64", a)
        ctx.fill()
        rrect(ctx, 6, -3, 2.5, 5, 1)
        rrect(ctx, 12, -3, 2.5, 5, 1)
        setc(ctx, "#26150F", a)
        ctx.fill()
    ctx.restore()


def cup(ctx, x, y, s=1.0, rot=0.0, a=1.0):
    """马克杯；(x, y) 为杯底中心。"""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    ctx.set_line_width(14)
    setc(ctx, "#4C8FD6", a)
    ctx.arc(52, -55, 26, -math.pi / 2, math.pi / 2)
    ctx.stroke()
    rrect(ctx, -50, -110, 100, 110, 14)
    ctx.set_source(lin(-50, 0, 50, 0, [(0, "#5AA0E8", a), (0.4, "#8CC4FF", a), (1, "#3B78C0", a)]))
    ctx.fill()
    ellipse(ctx, 0, -108, 46, 9)
    setc(ctx, "#2D5E99", a)
    ctx.fill()
    for i, c in enumerate(["#FFFFFF", "#FFD27A"]):
        circle(ctx, -14 + i * 26, -58, 8)
        setc(ctx, c, 0.8 * a)
        ctx.fill()
    ctx.restore()


def pendulum(ctx, x, y, L, ang, a=1.0, bob_r=34):
    """(x, y) 为悬挂点。"""
    bx, by = x + math.sin(ang) * L, y + math.cos(ang) * L
    rrect(ctx, x - 70, y - 18, 140, 18, 6)
    ctx.set_source(lin(0, y - 18, 0, y, [(0, "#8A5A3C", a), (1, "#5E3B26", a)]))
    ctx.fill()
    line(ctx, x, y, bx, by, 6, "#B48A4A", a)
    circle(ctx, x, y, 7)
    setc(ctx, "#5E3B26", a)
    ctx.fill()
    glow(ctx, bx, by, bob_r * 2.4, "#FFD27A", 0.25 * a)
    circle(ctx, bx, by, bob_r)
    ctx.set_source(rad(bx - bob_r * 0.35, by - bob_r * 0.35, 2, bob_r * 1.1,
                       [(0, "#FFF3C4", a), (0.5, "#F2C14E", a), (1, "#B9852A", a)]))
    ctx.fill()
    return bx, by


def quartz(ctx, x, y, t, a=1.0, amp=1.0):
    """石英音叉晶体，(x, y) 为底部中心。"""
    vib = math.sin(t * 90) * 4 * amp
    rrect(ctx, x - 28, y - 70, 56, 70, 8)
    ctx.set_source(lin(x - 28, 0, x + 28, 0, [(0, "#B9D9F2", a), (0.5, "#F2FBFF", a), (1, "#9CC2E0", a)]))
    ctx.fill()
    for sx in (-1, 1):
        ox = sx * vib
        # 振动残影
        for k, al in ((1.0, 0.25), (-1.0, 0.25), (0, 1.0)):
            dx = ox * k if k else ox
            rrect(ctx, x + sx * 34 - 16 + dx, y - 290, 32, 240, 10)
            ctx.set_source(lin(x + sx * 34 - 16, 0, x + sx * 34 + 16, 0,
                               [(0, "#C9E6FA", a * al), (0.5, "#FFFFFF", a * al), (1, "#A8CDEA", a * al)]))
            ctx.fill()
    rrect(ctx, x - 50, y - 80, 100, 24, 8)
    setc(ctx, "#D6ECFA", a)
    ctx.fill()


def atom(ctx, x, y, r, t, a=1.0, speed=1.0, wave_amp=1.0):
    glow(ctx, x, y, r * 1.6, "#7FD8FF", 0.25 * a)
    for i in range(3):
        rot = i * math.pi / 3 + 0.2
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(rot)
        ctx.scale(1, 0.32)
        ctx.new_path()
        ctx.arc(0, 0, r, 0, TAU)
        ctx.restore()
        ctx.set_line_width(3)
        setc(ctx, "#9BE4FF", 0.5 * a)
        ctx.stroke()
        ang = t * speed * (2.2 + i * 0.4) + i * 2
        ex, ey = math.cos(ang) * r, math.sin(ang) * r * 0.32
        px = x + ex * math.cos(rot) - ey * math.sin(rot)
        py = y + ex * math.sin(rot) + ey * math.cos(rot)
        glow(ctx, px, py, 22, "#AEEBFF", 0.8 * a)
        circle(ctx, px, py, 7)
        setc(ctx, "#FFFFFF", a)
        ctx.fill()
    pulse = 1 + 0.08 * math.sin(t * 40) * wave_amp
    glow(ctx, x, y, r * 0.45 * pulse, "#FFD27A", 0.7 * a)
    for i, (dx, dy, c) in enumerate([(-8, -6, "#FF8A65"), (8, -4, "#FFD27A"), (0, 8, "#FF8A65"),
                                     (-6, 8, "#FFD27A"), (7, 9, "#FF8A65"), (0, -10, "#FFD27A")]):
        circle(ctx, x + dx * pulse, y + dy * pulse, 10)
        ctx.set_source(rad(x + dx - 3, y + dy - 3, 1, 11, [(0, "#FFFFFF", a), (1, c, a)]))
        ctx.fill()


def black_hole(ctx, x, y, r, t, a=1.0):
    """带吸积盘与光子环的黑洞（风格化）。"""
    glow(ctx, x, y, r * 5, "#FF9A3C", 0.18 * a)
    # 吸积盘后半部分（被引力透镜弯到上方的光环）
    ctx.save()
    ctx.translate(x, y)
    for k in range(26):
        u = k / 25
        rr = r * (1.25 + u * 0.75)
        ctx.set_line_width(r * 0.05)
        c = "#FFF1C8" if u < 0.3 else ("#FFC46B" if u < 0.65 else "#E0642E")
        setc(ctx, c, a * (0.55 - u * 0.4))
        ctx.save()
        ctx.scale(1, 0.92)
        ctx.arc(0, -r * 0.05, rr * 0.82, math.pi * 1.0, math.pi * 2.0)
        ctx.restore()
        ctx.stroke()
    # 盘面（后半）
    for k in range(30):
        u = k / 29
        rr = r * (1.4 + u * 1.9)
        ctx.set_line_width(r * 0.07)
        c = "#FFF6D8" if u < 0.25 else ("#FFC46B" if u < 0.6 else "#D2552A")
        setc(ctx, c, a * (0.75 - u * 0.6))
        ctx.save()
        ctx.scale(1, 0.22)
        ctx.arc(0, 0, rr, math.pi, TAU)
        ctx.restore()
        ctx.stroke()
    # 事件视界
    circle(ctx, 0, 0, r)
    setc(ctx, "#000000", a)
    ctx.fill()
    ctx.set_line_width(r * 0.06)
    setc(ctx, "#FFE6A8", 0.9 * a)
    circle(ctx, 0, 0, r * 1.04)
    ctx.stroke()
    glow(ctx, 0, 0, r * 1.25, "#FFD38A", 0.0)
    # 盘面（前半）
    for k in range(30):
        u = k / 29
        rr = r * (1.4 + u * 1.9)
        ctx.set_line_width(r * 0.07)
        c = "#FFF6D8" if u < 0.25 else ("#FFC46B" if u < 0.6 else "#D2552A")
        setc(ctx, c, a * (0.9 - u * 0.7))
        ctx.save()
        ctx.scale(1, 0.22)
        ctx.arc(0, 0, rr, 0, math.pi)
        ctx.restore()
        ctx.stroke()
    # 旋转的亮斑
    rr = rng(9)
    for i in range(40):
        rad_ = r * rr.uniform(1.5, 3.2)
        ang = rr.uniform(0, TAU) + t * (2.2 / (rad_ / r))
        px, py = math.cos(ang) * rad_, math.sin(ang) * rad_ * 0.22
        if math.sin(ang) < 0 and abs(px) < r * 1.05 and py > -r:
            continue
        setc(ctx, "#FFFFFF", a * 0.7)
        ellipse(ctx, px, py, 6, 2)
        ctx.fill()
    ctx.restore()


def big_bang(ctx, x, y, p, a=1.0, seed=2):
    """大爆炸闪光：p 0..1。"""
    if p <= 0:
        return
    e = ease_out(p)
    glow(ctx, x, y, 40 + 600 * e, "#FFFFFF", a * (1 - p) * 0.9)
    glow(ctx, x, y, 30 + 300 * e, "#FFE7A8", a * (1 - p * 0.6))
    r = rng(seed)
    for i in range(70):
        ang = r.uniform(0, TAU)
        sp = r.uniform(0.3, 1.0)
        d = e * 520 * sp
        l = 30 * (1 - p) + 6
        px, py = x + math.cos(ang) * d, y + math.sin(ang) * d
        line(ctx, px, py, px - math.cos(ang) * l, py - math.sin(ang) * l, 2.5,
             r.choice(["#FFFFFF", "#FFD27A", "#9AD7FF", "#FF9BC4"]), a * (1 - p) ** 0.6)


def dino(ctx, x, y, s=1.0, a=1.0, color="#5BAF6A"):
    """可爱的小恐龙剪影，(x, y) 为脚底中心。"""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    setc(ctx, color, a)
    ctx.move_to(-70, -40)
    ctx.curve_to(-100, -50, -120, -30, -130, -20)
    ctx.curve_to(-100, -30, -80, -20, -60, -18)
    ctx.line_to(-40, -10)
    ctx.line_to(-40, 0)
    ctx.line_to(-25, 0)
    ctx.line_to(-22, -12)
    ctx.line_to(10, -12)
    ctx.line_to(14, 0)
    ctx.line_to(29, 0)
    ctx.line_to(30, -22)
    ctx.curve_to(45, -40, 45, -70, 40, -90)
    ctx.curve_to(40, -110, 50, -120, 70, -120)
    ctx.curve_to(95, -120, 100, -105, 98, -98)
    ctx.curve_to(96, -90, 80, -90, 64, -88)
    ctx.curve_to(60, -70, 50, -55, 30, -50)
    ctx.curve_to(0, -60, -40, -60, -70, -40)
    ctx.close_path()
    ctx.fill()
    circle(ctx, 78, -110, 4)
    setc(ctx, "#1C2A1C", a)
    ctx.fill()
    for i in range(4):
        ctx.move_to(-40 + i * 20, -56 + i * 1)
        ctx.line_to(-30 + i * 20, -70)
        ctx.line_to(-20 + i * 20, -56)
        setc(ctx, "#3E8E50", a)
        ctx.fill()
    ctx.restore()


def human(ctx, x, y, s=1.0, a=1.0, color="#FFE3C4"):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    circle(ctx, 0, -78, 13)
    setc(ctx, color, a)
    ctx.fill()
    for (x0, y0, x1, y1) in [(0, -62, 0, -28), (0, -55, -18, -38), (0, -55, 18, -38),
                             (0, -28, -12, 0), (0, -28, 12, 0)]:
        line(ctx, x0, y0, x1, y1, 8, color, a)
    ctx.restore()


def hourglass(ctx, x, y, s, p, a=1.0):
    """沙漏；p 为沙子流下的比例。"""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for sy in (-1, 1):
        rrect(ctx, -60, sy * 100 - 8, 120, 16, 6)
        setc(ctx, "#8A5A3C", a)
        ctx.fill()
    ctx.move_to(-48, -92)
    ctx.line_to(48, -92)
    ctx.curve_to(48, -40, 8, -20, 8, 0)
    ctx.curve_to(8, 20, 48, 40, 48, 92)
    ctx.line_to(-48, 92)
    ctx.curve_to(-48, 40, -8, 20, -8, 0)
    ctx.curve_to(-8, -20, -48, -40, -48, -92)
    ctx.close_path()
    setc(ctx, "#DFF1FF", 0.35 * a)
    ctx.fill_preserve()
    ctx.set_line_width(3)
    setc(ctx, "#FFFFFF", 0.7 * a)
    ctx.stroke()
    top = (1 - p)
    if top > 0.01:
        h = 70 * top
        ctx.move_to(-40 * top - 6, -10 - h)
        ctx.line_to(40 * top + 6, -10 - h)
        ctx.line_to(6, -6)
        ctx.line_to(-6, -6)
        ctx.close_path()
        setc(ctx, "#F2C14E", a)
        ctx.fill()
        line(ctx, 0, -4, 0, 88, 2.5, "#F2C14E", a)
    h = 70 * p
    ctx.move_to(-46, 90)
    ctx.line_to(46, 90)
    ctx.line_to(0, 90 - h * 1.1)
    ctx.close_path()
    setc(ctx, "#F2C14E", a)
    ctx.fill()
    ctx.restore()
