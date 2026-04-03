import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { COLORS, FONT, RADIUS, SHADOW, SPACING } from '../utils/theme';
import { fadeIn, slideUp, scaleIn } from '../utils/animation';

export const InfoCard: React.FC<{
  title: string;
  subtitle?: string;
  icon?: string;
  delay?: number;
  accentColor?: string;
  width?: number;
}> = ({ title, subtitle, icon, delay = 0, accentColor = COLORS.primary, width = 260 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const opacity = fadeIn(frame, delay, 12);
  const y = slideUp(frame, delay, 24, 14);
  const scale = scaleIn(frame, delay, fps);

  return (
    <div
      style={{
        opacity,
        transform: `translateY(${y}px) scale(${scale})`,
        width,
        padding: SPACING.md,
        backgroundColor: COLORS.bgCard,
        borderRadius: RADIUS.lg,
        boxShadow: SHADOW.card,
        border: `1px solid ${COLORS.border}`,
        borderTop: `2px solid ${accentColor}`,
      }}
    >
      {icon && (
        <div style={{ fontSize: 28, marginBottom: 10 }}>{icon}</div>
      )}
      <div
        style={{
          fontSize: 18,
          fontFamily: FONT.heading,
          fontWeight: 700,
          color: COLORS.textPrimary,
          marginBottom: 6,
        }}
      >
        {title}
      </div>
      {subtitle && (
        <div
          style={{
            fontSize: 14,
            fontFamily: FONT.body,
            color: COLORS.textSecondary,
            lineHeight: 1.4,
          }}
        >
          {subtitle}
        </div>
      )}
    </div>
  );
};
