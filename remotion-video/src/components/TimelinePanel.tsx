import React from 'react';
import { useCurrentFrame, interpolate, Easing } from 'remotion';
import { COLORS, FONT, RADIUS, SHADOW, SPACING } from '../utils/theme';
import { fadeIn, stagger } from '../utils/animation';

interface TimelineTrack {
  label: string;
  color: string;
  widthPercent: number;
  offsetPercent: number;
}

export const TimelinePanel: React.FC<{
  tracks: TimelineTrack[];
  delay?: number;
  width?: number;
}> = ({ tracks, delay = 0, width = 520 }) => {
  const frame = useCurrentFrame();
  const panelOpacity = fadeIn(frame, delay, 14);

  return (
    <div
      style={{
        opacity: panelOpacity,
        width,
        backgroundColor: COLORS.bgCard,
        borderRadius: RADIUS.lg,
        boxShadow: SHADOW.card,
        border: `1px solid ${COLORS.border}`,
        padding: SPACING.md,
      }}
    >
      <div
        style={{
          fontSize: 12,
          fontFamily: FONT.mono,
          color: COLORS.textMuted,
          marginBottom: SPACING.sm,
        }}
      >
        TIMELINE
      </div>
      {tracks.map((track, i) => {
        const d = delay + 10 + stagger(i, 8);
        const opacity = fadeIn(frame, d, 8);
        const barGrow = interpolate(frame, [d, d + 20], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: Easing.out(Easing.cubic),
        });

        return (
          <div key={i} style={{ opacity, marginBottom: 10 }}>
            <div
              style={{
                fontSize: 11,
                fontFamily: FONT.mono,
                color: COLORS.textMuted,
                marginBottom: 4,
              }}
            >
              {track.label}
            </div>
            <div
              style={{
                height: 20,
                backgroundColor: `${COLORS.border}66`,
                borderRadius: 4,
                position: 'relative',
                overflow: 'hidden',
              }}
            >
              <div
                style={{
                  position: 'absolute',
                  left: `${track.offsetPercent}%`,
                  width: `${track.widthPercent * barGrow}%`,
                  height: '100%',
                  backgroundColor: track.color,
                  borderRadius: 4,
                  opacity: 0.8,
                }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
};
