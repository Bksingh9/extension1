/**
 * Cloud Upload Script — Cloudflare R2 (S3-compatible)
 *
 * Upload rendered videos to Cloudflare R2 for public access.
 * R2 has zero egress cost — unlimited downloads for free.
 *
 * Setup:
 * 1. Create Cloudflare account: https://dash.cloudflare.com
 * 2. Go to R2 → Create bucket (e.g. "ai-render-lab")
 * 3. Go to R2 → Manage R2 API Tokens → Create API Token
 * 4. Copy Account ID, Access Key ID, Secret Access Key
 * 5. Add to .env file (see .env.example)
 * 6. Run: node upload.mjs
 */

import { S3Client, PutObjectCommand, ListObjectsV2Command } from '@aws-sdk/client-s3';
import { readFileSync, readdirSync, statSync } from 'fs';
import { join, extname, basename } from 'path';

// Load env
const envFile = readFileSync('.env', 'utf-8');
const env = {};
envFile.split('\n').forEach(line => {
  const [key, ...val] = line.split('=');
  if (key && val.length) env[key.trim()] = val.join('=').trim();
});

const R2_ACCOUNT_ID = env.R2_ACCOUNT_ID;
const R2_ACCESS_KEY = env.R2_ACCESS_KEY_ID;
const R2_SECRET_KEY = env.R2_SECRET_ACCESS_KEY;
const R2_BUCKET = env.R2_BUCKET || 'ai-render-lab';
const R2_PUBLIC_URL = env.R2_PUBLIC_URL || `https://${R2_BUCKET}.${R2_ACCOUNT_ID}.r2.cloudflarestorage.com`;

if (!R2_ACCOUNT_ID || !R2_ACCESS_KEY || !R2_SECRET_KEY) {
  console.error('\n  Missing R2 credentials in .env file!');
  console.error('  Copy .env.example to .env and fill in your Cloudflare R2 details.\n');
  console.error('  Get credentials at: https://dash.cloudflare.com → R2 → Manage R2 API Tokens\n');
  process.exit(1);
}

const s3 = new S3Client({
  region: 'auto',
  endpoint: `https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com`,
  credentials: {
    accessKeyId: R2_ACCESS_KEY,
    secretAccessKey: R2_SECRET_KEY,
  },
});

const MIME_TYPES = {
  '.mp4': 'video/mp4',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.html': 'text/html',
};

async function upload(filePath, key) {
  const body = readFileSync(filePath);
  const ext = extname(filePath);
  const contentType = MIME_TYPES[ext] || 'application/octet-stream';
  const size = (statSync(filePath).size / 1024 / 1024).toFixed(1);

  console.log(`  Uploading ${key} (${size} MB)...`);
  await s3.send(new PutObjectCommand({
    Bucket: R2_BUCKET,
    Key: key,
    Body: body,
    ContentType: contentType,
  }));
  console.log(`  ✓ ${key} uploaded → ${R2_PUBLIC_URL}/${key}`);
}

async function main() {
  console.log('\n  ╔══════════════════════════════════════╗');
  console.log('  ║   AI Render Lab — Cloud Upload       ║');
  console.log('  ║   Cloudflare R2 (zero egress cost)   ║');
  console.log('  ╚══════════════════════════════════════╝\n');

  const outDir = join(import.meta.dirname, 'out');
  const files = readdirSync(outDir).filter(f =>
    ['.mp4', '.png'].includes(extname(f))
  );

  console.log(`  Found ${files.length} files to upload:\n`);

  for (const file of files) {
    await upload(join(outDir, file), `videos/${file}`);
  }

  console.log('\n  All uploads complete!\n');
  console.log('  Public URLs:');
  for (const file of files) {
    console.log(`    ${R2_PUBLIC_URL}/videos/${file}`);
  }
  console.log('');
}

main().catch(err => {
  console.error('Upload failed:', err.message);
  process.exit(1);
});
