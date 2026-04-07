import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate, Easing } from 'remotion';
import { CartoonBg } from './CartoonBg';
import { C, CFONT, GRADIENT, SHADOW, SPRING } from '../theme';
import { fadeIn } from '../animation';

export const ChapterTitle: React.FC<{
  chapter: number;
  title: string;
  subtitle: string;
  color: string;
  icon: string;
}> = ({ chapter, title, subtitle, color, icon }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({ frame: frame - 12, fps, config: SPRING.dramatic });
  const iconScale = spring({ frame: frame - 8, fps, config: SPRING.bouncy });
  const lineW = interpolate(frame, [30, 65], [0, 500], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });
  const fadeOut = interpolate(frame, [140, 160], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ opacity: fadeOut }}>
      <CartoonBg color="#070412" accentColor={color} particleColor={color} particleCount={30} />
      <AbsoluteFill style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', gap: 16 }}>
        <div style={{
          opacity: fadeIn(frame, 3, 12),
          fontSize: 13,
          fontFamily: CFONT.mono,
          color: C.textMuted,
          letterSpacing: '0.2em',
          fontWeight: 500,
        }}>
          CHAPTER {chapter}
        </div>
        <div style={{ fontSize: 64, transform: `scale(${iconScale})`, filter: `drop-shadow(0 0 20px ${color}44)` }}>
          {icon}
        </div>
        <div style={{
          transform: `scale(${scale})`,
          fontSize: 68,
          fontFamily: CFONT.display,
          fontWeight: 800,
          color,
          letterSpacing: '-0.02em',
          textTransform: 'uppercase',
          textShadow: `3px 3px 0 ${C.outline}, ${SHADOW.text(color)}`,
          textAlign: 'center',
          lineHeight: 1.1,
        }}>
          {title}
        </div>
        <div style={{ width: lineW, height: 3, background: `linear-gradient(90deg, transparent, ${color}, transparent)`, borderRadius: 2 }} />
        <div style={{
          opacity: fadeIn(frame, 42, 15),
          fontSize: 20,
          fontFamily: CFONT.body,
          color: C.textLight,
          textAlign: 'center',
          maxWidth: 700,
          fontWeight: 400,
        }}>
          {subtitle}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
