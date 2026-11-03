#!/usr/bin/env python3
"""Instagram Reels / YouTube Shorts 竖版导出（在项目目录里、用项目 venv 的 python 运行）：

  python export_reels.py --chapter 3                                   # 按第 3 章的起止时间
  python export_reels.py --start 101 --end 160 --title "勾股定理的拼图证明"
  python export_reels.py --start 18 --end 56 --src out/<slug>_1080p.mp4

输出 out/<slug>_reels_<起>-<止>.mp4：1080×1920，中间是完整的 16:9 画面（字幕、出处都在），
上下是同一画面去掉黑边后的模糊放大做底，上方可加一行宋体标题（在 Instagram 界面的安全区内）。
YouTube 正片的上传物料由 youtube-publish 技能负责。
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.getcwd()
sys.path.insert(0, ROOT)


def ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        ff = shutil.which("ffmpeg")
        if not ff:
            sys.exit("找不到 ffmpeg：请用项目 venv 的 python 运行")
        return ff


def title_png(path, s, w=1080, h=300):
    import cairo
    from aivid.core import text
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surf)
    size = 76 if len(s) <= 10 else 60
    text(ctx, s, w / 2 + 3, h / 2 + 4, size, "#000000", 0.6, "serif_k")
    text(ctx, s, w / 2, h / 2, size, "#F6EEDF", 1.0, "serif_k")
    ctx.rectangle(w / 2 - 160, h / 2 + size * 0.75, 320, 3)
    ctx.set_source_rgba(0.85, 0.70, 0.42, 0.9)
    ctx.fill()
    surf.write_to_png(path)


def reels(args):
    try:
        from aivid import project
        slug = project.SLUG
    except ImportError:                      # 老项目没有 aivid/project.py
        slug = os.path.basename(ROOT)
    from aivid.timeline import CHAPTERS, DURATION
    out = os.path.join(ROOT, "out")
    if args.chapter:
        s0, s1, ch = CHAPTERS[args.chapter - 1]
        start, end = s0, s1
        title = args.title or f"{ch['num'].replace(' ', '')} {ch['title']}"
    else:
        start, end = args.start, args.end if args.end is not None else DURATION
        title = args.title
    dur = end - start
    if dur > 180:
        print(f"提示：这段 {dur:.0f} 秒，超过 Reels / Shorts 目前约 3 分钟的上限（以平台最新规定为准），建议分段。")
    src = args.src
    if not src:
        import glob
        found = (sorted(glob.glob(os.path.join(out, "*_1080p.mp4"))) + sorted(glob.glob(os.path.join(out, "*_720p.mp4")))
                 + sorted(glob.glob(os.path.join(out, "*_480p.mp4"))))
        src = found[0] if found else None
    if not src or not os.path.exists(src):
        sys.exit("没有找到成片：先 python render.py --res 1080（竖版放大后 480p 会糊）")
    tag = f"{start:g}-{end:g}".replace(".", "_")
    dst = os.path.join(out, f"{slug}_reels_{tag}.mp4")
    fo = max(0.0, dur - 0.6)
    fg = ("[0:v]split=2[a][b];"
          "[a]crop=iw:ih*0.82:0:ih*0.09,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
          "boxblur=24:3,eq=brightness=-0.22[bg];"
          "[b]scale=1080:-2:flags=lanczos[fg];"
          "[bg][fg]overlay=(W-w)/2:(H-h)/2[v0]")
    inputs = ["-ss", f"{start}", "-t", f"{dur}", "-i", src]
    tmp = None
    if title:
        tmp = tempfile.mkdtemp()
        png = os.path.join(tmp, "title.png")
        title_png(png, title)
        inputs += ["-i", png]
        fg += ";[v0][1:v]overlay=0:330[v1]"
        last = "v1"
    else:
        last = "v0"
    fg += f";[{last}]fade=t=in:st=0:d=0.4,fade=t=out:st={fo}:d=0.6,format=yuv420p[v]"
    cmd = [ffmpeg(), "-y", "-hide_banner", "-loglevel", "error", *inputs, "-filter_complex", fg, "-map", "[v]",
           "-map", "0:a?", "-af", f"afade=t=in:st=0:d=0.4,afade=t=out:st={fo}:d=0.6",
           "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-profile:v", "high", "-r", "30",
           "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart", dst]
    subprocess.run(cmd, check=True)
    if tmp:
        shutil.rmtree(tmp, ignore_errors=True)
    print(dst, f"（1080×1920，{dur:.1f} 秒）")


def main():
    ap = argparse.ArgumentParser(description="Instagram Reels / YouTube Shorts 竖版导出")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=None)
    ap.add_argument("--chapter", type=int, default=None, help="按第几章（1 起）的起止时间导出")
    ap.add_argument("--title", default=None, help="竖版上方的一行标题")
    ap.add_argument("--src", default=None, help="源视频（默认找 out/*_1080p / 720p / 480p.mp4）")
    reels(ap.parse_args())


if __name__ == "__main__":
    main()
