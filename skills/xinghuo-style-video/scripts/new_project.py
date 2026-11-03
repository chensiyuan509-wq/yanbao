#!/usr/bin/env python3
"""新建一个视频项目：复制引擎（aivid + mascot + render/check + 工具 + 地图数据 + 已授权素材），
再按你给的分段生成**可运行的空白占位场景**——内容、镜头、转场都由这部片自己设计，不套用任何旧片。

  python new_project.py ~/csy/ocean_video --title "深蓝：海洋探索简史" --slug shenlan --minutes 6 \\
      --sections "第一次下海,大航海,深海热泉,今天的海洋" [--chapter-cards] [--keys "好奇,勇气,发现,守护"] \\
      [--eras "约 3000 年前,1405—1522 年,1977 年,今天"] [--no-prologue] [--no-epilogue]

  python new_project.py ~/csy/xinghuo_ref --example     # 复制完整的《星火》作参考 / 回归测试（不要当模板改）

  --chapter-cards   每段开头显示电影字卡（"第 N 章 标题"）；不加就没有字卡，适合不分章的片子
  --link-assets     素材库用软链接而不是复制（省 45 MB）
生成后：cd <目录> && bash setup_env.sh（或复用已有 venv）→ python check.py --quick
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


def chinese_num(i):
    if i <= 10:
        return NUMS[i - 1]
    return "十" + NUMS[i - 11] if i < 20 else str(i)


def items(s, n, fill):
    out = [x.strip() for x in (s or "").split(",") if x.strip()]
    return (out + [fill] * n)[:n]


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
        f.write('"""项目配置：片名、输出文件名前缀、目标时长、章节字卡数。"""\n')
        f.write(f"TITLE = {title!r}\nSLUG = {slug!r}\nTARGET_SEC = {float(target)!r}\nCHAPTERS = {chapters!r}\n")


def stub(label, title, dur, chapter):
    s = open(os.path.join(TEMPLATES, "stub_template.py"), encoding="utf-8").read()
    for k, v in (("LABEL", label), ("TITLE", title), ("DUR", dur), ("CHAPTER", chapter)):
        s = s.replace(f"__{k}__", str(v))
    left = re.findall(r"__[A-Z]+__", s)
    assert not left, left
    return s


def main():
    ap = argparse.ArgumentParser(description="新建视频项目（引擎 + 空白占位分镜）")
    ap.add_argument("dest")
    ap.add_argument("--title", default="（片名）")
    ap.add_argument("--slug", default="video", help="输出文件名前缀（英文 / 拼音）")
    ap.add_argument("--minutes", type=float, default=5.0)
    ap.add_argument("--sections", "--chapters", dest="sections", default="", help="逗号分隔的段落 / 章节名")
    ap.add_argument("--chapter-cards", action="store_true", help="每段开头显示章节字卡")
    ap.add_argument("--keys", default="", help="逗号分隔，字卡下的关键词（可选）")
    ap.add_argument("--eras", default="", help="逗号分隔，字卡下的年代 / 副标题（可选）")
    ap.add_argument("--no-prologue", action="store_true")
    ap.add_argument("--no-epilogue", action="store_true")
    ap.add_argument("--link-assets", action="store_true")
    ap.add_argument("--example", action="store_true", help="复制完整的《星火》作参考")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    dest = os.path.abspath(os.path.expanduser(a.dest))
    if os.path.exists(dest) and os.listdir(dest) and not a.force:
        raise SystemExit(f"{dest} 不是空目录（确认要覆盖就加 --force）")
    os.makedirs(dest, exist_ok=True)
    copy_engine(dest, a.link_assets)
    scenes = os.path.join(dest, "aivid", "scenes")

    if a.example:
        for fn in os.listdir(os.path.join(EXAMPLE, "scenes")):
            shutil.copy2(os.path.join(EXAMPLE, "scenes", fn), os.path.join(scenes, fn))
        write_project_py(dest, "星火：人类科学简史", "xinghuo", 480.0, 8)
        shutil.copy2(os.path.join(EXAMPLE, "README.md"), os.path.join(dest, "README.md"))
        print(f"已复制《星火》完整示例 → {dest}（参考用）")
        return

    names = [x.strip() for x in a.sections.split(",") if x.strip()] or ["（第一段）", "（第二段）", "（第三段）"]
    n = len(names)
    keys, eras = items(a.keys, n, ""), items(a.eras, n, "")
    total = a.minutes * 60
    pro = 0.0 if a.no_prologue else (15.0 if total >= 240 else 10.0)
    epi = 0.0 if a.no_epilogue else (20.0 if total >= 240 else 12.0)
    rest = total - pro - epi
    if rest < n * 15:
        raise SystemExit(f"时长不够：{total:.0f} 秒放不下 {n} 段（每段至少 15 秒）")
    each = round(rest / n / 0.2) * 0.2
    durs = [each] * (n - 1) + [round(rest - each * (n - 1), 3)]

    mods = []
    if pro:
        mods.append(("s00_open", stub("开场", "开场", pro, "None")))
    for i, (nm, d, k, e) in enumerate(zip(names, durs, keys, eras), 1):
        ch = (f'dict(num="第 {" ".join(chinese_num(i))} 章", title={nm!r}, era={e!r}, key={k!r}, at=0.4, dur=4.0)'
              if a.chapter_cards else "None")
        mods.append((f"s{i:02d}_part{i}", stub(f"第 {i} 段", nm, d, ch)))
    if epi:
        mods.append((f"s{n + 1:02d}_close", stub("结尾", "结尾", epi, "None")))
    for name, src in mods:
        with open(os.path.join(scenes, name + ".py"), "w", encoding="utf-8") as f:
            f.write(src)
    order = [m[0] for m in mods]
    with open(os.path.join(scenes, "__init__.py"), "w", encoding="utf-8") as f:
        f.write('"""场景顺序与段间转场。\n\n占位转场都是溶解；设计分镜时按内容换成有理由的电影式转场'
                '（见 references/camera-and-transitions.md），相邻不要重复。\n"""\n')
        f.write(f"from . import {', '.join(order)}\n\nORDER = [{', '.join(order)}]\n\n")
        f.write("# (种类, 时长, 参数)；第 i 个转场位于 ORDER[i] 与 ORDER[i+1] 之间（以交界为中心）\nTRANSITIONS = [\n")
        f.write("".join('    ("dissolve", 1.2, {}),\n' for _ in range(len(order) - 1)))
        f.write("]\n")
    write_project_py(dest, a.title, a.slug, total, n if a.chapter_cards else 0)
    with open(os.path.join(dest, "README.md"), "w", encoding="utf-8") as f:
        f.write(f"# {a.title}\n\n## 分镜（先设计再写代码）\n\n| 时间 | 段落 | 讲什么 | 画面与运镜 | 素材 |\n|---|---|---|---|---|\n")
        acc = 0.0
        for nm, d in ([("开场", pro)] if pro else []) + list(zip(names, durs)) + ([("结尾", epi)] if epi else []):
            f.write(f"| {int(acc // 60)}:{int(acc % 60):02d} | {nm} |  |  |  |\n")
            acc += d
        f.write("\n## 片中事实与说法\n\n| 说法 | 依据 |\n|---|---|\n\n## 图像来源\n\n见 assets/archive/CREDITS.md\n\n"
                f"```bash\npython check.py --quick\npython render.py            # → out/{a.slug}_480p.mp4\n```\n")
    print(f"新项目 → {dest}")
    print(f"  {len(order)} 个场景：{', '.join(f'{m}' for m in order)}；合计 {total:g} 秒")
    print("  这些只是占位。下一步：按 SKILL.md 先写分镜设计，再逐段实现。")


if __name__ == "__main__":
    sys.exit(main())
