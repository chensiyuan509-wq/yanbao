#!/usr/bin/env python3
"""校验脚本：在正式渲染前检查代码与时间轴。

  python check.py            # 全部检查（含逐帧冒烟渲染，约 1–2 分钟）
  python check.py --quick    # 跳过逐帧渲染，只做静态检查 + 抽样渲染
"""
import argparse
import glob
import math
import os
import re
import sys
import time
from multiprocessing import get_context

import cairo

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from aivid.core import FPS, FONTS, W, parse_marked, rich_w, wrap_marked  # noqa: E402
from aivid.timeline import (CHAPTERS, DURATION, ORDER, STARTS, SUBS, SUB_MAX_W, SUB_SIZE,  # noqa: E402
                            TRANSITIONS, all_sfx)

OK, FAIL = "✓", "✗"
problems = []


def report(ok, msg):
    print(f"  {OK if ok else FAIL} {msg}")
    if not ok:
        problems.append(msg)


def check_timeline():
    print("时间轴")
    report(abs(DURATION - 300.0) < 1e-6, f"总时长 {DURATION:.2f}s（目标 300s = 5 分钟）")
    report(len(TRANSITIONS) == len(ORDER) - 1, f"{len(ORDER)} 个场景，{len(TRANSITIONS)} 个转场")
    for i, tr in enumerate(TRANSITIONS):
        d = tr[1]
        a, b = ORDER[i], ORDER[i + 1]
        if d / 2 > min(a.DUR, b.DUR) / 2:
            report(False, f"转场 {i} 时长 {d}s 超过相邻场景的一半")
    report(True, "转场窗口都在相邻场景范围内")
    names = [m.__name__.split(".")[-1] for m in ORDER]
    for i, m in enumerate(ORDER):
        for attr in ("DUR", "SUBS", "draw", "sfx"):
            if not hasattr(m, attr):
                report(False, f"{names[i]} 缺少 {attr}")
    print("    " + "  ".join(f"{n}@{s:.1f}s" for n, s in zip(names, STARTS)))


def check_subtitles():
    print("字幕")
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 10, 10)
    ctx = cairo.Context(s)
    prev_end = -1
    worst_cps, worst = 0.0, ""
    for (a, b, txt) in SUBS:
        plain = txt.replace("{", "").replace("}", "")
        if a < prev_end - 1e-6:
            report(False, f"字幕重叠：{plain[:12]}… 开始于 {a:.2f}s，上一条结束于 {prev_end:.2f}s")
        if b > DURATION or a < 0 or b <= a:
            report(False, f"字幕时间异常：{plain[:12]}…")
        n_chars = len(re.sub(r"[\s，。：；！？、（）「」…—,.:;!?()\"“”‘’·→＝＋+=/]", "", plain))
        cps = n_chars / (b - a)
        if cps > worst_cps:
            worst_cps, worst = cps, plain
        if cps > 7.5:
            report(False, f"语速过快 {cps:.1f} 字/秒：{plain}")
        if txt.count("{") != txt.count("}"):
            report(False, f"高亮括号不成对：{txt}")
        lines = wrap_marked(ctx, txt, SUB_SIZE, "bold", SUB_MAX_W)
        widths = [rich_w(ctx, parse_marked(L), SUB_SIZE, "bold") for L in lines]
        if len(lines) > 2 or max(widths) > SUB_MAX_W + 1:
            report(False, f"字幕超宽：{plain}")
        prev_end = b
    report(True, f"{len(SUBS)} 条字幕，最快 {worst_cps:.1f} 字/秒（{worst[:14]}…）")
    report(len(CHAPTERS) == 9, f"{len(CHAPTERS)} 个章节标签")


def _glyph_ok(ctx, ch, fam, weight):
    """把字符画出来，与"缺字方框"比较，判断字体里有没有这个字。"""
    def render(c):
        s = cairo.ImageSurface(cairo.FORMAT_A8, 64, 64)
        g = cairo.Context(s)
        g.select_font_face(fam, cairo.FONT_SLANT_NORMAL, weight)
        g.set_font_size(48)
        g.move_to(4, 52)
        g.show_text(c)
        s.flush()
        return bytes(s.get_data())
    return render(ch) != render("\u2717")  # U+2717 在 Noto CJK 中缺字，用它代表"缺字方框"


def check_glyphs():
    print("字体与字符")
    chars = set()
    for p in glob.glob(os.path.join(ROOT, "aivid", "**", "*.py"), recursive=True):
        src = open(p, encoding="utf-8").read()
        for lit in re.findall(r'"([^"\n]*)"', src):
            chars.update(c for c in lit if ord(c) > 127)
    missing = {}
    for key in ("bold", "mono"):
        fam, weight = FONTS[key]
        for ch in sorted(chars):
            if not _glyph_ok(None, ch, fam, weight):
                missing.setdefault(ch, []).append(key)
    # mono 字体只用于终端文字，只关心 bold 缺字；mono 缺字时也列出供参考
    hard = sorted(c for c, ks in missing.items() if "bold" in ks)
    report(not hard, f"检查了 {len(chars)} 个非 ASCII 字符，正文字体缺字：{''.join(hard) or '无'}")
    mono_only = sorted(c for c, ks in missing.items() if ks == ["mono"])
    if mono_only:
        print(f"    （等宽字体缺：{''.join(mono_only)}，仅在终端文字中出现时需要注意）")


def check_sfx():
    print("音效")
    from aivid.audio import SOUNDS
    cues = all_sfx()
    unknown = sorted({n for _, n, _ in cues if n not in SOUNDS})
    report(not unknown, f"{len(cues)} 个音效触发点，{len(SOUNDS)} 种音效；未定义：{unknown or '无'}")
    out = [t for t, _, _ in cues if t < -0.5 or t > DURATION]
    report(not out, f"触发时间都在片长范围内（越界 {len(out)} 个）")


def _smoke(args):
    f0, f1, step, pw, ph = args
    from render import render_frame
    bad = []
    for i in range(f0, f1, step):
        try:
            render_frame(i / FPS, pw, ph)
        except Exception as e:  # noqa: BLE001
            bad.append((i, repr(e)))
    return bad


def check_render(step, workers):
    print("逐帧冒烟渲染" if step == 1 else f"抽样渲染（每 {step} 帧一张）")
    n = int(round(DURATION * FPS))
    pw, ph = 320, 180
    chunk = math.ceil(n / workers)
    jobs = [(w * chunk, min(n, (w + 1) * chunk), step, pw, ph) for w in range(workers)]
    t0 = time.time()
    with get_context("spawn").Pool(workers) as pool:
        res = pool.map(_smoke, jobs)
    bad = [b for r in res for b in r]
    report(not bad, f"渲染 {len(range(0, n, step))} 帧（{pw}x{ph}），用时 {time.time() - t0:.0f}s，出错 {len(bad)} 帧")
    for i, e in bad[:5]:
        print(f"      帧 {i}（{i / FPS:.2f}s）：{e}")


def check_audio():
    print("音轨")
    import tempfile
    import wave
    import numpy as np
    from aivid.audio import build_audio
    path = os.path.join(tempfile.gettempdir(), "aivid_check.wav")
    t0 = time.time()
    build_audio(path, verbose=False)
    w = wave.open(path)
    n, sr = w.getnframes(), w.getframerate()
    x = np.frombuffer(w.readframes(n), dtype=np.int16)
    w.close()
    os.remove(path)
    peak = np.abs(x.astype(np.int32)).max() / 32768
    report(abs(n / sr - DURATION) < 0.01 and 0.5 < peak < 0.999,
           f"时长 {n / sr:.2f}s，峰值 {peak:.2f}，生成用时 {time.time() - t0:.0f}s")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="只抽样渲染（每 15 帧一张）")
    ap.add_argument("--workers", type=int, default=max(1, min(8, (os.cpu_count() or 2) - 1)))
    args = ap.parse_args()
    check_timeline()
    check_subtitles()
    check_glyphs()
    check_sfx()
    check_render(15 if args.quick else 1, args.workers)
    check_audio()
    print()
    if problems:
        print(f"发现 {len(problems)} 个问题：")
        for p in problems:
            print("  - " + p)
        return 1
    print("全部检查通过 ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
