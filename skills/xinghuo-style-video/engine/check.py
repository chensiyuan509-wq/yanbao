#!/usr/bin/env python3
"""渲染前校验：

  python check.py            # 全部检查（含每 3 帧一张的冒烟渲染，约 2–4 分钟）
  python check.py --quick    # 只抽样渲染（每 30 帧一张）
  python check.py --audio    # 额外生成一遍完整音轨，检查响度与峰值（约 1 分钟）
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

from aivid import narration, project  # noqa: E402
from aivid.core import FPS, FONTS, parse_marked, rich_w, wrap_marked  # noqa: E402
from aivid.timeline import (CHAPTERS, DURATION, NAMES, ORDER, STARTS, SUBS, SUB_MAX_W, SUB_SIZE,  # noqa: E402
                            TRANSITIONS, VO, all_sfx)

OK, FAIL, WARN = "✓", "✗", "!"
problems, warnings = [], []
TARGET = project.TARGET_SEC


def report(ok, msg, warn_only=False):
    print(f"  {OK if ok else (WARN if warn_only else FAIL)} {msg}")
    if not ok:
        (warnings if warn_only else problems).append(msg)


def check_timeline():
    print("时间轴")
    report(abs(DURATION - TARGET) < 1e-6, f"总时长 {DURATION:.2f}s（目标 {TARGET:.0f}s = {TARGET / 60:g} 分钟）")
    report(len(TRANSITIONS) == len(ORDER) - 1, f"{len(ORDER)} 个场景，{len(TRANSITIONS)} 个转场")
    for i, tr in enumerate(TRANSITIONS):
        d = tr[1]
        if d / 2 > min(ORDER[i].DUR, ORDER[i + 1].DUR) / 2:
            report(False, f"转场 {i} 时长 {d}s 超过相邻场景的一半")
    for i, m in enumerate(ORDER):
        for attr in ("DUR", "VO", "draw", "sfx"):
            if not hasattr(m, attr):
                report(False, f"{NAMES[i]} 缺少 {attr}")
    print("    " + "  ".join(f"{n[:3]}@{s:.0f}s" for n, s in zip(NAMES, STARTS)))


def check_captions():
    print("字幕文案（每句的阅读时间）")
    short = 0
    for L in VO:
        room = L["slot_end"] - L["start"]
        if room < narration.estimate(L["text"]):
            short += 1
            report(False, f"{L['id']} 只有 {room:.2f}s，读不完：{narration.plain(L['text'])[:18]}…", warn_only=True)
    report(True, f"{len(VO)} 句文案，阅读时间偏紧的 {short} 句")


def check_subtitles():
    print("字幕")
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, 10, 10)
    ctx = cairo.Context(s)
    prev_end = -1
    worst_cps, worst = 0.0, ""
    for (a, b, txt) in SUBS:
        plain = txt.replace("{", "").replace("}", "")
        if a < prev_end - 0.05:
            report(False, f"字幕重叠：{plain[:12]}… 开始于 {a:.2f}s，上一条结束于 {prev_end:.2f}s")
        if b > DURATION + 0.3 or a < 0 or b <= a:
            report(False, f"字幕时间异常：{plain[:12]}…")
        n_chars = len(re.sub(r"[\s，。：；！？、（）「」《》…—,.:;!?()\"“”‘’·→＝＋+=/%]", "", plain))
        cps = n_chars / max(b - a, 0.01)
        if cps > worst_cps:
            worst_cps, worst = cps, plain
        if txt.count("{") != txt.count("}"):
            report(False, f"高亮括号不成对：{txt}")
        lines = wrap_marked(ctx, txt, SUB_SIZE, "medium", SUB_MAX_W)
        widths = [rich_w(ctx, parse_marked(L), SUB_SIZE, "medium") for L in lines]
        if len(lines) > 2 or max(widths) > SUB_MAX_W + 1:
            report(False, f"字幕超宽：{plain}")
        prev_end = b
    report(True, f"{len(SUBS)} 条字幕，单条最快 {worst_cps:.1f} 字/秒（{worst[:14]}…）")
    report(len(CHAPTERS) == project.CHAPTERS, f"{len(CHAPTERS)} 个章节标题（应为 {project.CHAPTERS}）")


def _glyph_ok(ch, fam, weight):
    def render(c):
        s = cairo.ImageSurface(cairo.FORMAT_A8, 64, 64)
        g = cairo.Context(s)
        g.select_font_face(fam, cairo.FONT_SLANT_NORMAL, weight)
        g.set_font_size(48)
        g.move_to(4, 52)
        g.show_text(c)
        s.flush()
        return bytes(s.get_data())
    return render(ch) != render("✗")


def check_glyphs():
    print("字体与字符")
    sub_chars = set()
    for L in VO:
        sub_chars.update(c for c in narration.plain(L["text"]) if ord(c) > 127)
    lab_chars = set()
    for p in glob.glob(os.path.join(ROOT, "aivid", "**", "*.py"), recursive=True):
        src = open(p, encoding="utf-8").read()
        for lit in re.findall(r"[\"']([^\"'\n]*)[\"']", src):
            lab_chars.update(c for c in lit if 0x2E80 <= ord(c) <= 0x9FFF or 0xFF00 <= ord(c) <= 0xFFEF)
    miss_sub = [c for c in sorted(sub_chars) if not _glyph_ok(c, FONTS["medium"][0], FONTS["medium"][1])]
    miss_lab = [c for c in sorted(lab_chars) if not _glyph_ok(c, FONTS["serif_sb"][0], FONTS["serif_sb"][1])]
    report(not miss_sub, f"字幕用到 {len(sub_chars)} 个非 ASCII 字符，缺字：{''.join(miss_sub) or '无'}")
    report(not miss_lab, f"画面文字用到 {len(lab_chars)} 个汉字 / 全角符号，宋体缺字：{''.join(miss_lab) or '无'}")


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
    t0 = time.time()
    n = 0
    for i in range(f0, f1, step):
        try:
            render_frame(i / FPS, pw, ph)
            n += 1
        except Exception as e:  # noqa: BLE001
            bad.append((i, repr(e)))
    return bad, n, time.time() - t0


def check_render(step, workers):
    print("逐帧冒烟渲染" if step == 1 else f"抽样渲染（每 {step} 帧一张）")
    n = int(round(DURATION * FPS))
    pw, ph = 480, 270
    chunk = math.ceil(n / workers)
    jobs = [(w * chunk, min(n, (w + 1) * chunk), step, pw, ph) for w in range(workers)]
    t0 = time.time()
    with get_context("spawn").Pool(workers) as pool:
        res = pool.map(_smoke, jobs)
    bad = [b for r in res for b in r[0]]
    cnt = sum(r[1] for r in res)
    report(not bad, f"渲染 {cnt} 帧（{pw}x{ph}），用时 {time.time() - t0:.0f}s，出错 {len(bad)} 帧")
    for i, e in bad[:6]:
        print(f"      帧 {i}（{i / FPS:.2f}s）：{e}")


def check_audio():
    print("音轨")
    import tempfile
    import wave
    import numpy as np
    from aivid.audio import build_audio, loudness
    path = os.path.join(tempfile.gettempdir(), f"{project.SLUG}_check.wav")
    t0 = time.time()
    build_audio(path, verbose=False)
    w = wave.open(path)
    n, sr = w.getnframes(), w.getframerate()
    x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32).reshape(-1, 2).T / 32768
    w.close()
    os.remove(path)
    peak = float(np.abs(x).max())
    lu = loudness(x)
    report(abs(n / sr - DURATION) < 0.05 and peak < 0.999 and -18 < lu < -13,
           f"时长 {n / sr:.2f}s，峰值 {20 * math.log10(peak):.1f} dBFS，响度约 {lu:.1f} LUFS，用时 {time.time() - t0:.0f}s")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--audio", action="store_true")
    ap.add_argument("--workers", type=int, default=max(1, min(8, (os.cpu_count() or 2) - 1)))
    args = ap.parse_args()
    check_timeline()
    check_captions()
    check_subtitles()
    check_glyphs()
    check_sfx()
    check_render(30 if args.quick else 3, args.workers)
    if args.audio:
        check_audio()
    print()
    for w in warnings:
        print("  提示：" + w)
    if problems:
        print(f"发现 {len(problems)} 个问题：")
        for p in problems:
            print("  - " + p)
        return 1
    print("全部检查通过 ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())
