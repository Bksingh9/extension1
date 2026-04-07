// ═══════════════════════════════════════════════════════════════
// ANIMATION SYSTEM — Hollywood-grade motion utilities
// ═══════════════════════════════════════════════════════════════

import { interpolate, spring, Easing } from 'remotion';
import { noise2D } from '@remotion/noise';
import { SPRING } from './theme';

const CLAMP = { extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const };

// ──── OPACITY ────
export const fadeIn = (frame: number, start: number, dur = 14): number =>
  interpolate(frame, [start, start + dur], [0, 1], CLAMP);

export const fadeOut = (frame: number, start: number, dur = 12): number =>
  interpolate(frame, [start, start + dur], [1, 0], CLAMP);

export const sceneFade = (frame: number, totalFrames: number, fadeDur = 12): number =>
  Math.min(fadeIn(frame, 0, fadeDur), fadeOut(frame, totalFrames - fadeDur, fadeDur));

// ──── POSITION ────
export const slideUp = (frame: number, start: number, dist = 40, dur = 18): number =>
  interpolate(frame, [start, start + dur], [dist, 0], { ...CLAMP, easing: Easing.out(Easing.cubic) });

export const slideDown = (frame: number, start: number, dist = 40, dur = 18): number =>
  interpolate(frame, [start, start + dur], [-dist, 0], { ...CLAMP, easing: Easing.out(Easing.cubic) });

export const slideRight = (frame: number, start: number, dist = 60, dur = 18): number =>
  interpolate(frame, [start, start + dur], [-dist, 0], { ...CLAMP, easing: Easing.out(Easing.cubic) });

export const slideLeft = (frame: number, start: number, dist = 60, dur = 18): number =>
  interpolate(frame, [start, start + dur], [dist, 0], { ...CLAMP, easing: Easing.out(Easing.cubic) });

// ──── SCALE ────
export const scaleIn = (frame: number, start: number, fps: number, config = SPRING.snappy): number =>
  spring({ frame: frame - start, fps, config });

export const bounceIn = (frame: number, start: number, fps: number): number =>
  spring({ frame: frame - start, fps, config: SPRING.bouncy });

export const elasticScale = (frame: number, start: number, fps: number): number =>
  spring({ frame: frame - start, fps, config: { damping: 5, stiffness: 200, mass: 0.6 } });

export const dramaticScale = (frame: number, start: number, fps: number): number =>
  spring({ frame: frame - start, fps, config: SPRING.dramatic });

// ──── WIDTH/SIZE ────
export const widthGrow = (frame: number, start: number, dur: number, max: number): number =>
  interpolate(frame, [start, start + dur], [0, max], { ...CLAMP, easing: Easing.out(Easing.cubic) });

export const barGrow = (frame: number, start: number, dur: number, pct: number): number =>
  interpolate(frame, [start, start + dur], [0, pct], { ...CLAMP, easing: Easing.out(Easing.exp) });

// ──── COUNTER ────
export const countUp = (frame: number, start: number, dur: number, target: number): number => {
  const raw = interpolate(frame, [start, start + dur], [0, target], { ...CLAMP, easing: Easing.out(Easing.cubic) });
  return Math.round(raw);
};

export const formatNumber = (n: number): string => {
  if (n >= 1e12) return `$${(n / 1e12).toFixed(1)}T`;
  if (n >= 1e9) return `$${(n / 1e9).toFixed(1)}B`;
  if (n >= 1e6) return `$${(n / 1e6).toFixed(0)}M`;
  if (n >= 1e3) return n.toLocaleString();
  return String(n);
};

// ──── TYPEWRITER ────
export const typewriter = (text: string, frame: number, start: number, speed = 0.5): string => {
  const chars = Math.floor(
    interpolate(frame, [start, start + text.length / speed], [0, text.length], CLAMP)
  );
  return text.slice(0, chars);
};

// ──── NOISE & ORGANIC MOTION ────
export const noiseWobble = (frame: number, seed: string, intensity = 3, speed = 0.04): number =>
  noise2D(seed, frame * speed, 0) * intensity;

export const noiseX = (frame: number, id: number, intensity = 5): number =>
  noise2D('x', frame * 0.03, id) * intensity;

export const noiseY = (frame: number, id: number, intensity = 5): number =>
  noise2D('y', frame * 0.03, id) * intensity;

// ──── PARALLAX ────
export const parallax = (frame: number, depth: number, speed = 0.3): number =>
  frame * speed * depth;

// ──── GLOW & PULSE ────
export const glowPulse = (frame: number, min = 0.4, max = 1, speed = 0.06): number =>
  min + (max - min) * (0.5 + 0.5 * Math.sin(frame * speed));

export const breathe = (frame: number, amount = 0.02, speed = 0.04): number =>
  1 + Math.sin(frame * speed) * amount;

// ──── STAGGER ────
export const stagger = (index: number, baseDelay = 6): number => index * baseDelay;

export const staggerGrid = (row: number, col: number, delayPerUnit = 4): number =>
  (row + col) * delayPerUnit;

// ──── ROTATION ────
export const rotate = (frame: number, start: number, dur: number, maxDeg: number): number =>
  interpolate(frame, [start, start + dur], [0, maxDeg], { ...CLAMP, easing: Easing.out(Easing.cubic) });

export const wobbleRotate = (frame: number, amount = 2, speed = 0.08): number =>
  Math.sin(frame * speed) * amount;

// ──── EASING PRESETS ────
export const EASE = {
  outCubic: Easing.out(Easing.cubic),
  outExp: Easing.out(Easing.exp),
  outQuart: Easing.out(Easing.poly(4)),
  inOutCubic: Easing.inOut(Easing.cubic),
  inOutQuart: Easing.inOut(Easing.poly(4)),
  bounce: Easing.bounce,
  elastic: Easing.elastic(1),
} as const;

// ──── CURSOR BLINK ────
export const cursorBlink = (frame: number, speed = 0.3): number =>
  Math.sin(frame * speed) > 0 ? 1 : 0;
