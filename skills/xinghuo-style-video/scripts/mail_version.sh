#!/usr/bin/env bash
# 做一份能发邮件的小文件（Gmail 附件上限 25 MB，base64 后 ≈ 19 MB 原文件）：
#   关掉胶片颗粒重渲染（颗粒在低码率下会糊成一片），再用 x264 两遍编码按目标大小压。
#   用法：在项目目录里  bash <skill>/scripts/mail_version.sh [目标MB，默认 18]
set -e
TARGET_MB="${1:-18}"
PY="${PYTHON:-python}"
SLUG=$("$PY" -c "from aivid import project; print(project.SLUG)")
DUR=$("$PY" -c "from aivid.timeline import DURATION; print(DURATION)")
"$PY" render.py --grain 0 --out "out/${SLUG}_480p_nograin.mp4"
FF=$("$PY" -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
VK=$("$PY" -c "print(max(120, int($TARGET_MB * 8192 / $DUR - 64 - 8)))")
echo "视频码率 ${VK}k + 音频 64k（${DUR}s → 约 ${TARGET_MB} MB）"
TMP=$(mktemp -d)
cd "$TMP"
"$FF" -y -hide_banner -loglevel error -i "$OLDPWD/out/${SLUG}_480p_nograin.mp4" -c:v libx264 -preset slow -b:v ${VK}k -pass 1 -an -f mp4 /dev/null
"$FF" -y -hide_banner -loglevel error -i "$OLDPWD/out/${SLUG}_480p_nograin.mp4" -c:v libx264 -preset slow -b:v ${VK}k -pass 2 \
  -c:a aac -b:a 64k -movflags +faststart "$OLDPWD/out/${SLUG}_480p_mail.mp4"
cd "$OLDPWD"; rm -rf "$TMP"
ls -la "out/${SLUG}_480p_mail.mp4"
