#!/usr/bin/env python3
"""用 Gmail（SMTP + 应用专用密码）把文件当附件发出去。只用 Python 标准库。

  python send_mail.py 文件 [文件 …] [--to 收件人] [--from 发件人] [--subject 标题] [--body 正文]
  python send_mail.py 文件 --check          # 只检查：配置、密码文件、附件大小（不连服务器、不发送）
  python send_mail.py --check-login         # 只登录一次 SMTP 验证密码可用（不发送）

配置（不在 skill 里，在本机）：~/.config/gmail-send/config.json
    {"user": "发件 Gmail", "to": "默认收件人", "password_file": "应用专用密码文件路径"}
密码查找顺序：环境变量 GMAIL_APP_PASSWORD_FILE → config 里的 password_file → ~/.config/gmail-send/app_password。
密码绝不打印、绝不写进日志；找不到文件时才在终端里提示输入（输入不回显）。
"""
import argparse
import getpass
import json
import mimetypes
import os
import smtplib
import sys
from email.message import EmailMessage

CONF_DIR = os.path.expanduser("~/.config/gmail-send")
LIMIT = 25 * 1024 * 1024          # Gmail 附件上限（按 base64 编码后计算）


def load_conf():
    p = os.path.join(CONF_DIR, "config.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def password_path(conf):
    for p in (os.environ.get("GMAIL_APP_PASSWORD_FILE"), conf.get("password_file"),
              os.path.join(CONF_DIR, "app_password")):
        if p and os.path.exists(os.path.expanduser(p)):
            return os.path.expanduser(p)
    return None


def read_password(conf):
    p = password_path(conf)
    if p:
        with open(p) as f:
            return f.read().strip().replace(" ", "")
    if not sys.stdin.isatty():
        sys.exit("找不到应用专用密码文件，且当前不是交互终端，无法输入。请先按 SKILL.md 配置密码文件。")
    return getpass.getpass("Gmail 应用专用密码（16 位，输入不显示）：").replace(" ", "")


def encoded_size(paths):
    return sum(os.path.getsize(p) for p in paths) * 4 / 3 + 64 * 1024


def main():
    conf = load_conf()
    ap = argparse.ArgumentParser(description="Gmail 发送附件")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--to", default=conf.get("to"))
    ap.add_argument("--from", dest="user", default=conf.get("user"))
    ap.add_argument("--subject", default=None)
    ap.add_argument("--body", default="文件见附件。")
    ap.add_argument("--check", action="store_true", help="只检查，不发送")
    ap.add_argument("--check-login", action="store_true", help="只验证能否登录 SMTP，不发送")
    a = ap.parse_args()

    if not a.user:
        sys.exit("没有发件人：在 ~/.config/gmail-send/config.json 里写 user，或加 --from")
    if a.check_login:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=60) as s:
            s.login(a.user, read_password(conf))
        print(f"登录成功 ✓（{a.user}）")
        return
    if not a.files:
        sys.exit("没有附件")
    if not a.to:
        sys.exit("没有收件人：在 config.json 里写 to，或加 --to")
    for p in a.files:
        if not os.path.isfile(p):
            sys.exit(f"找不到文件：{p}")
    enc = encoded_size(a.files)
    raw = sum(os.path.getsize(p) for p in a.files)
    if enc > LIMIT:
        sys.exit(f"附件共 {raw / 1e6:.1f} MB，编码后约 {enc / 1e6:.1f} MB，超过 Gmail 25 MB 上限。"
                 f"视频请先用 fit_for_email.sh 压到 18 MB 左右。")
    if a.check:
        pw = password_path(conf)
        print(f"发件人 {a.user} → 收件人 {a.to}")
        print(f"附件 {len(a.files)} 个，共 {raw / 1e6:.1f} MB（编码后约 {enc / 1e6:.1f} MB，上限 25 MB）✓")
        print(f"密码文件：{'已找到' if pw else '未找到（发送时会提示输入）'}")
        return

    msg = EmailMessage()
    msg["From"], msg["To"] = a.user, a.to
    msg["Subject"] = a.subject or "、".join(os.path.basename(p) for p in a.files)
    msg.set_content(a.body)
    for p in a.files:
        ctype = mimetypes.guess_type(p)[0] or "application/octet-stream"
        main_t, sub_t = ctype.split("/", 1)
        with open(p, "rb") as f:
            msg.add_attachment(f.read(), maintype=main_t, subtype=sub_t, filename=os.path.basename(p))
    print(f"正在发送 {raw / 1e6:.1f} MB → {a.to} …（上传需要一点时间）", flush=True)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=900) as s:
        s.login(a.user, read_password(conf))
        s.send_message(msg)
    print("已发送 ✓")


if __name__ == "__main__":
    main()
