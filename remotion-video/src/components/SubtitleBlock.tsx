import React from 'react';
import { useCurrentFrame } from 'remotion';
import { COLORS, FONT } from '../utils/theme';
import { fadeIn, slideUp } from '../utils/animation';

export const SubtitleBlock: React.FC<{
  text: string;
  delay?: number;
  fontSize?: number;
}> = ({ text, delay = 10, fontSize = 28 }) => {
  const frame = useCurrentFrame();
  const opacity = fadeIn(frame, delay, 16);
  const y = slideUp(frame, delay, 20, 18);

  return (
    <div
      style={{
        opacity,
        transform: `translateY(${y}px)`,
        fontSize,
        fontFamily: FONT.body,
        fontWeight: 400,
        color: COLORS.textSecondary,
        letterSpacing: '0.01em',
        lineHeight: 1.5,
        textAlign: 'center',
        maxWidth: 800,
      }}
    >
      {text}
    </div>
  );
};
