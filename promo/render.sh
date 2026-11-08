#!/bin/sh
# Render the social promo images from poster_template.html (uses the site's data via src/build.py).
#   sh promo/render.sh
# Output (exact sizes): promo/out/ig-fb-threads-1080x1350.png, story-1080x1920.png, link-preview-1200x630.png
set -e
cd "$(dirname "$0")/.."
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
python3 -I src/stores_src.py >/dev/null
python3 src/build.py ../promo/poster_template.html ../promo/poster.html >/dev/null
mkdir -p promo/out
shot() { # format width height outfile
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
    --window-size="$2,$3" --virtual-time-budget=15000 --allow-file-access-from-files \
    --screenshot="promo/out/.tmp.png" "file://$PWD/promo/poster.html?f=$1" >/dev/null 2>&1
  sips --resampleWidth "$2" "promo/out/.tmp.png" --out "promo/out/$4" >/dev/null
  rm -f promo/out/.tmp.png
  echo "promo/out/$4 $(sips -g pixelWidth -g pixelHeight "promo/out/$4" | awk '/pixel/{printf "%s ", $2}')"
}
shot portrait 1080 1350 ig-fb-threads-1080x1350.png
shot story 1080 1920 story-1080x1920.png
shot wide 1200 630 link-preview-1200x630.png
cp promo/out/link-preview-1200x630.png docs/img/og.png  # the site's share thumbnail (og:image)
