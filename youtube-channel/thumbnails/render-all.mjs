import { execSync } from 'child_process';

const thumbs = [
  'Thumb01-PromptToVideo',
  'Thumb02-StockSim',
  'Thumb03-RemotionGuide',
  'Thumb04-ClaudeCode',
  'Thumb05-Workflow',
];

const browserFlag = '--browser-executable=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell';

for (const id of thumbs) {
  console.log(`\nRendering ${id}...`);
  try {
    execSync(
      `npx remotion still src/index.ts ${id} out/${id}.png ${browserFlag}`,
      { stdio: 'inherit' }
    );
    console.log(`✓ ${id} rendered`);
  } catch (e) {
    console.error(`✗ ${id} failed`);
  }
}

console.log('\nAll thumbnails rendered to out/');
