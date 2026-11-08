# 台北唱片行變遷地圖

2000 年至今台北市實體唱片行的開店、搬遷與收店。網站：https://records.22cs.xyz/

- `docs/`：GitHub Pages 發布的網站（`index.html`、照片、頭像、`CNAME`）
- `src/`：資料與產生網站的程式
  - `stores_src.py`：店家、來源、搬遷關係的原始資料（要改資料就改這裡）
  - `template.html`：網頁版型
  - `build.py`：地址轉座標（結果存在 `geocache.json`）並把資料塞進版型
  - `make_site.py`：一次跑完上面三步，輸出 `docs/index.html`

## 更新網站

```bash
python3 src/make_site.py
git add -A && git commit -m "更新資料" && git push
```

推上去後約一分鐘，GitHub Pages 會自動更新。
