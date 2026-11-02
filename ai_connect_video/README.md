# 连接的力量 · AI 为什么先在美国爆发？

纯 Python 代码生成的 5 分钟科普动画。主角"小橙"按 `assets/image.jpg` 的造型与 11 种表情矢量重绘，带着不懂 AI 的观众，从"什么是大语言模型""什么是智能体"讲到产品形态、语料、软硬件底座、应用互联、竞合与"孤岛"，最后落到：**开放互联才是 AI 先发优势的根**。

| 项目 | 规格 |
|---|---|
| 时长 | 5:00（9000 帧） |
| 分辨率 / 帧率 | 默认 1280×720，可选 854×480；30fps |
| 编码 | H.264（yuv420p）+ AAC 48kHz 立体声，`+faststart` |
| 字幕 | 中文字幕烧录在画面里，另导出 `out/subtitles.srt` |
| 声音 | **只有音效，没有背景音乐、没有旁白**；70 种音效全部由 numpy 现场合成 |
| 素材 | 除角色参考图外，所有画面、图标、音效都是代码绘制 / 合成的 |

## 快速开始

```bash
cd ai_connect_video
bash setup_env.sh                 # 建虚拟环境 .venv（复用系统的 pycairo，装 numpy + imageio-ffmpeg）
source .venv/bin/activate

python check.py                   # 可选：渲染前校验（时间轴 / 字幕 / 缺字 / 音效 / 逐帧冒烟渲染），约 1 分钟
python render.py                  # 渲染 720p 成片 → out/ai_connect.mp4
python render.py --res 480        # 改为 854×480
```

在 8 核机器上，720p 全片渲染约 2 分钟（画面 7 进程并行 + 音轨合成 + 封装）。

### 其他用法

```bash
python render.py --still 12 95.5 230        # 只导出这几秒的画面 → out/stills/
python render.py --sheet 2.5                # 每 2.5 秒取一帧拼成预览联系表 → out/sheet_*.jpg
python render.py --start 84 --end 124.5     # 只渲染一段（带对应音轨），例如"产品形态巡礼"
python render.py --audio-only               # 只生成音轨 → out/soundtrack.wav
python render.py --workers 4 --crf 20       # 指定进程数 / 画质（crf 越小越清晰，默认 18）
```

### 环境说明

- Python 3.9+；依赖 `pycairo`、`numpy`、`imageio-ffmpeg`（自带 ffmpeg，无需系统安装），`Pillow` 仅 `--sheet` 预览时用到。
- 中文字体：Noto Sans CJK SC（Ubuntu/Debian：`sudo apt install fonts-noto-cjk`）。
- pycairo 优先用系统包（`sudo apt install python3-cairo`），所以虚拟环境要带 `--system-site-packages`；若想在虚拟环境里 `pip install pycairo`，需要先 `sudo apt install libcairo2-dev pkg-config`。
- 没有 uv 时，`setup_env.sh` 会退回用 `python3 -m venv`（需要系统装了 `python3-venv`）。

## 分镜

| 时间 | 章节 | 讲什么 | 画面 |
|---|---|---|---|
| 0:00–0:17 | 开场 | AI 新闻刷屏：它们是什么？为什么在美国先爆发？ | 深夜浮岛上熟睡的小橙被一连串推送"叮"醒；弹幕刷屏；星星连成网络，片名《连接的力量》 |
| 0:17–0:30 | 01 大语言模型 | LLM 本质是"文字接龙" | 输入"床前明月"，候选字概率条（光 92%）→"光"飞入空槽 → 一字一字续写"疑是地上霜" |
| 0:30–0:41 | 01 | 读海量文字，把规律压缩进千亿参数 | 网页 / 书籍 / 论文 / 代码飞进模型球，计数器滚到数十万亿；镜头推进模型内部，千亿个"旋钮"被拧准 |
| 0:41–0:50 | 01 | 大脑只会说、不会做 | 技能徽章一个个点亮；伸手够机票却够不着，"我只能告诉你怎么订……" |
| 0:50–1:11 | 02 智能体 | Agent = 大模型 + 工具；拆解-调用-检查循环；订机票全流程 | 大脑 + 工具 = 智能体（工具绕身旋转）；循环光点；查航班 → 比价 → 填表 → 付款前确认 → 出票成功 |
| 1:11–1:24 | 02 | 四年从"陪你聊"到"替你干"；领跑者多在美国 | 小橙沿时间轴跳过 5 个里程碑，跳下时间轴，镜头下摇到美国西海岸地图，几家公司在湾区落钉 |
| 1:24–2:04 | 03 产品形态 | ChatGPT、Codex、Claude Code、OpenCode、OpenClaw、WorkBuddy、Muse | 镜头逐站平移的展厅，每站一张卡片 + 一段演示；最后所有产品连线到各种工具："连接 = 能力" |
| 2:04–2:29 | 04 语料 | 吃得好才聪明；英文互联网是开放粮仓；英文近半、中文不到 6%；内容锁在 App 里 | 小橙吃书籍 / 论文 / 代码，推开垃圾广告；敞开大门的粮仓；Common Crawl 柱状图；网民占比甜甜圈 + 上锁的 App |
| 2:29–2:44 | 04 | 数据授权；更宝贵的是"行为数据" | Reddit 把授权合同递给 Google / OpenAI、金币回流；智能体日志被打包成光块喂给下一代模型 |
| 2:44–3:08 | 05 软硬件底座 | 显卡、CUDA、Linux / Ubuntu、PyTorch、大模型、智能体层层咬合 | 六层底座砸落叠起，小橙一层层跳上去，两侧齿轮咬合；终端里一条命令装好驱动 |
| 3:08–3:38 | 06 应用层互联 | Muse 一句话授权，连上 Google 全家桶 + Instagram；一句话跑完周报流程；飞轮效应 | 授权弹窗 → 节点逐个连上 → 数据流经 Ins → 表格 → 文档 → 邮件 → 任务 → 加速旋转的飞轮 |
| 3:38–4:04 | 07 竞合 | Google 对 Meta 开放接口；苹果用 Gemini 驱动 Siri；MCP 交给 Linux 基金会 | VS 火花后插头插进开放接口；Gemini 星光飞进 iPhone；各家插进 MCP 枢纽、被基金会大楼罩住；竞争 / 合作绕着越变越大的蛋糕 |
| 4:04–4:40 | 08 孤岛 | 模型不差，差在互联；WorkBuddy 连不上抖音、小红书；豆包助手被 150 多款 App 拒绝 | 大海上一座座围墙花园；WorkBuddy 小船连得上海外应用、连不上抖音 / 小红书；"拒绝"印章砸下、计数涨到 150+；小橙伸手够不着 |
| 4:40–5:00 | 结语 | 下半场是生态之战；开放协同是先发优势的根 | 算力 / 算法的军备竞赛 → 协议连成的网络 → 从"开放协同的土壤"长出的产品之树 → 日出时孤岛之间架起光桥 |

13 处转场、9 种效果：橙色方块开窗（小橙的身体形状）、穿越推镜、甩镜头（运动模糊）、圆形展开、上推、斜向柔边擦除、百叶窗、数字故障、暖色闪白；场景内还有推拉、平移、下摇、视差、手持感漂移等运镜。

## 片中事实与出处

字幕里的事实性说法都按 2026 年 11 月前的公开报道核对过：

| 说法 | 依据 |
|---|---|
| ChatGPT 每周约 9 亿人在用 | 2026 年 2 月 OpenAI 披露的周活数字（媒体报道） |
| OpenClaw：开源个人智能体，GitHub 星标超 10 万；作者 2026 年 2 月加入 OpenAI，项目转为开源基金会 | [The Register](https://www.theregister.com/2026/02/16/open_ai_grabs_openclaw) |
| OpenCode：开源（MIT），支持 75+ 模型服务商 | [GitHub: anomalyco/opencode](https://github.com/anomalyco/opencode) |
| WorkBuddy：腾讯 2026 年 3 月上线的桌面智能体，基于 MCP 的连接器可接 Gmail、Slack、Notion 等 | IT之家、[环球网](https://tech.huanqiu.com/article/4RkP4GkcZrP) 报道 |
| Muse：Meta 2026 年 9 月发布的个人智能体，可连 Gmail、Google 文档 / 表格 / Tasks / 日历，Instagram 等 Meta 账号自动连接 | [Meta 帮助中心：How Muse works with Connectors](https://www.meta.com/help/artificial-intelligence/1687253048996149/)、[第三方连接器清单](https://postfa.st/blog/meta-muse-connectors-list) |
| 公开网页语料里英文约 46%，中文不到 6% | Common Crawl 2023 年 3 月抓取的语言统计（[维基百科：Common Crawl](https://en.wikipedia.org/wiki/Common_Crawl)） |
| Reddit 把内容授权给 Google、OpenAI | 2024 年 2 月（Google）、5 月（OpenAI）公开报道 |
| Canonical 宣布在 Ubuntu 官方软件源中分发 CUDA | [Canonical 博客（2025 年 9 月）](https://canonical.com/blog/canonical-announces-it-will-support-and-distribute-nvidia-cuda-in-ubuntu) |
| PyTorch 由 Meta 开源，2022 年移交 Linux 基金会旗下的 PyTorch 基金会 | PyTorch 基金会公告（2022 年 9 月） |
| MCP 由 Anthropic 于 2024 年 11 月开源；2025 年 12 月交给 Linux 基金会的智能体 AI 基金会（AAIF），OpenAI、Google、微软、AWS 等为成员 | [Anthropic 发布 MCP](https://www.anthropic.com/news/model-context-protocol)、[AAIF 成立报道](https://itsfoss.com/news/agentic-ai-foundation-launch/) |
| 苹果 2026 年 1 月宣布新 Siri 由 Gemini 驱动 | [The Register](https://www.theregister.com/2026/01/12/apple_taps_google_gemini_siri/) |
| 豆包手机助手：2025 年 12 月遭微信等限制；2026 年 10 月公布约 150 多款拒绝 AI 代操作的 App（微信、淘宝、支付宝、美团、小红书等） | [同花顺财经（2026-10-16）](https://news.10jqka.com.cn/20261016/c680769118.shtml)、第一财经等报道（各家统计为 151–155 款） |

两处措辞特意做了调整，保证准确：

1. **WorkBuddy 与字节跳动**：WorkBuddy 2026 年 6 月已上线**官方飞书连接器**（飞书是字节的产品），所以字幕没有写"用不了字节的接口"，而是写"没有**抖音、小红书**的官方连接器"——目前查不到这两家的官方连接器，第三方工具只能靠抓取或模拟登录绕路。
2. **"美国模型好是因为语料好"**：片中把语料作为重要原因之一来讲（英文开放网页多、可授权、交互数据丰富），没有说成唯一原因；同时明确"问题不在模型，DeepSeek 等国产模型已是世界第一梯队"。

## 目录结构

```
render.py            渲染入口：多进程逐帧绘制 → 各进程用 ffmpeg 分段编码 → 拼接 → 混入音轨
check.py             渲染前校验（时间轴、字幕语速与宽度、缺字、音效、逐帧冒烟渲染、音轨）
setup_env.sh         一键建虚拟环境
requirements.txt     Python 依赖
subtitles.srt        全部 51 条中文字幕（渲染时也会输出到 out/subtitles.srt）
assets/image.jpg     角色表情参考素材
aivid/core.py        引擎：缓动、关键帧、噪声、颜色、图形、文字、镜头、粒子
aivid/ui.py          界面组件：卡片、气泡、窗口、终端、按钮、表格、印章……
aivid/icons.py       40 多个矢量图标（产品、应用、显卡、齿轮、锁、蛋糕……，均为通用风格，非官方 Logo）
aivid/mascot.py      小橙：16 种表情的平滑过渡、眨眼、视线、走 / 跳 / 挥手 / 伸手 / 说话，以及 Puppet 动作时间轴
aivid/transitions.py 转场合成
aivid/timeline.py    场景拼接、字幕、章节标签、进度条、SRT 导出
aivid/audio.py       70 种音效的合成、混响与限幅
aivid/scenes/        14 个场景（s01_intro … s14_ending）与转场表 __init__.py
```

## 怎么改

- **改字幕**：每个场景文件顶部的 `SUBS = [(开始, 结束, "文字"), ...]`，时间是该场景内的本地秒数；`{花括号}` 里的字会高亮成橙黄色。改完跑一次 `python check.py`，会检查重叠、语速和是否超宽。
- **改场景时长**：改场景文件里的 `DUR`，以及该场景内对应的关键帧时间；全片总长由各场景 `DUR` 相加得到（现在正好 300 秒）。
- **换转场**：`aivid/scenes/__init__.py` 的 `TRANSITIONS`。
- **调音效**：各场景的 `sfx()` 返回 `(时间, 音效名, {参数})`；音效本身在 `aivid/audio.py`（`s_音效名` 函数）。
