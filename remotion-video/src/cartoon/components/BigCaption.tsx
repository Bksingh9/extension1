import React from 'react';
import { useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';
import { C, CFONT } from '../theme';

export const BigCaption: React.FC<{
  text: string;
  delay?: number;
  color?: string;
  fontSize?: number;
  sub?: string;
}> = ({ text, delay = 0, color = C.textWhite, fontSize = 56, sub }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({ frame: frame - delay, fps, config: { damping: 11, stiffness: 130, mass: 0.8 } });
  const opacity = interpolate(frame, [delay, delay + 10], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div style={{ opacity, transform: `scale(${scale})`, textAlign: 'center' }}>
      <div
        style={{
          fontSize,
          fontFamily: CFONT.title,
          fontWeight: 900,
          color,
          letterSpacing: '0.04em',
          textTransform: 'uppercase',
          textShadow: `3px 3px 0px ${C.outline}, -1px -1px 0px ${C.outline}, 0 0 20px ${color}44`,
          lineHeight: 1.1,
        }}
      >
        {text}
      </div>
      {sub && (
        <div
          style={{
            opacity: interpolate(frame, [delay + 12, delay + 24], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            }),
            fontSize: fontSize * 0.38,
            fontFamily: CFONT.body,
            color: C.textLight,
            marginTop: 12,
          }}
        >
          {sub}
        </div>
      )}
    </div>
  );
};
