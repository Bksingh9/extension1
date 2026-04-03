import React from 'react';
import { ThumbnailBase } from '../components/ThumbnailBase';
import { COLORS, FONT } from '../theme';

export const Thumb02_StockSim: React.FC = () => (
  <ThumbnailBase glowColor={COLORS.success} glowX="65%" glowY="45%">
    <div style={{ display: 'flex', height: '100%', alignItems: 'center', gap: 40 }}>
      {/* Left: Text */}
      <div style={{ flex: 1 }}>
        <div
          style={{
            fontSize: 24,
            fontFamily: FONT.heading,
            fontWeight: 600,
            color: COLORS.warning,
            letterSpacing: '0.05em',
            marginBottom: 8,
          }}
        >
          AI AGENTS
        </div>
        <div
          style={{
            fontSize: 58,
            fontFamily: FONT.heading,
            fontWeight: 800,
            color: COLORS.textPrimary,
            lineHeight: 1.1,
            letterSpacing: '-0.03em',
          }}
        >
          Simulate
        </div>
        <div
          style={{
            fontSize: 58,
            fontFamily: FONT.heading,
            fontWeight: 800,
            color: COLORS.success,
            lineHeight: 1.1,
            letterSpacing: '-0.03em',
          }}
        >
          The Market
        </div>
        <div
          style={{
            fontSize: 20,
            fontFamily: FONT.heading,
            color: COLORS.textSecondary,
            marginTop: 16,
          }}
        >
          1,000 AI investors. Real behavioral insights.
        </div>
      </div>

      {/* Right: Fake chart / metric cards */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        {[
          { label: 'Retail Sentiment', value: 'Bullish', pct: '+72%', color: COLORS.success },
          { label: 'Institutional', value: 'Accumulating', pct: '+45%', color: COLORS.primary },
          { label: 'Media Narrative', value: 'Mixed', pct: '±12%', color: COLORS.warning },
        ].map((item, i) => (
          <div
            key={i}
            style={{
              width: 340,
              padding: '14px 18px',
              backgroundColor: COLORS.card,
              border: `1px solid ${COLORS.border}`,
              borderLeft: `3px solid ${item.color}`,
              borderRadius: 10,
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <div>
              <div style={{ fontSize: 12, fontFamily: FONT.mono, color: COLORS.textMuted }}>
                {item.label}
              </div>
              <div style={{ fontSize: 18, fontFamily: FONT.heading, fontWeight: 700, color: COLORS.textPrimary, marginTop: 2 }}>
                {item.value}
              </div>
            </div>
            <div style={{ fontSize: 22, fontFamily: FONT.mono, fontWeight: 700, color: item.color }}>
              {item.pct}
            </div>
          </div>
        ))}
      </div>
    </div>
  </ThumbnailBase>
);
