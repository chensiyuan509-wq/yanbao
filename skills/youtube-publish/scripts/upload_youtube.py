#!/usr/bin/env python3
"""YouTube 上传（YouTube Data API v3，OAuth）。默认只做检查，不上传。

  python upload_youtube.py out/youtube/metadata.json                 # 检查（默认）：文件、元数据、凭据是否就位
  python upload_youtube.py --auth-only                               # 只做 OAuth 授权并显示频道名（需要浏览器）
  python upload_youtube.py out/youtube/metadata.json --upload        # 真正上传（隐私按 metadata，默认 private）
  python upload_youtube.py out/youtube/metadata.json --upload --privacy unlisted
  python upload_youtube.py --set-privacy <视频ID> public             # 审核过后再公开

凭据（不在 skill 里、不进 git）：
  ~/.config/youtube-publish/client_secret.json   Google Cloud 里创建的"桌面应用"OAuth 客户端
  ~/.config/youtube-publish/token.json           首次授权后自动生成
依赖：pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
"""
import argparse
import json
import os
import sys
import time

CONF = os.path.expanduser("~/.config/youtube-publish")
SECRET = os.path.join(CONF, "client_secret.json")
TOKEN = os.path.join(CONF, "token.json")
SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.force-ssl"]


def need_libs():
    try:
        import googleapiclient  # noqa: F401
        import google_auth_oauthlib  # noqa: F401
        return True
    except ImportError:
        return False


def service():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    creds = Credentials.from_authorized_user_file(TOKEN, SCOPES) if os.path.exists(TOKEN) else None
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        if not os.path.exists(SECRET):
            sys.exit(f"缺少 {SECRET}：先按 references/setup-auth.md 创建 OAuth 客户端")
        flow = InstalledAppFlow.from_client_secrets_file(SECRET, SCOPES)
        creds = flow.run_local_server(port=0, open_browser=True)
        os.makedirs(CONF, exist_ok=True)
        with open(TOKEN, "w") as f:
            f.write(creds.to_json())
        os.chmod(TOKEN, 0o600)
    return build("youtube", "v3", credentials=creds)


def check(meta_path):
    ok = True
    print("凭据")
    print(f"  {'✓' if need_libs() else '✗'} Python 依赖（google-api-python-client、google-auth-oauthlib）")
    print(f"  {'✓' if os.path.exists(SECRET) else '✗'} OAuth 客户端 {SECRET}")
    print(f"  {'✓' if os.path.exists(TOKEN) else '·'} 授权令牌 {TOKEN}{'' if os.path.exists(TOKEN) else '（首次上传时在浏览器里授权后生成）'}")
    if meta_path and not os.path.exists(meta_path):
        print(f"✗ 没有 {meta_path}：先在项目目录里运行 prepare_youtube.py")
        return False
    if meta_path:
        m = json.load(open(meta_path, encoding="utf-8"))
        print("物料")
        for label, p in (("视频", m.get("video")), ("封面", m.get("thumbnail")), ("字幕", (m.get("captions") or {}).get("file"))):
            exists = bool(p) and os.path.exists(p)
            ok &= exists or label != "视频"
            size = f"{os.path.getsize(p) / 1e6:.1f} MB" if exists else "缺失"
            print(f"  {'✓' if exists else '✗'} {label}：{p}（{size}）")
        sn, st = m["snippet"], m["status"]
        print(f"  标题：{sn['title']}")
        print(f"  隐私：{st['privacyStatus']}  分类：{sn['categoryId']}  语言：{sn.get('defaultLanguage')}")
    print("（检查模式：没有上传任何东西。真正上传要加 --upload，且必须是用户明确要求的。）")
    return ok


def upload(meta_path, privacy=None):
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
    m = json.load(open(meta_path, encoding="utf-8"))
    if privacy:
        m["status"]["privacyStatus"] = privacy
    yt = service()
    body = {"snippet": m["snippet"], "status": m["status"]}
    media = MediaFileUpload(m["video"], chunksize=8 * 1024 * 1024, resumable=True, mimetype="video/mp4")
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp, last = None, -1
    print(f"上传 {os.path.basename(m['video'])}（{os.path.getsize(m['video']) / 1e6:.1f} MB，隐私：{m['status']['privacyStatus']}）")
    while resp is None:
        try:
            status, resp = req.next_chunk()
        except HttpError as e:
            if e.resp.status in (500, 502, 503, 504):
                time.sleep(5)
                continue
            raise
        if status and int(status.progress() * 100) // 10 != last:
            last = int(status.progress() * 100) // 10
            print(f"  {status.progress() * 100:.0f}%", flush=True)
    vid = resp["id"]
    print(f"✓ 视频已上传：https://youtu.be/{vid}   Studio：https://studio.youtube.com/video/{vid}/edit")
    result = {"id": vid, "privacy": m["status"]["privacyStatus"], "time": time.strftime("%Y-%m-%d %H:%M:%S")}
    if m.get("thumbnail") and os.path.exists(m["thumbnail"]):
        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(m["thumbnail"], mimetype="image/jpeg")).execute()
            print("✓ 封面已设置")
            result["thumbnail"] = True
        except HttpError as e:
            print(f"! 封面没设上（{e.resp.status}）：自定义封面需要频道完成手机验证；可以之后在 Studio 里手动换。")
    cap = m.get("captions") or {}
    if cap.get("file") and os.path.exists(cap["file"]):
        try:
            yt.captions().insert(part="snippet", body={"snippet": {"videoId": vid, "language": cap.get("language", "zh-Hans"),
                                                                    "name": cap.get("name", "中文"), "isDraft": False}},
                                 media_body=MediaFileUpload(cap["file"], mimetype="application/octet-stream")).execute()
            print("✓ 字幕已上传")
            result["captions"] = True
        except HttpError as e:
            print(f"! 字幕没传上（{e.resp.status}），可以之后在 Studio 里手动上传 captions.srt")
    json.dump(result, open(os.path.join(os.path.dirname(meta_path), "upload_result.json"), "w"), indent=2)
    return vid


def main():
    ap = argparse.ArgumentParser(description="YouTube 上传（默认只检查）")
    ap.add_argument("meta", nargs="?")
    ap.add_argument("--upload", action="store_true", help="真正上传")
    ap.add_argument("--privacy", choices=["private", "unlisted", "public"])
    ap.add_argument("--auth-only", action="store_true")
    ap.add_argument("--set-privacy", nargs=2, metavar=("VIDEO_ID", "PRIVACY"))
    a = ap.parse_args()
    if a.auth_only or a.upload or a.set_privacy:
        if not need_libs():
            sys.exit("缺少依赖：pip install google-api-python-client google-auth-oauthlib google-auth-httplib2")
    if a.auth_only:
        ch = service().channels().list(part="snippet", mine=True).execute().get("items", [])
        print("授权成功 ✓ 频道：" + (ch[0]["snippet"]["title"] if ch else "（这个账号还没有频道）"))
        return
    if a.set_privacy:
        vid, pv = a.set_privacy
        service().videos().update(part="status", body={"id": vid, "status": {"privacyStatus": pv}}).execute()
        print(f"✓ {vid} → {pv}")
        return
    if not a.meta:
        sys.exit(__doc__)
    if a.upload:
        upload(a.meta, a.privacy)
    else:
        sys.exit(0 if check(a.meta) else 1)


if __name__ == "__main__":
    main()
