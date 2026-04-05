import React from 'react';
import { AbsoluteFill } from 'remotion';
import { COLORS, FONT } from '../utils/theme';
import { GridOverlay } from '../components/GridOverlay';
import { BackgroundGlow } from '../components/BackgroundGlow';

/**
 * Channel Banner: 2560x1440
 * YouTube displays different crops on different devices:
 * - Desktop: full width, ~423px height centered
 * - Mobile: center 1546x423 area
 * - TV: full 2560x1440
 * Safe area for text: center 1546x423
 */
export const ChannelBanner: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg }}>
      <GridOverlay />
      <BackgroundGlow color={COLORS.primaryGlow} x="30%" y="50%" size={700} pulse={false} />
      <BackgroundGlow color={COLORS.secondary} x="75%" y="45%" size={500} pulse={false} />

      {/* Content centered in safe zone */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          padding: '0 200px',
        }}
      >
        <div
          style={{
            display: 'flex',
            width: '100%',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          {/* Left: Logo + Name */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 28 }}>
            <div
              style={{
                width: 90,
                height: 90,
                borderRadius: 45,
                backgroundColor: COLORS.primary,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: `0 0 50px ${COLORS.primary}44`,
              }}
            >
              <span
                style={{
                  fontSize: 38,
                  fontFamily: FONT.heading,
                  fontWeight: 800,
                  color: '#fff',
                  letterSpacing: '-0.02em',
                }}
              >
                AR
              </span>
            </div>
            <div>
              <div
                style={{
                  fontSize: 48,
                  fontFamily: FONT.heading,
                  fontWeight: 800,
                  color: COLORS.textPrimary,
                  letterSpacing: '-0.02em',
                }}
              >
                AI RENDER LAB
              </div>
              <div
                style={{
                  fontSize: 20,
                  fontFamily: FONT.body,
                  color: COLORS.textSecondary,
                  marginTop: 4,
                  letterSpacing: '0.02em',
                }}
              >
                Turn ideas into rendered videos with AI
              </div>
            </div>
          </div>

          {/* Right: Mini terminal */}
          <div
            style={{
              width: 420,
              backgroundColor: '#0d1117',
              borderRadius: 16,
              border: `1px solid ${COLORS.border}`,
              overflow: 'hidden',
              boxShadow: '0 8px 40px rgba(0,0,0,0.4)',
            }}
          >
            <div
              style={{
                display: 'flex',
                gap: 6,
                padding: '10px 14px',
                borderBottom: `1px solid ${COLORS.border}`,
              }}
            >
              <div style={{ width: 10, height: 10, borderRadius: 5, backgroundColor: '#ff5f57' }} />
              <div style={{ width: 10, height: 10, borderRadius: 5, backgroundColor: '#febc2e' }} />
              <div style={{ width: 10, height: 10, borderRadius: 5, backgroundColor: '#28c840' }} />
            </div>
            <div style={{ padding: '14px 18px' }}>
              {[
                { prefix: '$ ', text: 'claude "Create a video"', color: COLORS.textPrimary },
                { prefix: '$ ', text: 'npx remotion render', color: COLORS.textPrimary },
                { prefix: '', text: '✓ Render Complete', color: COLORS.success },
              ].map((line, i) => (
                <div
                  key={i}
                  style={{
                    fontSize: 16,
                    fontFamily: FONT.mono,
                    color: line.color,
                    lineHeight: 1.9,
                  }}
                >
                  {line.prefix && <span style={{ color: COLORS.success }}>{line.prefix}</span>}
                  {line.text}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Bottom accent line */}
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          height: 4,
          background: `linear-gradient(90deg, transparent, ${COLORS.primary}, ${COLORS.secondary}, ${COLORS.success}, transparent)`,
        }}
      />
    </AbsoluteFill>
  );
};
