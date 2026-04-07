import React from 'react';
import { useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { C, CFONT, SHADOW, SPRING } from '../theme';
import { fadeIn } from '../animation';

export const BigCaption: React.FC<{
  text: string;
  delay?: number;
  color?: string;
  fontSize?: number;
  sub?: string;
  gradient?: string;
  letterReveal?: boolean;
}> = ({ text, delay = 0, color = C.textWhite, fontSize = 56, sub, gradient, letterReveal = false }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({ frame: frame - delay, fps, config: SPRING.bouncy });
  const opacity = fadeIn(frame, delay, 10);

  const textStyle: React.CSSProperties = {
    fontSize,
    fontFamily: CFONT.display,
    fontWeight: 800,
    letterSpacing: '-0.02em',
    lineHeight: 1.1,
    textAlign: 'center',
    textShadow: `3px 3px 0px ${C.outline}, -1px -1px 0px ${C.outline}, ${SHADOW.text(color)}`,
  };

  if (gradient) {
    Object.assign(textStyle, {
      background: gradient,
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
      backgroundClip: 'text',
    });
  } else {
    textStyle.color = color;
  }

  return (
    <div style={{ opacity, transform: `scale(${scale})`, textAlign: 'center' }}>
      <div style={textStyle}>
        {letterReveal
          ? text.split('').map((ch, i) => (
              <span key={i} style={{ opacity: fadeIn(frame, delay + i * 1.5, 6), display: 'inline-block' }}>
                {ch === ' ' ? '\u00A0' : ch}
              </span>
            ))
          : text}
      </div>
      {sub && (
        <div
          style={{
            opacity: fadeIn(frame, delay + 14, 12),
            fontSize: fontSize * 0.35,
            fontFamily: CFONT.body,
            fontWeight: 400,
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
