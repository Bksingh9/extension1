import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring, Easing } from 'remotion';
import { COLORS, FONT } from '../utils/theme';
import { GridOverlay } from '../components/GridOverlay';
import { BackgroundGlow } from '../components/BackgroundGlow';

export const IntroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Logo monogram entrance
  const logoScale = spring({ frame: frame - 10, fps, config: { damping: 12, stiffness: 100 } });
  const logoOpacity = interpolate(frame, [10, 22], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Text entrance
  const textOpacity = interpolate(frame, [35, 50], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const textY = interpolate(frame, [35, 52], [16, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  // Accent line
  const lineWidth = interpolate(frame, [55, 80], [0, 120], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  // Tagline
  const tagOpacity = interpolate(frame, [70, 85], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Final fade out
  const fadeOut = interpolate(frame, [130, 148], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg }}>
      <GridOverlay />
      <BackgroundGlow color={COLORS.primaryGlow} x="50%" y="50%" size={500} />
      <AbsoluteFill
        style={{
          opacity: fadeOut,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: 16,
          }}
        >
          {/* Logo circle */}
          <div
            style={{
              opacity: logoOpacity,
              transform: `scale(${logoScale})`,
              width: 80,
              height: 80,
              borderRadius: 40,
              backgroundColor: COLORS.primary,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: `0 0 40px ${COLORS.primary}44`,
            }}
          >
            <span
              style={{
                fontSize: 32,
                fontFamily: FONT.heading,
                fontWeight: 800,
                color: '#fff',
                letterSpacing: '-0.02em',
              }}
            >
              AR
            </span>
          </div>

          {/* Channel name */}
          <div
            style={{
              opacity: textOpacity,
              transform: `translateY(${textY}px)`,
              fontSize: 42,
              fontFamily: FONT.heading,
              fontWeight: 800,
              color: COLORS.textPrimary,
              letterSpacing: '-0.02em',
            }}
          >
            AI RENDER LAB
          </div>

          {/* Accent line */}
          <div
            style={{
              width: lineWidth,
              height: 3,
              backgroundColor: COLORS.primary,
              borderRadius: 2,
            }}
          />

          {/* Tagline */}
          <div
            style={{
              opacity: tagOpacity,
              fontSize: 16,
              fontFamily: FONT.body,
              color: COLORS.textSecondary,
              letterSpacing: '0.08em',
            }}
          >
            TURN IDEAS INTO RENDERED VIDEOS WITH AI
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
