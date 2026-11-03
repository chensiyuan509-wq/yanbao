"""场景共用：Claude 角色、光照（给角色染上场景光色）、倒影、分镜切换、常用小件。"""
import math
from contextlib import contextmanager

from mascot import Actor

from ..core import FILTER, H, W, clamp, ease_out, glow, lin, pop, prog, rad, rrect, setc, smooth, text


def claude(x, y, s=0.6, expr="neutral", seed=1.0, hat=None, **kw):
    """主角 Claude（没有人声，不对口型）。"""
    return Actor(x, y, s, expr, seed=seed, hat=hat, **kw)


@contextmanager
def lit(tint=None, amt=0.0, bright=1.0, desat=0.0):
    """临时设置调色滤镜：让角色（或某一层）融进场景光线。"""
    old = dict(FILTER)
    FILTER.update(tint=tint, tint_amt=amt, bright=bright, desat=desat)
    try:
        yield
    finally:
        FILTER.clear()
        FILTER.update(old)


def reflect(ctx, fn, ground_y, a=0.25, fade=160):
    """在 ground_y 处画倒影：fn(ctx) 画原物（世界坐标），这里上下翻转并渐隐。"""
    if a <= 0.003:
        return
    ctx.push_group()
    ctx.save()
    ctx.translate(0, 2 * ground_y)
    ctx.scale(1, -1)
    fn(ctx)
    ctx.restore()
    ctx.pop_group_to_source()
    m = lin(0, ground_y, 0, ground_y + fade, [(0, "#000000", a), (1, "#000000", 0)])
    ctx.mask(m)


def shot(t, cuts):
    """分镜：cuts = [开始时间, ...]（升序），返回 (镜头序号, 镜头内时间)。"""
    i = 0
    for k, c in enumerate(cuts):
        if t >= c:
            i = k
    return i, t - cuts[i]


def fade_io(t, t0, t1, fin=0.35, fout=0.35):
    if t <= t0 or t >= t1:
        return 0.0
    return min(smooth((t - t0) / fin) if fin > 0 else 1.0, smooth((t1 - t) / fout) if fout > 0 else 1.0)


def appear(t, t0, dur=0.45):
    return pop(t, t0, dur)


def label(ctx, s, x, y, size=30, color="#F4E6C8", a=1.0, weight="serif_sb", sub=None, sub_size=None,
          sub_color="#CDBA92", shadow=True, align="c"):
    """画面里的说明文字（宋体，带柔和投影）。"""
    if a <= 0.003:
        return
    if shadow:
        text(ctx, s, x + 2, y + 2.5, size, "#000000", 0.55 * a, weight, align)
    text(ctx, s, x, y, size, color, a, weight, align)
    if sub:
        ss = sub_size or size * 0.62
        if shadow:
            text(ctx, sub, x + 2, y + size * 0.95 + 2, ss, "#000000", 0.5 * a, "serif_r", align)
        text(ctx, sub, x, y + size * 0.95, ss, sub_color, a, "serif_r", align)


def counter_text(v, fmt="{:,.0f}"):
    return fmt.format(v)
