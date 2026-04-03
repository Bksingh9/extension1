import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { COLORS, FONT, RADIUS, SHADOW } from '../utils/theme';
import { fadeIn, scaleIn } from '../utils/animation';

export const RenderSuccessBadge: React.FC<{
  delay?: number;
  label?: string;
}> = ({ delay = 0, label = 'Render Complete' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const opacity = fadeIn(frame, delay, 10);
  const scale = scaleIn(frame, delay, fps);
  const glowPulse = 0.15 + Math.sin((frame - delay) * 0.08) * 0.1;

  return (
    <div
      style={{
        opacity,
        transform: `scale(${scale})`,
        display: 'inline-flex',
        alignItems: 'center',
        gap: 10,
        padding: '14px 28px',
        backgroundColor: `${COLORS.success}18`,
        border: `1px solid ${COLORS.success}55`,
        borderRadius: RADIUS.xl,
        boxShadow: `0 0 ${40 + glowPulse * 100}px ${COLORS.success}${Math.round(glowPulse * 255).toString(16).padStart(2, '0')}`,
      }}
    >
      <div
        style={{
          width: 22,
          height: 22,
          borderRadius: 11,
          backgroundColor: COLORS.success,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 14,
          color: '#fff',
          fontWeight: 700,
        }}
      >
        ✓
      </div>
      <span
        style={{
          fontSize: 18,
          fontFamily: FONT.heading,
          fontWeight: 700,
          color: COLORS.success,
          letterSpacing: '0.02em',
        }}
      >
        {label}
      </span>
    </div>
  );
};
