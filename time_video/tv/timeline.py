"""时间轴：字幕脚本、章节、全局叠加层（字幕 / 章节卡 / 进度条）。

所有时间都是视频里的全局秒数。
"""
from .core import (H, W, clamp, ease_back, ease_io, ease_out, env, font,
                   lin, prog, rrect, setc, smooth, text, text_w)

DURATION = 180.0

# {…} 内的文字会以高亮色显示
SUBS = [
    (0.8, 4.0, "嗨，我是 {Claude}。"),
    (4.2, 8.4, "今天想带你看清一样东西：它无处不在，却看不见、摸不着。"),
    (8.6, 11.6, "它就是——{时间}。"),
    (12.6, 16.4, "想象一下：如果宇宙里的一切都静止不动——"),
    (16.6, 20.2, "没有变化，就分不出“之前”和“之后”。"),
    (20.4, 25.0, "所以，时间就像一把{尺子}，用来给{变化}排顺序。"),
    (25.2, 29.6, "蜡烛变短、叶子飘落、我打了个哈欠——都是时间的脚印。"),
    (30.4, 34.6, "宇宙已经 {138 亿岁}了。太大了？我们把它压缩成{一年}。"),
    (34.8, 38.8, "1 月 1 日零点，大爆炸。{9 月初}，太阳和地球才诞生。"),
    (39.0, 42.8, "恐龙在 {12 月 25 日}登场，30 日就谢幕了。"),
    (43.0, 46.8, "而人类，直到除夕夜 {23:48} 才出现。"),
    (47.0, 50.6, "有文字记载的全部历史？只占{最后 12 秒}。"),
    (51.4, 55.2, "时间还有方向：杯子会摔碎，却从不自己拼回去。"),
    (55.4, 59.0, "因为宇宙总是从有序走向混乱，这叫“{熵增}”。"),
    (59.2, 62.6, "熵增给时间装上了{箭头}：从过去，指向未来。"),
    (63.6, 67.0, "那怎么测量时间？秘诀是：{数重复}。"),
    (67.2, 71.6, "钟摆每秒摆一下；手表里的石英，每秒振动 {32,768} 次。"),
    (71.8, 76.0, "原子钟数的是铯原子：每秒 {9,192,631,770} 次。"),
    (76.2, 79.6, "数满这么多下就是 1 秒，{上亿年}也差不了 1 秒。"),
    (80.4, 84.6, "可大脑的感受并不准：开心时光飞逝，无聊时度日如年。"),
    (84.8, 88.6, "更奇妙的是：你看到的一切，都是它的{过去}。"),
    (88.8, 94.4, "月光走了 {1.3 秒}，阳光走了 {8 分 20 秒}，北极星的光走了约 {430 年}。"),
    (94.6, 99.4, "看得越远，看到的越古老。仰望星空，就是在翻宇宙的{相册}。"),
    (100.6, 104.0, "这说明：时间和空间，是{绑在一起}的。"),
    (104.2, 108.4, "把每个瞬间的宇宙拍成一张照片，再一张张叠起来——"),
    (108.6, 113.2, "就得到了“{时空}”。我走过的路，在里面是一条线：{世界线}。"),
    (113.4, 117.6, "{光速}是时空的限速，任何东西都追不上它。"),
    (118.4, 122.4, "看这只“{光钟}”：光在两面镜子间弹一次，就算一下。"),
    (122.6, 127.2, "让光钟高速飞行，光得走{斜线}，路更长，每一下就变慢了。"),
    (127.4, 131.4, "这就是相对论：{跑得越快，时间走得越慢}。"),
    (131.6, 134.4, "如果以 {0.87 倍光速}飞行——"),
    (134.6, 137.6, "飞船上的我过了 {5 年}，地球上的双胞胎已过了 {10 年}。"),
    (138.6, 142.0, "还有一样东西能改变时间：{质量}。"),
    (142.2, 146.6, "质量会把时空{压弯}，越靠近它，时间走得{越慢}。"),
    (146.8, 151.0, "GPS 卫星离地球远，它的钟每天比地面快 {38 微秒}。"),
    (151.2, 154.6, "不校正的话，导航每天会偏差约 {10 公里}。"),
    (155.4, 159.4, "到了{黑洞}边缘，时空弯曲到了极致——"),
    (159.6, 164.4, "从远处看，那里的时钟几乎{停止}，时间仿佛被冻结。"),
    (165.4, 169.4, "所以，时间不是一成不变的背景滴答声。"),
    (169.6, 173.6, "它会{伸缩}，会{弯曲}，和空间一起，织成了宇宙。"),
    (173.8, 176.6, "你刚刚度过的这三分钟，{独一无二}。"),
    (176.8, 179.6, "谢谢你，陪我一起{看见时间}。"),
]

CHAPTERS = [
    (12.0, 63.0, "第一章", "什么是时间"),
    (63.0, 100.0, "第二章", "怎么感知时间"),
    (100.0, 138.0, "第三章", "时间与空间"),
    (138.0, 165.0, "第四章", "质量扭曲时间"),
]

ACCENT = "#FFC765"


def _segments(s):
    """把 '{高亮}' 标记拆成 [(文字, 是否高亮), ...]。"""
    out, buf, hi = [], "", False
    for ch in s:
        if ch == "{":
            if buf:
                out.append((buf, hi))
            buf, hi = "", True
        elif ch == "}":
            if buf:
                out.append((buf, hi))
            buf, hi = "", False
        else:
            buf += ch
    if buf:
        out.append((buf, hi))
    return out


def plain(s):
    return s.replace("{", "").replace("}", "")


def draw_subtitle(ctx, T):
    for t0, t1, s in SUBS:
        if t0 - 0.05 <= T <= t1 + 0.25:
            a = env(T, t0, t1 + 0.2, 0.22, 0.25)
            if a <= 0:
                continue
            rise = (1 - ease_out(prog(T, t0, t0 + 0.35))) * 14
            size = 42
            segs = _segments(s)
            widths = [text_w(ctx, seg, size, "bold") for seg, _ in segs]
            tw = sum(widths)
            y = H - 82 + rise
            pw, ph = tw + 64, 66
            rrect(ctx, W / 2 - pw / 2, y - ph / 2, pw, ph, 18)
            setc(ctx, "#0C0A14", 0.52 * a)
            ctx.fill()
            x = W / 2 - tw / 2
            for (seg, hi), wseg in zip(segs, widths):
                text(ctx, seg, x, y, size, ACCENT if hi else "#FFFFFF", a, "bold", "l",
                     shadow=(0, 2, "#000000", 0.45))
                x += wseg


def draw_chapter(ctx, T):
    for c0, c1, num, title in CHAPTERS:
        if not (c0 <= T <= c1 + 0.5):
            continue
        # 章节卡（大）
        k0, k1 = c0 + 0.35, c0 + 3.1
        if k0 <= T <= k1:
            u = prog(T, k0, k1)
            open_ = ease_out(prog(T, k0, k0 + 0.5))
            close = ease_io(prog(T, k1 - 0.5, k1))
            hgt = 210 * open_ * (1 - close)
            if hgt > 1:
                cy = H * 0.5
                ctx.rectangle(0, cy - hgt / 2, W, hgt)
                ctx.set_source(lin(0, 0, W, 0, [(0, "#0B0A18", 0.0), (0.2, "#0B0A18", 0.62),
                                                  (0.8, "#0B0A18", 0.62), (1, "#0B0A18", 0.0)]))
                ctx.fill()
                a = env(T, k0 + 0.15, k1 - 0.15, 0.35, 0.3)
                lw = 260 * ease_out(prog(T, k0 + 0.1, k0 + 0.8))
                for sx in (-1, 1):
                    x0 = W / 2 + sx * 120
                    ctx.set_line_width(2)
                    setc(ctx, ACCENT, a * 0.8)
                    ctx.move_to(x0, cy - 52)
                    ctx.line_to(x0 + sx * lw, cy - 52)
                    ctx.stroke()
                text(ctx, num, W / 2, cy - 52, 34, ACCENT, a, "bold", spacing=0.3)
                drift = (u - 0.5) * 16
                text(ctx, title, W / 2 + drift, cy + 26, 86, "#FFFFFF", a, "black",
                     spacing=0.12, shadow=(0, 4, "#000000", 0.4))
        # 左上角章节标签
        ta = env(T, c0 + 2.9, c1 - 0.2, 0.6, 0.5)
        if ta > 0:
            label = f"{num} · {title}"
            tw = text_w(ctx, label, 26, "bold")
            x0, y0 = 54, 44
            rrect(ctx, x0, y0, tw + 52, 46, 23)
            setc(ctx, "#0C0A14", 0.42 * ta)
            ctx.fill()
            ctx.arc(x0 + 23, y0 + 23, 6, 0, 6.2832)
            setc(ctx, ACCENT, ta)
            ctx.fill()
            text(ctx, label, x0 + 38, y0 + 23, 26, "#FFFFFF", ta * 0.95, "bold", "l")


def draw_progress(ctx, T):
    a = env(T, 12.0, DURATION - 1.2, 0.8, 0.8) * 0.85
    if a <= 0:
        return
    y, h = H - 10, 4
    x0, x1 = 0, W
    total = DURATION
    for c0, c1, _, _ in [(0, 12, 0, 0)] + CHAPTERS + [(165, 180, 0, 0)]:
        sx0 = x0 + (x1 - x0) * c0 / total + 2
        sx1 = x0 + (x1 - x0) * c1 / total - 2
        ctx.rectangle(sx0, y, sx1 - sx0, h)
        setc(ctx, "#FFFFFF", 0.18 * a)
        ctx.fill()
        fill = clamp((T - c0) / (c1 - c0))
        if fill > 0:
            ctx.rectangle(sx0, y, (sx1 - sx0) * fill, h)
            setc(ctx, ACCENT, 0.9 * a)
            ctx.fill()


def draw_overlays(ctx, T):
    draw_chapter(ctx, T)
    draw_subtitle(ctx, T)
    draw_progress(ctx, T)
    # 片头淡入 / 片尾淡出
    fade = max(1 - smooth(prog(T, 0.0, 0.9)), smooth(prog(T, DURATION - 1.1, DURATION - 0.05)))
    if fade > 0:
        ctx.set_source_rgba(0, 0, 0, fade)
        ctx.paint()


def srt_text():
    def ts(x):
        ms = int(round(x * 1000))
        h, ms = divmod(ms, 3600000)
        m, ms = divmod(ms, 60000)
        s, ms = divmod(ms, 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    lines = []
    for i, (t0, t1, s) in enumerate(SUBS, 1):
        lines += [str(i), f"{ts(t0)} --> {ts(t1)}", plain(s), ""]
    return "\n".join(lines)


__all__ = ["SUBS", "CHAPTERS", "DURATION", "draw_overlays", "srt_text", "ease_back", "font"]
