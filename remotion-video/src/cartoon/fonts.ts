// Font system — using high-quality system font stacks
// Since Google Fonts CDN is unavailable in this render environment,
// we use premium system font stacks that look professional

export const FONTS = {
  title: '"Segoe UI", "Helvetica Neue", Arial, sans-serif',
  display: 'system-ui, -apple-system, "Segoe UI", Helvetica, sans-serif',
  body: '"Segoe UI", system-ui, -apple-system, sans-serif',
  mono: '"Cascadia Code", "Fira Code", "SF Mono", "Consolas", monospace',
} as const;
