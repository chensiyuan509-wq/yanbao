"""宇宙样张（参考，不是模板）：真实的哈勃极深场做主视觉 + 指向细节的标注 + 右栏信息面板；
然后切到蓝图原理图：光从太阳出发，8 分 20 秒到地球；Claude 在下方看着。"""
import math

from ..core import H, W, ease_io, glow, lerp, prog, smooth
from .. import film
from ..layout import GRID, headline, info_panel, pointer, reveal, source_note, stat
from ..diagram import orbit
from ..exhibit import blueprint_bg
from .common import arch, claude, lit, sequence

DUR = 22.4
CHAPTER = dict(num="第 一 章", title="看不见的远方", era="宇宙", key="尺度", at=0.4, dur=4.0, x=620)
GRAIN = 0.07
VO = [
    (4.6, "哈勃极深场里，几乎每一个光点都是{一个星系}。"),
    (8.4, "其中最远的光，已经走了{130 亿年}。"),
    (12.0, "近一点：太阳到地球约 1.5 亿公里，"),
    (15.4, "光也要走 {8 分 20 秒}——我们看到的永远是过去的太阳。"),
]
SUPERS = []
T_B = 11.6


def _a(ctx, t):
    to = arch(ctx, t, "hudf", 0.0, T_B + 0.6, (0.5, 0.5, 1.0), (0.46, 0.56, 1.5), "哈勃极深场",
              "NASA / ESA · 2004 · 公有领域", cap=(4.6, None))
    gx, gy = to(0.43, 0.6)
    pointer(ctx, t, 6.4, (gx, gy), (gx - 230, gy - 150), "一个星系", "像银河系一样，有上千亿颗恒星")
    info_panel(ctx, t, 4.8, "哈勃极深场 · 2004", [("曝光", "约 100 万秒"), ("星系", "约 1 万个"), ("最远的光", "约 130 亿年")],
               conclusion="看得越远，看到的越早")


VIEWER = claude(330, 950, 0.5, "curious", seed=7.0).look(T_B + 0.4, 0.6, -0.6).expr(T_B + 4.0, "awe")


def _b(ctx, t):
    u = t - T_B
    blueprint_bg(ctx, W, H, t)
    sx, sy = 520, 540
    glow(ctx, sx, sy, 160, "#FFC46B", 0.7)
    film.sun(ctx, sx, sy, 54, 1.0, "#FFF2C8", "#FF9A3A", 180)
    ang = -0.35 + u * 0.03
    ex, ey = orbit(ctx, sx, sy, 520, 330, 0.0, smooth(prog(u, 0.0, 0.6)), body=ang, body_r=12,
                   body_color="#7FB6FF", trail=0.5)
    # 光脉冲：从太阳射向地球
    f = ease_io(prog(u, 1.0, 6.0))
    if 0 < f < 1:
        px, py = lerp(sx, ex, f), lerp(sy, ey, f)
        glow(ctx, px, py, 30, "#FFE2B0", 0.9)
    headline(ctx, "光从太阳到地球", 700, GRID["title_y"], smooth(prog(u, 0.2, 0.7)))
    info_panel(ctx, t, T_B + 0.6, "日地距离", [("距离", "约 1.5 亿公里"), ("光速", "约 30 万公里/秒")],
               theme="blueprint", y=200)
    secs = 500 * ease_io(prog(u, 1.0, 6.0))
    stat(ctx, t, T_B + 1.0, 1500, 640, f"{int(secs // 60)} 分 {int(secs % 60):02d} 秒", "光走完这段路",
         "你看到的太阳，是 8 分钟前的太阳")
    source_note(ctx, "示意图，距离未按比例", x=GRID["margin"], y=950)
    with lit("#9AB6FF", 0.25, 0.85):
        VIEWER.draw(ctx, t)
    film.vignette(ctx, 0.45)


SHOTS = [(0.0, _a), (T_B, _b)]
TRANS = {1: ("luma", 1.0)}


def draw(ctx, t):
    sequence(ctx, t, SHOTS, TRANS)


def sfx():
    return [(0.0, "ambience_space", {"dur": DUR, "gain": 0.45}), (4.8, "shimmer", {"dur": 1.6, "gain": 0.18}),
            (6.4, "blip", {"gain": 0.15}), (T_B, "hush", {"dur": 1.6, "gain": 0.25}),
            (T_B + 1.0, "rise", {"dur": 5.0, "gain": 0.2}), (T_B + 6.0, "ding", {"gain": 0.2})]
