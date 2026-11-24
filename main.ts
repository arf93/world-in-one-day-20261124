// Entrypoint for the news-image-20261124 entry.
//
// The picture is rendered ahead of time by render.py into entry.png.
// This program copies that file to the output directory and verifies it:
// the file must be a real PNG, 1024x1024, no larger than 1 MiB, and the
// bytes written out must match the source exactly. It only uses the
// Node standard library and performs no network or random operations,
// so running it twice produces identical output.

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const SOURCE = new URL("./entry.png", import.meta.url).pathname;
const MAX_BYTES = 1024 * 1024;
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

function fail(message: string): never {
  throw new Error(message);
}

const png = readFileSync(SOURCE);

if (png.length < 24) {
  fail("entry.png is too small to be a PNG file");
}
for (let i = 0; i < PNG_SIGNATURE.length; i++) {
  if (png[i] !== PNG_SIGNATURE[i]) {
    fail("entry.png does not start with the PNG signature");
  }
}
if (png.length > MAX_BYTES) {
  fail(`entry.png is ${png.length} bytes, over the 1 MiB limit`);
}
// The IHDR chunk stores the width at byte 16 and the height at byte 20.
const width = png.readUInt32BE(16);
const height = png.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  fail(`entry.png is ${width}x${height}, expected 1024x1024`);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
const target = join(OUTPUT_DIR, "entry.png");
copyFileSync(SOURCE, target);

const written = readFileSync(target);
if (!written.equals(png)) {
  fail("bytes read back from the output differ from entry.png");
}

console.log(`wrote ${target} (${written.length} bytes, ${width}x${height})`);
