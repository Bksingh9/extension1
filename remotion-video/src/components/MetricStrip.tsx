import React from 'react';
import { useCurrentFrame } from 'remotion';
import { interpolate, Easing } from 'remotion';
import { COLORS, FONT, SPACING } from '../utils/theme';
import { fadeIn, stagger } from '../utils/animation';

interface Metric {
  label: string;
  value: string;
  color?: string;
}

export const MetricStrip: React.FC<{
  metrics: Metric[];
  delay?: number;
}> = ({ metrics, delay = 0 }) => {
  const frame = useCurrentFrame();

  return (
    <div style={{ display: 'flex', gap: SPACING.lg, justifyContent: 'center' }}>
      {metrics.map((m, i) => {
        const d = delay + stagger(i, 8);
        const opacity = fadeIn(frame, d, 10);
        const barWidth = interpolate(frame, [d + 5, d + 25], [0, 60], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: Easing.out(Easing.cubic),
        });

        return (
          <div key={i} style={{ opacity, textAlign: 'center' }}>
            <div
              style={{
                fontSize: 36,
                fontFamily: FONT.heading,
                fontWeight: 800,
                color: m.color || COLORS.primary,
                letterSpacing: '-0.02em',
              }}
            >
              {m.value}
            </div>
            <div
              style={{
                fontSize: 14,
                fontFamily: FONT.body,
                color: COLORS.textSecondary,
                marginTop: 4,
              }}
            >
              {m.label}
            </div>
            <div
              style={{
                height: 3,
                width: barWidth,
                backgroundColor: m.color || COLORS.primary,
                borderRadius: 2,
                margin: '8px auto 0',
                opacity: 0.6,
              }}
            />
          </div>
        );
      })}
    </div>
  );
};
