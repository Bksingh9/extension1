#!/usr/bin/env node
/**
 * YouTube Upload Automation
 * =========================
 * Uploads rendered videos to YouTube via Data API v3.
 *
 * Setup:
 * 1. Go to https://console.cloud.google.com
 * 2. Create project → Enable YouTube Data API v3
 * 3. Create OAuth 2.0 credentials (Desktop app)
 * 4. Download client_secret.json to this directory
 * 5. Run: node scripts/youtube-upload.mjs --auth (first time)
 * 6. Run: node scripts/youtube-upload.mjs --all
 *
 * Usage:
 *   node scripts/youtube-upload.mjs --auth                    # First-time auth
 *   node scripts/youtube-upload.mjs --file out/short-petrodollar.mp4 --title "..."
 *   node scripts/youtube-upload.mjs --all                     # Upload all videos
 *   node scripts/youtube-upload.mjs --shorts                  # Upload all Shorts
 *   node scripts/youtube-upload.mjs --schedule "2026-04-14T09:00:00Z"
 */

import { google } from 'googleapis';
import { readFileSync, existsSync, createReadStream } from 'fs';
import { join, basename } from 'path';
import { createInterface } from 'readline';

const SCRIPT_DIR = import.meta.dirname;
const PROJECT_DIR = join(SCRIPT_DIR, '..');
const OUT_DIR = join(PROJECT_DIR, 'out');
const CLIENT_SECRET = join(SCRIPT_DIR, 'client_secret.json');
const TOKEN_FILE = join(SCRIPT_DIR, '.youtube-token.json');

// ─── Video metadata templates ───
const VIDEOS = {
  'geopolitics-final.mp4': {
    title: 'Who Actually Runs This Planet? | Geo-Politics Documentary',
    description: `🔴 The facts they don't want you to know.

Every claim is sourced. Every number is real. This is not conspiracy — it's public record.

📊 Sources: Brown University, IMF, World Bank, SIPRI, BIS, OECD
🎬 Made with: Remotion + Open-Source AI (100% code-generated)

⏱️ Chapters:
0:00 — Who Runs This Planet?
0:08 — Ch1: The Petrodollar System
1:15 — Ch2: The Chip War
2:20 — Ch3: Energy Chess
3:10 — Ch4: BRICS Rising
3:50 — Ch5: Middle East Chess
4:25 — Ch6: The Watchers
5:00 — Ch7: War Machine

🔔 Subscribe for weekly deep dives into uncomfortable truths.

#geopolitics #conspiracy #documentary #AI #petrodollar #BRICS

⚠️ For entertainment & educational purposes. Always do your own research.`,
    tags: ['geopolitics', 'conspiracy', 'documentary', 'petrodollar', 'BRICS', 'chip war', 'surveillance', 'military industrial complex', 'animated explainer', 'AI'],
    category: '25', // News & Politics
    privacy: 'public',
  },
  'short-petrodollar.mp4': {
    title: 'Every Country That Ditched the Dollar Got Invaded #shorts',
    description: '🔴 Iraq, Libya, Venezuela, Iran... see the pattern?\n\n#geopolitics #conspiracy #shorts #petrodollar',
    tags: ['geopolitics', 'petrodollar', 'shorts', 'conspiracy', 'dollar collapse'],
    category: '25',
    privacy: 'public',
  },
  'short-chipwar.mp4': {
    title: 'One Island Makes 90% of ALL Chips #shorts',
    description: '🔴 TSMC, Taiwan, and the $52.7B chip war.\n\n#chipwar #geopolitics #shorts #TSMC #taiwan',
    tags: ['chip war', 'TSMC', 'taiwan', 'huawei', 'shorts', 'geopolitics'],
    category: '28', // Science & Technology
    privacy: 'public',
  },
  'short-nordstream.mp4': {
    title: 'Who Blew Up Nord Stream? Nobody Knows. #shorts',
    description: '🔴 $18 billion destroyed. Zero arrests.\n\n#nordstream #geopolitics #shorts #conspiracy',
    tags: ['nord stream', 'pipeline', 'sabotage', 'geopolitics', 'shorts'],
    category: '25',
    privacy: 'public',
  },
  'short-brics.mp4': {
    title: 'The Anti-Dollar Group Chat (BRICS) #shorts',
    description: '🔴 Central banks hoarding gold like doomsday preppers with PhDs.\n\n#BRICS #dollar #shorts',
    tags: ['BRICS', 'de-dollarization', 'gold', 'shorts', 'geopolitics'],
    category: '25',
    privacy: 'public',
  },
  'short-oil.mp4': {
    title: 'Oil Went NEGATIVE — They Paid You to Take It #shorts',
    description: '🔴 From -$37 to $120. OPEC controls the game.\n\n#oil #OPEC #shorts #geopolitics',
    tags: ['oil', 'OPEC', 'oil price', 'shorts', 'geopolitics'],
    category: '25',
    privacy: 'public',
  },
  'short-surveillance.mp4': {
    title: 'Your Phone is a Snitch #shorts',
    description: '🔴 Five Eyes, PRISM, 600M cameras. Privacy is dead.\n\n#surveillance #privacy #shorts #snowden',
    tags: ['surveillance', 'privacy', 'snowden', 'NSA', 'shorts', 'five eyes'],
    category: '25',
    privacy: 'public',
  },
  'short-warmachine.mp4': {
    title: '$886 Billion Per Year on War #shorts',
    description: '🔴 More than the next 10 countries combined. For "defense."\n\n#military #war #shorts #geopolitics',
    tags: ['military', 'defense budget', 'war machine', 'shorts', 'geopolitics'],
    category: '25',
    privacy: 'public',
  },
};

// ─── Auth helpers ───
async function getAuthClient() {
  if (!existsSync(CLIENT_SECRET)) {
    console.error('\n  [ERROR] client_secret.json not found!');
    console.error('  Download from: https://console.cloud.google.com/apis/credentials');
    console.error(`  Save to: ${CLIENT_SECRET}\n`);
    process.exit(1);
  }

  const creds = JSON.parse(readFileSync(CLIENT_SECRET, 'utf-8'));
  const { client_id, client_secret, redirect_uris } = creds.installed || creds.web;

  const oauth2 = new google.auth.OAuth2(client_id, client_secret, redirect_uris[0]);

  if (existsSync(TOKEN_FILE)) {
    const tokens = JSON.parse(readFileSync(TOKEN_FILE, 'utf-8'));
    oauth2.setCredentials(tokens);
    return oauth2;
  }

  // First-time auth flow
  const authUrl = oauth2.generateAuthUrl({
    access_type: 'offline',
    scope: ['https://www.googleapis.com/auth/youtube.upload'],
  });

  console.log('\n  Open this URL in your browser:\n');
  console.log(`  ${authUrl}\n`);

  const rl = createInterface({ input: process.stdin, output: process.stdout });
  const code = await new Promise(resolve => {
    rl.question('  Paste the authorization code: ', resolve);
  });
  rl.close();

  const { tokens } = await oauth2.getToken(code);
  oauth2.setCredentials(tokens);

  const { writeFileSync } = await import('fs');
  writeFileSync(TOKEN_FILE, JSON.stringify(tokens, null, 2));
  console.log('  [OK] Token saved. You won\'t need to auth again.\n');

  return oauth2;
}

// ─── Upload function ───
async function uploadVideo(auth, filePath, metadata, scheduledDate) {
  const youtube = google.youtube({ version: 'v3', auth });
  const fileName = basename(filePath);
  const fileSize = readFileSync(filePath).length;
  const sizeMB = (fileSize / 1024 / 1024).toFixed(1);

  console.log(`  Uploading: ${fileName} (${sizeMB} MB)...`);

  const resource = {
    snippet: {
      title: metadata.title,
      description: metadata.description,
      tags: metadata.tags,
      categoryId: metadata.category,
    },
    status: {
      privacyStatus: metadata.privacy || 'public',
    },
  };

  // Schedule for later if specified
  if (scheduledDate) {
    resource.status.privacyStatus = 'private';
    resource.status.publishAt = scheduledDate;
    console.log(`  Scheduled for: ${scheduledDate}`);
  }

  const res = await youtube.videos.insert({
    part: 'snippet,status',
    requestBody: resource,
    media: {
      body: createReadStream(filePath),
    },
  });

  console.log(`  [OK] Uploaded: https://youtube.com/watch?v=${res.data.id}`);
  return res.data;
}

// ─── Main ───
async function main() {
  const args = process.argv.slice(2);

  console.log('\n  ╔═══════════════════════════════════════════╗');
  console.log('  ║  YouTube Upload — AI Render Lab            ║');
  console.log('  ║  Automated via YouTube Data API v3         ║');
  console.log('  ╚═══════════════════════════════════════════╝\n');

  const auth = await getAuthClient();

  if (args.includes('--auth')) {
    console.log('  Auth complete. Ready to upload.\n');
    return;
  }

  const schedule = args.includes('--schedule')
    ? args[args.indexOf('--schedule') + 1]
    : null;

  let filesToUpload = [];

  if (args.includes('--all')) {
    filesToUpload = Object.keys(VIDEOS).map(f => ({
      path: join(OUT_DIR, f),
      meta: VIDEOS[f],
    }));
  } else if (args.includes('--shorts')) {
    filesToUpload = Object.keys(VIDEOS)
      .filter(f => f.startsWith('short-'))
      .map(f => ({ path: join(OUT_DIR, f), meta: VIDEOS[f] }));
  } else if (args.includes('--file')) {
    const filePath = args[args.indexOf('--file') + 1];
    const fileName = basename(filePath);
    const meta = VIDEOS[fileName] || {
      title: args.includes('--title') ? args[args.indexOf('--title') + 1] : fileName,
      description: 'Uploaded by AI Render Lab',
      tags: ['geopolitics', 'AI'],
      category: '25',
      privacy: 'public',
    };
    filesToUpload = [{ path: filePath, meta }];
  } else {
    console.log('  Usage:');
    console.log('    --auth              First-time authentication');
    console.log('    --all               Upload all videos');
    console.log('    --shorts            Upload all Shorts');
    console.log('    --file <path>       Upload specific file');
    console.log('    --schedule <date>   Schedule publish date (ISO 8601)');
    console.log('');
    return;
  }

  // Filter to existing files
  filesToUpload = filesToUpload.filter(f => {
    if (!existsSync(f.path)) {
      console.log(`  [SKIP] ${basename(f.path)} — not found`);
      return false;
    }
    return true;
  });

  console.log(`  Uploading ${filesToUpload.length} videos...\n`);

  for (const { path, meta } of filesToUpload) {
    try {
      await uploadVideo(auth, path, meta, schedule);
    } catch (err) {
      console.error(`  [ERROR] ${basename(path)}: ${err.message}`);
    }
  }

  console.log('\n  All done!\n');
}

main().catch(err => {
  console.error('Fatal:', err.message);
  process.exit(1);
});
