import React from 'react';
import { ThumbnailBase } from '../components/ThumbnailBase';
import { COLORS, FONT } from '../theme';

const steps = [
  { num: '01', label: 'Describe the idea', status: '✓', color: COLORS.success },
  { num: '02', label: 'Claude generates scenes', status: '✓', color: COLORS.success },
  { num: '03', label: 'Components auto-created', status: '✓', color: COLORS.success },
  { num: '04', label: 'Render the final video', status: '▶', color: COLORS.primary },
];

export const Thumb04_ClaudeCode: React.FC = () => (
  <ThumbnailBase glowColor={COLORS.primaryGlow} glowX="70%" glowY="50%">
    <div style={{ display: 'flex', height: '100%', alignItems: 'center', gap: 50 }}>
      <div style={{ flex: 1 }}>
        <div
          style={{
            fontSize: 22,
            fontFamily: FONT.mono,
            fontWeight: 600,
            color: COLORS.primary,
            letterSpacing: '0.05em',
            marginBottom: 8,
          }}
        >
          CLAUDE CODE
        </div>
        <div
          style={{
            fontSize: 60,
            fontFamily: FONT.heading,
            fontWeight: 800,
            color: COLORS.textPrimary,
            lineHeight: 1.1,
            letterSpacing: '-0.03em',
          }}
        >
          Build Videos
          <br />
          <span style={{ color: COLORS.primary }}>With AI</span>
        </div>
        <div
          style={{
            fontSize: 18,
            fontFamily: FONT.heading,
            color: COLORS.textSecondary,
            marginTop: 14,
          }}
        >
          From prompt to production in minutes
        </div>
      </div>

      {/* Right: Step list */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
        {steps.map((s, i) => (
          <div
            key={i}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 14,
              width: 360,
              padding: '12px 18px',
              backgroundColor: COLORS.card,
              border: `1px solid ${s.color === COLORS.primary ? `${COLORS.primary}44` : COLORS.border}`,
              borderRadius: 10,
            }}
          >
            <div
              style={{
                fontSize: 14,
                fontFamily: FONT.mono,
                color: COLORS.textMuted,
                minWidth: 24,
              }}
            >
              {s.num}
            </div>
            <div
              style={{
                flex: 1,
                fontSize: 17,
                fontFamily: FONT.heading,
                fontWeight: 600,
                color: COLORS.textPrimary,
              }}
            >
              {s.label}
            </div>
            <div
              style={{
                fontSize: 18,
                color: s.color,
                fontWeight: 700,
              }}
            >
              {s.status}
            </div>
          </div>
        ))}
      </div>
    </div>
  </ThumbnailBase>
);
