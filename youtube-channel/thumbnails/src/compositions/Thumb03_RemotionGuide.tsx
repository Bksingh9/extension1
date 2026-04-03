import React from 'react';
import { ThumbnailBase } from '../components/ThumbnailBase';
import { TerminalSnippet } from '../components/TerminalSnippet';
import { COLORS, FONT } from '../theme';

export const Thumb03_RemotionGuide: React.FC = () => (
  <ThumbnailBase glowColor={COLORS.secondary} glowX="50%" glowY="40%">
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        justifyContent: 'center',
        alignItems: 'center',
        gap: 30,
      }}
    >
      <div
        style={{
          fontSize: 22,
          fontFamily: FONT.mono,
          fontWeight: 600,
          color: COLORS.secondary,
          letterSpacing: '0.06em',
        }}
      >
        COMPLETE GUIDE
      </div>
      <div
        style={{
          fontSize: 68,
          fontFamily: FONT.heading,
          fontWeight: 800,
          color: COLORS.textPrimary,
          lineHeight: 1.05,
          letterSpacing: '-0.03em',
          textAlign: 'center',
        }}
      >
        Remotion in
        <br />
        <span style={{ color: COLORS.primary }}>20 Minutes</span>
      </div>
      <div
        style={{
          display: 'flex',
          gap: 12,
        }}
      >
        {['React', 'TypeScript', 'Motion Graphics', '4K Render'].map((tag, i) => (
          <div
            key={i}
            style={{
              padding: '6px 16px',
              backgroundColor: COLORS.card,
              border: `1px solid ${COLORS.border}`,
              borderRadius: 20,
              fontSize: 15,
              fontFamily: FONT.heading,
              fontWeight: 600,
              color: COLORS.textSecondary,
            }}
          >
            {tag}
          </div>
        ))}
      </div>
    </div>
  </ThumbnailBase>
);
