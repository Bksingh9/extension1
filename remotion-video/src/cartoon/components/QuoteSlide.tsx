import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';
import { CartoonBg } from './CartoonBg';
import { C, CFONT } from '../theme';

export const QuoteSlide: React.FC<{
  quote: string;
  attribution?: string;
  color?: string;
  bgColor?: string;
}> = ({ quote, attribution, color = C.glow, bgColor = '#0a0518' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({ frame: frame - 15, fps, config: { damping: 12 } });
  const fadeIn = interpolate(frame, [0, 15], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ opacity: fadeIn }}>
      <CartoonBg color={bgColor} />
      <AbsoluteFill style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '60px 120px' }}>
        <div style={{ transform: `scale(${scale})`, textAlign: 'center' }}>
          <div style={{ fontSize: 72, color, marginBottom: 20, fontFamily: 'Georgia, serif' }}>"</div>
          <div style={{
            fontSize: 36,
            fontFamily: CFONT.caption,
            fontStyle: 'italic',
            color: C.textWhite,
            lineHeight: 1.5,
            maxWidth: 900,
          }}>
            {quote}
          </div>
          {attribution && (
            <div style={{
              opacity: interpolate(frame, [40, 55], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
              fontSize: 20,
              fontFamily: CFONT.body,
              color,
              marginTop: 24,
            }}>
              — {attribution}
            </div>
          )}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
