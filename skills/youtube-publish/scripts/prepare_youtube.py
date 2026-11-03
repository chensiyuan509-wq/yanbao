#!/usr/bin/env python3
"""准备 YouTube 上传物料（不联网、不上传）。在视频项目目录里、用项目 venv 的 python 运行：

  python prepare_youtube.py [--video out/<slug>_1080p.mp4] [--thumb 15.6] [--tags "科学史,科普,Claude"]
                            [--category 27] [--privacy private] [--summary "一两句简介"]

输出 out/youtube/：
  metadata.json     上传脚本读取的全部信息（标题、简介、标签、分类、语言、隐私、文件路径）
  description.txt   简介全文（章节时间戳 + 图像署名），也可以手动贴进 YouTube Studio
  captions.srt      字幕（画面里已烧录中文字幕；这份可另传为 CC 字幕）
  thumbnail.jpg     1280×720 封面
并检查 YouTube 的硬性规则：标题 ≤ 100 字符、简介 ≤ 5000 字节、标题 / 简介里不能有 < >、标签合计 ≤ 500 字符、
章节（第一条 00:00、至少 3 条、每段 ≥ 10 秒）、封面 ≤ 2 MB。
"""
import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.getcwd()
sys.path.insert(0, ROOT)


def mmss(t):
    t = int(round(t))
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60:02d}:{t % 60:02d}"


def chapter_lines(ORDER, STARTS):
    rows = []
    for i, m in enumerate(ORDER):
        ch = getattr(m, "CHAPTER", None)
        if ch:
            rows.append((STARTS[i], f"{ch['num'].replace(' ', '')} {ch['title']}"))
        elif i == 0:
            rows.append((0.0, "序章"))
        elif i == len(ORDER) - 1:
            rows.append((STARTS[i], "尾声"))
    return rows


def used_cc_by(scenes_dir):
    """扫描场景源码里出现的素材键，列出其中 CC BY 授权的（简介里需要署名）。"""
    cpath = os.path.join(ROOT, "assets", "archive", "credits.json")
    if not os.path.exists(cpath):
        return []
    credits = json.load(open(cpath, encoding="utf-8"))
    src = ""
    for fn in os.listdir(scenes_dir):
        if fn.endswith(".py"):
            src += open(os.path.join(scenes_dir, fn), encoding="utf-8").read()
    out = []
    for k, m in credits.items():
        if re.search(rf'"{re.escape(k)}"', src) and re.search(r"cc[ -]by", m.get("license", ""), re.I):
            out.append(f"· {m['title']} — {m.get('artist') or '佚名'}（{m['license']}）")
    return out


def project_info():
    """新引擎有 aivid/project.py；老项目没有时，片名取 README 的一级标题，文件名前缀从 out/*_<分辨率>p.mp4 推断。"""
    try:
        from aivid import project
        return project.TITLE, project.SLUG
    except ImportError:
        title, slug = None, None
        readme = os.path.join(ROOT, "README.md")
        if os.path.exists(readme):
            for line in open(readme, encoding="utf-8"):
                if line.startswith("# "):
                    title = line[2:].strip().replace(" · ", "：")
                    break
        outdir = os.path.join(ROOT, "out")
        for fn in sorted(os.listdir(outdir)) if os.path.isdir(outdir) else []:
            m = re.match(r"(.+?)_(1080|720|480)p\.mp4$", fn)
            if m:
                slug = m.group(1)
                break
        return title or os.path.basename(ROOT), slug or os.path.basename(ROOT)


def main():
    TITLE, SLUG = project_info()
    from aivid.timeline import DURATION, ORDER, STARTS, srt_text
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", default=None)
    ap.add_argument("--thumb", type=float, default=None, help="封面取全片第几秒（默认 15.6 或片长的 3%%）")
    ap.add_argument("--title", default=None, help="默认用 aivid/project.py 的 TITLE")
    ap.add_argument("--summary", default="", help="简介开头的一两句话")
    ap.add_argument("--tags", default="科普,历史,科学史,纪录片,动画,Claude")
    ap.add_argument("--category", default="27", help="27 教育；28 科学与技术")
    ap.add_argument("--language", default="zh-Hans")
    ap.add_argument("--privacy", default="private", choices=["private", "unlisted", "public"])
    a = ap.parse_args()

    out = os.path.join(ROOT, "out", "youtube")
    os.makedirs(out, exist_ok=True)
    problems = []

    video = a.video
    if not video:
        for r in (1080, 720, 480):
            c = os.path.join(ROOT, "out", f"{SLUG}_{r}p.mp4")
            if os.path.exists(c):
                video = c
                break
    if not video or not os.path.exists(video):
        problems.append("没有找到成片：先在项目里 python render.py --res 1080")
    elif "_1080p" not in video:
        print(f"提示：{os.path.basename(video)} 不是 1080p，YouTube 上会显得模糊；建议 python render.py --res 1080")

    title = (a.title or TITLE).strip()
    if len(title) > 100:
        problems.append(f"标题 {len(title)} 字符，超过 100")
    rows = chapter_lines(ORDER, STARTS)
    if len(rows) < 3 or rows[0][0] != 0:
        problems.append("章节不足 3 条或第一条不是 00:00，YouTube 不会显示章节")
    for (t0, _), (t1, nm) in zip(rows, rows[1:] + [(DURATION, "")]):
        if t1 - t0 < 10:
            problems.append(f"章节 {mmss(t0)} 不足 10 秒")
    desc = []
    if a.summary:
        desc += [a.summary, ""]
    desc += [f"{mmss(t)} {nm}" for t, nm in rows]
    desc += ["", "历史图像来自 Wikimedia Commons（公有领域 / CC0 / CC BY），每张在片中左下角标注出处。"]
    cc = used_cc_by(os.path.join(ROOT, "aivid", "scenes"))
    if cc:
        desc += ["CC BY 授权图像：", *cc]
    desc += ["地图：Natural Earth；NASA Blue Marble / Earth's City Lights。", "本片无背景音乐，音效均为程序合成。"]
    description = "\n".join(desc)
    if len(description.encode("utf-8")) > 5000:
        problems.append(f"简介 {len(description.encode('utf-8'))} 字节，超过 5000")
    if re.search(r"[<>]", title + description):
        problems.append("标题或简介里有 < 或 >，YouTube 不允许")
    tags = [t.strip() for t in a.tags.split(",") if t.strip()]
    if sum(len(t) + (2 if " " in t else 0) for t in tags) + len(tags) - 1 > 500:
        problems.append("标签合计超过 500 字符")

    open(os.path.join(out, "description.txt"), "w", encoding="utf-8").write(description + "\n")
    open(os.path.join(out, "captions.srt"), "w", encoding="utf-8").write(srt_text())

    thumb_t = a.thumb if a.thumb is not None else min(15.6, DURATION * 0.03 + 2)
    subprocess.run([sys.executable, "render.py", "--still", str(thumb_t), "--res", "720"], check=True,
                   stdout=subprocess.DEVNULL)
    from PIL import Image
    png = os.path.join(ROOT, "out", "stills", f"t{thumb_t:06.2f}.png")
    thumb = os.path.join(out, "thumbnail.jpg")
    Image.open(png).convert("RGB").save(thumb, quality=90)
    if os.path.getsize(thumb) > 2 * 1024 * 1024:
        problems.append("封面超过 2 MB")

    meta = {
        "video": os.path.abspath(video) if video else None,
        "thumbnail": os.path.abspath(thumb),
        "captions": {"file": os.path.abspath(os.path.join(out, "captions.srt")), "language": a.language, "name": "中文"},
        "snippet": {"title": title, "description": description, "tags": tags, "categoryId": a.category,
                    "defaultLanguage": a.language, "defaultAudioLanguage": a.language},
        "status": {"privacyStatus": a.privacy, "selfDeclaredMadeForKids": False, "embeddable": True,
                   "license": "youtube"},
    }
    json.dump(meta, open(os.path.join(out, "metadata.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"→ {out}")
    print(f"  标题：{title}")
    print(f"  隐私：{a.privacy}  分类：{a.category}  标签：{', '.join(tags)}")
    print("  章节：" + " | ".join(f"{mmss(t)} {nm}" for t, nm in rows))
    if problems:
        print("✗ 需要处理：\n  - " + "\n  - ".join(problems))
        sys.exit(1)
    print("✓ 物料齐全，符合 YouTube 的硬性限制（尚未上传）")


if __name__ == "__main__":
    main()
