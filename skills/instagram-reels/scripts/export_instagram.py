#!/usr/bin/env python3
"""把横版（16:9）视频转成 Instagram 竖版：Reels 9:16（1080×1920）或动态 4:5（1080×1350）。

  python export_instagram.py 成片.mp4 --start 101 --end 160 --title "勾股定理的拼图证明"
  python export_instagram.py 成片.mp4 --format feed --start 30 --end 75
  python export_instagram.py 成片.mp4 --chapter 3            # 在 aivid 视频项目目录里运行时，可按章节取起止
  python export_instagram.py 成片.mp4 --all-chapters          # 每章导出一条（超过 3 分钟的会提示）

版式：中间是完整的横版画面（字幕、出处都保留），上下用同一画面去掉遮幅黑边后模糊放大做底，
上方可加一行宋体标题（落在 Instagram 界面不遮挡的区域）。同时输出：
  <名字>.mp4          H.264 + AAC，30fps，+faststart
  <名字>_cover.jpg    封面（同尺寸，取 --cover 秒，默认这段的 40% 处）
  <名字>.txt          配文草稿（标题、图像来源说明、话题标签），发之前自己改
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

SIZES = {"reels": (1080, 1920, 330), "feed": (1080, 1350, 40)}      # 宽、高、标题条的 y
LB_FRAC = 96 / 1080                                                  # 星火风格的遮幅黑边比例（底图裁掉它）


def ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        ff = shutil.which("ffmpeg")
        if not ff:
            sys.exit("找不到 ffmpeg：装系统 ffmpeg，或用带 imageio-ffmpeg 的 python 运行")
        return ff


def duration(src):
    out = subprocess.run([ffmpeg(), "-hide_banner", "-i", src], capture_output=True, text=True).stderr
    for line in out.splitlines():
        if "Duration:" in line:
            h, m, s = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    sys.exit(f"读不到时长：{src}")


def title_png(path, s, w):
    """宋体标题条（透明底）。用 pycairo + 系统思源宋体；没有 pycairo 就跳过标题。"""
    try:
        import cairo
    except ImportError:
        print("提示：没有 pycairo，跳过标题（用视频项目的 venv 运行即可）")
        return False
    h = 300
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surf)
    ctx.select_font_face("Noto Serif CJK SC Black", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    size = 76 if len(s) <= 10 else (62 if len(s) <= 14 else 50)
    ctx.set_font_size(size)
    ext = ctx.text_extents(s)
    x, y = (w - ext.width) / 2 - ext.x_bearing, h / 2 + size * 0.35
    ctx.set_source_rgba(0, 0, 0, 0.6)
    ctx.move_to(x + 3, y + 4)
    ctx.show_text(s)
    ctx.set_source_rgba(0.965, 0.933, 0.875, 1)
    ctx.move_to(x, y)
    ctx.show_text(s)
    ctx.rectangle(w / 2 - 160, y + size * 0.45, 320, 3)
    ctx.set_source_rgba(0.85, 0.70, 0.42, 0.9)
    ctx.fill()
    surf.write_to_png(path)
    return True


def chapters_from_project():
    """在 aivid 视频项目目录里运行时，读取章节起止。"""
    sys.path.insert(0, os.getcwd())
    try:
        from aivid.timeline import CHAPTERS
    except Exception:
        sys.exit("--chapter / --all-chapters 需要在 aivid 视频项目目录里运行；否则用 --start / --end")
    return [(s0, s1, f"{ch['num'].replace(' ', '')} {ch['title']}") for s0, s1, ch in CHAPTERS]


def export(src, start, end, title, fmt, outdir, cover_at=None, letterboxed=True):
    W, H, ty = SIZES[fmt]
    dur = end - start
    if fmt == "reels" and dur > 180:
        print(f"提示：{dur:.0f} 秒，超过 Reels 目前约 3 分钟的上限（以 Instagram 最新规定为准），建议拆成几段。")
    base = os.path.splitext(os.path.basename(src))[0]
    name = f"{base}_{fmt}_{start:g}-{end:g}".replace(".", "_")
    dst = os.path.join(outdir, name + ".mp4")
    crop = f"crop=iw:ih*{1 - 2 * LB_FRAC - 0.002:.4f}:0:ih*{LB_FRAC:.4f}," if letterboxed else ""
    fo = max(0.0, dur - 0.6)
    fg = ("[0:v]split=2[a][b];"
          f"[a]{crop}scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=24:3,eq=brightness=-0.22[bg];"
          f"[b]scale={W}:-2:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2[v0]")
    inputs = ["-ss", f"{start}", "-t", f"{dur}", "-i", src]
    tmp = tempfile.mkdtemp()
    last = "v0"
    if title and title_png(os.path.join(tmp, "t.png"), title, W):
        inputs += ["-i", os.path.join(tmp, "t.png")]
        fg += f";[v0][1:v]overlay=0:{ty}[v1]"
        last = "v1"
    fg += f";[{last}]fade=t=in:st=0:d=0.4,fade=t=out:st={fo}:d=0.6,format=yuv420p[v]"
    ff = ffmpeg()
    subprocess.run([ff, "-y", "-hide_banner", "-loglevel", "error", *inputs, "-filter_complex", fg, "-map", "[v]",
                    "-map", "0:a?", "-af", f"afade=t=in:st=0:d=0.4,afade=t=out:st={fo}:d=0.6",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-profile:v", "high", "-r", "30",
                    "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart", dst], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    t_cover = cover_at if cover_at is not None else dur * 0.4
    cover = os.path.join(outdir, name + "_cover.jpg")
    subprocess.run([ff, "-y", "-hide_banner", "-loglevel", "error", "-ss", f"{t_cover}", "-i", dst, "-frames:v", "1",
                    "-q:v", "2", cover], check=True)
    cap = os.path.join(outdir, name + ".txt")
    with open(cap, "w", encoding="utf-8") as f:
        f.write(f"{title or '（标题）'}\n\n（一两句话：这一段讲了什么、最有意思的那个事实。）\n\n"
                "历史图像来自 Wikimedia Commons（公有领域 / CC0 / CC BY），出处见画面左下角。完整版见 YouTube（链接）。\n\n"
                "#科普 #历史 #科学史 #纪录片 #动画\n")
    print(f"{dst}（{W}×{H}，{dur:.1f} 秒）\n  封面 {cover}\n  配文草稿 {cap}")
    return dst


def main():
    ap = argparse.ArgumentParser(description="Instagram 竖版导出（Reels 9:16 / 动态 4:5）")
    ap.add_argument("src", help="横版成片（建议 1080p）")
    ap.add_argument("--format", choices=sorted(SIZES), default="reels")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=None)
    ap.add_argument("--title", default=None)
    ap.add_argument("--chapter", type=int, default=None, help="第几章（1 起；需在 aivid 视频项目目录里）")
    ap.add_argument("--all-chapters", action="store_true")
    ap.add_argument("--cover", type=float, default=None, help="封面取这一段的第几秒")
    ap.add_argument("--no-letterbox", action="store_true", help="源视频没有遮幅黑边时加上")
    ap.add_argument("--outdir", default=None, help="默认与源视频同目录下的 instagram/")
    a = ap.parse_args()
    if not os.path.exists(a.src):
        sys.exit(f"找不到 {a.src}")
    if "_480p" in os.path.basename(a.src):
        print("提示：源是 480p，竖版放大后会糊；上传前最好用 1080p 成片重新导出。")
    outdir = a.outdir or os.path.join(os.path.dirname(os.path.abspath(a.src)), "instagram")
    os.makedirs(outdir, exist_ok=True)
    lb = not a.no_letterbox
    if a.all_chapters:
        for s0, s1, ttl in chapters_from_project():
            export(a.src, s0, s1, a.title or ttl, a.format, outdir, a.cover, lb)
        return
    if a.chapter:
        s0, s1, ttl = chapters_from_project()[a.chapter - 1]
        export(a.src, s0, s1, a.title or ttl, a.format, outdir, a.cover, lb)
        return
    end = a.end if a.end is not None else duration(a.src)
    export(a.src, a.start, end, a.title, a.format, outdir, a.cover, lb)


if __name__ == "__main__":
    main()
