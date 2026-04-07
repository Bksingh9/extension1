import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { CartoonBg } from './CartoonBg';
import { C, CFONT, SHADOW, SPRING, GRADIENT } from '../theme';
import { fadeIn } from '../animation';

export const QuoteSlide: React.FC<{
  quote: string;
  attribution?: string;
  color?: string;
  bgColor?: string;
}> = ({ quote, attribution, color = C.glow, bgColor = '#070412' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({ frame: frame - 15, fps, config: SPRING.dramatic });

  return (
    <AbsoluteFill>
      <CartoonBg color={bgColor} accentColor={color} particleColor={color} particleCount={25} />
      <AbsoluteFill style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '60px 140px' }}>
        <div style={{ transform: `scale(${scale})`, textAlign: 'center' }}>
          <div style={{ fontSize: 72, color: `${color}88`, fontFamily: CFONT.display, marginBottom: 16 }}>"</div>
          <div style={{
            fontSize: 34,
            fontFamily: CFONT.body,
            fontStyle: 'italic',
            fontWeight: 500,
            color: C.textWhite,
            lineHeight: 1.6,
            maxWidth: 850,
            textShadow: '0 2px 8px rgba(0,0,0,0.4)',
          }}>
            {quote}
          </div>
          {attribution && (
            <div style={{
              opacity: fadeIn(frame, 40, 15),
              fontSize: 18,
              fontFamily: CFONT.body,
              fontWeight: 600,
              color,
              marginTop: 28,
              letterSpacing: '0.02em',
            }}>
              — {attribution}
            </div>
          )}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
