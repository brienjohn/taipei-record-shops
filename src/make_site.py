"""Build the standalone site into ../docs (served by GitHub Pages).

    python3 src/make_site.py

stores_src.py -> stores.json -> build.py (geocodes new addresses, injects data) -> docs/index.html
"""
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(os.path.dirname(HERE), "docs")
subprocess.run([sys.executable, "-I", os.path.join(HERE, "stores_src.py")], check=True)
subprocess.run([sys.executable, os.path.join(HERE, "build.py"), "template.html", "page.html"], check=True, cwd=HERE)
page = open(os.path.join(HERE, "page.html"), encoding="utf-8").read()
os.remove(os.path.join(HERE, "page.html"))

# the 2020 docx list is credited only as 蔡政忠提供; never publish the other names
for bad in ("鄭志鵬", "高雄流行", "高流", "策展"):
    assert bad not in page, f"forbidden credit text in page: {bad}"

page = re.sub(r"<title>.*?</title>\s*", "", page, count=1)
page = page.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
domain = open(os.path.join(DOCS, "CNAME")).read().strip() if os.path.exists(os.path.join(DOCS, "CNAME")) else ""
desc = "2000 年至今台北市實體唱片行的開店、搬遷與收店：拖曳時間軸，看地圖、店家清單與各商圈聚落跟著變化。"
icon = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
        "%3Ccircle cx='16' cy='16' r='15' fill='%23141414'/%3E%3Ccircle cx='16' cy='16' r='6' fill='%23ff5a3c'/%3E"
        "%3Ccircle cx='16' cy='16' r='1.6' fill='%23141414'/%3E%3C/svg%3E")
head = f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>台北唱片行變遷地圖｜22CS</title>
<meta name="description" content="{desc}">
<meta name="author" content="Brien John">
<meta property="og:type" content="website">
<meta property="og:site_name" content="22 世紀衛星">
<meta property="og:title" content="台北唱片行變遷地圖">
<meta property="og:description" content="{desc}">
{f'<meta property="og:url" content="https://{domain}/">' if domain else ''}
<link rel="icon" href="{icon}">
<style>body{{margin:0}}[hidden]{{display:none!important}}img{{max-width:100%}}</style>
</head>
<body>
"""
open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8").write(head + page + "\n</body>\n</html>\n")
print("wrote", os.path.join(DOCS, "index.html"))
