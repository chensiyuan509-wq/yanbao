#!/usr/bin/env python3
"""风格审计：把一部片和《星火》的"风格指纹"逐项对比，指出哪里偏了、往哪个方向改。

  python style_audit.py out/片名_480p.mp4          # 只测画面（任何视频都行）
  python style_audit.py out/片名_480p.mp4 --project .   # 在 aivid 项目里：再测分镜、字幕、字号、转场、Claude 出场、音效

指纹来自《星火》全片（480 帧画面 + 全部场景代码）的统计，目标区间是"保持同一风格"的合理范围，
不是要求数值一模一样。偏出区间的项会给出调整建议。
"""
import argparse
import json
import os
import re
import statistics as st
import subprocess
import sys

import numpy as np

# 《星火》实测（中位数，括号里为 10% / 90% 分位）
REF = dict(luma_mean=0.232, luma_p90=0.644, contrast=0.472, sat_mean=0.392, colorfulness=20.9, quiet_area=0.636,
           edge_density=0.062, luma_center_x=0.501, shot_median=4.6, vo_cps=7.0, vo_number_ratio=0.53,
           vo_per_min=15.6, text_min=16)

TARGET = [  # (键, 说明, 下限, 上限, 偏低时的建议, 偏高时的建议)
    ("luma_mean", "画面亮度（中位）", 0.14, 0.36, "整体太暗：穿插亮场——真实照片 / 油画 / 纸面（拜恩配色）图解，别全是深色底",
     "整体太亮：多用暗角、暗场和有方向的光，主体之外压暗"),
    ("luma_p90", "亮场亮度（90% 分位）", 0.45, 0.85, "缺少亮场：每 30–60 秒至少一个明亮的主视觉（纸面、照片、日光）", "亮场过曝，压一压高光"),
    ("contrast", "明暗对比（中位）", 0.30, 0.68, "画面发灰发平：主体加光、背景压暗、加暗角", "对比过硬，柔化高光或提一点暗部"),
    ("sat_mean", "饱和度（中位）", 0.22, 0.56, "颜色太淡：真实图像保留原色，强调色用金 / 拜恩红黄蓝", "颜色太艳：降饱和，统一调色"),
    ("quiet_area", "留白比例（中位）", 0.45, 0.92, "画面太满：一屏一个重点，面板 ≤ 4 行，标签 ≤ 6 个", "画面太空：加主视觉或缓慢运动的细节"),
    ("edge_density", "细节密度（中位）", 0.02, 0.12, "细节太少：主视觉要有可看的质感（照片、纹理）", "细节太碎：减少同时出现的小元素"),
    ("luma_center_x", "画面重心（0 左 1 右）", 0.42, 0.58, "重心偏左：右栏放面板 / 主体右移", "重心偏右：主视觉往左放，面板别太亮"),
    ("shot_median", "镜头时长中位（秒）", 3.0, 7.0, "切得太碎：一个镜头至少 3 秒，让观众看清", "镜头太长：超过 7 秒的拆成两三个镜头或加推拉"),
    ("vo_cps", "字幕速度中位（字/秒）", 3.5, 8.0, "字幕太稀：信息密度不够", "字幕太快：删字或拉开时间（≤ 8 字/秒）"),
    ("vo_number_ratio", "带数字的字幕比例", 0.35, 1.0, "数字太少：讲具体的年份、数量、对比", ""),
    ("vo_per_min", "每分钟字幕句数", 10, 20, "叙述太少，画面会空", "叙述太密，观众跟不上"),
    ("text_min", "画面最小字号（设计坐标）", 20, 999, "有字小于 20 号，480p 下看不清", ""),
    ("trans_kinds", "章内转场种类", 4, 99, "转场太单一：按画面内容选 luma / lightsweep / zoomblur / defocus / flare …", ""),
    ("trans_repeat", "相邻重复转场次数", 0, 2, "", "相邻两个转场用了同一种，换一种"),
    ("claude_missing", "没有 Claude 出场的章节数", 0, 0, "", "每章至少让 Claude 出场一次（参观者 / 扮演者 / 第一视角）"),
]


def frame_metrics(video, fps=1.0):
    try:
        import imageio_ffmpeg
        ff = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        ff = "ffmpeg"
    W, H = 854, 480
    lb = int(round(96 / 1080 * H))
    p = subprocess.Popen([ff, "-v", "error", "-i", video, "-vf", f"fps={fps},scale={W}:{H}", "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    rows = {k: [] for k in ("luma_mean", "luma_p90", "contrast", "sat_mean", "colorfulness", "quiet_area",
                            "edge_density", "luma_center_x")}
    n = W * H * 3
    while True:
        buf = p.stdout.read(n)
        if len(buf) < n:
            break
        f = np.frombuffer(buf, np.uint8).reshape(H, W, 3)[lb:H - lb].astype(np.float32) / 255
        R, G, B = f[..., 0], f[..., 1], f[..., 2]
        Y = 0.2126 * R + 0.7152 * G + 0.0722 * B
        mx, mn = f.max(-1), f.min(-1)
        S = np.where(mx > 1e-3, (mx - mn) / np.maximum(mx, 1e-3), 0)
        rg, yb = R - G, 0.5 * (R + G) - B
        gx = np.abs(np.diff(Y, axis=1))[:-1, :]
        gy = np.abs(np.diff(Y, axis=0))[:, :-1]
        h2, w2 = (Y.shape[0] // 16) * 16, (Y.shape[1] // 16) * 16
        blocks = Y[:h2, :w2].reshape(h2 // 16, 16, w2 // 16, 16).std((1, 3))
        xs = np.linspace(0, 1, Y.shape[1])
        rows["luma_mean"].append(Y.mean())
        rows["luma_p90"].append(Y.mean())
        rows["contrast"].append(np.percentile(Y, 95) - np.percentile(Y, 5))
        rows["sat_mean"].append(S.mean())
        rows["colorfulness"].append(255 * (np.hypot(rg.std(), yb.std()) + 0.3 * np.hypot(rg.mean(), yb.mean())))
        rows["quiet_area"].append((blocks < 0.02).mean())
        rows["edge_density"].append(((gx + gy) > 0.08).mean())
        rows["luma_center_x"].append((Y.sum(0) * xs).sum() / max(Y.sum(), 1e-6))
    p.wait()
    out = {k: float(np.median(v)) for k, v in rows.items() if v}
    if rows["luma_p90"]:
        out["luma_p90"] = float(np.percentile(rows["luma_p90"], 90))
    out["_frames"] = len(rows["luma_mean"])
    return out


def project_metrics(root):
    sys.path.insert(0, root)
    os.chdir(root)
    from aivid import narration
    from aivid.scenes import ORDER
    from aivid.timeline import DURATION, VO
    out = {}
    durs, kinds, repeats, missing = [], set(), 0, []
    sizes = []
    for m in ORDER:
        name = m.__name__.split(".")[-1]
        src = open(os.path.join(root, "aivid", "scenes", name + ".py"), encoding="utf-8").read()
        shots = getattr(m, "SHOTS", None)
        ts = ([s[0] for s in shots] if shots else [0.0]) + [m.DUR]
        durs += [b - a for a, b in zip(ts, ts[1:])]
        tr = getattr(m, "TRANS", {})
        seq = [tr[k][0] for k in sorted(tr)]
        kinds |= set(seq)
        repeats += sum(1 for a, b in zip(seq, seq[1:]) if a == b)
        if getattr(m, "CHAPTER", None) and not re.search(r"\b(claude|role)\(|pov_arm\(", src):
            missing.append(name)
        sizes += [int(x) for x in re.findall(r"\btext\(ctx, [^,]+, [^,]+, [^,]+, (\d+),", src)]
    out["shot_median"] = st.median(durs)
    out["trans_kinds"] = len(kinds)
    out["trans_repeat"] = repeats
    out["claude_missing"] = len(missing)
    out["_claude_missing_names"] = missing
    if sizes:                                   # 全部用 layout 组件时没有写死的字号，不检查
        out["text_min"] = min(sizes)
    cps = [len(narration.plain(L["text"])) / max(0.1, L["slot_end"] - L["start"]) for L in VO]
    out["vo_cps"] = st.median(cps) if cps else 0
    out["vo_number_ratio"] = sum(1 for L in VO if re.search(r"\d", L["text"])) / max(1, len(VO))
    out["vo_per_min"] = len(VO) / (DURATION / 60)
    return out


def main():
    ap = argparse.ArgumentParser(description="风格审计（对照《星火》指纹）")
    ap.add_argument("video", nargs="?")
    ap.add_argument("--project", default=None, help="aivid 项目目录（测分镜、字幕、字号、转场、Claude）")
    ap.add_argument("--fps", type=float, default=1.0)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    m = {}
    if a.video:
        m.update(frame_metrics(os.path.abspath(a.video), a.fps))
    if a.project:
        m.update(project_metrics(os.path.abspath(a.project)))
    if not m:
        sys.exit(__doc__)
    if a.json:
        print(json.dumps(m, ensure_ascii=False, indent=1))
        return
    bad = 0
    print(f"{'项目':<22}{'本片':>9}{'星火':>9}   目标区间")
    for key, label, lo, hi, low_tip, high_tip in TARGET:
        if key not in m:
            continue
        v = m[key]
        ok = lo <= v <= hi
        bad += not ok
        ref = REF.get(key, "")
        rs = f"{ref:.3g}" if isinstance(ref, float) else str(ref)
        print(f"{'✓' if ok else '!'} {label:<20}{v:>9.3g}{rs:>9}   {lo:g}–{hi:g}" if hi < 999 else
              f"{'✓' if ok else '!'} {label:<20}{v:>9.3g}{rs:>9}   ≥ {lo:g}")
        if not ok:
            print(f"    → {low_tip if v < lo else high_tip}")
    if m.get("_claude_missing_names"):
        print("    没有 Claude 的章节：" + "、".join(m["_claude_missing_names"]))
    if "_frames" in m:
        print(f"（画面抽样 {m['_frames']} 帧）")
    print("全部在区间内 ✓" if not bad else f"{bad} 项偏离星火风格，按建议调整后再测")


if __name__ == "__main__":
    main()
