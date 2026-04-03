import React from 'react';
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Easing,
} from 'remotion';
import { COLORS, FONT, RADIUS, SHADOW } from '../utils/theme';
import { GridOverlay } from '../components/GridOverlay';
import { BackgroundGlow } from '../components/BackgroundGlow';

export const OutroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Fade in
  const fadeIn = interpolate(frame, [0, 15], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Subscribe button entrance
  const btnScale = spring({ frame: frame - 20, fps, config: { damping: 10, stiffness: 120 } });
  const btnOpacity = interpolate(frame, [20, 32], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Next video card
  const cardOpacity = interpolate(frame, [40, 55], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const cardX = interpolate(frame, [40, 58], [40, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  // Channel info
  const infoOpacity = interpolate(frame, [60, 75], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Subtle pulse on subscribe button
  const pulse = 1 + Math.sin(frame * 0.08) * 0.02;

  // Final fade
  const fadeOut = interpolate(frame, [220, 238], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg }}>
      <GridOverlay />
      <BackgroundGlow color={COLORS.primaryGlow} x="30%" y="50%" size={500} />
      <BackgroundGlow color={COLORS.success} x="75%" y="60%" size={300} pulse={false} />
      <AbsoluteFill
        style={{
          opacity: fadeIn * fadeOut,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          padding: '60px 100px',
        }}
      >
        <div
          style={{
            display: 'flex',
            width: '100%',
            gap: 60,
            alignItems: 'center',
          }}
        >
          {/* Left side: CTA */}
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 24 }}>
            {/* Logo + name */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
              <div
                style={{
                  width: 52,
                  height: 52,
                  borderRadius: 26,
                  backgroundColor: COLORS.primary,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <span
                  style={{
                    fontSize: 20,
                    fontFamily: FONT.heading,
                    fontWeight: 800,
                    color: '#fff',
                  }}
                >
                  AR
                </span>
              </div>
              <div>
                <div
                  style={{
                    fontSize: 24,
                    fontFamily: FONT.heading,
                    fontWeight: 700,
                    color: COLORS.textPrimary,
                  }}
                >
                  AI Render Lab
                </div>
                <div
                  style={{
                    fontSize: 14,
                    fontFamily: FONT.body,
                    color: COLORS.textSecondary,
                  }}
                >
                  AI-powered video creation
                </div>
              </div>
            </div>

            {/* Thanks message */}
            <div
              style={{
                fontSize: 38,
                fontFamily: FONT.heading,
                fontWeight: 800,
                color: COLORS.textPrimary,
                lineHeight: 1.2,
                letterSpacing: '-0.02em',
              }}
            >
              Thanks for
              <br />
              watching.
            </div>

            {/* Subscribe button */}
            <div
              style={{
                opacity: btnOpacity,
                transform: `scale(${btnScale * pulse})`,
                alignSelf: 'flex-start',
              }}
            >
              <div
                style={{
                  padding: '14px 36px',
                  backgroundColor: COLORS.danger,
                  borderRadius: RADIUS.xl,
                  fontSize: 18,
                  fontFamily: FONT.heading,
                  fontWeight: 700,
                  color: '#fff',
                  letterSpacing: '0.03em',
                  boxShadow: '0 4px 20px rgba(239,68,68,0.3)',
                }}
              >
                SUBSCRIBE
              </div>
            </div>

            {/* Social links */}
            <div
              style={{
                opacity: infoOpacity,
                display: 'flex',
                gap: 20,
              }}
            >
              {['GitHub', 'Twitter/X'].map((platform) => (
                <div
                  key={platform}
                  style={{
                    fontSize: 14,
                    fontFamily: FONT.mono,
                    color: COLORS.textMuted,
                  }}
                >
                  @bksingh9 / {platform}
                </div>
              ))}
            </div>
          </div>

          {/* Right side: Next video card */}
          <div
            style={{
              opacity: cardOpacity,
              transform: `translateX(${cardX}px)`,
              width: 480,
              backgroundColor: COLORS.bgCard,
              borderRadius: RADIUS.lg,
              boxShadow: SHADOW.card,
              border: `1px solid ${COLORS.border}`,
              overflow: 'hidden',
            }}
          >
            {/* Fake video preview */}
            <div
              style={{
                height: 240,
                backgroundColor: '#0d1117',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                position: 'relative',
              }}
            >
              {/* Play button */}
              <div
                style={{
                  width: 60,
                  height: 60,
                  borderRadius: 30,
                  backgroundColor: 'rgba(255,255,255,0.15)',
                  border: '2px solid rgba(255,255,255,0.3)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <div
                  style={{
                    width: 0,
                    height: 0,
                    borderTop: '12px solid transparent',
                    borderBottom: '12px solid transparent',
                    borderLeft: '20px solid rgba(255,255,255,0.8)',
                    marginLeft: 4,
                  }}
                />
              </div>
              <div
                style={{
                  position: 'absolute',
                  top: 12,
                  left: 12,
                  fontSize: 11,
                  fontFamily: FONT.mono,
                  color: COLORS.textMuted,
                  padding: '4px 8px',
                  backgroundColor: 'rgba(0,0,0,0.6)',
                  borderRadius: 4,
                }}
              >
                UP NEXT
              </div>
            </div>
            <div style={{ padding: '16px 20px' }}>
              <div
                style={{
                  fontSize: 17,
                  fontFamily: FONT.heading,
                  fontWeight: 700,
                  color: COLORS.textPrimary,
                  lineHeight: 1.3,
                }}
              >
                Next: More AI-Powered Builds
              </div>
              <div
                style={{
                  fontSize: 13,
                  fontFamily: FONT.body,
                  color: COLORS.textMuted,
                  marginTop: 6,
                }}
              >
                AI Render Lab • New videos weekly
              </div>
            </div>
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
