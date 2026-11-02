#!/usr/bin/env python3
"""渲染入口。

  python render.py                         # 完整渲染 1280×720 / 30fps → out/ai_connect.mp4
  python render.py --res 480               # 854×480
  python render.py --still 12 95.5 230     # 只导出这几个时间点的 PNG 到 out/stills/
  python render.py --sheet 5               # 每 5 秒取一帧，拼成预览联系表 out/sheet_*.jpg
  python render.py --start 60 --end 90     # 只渲染一段（带音轨）
  python render.py --audio-only            # 只生成音轨 out/soundtrack.wav
"""
import argparse
import math
import os
import shutil
import subprocess
import sys
import time
from multiprocessing import get_context

import cairo

from aivid.core import FPS, H, W, reset_filter
from aivid.timeline import DURATION, ORDER, STARTS, draw_overlays, scene_index, srt_text, transition_at
from aivid.transitions import composite

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "out")
RES = {360: (640, 360), 480: (854, 480), 720: (1280, 720), 1080: (1920, 1080)}


def ffmpeg_exe():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        exe = shutil.which("ffmpeg")
        if not exe:
            sys.exit("找不到 ffmpeg：请 pip install imageio-ffmpeg，或安装系统 ffmpeg。")
        return exe


def _design(ctx, pw, ph):
    sc = ph / H
    ctx.translate((pw - W * sc) / 2, 0)
    ctx.scale(sc, sc)


def _draw_scene(ctx, idx, t, pw, ph):
    reset_filter()
    ctx.save()
    _design(ctx, pw, ph)
    ORDER[idx].draw(ctx, t)
    ctx.restore()
    reset_filter()


def _offscreen(idx, t, pw, ph):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, pw, ph)
    c = cairo.Context(s)
    c.set_source_rgb(0, 0, 0)
    c.paint()
    _draw_scene(c, idx, t, pw, ph)
    s.flush()
    return s


def render_frame(T, pw, ph):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, pw, ph)
    ctx = cairo.Context(surf)
    ctx.set_source_rgb(0, 0, 0)
    ctx.paint()
    tr = transition_at(T)
    if tr:
        ia, ib, kind, p, params = tr
        sa = _offscreen(ia, T - STARTS[ia], pw, ph)
        sb = _offscreen(ib, T - STARTS[ib], pw, ph)
        composite(ctx, kind, p, sa, sb, pw, ph, params)
    else:
        i = scene_index(T)
        _draw_scene(ctx, i, T - STARTS[i], pw, ph)
    ctx.save()
    _design(ctx, pw, ph)
    draw_overlays(ctx, T)
    ctx.restore()
    surf.flush()
    return surf


# ---------------------------------------------------------------- 并行渲染


def _worker(job):
    wid, f0, f1, pw, ph, seg_path, crf, preset = job
    cmd = [ffmpeg_exe(), "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{pw}x{ph}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-tune", "animation",
           "-threads", "2", "-pix_fmt", "yuv420p", "-r", str(FPS), seg_path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t_start = time.time()
    n = f1 - f0
    for i in range(f0, f1):
        surf = render_frame(i / FPS, pw, ph)
        proc.stdin.write(bytes(surf.get_data()))
        done = i - f0 + 1
        if wid == 0 and (done % 90 == 0 or done == n):
            el = time.time() - t_start
            eta = el / done * (n - done)
            print(f"  [进程0] {done}/{n} 帧  {el / done:.3f}s/帧  预计还需 {eta:.0f}s", flush=True)
    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"ffmpeg 编码失败：{seg_path}")
    return seg_path


def render_video(start, end, pw, ph, workers, crf, preset):
    seg_dir = os.path.join(OUT, "segments")
    os.makedirs(seg_dir, exist_ok=True)
    for f in os.listdir(seg_dir):
        os.remove(os.path.join(seg_dir, f))
    f0, f1 = int(round(start * FPS)), int(round(end * FPS))
    n = f1 - f0
    chunk = math.ceil(n / workers)
    jobs = []
    for w in range(workers):
        a, b = f0 + w * chunk, min(f1, f0 + (w + 1) * chunk)
        if a < b:
            jobs.append((w, a, b, pw, ph, os.path.join(seg_dir, f"seg_{w:02d}.mp4"), crf, preset))
    print(f"渲染 {n} 帧（{start:.1f}s – {end:.1f}s），{len(jobs)} 个进程，{pw}x{ph} @ {FPS}fps")
    t0 = time.time()
    with get_context("spawn").Pool(len(jobs)) as pool:
        segs = pool.map(_worker, jobs)
    print(f"画面渲染完成，用时 {time.time() - t0:.0f}s")
    listfile = os.path.join(seg_dir, "list.txt")
    with open(listfile, "w") as f:
        for s in segs:
            f.write(f"file '{os.path.abspath(s)}'\n")
    silent = os.path.join(seg_dir, "video_silent.mp4")
    subprocess.run([ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", listfile, "-c", "copy", silent], check=True)
    return silent


def mux(video, audio, out_path, start=0.0, end=None):
    cmd = [ffmpeg_exe(), "-y", "-loglevel", "error", "-i", video, "-ss", f"{start:.3f}"]
    if end is not None:
        cmd += ["-to", f"{end:.3f}"]
    cmd += ["-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
            "-b:a", "192k", "-shortest", "-movflags", "+faststart", out_path]
    subprocess.run(cmd, check=True)


def contact_sheet(times, pw, ph, path, cols=4):
    from PIL import Image
    tw, th = 480, 270
    rows = math.ceil(len(times) / cols)
    sheet = Image.new("RGB", (tw * cols, th * rows), "black")
    for i, T in enumerate(times):
        surf = render_frame(T, pw, ph)
        im = Image.frombuffer("RGBA", (pw, ph), bytes(surf.get_data()), "raw", "BGRA", 0, 1)
        im = im.convert("RGB").resize((tw, th), Image.LANCZOS)
        sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
    sheet.save(path, quality=88)
    return path


def main():
    ap = argparse.ArgumentParser(description="渲染《连接的力量：AI 为什么先在美国爆发》")
    ap.add_argument("--res", type=int, default=720, choices=sorted(RES), help="输出高度（默认 720）")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=DURATION)
    ap.add_argument("--workers", type=int, default=max(1, min(8, (os.cpu_count() or 2) - 1)))
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--preset", default="medium")
    ap.add_argument("--still", type=float, nargs="*", help="只导出这些时间点（秒）的 PNG")
    ap.add_argument("--sheet", type=float, help="每隔多少秒取一帧，拼成预览联系表")
    ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--audio-only", action="store_true")
    ap.add_argument("--out", default=os.path.join(OUT, "ai_connect.mp4"))
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    pw, ph = RES[args.res]

    if args.still:
        d = os.path.join(OUT, "stills")
        os.makedirs(d, exist_ok=True)
        for T in args.still:
            p = os.path.join(d, f"t{T:06.2f}.png")
            render_frame(T, pw, ph).write_to_png(p)
            print(p)
        return 0

    if args.sheet:
        times = []
        T = args.start + args.sheet / 2
        while T < args.end:
            times.append(T)
            T += args.sheet
        k = 0
        for i in range(0, len(times), 24):
            p = os.path.join(OUT, f"sheet_{k:02d}.jpg")
            contact_sheet(times[i:i + 24], pw, ph, p)
            print(p, f"{times[i]:.1f}s – {times[min(i + 23, len(times) - 1)]:.1f}s")
            k += 1
        return 0

    wav = os.path.join(OUT, "soundtrack.wav")
    if args.audio_only:
        from aivid.audio import build_audio
        build_audio(wav)
        return 0

    with open(os.path.join(OUT, "subtitles.srt"), "w", encoding="utf-8") as f:
        f.write(srt_text())
    t0 = time.time()
    silent = render_video(args.start, args.end, pw, ph, args.workers, args.crf, args.preset)
    if args.no_audio:
        shutil.move(silent, args.out)
    else:
        from aivid.audio import build_audio
        build_audio(wav)
        mux(silent, wav, args.out, args.start, args.end)
    print(f"完成 → {args.out}（总用时 {time.time() - t0:.0f}s）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
