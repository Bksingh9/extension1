import React from 'react';
import { useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { C, CFONT, SPRING, RAD, SHADOW } from '../theme';
import { fadeIn, typewriter as tw, wobbleRotate } from '../animation';

export const SpeechBubble: React.FC<{
  text: string;
  x: number;
  y: number;
  delay?: number;
  tailDirection?: 'left' | 'right' | 'down';
  width?: number;
  variant?: 'speech' | 'thought' | 'shout';
  fontSize?: number;
  typeEffect?: boolean;
}> = ({
  text, x, y, delay = 0, tailDirection = 'down', width = 300,
  variant = 'speech', fontSize = 18, typeEffect = false,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  // Squash/stretch entrance
  const scaleRaw = spring({ frame: frame - delay, fps, config: SPRING.bouncy });
  const wobble = wobbleRotate(frame, 0.5, 0.06);
  const opacity = fadeIn(frame, delay, 8);

  const isShout = variant === 'shout';
  const isThought = variant === 'thought';
  const bg = isShout ? '#fef3c7' : C.speechBg;
  const border = isShout ? C.danger : C.speechBorder;
  const textColor = C.speechText;
  const borderW = isShout ? 3 : 2.5;
  const rad = isShout ? RAD.md : RAD.xl;

  const displayText = typeEffect ? tw(text, frame, delay + 8, 0.6) : text;

  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        opacity,
        transform: `scale(${scaleRaw}) rotate(${wobble}deg)`,
        transformOrigin:
          tailDirection === 'left' ? 'left bottom' :
          tailDirection === 'right' ? 'right bottom' : 'center bottom',
      }}
    >
      <div style={{
        width,
        padding: '12px 18px',
        backgroundColor: bg,
        border: `${borderW}px solid ${border}`,
        borderRadius: rad,
        boxShadow: isShout
          ? `0 0 24px ${C.warning}44, ${SHADOW.card}`
          : `0 6px 20px rgba(0,0,0,0.35), 0 0 0 1px rgba(255,255,255,0.05)`,
        position: 'relative',
      }}>
        <div style={{
          fontSize: isShout ? fontSize * 1.15 : fontSize,
          fontFamily: CFONT.body,
          fontWeight: isShout ? 800 : 600,
          color: textColor,
          lineHeight: 1.4,
          textAlign: 'center',
          textTransform: isShout ? 'uppercase' : 'none',
        }}>
          {displayText}
        </div>
      </div>
      {/* Tail */}
      {!isThought && (
        <svg width="28" height="18" style={{
          position: 'absolute',
          bottom: -16,
          left: tailDirection === 'left' ? 28 : tailDirection === 'right' ? width - 56 : width / 2 - 14,
        }}>
          <polygon points="0,0 14,18 28,0" fill={bg} stroke={border} strokeWidth={borderW} />
          <rect x="2" y="0" width="24" height="4" fill={bg} />
        </svg>
      )}
      {isThought && (
        <>
          <div style={{ position: 'absolute', bottom: -12, left: width / 2 - 6, width: 12, height: 10, borderRadius: '50%', backgroundColor: bg, border: `${borderW}px solid ${border}` }} />
          <div style={{ position: 'absolute', bottom: -22, left: width / 2 + 2, width: 8, height: 6, borderRadius: '50%', backgroundColor: bg, border: `${borderW}px solid ${border}` }} />
        </>
      )}
    </div>
  );
};
