import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from 'remotion';
import { CartoonBg } from '../components/CartoonBg';
import { BigCaption } from '../components/BigCaption';
import { C, CFONT, GRADIENT } from '../theme';
import { fadeIn } from '../animation';

export const IntroCard: React.FC = () => {
  const frame = useCurrentFrame();
  const lineW = interpolate(frame, [42, 75], [0, 600], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });

  return (
    <AbsoluteFill>
      <CartoonBg color="#060310" accentColor={C.danger} particleColor={C.glow} particleCount={40} />
      <AbsoluteFill style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', gap: 16 }}>
        <div style={{
          opacity: fadeIn(frame, 8, 12),
          padding: '6px 22px',
          backgroundColor: C.danger,
          borderRadius: 4,
          fontSize: 14,
          fontFamily: CFONT.display,
          fontWeight: 700,
          color: '#fff',
          letterSpacing: '0.1em',
          textTransform: 'uppercase',
        }}>Geo-Politics Explained</div>

        <BigCaption text="Who Really" delay={14} color={C.textWhite} fontSize={76} />
        <BigCaption text="Runs The World?" delay={26} color={C.glow} fontSize={84} gradient={GRADIENT.goldOrange} />

        <div style={{ width: lineW, height: 3, background: `linear-gradient(90deg, transparent, ${C.danger}, transparent)`, borderRadius: 2, marginTop: 8 }} />

        <div style={{
          opacity: fadeIn(frame, 60, 15),
          fontSize: 20,
          fontFamily: CFONT.body,
          fontWeight: 400,
          color: C.textLight,
          marginTop: 8,
        }}>Money, power, and the stories they don't tell you...</div>

        <div style={{
          opacity: fadeIn(frame, 80, 15) * 0.5,
          fontSize: 12,
          fontFamily: CFONT.body,
          fontStyle: 'italic',
          color: C.textMuted,
          marginTop: 24,
        }}>For entertainment & educational purposes only.</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
