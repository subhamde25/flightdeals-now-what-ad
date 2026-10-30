// Usage:
//   node render.mjs stills 0.6 2.4 4.6 ...   -> build/stills/t_<t>.png
//   node render.mjs video [fps]               -> build/video_noaudio.mp4 (+ build/captions.srt)
import { chromium } from 'playwright-core';
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const [mode = 'stills', ...rest] = process.argv.slice(2);

const browser = await chromium.launch({ channel: 'msedge', args: ['--force-color-profile=srgb', '--hide-scrollbars'] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
page.on('pageerror', e => console.error('PAGE ERROR:', e.message));
await page.goto(pathToFileURL(path.join(here, 'h169', 'index.html')).href);
await page.waitForFunction(() => window.__ready === true, null, { timeout: 60000 });
const clip = { x: 0, y: 0, width: 1920, height: 1080 };

if (mode === 'stills') {
  mkdirSync(path.join(here, 'build', 'stills'), { recursive: true });
  for (const t of rest.map(Number)) {
    await page.evaluate(t => window.seek(t), t);
    await page.screenshot({ path: path.join(here, 'build', 'stills', `t_${t.toFixed(2)}.png`), clip });
    console.log('still', t);
  }
} else {
  const fps = Number(rest[0] || 60);
  const dur = await page.evaluate(() => window.DUR);
  const n = Math.round(dur * fps);
  mkdirSync(path.join(here, 'build'), { recursive: true });
  writeFileSync(path.join(here, 'build', 'captions.srt'), await page.evaluate(() => window.getSRT()));
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
    path.join(here, 'build', 'video_noaudio.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let f = 0; f < n; f++) {
    await page.evaluate(t => window.seek(t), f / fps);
    const buf = await page.screenshot({ type: 'png', clip });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 60 === 0) console.log(`frame ${f}/${n}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  console.log('done', n, 'frames');
}
await browser.close();
