"""背景音乐：全部用 numpy 现场合成（无版权问题），按章节切换情绪。

- 96 BPM，D 大调；每个场景对应一种"情绪"（和弦进行 + 各声部音量）；
- 声部：铺底 pad、拨弦琶音、低音、轻鼓、铃声点缀；
- 章节交界处 2 秒交叉淡变，和弦始终落在统一的小节线上，听起来是一首连续的曲子。
"""
import math

import numpy as np

SR = 48000
BPM = 96
BEAT = 60 / BPM
BAR = BEAT * 4

# 和弦（MIDI 音高，D 大调）
CH = {
    "D": [62, 66, 69], "A": [57, 61, 64, 69], "Bm": [59, 62, 66], "G": [55, 59, 62, 67],
    "Em": [52, 55, 59, 64], "F#m": [54, 57, 61, 66], "F#": [54, 58, 61, 66], "Dmaj7": [62, 66, 69, 73],
    "Gmaj7": [55, 59, 62, 66], "A/C#": [61, 64, 69], "Asus": [57, 62, 64, 69],
}
ROOT = {"D": 38, "A": 45, "Bm": 47, "G": 43, "Em": 40, "F#m": 42, "F#": 42, "Dmaj7": 38, "Gmaj7": 43,
        "A/C#": 37, "Asus": 45}

# 情绪：和弦进行（每个和弦一小节）+ 声部音量
MOODS = {
    "intro":    (["Dmaj7", "Bm", "Gmaj7", "Asus"], dict(pad=0.85, arp=0.45, bass=0.30, drums=0.0, bell=0.5)),
    "curious":  (["G", "A", "F#m", "Bm"], dict(pad=0.60, arp=0.80, bass=0.45, drums=0.15, bell=0.3)),
    "tech":     (["Bm", "G", "D", "A"], dict(pad=0.50, arp=0.75, bass=0.75, drums=0.60, bell=0.2)),
    "bright":   (["D", "A", "Bm", "G"], dict(pad=0.55, arp=0.85, bass=0.60, drums=0.50, bell=0.3)),
    "us":       (["G", "D", "A", "Bm"], dict(pad=0.60, arp=0.75, bass=0.60, drums=0.55, bell=0.3)),
    "flywheel": (["D", "A", "Bm", "G"], dict(pad=0.50, arp=0.90, bass=0.70, drums=0.70, bell=0.2)),
    "china":    (["Bm", "G", "Em", "F#"], dict(pad=0.85, arp=0.35, bass=0.45, drums=0.0, bell=0.25)),
    "open":     (["Em", "G", "D", "A"], dict(pad=0.70, arp=0.55, bass=0.50, drums=0.25, bell=0.3)),
    "warm":     (["D", "F#m", "G", "A"], dict(pad=0.70, arp=0.75, bass=0.55, drums=0.40, bell=0.35)),
    "ending":   (["G", "A", "Bm", "G", "Em", "A", "D", "D"],
                 dict(pad=0.95, arp=0.80, bass=0.60, drums=0.45, bell=0.5)),
}

SCENE_MOOD = {
    "s01_intro": "intro", "s02_paper": "curious", "s03_gpt": "curious", "s04_cuda": "tech",
    "s05_asic": "tech", "s06_fab": "tech", "s07_products": "bright", "s08_coop": "us",
    "s09_capital": "us", "s10_flywheel": "flywheel", "s11_china": "china", "s12_walls": "china",
    "s13_open": "open", "s14_work": "warm", "s15_life": "warm", "s16_ending": "ending",
}


def _f(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def _rng(seed):
    return np.random.default_rng(seed)


# ---------------------------------------------------------------- 乐器

_TABLE_N = 2048
_ph = np.arange(_TABLE_N) / _TABLE_N
_PAD_TABLE = sum((1 / n ** 1.7) * np.sin(2 * np.pi * n * _ph) for n in range(1, 8))
_PAD_TABLE /= np.max(np.abs(_PAD_TABLE))


def pad_note(m, dur, cents=0.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = _f(m) * 2 ** (cents / 1200)
    phase = (f * t) % 1.0
    x = np.interp(phase * _TABLE_N, np.arange(_TABLE_N + 1), np.append(_PAD_TABLE, _PAD_TABLE[0]))
    att, rel = 0.45, 0.8
    env = np.minimum(1, t / att) * np.clip((dur - t) / rel, 0, 1)
    return (x * env * (0.85 + 0.15 * np.sin(2 * np.pi * 0.3 * t))).astype(np.float32)


def pluck(m, vel=1.0, dur=0.9):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = _f(m)
    x = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) * np.exp(-t * 9) + \
        0.12 * np.sin(6 * np.pi * f * t) * np.exp(-t * 14)
    env = np.exp(-t * 5.5) * np.minimum(1, t / 0.004)
    return (x * env * vel).astype(np.float32)


def bass_note(m, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = _f(m)
    x = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t)
    x = np.tanh(1.4 * x)
    env = np.exp(-t * 2.6) * np.minimum(1, t / 0.01) * np.clip((dur - t) / 0.05, 0, 1)
    return (x * env).astype(np.float32)


def kick():
    d = 0.32
    t = np.arange(int(d * SR)) / SR
    f = 46 + 110 * np.exp(-t * 32)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11)
    return x.astype(np.float32)


def hat(seed):
    d = 0.06
    t = np.arange(int(d * SR)) / SR
    x = _rng(seed).standard_normal(len(t))
    x = np.diff(np.concatenate([[0], x]))           # 简单高通
    return (x * np.exp(-t * 70) * 0.5).astype(np.float32)


def snap(seed):
    d = 0.16
    t = np.arange(int(d * SR)) / SR
    x = _rng(seed).standard_normal(len(t))
    x = x - np.convolve(x, np.ones(6) / 6, mode="same")
    return (x * np.exp(-t * 26) * 0.6).astype(np.float32)


def bell(m, dur=2.0):
    t = np.arange(int(dur * SR)) / SR
    f = _f(m)
    mod = 1.2 * np.exp(-t * 3) * np.sin(2 * np.pi * f * 3.5 * t)
    x = np.sin(2 * np.pi * f * t + mod) * np.exp(-t * 2.2)
    return (x * np.minimum(1, t / 0.003)).astype(np.float32)


# ---------------------------------------------------------------- 编曲


def _add(bus, i0, sig, gain, pan=0.0):
    if i0 >= bus.shape[1] or gain <= 1e-4:
        return
    if i0 < 0:
        sig = sig[-i0:]
        i0 = 0
    n = min(len(sig), bus.shape[1] - i0)
    th = (pan + 1) * math.pi / 4
    bus[0, i0:i0 + n] += sig[:n] * gain * math.cos(th)
    bus[1, i0:i0 + n] += sig[:n] * gain * math.sin(th)


def _gain_curve(scene_spans, layer, n):
    """每个声部随时间变化的音量（章节交界 2 秒交叉淡变）。"""
    g = np.zeros(n, dtype=np.float32)
    t = np.arange(n) / SR
    for (a, b, mood) in scene_spans:
        v = MOODS[mood][1][layer]
        w = np.clip((t - (a - 1.0)) / 2.0, 0, 1) * np.clip(((b + 1.0) - t) / 2.0, 0, 1)
        g += (v * w).astype(np.float32)
    return g


def build_music(duration, scene_spans, seed=3):
    """scene_spans: [(开始, 结束, 场景名)] → 立体声 float32 数组 (2, n)。"""
    n = int(math.ceil(duration * SR))
    spans = [(a, b, SCENE_MOOD.get(name, "bright")) for (a, b, name) in scene_spans]
    layers = {k: np.zeros((2, n), dtype=np.float32) for k in ("pad", "arp", "bass", "drums", "bell")}
    R = _rng(seed)
    nbars = int(math.ceil(duration / BAR)) + 1
    # 每个情绪段从段首所在小节开始数和弦
    mood_start_bar = {}
    for (a, b, mood) in spans:
        mood_start_bar.setdefault((mood, round(a, 2)), int(round(a / BAR)))

    def mood_at(t):
        for (a, b, mood) in spans:
            if a <= t < b:
                return mood, int(round(a / BAR))
        return spans[-1][2], int(round(spans[-1][0] / BAR))

    for bi in range(nbars):
        t0 = bi * BAR
        if t0 >= duration:
            break
        mood, sb = mood_at(t0 + 0.01)
        prog = MOODS[mood][0]
        name = prog[(bi - sb) % len(prog)]
        chord = CH[name]
        i0 = int(t0 * SR)
        for j, m in enumerate(chord):
            for c, pan in ((-5, -0.35), (5, 0.35)):
                _add(layers["pad"], i0, pad_note(m, BAR + 0.9, c), 0.16, pan)
        # 琶音：八分音符
        pattern = [0, 1, 2, 1, 2, 3, 2, 1]
        tones = sorted(chord) + [chord[0] + 12]
        for k in range(8):
            m = tones[pattern[k] % len(tones)] + 12
            if mood == "china" and k % 2 == 1:
                continue
            vel = 0.55 + 0.25 * (k % 4 == 0) + R.uniform(-0.08, 0.08)
            _add(layers["arp"], i0 + int(k * BEAT / 2 * SR), pluck(m, vel), 0.16,
                 -0.3 if k % 2 == 0 else 0.3)
        # 低音：每拍根音，第 3 拍五度
        root = ROOT[name]
        for k in range(4):
            m = root + (7 if k == 2 else 0)
            _add(layers["bass"], i0 + int(k * BEAT * SR), bass_note(m, BEAT * 0.95), 0.32, 0.0)
        # 鼓：1、3 拍底鼓，2、4 拍响指，八分音符踩镲
        for k in range(4):
            ik = i0 + int(k * BEAT * SR)
            if k in (0, 2):
                _add(layers["drums"], ik, kick(), 0.55)
            else:
                _add(layers["drums"], ik, snap(bi * 7 + k), 0.18, 0.15)
            for h in range(2):
                _add(layers["drums"], ik + int(h * BEAT / 2 * SR), hat(bi * 13 + k * 2 + h), 0.10, -0.2)
        # 铃声：每两小节一次
        if bi % 2 == 0:
            _add(layers["bell"], i0, bell(max(chord) + 12, 2.5), 0.1, 0.25)

    mix = np.zeros((2, n), dtype=np.float32)
    for k, bus in layers.items():
        g = _gain_curve(spans, k, n)
        mix += bus * g
    # 片头淡入、片尾淡出
    t = np.arange(n) / SR
    mix *= np.clip(t / 2.5, 0, 1) * np.clip((duration - t) / 3.0, 0, 1)
    return mix
