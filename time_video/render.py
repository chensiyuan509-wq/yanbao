#!/usr/bin/env python3
"""渲染入口。

  python render.py                      # 渲染完整视频 → out/claude_time.mp4
  python render.py --scale 0.5          # 半分辨率快速预览
  python render.py --still 10 25.5 140  # 只导出几帧 PNG 到 out/stills/
  python render.py --start 60 --end 80  # 只渲染一段
"""
import argparse
import math
import os
import subprocess
import sys
import time
from multiprocessing import Pool

import cairo

from tv.core import H, STYLE, W, FPS, ease_io, lin, rad, setc, smooth
from tv.scenes import SCENES, TRANSITIONS
from tv.timeline import DURATION, draw_overlays, srt_text

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "out")


def ffmpeg_exe():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return "ffmpeg"


def reset_style():
    STYLE.update(desat=0.0, tint=None, tint_amt=0.0, bright=1.0)


def draw_scene(ctx, idx, T):
    reset_style()
    ctx.save()
    SCENES[idx][3](ctx, T)
    ctx.restore()
    reset_style()


def scene_index(T):
    for i, (_, t0, t1, _) in enumerate(SCENES):
        if t0 <= T < t1:
            return i
    return len(SCENES) - 1


def offscreen(pw, ph, scale, idx, T):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, pw, ph)
    c = cairo.Context(s)
    c.scale(scale, scale)
    draw_scene(c, idx, T)
    return s


def composite(ctx, kind, p, sa, sb, pw, ph):
    """在像素坐标下把两张画面按转场类型合成。"""
    e = ease_io(p)
    ctx.save()
    ctx.identity_matrix()
    ctx.set_source_rgb(0, 0, 0)
    ctx.paint()

    def paint(surf, alpha=1.0, scale=1.0, dx=0.0, dy=0.0):
        ctx.save()
        ctx.translate(pw / 2 + dx, ph / 2 + dy)
        ctx.scale(scale, scale)
        ctx.translate(-pw / 2, -ph / 2)
        ctx.set_source_surface(surf, 0, 0)
        ctx.paint_with_alpha(max(0.0, min(1.0, alpha)))
        ctx.restore()

    if kind == "fade":
        paint(sa)
        paint(sb, e)
    elif kind in ("zoom", "zoomin"):
        big = 1.35 if kind == "zoom" else 2.6
        paint(sa, 1.0, 1 + (big - 1) * ease_io(p))
        paint(sb, smooth(p * 1.4 - 0.2), (0.8 if kind == "zoom" else 0.6) + (0.2 if kind == "zoom" else 0.4) * e)
    elif kind == "iris":
        paint(sa)
        r = e * math.hypot(pw, ph) / 2 * 1.04
        if r > 0.5:
            ctx.save()
            ctx.arc(pw / 2, ph / 2, r, 0, math.tau)
            ctx.clip()
            paint(sb)
            ctx.restore()
            ctx.set_line_width(max(2, 14 * (1 - p)) * pw / W)
            ctx.set_source_rgba(1, 0.86, 0.6, 0.85 * (1 - p))
            ctx.arc(pw / 2, ph / 2, r, 0, math.tau)
            ctx.stroke()
    elif kind == "wipe":
        paint(sa)
        band = 260 * pw / W
        x = -band + (pw + 2 * band) * e
        g = cairo.LinearGradient(x - band, 0, x + band, 0)
        g.add_color_stop_rgba(0, 0, 0, 0, 1)
        g.add_color_stop_rgba(1, 0, 0, 0, 0)
        ctx.set_source_surface(sb, 0, 0)
        ctx.mask(g)
        ctx.set_source(lin(x - 6, 0, x + 6, 0, [(0, "#FFFFFF", 0), (0.5, "#FFE2A8", 0.5 * math.sin(math.pi * p)), (1, "#FFFFFF", 0)]))
        ctx.rectangle(x - 6, 0, 12, ph)
        ctx.fill()
    elif kind == "push":
        paint(sa, 1.0, 1.0, -pw * e)
        paint(sb, 1.0, 1.0, pw * (1 - e))
    elif kind == "flash":
        if p < 0.5:
            paint(sa)
            ctx.set_source_rgba(1, 0.97, 0.9, smooth(p * 2))
        else:
            paint(sb)
            ctx.set_source_rgba(1, 0.97, 0.9, smooth((1 - p) * 2))
        ctx.paint()
    else:
        paint(sb if p > 0.5 else sa)
    ctx.restore()


def render_frame(T, scale=1.0):
    pw, ph = int(round(W * scale)), int(round(H * scale))
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, pw, ph)
    ctx = cairo.Context(surf)
    ctx.scale(scale, scale)
    done = False
    for b, kind, dur in TRANSITIONS:
        if b - dur / 2 <= T < b + dur / 2:
            ia = scene_index(b - 1e-3)
            ib = scene_index(b + 1e-3)
            p = (T - (b - dur / 2)) / dur
            sa = offscreen(pw, ph, scale, ia, T)
            sb = offscreen(pw, ph, scale, ib, T)
            composite(ctx, kind, p, sa, sb, pw, ph)
            done = True
            break
    if not done:
        draw_scene(ctx, scene_index(T), T)
    reset_style()
    draw_overlays(ctx, T)
    surf.flush()
    return surf


# ---------------------------------------------------------------- 并行渲染


def _worker(args):
    wid, f0, f1, scale, seg_path, crf = args
    pw, ph = int(round(W * scale)), int(round(H * scale))
    cmd = [ffmpeg_exe(), "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{pw}x{ph}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-tune", "animation",
           "-pix_fmt", "yuv420p", "-r", str(FPS), seg_path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t_start = time.time()
    for i in range(f0, f1):
        surf = render_frame(i / FPS, scale)
        proc.stdin.write(bytes(surf.get_data()))
        if wid == 0 and (i - f0) % 60 == 0:
            done = i - f0 + 1
            el = time.time() - t_start
            print(f"  [worker0] {done}/{f1 - f0} 帧, {el / done:.3f}s/帧", flush=True)
    proc.stdin.close()
    proc.wait()
    return seg_path


def render_video(start, end, scale, workers, out_path, crf):
    os.makedirs(os.path.join(OUT, "segments"), exist_ok=True)
    f0, f1 = int(round(start * FPS)), int(round(end * FPS))
    n = f1 - f0
    chunk = math.ceil(n / workers)
    jobs = []
    for w in range(workers):
        a, b = f0 + w * chunk, min(f1, f0 + (w + 1) * chunk)
        if a < b:
            jobs.append((w, a, b, scale, os.path.join(OUT, "segments", f"seg_{w:02d}.mp4"), crf))
    print(f"渲染 {n} 帧（{start:.1f}s–{end:.1f}s），{len(jobs)} 个进程，分辨率 {int(W * scale)}x{int(H * scale)}")
    t0 = time.time()
    with Pool(len(jobs)) as pool:
        segs = pool.map(_worker, jobs)
    print(f"画面渲染完成，用时 {time.time() - t0:.0f}s")
    listfile = os.path.join(OUT, "segments", "list.txt")
    with open(listfile, "w") as f:
        for s in segs:
            f.write(f"file '{os.path.abspath(s)}'\n")
    silent = os.path.join(OUT, "segments", "video_silent.mp4")
    subprocess.run([ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", listfile, "-c", "copy", silent], check=True)
    return silent


def mux(video, audio, out_path, start=0.0, end=None):
    cmd = [ffmpeg_exe(), "-y", "-loglevel", "error", "-i", video, "-ss", f"{start:.3f}"]
    if end is not None:
        cmd += ["-to", f"{end:.3f}"]
    cmd += ["-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-movflags", "+faststart", out_path]
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser(description="渲染《Claude 的宇宙时间课》")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=DURATION)
    ap.add_argument("--scale", type=float, default=1.0, help="分辨率缩放，0.5 = 960x540 预览")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--still", type=float, nargs="*", help="只导出这些时间点的 PNG")
    ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--out", default=os.path.join(OUT, "claude_time.mp4"))
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)

    if args.still:
        d = os.path.join(OUT, "stills")
        os.makedirs(d, exist_ok=True)
        for T in args.still:
            p = os.path.join(d, f"t{T:06.2f}.png")
            render_frame(T, args.scale).write_to_png(p)
            print(p)
        return

    with open(os.path.join(OUT, "subtitles.srt"), "w", encoding="utf-8") as f:
        f.write(srt_text())
    silent = render_video(args.start, args.end, args.scale, args.workers, args.out, args.crf)
    if args.no_audio:
        os.replace(silent, args.out)
    else:
        from tv.audio import build_audio
        wav = os.path.join(OUT, "soundtrack.wav")
        build_audio(wav)
        mux(silent, wav, args.out, args.start, args.end)
    print("完成 →", args.out)


if __name__ == "__main__":
    sys.exit(main())
