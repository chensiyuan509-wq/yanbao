"""字幕文案：切分小句、估算显示时长。视频没有人声旁白，文案只以字幕形式出现在画面上。

各场景用 VO = [(本地开始秒, "文案，{高亮}"), ...] 写字幕。
"""
import re

FPS = 30

_PUNCT_END = "，。；：、,;:"
_BREAKS = "，。；：！？…,;:!?"


def plain(s):
    return s.replace("{", "").replace("}", "")


def count_units(s):
    """估算朗读"音节量"：汉字 1，英文单词约 1.6，数字每位 0.7。"""
    s = plain(s)
    cjk = len(re.findall("[\\u4e00-\\u9fff]", s))
    words = re.findall(r"[A-Za-z][A-Za-z\-\.']*", s)
    latin = sum(1.0 + 0.25 * max(0, len(w) - 4) / 2 for w in words)
    digits = len(re.findall(r"\d", s))
    pauses = len(re.findall(r"[，。；：！？、,;:!?]", s))
    return cjk + latin * 1.6 + digits * 0.7 + pauses * 0.6


def estimate(s):
    """估算正常语速读完这句的时长（秒），字幕按它再加阅读余量。"""
    s = plain(s)
    cjk = len(re.findall("[\\u4e00-\\u9fff]", s))
    words = re.findall(r"[A-Za-z][A-Za-z\-\.']*", s)
    digits = len(re.findall(r"\d", s))
    pauses = len(re.findall(r"[，。；：！？、,;:!?]", s))
    d = 0.163 * cjk + 0.436 * len(words) + 0.013 * sum(len(w) for w in words) + 0.167 * digits + \
        0.369 * pauses - 0.155
    return max(0.6, d)


# ---------------------------------------------------------------- 字幕切分


def split_clauses(s, max_len=20, min_len=6):
    """把一句旁白按标点切成适合屏幕的字幕小句（保留 {高亮}，去掉句末的逗号句号）。"""
    parts, buf = [], ""
    for i, ch in enumerate(s):
        buf += ch
        nxt = s[i + 1] if i + 1 < len(s) else ""
        if ch in _BREAKS and not (ch == "…" and nxt == "…") and nxt not in "」》）}":
            parts.append(buf)
            buf = ""
    if buf.strip():
        parts.append(buf)
    # 合并太短的小句
    merged = []
    for p in parts:
        if merged and (len(plain(merged[-1])) < min_len or len(plain(p)) < min_len - 2) and \
                len(plain(merged[-1] + p)) <= max_len:
            merged[-1] += p
        else:
            merged.append(p)
    # 拆开太长的小句（在顿号、空格处，或者硬切）
    out = []
    for p in merged:
        while len(plain(p)) > max_len + 6:
            cut = _soft_cut(p, max_len)
            out.append(p[:cut])
            p = p[cut:]
        out.append(p)
    # 修补被拆开的高亮括号
    fixed, carry = [], False
    for p in out:
        if carry:
            p = "{" + p
        opens, closes = p.count("{"), p.count("}")
        carry = opens > closes
        if carry:
            p = p + "}"
        fixed.append(p)
    return [c for c in fixed if plain(c).strip(_PUNCT_END + " ")]


def _soft_cut(p, max_len):
    vis = 0
    best = None
    for i, ch in enumerate(p):
        if ch not in "{}":
            vis += 1
        if vis >= max_len * 0.5 and ch in "、 " and vis <= max_len + 2:
            best = i + 1
        if vis > max_len + 2:
            break
    if best:
        return best
    vis = 0
    for i, ch in enumerate(p):
        if ch not in "{}":
            vis += 1
        if vis >= max_len:
            return i + 1
    return len(p)


def display(c):
    """字幕显示文本：去掉句末的逗号、句号、分号、冒号。"""
    c = c.strip()
    while c and c[-1] in _PUNCT_END:
        c = c[:-1]
    if c.endswith("}") and len(c) > 1 and c[-2] in _PUNCT_END:
        c = c[:-2] + "}"
    return c.strip()


def estimate_cues(text, t0, dur):
    """按字数比例估算每个小句的时间。"""
    cl = split_clauses(text)
    w = [max(1.0, count_units(c)) for c in cl]
    tot = sum(w)
    out, acc = [], t0
    for c, wi in zip(cl, w):
        d = dur * wi / tot
        out.append((acc, acc + d, display(c)))
        acc += d
    return out


# ---------------------------------------------------------------- 口型（已停用）

CUR = [0.0]       # 当前正在绘制的场景在全片中的开始时间（render 每帧设置）


def speech(t):
    """没有人声，说话音量恒为 0。"""
    return 0.0
