"""配乐与音效：全部用 numpy 合成（无需任何外部素材）。"""
import math
import wave

import numpy as np

SR = 44100
DUR = 180.0
N = int(SR * DUR)
RNG = np.random.default_rng(7)


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def _add(buf, start, sig, pan=0.0, gain=1.0):
    """把单声道 sig 加到立体声 buf（等功率声像）。"""
    i0 = int(start * SR)
    if i0 >= N or len(sig) == 0:
        return
    if i0 < 0:
        sig = sig[-i0:]
        i0 = 0
    n = min(len(sig), N - i0)
    th = (pan + 1) * math.pi / 4
    buf[0, i0:i0 + n] += sig[:n] * math.cos(th) * gain
    buf[1, i0:i0 + n] += sig[:n] * math.sin(th) * gain


def _t(dur):
    return np.arange(int(dur * SR)) / SR


def adsr(n, a, r, sr=SR):
    env = np.ones(n)
    na, nr = int(a * sr), int(r * sr)
    if na > 0:
        env[:na] = np.linspace(0, 1, na) ** 1.5
    if nr > 0:
        env[-nr:] *= np.linspace(1, 0, nr) ** 1.5
    return env


def onepole_lp(x, cutoff):
    """一阶低通（cutoff 可为数组，实现扫频）。"""
    c = np.broadcast_to(np.asarray(cutoff, dtype=float), x.shape)
    a = 1 - np.exp(-2 * np.pi * c / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):  # 只用于短音效
        acc += a[i] * (x[i] - acc)
        y[i] = acc
    return y


def fft_lowpass(x, cutoff):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / cutoff) ** 4)
    return np.fft.irfft(X, len(x))


# ---------------------------------------------------------------- 乐器


def pad_note(freq, dur, a=1.6, r=2.0, bright=5):
    t = _t(dur + r)
    sig = np.zeros_like(t)
    for det in (-0.004, 0.0, 0.0042):
        f = freq * (1 + det)
        for h in range(1, bright + 1):
            sig += np.sin(2 * np.pi * f * h * t + h * 1.3) / h ** 1.6
    lfo = 1 + 0.15 * np.sin(2 * np.pi * 0.23 * t)
    return sig * adsr(len(t), a, r) * lfo / 3.0


def bass_note(freq, dur, r=1.2):
    t = _t(dur + r)
    sig = np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(4 * np.pi * freq * t)
    return sig * adsr(len(t), 0.4, r)


def bell(freq, dur=2.2, idx=2.2, ratio=3.5):
    t = _t(dur)
    env = np.exp(-t * 2.6)
    mod = idx * np.exp(-t * 5) * np.sin(2 * np.pi * freq * ratio * t)
    sig = np.sin(2 * np.pi * freq * t + mod) * env
    sig[: int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
    return sig


def click(freq=1500, dur=0.06, noise=0.6):
    t = _t(dur)
    sig = np.sin(2 * np.pi * freq * t) * np.exp(-t * 90)
    sig += noise * RNG.standard_normal(len(t)) * np.exp(-t * 160)
    return sig


def ping(freq, dur=0.5):
    t = _t(dur)
    return (np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 2.01 * t)) * np.exp(-t * 9)


def whoosh(dur=1.0, peak=0.5):
    n = int(dur * SR)
    x = RNG.standard_normal(n)
    t = np.arange(n) / n
    env = np.where(t < peak, (t / peak) ** 2, ((1 - t) / (1 - peak)) ** 1.5)
    cut = 300 + 3500 * env
    return onepole_lp(x, cut) * env * 1.6


def boom(dur=2.5, f0=110, f1=32):
    t = _t(dur)
    f = f1 + (f0 - f1) * np.exp(-t * 3)
    ph = 2 * np.pi * np.cumsum(f) / SR
    sig = np.sin(ph) * np.exp(-t * 1.4)
    nz = fft_lowpass(RNG.standard_normal(len(t)), 400) * np.exp(-t * 5) * 2.5
    return sig + nz


def boing(f0=280, f1=620, dur=0.28):
    t = _t(dur)
    f = f0 + (f1 - f0) * (t / dur) ** 0.6
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.sin(np.pi * t / dur) ** 0.7


def shimmer(dur=1.2, f0=600, f1=2400):
    t = _t(dur)
    sig = np.zeros_like(t)
    for k in range(10):
        st = k / 10 * dur * 0.7
        f = f0 * (f1 / f0) ** (k / 9)
        i0 = int(st * SR)
        bb = bell(f, dur - st, 1.2, 2.0)
        sig[i0:i0 + len(bb)] += bb[: len(sig) - i0] * 0.5
    return sig


def shatter(dur=1.4):
    t = _t(dur)
    sig = fft_lowpass(RNG.standard_normal(len(t)), 6000) * np.exp(-t * 18) * 1.4
    for k in range(26):
        st = RNG.uniform(0, 0.5)
        f = RNG.uniform(2500, 7000)
        i0 = int(st * SR)
        tt = t[: len(t) - i0]
        sig[i0:] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * RNG.uniform(18, 40)) * 0.35
    return sig


# ---------------------------------------------------------------- 和声

CH = {
    "Cmaj9": [36, 48, 55, 59, 62, 64],
    "Am9": [33, 45, 52, 55, 59, 60],
    "Fmaj9": [29, 41, 48, 52, 55, 57],
    "G6sus": [31, 43, 50, 55, 57, 60],
    "Em7": [28, 40, 47, 50, 55, 59],
    "Dm9": [26, 38, 45, 48, 52, 53],
    "Bbmaj7": [34, 46, 53, 57, 58, 62],
    "Cdark": [24, 36, 43, 51, 55, 60],
    "Ebmaj7": [27, 39, 46, 50, 55, 58],
}


def chord_plan():
    plan = [(0.0, 6.0, "Cmaj9"), (6.0, 6.2, "Am9"), (12.2, 8.2, "Em7")]
    t = 20.4
    sections = [
        (63.0, ["Fmaj9", "G6sus", "Em7", "Am9"]),
        (100.0, ["Fmaj9", "Em7", "Dm9", "Cmaj9"]),
        (138.0, ["Am9", "Fmaj9", "Cmaj9", "G6sus"]),
        (155.0, ["Dm9", "Bbmaj7", "Fmaj9", "Cmaj9"]),
    ]
    for end, prog_ in sections:
        k = 0
        while t < end - 0.01:
            d = min(4.0, end - t)
            plan.append((t, d, prog_[k % 4]))
            t += d
            k += 1
    plan += [(155.0, 5.0, "Cdark"), (160.0, 5.0, "Ebmaj7"),
             (165.0, 3.5, "Fmaj9"), (168.5, 3.5, "G6sus"), (172.0, 2.4, "Am9"),
             (174.4, 2.4, "Fmaj9"), (176.8, 3.2, "Cmaj9")]
    return plan


def build_music():
    mus = np.zeros((2, N))
    bells = np.zeros((2, N))
    for t0, d, name in chord_plan():
        notes = CH[name]
        dark = name in ("Cdark", "Ebmaj7")
        last = t0 >= 176.8
        rel = 3.0 if last else 1.8
        for i, m in enumerate(notes[1:]):
            g = 0.06 if not dark else 0.075
            _add(mus, t0 - 0.3, pad_note(mtof(m), d + 0.3, 1.4, rel, 3 if dark else 5), pan=(i - 2) * 0.35, gain=g)
        _add(mus, t0, bass_note(mtof(notes[0] + 12 if notes[0] < 30 else notes[0]), d, 1.0), gain=0.11)
        # 铃声琶音
        if (12.2 <= t0 < 20.4) or dark:
            continue
        step = 0.5
        pattern = [notes[1] + 24, notes[3] + 12, notes[4] + 12, notes[5] + 12, notes[3] + 24, notes[5]]
        k = 0
        tt = t0
        while tt < t0 + d - 0.05:
            if RNG.random() < (0.55 if t0 < 12 else 0.68):
                m = pattern[k % len(pattern)]
                _add(bells, tt, bell(mtof(m), 2.0), pan=RNG.uniform(-0.6, 0.6), gain=0.045)
            tt += step
            k += 1
    return mus, bells


# ---------------------------------------------------------------- 音效时间表


def build_sfx():
    fx = np.zeros((2, N))
    from .scenes import TRANSITIONS
    for b, kind, dur in TRANSITIONS:
        _add(fx, b - dur / 2, whoosh(dur + 0.2, 0.55), pan=0.0, gain=0.10)
    # 开场
    _add(fx, 1.45, shimmer(1.0, 1200, 4000), pan=0.4, gain=0.07)          # 流星
    _add(fx, 8.75, boing(), gain=0.10)
    _add(fx, 8.7, bell(mtof(84), 3.0), gain=0.08)
    _add(fx, 8.9, bell(mtof(91), 3.0), gain=0.06)
    # 冻结 / 解冻
    _add(fx, 20.4, shimmer(1.4, 500, 3000), gain=0.12)
    _add(fx, 20.55, bell(mtof(88), 2.0, 1.0), gain=0.07)
    for te in (22.4, 25.4, 26.4, 27.8):
        _add(fx, te, ping(1320, 0.4), pan=-0.3 + (te - 22) / 10, gain=0.06)
    _add(fx, 27.5, boing(420, 260, 0.6), gain=0.05)
    # 宇宙日历
    _add(fx, 30.3, boom(3.0, 140, 30), gain=0.22)
    for i, te in enumerate([34.9, 36.8, 39.6, 41.8, 44.9, 48.4]):
        _add(fx, te, ping(990 + 110 * i, 0.5), gain=0.06)
    _add(fx, 41.0, whoosh(0.8, 0.8), pan=0.4, gain=0.06)
    _add(fx, 41.8, boom(1.2, 90, 40), gain=0.10)
    # 杯子
    _add(fx, 52.7, shatter(), pan=-0.4, gain=0.16)
    _add(fx, 53.8, shimmer(0.8, 3000, 700), pan=-0.3, gain=0.05)            # 倒放
    _add(fx, 54.55, click(220, 0.25, 0.9), gain=0.10)                         # ✕
    _add(fx, 59.3, bell(mtof(88), 2.0, 1.0), gain=0.07)
    # 钟摆嘀嗒
    for k in range(1, 7):
        _add(fx, 63.0 + k, click(1800 if k % 2 else 1300, 0.07), pan=0.25 * (1 if k % 2 else -1), gain=0.16)
    # 石英嗡鸣 + 原子钟上升音
    t = _t(2.2)
    hum = np.sin(2 * np.pi * 2048 * t) * np.sin(np.pi * t / 2.2) ** 2
    _add(fx, 69.4, hum, gain=0.012)
    t = _t(3.0)
    sweep = np.sin(2 * np.pi * np.cumsum(300 + 2700 * (t / 3.0) ** 2) / SR) * np.sin(np.pi * t / 3.0)
    _add(fx, 72.2, sweep, gain=0.025)
    _add(fx, 75.2, bell(mtof(91), 2.0), gain=0.07)
    # 心理时间：开心的快嘀嗒、无聊的慢嘀嗒
    for k in range(18):
        _add(fx, 80.0 + k * 0.25, click(2400, 0.04, 0.3), pan=-0.6, gain=0.04)
    for k in range(3):
        _add(fx, 80.6 + k * 1.6, click(900, 0.1, 0.4), pan=0.6, gain=0.06)
    _add(fx, 81.6, boing(), pan=-0.5, gain=0.06)
    _add(fx, 83.3, boing(), pan=-0.5, gain=0.05)
    for te in (85.4, 89.6, 91.2, 93.0, 95.4):
        _add(fx, te, bell(mtof(96), 1.6, 0.8), pan=0.3, gain=0.05)
    for i in range(4):
        _add(fx, 96.6 + i * 0.35, click(3000, 0.05, 0.8), gain=0.05)               # 相册“咔嚓”
    # 时空
    for i in range(8):
        _add(fx, 104.5 + i * 0.42, ping(660 + 60 * i, 0.35), pan=-0.4 + i * 0.1, gain=0.05)
    _add(fx, 108.7, shimmer(1.6, 400, 1600), gain=0.06)
    # 光钟：静止钟高音，飞行钟低音
    T_A0, T_B0, TRIP_A = 118.8, 122.8, 1.0
    TRIP_B = TRIP_A / 0.6
    k = 1
    while T_A0 + k * TRIP_A < 131.3:
        _add(fx, T_A0 + k * TRIP_A, ping(2637, 0.35), pan=-0.5 if T_A0 + k > 123 else 0, gain=0.06)
        k += 1
    k = 1
    while T_B0 + k * TRIP_B < 131.3:
        _add(fx, T_B0 + k * TRIP_B, ping(1568, 0.45), pan=0.5, gain=0.07)
        k += 1
    _add(fx, 127.6, bell(mtof(88), 2.0, 1.0), gain=0.06)
    # 双生子：火箭
    t = _t(5.0)
    roar = fft_lowpass(RNG.standard_normal(len(t)), 900) * np.sin(np.pi * t / 5.0) ** 0.6
    _add(fx, 131.9, roar, gain=0.07)
    _add(fx, 136.9, ping(1046, 0.6), gain=0.06)
    # 质量：行星落下
    _add(fx, 139.4, whoosh(1.8, 0.95), gain=0.08)
    _add(fx, 141.15, boom(2.0, 90, 30), gain=0.22)
    for te in (147.2, 147.9, 148.7, 151.6, 153.0):
        _add(fx, te, ping(1175, 0.45), gain=0.05)
    # 黑洞：低频轰鸣 + 越来越慢、最终停住的嘀嗒
    t = _t(10.5)
    rum = fft_lowpass(RNG.standard_normal(len(t)), 120) * 3.0
    rum += 0.6 * np.sin(2 * np.pi * 41 * t)
    rum *= np.minimum(1, t / 1.5) * np.minimum(1, (10.5 - t) / 1.0)
    _add(fx, 154.7, rum, gain=0.10)
    prev = 0
    for i in range(1, 4000):
        s = i / 400.0
        u = 1 - math.exp(-s / 2.4)
        tau = 2.4 * u
        if int(tau / 0.25) > prev:
            prev = int(tau / 0.25)
            _add(fx, 155.0 + s, click(1500, 0.06, 0.5), pan=-0.3, gain=0.10 * (1 - u * 0.7))
    # 结尾
    for k in range(3):
        _add(fx, 174.0 + k, click(1600, 0.06, 0.4), gain=0.07)
    _add(fx, 173.9, boing(), gain=0.06)
    for i, m in enumerate([72, 76, 79, 84]):
        _add(fx, 176.85 + i * 0.12, bell(mtof(m), 4.0, 1.2), pan=-0.3 + i * 0.2, gain=0.08)
    return fx


# ---------------------------------------------------------------- 混响 + 母带


def reverb(x, seconds=2.6, mix=0.32):
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir = np.zeros((2, n))
    for ch in range(2):
        r = RNG.standard_normal(n) * np.exp(-t * 3.2)
        ir[ch] = fft_lowpass(r, 5000)
    ir /= np.sqrt(np.sum(ir ** 2, axis=1, keepdims=True))
    size = 1 << int(np.ceil(np.log2(N + n)))
    out = np.zeros_like(x)
    for ch in range(2):
        X = np.fft.rfft(x[ch], size)
        Hh = np.fft.rfft(ir[ch], size)
        out[ch] = np.fft.irfft(X * Hh, size)[:N]
    return x * (1 - mix) + out * mix * 1.4


def build_audio(path):
    print("合成配乐与音效 …")
    mus, bells = build_music()
    fx = build_sfx()
    music = reverb(mus + bells, 3.0, 0.38)
    fxr = reverb(fx, 1.6, 0.22)
    mix = music * 0.9 + fxr
    t = np.arange(N) / SR
    fade = np.minimum(1, t / 1.0) * np.clip((DUR - t) / 1.6, 0, 1)
    mix *= fade
    peak = np.max(np.abs(mix))
    mix = np.tanh(mix / peak * 1.15) / np.tanh(1.15) * 0.89
    pcm = (mix.T * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("音轨 →", path)
    return path


if __name__ == "__main__":
    import sys
    build_audio(sys.argv[1] if len(sys.argv) > 1 else "soundtrack.wav")
