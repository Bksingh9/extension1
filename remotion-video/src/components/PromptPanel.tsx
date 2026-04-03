import React from 'react';
import { useCurrentFrame, interpolate } from 'remotion';
import { COLORS, FONT, RADIUS, SHADOW, SPACING } from '../utils/theme';
import { fadeIn, slideUp } from '../utils/animation';

export const PromptPanel: React.FC<{
  prompt: string;
  delay?: number;
  width?: number;
}> = ({ prompt, delay = 0, width = 680 }) => {
  const frame = useCurrentFrame();
  const opacity = fadeIn(frame, delay, 14);
  const y = slideUp(frame, delay, 30, 16);
  const charCount = prompt.length;
  const typed = Math.floor(
    interpolate(frame, [delay + 8, delay + 8 + charCount * 0.4], [0, charCount], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    })
  );

  return (
    <div
      style={{
        opacity,
        transform: `translateY(${y}px)`,
        width,
        backgroundColor: COLORS.bgCard,
        borderRadius: RADIUS.lg,
        boxShadow: SHADOW.card,
        border: `1px solid ${COLORS.primary}44`,
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          padding: '10px 16px',
          borderBottom: `1px solid ${COLORS.border}`,
          fontSize: 12,
          fontFamily: FONT.mono,
          color: COLORS.textMuted,
          display: 'flex',
          alignItems: 'center',
          gap: 8,
        }}
      >
        <span style={{ color: COLORS.primary }}>{'>'}</span> prompt
      </div>
      <div
        style={{
          padding: SPACING.md,
          fontSize: 17,
          fontFamily: FONT.mono,
          color: COLORS.textPrimary,
          lineHeight: 1.6,
          minHeight: 50,
        }}
      >
        {prompt.slice(0, typed)}
        <span
          style={{
            display: 'inline-block',
            width: 9,
            height: 20,
            backgroundColor: COLORS.primary,
            marginLeft: 2,
            opacity: Math.sin(frame * 0.3) > 0 ? 1 : 0,
            verticalAlign: 'text-bottom',
          }}
        />
      </div>
    </div>
  );
};
