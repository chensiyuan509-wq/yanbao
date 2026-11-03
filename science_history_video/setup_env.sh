#!/usr/bin/env bash
# 一键建虚拟环境 .venv：复用系统自带的 pycairo，再装 numpy、imageio-ffmpeg（自带 ffmpeg）、Pillow
set -e
cd "$(dirname "$0")"
PY="${PYTHON:-/usr/bin/python3}"

if ! "$PY" -c "import cairo" 2>/dev/null; then
  echo "提示：$PY 里没有 pycairo。请先执行 sudo apt install python3-cairo"
  echo "      （或 sudo apt install libcairo2-dev pkg-config 后，在虚拟环境里 pip install pycairo）"
fi

if command -v uv >/dev/null 2>&1; then
  uv venv -p "$PY" --system-site-packages .venv
  uv pip install --python .venv/bin/python -r requirements.txt
else
  "$PY" -m venv --system-site-packages .venv
  .venv/bin/python -m pip install -r requirements.txt
fi

.venv/bin/python -c "import cairo, numpy, imageio_ffmpeg; print('环境就绪：pycairo', cairo.version, '| numpy', numpy.__version__, '| ffmpeg', imageio_ffmpeg.get_ffmpeg_version())"
fc-list ':lang=zh' family 2>/dev/null | grep -q "Noto Sans CJK SC" && echo "字体就绪：Noto Sans CJK SC" || echo "提示：未找到 Noto Sans CJK SC，请 sudo apt install fonts-noto-cjk"
echo "下一步：source .venv/bin/activate && python render.py"
