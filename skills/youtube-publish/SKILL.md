---
name: youtube-publish
description: 把做好的视频发布到用户的 YouTube 频道：准备上传物料（1080p 成片、标题、带章节时间戳的简介、标签、分类、中文字幕 SRT、1280×720 封面），检查 YouTube 的硬性限制，并通过 YouTube Data API（OAuth）上传、设置封面和字幕、改隐私状态。用户提到"发 YouTube""上传油管""YouTube 简介 / 章节 / 封面""发到频道""公开视频"，或问怎么认证 YouTube 账号、怎么配置 YouTube API 时使用。上传和公开都只在用户明确要求时做。
---

# YouTube 发布

**当前状态（2026-11-03）：用户还没有认证 YouTube 账号，说过"后续认证后再决定发布"。**
所以现在只做两件事：准备物料、检查物料；**不要上传**。等用户完成 `references/setup-auth.md` 的步骤、
并在当轮明确说"上传 / 发布"之后，才运行上传。上传是对外动作，公开更是——每一步都要用户点头。

## 流程

### 1. 准备物料（随时可做，不联网）

在视频项目目录里（例如用 xinghuo-style-video 做的项目），用项目的 venv：
```bash
python render.py --res 1080                         # 上传用 1080p；480p 在 YouTube 上会被当成低画质
python ~/.claude/skills/youtube-publish/scripts/prepare_youtube.py --thumb 15.6 \
       --summary "一两句话说这部片讲什么" --tags "科学史,科普,历史,纪录片,动画,Claude"
```
输出 `out/youtube/`：`metadata.json`、`description.txt`（章节时间戳 + 图像署名，含 CC BY 作者）、`captions.srt`、`thumbnail.jpg`。
脚本会检查：标题 ≤ 100 字符、简介 ≤ 5000 字节、标题 / 简介不能含 `<` `>`、标签合计 ≤ 500 字符、
章节（第一条 00:00、至少 3 条、每段 ≥ 10 秒）、封面 ≤ 2 MB。

写标题和简介的习惯（细节见 `references/metadata.md`）：
- 标题：片名 + 一个钩子，中文为主，可加英文副标题方便海外搜索。
- 封面：选最有冲击力的真实历史画面或片名帧；画面里已有大字的话不要再叠字。
- 分类：27 教育（默认）或 28 科学与技术；语言 `zh-Hans`；不是儿童内容。
- 默认 `private`。

### 2. 检查凭据与物料（随时可做，不上传）
```bash
python ~/.claude/skills/youtube-publish/scripts/upload_youtube.py out/youtube/metadata.json
```
列出：依赖是否装好、OAuth 客户端和令牌是否就位、视频 / 封面 / 字幕是否存在、标题与隐私设置。

### 3. 一次性认证（用户自己操作）
按 `references/setup-auth.md`：频道手机验证 → Google Cloud 启用 YouTube Data API v3 → 创建桌面应用 OAuth 客户端 →
`client_secret.json` 放到 `~/.config/youtube-publish/` → 用户用 `! … upload_youtube.py --auth-only` 在浏览器里授权。

### 4. 上传（仅在用户明确要求时）
```bash
python ~/.claude/skills/youtube-publish/scripts/upload_youtube.py out/youtube/metadata.json --upload
```
先以 **private** 上传，自动设置封面和字幕，打印视频链接和 Studio 编辑链接，结果写进 `out/youtube/upload_result.json`。
未经审核的 API 项目只能上传为私享——这正好符合"先私享、检查后再公开"的流程。

### 5. 公开（仅在用户看过并明确要求时）
在 YouTube Studio 里手动改为公开（API 项目未审核时只能这样）；项目审核通过后也可以：
`upload_youtube.py --set-privacy <视频ID> public`。

## 凭据与隐私

- `~/.config/youtube-publish/client_secret.json`、`token.json`：只在本机，权限 600，**不进 git、不打印、不贴进对话**。
- 备份 skill 到仓库时只备份 `~/.claude/skills/youtube-publish/`，里面不含任何凭据。

## 和其他技能的关系

- 视频本身用 **xinghuo-style-video** 制作；Instagram 竖版用 **instagram-reels** 导出。
- 想先发到自己邮箱看效果，用 **gmail-send**。
