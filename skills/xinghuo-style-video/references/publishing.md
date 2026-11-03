# 发布：YouTube 与 Instagram

用户把视频发在 **YouTube** 和 **Instagram**（不是 B 站、不是视频号）。正片是 16:9（画面内 2.2:1 遮幅），
YouTube 直接传正片；Instagram 用竖版 9:16 的片段。平台规则会变，下面的数字是 2026 年时的常识，拿不准就查一下最新规定。

## 分辨率怎么选

- 预览、发邮件：480p（默认，渲染最快）。
- **上传平台：渲染 1080p**（`python render.py --res 1080`，8 分钟约 10 分钟）。480p 在 YouTube 上会被判成低画质，
  竖版放大后也会糊。用户若明确只要 480p 就照办，但上传前提醒一句。

## YouTube（正片）

```bash
python render.py --res 1080                                   # → out/<slug>_1080p.mp4，直接上传
python <skill>/scripts/export_social.py youtube --thumb 15.6  # 章节时间戳 + SRT + 1280×720 封面
```
- `out/youtube_description.txt`：章节时间戳（第一条 00:00、至少 3 条、每段 ≥ 10 秒——YouTube 章节的规则），后面附图像来源说明，
  贴进简介即可生成进度条章节。
- `out/<slug>.srt`：画面里已经烧了中文字幕；SRT 可在 YouTube Studio 另传为 CC 字幕（方便搜索和自动翻译）。
- `out/thumbnail.jpg`：从片中取一帧（片名、最有冲击力的历史画面都行），1280×720。
- 2.2:1 遮幅已经画在 16:9 画面里，不用再处理。

## Instagram（Reels，竖版 9:16）

```bash
python <skill>/scripts/export_social.py reels --chapter 3                         # 整章
python <skill>/scripts/export_social.py reels --start 101 --end 160 --title "勾股定理的拼图证明"
```
- 输出 1080×1920：中间是完整的 16:9 画面（字幕和出处都在），上下是同一画面的模糊放大做底，上方一行宋体标题。
- Reels 时长有上限（目前约 3 分钟），8 分钟正片要按章节或精彩段落切；最好每段自成一个小故事
  （一个证明、一个实验、一件发明），开头 2 秒就要有画面冲击力。
- 界面会盖住画面顶部约 250 像素、底部约 350 像素和右侧一列按钮——标题放在 y≈330–630，主体在中间，都在安全区内。
- 同一段也可以当 YouTube Shorts 用（也是竖版、时长上限同样约 3 分钟）。

## 署名与说明

- 片中每张历史图像已有出处字幕；简介里再写一句"历史图像来自 Wikimedia Commons（公有领域 / CC0 / CC BY）"。
- 用了 CC BY 的图（如 M87 黑洞照片、Frontier 超算、深蓝），简介里最好列出作者和授权。
- 无背景音乐，音效全部程序合成，不存在版权音乐问题。
