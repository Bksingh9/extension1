export const COLORS = {
  bg: '#0a0a0f',
  bgCard: '#12121a',
  bgCardHover: '#1a1a28',
  primary: '#3b82f6',
  primaryGlow: '#2563eb',
  secondary: '#6366f1',
  success: '#22c55e',
  successGlow: '#16a34a',
  warning: '#f59e0b',
  danger: '#ef4444',
  textPrimary: '#f1f5f9',
  textSecondary: '#94a3b8',
  textMuted: '#64748b',
  border: '#1e293b',
  borderLight: '#334155',
  gridLine: 'rgba(59, 130, 246, 0.06)',
} as const;

export const FONT = {
  heading: 'Inter, system-ui, -apple-system, sans-serif',
  mono: '"SF Mono", "Fira Code", "Cascadia Code", monospace',
  body: 'Inter, system-ui, sans-serif',
} as const;

export const SPACING = {
  xs: 8,
  sm: 16,
  md: 24,
  lg: 40,
  xl: 64,
  xxl: 96,
} as const;

export const RADIUS = {
  sm: 6,
  md: 12,
  lg: 16,
  xl: 24,
} as const;

export const SHADOW = {
  card: '0 4px 24px rgba(0,0,0,0.4), 0 0 0 1px rgba(59,130,246,0.08)',
  glow: '0 0 40px rgba(59,130,246,0.15)',
  successGlow: '0 0 40px rgba(34,197,94,0.2)',
} as const;
