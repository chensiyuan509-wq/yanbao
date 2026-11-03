"""项目配置：片名、输出文件名前缀、目标时长、章节数。新项目由 scripts/new_project.py 生成这份文件。"""
TITLE = "星火：人类科学简史"     # 片名（render.py 的说明里用）
SLUG = "xinghuo"                  # 输出文件名前缀：out/<SLUG>_480p.mp4
TARGET_SEC = 480.0                # 目标总时长（秒），check.py 会核对
CHAPTERS = 8                      # 章节标题（CHAPTER 不为 None 的场景）个数，check.py 会核对
