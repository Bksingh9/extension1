import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';
import { CartoonBg } from '../components/CartoonBg';
import { BigCaption } from '../components/BigCaption';
import { C, CFONT, SPRING, GRADIENT } from '../theme';
import { fadeIn, glowPulse } from '../animation';

export const OutroCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pulse = glowPulse(frame, 0.97, 1.03, 0.08);

  return (
    <AbsoluteFill>
      <CartoonBg color="#060310" accentColor={C.success} particleColor={C.glow} />
      <AbsoluteFill style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', gap: 24 }}>
        <BigCaption text="Stay Curious." delay={5} color={C.textWhite} fontSize={68} />
        <BigCaption text="Stay Skeptical." delay={18} color={C.glow} fontSize={68} gradient={GRADIENT.goldOrange} />

        <div style={{
          opacity: fadeIn(frame, 40, 12),
          transform: `scale(${spring({ frame: frame - 40, fps, config: SPRING.bouncy }) * pulse})`,
          padding: '14px 44px',
          backgroundColor: C.danger,
          borderRadius: 8,
          fontSize: 24,
          fontFamily: CFONT.display,
          fontWeight: 800,
          color: '#fff',
          letterSpacing: '0.06em',
          textTransform: 'uppercase',
          boxShadow: `0 4px 24px ${C.danger}66`,
          marginTop: 12,
        }}>SUBSCRIBE FOR MORE</div>

        <div style={{
          opacity: fadeIn(frame, 55, 12),
          display: 'flex', alignItems: 'center', gap: 10, marginTop: 16,
        }}>
          <div style={{
            width: 36, height: 36, borderRadius: 18,
            backgroundColor: C.info,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 14, fontFamily: CFONT.display, fontWeight: 800, color: '#fff',
          }}>AR</div>
          <span style={{ fontSize: 16, fontFamily: CFONT.display, fontWeight: 600, color: C.textLight, letterSpacing: '0.04em' }}>
            AI RENDER LAB
          </span>
        </div>

        <div style={{
          opacity: fadeIn(frame, 70, 12) * 0.45,
          fontSize: 11, fontFamily: CFONT.body, fontStyle: 'italic', color: C.textMuted, marginTop: 20,
        }}>For entertainment & educational purposes. Always do your own research.</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
