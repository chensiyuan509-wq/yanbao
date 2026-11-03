#!/usr/bin/env python3
"""用 Gmail 把文件当附件发出去（只用 Python 标准库，不用安装任何东西）。

  python3 send_mail.py 你的Gmail地址 收件地址 文件路径

密码优先从上一级目录的 .gmail_app_password 读取（已在 .git/info/exclude 里忽略，不会被提交）；
没有这个文件时，才提示输入 Gmail 的"应用专用密码"（16 位，输入时不显示）。
"""
import getpass
import mimetypes
import os
import smtplib
import sys
from email.message import EmailMessage


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    user, to, path = sys.argv[1:]
    size = os.path.getsize(path)
    if size * 4 / 3 > 25 * 1024 * 1024:
        sys.exit(f"文件 {size / 1e6:.1f} MB，编码后会超过 Gmail 的 25 MB 上限，请换小一点的文件。")
    pw_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".gmail_app_password")
    if os.path.exists(pw_file):
        with open(pw_file) as f:
            pw = f.read().strip().replace(" ", "")
    else:
        pw = getpass.getpass("Gmail 应用专用密码：").replace(" ", "")

    msg = EmailMessage()
    msg["From"], msg["To"] = user, to
    msg["Subject"] = os.path.basename(path)
    msg.set_content("视频见附件。")
    ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
    main_t, sub_t = ctype.split("/", 1)
    with open(path, "rb") as f:
        msg.add_attachment(f.read(), maintype=main_t, subtype=sub_t, filename=os.path.basename(path))

    print(f"正在发送 {size / 1e6:.1f} MB …（上传需要一点时间）")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=600) as s:
        s.login(user, pw)
        s.send_message(msg)
    print("已发送 ✓")


if __name__ == "__main__":
    main()
