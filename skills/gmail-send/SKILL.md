---
name: gmail-send
description: 用用户自己的 Gmail（SMTP + 应用专用密码）把文件——尤其是渲染好的视频——当附件发到邮箱，并在需要时先把视频压到 25 MB 附件上限以内。用户说"发到邮箱""发邮件给我""把视频 / 文件发我邮箱""邮件发一份"、或者要把成片、截图、文档通过 Gmail 传到手机上时，都用本技能。只在用户明确要求发送时才发。
---

# Gmail 发送附件

用户的下载链路慢，习惯把成片用 Gmail **发给自己**，在手机上看。本技能负责：检查大小 → 必要时压缩 → 发送。

## 配置（在本机，不在 skill 里）

- `~/.config/gmail-send/config.json`：`{"user": 发件 Gmail, "to": 默认收件人, "password_file": 密码文件路径}`。
  目前发件人和收件人都是用户自己的 Gmail（见记忆 gmail-sending）。
- 密码是 Gmail 的**应用专用密码**（16 位），存在 `password_file` 指向的文件里（权限 600，已加入 git 忽略）。
- 查找顺序：环境变量 `GMAIL_APP_PASSWORD_FILE` → config 的 `password_file` → `~/.config/gmail-send/app_password`。

安全规矩（这些都是用户托付的私密信息）：
- **绝不**打印、cat、echo、grep 密码文件内容，不放进命令行参数、日志、提交或 skill 文件。
- 密码文件和 config 都不进 git；备份 skill 到仓库时只备份 `~/.claude/skills/gmail-send/`，它本身不含任何密码或地址。
- 如果找不到密码文件：请用户自己在终端里输入（脚本会用不回显的方式提示），或请他们把新密码写进文件；不要让用户把密码贴进对话。

## 流程

1. **确认用户要发**：发邮件是对外的、不可撤回的动作，只在用户这一轮明确说"发"时执行；收件人不是默认地址时复述一遍。
2. **检查**（不连服务器）：
   ```bash
   python ~/.claude/skills/gmail-send/scripts/send_mail.py <文件> --check
   ```
   会显示发件人、收件人、附件大小（按编码后算）和密码文件是否就位。
3. **超过上限就压缩**：Gmail 附件 25 MB 是按 base64 编码后计算的，原文件要 ≤ 约 19 MB。
   ```bash
   PYTHON=<项目 venv 的 python> bash ~/.claude/skills/gmail-send/scripts/fit_for_email.sh out/片名_480p.mp4 18
   ```
   两遍编码按目标大小压（8 分钟约 225 kbps 视频 + 64 kbps 音频 ≈ 18 MB）。
   **星火风格的项目先渲染无颗粒版**再压：`python render.py --grain 0 --out out/<slug>_480p_nograin.mp4`——
   胶片颗粒在低码率下会糊成一片。压完抽两三帧看一眼文字是否清楚。
4. **发送**：
   ```bash
   python ~/.claude/skills/gmail-send/scripts/send_mail.py out/片名_480p_mail.mp4 --subject "《片名》480p 邮件版" --body "……"
   ```
   默认收件人取自 config；`--to` 可改。上传十几 MB 需要一两分钟，用较长的超时（命令超时设 10 分钟）。
5. **回报**：发了什么文件、多大、发给谁；如果压缩过，说明画质有损、原画质文件在哪。

## 常见问题

- `535 Username and Password not accepted`：应用专用密码失效或账号未开两步验证 → 请用户到 Google 账号「安全性 → 应用专用密码」重新生成，
  由用户自己写进密码文件（`printf '%s' 'xxxx xxxx xxxx xxxx' > 文件 && chmod 600 文件`，在他们自己的终端里执行）。
- 验证密码能用但不想发信：`send_mail.py --check-login`。
- 文件再压也超过 25 MB（很长的视频）：缩短（只发一段 / 一章）或降到 360p，再不行就告诉用户需要网盘链接。
