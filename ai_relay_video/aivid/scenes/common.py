"""场景共用：主持人（Claude 形象）、背景、占位画面、常用小动画。"""
import math

from mascot import Actor

from ..core import (H, W, clamp, ease_back, ease_out, glow, lin, pop, prog, rad, rrect, setc, smooth,
                    text)
from ..narration import plain


def host(x, y, s=0.6, expr="smile", seed=1.0, hat="explorer", **kw):
    """主持人（Claude 形象）。视频没有人声，不对口型。"""
    a = Actor(x, y, s, expr, seed=seed, hat=hat, **kw)
    return a


def talk_lines(actor, vo, idx=None, smile=0.3, tail=0.0):
    """原用于按旁白对口型；现在视频没有人声，角色不再张嘴说话，保留接口以免改动各场景。"""
    return actor


def appear(t, t0, dur=0.45):
    """弹出缩放 0→1（带回弹）。"""
    return pop(t, t0, dur)


def fade_io(t, t0, t1, fin=0.35, fout=0.35):
    if t <= t0 or t >= t1:
        return 0.0
    return min(smooth((t - t0) / fin) if fin > 0 else 1.0, smooth((t1 - t) / fout) if fout > 0 else 1.0)


def vignette(ctx, a=0.35, color="#000000"):
    g = rad(W / 2, H / 2, H * 0.45, H * 1.1, [(0, color, 0), (1, color, a)])
    ctx.set_source(g)
    ctx.paint()


def placeholder(ctx, t, name, vo):
    ctx.set_source(lin(0, 0, 0, H, [(0, "#2A2440"), (1, "#3D2A3A")]))
    ctx.paint()
    text(ctx, name.split(".")[-1], W / 2, 200, 60, "#FFFFFF", 0.8, "black")
    cur = [s for (t0, s, *_r) in vo if t0 <= t]
    if cur:
        text(ctx, plain(cur[-1])[:30], W / 2, 540, 40, "#FFE3C8", 0.9, "bold")


def mini_icon(ctx, kind, x, y, s, color="#FF9F68"):
    """小图标（不用 emoji，全部手绘）：plane / cal / bag / laptop / case / house / check / doc / bolt。"""
    from ..core import check_mark, circle, fill, poly, rrect, setc
    from ..icons import ic_plane
    u = s / 100
    if kind == "plane":
        ic_plane(ctx, x, y, s, 1.0, 0.0, color, -0.5)
    elif kind == "cal":
        rrect(ctx, x - 38 * u, y - 34 * u, 76 * u, 72 * u, 10 * u)
        fill(ctx, "#FFFFFF")
        rrect(ctx, x - 38 * u, y - 34 * u, 76 * u, 72 * u, 10 * u)
        ctx.set_line_width(5 * u)
        setc(ctx, color)
        ctx.stroke()
        ctx.rectangle(x - 38 * u, y - 34 * u, 76 * u, 18 * u)
        fill(ctx, color)
        for i in range(3):
            for j in range(2):
                rrect(ctx, x - 26 * u + i * 20 * u, y - 4 * u + j * 18 * u, 12 * u, 10 * u, 2 * u)
                fill(ctx, color, 0.6)
    elif kind == "bag":
        rrect(ctx, x - 34 * u, y - 18 * u, 68 * u, 58 * u, 10 * u)
        fill(ctx, color)
        ctx.new_sub_path()
        ctx.arc(x, y - 18 * u, 18 * u, 3.3, 6.12)
        ctx.set_line_width(7 * u)
        setc(ctx, color)
        ctx.stroke()
    elif kind == "laptop":
        rrect(ctx, x - 36 * u, y - 30 * u, 72 * u, 46 * u, 6 * u)
        fill(ctx, "#3A3646")
        rrect(ctx, x - 30 * u, y - 24 * u, 60 * u, 34 * u, 3 * u)
        fill(ctx, "#7CC6FF")
        rrect(ctx, x - 46 * u, y + 16 * u, 92 * u, 10 * u, 4 * u)
        fill(ctx, "#C9C5D3")
    elif kind == "case":
        rrect(ctx, x - 40 * u, y - 22 * u, 80 * u, 56 * u, 10 * u)
        fill(ctx, "#8C5A33")
        rrect(ctx, x - 16 * u, y - 36 * u, 32 * u, 18 * u, 6 * u)
        ctx.set_line_width(6 * u)
        setc(ctx, "#8C5A33")
        ctx.stroke()
        ctx.rectangle(x - 40 * u, y - 2 * u, 80 * u, 6 * u)
        fill(ctx, "#5E3A1E")
    elif kind == "house":
        poly(ctx, [(x - 44 * u, y - 4 * u), (x, y - 42 * u), (x + 44 * u, y - 4 * u)])
        fill(ctx, color)
        rrect(ctx, x - 32 * u, y - 6 * u, 64 * u, 44 * u, 4 * u)
        fill(ctx, "#FFF1DB")
        rrect(ctx, x - 9 * u, y + 12 * u, 18 * u, 26 * u, 3 * u)
        fill(ctx, "#8C5A33")
    elif kind == "check":
        circle(ctx, x, y, 40 * u)
        fill(ctx, "#3CCB7F")
        check_mark(ctx, x, y, 46 * u, "#FFFFFF", 1.0)
    elif kind == "bolt":
        poly(ctx, [(x + 8 * u, y - 44 * u), (x - 26 * u, y + 6 * u), (x - 2 * u, y + 6 * u), (x - 10 * u, y + 44 * u),
                   (x + 26 * u, y - 8 * u), (x + 2 * u, y - 8 * u)])
        fill(ctx, color)
