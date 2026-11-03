"""编程样张（参考，不是模板）：代码就是这个题材的"实物"——代码面板逐字打出、逐行高亮；
算法过程用蓝图节点演示；终端给出实测结果；Claude 坐在一旁敲键盘。"""
from ..core import H, W, ease_io, lerp, prog, rad, smooth
from .. import film
from ..layout import GRID, headline, info_panel, reveal, stat, tag
from ..codeview import code_panel, terminal
from ..diagram import BYRNE, node
from ..exhibit import blueprint_bg
from ..proofs import paper
from .common import claude, lit, sequence

DUR = 22.6
CHAPTER = dict(num="第 二 章", title="二分查找", era="代码", key="算法", at=0.4, dur=4.0, x=620)
GRAIN = 0.07
VO = [
    (4.6, "在排好序的 100 万个数里找一个数，"),
    (7.6, "每次只看中间那个，就能{排除一半}。"),
    (11.4, "16 个数，最多看 4 次；"),
    (14.6, "100 万个数，最多也只要 {20 次}。"),
]
SUPERS = []
CODE = '''def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2      # 只看中间
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1          # 丢掉左半边
        else:
            hi = mid - 1          # 丢掉右半边
    return -1'''
T_B = 11.2
CODER = (claude(1640, 960, 0.5, "focused", seed=9.0).hold(0.0, ("laptop",), "front").type(4.4, 9.0)
         .expr(9.4, "happy"))


def _a(ctx, t):
    ctx.set_source(rad(700, 520, 0, 1300, [(0, "#1A1820"), (1, "#050407")]))
    ctx.paint()
    film.paint_texture(ctx, "stone", 0, 0, W, H, 0.06, scale=0.5)
    code_panel(ctx, t, 4.4, CODE, x=140, y=170, w=980, title="search.py", cps=70,
               highlight=[(4, 6.6, 8.6), (8, 8.8, 10.2)])
    info_panel(ctx, t, 4.6, "二分查找", ["每次比较中间的数", "目标更大 → 丢掉左半边", "目标更小 → 丢掉右半边"],
               conclusion="每一步，范围减半", y=190)
    with lit("#FFE2B0", 0.15, 0.9):
        CODER.draw(ctx, t)
    film.vignette(ctx, 0.45)


VALS = [3, 8, 12, 17, 21, 26, 30, 34, 41, 47, 52, 58, 63, 70, 77, 85]
STEPS = [(0, 15, 7), (8, 15, 11), (8, 10, 9), (9, 9, 9)]      # 找 47：lo, hi, mid


def _b(ctx, t):
    """亮场：算法画在纸面上，拜恩配色——蓝 = 范围下界，黄 = 正在比较的中间数，红 = 范围上界。"""
    u = t - T_B
    paper(ctx)
    headline(ctx, "在 16 个数里找 47", 640, GRID["title_y"], smooth(prog(u, 0.1, 0.6)), color=BYRNE["ink"])
    si = min(len(STEPS) - 1, max(0, int((u - 1.0) / 1.6)))
    lo, hi, mid = STEPS[si]
    x0, cw, y = 160, 60, 520
    for i, v in enumerate(VALS):
        k = reveal(t, T_B + 0.2, i, 0.03)
        live = lo <= i <= hi
        fc = None
        if u > 1.0:
            fc = BYRNE["yellow"] if i == mid else (BYRNE["blue"] if i == lo and lo != mid else
                                                   (BYRNE["red"] if i == hi and hi != mid else None))
        node(ctx, x0 + i * cw + cw / 2, y, cw - 8, 70, str(v), None, 1.0 if live else 0.25, k, "paper",
             title_size=24, fill_color=fc, fill_a=0.85)
    if u > 1.0:
        tag(ctx, f"第 {si + 1} 次", x0 + mid * cw + cw / 2, y + 90, 1.0, align="c", theme="paper")
    info_panel(ctx, t, T_B + 0.8, "最多比较几次", [("16 个数", "4 次"), ("1000 个", "10 次"), ("100 万个", "20 次")],
               conclusion="规模翻倍，只多一次", theme="paper", y=190)
    terminal(ctx, t, T_B + 5.4, [("cmd", "python search.py"), ("ok", "找到 47：下标 9，比较 4 次")], x=1180, y=650, w=640)
    film.vignette(ctx, 0.35)


SHOTS = [(0.0, _a), (T_B, _b)]
TRANS = {1: ("zoomblur", 0.7, {"x": 620, "y": 330})}


def draw(ctx, t):
    sequence(ctx, t, SHOTS, TRANS)


def sfx():
    return [(0.0, "ambience_data", {"dur": DUR, "gain": 0.35}), (4.4, "typing", {"dur": 3.2, "gain": 0.2}),
            (6.6, "blip", {"gain": 0.15}), (8.8, "blip", {"gain": 0.15, "pitch": 1.2}),
            (T_B + 1.0, "click", {"gain": 0.2}), (T_B + 2.6, "click", {"gain": 0.2, "pitch": 1.1}),
            (T_B + 4.2, "click", {"gain": 0.2, "pitch": 1.2}), (T_B + 5.8, "success", {"gain": 0.18})]
