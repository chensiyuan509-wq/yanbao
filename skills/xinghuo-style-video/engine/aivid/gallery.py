"""人类文明博物馆：Claude 在展厅里走过一幅幅真实的历史画作 / 照片，镜头跟拍横移，最后推进到其中一幅画里。

    g = Gallery([("athens", "拉斐尔《雅典学院》"), ("byrne_title", "拜恩版《几何原本》"), ...], actor, t0, t1, push=0)
    g.draw(ctx, t)

镜头在 [t0, t1] 里从第一幅移到 push 指定的那一幅，最后 1.4 秒推进到画框里（画心铺满画面）。
"""
import math

from .archive import framed, size
from .core import H, W, clamp, ease_in, ease_io, glow, lerp, lin, rad, rrect, setc, smooth, text
from . import film

WALL_Y0, FLOOR_Y = 96, 850
FRAME_Y = 460
GAP = 760


class Gallery:
    def __init__(self, items, actor, t0, t1, push=0, push_dur=1.6, frame_h=440, start=0, lead=380):
        self.items, self.actor, self.t0, self.t1 = items, actor, t0, t1
        self.lead = lead
        self.push, self.push_dur, self.frame_h, self.start = push, push_dur, frame_h, start

    def frame_x(self, i):
        return 960 + i * GAP

    def cam(self, t):
        """返回 (镜头中心 x, 缩放)。"""
        tp = self.t1 - self.push_dur
        u = ease_io(clamp((t - self.t0) / max(tp - self.t0, 1e-3)))
        x = lerp(self.frame_x(self.start) - self.lead, self.frame_x(self.push), u)
        k = ease_in(clamp((t - tp) / self.push_dur))
        key = self.items[self.push][0]
        iw, ih = size(key)
        fh = self.frame_h
        fw = fh * iw / ih
        zfull = max(1080 / fh, 1920 / fw) * 1.02
        z = 1 + (zfull - 1) * k
        return x, z, k

    def draw(self, ctx, t):
        cx, z, pk = self.cam(t)
        ctx.save()
        ctx.translate(W / 2, lerp(FRAME_Y, H / 2, pk))     # 推进时画框中心移到画面正中，便于无缝切进画里
        ctx.scale(z, z)
        ctx.translate(-cx, -FRAME_Y)
        # 墙
        ctx.set_source(lin(0, WALL_Y0, 0, FLOOR_Y, [(0, "#1A1512"), (0.6, "#2A221C"), (1, "#16120F")]))
        ctx.rectangle(cx - 3000, -200, 6000, FLOOR_Y + 200)
        ctx.fill()
        film.paint_texture(ctx, "stone", cx - 3000, -200, 6000, FLOOR_Y + 200, 0.12, scale=0.5)
        # 地面（带倒影感的深色地板）
        ctx.set_source(lin(0, FLOOR_Y, 0, H + 200, [(0, "#2A211A"), (1, "#0C0907")]))
        ctx.rectangle(cx - 3000, FLOOR_Y, 6000, 800)
        ctx.fill()
        ctx.rectangle(cx - 3000, FLOOR_Y - 3, 6000, 6)
        setc(ctx, "#5A4634", 0.6)
        ctx.fill()
        for i, it in enumerate(self.items):
            x = self.frame_x(i)
            if abs(x - cx) > 2200 / max(z, 1):
                continue
            key, title = it[0], it[1]
            sub = it[2] if len(it) > 2 else ""
            # 顶灯光锥
            ctx.move_to(x - 40, WALL_Y0 - 40)
            ctx.line_to(x + 40, WALL_Y0 - 40)
            ctx.line_to(x + 330, FLOOR_Y)
            ctx.line_to(x - 330, FLOOR_Y)
            ctx.close_path()
            ctx.set_source(lin(0, WALL_Y0, 0, FLOOR_Y, [(0, "#FFE2B0", 0.22), (1, "#FFE2B0", 0.0)]))
            ctx.fill()
            glow(ctx, x, FRAME_Y, 420, "#FFD9A0", 0.16)
            framed(ctx, key, x, FRAME_Y, self.frame_h, 1.0)
            # 地板上的倒影
            ctx.save()
            ctx.translate(0, 2 * FLOOR_Y + 30)
            ctx.scale(1, -1)
            ctx.push_group()
            framed(ctx, key, x, FRAME_Y, self.frame_h, 1.0, shadow=0)
            ctx.pop_group_to_source()
            ctx.paint_with_alpha(0.12)
            ctx.restore()
            # 说明牌
            text(ctx, title, x, FRAME_Y + self.frame_h / 2 + 64, 28, "#F2E6CE", 0.95 * (1 - pk), "serif_sb")
            if sub:
                text(ctx, sub, x, FRAME_Y + self.frame_h / 2 + 102, 20, "#BFAE8E", 0.9 * (1 - pk), "serif_r")
        if self.actor is not None:
            self.actor.draw(ctx, t)
        ctx.restore()
        film.vignette(ctx, 0.6)
