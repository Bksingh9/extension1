import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate, Easing } from 'remotion';
import { CartoonBg } from './CartoonBg';
import { C, CFONT } from '../theme';

export const ChapterTitle: React.FC<{
  chapter: number;
  title: string;
  subtitle: string;
  color: string;
  icon: string;
}> = ({ chapter, title, subtitle, color, icon }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({ frame: frame - 10, fps, config: { damping: 10, stiffness: 120 } });
  const fadeIn = interpolate(frame, [0, 15], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const fadeOut = interpolate(frame, [140, 160], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const lineW = interpolate(frame, [30, 60], [0, 400], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });

  return (
    <AbsoluteFill style={{ opacity: Math.min(fadeIn, fadeOut) }}>
      <CartoonBg color="#0a0518" />
      <AbsoluteFill style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', gap: 16 }}>
        <div style={{ opacity: fadeIn, fontSize: 14, fontFamily: CFONT.title, color: C.textLight, letterSpacing: '0.15em' }}>
          CHAPTER {chapter}
        </div>
        <div style={{ fontSize: 64, marginBottom: 4, transform: `scale(${scale})` }}>{icon}</div>
        <div style={{
          transform: `scale(${scale})`,
          fontSize: 62,
          fontFamily: CFONT.title,
          fontWeight: 900,
          color,
          letterSpacing: '0.04em',
          textTransform: 'uppercase',
          textShadow: `3px 3px 0px ${C.outline}, 0 0 20px ${color}44`,
          textAlign: 'center',
          lineHeight: 1.1,
        }}>
          {title}
        </div>
        <div style={{ width: lineW, height: 4, backgroundColor: color, borderRadius: 2 }} />
        <div style={{
          opacity: interpolate(frame, [40, 55], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
          fontSize: 22,
          fontFamily: CFONT.body,
          color: C.textLight,
          textAlign: 'center',
          maxWidth: 700,
        }}>
          {subtitle}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
