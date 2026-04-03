import React from 'react';
import { ThumbnailBase } from '../components/ThumbnailBase';
import { COLORS, FONT } from '../theme';

const nodes = [
  { label: 'Idea', color: COLORS.textSecondary, bg: COLORS.card },
  { label: 'Claude Code', color: COLORS.primary, bg: `${COLORS.primary}15` },
  { label: 'Remotion', color: COLORS.secondary, bg: `${COLORS.secondary}15` },
  { label: 'Rendered MP4', color: COLORS.success, bg: `${COLORS.success}15` },
];

export const Thumb05_Workflow: React.FC = () => (
  <ThumbnailBase glowColor="#6366f1" glowX="50%" glowY="60%">
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        justifyContent: 'center',
        alignItems: 'center',
        gap: 36,
      }}
    >
      <div
        style={{
          fontSize: 60,
          fontFamily: FONT.heading,
          fontWeight: 800,
          color: COLORS.textPrimary,
          lineHeight: 1.1,
          letterSpacing: '-0.03em',
          textAlign: 'center',
        }}
      >
        The AI Video
        <br />
        <span style={{ color: COLORS.secondary }}>Pipeline</span>
      </div>

      {/* Flow diagram */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
        {nodes.map((node, i) => (
          <React.Fragment key={i}>
            <div
              style={{
                padding: '14px 24px',
                backgroundColor: node.bg,
                border: `1px solid ${node.color}44`,
                borderRadius: 12,
                fontSize: 18,
                fontFamily: FONT.heading,
                fontWeight: 700,
                color: node.color,
              }}
            >
              {node.label}
            </div>
            {i < nodes.length - 1 && (
              <div style={{ fontSize: 22, color: COLORS.textMuted }}>→</div>
            )}
          </React.Fragment>
        ))}
      </div>

      <div
        style={{
          fontSize: 18,
          fontFamily: FONT.heading,
          color: COLORS.textMuted,
          letterSpacing: '0.04em',
        }}
      >
        Fully automated. Fully local. Fully yours.
      </div>
    </div>
  </ThumbnailBase>
);
