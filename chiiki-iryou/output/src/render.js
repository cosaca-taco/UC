// 使い方: node render.js <入力.html> <出力.pdf> [出力.png]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [inp, pdf, png] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 2 });
  await page.goto('file://' + path.resolve(inp), { waitUntil: 'networkidle' });
  await page.pdf({ path: pdf, preferCSSPageSize: true, printBackground: true });
  if (png) {
    await page.setViewportSize({ width: 1123, height: 794 });
    await page.screenshot({ path: png, fullPage: false });
  }
  await browser.close();
})();
