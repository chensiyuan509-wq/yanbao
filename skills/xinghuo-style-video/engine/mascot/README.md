# mascot · 可复用的橙色小方块角色库

按 `assets/image.jpg` 的造型与 11 种表情矢量重绘，并扩展到 **41 种表情、38 类动作、11 种前置手臂姿势、24 种漫画特效、6 种帽子、3 种眼镜、12 种手持道具**。
只依赖 `pycairo`，整个 `mascot/` 文件夹可以直接拷到任何 Python 项目里用。

| 总览图 | 内容 |
|---|---|
| `sheets/expressions.png` | 全部表情（前 11 种对应素材图） |
| `sheets/actions.png` | 动作 / 姿势示例 |
| `sheets/gear.png` | 帽子、眼镜、道具 |
| `sprites/expr_*.png / .svg` | 每个表情的透明 PNG（512px）与 SVG，可直接拖进剪映、PPT、Figma |
| `catalog.json` | 机器可读的清单（表情、动作、姿势、特效、配件、道具） |

重新导出：`python -m mascot.export --sprites`

## 两种用法

### 1. 直接画一帧

```python
import cairo
from mascot import draw_mascot

surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 600)
ctx = cairo.Context(surf)
draw_mascot(ctx, 400, 520, 1.2, expr="starry", t=1.0, hat="explorer", fx=("sparkles",))
surf.write_to_png("hello.png")
```

坐标约定：`(x, y)` 是**脚底中心**（地面），`s=1` 时身体宽 300、总高约 250。

### 2. 用时间轴写动作（Actor）

```python
from mascot import Actor

a = (Actor(960, 820, 0.7, "sleep", seed=1.0, hat="explorer")
     .expr(2.0, "surprised").startle(2.0)          # 被吵醒，吓一跳
     .expr(2.8, "happy").wave(3.0, 4.6)            # 开心挥手
     .walk_to(5.0, 7.0, 1400, 820)                 # 走过去（迈腿、起伏、前倾、看向前方）
     .expr(7.1, "think").fx(7.1, ("ellipsis",))    # 托腮思考
     .hold(9.0, ("sign", {"label": "AI"}), "r", -0.35).arm(9.0, "r", 0.9)   # 举牌
     .talk(9.5, 12.0, smile=0.4))                  # 说话（口型）
a.talk_fn = lambda t: my_audio_level(t)            # 可选：用真实配音音量驱动口型
a.draw(ctx, t)                                     # 每一帧调用
```

所有动作方法都返回自身，可以链式调用；动作之间可以叠加（边走边说、边跳边挥手）。

## 表情（41 种）

素材原有：`neutral` 平静 · `happy` 开心 · `curious` 好奇 · `think` 思考（手托下巴）· `surprised` 惊讶 · `determined` 下定决心（握拳 + 闪光）· `tired` 疲惫 · `sleep` 睡觉 · `yawn` 打哈欠 · `proud` 自豪 · `excited` 兴奋

扩展：`smile` 微笑 · `grin` 咧嘴笑 · `laugh` 大笑 · `love` 喜爱 · `starry` 星星眼 · `awe` 惊叹 · `wink` 眨眼 · `cheeky` 调皮 · `relieved` 松了口气 · `fired_up` 斗志燃烧 · `smug` 得意 · `focused` 专注 · `hmm` 琢磨 · `confused` 困惑 · `skeptical` 怀疑 · `deadpan` 面无表情 · `sleepy` 困 · `sad` 难过 · `cry` 哭 · `moved` 感动 · `worried` 担心 · `nervous` 紧张 · `embarrassed` 尴尬 · `shock` 震惊 · `scared` 惊恐 · `angry` 生气 · `pout` 不服 · `dizzy` 晕 · `ko` 被撞晕 · `gloomy` 郁闷

表情切换自动平滑过渡（眼型不同就"眨眼换形"，眉毛 / 腮红插值，嘴巴缩放交替），并带一个小弹跳。新增表情只需在 `expressions.py` 里加一行。

## 动作（Actor 方法）

| 类别 | 方法 |
|---|---|
| 移动 | `walk_to` 走 · `run_to` 跑（扬尘）· `march` 原地踏步 · `move` 平移 · `place` 瞬移 · `float` 漂浮 |
| 跳跃 | `hop` 小跳（预备—腾空—落地回弹）· `jump` 大跳 · `land` 落地挤压 · `startle` 吓一跳 · `bounce` 原地弹 |
| 手势 | `wave` 挥手 · `cheer` 欢呼 · `clap` 拍手 · `point` 指向 · `shrug` 摊手 · `type` 打字 · `push` 推 · `strain` 使劲够 |
| 头部 | `look` / `look_at` 视线（大幅转头自动眨眼）· `nod` 点头 · `shake_head` 摇头 · `blink` 眨眼 |
| 身体 | `tilt` 倾斜 · `shake` 晃 · `shiver` 发抖 · `wobble` 晕乎乎地摇 · `sigh` 叹气 · `bonk` 撞墙 · `spin` 转圈 · `face` 转身 · `sit` / `stand` 坐下 / 站起 · `dance` 跳舞 |
| 外观 | `expr` 表情 · `fx` 特效 · `front` 前置手臂姿势 · `hold` / `drop` 拿起 / 放下道具 · `hat` 帽子 · `glasses` 眼镜 · `scale` · `fade` · `pop_in` / `pop_out` |
| 说话 | `talk(t0, t1, smile)`：口型 + 轻微点头节奏 + 句首扬眉 + 偶尔的手势；设置 `talk_fn` 后口型跟随真实音量 |

前置手臂姿势（`front`）：`think` 托下巴 · `fists` 握拳 · `cover` 扶额 · `cross` 抱臂 · `hold` 捧着 · `carry` 举过头顶 · `clap` 拍手 · `type` 打字 · `point_up` 指天 · `salute` 眺望 · `chin` 托腮

待机微动（默认开启）：呼吸、自然眨眼（偶尔连眨）、眼球微动、重心轻摆、视线微漂；帽子有惯性（起跳被压住、腾空飘起、落地一沉）。

## 特效、配件、道具

- 特效 `fx`：`zzz` `sparkle` `sparkles` `bulb` `idea` `question` `question2` `exclaim` `sweat` `drops` `heart` `gloom` `anger` `tears` `tears_joy` `dizzy` `puff` `music` `flame` `shock` `blush_lines` `ellipsis` `confetti` `steam`
- 帽子 `hat`：`explorer` 探险帽 · `hardhat` 安全帽 · `grad` 学士帽 · `headset` 耳麦 · `crown` 王冠 · `party` 派对帽
- 眼镜 `glasses`：`round` 圆框 · `goggles` 护目镜 · `sun` 墨镜
- 道具 `hold(t, prop, at)`：`baton` 接力棒 · `magnifier` 放大镜 · `flag` 旗子 · `sign` 举牌 · `laptop` · `phone` · `book` · `paper` 论文 · `coffee` · `wrench` · `pointer` 教鞭 · `chip` 芯片；`at` 可选 `front`（双手捧）/ `over`（举过头顶）/ `l` / `r`（单手）。也可以传一个函数 `fn(ctx, t, a)` 作为自定义道具。

## 接入项目的调色滤镜

```python
import mascot
mascot.set_color_hook(my_filter)   # my_filter((r, g, b)) -> (r, g, b)，用于去色、色调、亮度等统一调色
```

## 文件

```
gfx.py          最小绘图工具（缓动、关键帧、噪声、图形、文字、颜色钩子）
const.py        造型常量与配色
face.py         眼睛 / 眉毛 / 嘴巴 / 腮红
expressions.py  表情表（声明式）
fx.py           漫画特效
gear.py         帽子 / 眼镜 / 道具
body.py         主绘制 draw_mascot、手臂与前置姿势、自然眨眼、表情混合
actor.py        Actor 时间轴与动作清单 ACTIONS
export.py       导出总览图、精灵、catalog.json
```
