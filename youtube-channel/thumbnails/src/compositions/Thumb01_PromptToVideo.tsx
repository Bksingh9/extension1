import React from 'react';
import { ThumbnailBase } from '../components/ThumbnailBase';
import { TerminalSnippet } from '../components/TerminalSnippet';
import { COLORS, FONT } from '../theme';

export const Thumb01_PromptToVideo: React.FC = () => (
  <ThumbnailBase glowColor={COLORS.primaryGlow} glowX="30%" glowY="50%">
    <div style={{ display: 'flex', height: '100%', alignItems: 'center', gap: 50 }}>
      {/* Left: Bold text */}
      <div style={{ flex: 1 }}>
        <div
          style={{
            fontSize: 62,
            fontFamily: FONT.heading,
            fontWeight: 800,
            color: COLORS.textPrimary,
            lineHeight: 1.1,
            letterSpacing: '-0.03em',
          }}
        >
          One Prompt.
        </div>
        <div
          style={{
            fontSize: 62,
            fontFamily: FONT.heading,
            fontWeight: 800,
            color: COLORS.primary,
            lineHeight: 1.1,
            letterSpacing: '-0.03em',
            marginTop: 8,
          }}
        >
          One Video.
        </div>
        <div
          style={{
            fontSize: 22,
            fontFamily: FONT.heading,
            fontWeight: 500,
            color: COLORS.textSecondary,
            marginTop: 20,
          }}
        >
          Claude Code + Remotion
        </div>
        {/* Arrow indicator */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 12,
            marginTop: 24,
          }}
        >
          <div
            style={{
              padding: '6px 14px',
              backgroundColor: COLORS.card,
              border: `1px solid ${COLORS.border}`,
              borderRadius: 8,
              fontSize: 14,
              fontFamily: FONT.mono,
              color: COLORS.textMuted,
            }}
          >
            prompt.txt
          </div>
          <span style={{ fontSize: 24, color: COLORS.primary }}>→</span>
          <div
            style={{
              padding: '6px 14px',
              backgroundColor: `${COLORS.success}18`,
              border: `1px solid ${COLORS.success}44`,
              borderRadius: 8,
              fontSize: 14,
              fontFamily: FONT.mono,
              color: COLORS.success,
            }}
          >
            final.mp4
          </div>
        </div>
      </div>

      {/* Right: Terminal */}
      <TerminalSnippet
        lines={[
          'claude "Create a 30s video"',
          'npx remotion render',
          '✓ Rendered 945 frames',
          '✓ out/final.mp4 — 3.7MB',
        ]}
        width={400}
      />
    </div>
  </ThumbnailBase>
);
