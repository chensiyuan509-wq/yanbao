"""导出角色素材：总览图、透明 PNG / SVG 精灵、机器可读清单。

    python -m mascot.export                 # → mascot/sheets/*.png, mascot/catalog.json
    python -m mascot.export --sprites       # 另外导出每个表情的透明 PNG + SVG → mascot/sprites/
"""
import argparse
import json
import math
import os

import cairo

from . import ACTIONS, EXPRESSIONS, FRONT_POSES, FX, GLASSES, HATS, ORIGINAL, PROPS, Actor, draw_mascot
from .gfx import lin, rrect, setc, text

HERE = os.path.dirname(os.path.abspath(__file__))


def _bg(ctx, w, h):
    ctx.set_source(lin(0, 0, 0, h, [(0, "#F4EFD6"), (0.55, "#FBE3C8"), (1, "#E9BFA6")]))
    ctx.paint()


def _cell_label(ctx, x, y, name, desc):
    text(ctx, name, x, y, 26, "#3A2A26", 1.0, True)
    if desc:
        text(ctx, desc, x, y + 32, 20, "#7A5A50", 1.0, False)


def expression_sheet(path, cols=7, cw=300, ch=330):
    names = ORIGINAL + [n for n in EXPRESSIONS if n not in ORIGINAL]
    rows = math.ceil(len(names) / cols)
    W, H = cols * cw, rows * ch + 90
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    _bg(ctx, W, H)
    text(ctx, f"表情 {len(names)} 种（前 11 种对应素材图，其余为扩展）", W / 2, 44, 34, "#3A2A26", 1, True)
    for i, n in enumerate(names):
        cx, cy = (i % cols) * cw + cw / 2, (i // cols) * ch + 90
        if n in ORIGINAL:
            rrect(ctx, cx - cw / 2 + 8, cy - 4, cw - 16, ch - 12, 18)
            setc(ctx, "#FFFFFF", 0.35)
            ctx.fill()
        draw_mascot(ctx, cx, cy + 228, 0.72, expr=n, t=1.3 + i * 0.37, since=5.0, seed=i * 0.7,
                    blink=False)
        _cell_label(ctx, cx, cy + 262, n, EXPRESSIONS[n].get("desc", ""))
    surf.write_to_png(path)
    return path


def _demo_actors():
    """每个演示：(标题, Actor, 取样时间)。"""
    X, Y = 0, 0
    d = []
    d.append(("walk_to 走", Actor(X - 60, Y, 0.62, "smile").walk_to(0, 2, X + 60, Y), 0.83))
    d.append(("run_to 跑", Actor(X - 80, Y, 0.62, "excited").run_to(0, 1.2, X + 80, Y), 0.55))
    d.append(("hop 小跳", Actor(X, Y, 0.62, "happy").hop(0.0, 70), 0.24))
    d.append(("jump 大跳", Actor(X, Y, 0.62, "excited").jump(0.0), 0.36))
    d.append(("wave 挥手", Actor(X, Y, 0.62, "happy").wave(0, 3), 1.2))
    d.append(("cheer 欢呼", Actor(X, Y, 0.62, "grin").cheer(0, 3), 1.25))
    d.append(("clap 拍手", Actor(X, Y, 0.62, "grin").clap(0, 3), 1.15))
    d.append(("type 打字", Actor(X, Y, 0.62, "focused").type(0, 3), 1.0))
    d.append(("point 指向", Actor(X, Y, 0.62, "curious").point(0, "r", 0.4, 90).look(0, 1, -0.3), 1.0))
    d.append(("think 思考", Actor(X, Y, 0.62, "think").fx(0, ("ellipsis",)), 1.0))
    d.append(("shrug 摊手", Actor(X, Y, 0.62, "confused").shrug(0.0, 3).fx(0, ()), 1.0))
    d.append(("cover 扶额", Actor(X, Y, 0.62, "sad").front(0, "cover").fx(0, ("gloom",)), 1.0))
    d.append(("cross 抱臂", Actor(X, Y, 0.62, "smug").front(0, "cross"), 1.0))
    d.append(("hold 举牌", Actor(X, Y, 0.62, "happy").hold(0, ("sign", {"label": "AI"}), "r", -0.35)
              .arm(0, "r", 0.9).ext(0, "r", 10), 1.0))
    d.append(("carry 举过头顶", Actor(X, Y, 0.62, "determined").hold(0, ("chip", {"label": "GPU"}), "over")
              .fx(0, ()), 1.0))
    d.append(("hold 捧着", Actor(X, Y, 0.62, "starry").hold(0, ("baton",)), 1.0))
    d.append(("sit 坐下", Actor(X, Y, 0.62, "relieved").sit(0.0), 1.2))
    d.append(("dance 跳舞", Actor(X, Y, 0.62, "grin").dance(0, 4), 1.3))
    d.append(("float 漂浮", Actor(X, Y, 0.62, "awe").float(0, 4, 60), 1.4))
    d.append(("spin 转圈", Actor(X, Y, 0.62, "happy").spin(0.0, 1, 1.0), 0.5))
    d.append(("startle 吓一跳", Actor(X, Y, 0.62, "shock").startle(0.0), 0.16))
    d.append(("push 推", Actor(X, Y, 0.62, "focused").push(0, 3), 1.1))
    d.append(("bonk 撞墙", Actor(X, Y, 0.62, "ko").bonk(0.0), 0.35))
    d.append(("salute 眺望", Actor(X, Y, 0.62, "curious", hat="explorer").front(0, "salute").look(0, 1, -0.4),
              1.0))
    d.append(("magnifier 放大镜", Actor(X, Y, 0.62, "curious", hat="explorer")
              .hold(0, ("magnifier",), "r", -0.2).arm(0, "r", 0.7).ext(0, "r", 0).look(0, 0.6, -0.3), 1.0))
    d.append(("sigh 叹气", Actor(X, Y, 0.62, "tired").sigh(0.0, 2), 0.7))
    d.append(("chin 托腮", Actor(X, Y, 0.62, "hmm").front(0, "chin").fx(0, ()), 1.0))
    d.append(("talk 说话", Actor(X, Y, 0.62, "smile").talk(0, 3, 0.6), 1.07))
    return d


def action_sheet(path, cols=7, cw=300, ch=360):
    demos = _demo_actors()
    rows = math.ceil(len(demos) / cols)
    W, H = cols * cw, rows * ch + 90
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    _bg(ctx, W, H)
    text(ctx, f"动作 / 姿势示例（Actor 时间轴，{len(ACTIONS)} 类动作）", W / 2, 44, 34, "#3A2A26", 1, True)
    for i, (title, a, ts) in enumerate(demos):
        cx, cy = (i % cols) * cw + cw / 2, (i // cols) * ch + 90
        ctx.save()
        ctx.translate(cx, cy + 270)
        a.draw(ctx, ts)
        ctx.restore()
        text(ctx, title, cx, cy + 305, 24, "#3A2A26", 1, True)
    surf.write_to_png(path)
    return path


def gear_sheet(path, cw=300, ch=330):
    items = [("hat", h) for h in HATS] + [("glasses", g) for g in GLASSES] + [("prop", p) for p in PROPS]
    cols = 7
    rows = math.ceil(len(items) / cols)
    W, H = cols * cw, rows * ch + 90
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    _bg(ctx, W, H)
    text(ctx, "配件与道具", W / 2, 44, 34, "#3A2A26", 1, True)
    labels = {"sign": {"label": "举牌"}, "flag": {"label": "GO"}, "chip": {"label": "GPU"},
              "paper": {"title": "论文"}}
    for i, (kind, name) in enumerate(items):
        cx, cy = (i % cols) * cw + cw / 2, (i // cols) * ch + 90
        if kind == "hat":
            draw_mascot(ctx, cx, cy + 240, 0.66, "smile", t=1.0, hat=name, blink=False)
        elif kind == "glasses":
            draw_mascot(ctx, cx, cy + 240, 0.66, "smile", t=1.0, glasses=name, blink=False)
        else:
            from .gear import draw_prop
            ctx.save()
            ctx.translate(cx, cy + 150)
            ctx.scale(0.8, 0.8)
            draw_prop(ctx, (name, labels.get(name, {})), 1.0)
            ctx.restore()
        text(ctx, f"{kind}: {name}", cx, cy + 280, 22, "#3A2A26", 1, True)
    surf.write_to_png(path)
    return path


def sprites(out_dir, size=512):
    os.makedirs(out_dir, exist_ok=True)
    for i, n in enumerate(EXPRESSIONS):
        for kind in ("png", "svg"):
            p = os.path.join(out_dir, f"expr_{n}.{kind}")
            if kind == "png":
                surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
            else:
                surf = cairo.SVGSurface(p, size, size)
            ctx = cairo.Context(surf)
            k = size / 512
            ctx.scale(k, k)
            draw_mascot(ctx, 256, 430, 1.25, expr=n, t=1.3 + i * 0.37, since=5.0, seed=i * 0.7, blink=False)
            if kind == "png":
                surf.write_to_png(p)
            else:
                surf.finish()
    return out_dir


def catalog(path):
    data = {
        "expressions": {n: v.get("desc", "") for n, v in EXPRESSIONS.items()},
        "original_11": ORIGINAL,
        "actions": ACTIONS,
        "front_poses": list(FRONT_POSES),
        "fx": sorted(FX),
        "hats": sorted(HATS),
        "glasses": sorted(GLASSES),
        "props": sorted(PROPS),
        "coords": "draw_mascot(ctx, x, y, s): (x, y) 为脚底中心；s=1 时身体宽 300、总高约 250",
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "sheets"))
    ap.add_argument("--sprites", action="store_true")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    print(expression_sheet(os.path.join(args.out, "expressions.png")))
    print(action_sheet(os.path.join(args.out, "actions.png")))
    print(gear_sheet(os.path.join(args.out, "gear.png")))
    print(catalog(os.path.join(HERE, "catalog.json")))
    if args.sprites:
        print(sprites(os.path.join(HERE, "sprites")))


if __name__ == "__main__":
    main()
