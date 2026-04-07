// ═══════════════════════════════════════════════════════════════
// CARTOON GEO-POLITICS THEME — PRODUCTION GRADE
// ═══════════════════════════════════════════════════════════════

import { FONTS } from './fonts';

// ──── COLOR SYSTEM ────
export const C = {
  // Backgrounds
  bgDark: '#0c0714',
  bgPanel: '#14102a',
  bgMap: '#0a1220',
  bgCard: '#1a1535',
  bgElevated: '#201a40',

  // Character colors (saturated)
  charRed: '#ef4444',
  charBlue: '#3b82f6',
  charGold: '#eab308',
  charGreen: '#22c55e',
  charPurple: '#a855f7',
  charOrange: '#f97316',

  // Character colors (light — for gradients)
  charRedLight: '#fca5a5',
  charBlueLight: '#93c5fd',
  charGoldLight: '#fde047',
  charGreenLight: '#86efac',
  charPurpleLight: '#d8b4fe',
  charOrangeLight: '#fdba74',

  // UI
  speechBg: '#ffffff',
  speechBorder: '#1e293b',
  speechText: '#0f172a',
  captionBg: 'rgba(0,0,0,0.82)',

  // Map
  mapLand: '#1e3a5f',
  mapOcean: '#0a1628',
  mapHighlight: '#ef4444',
  mapLine: '#eab308',

  // Accents
  danger: '#ef4444',
  warning: '#f59e0b',
  info: '#3b82f6',
  mystery: '#a855f7',
  glow: '#eab308',
  success: '#22c55e',

  // Text
  textWhite: '#f8fafc',
  textLight: '#cbd5e1',
  textMuted: '#64748b',
  textDark: '#1e293b',
  textAccent: '#eab308',

  // Outline
  outline: '#1e293b',
  outlineLight: '#334155',
} as const;

// ──── FONT SYSTEM (Google Fonts via @remotion/google-fonts) ────
export const CFONT = {
  title: FONTS.title,
  display: FONTS.display,
  body: FONTS.body,
  mono: FONTS.mono,
  caption: FONTS.body,
} as const;

// ──── GRADIENT PRESETS ────
export const GRADIENT = {
  blueViolet: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
  goldOrange: 'linear-gradient(135deg, #eab308, #f97316)',
  redPink: 'linear-gradient(135deg, #ef4444, #ec4899)',
  greenTeal: 'linear-gradient(135deg, #22c55e, #14b8a6)',
  purpleMystery: 'linear-gradient(135deg, #a855f7, #6366f1)',
  darkToBlue: 'linear-gradient(180deg, #0c0714 0%, #0a1628 100%)',
  subtleGlow: (color: string) => `radial-gradient(ellipse at center, ${color}18 0%, transparent 70%)`,
} as const;

// ──── SHADOW PRESETS ────
export const SHADOW = {
  card: '0 8px 32px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.04)',
  glow: (color: string) => `0 0 40px ${color}33, 0 0 80px ${color}11`,
  depth: '0 16px 48px rgba(0,0,0,0.6)',
  text: (color: string) => `0 2px 8px ${color}66, 0 0 20px ${color}22`,
  inset: 'inset 0 -4px 12px rgba(0,0,0,0.3)',
} as const;

// ──── SPACING SCALE ────
export const SP = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  '2xl': 48,
  '3xl': 64,
  '4xl': 96,
} as const;

// ──── RADIUS ────
export const RAD = {
  sm: 6,
  md: 12,
  lg: 16,
  xl: 24,
  full: 999,
} as const;

// ──── SPRING CONFIG PRESETS ────
export const SPRING = {
  snappy: { damping: 18, stiffness: 200, mass: 0.6 },
  smooth: { damping: 14, stiffness: 100, mass: 1.0 },
  bouncy: { damping: 8, stiffness: 170, mass: 0.8 },
  dramatic: { damping: 10, stiffness: 80, mass: 1.2 },
  gentle: { damping: 20, stiffness: 60, mass: 1.0 },
} as const;

// ──── SCENE TIMINGS (frames at 30fps) ────
export const CARTOON_SCENES = {
  intro:      { start: 0,    duration: 120 },
  scene1:     { start: 120,  duration: 210 },
  scene2:     { start: 330,  duration: 240 },
  scene3:     { start: 570,  duration: 210 },
  scene4:     { start: 780,  duration: 210 },
  scene5:     { start: 990,  duration: 180 },
  outro:      { start: 1170, duration: 120 },
} as const;

export const CARTOON_TOTAL = 1290;
