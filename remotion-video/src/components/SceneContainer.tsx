import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { COLORS } from '../utils/theme';
import { fadeIn, fadeOut } from '../utils/animation';
import { GridOverlay } from './GridOverlay';
import { BackgroundGlow } from './BackgroundGlow';

export const SceneContainer: React.FC<{
  children: React.ReactNode;
  glowColor?: string;
  glowX?: string;
  glowY?: string;
  fadeDuration?: number;
  totalFrames: number;
}> = ({ children, glowColor, glowX, glowY, fadeDuration = 12, totalFrames }) => {
  const frame = useCurrentFrame();
  const enterOpacity = fadeIn(frame, 0, fadeDuration);
  const exitOpacity = fadeOut(frame, totalFrames - fadeDuration, fadeDuration);
  const opacity = Math.min(enterOpacity, exitOpacity);

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg }}>
      <GridOverlay />
      {glowColor && <BackgroundGlow color={glowColor} x={glowX} y={glowY} />}
      <AbsoluteFill
        style={{
          opacity,
          padding: '60px 80px',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        {children}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
