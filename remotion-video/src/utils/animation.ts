import { interpolate, spring, Easing } from 'remotion';

export const fadeIn = (frame: number, start: number, duration = 15): number =>
  interpolate(frame, [start, start + duration], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

export const fadeOut = (frame: number, start: number, duration = 12): number =>
  interpolate(frame, [start, start + duration], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

export const slideUp = (frame: number, start: number, distance = 40, duration = 18): number =>
  interpolate(frame, [start, start + duration], [distance, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

export const slideRight = (frame: number, start: number, distance = 60, duration = 18): number =>
  interpolate(frame, [start, start + duration], [-distance, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

export const scaleIn = (frame: number, start: number, fps: number): number =>
  spring({ frame: frame - start, fps, config: { damping: 14, stiffness: 120, mass: 0.8 } });

export const widthGrow = (frame: number, start: number, duration: number, maxWidth: number): number =>
  interpolate(frame, [start, start + duration], [0, maxWidth], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.cubic),
  });

export const stagger = (index: number, baseDelay = 6): number => index * baseDelay;
