#!/usr/bin/env python3
"""新建一个"星火风格"视频项目：复制引擎 + 素材库，按章节生成可直接渲染的场景骨架。

  python new_project.py ~/csy/ocean_video --title "深蓝：海洋探索简史" --slug shenlan --minutes 6 \\
      --chapters "第一次下海,大航海,深海热泉,今天的海洋" --keys "好奇,勇气,发现,守护" \\
      --eras "约 3000 年前,1405—1522 年,1977 年,今天"

  python new_project.py ~/csy/xinghuo_copy --example     # 复制完整的《星火》8 分钟示例（用于参考 / 回归测试）

生成后：
  cd <dest> && bash setup_env.sh            # 或复用已有的 venv（需要 pycairo、numpy、imageio-ffmpeg、Pillow）
  python check.py --quick                   # 骨架应当直接通过
  python render.py --still 5 30 60          # 看几帧
"""
import argparse
import os
import re
import shutil
import sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(SKILL, "engine")
TEMPLATES = os.path.join(SKILL, "templates")
EXAMPLE = os.path.join(SKILL, "examples", "xinghuo")

NUMS = "一二三四五六七八九十"
# 章与章之间的转场轮换（电影式；避免连续两次同一种）
CHAPTER_TRANS = [
    ('("flare", 1.4, {"x": 960, "y": 540, "sound": "swell", "gain": 0.35})', "强光过曝"),
    ('("lightsweep", 1.4, {"color": "#FFE2B0", "sound": "whoosh_short", "gain": 0.25})', "光带扫过"),
    ('("burn", 1.8, {"seed": 11, "sound": "ignite", "gain": 0.45})', "纸面燃烧"),
    ('("pages", 1.4, {"seed": 5, "sound": "pages_flurry", "gain": 0.5})', "书页飞过"),
    ('("smoke", 1.6, {"seed": 3, "sound": "steam", "gain": 0.45})', "蒸汽遮挡"),
    ('("flash", 1.0, {"sound": "crackle", "gain": 0.4})', "电光闪白"),
    ('("defocus", 1.6, {"max": 16, "sound": "hush", "gain": 0.3})', "虚焦"),
]
HALL_KEYS = ["lascaux_replica", "athens", "faraday_lecture", "qingming", "galileo", "coalbrookdale", "solvay",
             "earthrise", "maqamat_library", "eniac", "stonehenge", "tycho"]


def chinese_num(i):
    if i <= 10:
        return NUMS[i - 1]
    if i < 20:
        return "十" + NUMS[i - 11]
    return str(i)


def split_list(s, n, fill):
    items = [x.strip() for x in (s or "").split(",") if x.strip()] if s else []
    while len(items) < n:
        items.append(fill(len(items)))
    return items[:n]


def copy_engine(dest, link_assets):
    ign = shutil.ignore_patterns("__pycache__", "*.pyc")
    for name in ("aivid", "mascot", "tools"):
        shutil.copytree(os.path.join(ENGINE, name), os.path.join(dest, name), ignore=ign, dirs_exist_ok=True)
    for name in ("render.py", "check.py", "setup_env.sh", "requirements.txt"):
        shutil.copy2(os.path.join(ENGINE, name), os.path.join(dest, name))
    os.makedirs(os.path.join(dest, "assets"), exist_ok=True)
    shutil.copy2(os.path.join(ENGINE, "assets", "claude_reference.jpg"), os.path.join(dest, "assets", "claude_reference.jpg"))
    shutil.copytree(os.path.join(ENGINE, "assets", "geo"), os.path.join(dest, "assets", "geo"), dirs_exist_ok=True)
    arch = os.path.join(dest, "assets", "archive")
    if link_assets:
        if not os.path.exists(arch):
            os.symlink(os.path.join(ENGINE, "assets", "archive"), arch)
    else:
        shutil.copytree(os.path.join(ENGINE, "assets", "archive"), arch, dirs_exist_ok=True)
    with open(os.path.join(dest, ".gitignore"), "w") as f:
        f.write(".venv/\nout/\n__pycache__/\n*.pyc\n")


def write_project_py(dest, title, slug, target, chapters):
    with open(os.path.join(dest, "aivid", "project.py"), "w", encoding="utf-8") as f:
        f.write('"""项目配置：片名、输出文件名前缀、目标时长、章节数。"""\n')
        f.write(f"TITLE = {title!r}\nSLUG = {slug!r}\nTARGET_SEC = {float(target)!r}\nCHAPTERS = {chapters!r}\n")


def fill(tpl, **kw):
    s = open(os.path.join(TEMPLATES, tpl), encoding="utf-8").read()
    for k, v in kw.items():
        s = s.replace(f"__{k}__", str(v))
    left = re.findall(r"__[A-Z_]+__", s)
    if left:
        raise SystemExit(f"模板 {tpl} 还有没替换的占位符：{sorted(set(left))}")
    return s


def plan_durations(total, n_ch):
    pro = 18.0 if total >= 240 else 12.0
    epi = 26.0 if total >= 240 else 16.0
    rest = total - pro - epi
    if rest < n_ch * 20:
        raise SystemExit(f"时长不够：{total:.0f} 秒放不下 {n_ch} 章（每章至少 20 秒）")
    each = round(rest / n_ch / 0.2) * 0.2
    durs = [each] * n_ch
    durs[-1] = round(rest - each * (n_ch - 1), 3)
    return pro, durs, epi


def main():
    ap = argparse.ArgumentParser(description="新建星火风格视频项目")
    ap.add_argument("dest")
    ap.add_argument("--title", default="新片：副标题", help="完整片名，如 “星火：人类科学简史”")
    ap.add_argument("--short", default=None, help="片头片尾的大字短名（默认取片名冒号前）")
    ap.add_argument("--slug", default="video", help="输出文件名前缀（英文 / 拼音）")
    ap.add_argument("--minutes", type=float, default=8.0)
    ap.add_argument("--chapters", default="", help="逗号分隔的章节标题")
    ap.add_argument("--keys", default="", help="逗号分隔的每章关键词（两个字，如 观察、记录）")
    ap.add_argument("--eras", default="", help="逗号分隔的每章年代说明")
    ap.add_argument("--link-assets", action="store_true", help="素材库用软链接而不是复制（省 45 MB）")
    ap.add_argument("--example", action="store_true", help="复制完整的《星火》示例而不是生成骨架")
    ap.add_argument("--force", action="store_true", help="目标目录非空也继续")
    a = ap.parse_args()

    dest = os.path.abspath(os.path.expanduser(a.dest))
    if os.path.exists(dest) and os.listdir(dest) and not a.force:
        raise SystemExit(f"{dest} 不是空目录（确认要覆盖就加 --force）")
    os.makedirs(dest, exist_ok=True)
    copy_engine(dest, a.link_assets)
    scenes = os.path.join(dest, "aivid", "scenes")
    os.makedirs(scenes, exist_ok=True)

    if a.example:
        for fn in os.listdir(os.path.join(EXAMPLE, "scenes")):
            shutil.copy2(os.path.join(EXAMPLE, "scenes", fn), os.path.join(scenes, fn))
        write_project_py(dest, "星火：人类科学简史", "xinghuo", 480.0, 8)
        shutil.copy2(os.path.join(EXAMPLE, "README.md"), os.path.join(dest, "README.md"))
        print(f"已复制《星火》完整示例 → {dest}")
        return

    titles = [x.strip() for x in a.chapters.split(",") if x.strip()] or ["（第一章标题）", "（第二章标题）", "（第三章标题）"]
    n = len(titles)
    keys = split_list(a.keys, n, lambda i: "关键词")
    eras = split_list(a.eras, n, lambda i: "（年代）")
    total = a.minutes * 60
    pro, durs, epi = plan_durations(total, n)
    short = a.short or re.split(r"[：:]", a.title)[0]
    sub = a.title[len(short):].lstrip("：: ") or "（副标题）"

    names = ["s00_prologue"]
    with open(os.path.join(scenes, "s00_prologue.py"), "w", encoding="utf-8") as f:
        f.write(fill("prologue_template.py", DUR=pro, TITLE_SHORT=short, SUBTITLE=sub))
    for i, (ti, k, e, d) in enumerate(zip(titles, keys, eras, durs), 1):
        name = f"s{i:02d}_ch{i}"
        names.append(name)
        with open(os.path.join(scenes, name + ".py"), "w", encoding="utf-8") as f:
            f.write(fill("chapter_template.py", DUR=d, NUM=f"第 {' '.join(chinese_num(i))} 章", TITLE=ti, ERA=e, KEY=k,
                         SEED=float(20 + i), HALL_KEY=HALL_KEYS[(i - 1) % len(HALL_KEYS)]))
    epi_name = f"s{n + 1:02d}_epilogue"
    names.append(epi_name)
    with open(os.path.join(scenes, epi_name + ".py"), "w", encoding="utf-8") as f:
        f.write(fill("epilogue_template.py", DUR=epi, TITLE_SHORT=short))

    trans = []
    for j in range(len(names) - 1):
        if j == 0:
            trans.append(('("blink", 1.3, {"sound": "hush", "gain": 0.3})', "眨眼：序章 → 第一章"))
        elif j == len(names) - 2:
            trans.append(('("blink", 1.6, {"sound": "hush", "gain": 0.35, "double": False})', "眨眼：→ 尾声"))
        else:
            trans.append(CHAPTER_TRANS[(j - 1) % len(CHAPTER_TRANS)])
    with open(os.path.join(scenes, "__init__.py"), "w", encoding="utf-8") as f:
        f.write('"""场景顺序与章间转场（电影式：眨眼、强光、光带、燃烧、书页、蒸汽、闪白、虚焦——不用 PPT 翻页）。\n'
                '章内镜头之间的转场写在各章的 SHOTS / TRANS 里。"""\n')
        f.write(f"from . import {', '.join(names)}\n\n")
        f.write(f"ORDER = [{', '.join(names)}]\n\n")
        f.write("# (种类, 时长, 参数)；第 i 个转场位于 ORDER[i] 与 ORDER[i+1] 之间（以交界为中心）\nTRANSITIONS = [\n")
        for spec, note in trans:
            f.write(f"    {spec},  # {note}\n")
        f.write("]\n")
    write_project_py(dest, a.title, a.slug, total, n)
    with open(os.path.join(dest, "README.md"), "w", encoding="utf-8") as f:
        f.write(f"# {a.title}\n\n星火风格（skill: xinghuo-style-video）生成的视频项目。\n\n"
                f"| 场景 | 时长 |\n|---|---|\n| 序章 | {pro:g}s |\n")
        for ti, d in zip(titles, durs):
            f.write(f"| {ti} | {d:g}s |\n")
        f.write(f"| 尾声 | {epi:g}s |\n\n```bash\nbash setup_env.sh && source .venv/bin/activate\n"
                f"python check.py --quick\npython render.py            # → out/{a.slug}_480p.mp4\n```\n\n"
                "## 片中事实与说法\n\n| 说法 | 依据 |\n|---|---|\n\n## 图像来源\n\n见 assets/archive/CREDITS.md\n")
    print(f"新项目 → {dest}")
    print(f"  {n} 章，序章 {pro:g}s + 各章 {', '.join(f'{d:g}' for d in durs)}s + 尾声 {epi:g}s = {total:g}s")
    print("  下一步：cd 进去 → bash setup_env.sh → python check.py --quick → python render.py --still 5 40")


if __name__ == "__main__":
    sys.exit(main())
