# 音效设计：没有背景音乐，只有声音的"现场感"

用户明确喜欢：**不含背景音乐，只有音效与环境声**。声音全部由 numpy 合成（`aivid/audio.py` 通用音效 +
`aivid/sfx_hist.py` 历史 / 科技音效），约 110 种。最后整片响度归一到 **−16 LUFS**，峰值 −1 dBFS，加一点混响和房间底噪。

## 写法

```python
def sfx():
    return [
        (0.0, "ambience_room", {"dur": 8.5, "gain": 0.35}),   # (本地秒, 音效名, 参数)
        (0.4, "shutter", {"gain": 0.3}),
        (2.4, "geiger", {"dur": 3.0, "rate": 6, "gain": 0.18}),
    ]
```
音效名就是 `s_xxx` 函数去掉前缀；`dur`、`pitch`、`rate`、`n` 等参数看函数签名。`check.py` 会报未定义的名字。

## 三层结构

1. **环境底（ambience，一直在）**：每个镜头都要有一层，**不能出现静音空洞**（静音 0.8 秒以上就算事故，检查方法见下）。
   相邻镜头的环境底要重叠 0.2–0.5 秒。gain 0.3–0.5。
2. **动作音（跟画面里的动作对齐）**：快门（照片出现）、翻页、粉笔、齿轮、点击（列表一条条出现）。gain 0.15–0.3。
3. **重音（少用，留给大事件）**：riser → boom、rumble、强光的 swell。gain 0.45–0.7。

## 场景 → 音效对照

| 画面 | 环境底 | 动作 / 重音 |
|---|---|---|
| 洞穴、篝火、史前 | `ambience_fire` `ambience_cave` `ambience_wind` | `knap` 打石、`flint` `ignite` 点火、`drip` `carve` 刻骨 |
| 河流、农田、古城 | `ambience_river` `ambience_birds` | `wedge` 压楔形字、`sand`、`caravan` 驼队（地图航线） |
| 书房、图书馆、展厅 | `ambience_room` | `page` `pages_flurry` `quill` `chalk`、`shutter`（照片 / 灯亮）、`bell_toll` |
| 工业 | `ambience_engine` | `steam` `thump` `gears_run` `ratchet` `brass` |
| 电气 | `hum` | `zap` `crackle` `telegraph` `relays` `whine` |
| 原子、辐射 | `ambience_room` | `geiger` `rumble` `boom` |
| 太空、星空 | `ambience_space` | `rocket` `shimmer` `hush` |
| 计算机、网络 | `ambience_data` | `typing` `relays` `blip` `scan` `stream` `success` `ding` |
| 棋盘 | — | `stone_click` 连续落子（间隔 0.26–0.28） |
| 列表 / 卡片逐条出现 | — | `pop` / `click`，音高逐条升高（pitch 1.0, 1.12, 1.24…） |
| 情绪段（回望、尾声） | `ambience_space` / `ambience_fire` | `hush` `heartbeat`（n=2）`shimmer` `chime` |
| 大揭晓 | — | `riser`（1.4–2 秒）→ `boom`；或 `swell` 配强光 |
| 转场 | — | 章间转场写在 `TRANSITIONS` 参数 `sound`；章内用 `whoosh` `whoosh_short` `hush` |

## 原则

- 声音服务画面，**每个声音在画面上都能找到来源**（照片出现 = 快门；地图航线 = 驼铃；电流 = 嗡鸣）。
- 少即是多：同一时刻最多两层动作音。
- 肃穆段落（战争、灾难）只留低频 rumble 和环境底，不加花哨音效。
- 结尾跟画面一起淡出（`fade_black` 的那 1.4 秒里不再触发新音效）。

## 检查

```bash
python check.py --audio            # 响度与峰值
ffmpeg -i out/soundtrack.wav -af silencedetect=noise=-50dB:d=0.8 -f null - 2>&1 | grep silence_
```
没有任何 `silence_start` 输出才算合格。
