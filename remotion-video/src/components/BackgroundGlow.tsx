import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { COLORS } from '../utils/theme';

export const BackgroundGlow: React.FC<{
  color?: string;
  x?: string;
  y?: string;
  size?: number;
  pulse?: boolean;
}> = ({ color = COLORS.primaryGlow, x = '50%', y = '50%', size = 600, pulse = true }) => {
  const frame = useCurrentFrame();
  const scale = pulse ? 1 + Math.sin(frame * 0.03) * 0.08 : 1;

  return (
    <AbsoluteFill>
      <div
        style={{
          position: 'absolute',
          left: x,
          top: y,
          width: size,
          height: size,
          transform: `translate(-50%, -50%) scale(${scale})`,
          borderRadius: '50%',
          background: `radial-gradient(circle, ${color}22 0%, transparent 70%)`,
          filter: 'blur(40px)',
          pointerEvents: 'none',
        }}
      />
    </AbsoluteFill>
  );
};
