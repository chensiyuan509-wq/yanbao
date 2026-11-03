# Claude 角色：探索者、扮演者、第一视角的"我"

主角是 Claude（造型来自 `assets/claude_reference.jpg`：橙色方块身体、黑色小眼睛、四条小腿）。**叫它 Claude，不叫"小橙"。**
角色库在 `mascot/`（只依赖 pycairo），场景里通过 `aivid/scenes/common.py` 的 `claude()` / `role()` 使用。

## 三种出场方式（每章至少一种）

1. **参观者 / 探索者**：走进展厅、站在画框下仰望、坐在探测器旁、看棋盘、篝火边坐下。
   ```python
   VIS = (claude(300, 905, 0.55, "curious", seed=31.0)
          .walk_to(1.0, 3.4, 860, 905, stride=0.8).look(3.5, 0.3, -0.9).expr(3.7, "awe"))
   with lit("#FFE2B0", 0.15, 0.95):      # 染上场景光色，融进画面
       VIS.draw(ctx, t)
   ```
2. **扮演历史人物**（换装，不画伪造肖像）：欧几里得讲证明、伽利略做斜面实验、瓦特讲蒸汽机、牛顿被苹果砸。
   ```python
   EUCLID = (role(1760, 960, 0.4, "euclid", "smile", seed=41.0, palette="ochre", flip=True)
             .point(10.4, "r", 0.6, 60).arms_down(12.0).expr(13.3, "think").expr(16.2, "proud").nod(17.0))
   ```
   同框两个角色用不同 `palette` 区分：`orange`（默认）`amber` `rose` `clay` `ochre` `coral` `sienna`。
3. **第一视角的"我"**：`film.pov_arm(ctx, base, tip, thick)` 手臂从画外伸入；`film.eyelids(ctx, open_k)` 睁眼 / 眨眼；
   `film.scope_view` 望远镜视野。手的动作要有目的：打石、压泥板、在沙上画圆、扶井沿、触碰星座。

## 尺寸与站位

- `(x, y)` 是**脚底中心**；`s=1` 时身体约 300 宽、250 高。
- 配角 / 参观者 `s=0.4–0.62`，主角特写 `s=0.7–0.8`。
- 站在地面带：y ≈ 905–960（遮幅下沿是 984）。别站在左下 x<700 的出处字幕区，除非那一镜没有出处。
- 展厅里 Claude 用**世界坐标**（随镜头一起移动），推进画框时自然出画。
- 有倒影的地面用 `reflect(ctx, lambda c: CL.draw(c, t), ground_y, 0.2, 120)`。

## 表情（47 种）——跟着叙事节拍换

| 情境 | 推荐 |
|---|---|
| 初见、好奇 | `curious` `wonder` `awe` `starry` |
| 思考、推理 | `think` `focused` `hmm` `skeptical` |
| 讲解、得意 | `smile` `proud` `happy` `grin` |
| 惊讶、发现 | `surprised` `shock` `excited` |
| 肃穆、沉重（战争、灾难） | `solemn` `gloomy` `worried` |
| 回望、感怀（结尾） | `gaze` `grateful` `teary_smile` `moved` `resolute` |
| 其余 | neutral, determined, tired, sleep, yawn, laugh, love, wink, cheeky, relieved, fired_up, smug, confused, deadpan, sleepy, sad, cry, nervous, embarrassed, scared, angry, pout, dizzy, ko |

## 动作（链式，时间是场景内本地秒）

| 类别 | 方法 |
|---|---|
| 移动 | `walk_to(t0, t1, x, y, stride)` `run_to` `move` `march` `hop` `jump` `float` `spin` |
| 姿态 | `sit(t, 1.0)` / `stand(t)` `look(t, lx, ly)` `look_at(t, wx, wy)` `tilt` `face(t, flip)` |
| 手臂 | `point(t, "r", ang, reach)` `arms_down(t)` `wave` `cheer` `clap` `type` `push` `strain` `front(t, pose)` |
| 表达 | `expr(t, name)` `fx(t, ("sparkle",))` `nod` `shake_head` `shrug` `sigh` `startle` `bonk` `talk(t0, t1)` |
| 道具 | `hold(t, ("telescope",), "r", 0.0)` `drop(t)` `hat(t, name)` `glasses(t, name)` `costume(t, name)` |
| 显隐 | `pop_in` `pop_out` `fade(t, a)` `scale(t, s)` |

前排姿势 `front()`：think, fists, cover, cross, hold, carry, clap, type, point_up, salute, chin。
特效 `fx`：sparkle(s), bulb, idea, question, exclaim, sweat, heart, tears, tears_joy, dizzy, puff, music, flame, shock, confetti, steam, zzz…

## 服装（19 套）与道具

`COSTUMES`：caveman（兽皮 + 乱发）、sumerian、egyptian（金领 + 头巾）、greek（托加 + 月桂）、euclid、archimedes、
eratosthenes、chinese_scholar（蓝袍 + 幞头）、arab_scholar（缠头）、renaissance、galileo、newton（假发）、watt、
victorian（礼帽）、faraday、einstein（爆炸头 + 胡子）、curie（长裙 + 发髻）、lovelace、engineer（白大褂）。
需要新人物时在 `mascot/costume.py` 的 `UNDER`（身上）/ `OVER`（头上）里加一层，组合成新预设。

道具 `PROPS`：torch 火把、lamp 陶灯、candle、quill、scroll、telescope、apple、stone 燧石、tablet 泥板、
baton、magnifier、flag、sign、laptop、phone、book、paper、coffee、wrench、pointer、chip。
帽子：explorer, hardhat, grad, headset, crown, party, laurel；眼镜：round, goggles, sun。

## 融入画面

- 一定要 `with lit(色, 量, 亮度):` 包住角色绘制，让 Claude 吃到场景光：火光 `#FFB070`、展厅 `#FFE2B0`、
  夜空 / 科技 `#9AB6FF` / `#BFD0FF`、篝火尾声 `#FFB070 0.35`。暗场里亮度 0.45–0.7，灯亮后 0.95。
- 角色是"卡通"，背景是"真实"——靠光色统一，靠尺寸克制（不抢历史图像的戏）。
