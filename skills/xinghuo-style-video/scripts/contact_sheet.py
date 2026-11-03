#!/usr/bin/env python3
"""预览联系表：检查构图、文字是否压图、有无缺字方块、转场是否突兀。

  python contact_sheet.py out.jpg a.png b.png ...            # 把若干张图拼成 3 列
  python contact_sheet.py out.jpg --video film.mp4 --every 16  # 从成片每 16 秒抽一帧，5 列，左上角标时间
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw


def tile(out, files, cols=3, tw=640, th=360, labels=None):
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (tw * cols, th * rows), "black")
    for i, f in enumerate(files):
        im = Image.open(f).convert("RGB").resize((tw, th), Image.LANCZOS)
        ImageDraw.Draw(im).text((6, 4), labels[i] if labels else os.path.basename(f), fill=(255, 255, 0))
        sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
    sheet.save(out, quality=88)
    print(out)


def from_video(out, video, every):
    import shutil
    try:
        import imageio_ffmpeg
        ff = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        ff = shutil.which("ffmpeg")
    if not ff:
        sys.exit("找不到 ffmpeg：请用项目 venv 的 python 运行（里面有 imageio-ffmpeg），或安装系统 ffmpeg")
    d = tempfile.mkdtemp()
    vf = f"select='isnan(prev_selected_t)+gte(t-prev_selected_t,{every})',scale=640:-1"
    base = [ff, "-hide_banner", "-loglevel", "error", "-i", video, "-vf", vf]
    pattern = os.path.join(d, "f%03d.jpg")
    if subprocess.run(base + ["-fps_mode", "vfr", pattern]).returncode != 0:      # ffmpeg ≥ 5.1
        subprocess.run(base + ["-vsync", "vfr", pattern], check=True)             # 旧版 ffmpeg
    files = sorted(os.path.join(d, f) for f in os.listdir(d))
    labels = [f"{int(i * every) // 60}:{int(i * every) % 60:02d}" for i in range(len(files))]
    tile(out, files, cols=5, tw=384, th=216, labels=labels)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    if sys.argv[2] == "--video":
        every = float(sys.argv[sys.argv.index("--every") + 1]) if "--every" in sys.argv else 16
        from_video(sys.argv[1], sys.argv[3], every)
    else:
        tile(sys.argv[1], sys.argv[2:])
