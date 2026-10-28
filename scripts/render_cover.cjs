// 用法：node render_cover.cjs <html 绝对路径> <输出目录> <元素 id...>，每个 id 截成 <输出目录>/<id>.png
// 用 Playwright 自带的无头 chromium，不用系统 Chrome（真 Chrome 会在 Dock 闪）。
const { chromium } = require(process.env.PLAYWRIGHT_CORE || "/opt/homebrew/lib/node_modules/@playwright/test/node_modules/playwright-core");
(async () => {
  const [html, outdir, ...ids] = process.argv.slice(2);
  const b = await chromium.launch({ headless: true });
  const p = await b.newPage({ viewport: { width: 2000, height: 1800 } });
  await p.goto('file://' + html); await p.waitForTimeout(1200);
  for (const id of ids) await p.locator('#' + id).screenshot({ path: `${outdir}/${id}.png` });
  await b.close();
})();
