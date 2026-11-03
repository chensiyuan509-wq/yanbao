#!/usr/bin/env bash
# 把视频压到能当 Gmail 附件的大小（默认 18 MB；Gmail 上限 25 MB 是按 base64 编码后算的，原文件约 19 MB 以内）。
#   用法：bash fit_for_email.sh 输入.mp4 [目标MB=18] [输出.mp4]
# x264 两遍编码按目标码率压，音频 64k AAC；分辨率不变。
# 提示：带胶片颗粒的视频在低码率下会糊——星火风格的项目先用 `python render.py --grain 0` 出无颗粒版再压。
set -e
IN="$1"; TARGET_MB="${2:-18}"; OUT="${3:-${IN%.*}_mail.mp4}"
[ -f "$IN" ] || { echo "用法：bash fit_for_email.sh 输入.mp4 [目标MB] [输出.mp4]"; exit 1; }
PY="${PYTHON:-python3}"
FF=$("$PY" -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())" 2>/dev/null || command -v ffmpeg || true)
[ -n "$FF" ] || { echo "找不到 ffmpeg（装系统 ffmpeg，或用带 imageio-ffmpeg 的 python：PYTHON=… bash fit_for_email.sh …）"; exit 1; }
DUR=$("$FF" -hide_banner -i "$IN" 2>&1 | sed -n 's/.*Duration: \([0-9:.]*\).*/\1/p' | awk -F: '{print $1*3600+$2*60+$3}')
VK=$(awk -v mb="$TARGET_MB" -v d="$DUR" 'BEGIN{v=int(mb*8192/d-64-8); if(v<100)v=100; print v}')
echo "时长 ${DUR}s → 视频 ${VK}k + 音频 64k（目标约 ${TARGET_MB} MB）"
ABS_IN=$(realpath "$IN"); ABS_OUT=$(realpath -m "$OUT")
TMP=$(mktemp -d); cd "$TMP"
"$FF" -y -hide_banner -loglevel error -i "$ABS_IN" -c:v libx264 -preset slow -b:v ${VK}k -pass 1 -an -f mp4 /dev/null
"$FF" -y -hide_banner -loglevel error -i "$ABS_IN" -c:v libx264 -preset slow -b:v ${VK}k -pass 2 \
  -c:a aac -b:a 64k -movflags +faststart "$ABS_OUT"
cd - >/dev/null; rm -rf "$TMP"
ls -la "$ABS_OUT"
