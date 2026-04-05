import React from 'react';
import { useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';
import { C, CFONT } from '../theme';

export const SpeechBubble: React.FC<{
  text: string;
  x: number;
  y: number;
  delay?: number;
  tailDirection?: 'left' | 'right' | 'down';
  width?: number;
  variant?: 'speech' | 'thought' | 'shout';
  fontSize?: number;
}> = ({
  text,
  x,
  y,
  delay = 0,
  tailDirection = 'down',
  width = 300,
  variant = 'speech',
  fontSize = 20,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({ frame: frame - delay, fps, config: { damping: 10, stiffness: 140 } });
  const opacity = interpolate(frame, [delay, delay + 8], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const isShout = variant === 'shout';
  const isThought = variant === 'thought';

  const bg = isShout ? C.warning : C.speechBg;
  const border = isShout ? C.danger : C.speechBorder;
  const textColor = C.speechText;
  const borderRadius = isShout ? 8 : 20;
  const borderWidth = isShout ? 4 : 3;

  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        opacity,
        transform: `scale(${scale})`,
        transformOrigin:
          tailDirection === 'left' ? 'left bottom' :
          tailDirection === 'right' ? 'right bottom' : 'center bottom',
      }}
    >
      {/* Bubble */}
      <div
        style={{
          width,
          padding: '14px 18px',
          backgroundColor: bg,
          border: `${borderWidth}px solid ${border}`,
          borderRadius,
          position: 'relative',
          boxShadow: isShout
            ? `0 0 20px ${C.warning}66`
            : '4px 4px 0px rgba(0,0,0,0.2)',
        }}
      >
        <div
          style={{
            fontSize: isShout ? fontSize * 1.2 : fontSize,
            fontFamily: CFONT.body,
            fontWeight: isShout ? 800 : 600,
            color: textColor,
            lineHeight: 1.4,
            textAlign: 'center',
            textTransform: isShout ? 'uppercase' : 'none',
          }}
        >
          {text}
        </div>
      </div>

      {/* Tail */}
      {!isThought && (
        <svg
          width="30"
          height="20"
          style={{
            position: 'absolute',
            bottom: -18,
            left: tailDirection === 'left' ? 30 : tailDirection === 'right' ? width - 60 : width / 2 - 15,
          }}
        >
          <polygon
            points="0,0 15,20 30,0"
            fill={bg}
            stroke={border}
            strokeWidth={borderWidth}
          />
          {/* Cover the top border where tail meets bubble */}
          <rect x="2" y="0" width="26" height="4" fill={bg} />
        </svg>
      )}

      {/* Thought bubbles */}
      {isThought && (
        <>
          <div
            style={{
              position: 'absolute',
              bottom: -14,
              left: width / 2 - 8,
              width: 16,
              height: 12,
              borderRadius: '50%',
              backgroundColor: bg,
              border: `${borderWidth}px solid ${border}`,
            }}
          />
          <div
            style={{
              position: 'absolute',
              bottom: -26,
              left: width / 2,
              width: 10,
              height: 8,
              borderRadius: '50%',
              backgroundColor: bg,
              border: `${borderWidth}px solid ${border}`,
            }}
          />
        </>
      )}
    </div>
  );
};
