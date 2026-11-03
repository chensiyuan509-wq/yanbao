# Claude Code skills（备份）

| skill | 用途 |
|---|---|
| `xinghuo-style-video/` | 视频制作：保持星火的风格与质量标准（参考，不照搬）；引擎、89 张授权历史图像、空白占位脚手架、风格 / 运镜 / 叙事 / 音效 / 素材规范 |
| `instagram-reels/` | 横版成片 → Instagram 竖版（Reels 9:16 / 动态 4:5），带标题条、封面、配文草稿 |
| `youtube-publish/` | YouTube 上传物料（标题、章节简介、标签、字幕、封面）与 API 上传（账号认证后再用） |
| `gmail-send/` | 用 Gmail 把文件（成片）发到邮箱，超过 25 MB 先压缩 |

凭据都不在这里：Gmail 的配置在 `~/.config/gmail-send/`，YouTube 的 OAuth 文件在 `~/.config/youtube-publish/`，均只存在本机。

安装 / 恢复到本机（Claude Code 会自动发现 `~/.claude/skills/` 下的 skill）：

```bash
mkdir -p ~/.claude/skills
for s in xinghuo-style-video instagram-reels youtube-publish gmail-send; do rsync -a skills/$s/ ~/.claude/skills/$s/; done
```

在本机改了 skill 之后，同步回仓库：

```bash
for s in xinghuo-style-video instagram-reels youtube-publish gmail-send; do
  rsync -a --delete --exclude '__pycache__' ~/.claude/skills/$s/ skills/$s/
done
```
