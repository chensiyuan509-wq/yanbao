# AI 接力赛 · 从一篇论文，到你的工作和生活

纯 Python 代码生成的 **10 分钟**科普动画。主角是 Claude 形象（按 `assets/image.jpg` 的造型重绘）戴上探险帽，带观众逛一遍 AI 世界：从 2017 年谷歌的 Transformer 论文讲起，经过英伟达 CUDA、Linux / Ubuntu、博通与 Marvell 的定制芯片和光通信、台积电代工与先进封装、横跨太平洋的台美产业接力，再到 AI 产品从聊天到智能体的演进；然后追问"为什么 AI 先在美国引爆"（竞合与互通、有耐心的钱、愿意付费的土壤、数据飞轮），对照中国 AI 的另一面（算法出色、却困在数据孤岛与付费习惯里，于是走向开放权重），最后落到 AI 会怎样改变每个人的工作和生活。

| 项目 | 规格 |
|---|---|
| 时长 | 10:00（18000 帧，16 个场景，7 个章节） |
| 画面 | 1280×720 / 30fps（可选 480p、1080p），H.264 yuv420p，`+faststart` |
| 配音 | 无人声旁白，文案全部以字幕呈现 |
| 字幕 | 中文字幕烧录在画面里（按阅读时长显示），另导出 `out/subtitles.srt` |
| 声音 | 程序生成的背景音乐（按章节换情绪）+ 500 多个音效；响度归一到 −16 LUFS，峰值 ≤ −1 dBFS |
| 素材 | 除角色参考图外，画面、图标、音乐、音效全部由代码绘制 / 合成；公司与产品只用名字和通用图形表示，不使用官方 Logo |

## 快速开始

```bash
cd ai_relay_video
bash setup_env.sh                 # 建虚拟环境 .venv（复用系统 pycairo，装 numpy / imageio-ffmpeg / Pillow）
source .venv/bin/activate
python check.py --quick           # 校验（可选）
python render.py                  # → out/ai_relay.mp4（8 核约 3–5 分钟，含音轨合成）
```

常用参数：

```bash
python render.py --res 480                 # 854×480 快速版
python render.py --res 1080                # 1920×1080（画面是矢量的，任何分辨率都清晰）
python render.py --start 89 --end 216      # 只渲染一段（这里是第 02 章"算力接力"），带对应音轨
python render.py --still 12 95.5 230       # 只导出这几秒的画面 → out/stills/
python render.py --sheet 5                 # 每 5 秒一帧拼成预览联系表 → out/sheet_*.jpg
python render.py --music none              # 不要背景音乐
python render.py --music 我的配乐.mp3       # 换成你自己的正版配乐（自动循环）
python render.py --no-subs                 # 不烧录字幕（单独用 out/subtitles.srt）
python render.py --audio-only              # 只生成音轨 → out/soundtrack.wav
```

渲染时每个进程独立画帧、分段编码再拼接；720p 平均每帧约 20 ms。

## 分镜

| 时间 | 章节 | 讲什么 | 画面 |
|---|---|---|---|
| 0:00–0:31 | 片头 | AI 先学会写代码，又进了办公室，还要打理生活；它怎么走到今天、为什么先在美国引爆、会怎样改变工作和生活 | 三座浮岛：自动写代码的屏幕 → 自己完成的周报 / 表格 / 邮件 → 订票、日程、比价的手机；镜头钻进手机里的世界地图，美国亮起；Claude戴上探险帽，举起接力棒，片名《AI 接力赛》 |
| 0:31–0:59 | 01 一篇论文 | 2017 年谷歌八位研究员的《注意力就是你所需要的一切》；排队过安检 vs 一眼看全；天生适合并行 | 2012→2017 翻页年份；论文、八位作者、结构示意、Transformer 印章；词块排队过闸门 → 所有词互相连线（"它的"指"小猫"）→ 词块落进显卡，模型越长越大 |
| 0:59–1:29 | 01 | 把它推向极致的是 OpenAI；参数涨一千多倍；ChatGPT 两个月破亿；八位作者陆续离开谷歌；论文公开、人才流动 | 论文像接力棒从谷歌大楼飞进车库；对数柱状图 ×1500；ChatGPT 窗口 + 用户计数器 + 彩纸；作者头像飞向各家公司；硅谷公路上传递的光棒 |
| 1:29–2:12 | 02 算力接力 | 显卡 + CUDA（2006）；AlexNet 两块显卡夺冠；CUDA 生态是护城河；跑在 Linux / Ubuntu 上；层层咬合的技术栈 | 推不动的大模型 → 显卡从天而降；游戏画面变矩阵、CUDA 大门打开；错误率对比 + 起飞曲线；护城河城堡、软件库砖块、涌来的开发者；成排服务器上的企鹅；六层技术栈落下、齿轮咬合 |
| 2:12–2:52 | 02 | 巨头定制 ASIC：谷歌 TPU 与博通、OpenAI × 博通 10 吉瓦；Marvell 的定制芯片与光通信；铜线 vs 光纤；光模块里的"翻译官"；一盘散沙 vs 一张光网 | 瑞士军刀 vs 专用芯片 + 能效条；合作卡片与十座输电塔；云厂商与定制芯片；发热的铜线打叉 → 光纤脉冲；透明光模块里 DSP 把方波变成光脉冲；散落的芯片被光纤连成网格 |
| 2:52–3:35 | 02 | 台积电"只代工、不设计"（1987）；英伟达们专心设计；先进封装、测试、组装；第一片美国造 Blackwell 晶圆还要飞回台湾封装；跨越太平洋的接力赛 | 设计图 → 台积电工厂；台湾—美国航线与印章；各家设计图飞进工厂、晶圆出炉；GPU 与 HBM 封装、探针测试、服务器机柜；点阵世界地图上晶圆从亚利桑那飞往台湾；美国设计、台湾制造、荷兰光刻机、韩国内存连成接力路线 |
| 3:35–4:20 | 03 从聊天到智能体 | 产品井喷；聊天机器人；编程助手；MCP 万能插头；各家支持并捐给 Linux 基金会；会干活的 Claude Code / Codex；开源的 OpenCode、OpenClaw | Claude站在左边讲解，右侧面板轮播：喷涌的产品图标、四家聊天卡片、Tab 接受建议的编辑器、MCP 插头连上 GitHub / Slack / 文档 / 日历 / 数据库、基金会大楼、终端里自动修 bug 跑测试、可切换模型的 OpenCode、龙虾钳 OpenClaw |
| 4:20–5:04 | 04 为什么是美国 | Muse 和 Gemini 是对手，却能连 Gmail、谷歌日历 / 文档、Outlook、Instagram；苹果谷歌斗了十几年，Siri 用上 Gemini；投资关系网；竞争、合作、投资缠在一起 | 镜头在天空的三层云台间上下移动：美国点阵地图 → VS 火花 → Muse 连线对手家的服务 → iPhone 上的谷歌全家桶与 Siri 光球 → 投资 / 合作 / 竞争三色关系网 → 三股线拧成一股绳 |
| 5:04–5:53 | 04 | 有耐心的钱：先让用户满意再赚钱；投入期与收获期的时间错配，2026 年四大巨头资本开支约 7000 亿美元；愿意付费的土壤：ServiceNow、财捷；AI 订阅 20 / 200 美元、企业按人头付费；商业飞轮 | 带钟面的金币；Muse 的三步走与爱心；J 曲线（投入期 / 收获期）+ 资本开支柱状图；落进土壤的硬币和幼苗；两棵订阅大树和收入卡片（97% 来自订阅）；价签与座位网格；转起来的商业飞轮 |
| 5:53–6:20 | 04 | 数据飞轮：用户 → 反馈 → 模型；Claude 在编程上的飞轮，一骑绝尘 | Claude推动飞轮、三段依次点亮；编辑器里的采纳 / 修改 / 跑测试化作光点飞进飞轮；飞轮滚滚向前、速度线和扬尘；企业编程市场份额 54% |
| 6:20–6:44 | 05 孤岛与飞轮 | 反观中国：DeepSeek 算法出色；WorkBuddy、千问办公、钉钉、豆包手机大多只在自家生态里畅通，一出岛就撞墙 | 暗场转入黄昏；地图转向中国；小鲸鱼与 MoE / MLA / FP8 / 强化学习徽章；腾讯、阿里、字节三座岛上应用之间光点流动；跨岛的智能体撞上升起的围墙 |
| 6:44–7:28 | 05 | 微信里淘宝 / 抖音只能复制口令；豆包手机助手被 150 多款 App 拒绝；私域流量与互联网地主；美国的反垄断法；开放语料英文约一半、中文不到 6%；数据碎片化、飞轮转不起来 | 聊天窗口里打不开的链接和"复制口令"；手机上一枚枚"不"字印章与计数器；升起的城堡与旗帜；法院、落下的法槌；语言占比柱状图与上锁的内容；漂浮的数据碎片、生锈被锁住的飞轮 |
| 7:28–8:25 | 05 | 付费飞轮也转不动：一步跨进移动互联网，免费 / 广告 / 补贴；2017 年未授权软件 66%；金山办公、金蝶与 ServiceNow 的收入差距；芯片受限，月之暗面、深度求索、智谱选择开放权重；既是无奈也是聪明的打法（下载量超过美国）；下载≠反馈、免费≠收入 | 卡住的付费飞轮；PC→移动的跳跃弧线；"盗版"印章与 66% 统计卡；收入对比柱状图；被锁住的高端芯片；Kimi / DeepSeek / GLM 三张卡片、权重光块飞向全球；开发者 / 影响力 / 人才与下载占比；两个"≠"、断开的闭环、够不着的山顶 |
| 8:25–8:59 | 06 AI 与你 | 程序员：从敲代码到描述需求、拆解任务、审查结果（谷歌超三成新代码由 AI 生成）；办公全流程；一个人带一群智能体；会提问、会判断、会验收的人更值钱 | 桌前打字的Claude；"过去 / 现在"对比与一队迷你Claude智能体；办公流水线；Claude领着一队小帮手前进；"重复"方块消失，三种能力升值 |
| 8:59–9:27 | 06 | 私人助理；AI 老师与 AI 看影像；AlphaFold 与 2024 诺贝尔化学奖；像电和互联网一样的新基础设施 | 沙发上喝咖啡的Claude与手机上的四件事；黑板与胸片；折叠的蛋白质链与奖牌；城市灯火随"电 → 互联网 → AI"三层亮起 |
| 9:27–10:00 | 结语 | AI 是一场接力赛；开放的连接、更好的数据、健康的商业；围墙开始松动（淘宝接入微信支付、WorkBuddy 连上飞书）；愿每一座孤岛都架起桥 | 日出跑道上传递接力棒（论文→芯片→代工→开源→产品）；三条价值横幅；海上孤岛之间先架起两座桥，再连成一张光网；片尾字卡 |

15 个转场、9 种效果：Claude身体形状的橙色方块开窗、甩镜头（运动模糊）、圆形展开、柔边擦除、推进穿越、白闪、上推、暗场、横推；场景内还有推拉、平移、上下摇、视差、手持感漂移、跟拍奔跑等运镜。

## 片中事实与出处（截至 2026 年 11 月）

| 说法 | 依据 |
|---|---|
| 2017 年谷歌八位研究员发表 Transformer 论文；到 2023 年八位作者已全部离开谷歌 | Vaswani 等，*Attention Is All You Need*（arXiv 1706.03762）；各家媒体报道 |
| GPT 1.17 亿 → GPT-2 15 亿 → GPT-3 1750 亿参数；ChatGPT 2022-11-30 上线，约两个月用户破亿 | OpenAI 论文；UBS 2023 年 1 月估算 |
| CUDA 2006 年发布；AlexNet 用两块 GTX 580 训练，ImageNet 2012 错误率 15.3%（第二名 26.2%）；CUDA 开发者 500 万以上 | 英伟达公告；Krizhevsky 等 2012；英伟达 2024 年公开数字 |
| 谷歌 TPU 由博通协助设计；OpenAI 与博通 10 吉瓦定制芯片合作（2025 年 10 月宣布） | 公开报道 |
| Marvell 为云厂商定制芯片，并是光模块 DSP 芯片的主要供应商之一（2025 年 12 月宣布收购光互连公司 Celestial AI） | [Business Wire](https://www.businesswire.com/news/home/20251202544302/en/Marvell-to-Acquire-Celestial-AI-Accelerating-Scale-up-Connectivity-for-Next-Generation-Data-Centers) |
| 台积电 1987 年由在德州仪器工作二十多年的张忠谋创办 | 公开资料 |
| 2025 年 10 月第一片美国造 Blackwell 晶圆在台积电亚利桑那厂下线，但 CoWoS 封装仍在台湾 | [DCD](https://www.datacenterdynamics.com/en/news/first-us-made-nvidia-blackwell-wafer-manufactured-at-tsmcs-arizona-fab/)、[The Register](https://www.theregister.com/2025/10/20/nvidia_arizona_blackwell/) |
| MCP 2024 年 11 月由 Anthropic 开源；2025 年 12 月捐给 Linux 基金会旗下的智能体 AI 基金会（AAIF） | [Anthropic](https://www.anthropic.com/news/model-context-protocol)、[AAIF 成立报道](https://itsfoss.com/news/agentic-ai-foundation-launch/) |
| OpenClaw 开源个人智能体，GitHub 星标超 10 万 | [The Register](https://www.theregister.com/2026/02/16/open_ai_grabs_openclaw) |
| Meta Muse（2026 年 9 月发布）可连接 Gmail、谷歌日历 / 文档 / Tasks、Outlook，Instagram 等 Meta 账号自动连接 | [Meta 帮助中心](https://www.meta.com/help/artificial-intelligence/1687253048996149/)、[连接器清单](https://postfa.st/blog/meta-muse-connectors-list) |
| 苹果 2026 年 1 月宣布新 Siri 由 Gemini 驱动 | [The Register](https://www.theregister.com/2026/01/12/apple_taps_google_gemini_siri/) |
| 微软投资 OpenAI，也在 Copilot 里用 Anthropic 的模型；亚马逊、谷歌投资 Anthropic；Meta 2025 年以 143 亿美元入股 Scale AI，创始人加盟 Meta | 公开报道 |
| 2026 年四大科技公司资本开支计划合计约 7000 亿美元（亚马逊约 2000 亿、微软约 1900 亿、谷歌母公司 1800–1900 亿、Meta 1250–1450 亿） | 2026 年 4 月财报指引，[Tom's Hardware 汇总](https://tomshardware.com/tech-industry/big-tech/big-techs-ai-spending-plans-reach-725-billion) |
| ServiceNow 2025 年收入 132.8 亿美元，97% 来自订阅；财捷 2026 财年收入 214 亿美元 | [ServiceNow 财报](https://investor.servicenow.com/news/news-details/2026/ServiceNow-Reports-Fourth-Quarter-and-Full-Year-2025-Financial-Results-Board-of-Directors-Authorizes-Additional-5B-for-Share-Repurchase-Program/default.aspx)、[Intuit 8-K](https://www.sec.gov/Archives/edgar/data/0000896878/000089687826000029/fy26q4earningspressrelease.htm) |
| 企业编程市场 Anthropic 占 54%、OpenAI 21%（2025 年 12 月） | Menlo Ventures *State of Generative AI in the Enterprise*（[报道](https://officechai.com/ai/anthropic-google-gain-market-share-at-openais-expense-in-enterprise-api-llm-usage-menlo-ventures-report)） |
| WorkBuddy（腾讯，2026 年 3 月）、千问办公（阿里，2026 年 8 月公测，已打通钉钉）、豆包手机助手 | [IT之家 / 环球网](https://tech.huanqiu.com/article/4RkP4GkcZrP)、[新华网](https://www.news.cn/tech/20260804/9735997ec1ce4738a74d8ea933b9ec0d/c.html) |
| 豆包手机助手遭 150 多款 App 拒绝代操作（2026 年 10 月统计，含微信、淘宝、支付宝、美团、小红书等） | [同花顺财经](https://news.10jqka.com.cn/20261016/c680769118.shtml)、第一财经等 |
| 开放网页语料里英文约 46%、中文不到 6% | Common Crawl 2023 年 3 月抓取的语言统计（[维基百科](https://en.wikipedia.org/wiki/Common_Crawl)） |
| 2017 年中国电脑未授权软件比例 66%，美国不到 20% | [BSA 全球软件调查（2018）](https://www.bsa.org/news-events/news/bsa-survey-unlicensed-software-use-still-high-globally-despite-costly-cybersecurity-threats-0) |
| 金山办公 2025 年收入 59.29 亿元、WPS 月活设备 6.78 亿；金蝶 2025 年收入 70.06 亿元 | [北京日报](https://news.bjd.com.cn/2026/03/26/11653037.shtml)、[金蝶年报新闻稿](https://investor.kingdee.com/static/temp/新闻稿_FY25_final（简体）_1773750223826.pdf) |
| Kimi K2.6（2026 年 4 月）、DeepSeek V4（2026 年 4 月预览版）、GLM-5（2026 年 2 月）开放权重 | [Epoch AI](https://epoch.ai/models/kimi-k2-6)、[NYU Shanghai RITS](https://rits.shanghai.nyu.edu/ai/deepseek-releases-v4-open-source-1-6t-moe-with-1m-context)、智谱发布 |
| Hugging Face 下载量：中国模型 41%、美国 36.5%（2025.2–2026.2） | Hugging Face 2026 春季报告（[EqualOcean 报道](https://equalocean.com/news/2026073122070)） |
| 谷歌超过三成新代码由 AI 生成 | 皮查伊，2025 年 4 月财报电话会 |
| 2024 年诺贝尔化学奖授予 AlphaFold 的研发者（哈萨比斯、江珀）与贝克 | 诺贝尔奖官网 |
| 淘宝 2024 年全面接入微信支付；WorkBuddy 2026 年 6 月上线飞书连接器 | 公开报道 |

几处措辞特意做了平衡：

1. **"数据难以互通"**：WorkBuddy 其实已经能连飞书、千问办公已打通钉钉，所以字幕说的是"大多只在自家生态里畅通无阻"，并在结尾专门讲"围墙已经开始松动"。
2. **"开源只是无奈"**：字幕改成"既是无奈，也是聪明的打法"，并给出中国模型下载量已超过美国的数据；结论落在"没有数据和付费的闭环，很难跑出**最强**的模型"，而不是"做不出强模型"。
3. **"盗版白嫖"**：用 BSA 的统计数字和"没养成为软件付费的习惯"来表述，避免情绪化的说法。
4. **飞轮领先**：Claude 在编程上的领先用 Menlo Ventures 的份额数字说话，并注明出处与时间。
5. 张忠谋等真实人物只用文字，不画肖像；所有公司 / 产品只用名字和通用图形。

## 角色库 mascot/（可复用）

`mascot/` 是独立的角色库（只依赖 pycairo），41 种表情、38 类动作、11 种手臂姿势、24 种特效、帽子 / 眼镜 / 道具，带口型与待机微动。总览图在 `mascot/sheets/`，透明 PNG / SVG 在 `mascot/sprites/`，用法见 `mascot/README.md`。

## 目录结构

```
render.py             渲染：多进程逐帧绘制 → 分段编码 → 拼接 → 混入音轨
check.py              校验：时间轴、字幕阅读时间与宽度、缺字、音效、冒烟渲染、响度
setup_env.sh          一键建虚拟环境
mascot/               可复用角色库（见上）
aivid/core.py         引擎：缓动、关键帧、颜色滤镜、图形、文字、镜头、粒子、景深
aivid/props.py        道具：芯片、晶圆、HBM、服务器、光纤、光模块、工厂、城堡、法槌、价签、奖牌……
aivid/charts.py       图表与地图：飞轮、柱状图、甜甜圈、J 曲线、点阵世界地图、航线
aivid/icons.py / ui.py  图标与界面组件
aivid/narration.py    字幕切分与显示时长估算
aivid/timeline.py     场景拼接、字幕、章节标签、进度条、SRT
aivid/transitions.py  转场合成
aivid/music.py        程序生成的背景音乐（按章节换情绪）
aivid/audio.py        音效库与混音（混响、响度归一、限幅）
aivid/scenes/         16 个场景 s01_intro … s16_ending，转场表在 __init__.py
```

## 怎么改

- **改字幕文案**：每个场景文件顶部的 `VO = [(开始秒, "文案，{高亮}"), ...]`，时间是场景内的本地秒数；`{花括号}` 里的字在字幕里高亮。改完运行 `python check.py --quick` 看看阅读时间是否够。
- **改时长**：改场景的 `DUR` 和对应的关键帧时间；全片总长 = 各场景 `DUR` 之和（现在正好 600 秒）。
- **换转场**：`aivid/scenes/__init__.py` 的 `TRANSITIONS`。
- **调音乐 / 音效**：音乐情绪在 `aivid/music.py` 的 `MOODS` 与 `SCENE_MOOD`；音量在 `aivid/audio.py` 顶部；各场景音效在 `sfx()` 里。
