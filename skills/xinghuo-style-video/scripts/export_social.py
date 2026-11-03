#!/usr/bin/env python3
"""发布用导出（在项目目录里、用项目 venv 的 python 运行）：

  python export_social.py youtube [--thumb 101.5]
      → out/youtube_description.txt（章节时间戳，可直接贴进 YouTube 简介）
        out/<slug>.srt（字幕文件，可在 YouTube Studio 里另传为 CC 字幕）
        out/thumbnail.jpg（1280×720 封面，取 --thumb 秒的画面，默认片名出现的时刻）

  python export_social.py reels --start 18 --end 56 [--title "第一章 火与石"] [--src out/<slug>_1080p.mp4]
      → out/<slug>_reels_18-56.mp4（Instagram Reels / YouTube Shorts 用的 1080×1920 竖版：
        上下是同一画面的模糊放大做底，中间是完整的 16:9 画面，上方可加一行宋体标题）

  python export_social.py reels --chapter 3       # 直接按第 3 章的起止时间导出
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


def mmss(t):
    t = int(round(t))
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60:02d}:{t % 60:02d}"


def youtube(args):
    from aivid import project
    from aivid.timeline import CHAPTERS, DURATION, NAMES, ORDER, STARTS, srt_text
    out = os.path.join(ROOT, "out")
    os.makedirs(out, exist_ok=True)
    lines = []
    for i, m in enumerate(ORDER):
        ch = getattr(m, "CHAPTER", None)
        if i == 0:
            label = "序章" if not ch else f"{ch['num'].replace(' ', '')} {ch['title']}"
        elif ch:
            label = f"{ch['num'].replace(' ', '')} {ch['title']}"
        elif i == len(ORDER) - 1:
            label = "尾声"
        else:
            continue
        lines.append(f"{mmss(STARTS[i])} {label}")
    # YouTube 章节规则：第一条必须是 00:00，至少 3 条，每段至少 10 秒
    desc = [f"《{project.TITLE}》", "", *lines, "",
            "历史图像来自 Wikimedia Commons（公有领域 / CC0 / CC BY），逐条署名见片中出处字幕。",
            "地图：Natural Earth；NASA Blue Marble / Earth's City Lights。",
            "本片无背景音乐，音效均为程序合成。"]
    p = os.path.join(out, "youtube_description.txt")
    open(p, "w", encoding="utf-8").write("\n".join(desc) + "\n")
    print(p)
    print("\n".join(lines))
    srt = os.path.join(out, f"{project.SLUG}.srt")
    open(srt, "w", encoding="utf-8").write(srt_text())
    print(srt)
    thumb_t = args.thumb if args.thumb is not None else min(15.6, DURATION - 0.1)
    subprocess.run([sys.executable, "render.py", "--still", str(thumb_t), "--res", "720"], check=True,
                   stdout=subprocess.DEVNULL)
    png = os.path.join(out, "stills", f"t{thumb_t:06.2f}.png")
    from PIL import Image
    jpg = os.path.join(out, "thumbnail.jpg")
    Image.open(png).convert("RGB").save(jpg, quality=92)
    print(jpg, "(1280×720)")


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
    from aivid import project
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
        for r in (1080, 720, 480):
            c = os.path.join(out, f"{project.SLUG}_{r}p.mp4")
            if os.path.exists(c):
                src = c
                break
    if not src or not os.path.exists(src):
        sys.exit("没有找到成片：先 python render.py --res 1080（竖版放大后 480p 会糊）")
    tag = f"{start:g}-{end:g}".replace(".", "_")
    dst = os.path.join(out, f"{project.SLUG}_reels_{tag}.mp4")
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
    ap = argparse.ArgumentParser(description="YouTube / Instagram 发布导出")
    sub = ap.add_subparsers(dest="cmd", required=True)
    y = sub.add_parser("youtube")
    y.add_argument("--thumb", type=float, default=None, help="封面取第几秒（全片时间）")
    r = sub.add_parser("reels")
    r.add_argument("--start", type=float, default=0.0)
    r.add_argument("--end", type=float, default=None)
    r.add_argument("--chapter", type=int, default=None, help="按第几章（1 起）的起止时间导出")
    r.add_argument("--title", default=None, help="竖版上方的一行标题")
    r.add_argument("--src", default=None, help="源视频（默认找 out/<slug>_1080p / 720p / 480p.mp4）")
    a = ap.parse_args()
    youtube(a) if a.cmd == "youtube" else reels(a)


if __name__ == "__main__":
    main()
