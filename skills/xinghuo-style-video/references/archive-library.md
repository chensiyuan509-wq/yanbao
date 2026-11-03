# 素材库：真实历史图像的来源、授权与用法

素材是这套风格的根：**真实的壁画、手稿、版画、油画、老照片、实物照片、NASA 影像**，只做调色、裁切、推拉，绝不伪造。

现有 89 张在 `engine/assets/archive/`（新项目会复制过去），是为《星火》（科学史）找的。
**每部新片按自己的题材重新找图**；只有内容真的重合时（比如又讲到法拉第）才复用这里的。
这份清单也是"什么样的图算好图"的样本：原作扫描、博物馆藏品照片、同时代的版画与照片。

## 目录
1. 授权规则
2. 找图与下载流程
3. 使用方式（kb / arch / framed / card / Gallery）
4. 现有图像清单（键 → 内容 → 推荐用法）
5. 地图数据与字体

---

## 1. 授权规则

- **只用**：公有领域（Public domain / PD-*）、**CC0**、**CC BY**（任何版本）。
- **不用**：CC BY-SA、NC、ND、"合理使用"、来源不明的图、AI 生成冒充的"历史图"。
- 每张图在画面里都要有出处：`caption(ctx, "作品名", "年代 · 作者 / 机构 · 授权")`，CC BY 的必须写作者名和"CC BY x.0"。
- 片尾加一行："历史图像：Wikimedia Commons（公有领域 / CC0 / CC BY，署名见片中与 CREDITS.md）"。

## 2. 找图与下载流程

1. **搜索**（返回候选标题、授权、尺寸，自动标出可用的 OK / 不可用的 --）：
   ```bash
   python <skill>/scripts/commons_search.py "Faraday Christmas lecture" "Colossus computer 1943"
   ```
   搜索词用英文（作品名 / 人名 + 年份 / 博物馆名）。优先选：原作扫描 > 博物馆照片 > 后世版画；分辨率 ≥ 1000。
2. **登记**：在项目 `tools/fetch_assets.py` 的 `MANIFEST` 末尾加一行
   `("键", "Commons 上的精确文件名.jpg")`，或者 `("键", "search:搜索词|标题必须包含的片段")`；
   卫星底图这类大图加 `{"width": 3840, "max": (3840, 1920)}`。
3. **下载**：`python tools/fetch_assets.py` —— 自动过滤授权、缩到 ≤ 2400×1800 的 JPEG、写 `credits.json` 和 `CREDITS.md`。
4. **先看再用**：用 `scripts/contact_sheet.py` 把新图拼成联系表看一眼——确认内容和标题相符（`mendeleev.jpg`
   就是标题说 1869 年、实际不是的反例），再决定裁切中心。

Commons 的坑：
- 缩略图宽度用 1920（2400 这类非标准宽度会被拒，3840 可以）；被限流时服务器给 `Retry-After`，照做；下载间隔 12 秒。
- User-Agent 用通用名（脚本里已经是 `cinematic-explainer-video/1.0`），**不要写用户邮箱**。
- 搜到的 SVG / PDF / TIFF 也能用（API 会给 JPEG 缩略图）。

## 3. 使用方式

```python
from ..archive import caption, framed, kb, show
from ..exhibit import card, panel
from ..gallery import Gallery
from .common import arch

arch(ctx, t, "athens", t0, t1, (0.5, 0.5, 1.02), (0.76, 0.76, 2.4), "拉斐尔《雅典学院》", "1509—1511 年 · 公有领域")
kb(ctx, "einstein", t, t0, t1, c0, c1, rect=(0, 0, W * 0.58, H), grade="sepia")   # 左图右文
framed(ctx, "xray", 560, 450, 520, a)                                             # 暗墙上的画框
card(ctx, "gramme", x, 520, 480, 620, "1871", "格拉姆发电机", ("机械能 → 电能", "工厂第一次用上电"), 1.0, k, crop, t, hot)
Gallery([("athens", "拉斐尔《雅典学院》", "1509—1511 年")], actor, t0, t1, push=0, lead=420)
```
裁切 `(u, v, zoom)`：u, v 是图像上要放在画面中心的点（0–1），zoom 以"铺满"为 1。`fit="contain"` 完整显示。

## 4. 现有图像清单

| 键 | 内容 | 授权 | 尺寸 | 推荐用法 |
|---|---|---|---|---|
| `lascaux_megaloceros` | 拉斯科洞窟：巨角鹿下方一排黑点（复制品照片） | Public domain | 1775×1744 | 史前计数 / 记录；裁 (0.5,0.55,1.05)→(0.6,0.7,1.3) 看点列 |
| `lascaux_horse` | 拉斯科洞窟：马 | Public domain | 1881×1800 | 史前艺术、观察 |
| `lascaux_replica` | 拉斯科复制洞全景，牛马群 | Public domain | 2016×1800 | 史前开场；适合配火光 lit 与原始人 Claude；展厅推镜 |
| `lascaux_squares` | 拉斯科：方格符号 | Public domain | 1434×1800 | 抽象符号、记录 |
| `manos` | 阿根廷手洞，满墙手印（约 9000 年前） | Public domain | 2400×1599 | "我来过"；尾声回声镜头；grade="warm" |
| `manos2` | 手洞另一角度 | Public domain | 1600×1200 | 同上，备用 |
| `stonehenge` | 康斯太布尔《巨石阵》水彩 1836 | Public domain | 2400×1643 | 天文观测、历法；整幅用，别裁掉边框 |
| `cuneiform_barley` | 大都会博物馆：大麦分配账目泥板（约前 3100） | CC0 | 1976×1800 | 文字起源 = 记账；CC0 |
| `plimpton` | 普林顿 322 号泥板（约前 1800） | Public domain | 1246×863 | 勾股数 119-120-169 |
| `rhind` | 莱因德数学纸草书 | Public domain | 750×449 | 埃及数学、π≈256/81；图小，适合局部或画框 |
| `nebamun` | 内巴蒙墓壁画 | Public domain | 2113×1800 | 古埃及生活；色彩好 |
| `pyramids_roberts` | 大卫·罗伯茨《狮身人面像与吉萨金字塔》1839 | Public domain | 2400×1524 | 金字塔朝向、天文；油画质感 |
| `pyramids_photo` | 斯佩尔泰里尼热气球航拍金字塔（约 1904） | Public domain | 1800×1320 | 俯瞰；黑白老照片 |
| `oracle` | 商代牛肩胛骨卜辞（CC0） | CC0 | 1920×1280 | 甲骨文、日月食记录 |
| `dunhuang` | 敦煌星图（唐） | Public domain | 1793×1800 | 古代星图；适合缓慢横移 |
| `athens` | 拉斐尔《雅典学院》1509–1511 | Public domain | 1920×1490 | 古希腊理性；推近右下角欧几里得 (0.76,0.76,2.4)；展厅推镜首选 |
| `byrne_pyth` | 拜恩版《几何原本》勾股定理页（彩色） | Public domain | 1920×1302 | Byrne 风格证明的出处 |
| `byrne_title` | 拜恩版《几何原本》扉页 1847 | Public domain | 1237×600 | 画框展示 |
| `archimedes` | 费蒂《阿基米德》约 1620 | Public domain | 1350×1800 | 人物肖像 + 圆周率 |
| `eratosthenes` | 斯特罗齐《埃拉托色尼在亚历山大教学》1635 | Public domain | 1070×856 | 测地球 |
| `library_alex` | 亚历山大图书馆（19 世纪想象版画） | Public domain | 1072×1090 | 标注"想象图"；sepia |
| `maqamat_library` | 《玛卡梅》插图里的图书馆（13 世纪） | Public domain | 974×989 | 伊斯兰黄金时代、智慧之家 |
| `khwarizmi` | 花拉子米《代数学》手稿页（博德利图书馆） | Public domain | 1000×722 | 代数起源；配配方法动画 |
| `taqi` | 塔基丁的伊斯坦布尔天文台（16 世纪细密画） | Public domain | 1235×1800 | 伊斯兰天文学 |
| `opticae` | 《光学宝库》1572 扉页（海赛姆光学） | Public domain | 1021×1536 | 光学、暗室 |
| `tiangong_paper` | 《天工开物》造纸图 1637 | Public domain | 357×510 | 很小（357×510），只做画框插图 |
| `qingming` | 《清明上河图》局部 | Public domain | 1920×960 | 宋代城市；横向长卷，适合横移 (0.15→0.75) |
| `printer_1568` | 约斯特·安曼《印刷工》木刻 1568 | Public domain | 751×879 | 印刷术；版画 |
| `gutenberg_bible` | 古腾堡圣经（法国国家图书馆藏，CC0） | CC0 | 1920×996 | 印刷革命 |
| `copernicus` | 《天体运行论》日心说手稿图 | Public domain | 1920×1645 | 哥白尼；可叠肖像 |
| `galileo_moon` | 伽利略手绘月相 1616 | Public domain | 585×818 | 观察；画框或特写 |
| `medicean` | 《星际信使》木星卫星记录 | Public domain | 334×500 | 很小，只做画框 |
| `galileo` | 苏斯特曼斯《伽利略像》约 1640 | Public domain | 1280×1646 | 人物肖像特写 |
| `tycho` | 第谷墙象限仪（1598 版画） | Public domain | 1333×1800 | 精确观测 |
| `newton` | 克内勒《牛顿像》1689 | Public domain | 1495×1800 | 肖像；可与 principia 左右并置 |
| `principia` | 《原理》1687 扉页 | Public domain | 1371×1800 | 万有引力 |
| `newcomen` | 纽科门大气式蒸汽机版画 | Public domain | 843×790 | grade="blueprint" 变蓝图 |
| `watt_1782` | 瓦特双作用蒸汽机专利图 | Public domain | 1428×1800 | blueprint 调色效果极好 |
| `watt_section` | 瓦特旋转式蒸汽机剖面幻灯片 | Public domain | 1800×1800 | 原理讲解 |
| `coalbrookdale` | 卢瑟堡《夜色中的煤溪谷》1801 | Public domain | 1920×1227 | 工业革命开场的经典画；炉火 |
| `locomotive` | "行星号"机车版画 1832 | Public domain | 1920×1250 | 铁路 |
| `faraday_lecture` | 法拉第在皇家研究院圣诞讲座 1856（布莱克利） | Public domain | 1920×1419 | 讲座 / 传播科学；展厅推镜 |
| `faraday_ring` | 法拉第感应线圈（1896 插图） | Public domain | 1484×1568 | 电磁感应；画框 |
| `maxwell` | 麦克斯韦肖像版画 | Public domain | 581×652 | 配方程组（eq 字体） |
| `mendeleev` | （不要用）标题说是 1869 周期表，实际是后来的显示版 | Public domain | 1920×1587 | 改用自己画的周期表动画 |
| `edison_patent` | 爱迪生电灯专利图 1880 | Public domain | 1107×1800 | blueprint 调色 |
| `bell_patent` | 贝尔电话专利图 1876 | Public domain | 864×1200 | blueprint 调色 |
| `jumbo_dynamo` | 爱迪生珍珠街 Jumbo 发电机（约 1885） | Public domain | 640×432 | 发电；图小 |
| `tesla_lab` | 特斯拉科罗拉多泉实验室 1899 | Public domain | 1016×749 | 交流电、高压放电 |
| `expo1881` | 1881 巴黎国际电力博览会纪念画（CC0） | CC0 | 1390×1800 | 电气时代 |
| `palais_elec` | 1900 巴黎世博会电力宫 | Public domain | 1920×1551 | 电气时代的浪漫 |
| `xray` | 伦琴拍下的第一张 X 光片：夫人的手 1895 | Public domain | 1252×1800 | 真实原件；暗墙画框 |
| `curie` | 居里夫人约 1920 | Public domain | 1325×1800 | 肖像 |
| `einstein` | 爱因斯坦 1921（施穆策尔摄），在黑板前 | Public domain | 1371×1800 | 左图右文 (rect 0..0.58W) |
| `eclipse1919` | 1919 年日食玻璃底片（负片，竖版 700×899） | Public domain | 700×899 | 放在灯箱上 + 光线偏折示意；别全屏放大 |
| `solvay` | 1927 年第五届索尔维会议合影 | Public domain | 1920×1389 | 量子力学；推近找爱因斯坦 / 居里 |
| `michelson` | 迈克耳孙–莫雷实验装置（石板）照片 | Public domain | 742×432 | grade="cool_mono"，再接干涉仪动画 |
| `hudf` | 哈勃极深场 | Public domain | 1800×1800 | 宇宙尺度；慢推到 1.6 |
| `m87` | M87 黑洞照片 2019（EHT，CC BY 4.0） | CC BY 4.0 | 1800×1800 | 署名"事件视界望远镜合作组织 · CC BY 4.0" |
| `earthrise` | "地出"阿波罗 8 号 1968（方形） | Public domain | 1800×1800 | 取景 (0.5,0.6,1.0)，要包含月面地平线 |
| `aldrin` | 奥尔德林在月面 1969 | Public domain | 1789×1800 | 登月 |
| `apollo_launch` | 阿波罗 11 号发射 1969 | Public domain | 1440×1800 | 发射瞬间；zoomblur 转场 |
| `ada` | 阿达·洛芙莱斯像（沙隆，约 1840） | Public domain | 1253×1800 | 肖像；展厅 |
| `babbage` | 巴贝奇差分机局部（1853 木刻） | Public domain | 549×725 | 计算机前史 |
| `eniac` | ENIAC 与两位女程序员 1946 | Public domain | 1920×1318 | 计算机 |
| `menna` | 麦纳墓壁画摹本：拉绳丈量土地（CC0） | CC0 | 1920×613 | 几何起源 = 测量土地；横幅 |
| `bluemarble` | NASA 蓝色弹珠（等距圆柱投影 3840×1920） | Public domain | 3840×1920 | 卫星地图底图（白天）；不直接展示 |
| `citylights` | NASA DMSP 夜间灯光（3840×1920） | Public domain | 3840×1920 | 卫星地图底图（夜间）；现代 / 网络 / 电气化 |
| `watt_engine` | （少用）博尔顿–瓦特蒸汽机实物，角度杂乱 | CC BY 2.0 | 996×1152 | CC BY 2.0 |
| `rocket_loco` | "火箭号"机车 1929 复制品（CC0） | CC0 | 1920×1280 | 实物照片，展品卡 |
| `gramme` | 格拉姆发电机实物 | Public domain | 1200×1800 | 展品卡 |
| `edison_bulb` | 爱迪生演示灯泡实物（CC0） | CC0 | 1200×1800 | 展品卡 |
| `bell_phone` | 贝尔 1876 单极电话发送器 | Public domain | 787×463 | 展品卡 |
| `siemens_loco` | 1879 西门子电力机车 | Public domain | 1920×1440 | 展品卡 |
| `marconi_room` | "奥林匹克号"上的马可尼无线电室 | Public domain | 1865×1444 | 展品卡 / 无线电 |
| `trinity` | "三位一体"核试验 1945 | Public domain | 1624×956 | grade="mono"，肃穆；配 flash/dip |
| `gps` | GPS IIIA 卫星示意图（方形） | Public domain | 1800×1800 | 取景 (0.56,0.6,1.0) 带出地球；面板放右侧 |
| `ligo` | LIGO 汉福德航拍（L 形臂） | Public domain | 1920×1280 | 引力波；右上放波形面板 |
| `hubble` | 哈勃望远镜在轨 | Public domain | 1920×1276 | 太空 |
| `dsky` | 阿波罗导航计算机 DSKY 键盘 | Public domain | 1920×1506 | 画框小插图（内存约 4KB） |
| `transistor` | 第一只晶体管复制品 | Public domain | 500×448 | 展品卡；图小 |
| `intel4004` | Intel 4004 版图海报（CC0） | CC0 | 1920×1280 | 展品卡；blueprint 调色当数据图背景 |
| `frontier` | Frontier 超级计算机（CC BY 2.0） | CC BY 2.0 | 1920×1275 | 算力；加暗场再放面板 |
| `bernoulli` | 阿达"注释 G"伯努利数计算表原件 1843 | Public domain | 1920×1344 | 展厅推镜进表 → 逐步翻译前四步 |
| `turing` | 图灵 16 岁照片 | Public domain | 675×919 | 暗墙画框 |
| `colossus` | Colossus 计算机 1943 | Public domain | 1920×1281 | 展品卡 |
| `ibm704` | IBM 704 计算机 1957（NASA） | Public domain | 1920×1521 | 达特茅斯 / 早期 AI |
| `arpanet` | ARPANET 逻辑拓扑图 1977 | Public domain | 1000×716 | grade="blueprint"；推向西海岸 |
| `deepblue` | 深蓝（计算机历史博物馆，CC BY 2.0） | CC BY 2.0 | 1067×1600 | 竖版，放左侧 rect |

## 5. 地图数据与字体

- `assets/geo/world.json`：Natural Earth 精简版（高 / 低精度陆地、湖泊、13 条大河：尼罗河、幼发拉底、底格里斯、印度河、
  恒河、黄河、长江、多瑙河、莱茵河、伏尔加河、泰晤士河、波河、密西西比河）。由 `tools/prepare_geo.py` 生成。
- 卫星底图：`bluemarble`（白天）、`citylights`（夜间），用 `oldmap.draw_satellite(ctx, cam, t, a, "day"/"night", "warm"/"natural"/"cool")`。
- 城市坐标在 `oldmap.CITIES`（乌鲁克、巴比伦、吉萨、雅典、亚历山大港、巴格达、长安、敦煌、撒马尔罕、君士坦丁堡、
  佛罗伦萨、伦敦、巴黎……约 45 个）；没有的用 `city_sat(..., lonlat=(lon, lat), label="名字")`。
- 字体全部来自系统 Noto 系列（`fonts-noto-cjk`、`fonts-noto-core`、`fonts-noto-extra`）+ DejaVu + AR PL UKai。
  缺字会被 `check.py` 报出来。
