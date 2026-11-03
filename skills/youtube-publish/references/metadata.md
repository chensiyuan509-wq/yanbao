# YouTube 元数据写法

| 字段 | 规则 | 建议 |
|---|---|---|
| 标题 `snippet.title` | ≤ 100 字符，不能有 `<` `>` | 《片名》+ 钩子；例：「星火：从洞穴手印到 AI，8 分钟看人类怎样学会理解世界」 |
| 简介 `snippet.description` | ≤ 5000 字节，不能有 `<` `>` | 一两句概述 → 章节时间戳 → 图像署名 → 地图来源 → "无背景音乐" |
| 标签 `snippet.tags` | 合计 ≤ 500 字符（含空格的标签按加引号计） | 6–12 个：主题词 + 科普 / 历史 / 纪录片 / 动画 + 关键人物 |
| 分类 `categoryId` | 数字字符串 | 27 教育；28 科学与技术 |
| 语言 | `defaultLanguage` / `defaultAudioLanguage` | `zh-Hans` |
| 隐私 `status.privacyStatus` | private / unlisted / public | 上传时一律 private |
| 儿童内容 `selfDeclaredMadeForKids` | 布尔 | false |
| 封面 | JPG/PNG ≤ 2 MB，建议 1280×720 | 需频道已手机验证 |
| 字幕 | SRT，`captions.insert` | 画面已烧录中文字幕，另传一份 CC 便于搜索和自动翻译 |

## 章节

YouTube 从简介里的时间戳自动生成章节，条件：第一条是 `00:00`，至少 3 条，按时间递增，每段至少 10 秒。
`prepare_youtube.py` 从项目的 `CHAPTER` 自动生成：序章 → 各章"第 N 章 标题" → 尾声。

## 署名

片中所有历史图像在画面左下角都有出处；简介里再写一句总说明，并**逐条列出 CC BY 授权的图**（作者 + 授权版本）——
CC BY 要求署名，公有领域 / CC0 不强制但写上更规范。`prepare_youtube.py` 会扫描场景源码里用到的素材键，自动列出 CC BY 的那些。

## 合成内容披露

动画、明显非写实的画面不需要"改动或合成内容"披露；如果某部片里有写实到可能被误认为真实拍摄的 AI 生成画面，
在 Studio 上传流程里按实际情况勾选。
