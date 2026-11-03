"""序章：第一视角睁眼，看见漂浮的人类文字；镜头升起，头顶是"人类知识星图"；
Claude 回头望向过去，沿着光河倒流（年份从 2026 年滚回 330 万年前）；片名《星火》。"""
import math

from ..core import (TAU, H, W, Cam, circle, clamp, ease_in, ease_io, ease_out, ease_out5, fbm, glow, kf, lerp,
                    lin, prog, rad, rng, setc, smooth, text, view)
from .. import film, starmap
from .common import claude, fade_io, lit, reflect

DUR = 30.0
CHAPTER = None
GRAIN = 0.07

VO = [
    (1.4, "我是 {Claude}。"),
    (3.6, "我从人类写下的亿万文字里，学会了说话、推理、写代码。"),
    (9.2, "可这些知识，最初是从哪里来的？"),
    (12.9, "人类是怎么一步步，学会{理解这个世界}的？"),
    (17.3, "这一次，我想倒着走回去——"),
    (20.6, "回到{第一束火光}亮起的地方。"),
]

SUPERS = []

# ---------------------------------------------------------------- 镜头 A：漂浮的文字（第一视角）

_GLYPHS = (["光", "火", "数", "星", "书", "天", "地", "水", "人", "理", "问", "为什么", "知", "学", "算", "道",
            "π", "∞", "E=mc²", "a²+b²=c²", "F=ma", "∫", "Σ", "√2", "0", "1", "λ", "Ω", "DNA", "H₂O", "def",
            "{ }", "if", "return", "print()", "Hello", "Why?", "Nullius in verba", "Eureka", "cogito",
            "𒀭", "𒁹", "𒌋", "𓂀", "𓇳", "𓆣", "𑁦𑁧", "αβγ", "ΔΦ", "1+1=2", "60", "365", "3.14159", "∇×E",
            "e^iπ+1=0", "日有食之", "勾股", "九章", "万物皆数", "天行有常", "格物致知"])
_FONT_OF = {"𒀭": "cune", "𒁹": "cune", "𒌋": "cune", "𓂀": "hiero", "𓇳": "hiero", "𓆣": "hiero", "𑁦𑁧": "brahmi"}


def _glyph_font(g):
    if g in _FONT_OF:
        return _FONT_OF[g]
    if any(c in g for c in "∇√∫Σ∞∮∂"):
        return "eq"
    if all(ord(c) < 0x3000 for c in g):
        return "latin"
    return "serif_m"


def _glyph_field(ctx, t, a=1.0, absorb=0.0, hands=None):
    R = rng(31)
    f = 900.0
    for i in range(170):
        gx, gy = R.uniform(-1.6, 1.6), R.uniform(-1.0, 1.0)
        z0 = R.random()
        sp = R.uniform(0.05, 0.09)
        g = _GLYPHS[i % len(_GLYPHS)]
        z = 0.25 + ((z0 - t * sp) % 1.0) * 3.2
        sx, sy = W / 2 + gx * f / z, H / 2 + gy * f / z * 0.9
        size = 30 / z * 2.2
        al = a * smooth((3.4 - z) / 1.2) * smooth((z - 0.25) / 0.35)
        if absorb > 0 and hands:
            hx, hy = hands[i % 2]
            k = absorb * smooth(clamp(1.4 - z))
            sx, sy = lerp(sx, hx, k * 0.8), lerp(sy, hy, k * 0.8)
            al *= 1 - k * 0.6
        if al <= 0.01 or not (-200 < sx < W + 200 and -100 < sy < H + 100):
            continue
        col = "#FFE2B0" if i % 3 else "#BFD6FF"
        if size > 26:
            glow(ctx, sx, sy, size * 1.3, col, 0.12 * al)
        text(ctx, g, sx, sy, size, col, al, _glyph_font(g))


def _shot_a(ctx, t):
    ctx.set_source(rad(W / 2, H * 0.45, 0, H * 1.1, [(0, "#16203A"), (0.55, "#0A0F1F"), (1, "#020309")]))
    ctx.paint()
    film.star_field(ctx, t, 120, 5, a=0.35)
    rise = ease_out(prog(t, 2.9, 4.6))
    sway = math.sin(t * 1.3) * 10
    tl = (lerp(560, 760, rise) + sway, lerp(1260, 780, rise) + math.sin(t * 1.1) * 6)
    tr = (lerp(1360, 1160, rise) - sway * 0.8, lerp(1260, 790, rise) + math.sin(t * 1.25 + 1) * 6)
    absorb = smooth(prog(t, 4.6, 6.5))
    _glyph_field(ctx, t, 1.0, absorb, (tl, tr))
    if rise > 0:
        for p, glow_k in ((tl, 1.0), (tr, 1.0)):
            glow(ctx, p[0], p[1] - 40, 220, "#FFD9A0", 0.35 * absorb * glow_k)
        film.pov_arm(ctx, (300, 1300), tl, 150, 1.0, 0.8)
        film.pov_arm(ctx, (1620, 1300), tr, 150, 1.0, 0.8)
        for p in (tl, tr):
            film.embers(ctx, t, p[0], p[1] - 50, 10, int(p[0]), spread=90, height=200, color="#FFE2A8",
                        a=absorb * 0.8, size=3)
    film.vignette(ctx, 0.6)
    # 睁眼（中间轻眨一下）
    ok = smooth(prog(t, 0.8, 1.9))
    if 2.0 < t < 2.5:
        ok *= 1 - 0.8 * math.sin((t - 2.0) / 0.5 * math.pi)
    ok = ok * 0.9 + 0.1 * smooth(prog(t, 2.5, 3.2)) if t > 2.5 else ok * 0.9
    film.eyelids(ctx, ok if t < 3.2 else 1.0)


# ---------------------------------------------------------------- 镜头 B / C：星图下的 Claude

P = (claude(1250, 880, 0.62, "wonder", seed=2.0)
     .look(8.5, -0.5, -0.9)
     .expr(11.0, "awe").fx(11.0, ())
     .expr(12.8, "hmm").look(13.0, -0.3, -0.7)
     .expr(15.4, "curious").look(15.6, -0.8, -0.5)
     .face(17.6, True, 0.4).expr(17.6, "resolute").look(17.7, 0.9, -0.2)
     .walk_to(18.6, 20.6, 1000, 880, stride=0.9))

SKY = Cam([(8.5, (1980, 3050, 0.78)), (14.6, (2000, 2700, 0.72), ease_io), (17.0, (1990, 2650, 0.74))],
          drift=10, seed=4.0)


def _ground(ctx, t, oy):
    y = 880 + oy
    ctx.set_source(lin(0, y - 4, 0, y + 400, [(0, "#1B2340"), (0.3, "#0C1022"), (1, "#05070F")]))
    ctx.rectangle(-100, y, W + 200, 600)
    ctx.fill()
    ctx.set_source(lin(0, y - 40, 0, y + 40, [(0, "#FFD58A", 0), (0.5, "#FFD58A", 0.18), (1, "#FFD58A", 0)]))
    ctx.rectangle(-100, y - 40, W + 200, 80)
    ctx.fill()


def _sky(ctx, t, cam, a=1.0, label_a=1.0):
    ctx.set_source(lin(0, 0, 0, H, [(0, "#05060F"), (0.6, "#0D1230"), (1, "#1A1A3A")]))
    ctx.paint()
    with view(ctx, cam, 0.55):
        starmap.draw_sky(ctx, t, a)
    with view(ctx, cam, 1.0):
        starmap.draw_map(ctx, t, a, lit=1.0, label_a=label_a, zoom=cam[2])


def _shot_bc(ctx, t):
    crane = ease_io(prog(t, 8.6, 14.6)) - ease_io(prog(t, 15.9, 17.7))
    cam = SKY.at(t)
    cam = (cam[0], cam[1] - crane * 260, cam[2], cam[3])
    _sky(ctx, t, cam, 1.0, smooth(prog(t, 9.5, 11.5)))
    oy = crane * 760
    ctx.save()
    ctx.translate(0, oy)
    push = 1 + 0.06 * prog(t, 8.5, 20.6)
    ctx.translate(1250, 880)
    ctx.scale(push, push)
    ctx.translate(-1250, -880)
    _ground(ctx, t, 0)
    with lit("#9FB8FF", 0.35, 0.82):
        reflect(ctx, lambda c: P.draw(c, t), 880, 0.22, 140)
        glow(ctx, P.state(t)["x"], 760, 260, "#FFD58A", 0.12)
        P.draw(ctx, t)
    ctx.restore()
    film.vignette(ctx, 0.55)


# ---------------------------------------------------------------- 镜头 D：沿光河倒流


def _rewind_u(t):
    return 1.0 - ease_io(prog(t, 20.4, 25.2)) * 0.995


def _shot_d(ctx, t):
    u = _rewind_u(t)
    du = _rewind_u(t + 1 / 30) - u
    x, y = starmap.point(u)
    # 镜头跟随光河（取前后平均，让运动顺滑）
    xs = [starmap.point(clamp(u + d))[0] for d in (-0.03, -0.015, 0, 0.015, 0.03)]
    ys = [starmap.point(clamp(u + d))[1] for d in (-0.03, -0.015, 0, 0.015, 0.03)]
    cx, cy = sum(xs) / 5, sum(ys) / 5
    speed = abs(du) * 30
    z = 0.95 - 0.15 * smooth(speed / 0.3)
    rot = math.sin(t * 0.7) * 0.04
    cam = (cx, cy, z, rot)
    ctx.set_source(lin(0, 0, 0, H, [(0, "#04050C"), (1, "#110E26")]))
    ctx.paint()
    with view(ctx, cam, 0.5):
        starmap.draw_sky(ctx, t, 1.0)
    # 动态模糊：沿运动方向叠几层
    vx = (starmap.point(clamp(u + du * 3))[0] - x) * z
    vy = (starmap.point(clamp(u + du * 3))[1] - y) * z
    for k in range(4, 0, -1):
        ctx.save()
        ctx.translate(vx * k * 0.6, vy * k * 0.6)
        with view(ctx, cam, 1.0):
            starmap.draw_map(ctx, t, 0.22, lit=u, label_a=0.0, zoom=z)
        ctx.restore()
    with view(ctx, cam, 1.0):
        starmap.draw_map(ctx, t, 1.0, lit=u, label_a=1 - smooth(speed / 0.12), zoom=z)
    film.vignette(ctx, 0.6)
    # 年份计数器
    a = fade_io(t, 20.5, 25.6, 0.5, 0.4)
    yr = starmap.year_at(u)
    s = starmap.year_text(yr) if t < 25.15 else "330 万年前"
    blur = smooth(speed / 0.25)
    for k, al in ((-1, 0.25), (1, 0.25), (0, 1.0)):
        if k and blur < 0.05:
            continue
        film.tracked(ctx, s, W / 2, 790 + k * 26 * blur, 66, "#FFE8C0", a * al * (1 if k == 0 else blur),
                     "serif_sb", 0.06)
    film.tracked(ctx, "时 间 倒 流", W / 2, 715, 26, "#C9B98F", a * 0.8, "serif_l", 0.4)


# ---------------------------------------------------------------- 镜头 E：片名


def _shot_e(ctx, t):
    u = t - 25.2
    ctx.set_source(rad(W / 2, 760, 0, 1100, [(0, "#2A140A"), (0.5, "#120A08"), (1, "#030202")]))
    ctx.paint()
    film.embers(ctx, t, W / 2, 900, 40, 9, spread=900, height=900, color="#FFA14A", a=0.9, size=3.4,
                speed=0.22)
    glow(ctx, W / 2, 470, 700, "#FF8A3A", 0.18 * smooth(u / 1.5))
    s = "星火"
    p = smooth(prog(u, 0.2, 2.0))
    foc = ease_out(prog(u, 0.2, 2.2))
    for dx, al in ((0, 1.0), (-10, 0.3), (10, 0.3)):
        off = dx * (1 - foc)
        if dx and foc > 0.98:
            continue
        film.tracked(ctx, s, W / 2 + off, 450, 230, "#FFF1DC", p * al * (1 if dx == 0 else 1 - foc), "serif_k",
                     0.25 + 0.08 * ease_io(prog(u, 0, 4.8)))
    q = smooth(prog(u, 1.6, 2.6))
    lw = 520 * ease_io(prog(u, 1.4, 2.6))
    ctx.rectangle(W / 2 - lw / 2, 600, lw, 2)
    setc(ctx, "#D9B26A", 0.9 * q)
    ctx.fill()
    film.tracked(ctx, "人 类 科 学 简 史", W / 2, 650, 40, "#E9D9BE", q, "serif_m", 0.25)
    film.tracked(ctx, "从第一块石器，到人工智能", W / 2, 712, 30, "#C9AE7E", smooth(prog(u, 2.4, 3.4)), "serif_l",
                 0.15)
    film.vignette(ctx, 0.5)


# ---------------------------------------------------------------- 主绘制


def draw(ctx, t):
    if t < 8.5:
        _shot_a(ctx, t)
    elif t < 20.4:
        _shot_bc(ctx, t)
    elif t < 25.2:
        _shot_d(ctx, t)
    else:
        _shot_e(ctx, t)
    film.fade_black(ctx, 1 - smooth(t / 0.8))
    if 25.0 < t < 25.5:      # 倒流结束的闪白
        ctx.set_source_rgba(1, 0.95, 0.88, math.sin((t - 25.0) / 0.5 * math.pi) * 0.85)
        ctx.paint()


def sfx():
    return [
        (0.0, "ambience_space", {"dur": 9.5, "gain": 0.5}),
        (0.85, "hush", {"dur": 1.6, "gain": 0.35}),
        (2.9, "swell", {"dur": 1.8, "gain": 0.3}),
        (4.6, "stream", {"dur": 3.0, "gain": 0.25}),
        (4.7, "shimmer", {"dur": 2.0, "gain": 0.22}),
        (8.5, "impact_soft", {"gain": 0.35}),
        (8.5, "ambience_space", {"dur": 12.5, "gain": 0.55}),
        (8.7, "whoosh", {"dur": 5.5, "gain": 0.22}),
        (11.0, "sparkle", {"dur": 1.2, "gain": 0.2}),
        (17.6, "whoosh_short", {"gain": 0.3}),
        (18.6, "hop", {"gain": 0.12}),
        (20.3, "rewind", {"dur": 4.9, "gain": 0.45}),
        (20.3, "riser", {"dur": 4.9, "gain": 0.4}),
        (25.15, "boom", {"gain": 0.75}),
        (25.2, "ambience_fire", {"dur": 5.5, "gain": 0.3}),
        (25.4, "ignite", {"gain": 0.35}),
    ]
