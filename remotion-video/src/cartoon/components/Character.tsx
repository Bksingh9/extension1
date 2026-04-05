import React from 'react';
import { useCurrentFrame, useVideoConfig, spring, interpolate, Easing } from 'remotion';

/**
 * Simple geometric cartoon character
 * Uses shapes to create recognizable figures (no external assets)
 */
export const Character: React.FC<{
  color: string;
  x: number;
  y: number;
  size?: number;
  delay?: number;
  expression?: 'neutral' | 'angry' | 'suspicious' | 'happy' | 'shocked';
  accessory?: 'tie' | 'hat' | 'crown' | 'glasses' | 'none';
  flip?: boolean;
  bobble?: boolean;
}> = ({
  color,
  x,
  y,
  size = 1,
  delay = 0,
  expression = 'neutral',
  accessory = 'none',
  flip = false,
  bobble = true,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame: frame - delay, fps, config: { damping: 12, stiffness: 100 } });
  const bob = bobble ? Math.sin((frame - delay) * 0.06) * 3 : 0;

  // Eye expression
  const eyeHeight =
    expression === 'angry' ? 6 : expression === 'shocked' ? 14 : expression === 'suspicious' ? 4 : 10;
  const eyeY = expression === 'angry' ? -2 : expression === 'suspicious' ? 2 : 0;
  const mouthCurve =
    expression === 'happy' ? 'M-8,4 Q0,12 8,4' :
    expression === 'angry' ? 'M-8,8 Q0,2 8,8' :
    expression === 'shocked' ? '' :
    'M-6,6 L6,6';

  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        transform: `scale(${size * enter}) translateY(${bob}px) scaleX(${flip ? -1 : 1})`,
        transformOrigin: 'center bottom',
      }}
    >
      <svg width="120" height="160" viewBox="-60 -160 120 160">
        {/* Body */}
        <ellipse cx="0" cy="-30" rx="30" ry="40" fill={color} stroke="#1a1a2e" strokeWidth="3" />

        {/* Head */}
        <circle cx="0" cy="-100" r="36" fill={color} stroke="#1a1a2e" strokeWidth="3" />

        {/* Eyes */}
        <ellipse cx="-12" cy={-104 + eyeY} rx="6" ry={eyeHeight / 2} fill="white" stroke="#1a1a2e" strokeWidth="2" />
        <ellipse cx="12" cy={-104 + eyeY} rx="6" ry={eyeHeight / 2} fill="white" stroke="#1a1a2e" strokeWidth="2" />
        <circle cx="-12" cy={-102 + eyeY} r="3" fill="#1a1a2e" />
        <circle cx="12" cy={-102 + eyeY} r="3" fill="#1a1a2e" />

        {/* Angry eyebrows */}
        {expression === 'angry' && (
          <>
            <line x1="-18" y1="-116" x2="-6" y2="-112" stroke="#1a1a2e" strokeWidth="3" strokeLinecap="round" />
            <line x1="6" y1="-112" x2="18" y2="-116" stroke="#1a1a2e" strokeWidth="3" strokeLinecap="round" />
          </>
        )}

        {/* Suspicious squint */}
        {expression === 'suspicious' && (
          <>
            <line x1="-18" y1="-112" x2="-6" y2="-110" stroke="#1a1a2e" strokeWidth="2.5" strokeLinecap="round" />
            <line x1="6" y1="-110" x2="18" y2="-112" stroke="#1a1a2e" strokeWidth="2.5" strokeLinecap="round" />
          </>
        )}

        {/* Mouth */}
        {expression === 'shocked' ? (
          <ellipse cx="0" cy="-82" rx="8" ry="10" fill="#1a1a2e" />
        ) : (
          <path d={mouthCurve} transform="translate(0, -86)" fill="none" stroke="#1a1a2e" strokeWidth="2.5" strokeLinecap="round" />
        )}

        {/* Arms */}
        <line x1="-28" y1="-50" x2="-45" y2="-20" stroke={color} strokeWidth="10" strokeLinecap="round" />
        <line x1="28" y1="-50" x2="45" y2="-20" stroke={color} strokeWidth="10" strokeLinecap="round" />

        {/* Accessories */}
        {accessory === 'tie' && (
          <polygon points="0,-60 -8,-50 0,-25 8,-50" fill="#e74c3c" stroke="#1a1a2e" strokeWidth="2" />
        )}
        {accessory === 'hat' && (
          <g>
            <rect x="-30" y="-136" width="60" height="8" rx="2" fill="#1a1a2e" />
            <rect x="-18" y="-160" width="36" height="26" rx="4" fill="#1a1a2e" />
          </g>
        )}
        {accessory === 'crown' && (
          <g>
            <polygon points="-22,-136 -18,-156 -8,-142 0,-160 8,-142 18,-156 22,-136" fill="#f1c40f" stroke="#e67e22" strokeWidth="2" />
          </g>
        )}
        {accessory === 'glasses' && (
          <g>
            <circle cx="-12" cy="-102" r="10" fill="none" stroke="#1a1a2e" strokeWidth="2.5" />
            <circle cx="12" cy="-102" r="10" fill="none" stroke="#1a1a2e" strokeWidth="2.5" />
            <line x1="-2" y1="-102" x2="2" y2="-102" stroke="#1a1a2e" strokeWidth="2" />
            <line x1="-22" y1="-104" x2="-30" y2="-106" stroke="#1a1a2e" strokeWidth="2" />
            <line x1="22" y1="-104" x2="30" y2="-106" stroke="#1a1a2e" strokeWidth="2" />
          </g>
        )}
      </svg>
    </div>
  );
};
