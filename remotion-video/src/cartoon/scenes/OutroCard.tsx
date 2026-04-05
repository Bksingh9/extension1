import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate, Easing } from 'remotion';
import { CartoonBg } from '../components/CartoonBg';
import { BigCaption } from '../components/BigCaption';
import { C, CFONT } from '../theme';

export const OutroCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pulseScale = 1 + Math.sin(frame * 0.08) * 0.03;

  return (
    <AbsoluteFill>
      <CartoonBg color="#0a0518" />

      <AbsoluteFill
        style={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          gap: 24,
        }}
      >
        <BigCaption
          text="Stay Curious."
          delay={5}
          color={C.textWhite}
          fontSize={68}
        />
        <BigCaption
          text="Stay Skeptical."
          delay={18}
          color={C.glow}
          fontSize={68}
        />

        {/* Subscribe CTA */}
        <div
          style={{
            opacity: interpolate(frame, [40, 55], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            }),
            transform: `scale(${spring({ frame: frame - 40, fps, config: { damping: 10 } }) * pulseScale})`,
            padding: '16px 48px',
            backgroundColor: C.danger,
            borderRadius: 8,
            fontSize: 26,
            fontFamily: CFONT.title,
            color: '#fff',
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            boxShadow: `0 4px 20px ${C.danger}66, 4px 4px 0px rgba(0,0,0,0.3)`,
            marginTop: 12,
          }}
        >
          SUBSCRIBE FOR MORE
        </div>

        {/* Channel badge */}
        <div
          style={{
            opacity: interpolate(frame, [55, 70], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            }),
            display: 'flex',
            alignItems: 'center',
            gap: 10,
            marginTop: 16,
          }}
        >
          <div
            style={{
              width: 36,
              height: 36,
              borderRadius: 18,
              backgroundColor: C.info,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 14,
              fontFamily: CFONT.title,
              fontWeight: 800,
              color: '#fff',
            }}
          >
            AR
          </div>
          <span
            style={{
              fontSize: 18,
              fontFamily: CFONT.title,
              color: C.textLight,
              letterSpacing: '0.04em',
            }}
          >
            AI RENDER LAB
          </span>
        </div>

        {/* Disclaimer */}
        <div
          style={{
            opacity: interpolate(frame, [70, 85], [0, 0.5], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            }),
            fontSize: 12,
            fontFamily: CFONT.caption,
            fontStyle: 'italic',
            color: C.textLight,
            marginTop: 20,
          }}
        >
          For entertainment & educational purposes. Always do your own research.
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
