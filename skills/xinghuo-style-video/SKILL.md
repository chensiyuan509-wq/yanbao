---
name: xinghuo-style-video
description: 用 Python/pycairo 代码生成"星火风格"的电影感科普 / 历史视频（发 YouTube 正片和 Instagram Reels 竖版）：真实历史图像（壁画、手稿、版画、老照片、NASA 影像）做 Ken Burns 推拉，博物馆长廊推镜，蓝图原理图，展品卡片，卫星地图，Byrne 风格证明，换装扮演历史人物的 Claude 角色，电影式转场，无背景音乐只有合成音效，遮幅 + 胶片颗粒 + 字幕。只要用户想做（或改）一个由代码生成的讲解视频、科普动画、历史 / 科学 / 技术 / 人物 / 发明 / 文明主题的短片，提到"YouTube""ins / Instagram""Reels""Shorts""做个视频""8 分钟视频""Claude 形象""像星火那样""电影感""纪录片风格""历史感""运镜转场""渲染 MP4"，或者要在 science_history_video / ai_relay_video 这类项目上继续做，都应使用本技能——即使用户没说"星火"两个字。Use for any code-generated cinematic explainer / documentary-style video with the Claude mascot.
---

# 星火风格视频

这套风格来自《星火：人类科学简史》（8 分钟，480p，`/home/wei/csy/science_history_video`）。用户对它的评价是
"非常非常好""无敌了"，特别喜欢：**史前壁画、法拉第讲座这类重要历史画面的插图风格**、厚重的历史感和氛围感、
运镜与转场的审美、叙事手段、信息密度与画面帧、**只有音效没有背景音乐**、Claude 的动作表情、素材与构图方式。
以后的视频都按这个标准做。本技能把它固定成：一个可复制的引擎 + 89 张已授权的历史图像 + 场景模板 + 一套审美规则。

## 什么时候读哪份参考

| 要做的事 | 读 |
|---|---|
| 定画面：颜色、字体、版式、时代调色、十三种构图 | `references/style-bible.md` |
| 定运镜和转场（章间 / 章内，各用在哪） | `references/camera-and-transitions.md` |
| 写分镜和字幕、控制信息密度、讲证明 / 原理 | `references/narrative-and-density.md` |
| 配音效（三层结构、场景对照表、检查静音） | `references/sound-design.md` |
| 找图、核对授权、看现有 89 张图各适合干什么 | `references/archive-library.md` |
| Claude 怎么出场、表情 / 动作 / 服装 / 道具 | `references/claude-character.md` |
| 函数签名、场景模块约定、渲染命令、**踩过的坑** | `references/engine-api.md` |
| 发布：Instagram 竖版 Reels 怎么切；YouTube / 邮件交给哪个技能 | `references/publishing.md` |
| 看完整实现（每种构图都有现成代码） | `examples/xinghuo/scenes/*.py` 和 `examples/xinghuo/README.md` |

开工前至少读 style-bible、camera-and-transitions、narrative-and-density 三份；写到具体镜头时再翻对应示例。

## 默认规格（用户没另说就照此）

- 30fps；预览默认 **480p**（854×480）；**上传 YouTube / Instagram 用 1080p**（`--res 1080`）；H.264 + AAC，`+faststart`。
- 发布平台是 **YouTube（16:9 正片）和 Instagram（9:16 竖版 Reels）**，不是 B 站或视频号。
- 2.2:1 遮幅黑边，字幕烧在下黑边里，另出 SRT；胶片颗粒 0.07、暗角。
- **没有人声旁白、没有背景音乐**，只有音效和环境声，响度 −16 LUFS。
- Claude 第一人称（"我"），叫它 Claude（不叫"小橙"）。
- 画面里的历史图像只用公有领域 / CC0 / CC BY，每张标出处。

## 工作流程

### 1. 定题与大纲
- 弄清主题、时长、受众、分辨率。时长按"序章 12–18 秒 + 每章 40–70 秒 + 尾声 16–26 秒"分配。
- 列章节：每章一个两字**关键词**（尾声收拢它们），每章写 5–6 个节拍：开场图 → 人 / 时 / 地 → **怎么做到 / 怎么证明** → 数字 → **应用落地** → 交棒。
- 事实先查清（WebSearch），数字、年份、引语都要有出处；不确定的写"约 / 一说 / 常被认为"。

### 2. 建项目
```bash
python ~/.claude/skills/xinghuo-style-video/scripts/new_project.py <目标目录> --title "片名：副标题" --slug <拼音> \
    --minutes 8 --chapters "章1,章2,…" --keys "观察,记录,…" --eras "年代1,年代2,…"
cd <目标目录> && bash setup_env.sh        # 或复用现有 venv：/home/wei/csy/ai_relay_video/.venv/bin/python
python check.py --quick                   # 骨架应直接通过
```
生成的每章骨架已经演示了五种常用构图（展厅推镜 → 档案推拉 + 面板 → 蓝图原理 → 展品卡片 → 卫星地图），
带好了 SHOTS / TRANS / sfx。要对照完整成片时用 `--example` 复制整部《星火》。

### 3. 找素材
先在 `references/archive-library.md` 的清单里找现成的；不够就用 `scripts/commons_search.py` 搜 Wikimedia Commons，
登记到项目的 `tools/fetch_assets.py` 再下载。**新图先拼联系表看一眼内容对不对**，再定裁切。没有可用授权的真图时，
画示意图并注明"示意"，不要编造"历史图像"。

### 4. 逐章写场景
- 一个镜头 3–6 秒，一章 8–14 个镜头；镜头函数挂在 `SHOTS`，镜头间转场写 `TRANS`（相邻不重复，一章至少三种）。
- 每个镜头：一个主视觉（真实图像或动画）+ 最多一个信息面板（3–4 行）+ 出处字幕；留白 ≥ 40%。
- 画面永远在缓慢运动（推拉、横移、地图飞行），元素淡入上浮，不弹跳、不飞入。
- Claude 每章至少出场一次（参观者 / 扮演者 / 第一视角），用 `lit()` 染上场景光。
- 字幕一句一个事实、带数字，≤ 8 字 / 秒；`{}` 高亮一个关键词。
- 音效三层：环境底不断（不留静音）、动作音对齐画面、重音留给大事件。

### 5. 自查（每章写完都做）
```bash
python check.py --quick
python render.py --still <这一章里 12–18 个关键时间点>
python ~/.claude/skills/xinghuo-style-video/scripts/contact_sheet.py sheet.jpg out/stills/t*.png
```
用 Read 看联系表，逐张找：文字压到主体 / 人脸、字卡和画框重叠、缺字方块、被黑边切掉的标题、画面空洞或太挤、
转场前后跳动、Claude 被字幕或面板挡住。发现就改，改完再出图确认。

### 6. 成片与交付
- 完整渲染放后台：`python render.py`（8 分钟约 2–3 分钟）。完成后：
  - 查静音：`ffmpeg -i out/soundtrack.wav -af silencedetect=noise=-50dB:d=0.8 -f null -` 无输出；响度约 −16 LUFS。
  - 出全片联系表：`contact_sheet.py sheet.jpg --video out/<slug>_480p.mp4 --every 16`，最后看一遍整体。
- 更新项目 README：分镜表、"片中事实与说法"（说法 | 依据）、图像来源。
- 发布物料（见 `references/publishing.md`）：`python render.py --res 1080` 出上传版；
  `scripts/export_reels.py --chapter N` 出 Instagram 竖版片段；YouTube 的上传物料与上传交给 **youtube-publish** 技能。
- 发到邮箱看效果交给 **gmail-send** 技能（先 `python render.py --grain 0` 出无颗粒版，它会压到 25 MB 以内再发）。
  **提交 git、推送、发邮件、上传 YouTube 都只在用户要求时做。**

## 质量线（用户明确否定过的东西）

第一版《星火》被打回过，原因是：人物成了火柴人；信息密度低，几何原本一笔带过；背景不好看、没有壁画的厚重感；
蒸汽机介绍简陋；世界地图像手绘草图；电气时代画面简陋、没有讲清电气革命的产物；相对论没讲怎么被证明、有什么应用；
整体可观赏性低。所以：
- 人物 = 真实肖像 / 照片，或换装的 Claude；**绝不用火柴人**。
- 科技内容必须具体：原理（蓝图动画）+ 证明（实验 / 推导）+ 数字 + 应用落地 + 真实器物照片。
- 地图 = 卫星影像 + 真实地理数据。
- 信息多但不挤：一屏一个重点，布局均匀。
- 运镜流畅，转场多样且有理由，像电影不像 PPT。

## 资源

- `engine/`：引擎快照（aivid、mascot、render.py、check.py、tools、assets）。新项目由 `new_project.py` 复制，**不要直接在这里改**；
  若在某个项目里改进了引擎（新转场、新构图、新音效），确认稳定后同步回 `engine/`，并在对应参考文档里补一行。
- `templates/`：序章、章节、尾声模板（`__占位符__` 由脚手架替换）。
- `examples/xinghuo/`：《星火》全部 10 个场景源码 + README（分镜、事实出处表）。
- `scripts/`：`new_project.py` 建项目、`commons_search.py` 搜图、`contact_sheet.py` 联系表、`export_reels.py` Instagram 竖版。
- 相关技能：**gmail-send**（发邮箱）、**youtube-publish**（YouTube 物料与上传）。
