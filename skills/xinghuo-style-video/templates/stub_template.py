"""__LABEL__：__TITLE__（待设计）

这是脚手架生成的**最小可运行占位**，不是模板：只保证整片能渲染、能检查。
按本片的内容重新设计这一段——画面、镜头数、构图、转场、音效都从故事出发，
风格标准见 references/，写法可以参考 examples/xinghuo/，但不要照搬那里的镜头和素材。
"""
from ..core import H, W, lin, prog, smooth, text
from .. import film

DUR = __DUR__
CHAPTER = __CHAPTER__
GRAIN = 0.07

VO = [
    (DUR * 0.25, "（这一段的第一句字幕）"),
]
SUPERS = []


def draw(ctx, t):
    ctx.set_source(lin(0, 0, 0, H, [(0, "#14110F"), (1, "#060504")]))
    ctx.paint()
    k = smooth(prog(t, 0.3, 1.2)) * (1 - smooth(prog(t, DUR - 1.0, DUR)))
    text(ctx, "（待设计）__TITLE__", W / 2, H / 2 + 60, 40, "#8C7A60", k, "serif_sb")
    film.vignette(ctx, 0.5)


def sfx():
    return [(0.0, "ambience_room", {"dur": DUR, "gain": 0.3})]
