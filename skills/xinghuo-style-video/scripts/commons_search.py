"""Commons 检索：python cs.py "查询1" "查询2" ... → 打印候选（标题、授权、尺寸）"""
import json, re, sys, urllib.parse, urllib.request, urllib.error
UA = "xinghuo-video/1.0 (educational, non-commercial)"
OK = re.compile(r"public domain|^pd|cc0|cc[- ]by[- ](?!sa)\d|cc by \d|^cc-by-\d", re.I)

import time
def q(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    for k in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            r = json.load(urllib.request.urlopen(req, timeout=30))
            time.sleep(1.5)
            return r
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(5 * (k + 1))
    raise SystemExit("rate limited")

for term in sys.argv[1:]:
    d = q(dict(action="query", format="json", generator="search", gsrsearch=term, gsrnamespace=6, gsrlimit=12,
               prop="imageinfo", iiprop="url|size|extmetadata", iiextmetadatafilter="LicenseShortName|Artist|DateTimeOriginal"))
    print(f"\n### {term}")
    pages = sorted((d.get("query", {}).get("pages", {}) or {}).values(), key=lambda p: p.get("index", 99))
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        lic = md.get("LicenseShortName", {}).get("value", "?")
        ok = "OK" if OK.search(lic) and "sa" not in lic.lower() else "--"
        print(f"  {ok} {lic[:22]:22s} {ii.get('width')}x{ii.get('height')}  {p['title'][5:][:90]}")
