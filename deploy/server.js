const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;
const PUBLIC = path.join(__dirname, 'public');

const MIME = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.mp4': 'video/mp4',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.ico': 'image/x-icon',
};

const server = http.createServer((req, res) => {
  let filePath = path.join(PUBLIC, req.url === '/' ? 'index.html' : req.url);
  const ext = path.extname(filePath);
  const mime = MIME[ext] || 'application/octet-stream';

  // Handle range requests for video streaming
  const stat = fs.existsSync(filePath) ? fs.statSync(filePath) : null;
  if (!stat) {
    res.writeHead(404);
    res.end('Not found');
    return;
  }

  const range = req.headers.range;
  if (range && ext === '.mp4') {
    const parts = range.replace(/bytes=/, '').split('-');
    const start = parseInt(parts[0], 10);
    const end = parts[1] ? parseInt(parts[1], 10) : stat.size - 1;
    const chunkSize = end - start + 1;
    const stream = fs.createReadStream(filePath, { start, end });
    res.writeHead(206, {
      'Content-Range': `bytes ${start}-${end}/${stat.size}`,
      'Accept-Ranges': 'bytes',
      'Content-Length': chunkSize,
      'Content-Type': mime,
    });
    stream.pipe(res);
  } else {
    res.writeHead(200, {
      'Content-Type': mime,
      'Content-Length': stat.size,
      'Cache-Control': 'public, max-age=3600',
    });
    fs.createReadStream(filePath).pipe(res);
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`\n  AI Render Lab is LIVE`);
  console.log(`  http://localhost:${PORT}\n`);
  console.log(`  Videos:`);
  console.log(`    /geopolitics-documentary.mp4  (22 MB)`);
  console.log(`    /cartoon-geopolitics.mp4      (7.6 MB)`);
  console.log(`    /full-video.mp4               (4.9 MB)`);
  console.log(`    /short-01.mp4                 (3.8 MB)\n`);
});
