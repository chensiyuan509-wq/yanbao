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


def role(x, y, s=0.6, costume=None, expr="neutral", seed=1.0, palette=None, **kw):
    """Claude 扮演历史人物（换上对应的服装），palette 用来区分同框的不同角色。"""
    return Actor(x, y, s, expr, seed=seed, costume=costume, palette=palette, **kw)


def arch(ctx, t, key, t0, t1, c0, c1, title=None, sub="", grade=None, cap=(0.6, None), rect=None, a=1.0,
         vig=0.5):
    """档案镜头：历史图像缓缓推拉（Ken Burns）+ 暗角 + 左下角出处字幕。返回图像坐标→画面坐标的映射。"""
    from ..archive import caption, kb
    from .. import film
    rect = rect or (0, 0, W, H)
    to = kb(ctx, key, t, t0, t1, c0, c1, rect=rect, a=a, grade=grade)
    if vig:
        film.vignette(ctx, vig)
    if title:
        c0_, c1_ = cap
        c1_ = c1_ if c1_ is not None else (t1 - t0) - 0.4
        ca = smooth(clamp((t - t0 - c0_) / 0.6)) * smooth(clamp((t0 + c1_ - t) / 0.5))
        caption(ctx, title, sub, ca * a)
    return to


def sequence(ctx, t, shots, trans=None):
    """章内分镜 + 镜头之间的转场。

    shots = [(开始秒, fn), ...]（fn(ctx, t) 画这个镜头）
    trans = {镜头序号 j: (种类, 时长, 参数)} —— 第 j 个镜头开始时用什么转场（以交界为中心）
    """
    import cairo
    from ..transitions import composite
    trans = trans or {}
    for j in range(1, len(shots)):
        if j in trans:
            kind, dur = trans[j][0], trans[j][1]
            params = trans[j][2] if len(trans[j]) > 2 else {}
            b = shots[j][0]
            if b - dur / 2 <= t < b + dur / 2:
                tgt = ctx.get_target()
                pw, ph = tgt.get_width(), tgt.get_height()
                m = ctx.get_matrix()
                surfs = []
                for fn in (shots[j - 1][1], shots[j][1]):
                    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, pw, ph)
                    c = cairo.Context(s)
                    c.set_source_rgb(0, 0, 0)
                    c.paint()
                    c.set_matrix(m)
                    fn(c, t)
                    s.flush()
                    surfs.append(s)
                composite(ctx, kind, (t - (b - dur / 2)) / dur, surfs[0], surfs[1], pw, ph, params)
                return
    idx = 0
    for k, (t0, _) in enumerate(shots):
        if t >= t0:
            idx = k
    shots[idx][1](ctx, t)
