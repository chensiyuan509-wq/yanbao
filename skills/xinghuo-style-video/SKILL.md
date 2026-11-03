---
name: xinghuo-style-video
description: 用 Python/pycairo 代码制作风格统一的电影感讲解视频——以《星火：人类科学简史》确立的审美与质量为标准：真实历史图像 / 实物照片为主视觉、缓慢的电影式运镜、有理由的转场、克制而高密度的信息面板、会探索会扮演的 Claude 角色、第一人称字幕叙事、无背景音乐只有分层音效、遮幅与胶片质感。每部新片都按自己的内容重新设计结构、镜头和素材，《星火》只作参考不照搬。用户想做 / 改一个代码生成的讲解视频——科普、历史、宇宙天文、编程与计算机、科学原理、技术产品、人物、文明等任何题材，提到"做个视频""8 分钟视频""Claude 形象""像星火那样""同样的风格""电影感""纪录片风格""历史感""运镜转场"，或要在 science_history_video 这类项目上继续做时，都使用本技能。导出与发布另有技能：instagram-reels、youtube-publish、gmail-send。
---

# 星火风格：统一的审美，原创的每一部

《星火：人类科学简史》（`/home/wei/csy/science_history_video`）是用户非常满意的一部片：史前壁画、法拉第讲座这类
历史画面的质感，运镜与转场的审美，叙事手段，信息密度与画面，只有音效没有音乐，Claude 的动作表情，素材与构图——
用户希望**以后的视频都保持这种风格和品位**。

但用户同样明确：**以后做其他视频不是照搬，只是参考。** 本技能固定的是"怎么做才好"，不是"做成什么样"。
新片的故事、结构、镜头、素材都从它自己的内容里长出来；《星火》是一本可以翻阅的范例，不是一个往里填字的模板。

## 必须保持一致的（风格基因）

- **主视觉是真的东西**：真实的历史图像、文物、手稿、老照片、实物照片、卫星影像；没有授权的真图就画示意图并注明，绝不伪造。
- **电影质感**：遮幅黑边、胶片颗粒、暗角、有方向的光；画面永远在缓慢运动；元素淡入、由虚到实，不弹跳不飞入。
- **转场有理由**：像剪辑而不像翻页；光、纸、电、冲进细节……转场来自画面内容，相邻不重复。
- **信息密、版面松**：每个镜头一个主视觉 + 至多一个面板；讲"怎么做到 / 怎么证明 / 数字 / 用在哪"，不罗列名字。
- **Claude 在场**：第一人称"我"在探索；以参观者、扮演者或第一视角出场；用场景光把卡通角色融进真实画面。
- **声音**：没有背景音乐、没有人声；环境底不断、动作音有来源、重音留给大事件；−16 LUFS。
- **版面与信息分层**：按 `references/design-system.md` 的网格和 L0–L5 层级——主视觉在左 / 中，面板在右栏，出处在左下；
  宋体系、暖白 + 金色强调；一镜一事，每屏 ≤ 3 个文字层级。
- **画面指纹**：暗调但有亮场（明暗交替），约 2/3 留白，重心居中，冷暖分区；用 `style_audit.py` 对照星火检查。
- **严谨**：每个数字和年份有出处，有争议就照实写；每张图标明出处和授权。
- **质量线**：不用火柴人；地图不手绘；科技内容讲到原理、证明、数字和应用；一屏一个重点。

## 每部片重新设计的（不要照搬）

- **结构**：是否分章、分几段、有没有序章 / 尾声、有没有"关键词"——由题材决定。星火的"8 章 + 8 个方法收成一只手"是它自己的构思。
- **镜头与构图**：从 `references/style-bible.md` 的构图词汇里按内容挑，或者发明新的；不要每段都套同一组镜头。
- **开场钩子和结尾余味**：为这部片单独想；不要复用星火的星图、手印、篝火。
- **调色**：按本片的时代 / 题材定（同样的原则：真实质感 + 统一的强调色）。
- **素材**：为本片的题材去找图（见 `references/archive-library.md` 的流程）；现有 89 张是为科学史找的，题材重合时才用。
- **转场和音效的具体选择**：根据本片的画面设计，而不是沿用星火的转场表和音效表。

## 怎么用《星火》做参考

- 想知道"某种效果怎么实现"（展厅推镜、蓝图动画、卫星地图、证明拼图、第一视角），翻 `examples/xinghuo/scenes/` 对应的函数学写法。
- 想知道"做到什么程度才算好"，看 `examples/xinghuo/README.md` 的分镜表和事实出处表。
- 不要复制它的分镜顺序、字幕、镜头组合或素材到新片；借的是手法和标准，不是内容。

## 参考文档

| 要做的事 | 读 |
|---|---|
| **设计系统**：版面网格、信息分层、出场编排、密度预算、画面指纹、12 种镜头语法、分镜方法 | `references/design-system.md` |
| 换题材（宇宙、编程、科学原理、产品……）：真东西是什么、素材来源、亮场、冷暖、Claude 身份、声音 | `references/domain-playbooks.md` |
| 星火的视觉细则：配色值、字体别名、按时代调色、十三种构图的实现 | `references/style-bible.md` |
| 运镜与转场的语法（各适合什么情境） | `references/camera-and-transitions.md` |
| 叙事、字幕写法、信息密度、讲证明 / 原理 | `references/narrative-and-density.md` |
| 音效的三层结构与选择原则 | `references/sound-design.md` |
| 找图、授权、现有素材清单 | `references/archive-library.md` |
| Claude 的出场方式、表情、动作、服装 | `references/claude-character.md` |
| 引擎函数、场景模块约定、渲染命令、**踩过的坑** | `references/engine-api.md` |

开工前必读 design-system（它是风格一致的依据），再按题材读 domain-playbooks 对应一节；写镜头时翻 camera-and-transitions、narrative-and-density。

## 默认规格（用户没另说就照此）

30fps；预览 480p，上传平台用 1080p（`--res 1080`）；2.2:1 遮幅，字幕烧在下黑边并另出 SRT；无人声、无背景音乐；
Claude 叫 Claude（不叫"小橙"）；图像只用公有领域 / CC0 / CC BY。

## 流程

1. **定题**：主题、时长、受众、分辨率。把题材里最有画面感、最能讲清"为什么"的几件事找出来。
2. **研究**：查清事实与数字（WebSearch），记下出处；同时想清楚每件事**能用什么真实图像**来讲。
3. **设计分镜（先于代码）**：在项目 README 的分镜表里写：每段讲什么 → 哪些镜头 → 每个镜头的主视觉、构图、运镜 →
   镜头间转场及理由 → 声音（表头见 design-system 第 9 节，镜头类型用第 8 节的 12 种）。写完自查：每段都有真实视觉、
   原理 / 证明、数字、应用；亮场暗场交替、冷暖分区；Claude 在场；有没有不自觉地套用星火的结构。
4. **建项目**：
   ```bash
   python ~/.claude/skills/xinghuo-style-video/scripts/new_project.py <目录> --title "片名" --slug <拼音> \
       --minutes 6 --sections "段1,段2,段3" [--chapter-cards] [--no-prologue] [--no-epilogue]
   cd <目录> && bash setup_env.sh    # 或复用现有 venv：/home/wei/csy/ai_relay_video/.venv/bin/python
   ```
   生成的只是引擎 + 能渲染的空白占位场景（和一张空白分镜表），没有任何预设镜头。
5. **找素材**：用 `scripts/commons_search.py` 搜，登记到 `tools/fetch_assets.py` 下载；新图先拼联系表看内容对不对再定裁切。
6. **逐段实现**：按分镜写 `SHOTS` / `TRANS` / `VO` / `SUPERS` / `sfx()`。文字一律用 `layout` 组件（`info_panel` `headline`
   `stat` `pointer` `tag`），图解用 `diagram`，代码用 `codeview`——层级、字号、出场节奏就自动和星火一致。
   需要的效果引擎里没有就写新的（好的新手法确认稳定后同步回 `engine/` 并补进参考文档）。
7. **自查（每段都做）**：`python check.py --quick` → `python render.py --still <关键时间点>` →
   `scripts/contact_sheet.py` 拼图后用 Read 逐张看：文字压主体、字卡与画面打架、缺字方块、被黑边切掉、空洞或拥挤、转场跳动、Claude 被挡。
8. **成片**：后台 `python render.py`；**风格审计** `python ~/.claude/skills/xinghuo-style-video/scripts/style_audit.py out/<slug>_480p.mp4 --project .`
   （画面亮度、对比、留白、重心、镜头时长、字幕速度、数字比例、转场种类、Claude 出场，对照星火区间）；查静音、响度、
   全片联系表；更新 README（分镜、事实出处、图像来源）。
9. **交付**：发邮箱用 **gmail-send**；Instagram 竖版用 **instagram-reels**；YouTube 物料与上传用 **youtube-publish**。
   提交 git、推送、发邮件、上传都只在用户要求时做。

## 资源

- `engine/`：引擎快照（aivid、mascot、render.py、check.py、tools、地图数据、89 张已授权图像）。新项目由脚手架复制，不在这里直接改。
- `templates/stub_template.py`：空白占位场景。
- `examples/xinghuo/`：《星火》全部场景源码与 README（参考）。
- `examples/cross_domain/`：宇宙、编程两段跨题材样张（参考），演示同一风格换题材。
- `scripts/`：`new_project.py` 建项目、`commons_search.py` 搜图、`contact_sheet.py` 联系表（图片或整片抽帧）、
  `style_audit.py` 风格审计。
