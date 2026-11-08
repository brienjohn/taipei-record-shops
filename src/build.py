"""Geocode stores, assign zones, inject into template -> taipei-record-shops.html"""
import json, math, os, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, "stores.json")))
cache_p = os.path.join(HERE, "geocache.json")
cache = json.load(open(cache_p)) if os.path.exists(cache_p) else {}

def geocode(addr):
    if addr in cache:
        return cache[addr]
    q = urllib.parse.urlencode({"SingleLine": addr, "f": "json", "maxLocations": 1, "outFields": "Addr_type"})
    url = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?" + q
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "record-map-build"}), timeout=20) as r:
        d = json.load(r)
    c = d.get("candidates") or []
    res = None
    if c:
        res = {"lat": c[0]["location"]["y"], "lng": c[0]["location"]["x"], "score": c[0]["score"],
               "type": c[0]["attributes"].get("Addr_type"), "match": c[0]["address"]}
    cache[addr] = res
    time.sleep(0.2)
    return res

def dist_m(a, b):
    R = 6371000
    la1, lo1, la2, lo2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    x = (lo2 - lo1) * math.cos((la1 + la2) / 2)
    return R * math.hypot(x, la2 - la1)

problems = []
for s in data["stores"]:
    if "lat" in s and "lng" in s:
        continue
    g = geocode(s.get("geo") or s["a"])
    if not g:
        problems.append((s["id"], s["a"], "no result"))
        continue
    s["lat"], s["lng"] = round(g["lat"], 6), round(g["lng"], 6)
    if g["type"] not in ("PointAddress", "Subaddress", "POI", "StreetAddress", "StreetAddressExt"):
        problems.append((s["id"], s["a"], g["type"], g["match"]))

json.dump(cache, open(cache_p, "w"), ensure_ascii=False, indent=1)

for s in data["stores"]:
    if "lat" not in s:
        continue
    best, bd = "其他", 1e9
    for z in data["zones"]:
        d = dist_m((s["lat"], s["lng"]), (z["lat"], z["lng"]))
        if d <= z["r"] and d < bd:
            best, bd = z["n"], d
    s.setdefault("zone", best)
    s.pop("geo", None)

missing = [s["id"] for s in data["stores"] if "lat" not in s]
data["stores"] = [s for s in data["stores"] if "lat" in s]
for p in problems:
    print("CHECK", p)
print("missing", missing)
print("stores", len(data["stores"]))
from collections import Counter
print(Counter(s["zone"] for s in data["stores"]))

TPL = sys.argv[1] if len(sys.argv) > 1 else "template.html"
OUTF = sys.argv[2] if len(sys.argv) > 2 else "taipei-record-shops.html"
tpl = open(os.path.join(HERE, TPL)).read()
geo = open(os.path.join(HERE, "districts.json")).read()
out = tpl.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":"))).replace("/*GEO*/null", geo).replace("/*BASE*/null", open(os.path.join(HERE, "basemap.json")).read())
open(os.path.join(HERE, OUTF), "w").write(out)
print("bytes", len(out.encode()))
