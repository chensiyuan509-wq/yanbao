#!/usr/bin/env python3
"""下载片中用到的历史图像（全部为公有领域 / CC0 / CC BY），统一缩放成 JPEG，并生成署名清单。

  python tools/fetch_assets.py            # 下载缺少的
  python tools/fetch_assets.py --force    # 全部重新下载

来源：Wikimedia Commons（API 返回的授权信息逐条记录在 assets/archive/credits.json 与 CREDITS.md）。
只接受 Public domain、CC0、CC BY（不接受 CC BY-SA / NC / ND）。
"""
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "archive")
UA = "xinghuo-video/1.0 (educational, non-commercial)"
API = "https://commons.wikimedia.org/w/api.php"

# (键, 精确标题 或 "search:查询|必须包含的片段")
MANIFEST = [
    # 第一章 史前
    ("lascaux_megaloceros", "Lascaux, Megaloceros.jpg"),
    ("lascaux_horse", "Lascaux, horse.JPG"),
    ("lascaux_replica", "Lascaux, replica 02.JPG"),
    ("lascaux_squares", "Lascaux, squares painting.JPG"),
    ("manos", "Cuevamanos3399.jpg"),
    ("manos2", "SantaCruz-CuevaManos-P2210651b.jpg"),
    ("stonehenge", "Stonehenge by John Constable.jpg"),
    # 第二章 文字与数
    ("cuneiform_barley", "search:cuneiform tablet barley account|administrative account of barley distribution with cylinder seal"),
    ("plimpton", "Plimpton 322.jpg"),
    ("rhind", "Rhind Mathematical Papyrus.jpg"),
    ("nebamun", "Tomb of Nebamun.jpg"),
    ("menna", "Rope stretching.jpg"),
    ("pyramids_roberts", "The Great Sphinx, Pyramids of Gizeh-1839) by David Roberts, RA.jpg"),
    ("pyramids_photo", "Spelterini Pyramids.jpg"),
    ("oracle", "Shang Ox Scapula Oracle Bones 1.jpg"),
    ("dunhuang", "Dunhuang star map.jpg"),
    # 第三章 古希腊
    ("athens", "\"The School of Athens\" by Raffaello Sanzio da Urbino.jpg"),
    ("byrne_pyth", "Byrne 1847 Pythagoras Querformat.jpg"),
    ("byrne_title", "The First Six Books of the Elements of Euclid.jpg"),
    ("archimedes", "Domenico-Fetti Archimedes 1620.jpg"),
    ("eratosthenes", "Eratosthenes Teaching in Alexandria (Bernardo Strozzi, Montreal).jpg"),
    ("library_alex", "Ancientlibraryalex.jpg"),
    # 第四章 传承
    ("maqamat_library", "Maqamat hariri.jpg"),
    ("khwarizmi", "Bodleian MS. Huntington 214 roll332 frame36.jpg"),
    ("taqi", "Taqi al din.jpg"),
    ("opticae", "search:Opticae thesaurus Alhazen 1572 frontispiece|Triplicus visus"),
    ("tiangong_paper", "Making Paper.gif"),
    ("qingming", "Along the River During the Qingming Festival (detail of original).jpg"),
    ("printer_1568", "Buchdrucker-1568.png"),
    ("gutenberg_bible", "Bible de Gutenberg, copie de la BNF Res A71-(2).jpg"),
    # 第五章 科学革命
    ("copernicus", "Copernican heliocentrism diagram-2.jpg"),
    ("galileo_moon", "Galileo moon phases.jpg"),
    ("medicean", "Sidereus Nuncius Medicean Stars.jpg"),
    ("galileo", "search:Galileo Galilei RMG BHC2700|(cropped)"),
    ("tycho", "Tycho-Brahe-Mural-Quadrant.jpg"),
    ("newton", "Portrait of Sir Isaac Newton, 1689.jpg"),
    ("principia", "search:Philosophiae Naturalis Principia Mathematica 1687 title page|Principia"),
    # 第六章 蒸汽与电
    ("newcomen", "Newcomen atmospheric engine (Heat Engines, 1913).jpg"),
    ("watt_1782", "search:Watt steam engine engraving|double steam engine from his specification of 1782"),
    ("watt_section", "search:Lantern Slide Cross-Section of Watt's Rotative Double-Acting Condensing Steam Engine|Cross-Section of Watt"),
    ("coalbrookdale", "Philipp Jakob Loutherbourg d. J. 002.jpg"),
    ("locomotive", "Planet locomotive engraving by William Miller after J Kindar.jpg"),
    ("faraday_lecture", "search:Faraday Christmas lecture 1856 Blaikley|RIIC"),
    ("faraday_ring", "Faradays transformer.png"),
    ("maxwell", "James Clerk Maxwell big.jpg"),
    ("mendeleev", "search:Series table designed by Dmitri Mendeleev (1869)|Series table designed by Dmitri Mendeleev (1869)"),
    ("edison_patent", "search:Drawing of the Incandescent Light Bulb by Thomas Edison 1880|Page 1 of 2"),
    ("bell_patent", "Alexander Graham Bell's Telephone Patent Drawing and Oath - NARA - 302052 (page 2).jpg"),
    ("jumbo_dynamo", "Edisons Jumbo dynamo in Pearl Street NYC.jpg"),
    ("tesla_lab", "Tesla Colorado Springs lab-primary circuit of Magnifying Transmitter.jpg"),
    ("expo1881", "Souvenir de l'Exposition internationale d'électricité, 1881, ND6068.jpg"),
    ("palais_elec", "Le palais de l'électricité et le Château d'eau, Exposition universelle 1900.jpg"),
    # 第七章 20 世纪
    ("xray", "First medical X-ray by Wilhelm Röntgen of his wife Anna Bertha Ludwig's hand - 18951222.jpg"),
    ("curie", "Marie Curie c1920.jpg"),
    ("einstein", "Einstein 1921 by F Schmutzer - restoration.jpg"),
    ("eclipse1919", "1919 eclipse negative.jpg"),
    ("solvay", "Solvay conference 1927.jpg"),
    ("michelson", "Michelson morley experiment 1887.jpg"),
    ("hudf", "Hubble ultra deep field.jpg"),
    ("m87", "Black hole - Messier 87 crop max res.jpg"),
    ("earthrise", "NASA-Apollo8-Dec24-Earthrise.jpg"),
    ("aldrin", "Aldrin Apollo 11 original.jpg"),
    ("apollo_launch", "Apollo 11 Launch - GPN-2000-000630.jpg"),
    # 第八章 计算
    # 真实底图（NASA，公有领域）
    ("bluemarble", "Whole world - land and oceans.jpg", {"width": 3840, "max": (3840, 1920)}),
    ("citylights", "Earth's City Lights by DMSP, 1994-1995 (large).jpg", {"width": 3840, "max": (3840, 1920)}),
    # 实物照片：蒸汽与电
    ("watt_engine", "Boulton-Watt steam engine, rocker beam (4804296580).jpg"),
    ("rocket_loco", "search:Robert Stephenson locomotive 1931 replica of 1829 original|view 1"),
    ("gramme", "GrammeMachine.jpg"),
    ("edison_bulb", "search:Demonstration light bulb first light bulb ever lit in public 1879|Demonstration light bulb"),
    ("bell_phone", "Bell Centennial single-pole telephone transmitter 1876.png"),
    ("siemens_loco", "1879 Siemens & Halske Wernerwerk Electric locomotive.jpg"),
    ("marconi_room", "Marconi radio room aboard the 'Olympic'.jpg"),
    # 实物照片：20 世纪与今天
    ("trinity", "Trinity Detonation T&B.jpg"),
    ("gps", "GPS Block IIIA.jpg"),
    ("ligo", "LIGO Hanford aerial 05.jpg"),
    ("hubble", "View of Hubble after Being Released from the Shuttle Atlantis (28223588012).jpg"),
    ("dsky", "Apollo display and keyboard unit (DSKY) used on F-8 DFBW DVIDS683588.jpg"),
    ("transistor", "Replica-of-first-transistor.jpg"),
    ("intel4004", "Intel 4004 Chip Layout (29983532570).jpg"),
    ("frontier", "Frontier Supercomputer (1).jpg"),
    ("ada", "Ada Lovelace portrait.jpg"),
    ("babbage", "Difference engine plate 1853.jpg"),
    ("eniac", "Two women operating ENIAC (full resolution).jpg"),
    ("bernoulli", "Diagram for the computation of Bernoulli numbers.jpg"),
    ("turing", "Alan Turing Aged 16.jpg"),
    ("colossus", "Colossus.jpg"),
    ("ibm704", "IBM Electronic Data Processing Machine - GPN-2000-001881.jpg"),
    ("arpanet", "Arpanet logical map, march 1977.png"),
    ("deepblue", "IBM Deep Blue at Computer History Museum (9361685537).jpg"),
]

OK = re.compile(r"public domain|^pd\b|^pd-|cc0|^cc by \d|^cc-by-\d", re.I)


def api(params):
    url = API + "?" + urllib.parse.urlencode(dict(params, format="json"))
    for k in range(8):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            r = json.load(urllib.request.urlopen(req, timeout=40))
            time.sleep(1.2)
            return r
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503):
                raise
            time.sleep(6 * (k + 1))
    raise RuntimeError("Commons API 限流，稍后再试")


def info(title, width=1920):
    d = api(dict(action="query", titles="File:" + title, prop="imageinfo", iiprop="url|size|extmetadata",
                 iiurlwidth=width))
    page = next(iter(d["query"]["pages"].values()))
    if "imageinfo" not in page:
        return None
    ii = page["imageinfo"][0]
    md = ii.get("extmetadata", {})
    strip = lambda s: re.sub(r"<[^>]+>", "", s or "").strip()
    return dict(title=page["title"][5:], url=ii.get("thumburl") or ii["url"], page=ii["descriptionurl"],
                width=ii["width"], height=ii["height"], license=strip(md.get("LicenseShortName", {}).get("value")),
                artist=strip(md.get("Artist", {}).get("value"))[:200],
                date=strip(md.get("DateTimeOriginal", {}).get("value"))[:60])


def resolve(spec):
    if not spec.startswith("search:"):
        return spec
    query, must = spec[7:].split("|", 1)
    d = api(dict(action="query", list="search", srsearch=query, srnamespace=6, srlimit=20))
    for hit in d["query"]["search"]:
        t = hit["title"][5:]
        if must.lower() in t.lower() and not t.lower().endswith((".pdf", ".djvu", ".webm", ".svg")):
            return t
    raise RuntimeError(f"没找到：{spec}")


def save(url, path, maxsize=(2400, 1800)):
    from PIL import Image
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    data = None
    for k in range(10):
        try:
            data = urllib.request.urlopen(req, timeout=120).read()
            break
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503):
                raise
            wait = int(e.headers.get("Retry-After") or 60)
            print(f"  （被限流，按服务器要求等待 {wait} 秒）", flush=True)
            time.sleep(min(wait, 900) + 5)
    if data is None:
        raise RuntimeError("下载被限流，稍后重试")
    time.sleep(12)
    im = Image.open(io.BytesIO(data))
    im = im.convert("RGB")
    im.thumbnail(maxsize, Image.LANCZOS)
    im.save(path, "JPEG", quality=87, optimize=True)
    return im.size


def main():
    force = "--force" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    cpath = os.path.join(OUT, "credits.json")
    credits = json.load(open(cpath, encoding="utf-8")) if os.path.exists(cpath) else {}
    for item in MANIFEST:
        key, spec = item[0], item[1]
        opts = item[2] if len(item) > 2 else {}
        path = os.path.join(OUT, key + ".jpg")
        if os.path.exists(path) and key in credits and not force:
            continue
        title = resolve(spec)
        meta = info(title, opts.get("width", 1920))
        if meta is None:
            print(f"✗ {key}: 没有这个文件 {title}")
            continue
        lic = meta["license"]
        if not OK.search(lic) or re.search(r"\bsa\b|nc|nd", lic, re.I):
            print(f"✗ {key}: 授权不符合（{lic}）{title}")
            continue
        size = save(meta["url"], path, tuple(opts.get("max", (2400, 1800))))
        meta["saved_size"] = size
        credits[key] = meta
        json.dump(credits, open(cpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"✓ {key:20s} {lic:16s} {size[0]}x{size[1]}  {title[:60]}", flush=True)
    # 署名清单
    lines = ["# 片中历史图像的来源与授权", "", "全部来自 Wikimedia Commons；只使用公有领域、CC0 或 CC BY 授权的文件。", "",
             "| 键 | 作品 / 文件 | 作者 | 授权 | 链接 |", "|---|---|---|---|---|"]
    for item in MANIFEST:
        key = item[0]
        m = credits.get(key)
        if m:
            lines.append(f"| {key} | {m['title']} | {m['artist'] or '—'} | {m['license']} | {m['page']} |")
    open(os.path.join(OUT, "CREDITS.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"共 {len(credits)} 张，署名清单 → assets/archive/CREDITS.md")


if __name__ == "__main__":
    main()
