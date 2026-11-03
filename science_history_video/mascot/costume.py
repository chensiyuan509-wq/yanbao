"""服装与配色：让 Claude"扮演"历史人物。

- 服装（costume）由若干图层组成：under 层画在身体之上、脸之下（长袍、兽皮、外套、领结……），
  over 层画在脸之上（胡子、假发、头巾、帽子……）。坐标为身体局部坐标（与帽子相同）。
- 配色（palette）只改身体 / 手臂 / 腿的颜色，表情不变；同框多人时用来区分角色。

    draw_mascot(ctx, x, y, s, costume="euclid", palette="clay")
    Actor(..., costume="newton").costume(t, "einstein")
"""
import math

from .const import BW, BH, TOP
from .gfx import circle, ellipse, fill, lin, poly, rad, rrect, setc, stroke

BOT = TOP + BH          # 身体底边 y（= -50）

# ---------------------------------------------------------------- 配色

PALETTES = {
    "orange": dict(t="#EE9669", m="#DE7C56", b="#C6664A", rim="#FBE9BB", leg="#A85B40", arm="#EE8C62"),
    "amber": dict(t="#F2A85E", m="#E08E46", b="#C2733A", rim="#FCEBC0", leg="#A86A34", arm="#F09E54"),
    "rose": dict(t="#EE8A7E", m="#DA6E66", b="#BE5650", rim="#FBE2D4", leg="#A04A44", arm="#EA8076"),
    "clay": dict(t="#D9A07C", m="#C4865F", b="#A86C4A", rim="#F4E2CC", leg="#8E5A3C", arm="#D49470"),
    "ochre": dict(t="#E0B060", m="#C9964A", b="#AA7A36", rim="#F8EBC4", leg="#8E6630", arm="#DAA856"),
    "coral": dict(t="#F49C80", m="#E58266", b="#C9684E", rim="#FDE6D6", leg="#AA5A44", arm="#F09276"),
    "sienna": dict(t="#C98462", m="#B06A4A", b="#925438", rim="#EFD8C2", leg="#7A4430", arm="#C47C5A"),
}


# ---------------------------------------------------------------- 身体上的图层（under）


def _toga(ctx, t, a, color="#F4EEDF", shade="#D8CDB4"):
    """希腊式长袍：从左肩斜披到右下。"""
    poly(ctx, [(-152, TOP + 118), (-152, TOP + 84), (152, BOT - 40), (152, BOT + 2), (60, BOT + 2)])
    ctx.set_source(lin(-150, TOP, 150, BOT, [(0, color, a), (1, shade, a)]))
    ctx.fill()
    for k in range(3):
        ctx.move_to(-150, TOP + 92 + k * 9)
        ctx.curve_to(-60, TOP + 120 + k * 9, 40, BOT - 50 + k * 8, 150, BOT - 30 + k * 10)
        stroke(ctx, shade, 3, 0.7 * a)
    circle(ctx, -130, TOP + 100, 9)
    fill(ctx, "#D9A83A", a)


def _sash(ctx, t, a, color="#2E7A5A"):
    poly(ctx, [(-152, TOP + 116), (-152, TOP + 92), (152, BOT - 28), (152, BOT + 2), (110, BOT + 2)])
    setc(ctx, color, a)
    ctx.fill()


def _pelt(ctx, t, a):
    """兽皮：腰间一圈带斑点的皮毛，下沿参差。"""
    pts = [(-152, BOT - 70), (152, BOT - 70)]
    x = 152
    while x > -152:
        pts.append((x, BOT + 6 + (10 if int(x / 24) % 2 else 0)))
        x -= 24
    pts.append((-152, BOT + 2))
    poly(ctx, pts)
    ctx.set_source(lin(0, BOT - 70, 0, BOT, [(0, "#B98A4E", a), (1, "#8A6232", a)]))
    ctx.fill()
    for (sx, sy) in ((-110, -95), (-60, -82), (-10, -100), (40, -86), (90, -98), (125, -80), (-130, -72)):
        ellipse(ctx, sx, sy, 9, 6)
        fill(ctx, "#4A3218", 0.75 * a)
    poly(ctx, [(-40, BOT - 70), (-10, TOP + 40), (20, TOP + 46), (0, BOT - 70)])
    setc(ctx, "#A87A42", a)
    ctx.fill()


def _coat(ctx, t, a, color="#2A2622", shirt="#F2EEE6", tie="bowtie", tie_color="#2A2622"):
    """外套 + 衬衫 + 领结（18—20 世纪）。"""
    poly(ctx, [(-152, BOT - 80), (-46, BOT - 80), (-14, BOT + 2), (-152, BOT + 2)])
    poly(ctx, [(152, BOT - 80), (46, BOT - 80), (14, BOT + 2), (152, BOT + 2)])
    setc(ctx, color, a)
    ctx.fill()
    poly(ctx, [(-46, BOT - 80), (46, BOT - 80), (14, BOT + 2), (-14, BOT + 2)])
    setc(ctx, shirt, a)
    ctx.fill()
    for sx in (-1, 1):
        poly(ctx, [(sx * 46, BOT - 80), (sx * 70, BOT - 80), (sx * 28, BOT - 26)])
        setc(ctx, "#4A443E" if color != "#F4F4F0" else "#D8D8D2", a)
        ctx.fill()
    if tie == "bowtie":
        poly(ctx, [(-26, BOT - 84), (0, BOT - 74), (-26, BOT - 64)])
        poly(ctx, [(26, BOT - 84), (0, BOT - 74), (26, BOT - 64)])
        setc(ctx, tie_color, a)
        ctx.fill()
        circle(ctx, 0, BOT - 74, 6)
        fill(ctx, tie_color, a)
    elif tie == "cravat":
        ellipse(ctx, 0, BOT - 70, 22, 16)
        fill(ctx, "#FFFFFF", a)


def _labcoat(ctx, t, a):
    _coat(ctx, t, a, color="#F4F4F0", shirt="#6A8AB0", tie=None)


def _collar_gold(ctx, t, a):
    """古埃及宽项圈：底部几道金 / 蓝弧。"""
    for k, col in enumerate(("#D9A83A", "#2E5A9A", "#D9A83A", "#3A8A6A")):
        ctx.new_path()
        ctx.arc(0, BOT - 150, 120 + k * 14, math.pi * 0.18, math.pi * 0.82)
        stroke(ctx, col, 12, a)


def _dress(ctx, t, a, color="#2A2430"):
    poly(ctx, [(-152, BOT - 60), (152, BOT - 60), (152, BOT + 2), (-152, BOT + 2)])
    setc(ctx, color, a)
    ctx.fill()
    ctx.new_path()
    ctx.arc(0, BOT - 64, 40, 0, math.pi)
    stroke(ctx, "#F2EEE6", 6, a)


# ---------------------------------------------------------------- 脸上 / 头上的图层（over）


def _beard(ctx, t, a, color="#C9C4BC", shade="#9A948C", long=1.0):
    """胡子：盖住嘴，下沿是几缕波浪。"""
    y0 = TOP + 104
    L = 70 * long
    ctx.move_to(-70, y0)
    ctx.curve_to(-70, y0 + L * 0.6, -40, y0 + L, -20, y0 + L * 0.9)
    ctx.curve_to(-10, y0 + L * 1.15, 10, y0 + L * 1.15, 20, y0 + L * 0.9)
    ctx.curve_to(40, y0 + L, 70, y0 + L * 0.6, 70, y0)
    ctx.curve_to(40, y0 + 18, -40, y0 + 18, -70, y0)
    ctx.close_path()
    ctx.set_source(lin(0, y0, 0, y0 + L, [(0, color, a), (1, shade, a)]))
    ctx.fill()
    for k in (-36, -12, 12, 36):
        ctx.move_to(k, y0 + 16)
        ctx.curve_to(k + 4, y0 + L * 0.4, k - 4, y0 + L * 0.6, k, y0 + L * 0.85)
        stroke(ctx, shade, 2.5, 0.6 * a)


def _mustache(ctx, t, a, color="#D8D4CC"):
    y = TOP + 108
    for sd in (-1, 1):
        ctx.move_to(0, y)
        ctx.curve_to(sd * 20, y - 14, sd * 52, y - 8, sd * 60, y + 10)
        ctx.curve_to(sd * 40, y + 4, sd * 18, y + 10, 0, y + 6)
        ctx.close_path()
        setc(ctx, color, a)
        ctx.fill()


def _wig(ctx, t, a, color="#E8E2D8", shade="#B8B0A2"):
    """17—18 世纪的长卷假发：头顶一层，两侧垂下几串卷。"""
    rrect(ctx, -BW / 2 - 6, TOP - 26, BW + 12, 44, 22)
    ctx.set_source(lin(0, TOP - 26, 0, TOP + 18, [(0, color, a), (1, shade, a)]))
    ctx.fill()
    for sd in (-1, 1):
        for k in range(5):
            cx = sd * (BW / 2 + 4 - (k % 2) * 10)
            cy = TOP + 10 + k * 26
            circle(ctx, cx, cy, 18)
            ctx.set_source(rad(cx - 4, cy - 4, 2, 20, [(0, color, a), (1, shade, a)]))
            ctx.fill()


def _einstein_hair(ctx, t, a, color="#ECEAE6", shade="#B9B4AC"):
    R = [(-130, -20, 30), (-90, -34, 34), (-40, -40, 36), (10, -42, 36), (60, -36, 34), (110, -24, 30), (150, 0, 26),
         (-150, 4, 24), (-160, 34, 20), (164, 30, 20)]
    for (x, y, r) in R:
        wob = math.sin(t * 2 + x) * 2
        circle(ctx, x, TOP + y + 14 + wob, r)
        ctx.set_source(rad(x - 6, TOP + y + 6, 2, r, [(0, color, a), (1, shade, a)]))
        ctx.fill()


def _turban(ctx, t, a, color="#F2EEE4", shade="#CFC6B4"):
    ellipse(ctx, 0, TOP - 14, 140, 46)
    ctx.set_source(lin(0, TOP - 60, 0, TOP + 30, [(0, color, a), (1, shade, a)]))
    ctx.fill()
    for k in range(3):
        ctx.move_to(-130, TOP - 4 - k * 16)
        ctx.curve_to(-40, TOP - 30 - k * 16, 40, TOP + 4 - k * 16, 130, TOP - 22 - k * 14)
        stroke(ctx, shade, 3, 0.7 * a)
    ellipse(ctx, 0, TOP - 52, 76, 26)
    fill(ctx, color, a)


def _futou(ctx, t, a):
    """宋代幞头：黑色方帽 + 两侧长翅。"""
    rrect(ctx, -70, TOP - 64, 140, 70, 16)
    setc(ctx, "#1E1A18", a)
    ctx.fill()
    for sd in (-1, 1):
        rrect(ctx, sd * 66 - (130 if sd < 0 else 0), TOP - 40, 130, 10, 5)
        setc(ctx, "#1E1A18", a)
        ctx.fill()


def _nemes(ctx, t, a):
    """古埃及条纹头巾。"""
    poly(ctx, [(-120, TOP - 30), (120, TOP - 30), (168, TOP + 120), (130, TOP + 120), (100, TOP + 20),
               (-100, TOP + 20), (-130, TOP + 120), (-168, TOP + 120)])
    setc(ctx, "#D9B44A", a)
    ctx.fill()
    for k in range(7):
        y = TOP - 22 + k * 20
        ctx.move_to(-170, y)
        ctx.line_to(170, y)
    ctx.save()
    poly(ctx, [(-120, TOP - 30), (120, TOP - 30), (168, TOP + 120), (130, TOP + 120), (100, TOP + 20),
               (-100, TOP + 20), (-130, TOP + 120), (-168, TOP + 120)])
    ctx.clip()
    ctx.new_path()
    for k in range(8):
        ctx.rectangle(-180, TOP - 26 + k * 20, 360, 8)
    setc(ctx, "#2E4E9A", a)
    ctx.fill()
    ctx.restore()


def _beret(ctx, t, a, color="#2A2230"):
    ellipse(ctx, 20, TOP - 6, 120, 30)
    setc(ctx, color, a)
    ctx.fill()
    circle(ctx, 30, TOP - 34, 8)
    fill(ctx, color, a)


def _tophat(ctx, t, a):
    rrect(ctx, -84, TOP - 140, 168, 136, 8)
    setc(ctx, "#1A1716", a)
    ctx.fill()
    rrect(ctx, -84, TOP - 40, 168, 18, 2)
    setc(ctx, "#5A2A22", a)
    ctx.fill()
    ellipse(ctx, 0, TOP - 4, 130, 14)
    fill(ctx, "#1A1716", a)


def _bun(ctx, t, a, color="#4A4440"):
    rrect(ctx, -BW / 2 + 4, TOP - 14, BW - 8, 34, 16)
    setc(ctx, color, a)
    ctx.fill()
    circle(ctx, 0, TOP - 30, 26)
    fill(ctx, color, a)


def _wild_hair(ctx, t, a, color="#4A3420"):
    for k in range(13):
        x = -140 + k * 23
        h = 30 + (k * 37 % 23)
        poly(ctx, [(x - 16, TOP + 10), (x + 4 + math.sin(t + k) * 3, TOP - h), (x + 18, TOP + 10)])
        setc(ctx, color, a)
        ctx.fill()


def _skullcap(ctx, t, a, color="#3A2A4A"):
    ctx.save()
    ctx.rectangle(-200, TOP - 80, 400, 84)
    ctx.clip()
    ellipse(ctx, 0, TOP + 4, 118, 30)
    setc(ctx, color, a)
    ctx.fill()
    ctx.restore()


def _headband(ctx, t, a, color="#A8322A"):
    rrect(ctx, -BW / 2 - 4, TOP + 6, BW + 8, 16, 6)
    setc(ctx, color, a)
    ctx.fill()


UNDER = {"toga": _toga, "sash": _sash, "pelt": _pelt, "coat": _coat, "labcoat": _labcoat,
         "collar_gold": _collar_gold, "dress": _dress,
         "coat_brown": lambda c, t, a: _coat(c, t, a, color="#5A3A26", tie="cravat"),
         "robe_blue": lambda c, t, a: _sash(c, t, a, "#2E4E8A"), "robe_red": lambda c, t, a: _sash(c, t, a, "#8A2A22")}
OVER = {"beard": _beard, "beard_brown": lambda c, t, a: _beard(c, t, a, "#6A4A30", "#4A3220"),
        "beard_black": lambda c, t, a: _beard(c, t, a, "#2A2420", "#121010", 1.3),
        "beard_short": lambda c, t, a: _beard(c, t, a, "#6A4A30", "#4A3220", 0.6),
        "mustache": _mustache, "wig": _wig, "einstein_hair": _einstein_hair, "turban": _turban, "futou": _futou,
        "nemes": _nemes, "beret": _beret, "tophat": _tophat, "bun": _bun, "wild_hair": _wild_hair,
        "skullcap": _skullcap, "headband": _headband,
        "laurel": lambda c, t, a: __import__("mascot.gear", fromlist=["hat_laurel"]).hat_laurel(c, t, a)}

# 角色预设（服装图层组合）
COSTUMES = {
    "caveman": ["pelt", "wild_hair"],
    "sumerian": ["robe_red", "headband"],
    "egyptian": ["collar_gold", "nemes"],
    "greek": ["toga", "laurel"],
    "euclid": ["toga", "beard", "laurel"],
    "archimedes": ["toga", "beard"],
    "eratosthenes": ["toga", "beard_brown", "laurel"],
    "chinese_scholar": ["robe_blue", "beard_black", "futou"],
    "arab_scholar": ["sash", "beard_black", "turban"],
    "renaissance": ["robe_red", "beard_brown", "beret"],
    "galileo": ["robe_red", "beard_brown", "beret"],
    "newton": ["coat_brown", "wig"],
    "watt": ["coat_brown", "skullcap"],
    "victorian": ["coat", "tophat"],
    "faraday": ["coat", "beard_short"],
    "einstein": ["coat", "mustache", "einstein_hair"],
    "curie": ["dress", "bun"],
    "lovelace": ["dress", "bun"],
    "engineer": ["labcoat"],
}


def draw_layers(ctx, costume, t, a=1.0, which="under"):
    if not costume:
        return
    layers = COSTUMES.get(costume, [costume]) if isinstance(costume, str) else costume
    table = UNDER if which == "under" else OVER
    for name in layers:
        fn = table.get(name)
        if fn:
            fn(ctx, t, a)
