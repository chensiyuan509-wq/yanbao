# Claude Code skills（备份）

| skill | 用途 |
|---|---|
| `xinghuo-style-video/` | 星火风格的电影感讲解视频：引擎、89 张授权历史图像、场景模板、风格 / 运镜 / 叙事 / 音效 / 发布（YouTube、Instagram）规则 |

安装 / 恢复到本机（Claude Code 会自动发现 `~/.claude/skills/` 下的 skill）：

```bash
mkdir -p ~/.claude/skills && rsync -a skills/xinghuo-style-video/ ~/.claude/skills/xinghuo-style-video/
```

在本机改了 skill 之后，同步回仓库：

```bash
rsync -a --delete --exclude '__pycache__' ~/.claude/skills/xinghuo-style-video/ skills/xinghuo-style-video/
```
