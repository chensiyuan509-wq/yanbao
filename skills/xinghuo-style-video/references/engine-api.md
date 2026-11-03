# 引擎 API 与踩过的坑

纯 Python：pycairo 逐帧画 1920×1080 设计坐标 → 缩放到输出分辨率 → 胶片颗粒 → 遮幅 → 字幕 → ffmpeg 分段编码 → 混入合成音轨。

## 目录
1. 项目结构
2. 场景模块约定
3. 常用函数速查
4. 渲染与检查命令
5. 坑（一定要看）

---

## 1. 项目结构

```
render.py  check.py  setup_env.sh  requirements.txt
aivid/project.py      片名、SLUG、目标时长、章节数
aivid/core.py         缓动、颜色、图形、文字（FONTS）、镜头 Cam / view
aivid/film.py         颗粒、遮幅、调色、暗角、光、火、烟、星空、月相、纹理、第一视角
aivid/archive.py      历史图像：show / kb / framed / caption（多级缓存）
aivid/gallery.py      博物馆长廊 Gallery
aivid/exhibit.py      card / panel / blueprint_bg
aivid/proofs.py       Byrne 风格证明
aivid/oldmap.py       Natural Earth + 卫星地图、MapCam、城市、航线
aivid/starmap.py      《星火》专用的手形知识星图（新片可删或改 STARS）
aivid/transitions.py  composite(kind, …) 所有转场
aivid/timeline.py     场景拼接、字幕、章节字卡、SUPERS、SRT
aivid/narration.py    字幕切分与朗读时长估算
aivid/audio.py + sfx_hist.py   音效合成、混音、响度
aivid/scenes/         __init__.py（ORDER + TRANSITIONS）+ 各场景 + common.py
mascot/               Claude 角色库
tools/fetch_assets.py  tools/prepare_geo.py
assets/archive/  assets/geo/  assets/claude_reference.jpg
```

## 2. 场景模块约定

```python
DUR = 66.0                                   # 场景时长（秒）；全片 = 各场景 DUR 之和
CHAPTER = dict(num="第 七 章", title="看不见的世界", era="1895 — 1969 年", key="协作", at=0.4, dur=4.0)  # 或 None
GRAIN = 0.07
VO = [(本地秒, "字幕{高亮}"), …]
SUPERS = [(t0, t1, "年份", "地点 · 事件"), …]
SHOTS = [(0.0, _s1), (8.5, _s2), …]           # 镜头开始时间 + 绘制函数 fn(ctx, t)
TRANS = {1: ("dissolve", 0.9), 2: ("lightsweep", 0.9, {"color": "#BFE0FF"}), …}   # 第 j 个镜头开始时的转场
def draw(ctx, t): sequence(ctx, t, SHOTS, TRANS)
def sfx(): return [(t, "音效名", {参数}), …]
```
`t` 是场景内本地时间，转场时可能略小于 0 或略大于 DUR。镜头函数里用 `u = t - 镜头开始` 计算局部进度。

## 3. 常用函数速查

- 缓动：`prog(t, t0, t1)`（0..1 截断）、`smooth`、`ease_io`、`ease_out`、`ease_in`、`lerp`、`clamp`、`kf(t, keys)`
- 图形：`rrect` `circle` `ellipse` `poly` `glow(ctx, x, y, r, color, a)` `stroke_pts(ctx, pts, w, color, a, dash=)`
  `polyline_partial(pts, p)`（描线动画）`dashed` `arrow` `star4` `check_mark` `ring_burst`
- 文字：`text(ctx, s, x, y, size, color, a, font, align)`、`label(...)`（带投影，可加 sub）、`film.tracked(...)`（字距拉开）
- 颜色：`setc(ctx, c, a)` `lin(x0,y0,x1,y1,[(pos,c,a)])` `rad(x,y,r0,r1,[…])` `mix(c1,c2,t)`
- 电影：`film.vignette` `film.grade(ctx, color, a)` `film.fade_black(ctx, a)` `film.star_field` `film.embers`
  `film.fire(ctx, x, y, size, t, a, seed, glow_a)` `film.logs(ctx, x, y, size)` `film.sun` `film.moon(phase)` `film.beams`
  `film.dust` `film.smoke_puffs` `film.paint_texture(ctx, "parchment|clay|stone|paper", x, y, w, h, a)` `film.pov_arm` `film.eyelids`
- 档案：`kb` `arch` `framed` `show(…, grade=, fit=)` `caption`
- 展示：`card` `panel` `blueprint_bg` `Gallery`
- 地图：`MapCam(keys).at(t)` `cam.xy(lon, lat)` `draw_satellite` `sat_vignette` `city_sat` `route` `river_lines`
- 角色：`claude()` `role()` `lit()` `reflect()`

## 4. 渲染与检查

```bash
python check.py --quick                 # 时长、字幕速度、缺字、音效名、抽样渲染（每次改完都跑）
python check.py --audio                 # 再查响度
python render.py --still 12 95.5 230    # 导出指定秒的 PNG → out/stills/（全片时间）
python render.py --sheet 5              # 每 5 秒一帧的联系表
python render.py --start 128 --end 182  # 只渲染一段
python render.py                        # 完整 480p → out/<SLUG>_480p.mp4（8 分钟约 2.5 分钟，8 核）
python render.py --res 720 / 1080
python render.py --grain 0 --out out/<SLUG>_480p_nograin.mp4   # 邮件版的源（交给 gmail-send 压缩发送）
```
全片时间 = 场景起点 + 本地时间；起点用 `python -c "from aivid.timeline import STARTS, NAMES; print(list(zip(NAMES, STARTS)))"` 查。

## 5. 坑

- **zsh**：命令里别写裸的 `*.png` 通配（没匹配时整条命令失败）；把一串数字传给 `--still` 要用 `${=S}` 分词。
- **字形**：`″ ✓ ≈ − ₀ ∇` 在宋体 / Noto Serif 里可能缺 → 用 `eq` 字体；`eq` 里放中文会缺 → 拆开画。打勾直接画线。
- **Python 字符串**：中文文案里的引号用 “ ” 或 ‘ ’，别用半角 `"`（会提前结束字符串）。
- **sequence 转场窗口**：两个镜头会用同一个 t 各画一遍；别在镜头里用会因负数出错的写法。
- **Gallery 推进**：结束时画心 = 铺满 × 1.02，画框中心已移到画面正中；下一镜 `kb` 从 `(0.5, 0.5, 1.02)` 开始才能无缝。
  `lead` 控制开场时镜头离第一幅画多远（给章节字卡留空墙）；`t0` 之前镜头不动。
- **章节字卡与画框重叠**：画面右侧有主体时用 `CHAPTER["x"] = 620`，并让镜头在字卡消失（at+dur）之后再推。
- **卫星夜景**：k < 6.5 会露出两极外的黑带；纬度上界超出 90° 的部分要藏在上黑边里。
- **kb 是 cover 模式**：竖图放进横框会被裁很多，竖图优先用 `rect` 放半边或 `framed`。
- **低分辨率原图**（如 `tiangong_paper` 357×510、`medicean`）：只做画框小图，不要全屏。
- **邮件版**：颗粒在低码率下会糊，先 `--grain 0` 再压。
- **长任务**：完整渲染放后台跑（几分钟），别在前台等；渲染时别同时跑别的重活。
