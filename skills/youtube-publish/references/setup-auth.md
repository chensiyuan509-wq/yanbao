# 一次性准备：YouTube 频道验证 + API 授权

用户**还没认证账号**。这些步骤要用户本人登录 Google 完成（涉及账号与手机号），Claude 只负责指路和检查结果，
不要替用户填表、不要让用户把密码或验证码贴进对话。

## 1. 频道验证（YouTube 网站上）

1. 用要发视频的 Google 账号登录 YouTube，没有频道就先创建频道（名称、头像、简介）。
2. 打开 <https://www.youtube.com/verify> 用手机号验证。验证后才解锁：**超过 15 分钟的视频**、**自定义封面**、直播等。
   （8 分钟的正片不验证也能传，但封面只能用自动截取的三张之一。）
3. 视频是中文、给成年观众的科普内容：上传时"是否为儿童打造"选**否**。

## 2. Google Cloud 里创建 API 凭据（只做一次）

1. <https://console.cloud.google.com/> → 新建项目（例如 `youtube-publish`）。
2. 「API 和服务 → 库」→ 搜索 **YouTube Data API v3** → 启用。
3. 「OAuth 同意屏幕」→ 用户类型 **外部** → 填应用名称和邮箱 → 在「测试用户」里加上用户自己的 Google 账号。
4. 「凭据 → 创建凭据 → OAuth 客户端 ID」→ 应用类型 **桌面应用** → 下载 JSON。
5. 把下载的 JSON 放到 `~/.config/youtube-publish/client_secret.json`，权限 600。**这个文件不进 git、不发到对话里。**

## 3. 安装依赖并授权

```bash
<venv>/bin/pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
! <venv>/bin/python ~/.claude/skills/youtube-publish/scripts/upload_youtube.py --auth-only
```
授权要在浏览器里点同意，所以让用户在会话里用 `!` 前缀自己运行（或在自己的终端里运行）。成功会显示频道名，
令牌存到 `~/.config/youtube-publish/token.json`。

## 必须知道的限制

- **未经审核的 API 项目，上传的视频会被锁定为"私享"**：YouTube 规定 2020 年 7 月 28 日之后创建、未通过审核的 API 项目，
  通过 API 上传的视频只能是 private。要公开：(a) 在 YouTube Studio 里手动改成公开；或 (b) 申请 API 审核。
  所以默认流程就是"API 上传为私享 → 用户在 Studio 里检查 → 用户手动公开"。
- **测试模式的令牌 7 天过期**：OAuth 同意屏幕处于"测试"状态时，刷新令牌约 7 天失效，届时重新运行 `--auth-only`。
- **配额**：默认每天 10000 单位，上传一次约 1600 单位（加封面、字幕各几十到几百），一天传几条没问题。
- 自定义封面需要频道已完成手机验证，否则 `thumbnails.set` 会 403——脚本会提示，之后在 Studio 里手动换即可。
