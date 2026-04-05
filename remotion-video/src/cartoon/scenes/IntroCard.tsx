import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate, Easing } from 'remotion';
import { CartoonBg } from '../components/CartoonBg';
import { BigCaption } from '../components/BigCaption';
import { C, CFONT } from '../theme';

export const IntroCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Dramatic zoom-in line
  const lineW = interpolate(frame, [40, 70], [0, 600], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  // "Episode" tag
  const tagOp = interpolate(frame, [10, 22], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill>
      <CartoonBg color="#0a0518" />
      <AbsoluteFill style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', gap: 16 }}>
        {/* Episode tag */}
        <div
          style={{
            opacity: tagOp,
            padding: '6px 24px',
            backgroundColor: C.danger,
            borderRadius: 4,
            fontSize: 16,
            fontFamily: CFONT.title,
            color: '#fff',
            letterSpacing: '0.12em',
            textTransform: 'uppercase',
          }}
        >
          Geo-Politics Explained
        </div>

        {/* Main title */}
        <BigCaption
          text="Who Really"
          delay={15}
          color={C.textWhite}
          fontSize={72}
        />
        <BigCaption
          text="Runs The World?"
          delay={28}
          color={C.glow}
          fontSize={80}
        />

        {/* Accent line */}
        <div
          style={{
            width: lineW,
            height: 4,
            backgroundColor: C.danger,
            borderRadius: 2,
            marginTop: 8,
          }}
        />

        {/* Subtitle */}
        <div
          style={{
            opacity: interpolate(frame, [60, 75], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            }),
            fontSize: 22,
            fontFamily: CFONT.body,
            color: C.textLight,
            marginTop: 8,
          }}
        >
          Money, power, and the stories they don't tell you...
        </div>

        {/* Disclaimer */}
        <div
          style={{
            opacity: interpolate(frame, [80, 95], [0, 0.6], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            }),
            fontSize: 13,
            fontFamily: CFONT.caption,
            fontStyle: 'italic',
            color: C.textLight,
            marginTop: 24,
          }}
        >
          For entertainment & educational purposes only.
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
