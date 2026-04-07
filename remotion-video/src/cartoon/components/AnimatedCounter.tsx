import React from 'react';
import { useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { C, CFONT, SPRING } from '../theme';
import { countUp, fadeIn } from '../animation';

export const AnimatedCounter: React.FC<{
  value: number;
  prefix?: string;
  suffix?: string;
  delay?: number;
  duration?: number;
  color?: string;
  fontSize?: number;
  label?: string;
}> = ({ value, prefix = '', suffix = '', delay = 0, duration = 30, color = C.glow, fontSize = 48, label }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const opacity = fadeIn(frame, delay, 10);
  const scale = spring({ frame: frame - delay, fps, config: SPRING.snappy });
  const current = countUp(frame, delay + 5, duration, value);

  // Format with commas
  const formatted = current.toLocaleString();

  return (
    <div style={{ opacity, transform: `scale(${scale})`, textAlign: 'center' }}>
      <div
        style={{
          fontSize,
          fontFamily: CFONT.display,
          fontWeight: 800,
          color,
          letterSpacing: '-0.03em',
          textShadow: `0 0 20px ${color}44`,
        }}
      >
        {prefix}{formatted}{suffix}
      </div>
      {label && (
        <div
          style={{
            fontSize: fontSize * 0.28,
            fontFamily: CFONT.body,
            color: C.textMuted,
            marginTop: 6,
            letterSpacing: '0.02em',
          }}
        >
          {label}
        </div>
      )}
    </div>
  );
};
