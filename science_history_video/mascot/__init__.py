"""可复用的橙色小方块角色库（按 assets/image.jpg 的造型矢量重绘，只依赖 pycairo）。

    from mascot import Actor, draw_mascot, EXPRESSIONS, ACTIONS

- draw_mascot(ctx, x, y, s, expr=..., ...)  直接画一帧（参数见 body.draw_mascot）
- Actor(...)                                用时间轴写动作（见 actor.py）
- EXPRESSIONS / ACTIONS / FX / HATS / GLASSES / PROPS / FRONT_POSES  可用的表情、动作、特效、配件清单
- set_color_hook(fn)                        接入项目的调色滤镜
- python -m mascot.export                   导出表情 / 动作总览图与透明 PNG / SVG 精灵
"""
from .actor import ACTIONS, KEEP, Actor
from .body import FRONT_POSES, blink_open, draw_mascot, hand_point
from .const import BW, BH, LEG_H, TOP
from .expressions import BROWS, EXPRESSIONS, ORIGINAL
from .fx import FX
from .gear import GLASSES, HATS, PROPS, draw_prop
from .gfx import set_color_hook

__all__ = ["Actor", "ACTIONS", "KEEP", "draw_mascot", "hand_point", "blink_open", "FRONT_POSES",
           "EXPRESSIONS", "ORIGINAL", "BROWS", "FX", "HATS", "GLASSES", "PROPS", "draw_prop",
           "set_color_hook", "BW", "BH", "LEG_H", "TOP"]
