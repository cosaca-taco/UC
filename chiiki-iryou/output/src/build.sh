#!/bin/bash
# 出力: ../<名前>.pdf（印刷・配布用）と ../<名前>.docx（編集用）
set -e
cd "$(dirname "$0")"
cp ../01_概要図.png overview.png   # 各資料に概要図を埋め込む
for md in 0[2-9]_*.md; do
  name="${md%.md}"
  pandoc "$md" -s -c doc.css -o "$name.html"
  node render.js "$name.html" "../$name.pdf"
  pandoc "$md" -o "../$name.docx"
  rm "$name.html"
done
rm overview.png
