// Render each SVG in a directory to PNG at 2x.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = process.argv[2], out = process.argv[3];
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 2 });
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.svg'))) {
    const svg = fs.readFileSync(path.join(dir, f), 'utf8');
    const m = svg.match(/width="(\d+)" height="(\d+)"/);
    await page.setViewportSize({ width: +m[1], height: +m[2] });
    await page.setContent(`<html><body style="margin:0">${svg}</body></html>`);
    await page.screenshot({ path: path.join(out, f.replace('.svg', '.png')), clip: { x: 0, y: 0, width: +m[1], height: +m[2] } });
  }
  await browser.close();
})();
