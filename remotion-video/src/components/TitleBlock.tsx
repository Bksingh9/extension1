import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { COLORS, FONT } from '../utils/theme';
import { fadeIn, slideUp, scaleIn } from '../utils/animation';

export const TitleBlock: React.FC<{
  text: string;
  delay?: number;
  fontSize?: number;
  color?: string;
  useSpring?: boolean;
}> = ({ text, delay = 0, fontSize = 72, color = COLORS.textPrimary, useSpring = false }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const opacity = fadeIn(frame, delay, 14);
  const y = slideUp(frame, delay, 30, 16);
  const scale = useSpring ? scaleIn(frame, delay, fps) : 1;

  return (
    <div
      style={{
        opacity,
        transform: `translateY(${y}px) scale(${scale})`,
        fontSize,
        fontFamily: FONT.heading,
        fontWeight: 800,
        color,
        letterSpacing: '-0.03em',
        lineHeight: 1.1,
        textAlign: 'center',
      }}
    >
      {text}
    </div>
  );
};
