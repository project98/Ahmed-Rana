// usage: node render.js <html> <outdir> <fps> <duration> [times-for-preview...]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [html, out, fps, dur, ...times] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(html));
  await p.evaluate(() => document.fonts.ready);
  const list = times.length ? times.map(Number) : [...Array(Math.round(dur * fps)).keys()].map(i => i / fps);
  for (let i = 0; i < list.length; i++) {
    await p.evaluate(t => render(t), list[i]);
    await p.screenshot({ path: `${out}/${String(i).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 92 });
  }
  await b.close();
})();
