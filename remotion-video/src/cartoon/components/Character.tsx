import React from 'react';
import { useCurrentFrame, useVideoConfig, spring } from 'remotion';
import { SPRING } from '../theme';
import { breathe, noiseWobble } from '../animation';

/**
 * Production-grade cartoon character
 * SVG with gradients, shadows, detailed faces, clothing, and idle animations
 */
export const Character: React.FC<{
  color: string;
  colorLight?: string;
  x: number;
  y: number;
  size?: number;
  delay?: number;
  expression?: 'neutral' | 'angry' | 'suspicious' | 'happy' | 'shocked' | 'thoughtful' | 'smug';
  accessory?: 'tie' | 'hat' | 'crown' | 'glasses' | 'none' | 'keffiyeh' | 'collar';
  flip?: boolean;
  label?: string;
}> = ({
  color,
  colorLight,
  x, y,
  size = 1,
  delay = 0,
  expression = 'neutral',
  accessory = 'none',
  flip = false,
  label,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ frame: frame - delay, fps, config: SPRING.bouncy });
  const cLight = colorLight || `${color}88`;
  const id = `char-${x}-${y}`;

  // Idle animations
  const b = breathe(frame, 0.015, 0.035);
  const armSwayL = noiseWobble(frame, `${id}-armL`, 4, 0.05);
  const armSwayR = noiseWobble(frame, `${id}-armR`, 4, 0.05);
  const eyeBlink = Math.sin(frame * 0.12 + delay) > 0.97 ? 0.15 : 1;

  // Eyes
  const eyeH = expression === 'angry' ? 5 : expression === 'shocked' ? 14 : expression === 'suspicious' ? 4 : expression === 'smug' ? 6 : 9;
  const eyeY = expression === 'angry' ? -1 : expression === 'suspicious' ? 2 : 0;
  const browAngle = expression === 'angry' ? 8 : expression === 'suspicious' ? 4 : expression === 'thoughtful' ? -4 : 0;

  // Mouth
  const mouth =
    expression === 'happy' ? 'M-9,4 Q0,14 9,4' :
    expression === 'angry' ? 'M-9,9 Q0,2 9,9' :
    expression === 'smug' ? 'M-6,6 Q4,11 9,4' :
    expression === 'thoughtful' ? 'M-4,7 Q0,4 4,7' :
    'M-7,7 L7,7';

  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        transform: `scale(${size * enter}) scaleX(${flip ? -1 : 1})`,
        transformOrigin: 'center bottom',
      }}
    >
      <svg width="180" height="240" viewBox="-90 -240 180 240" overflow="visible">
        <defs>
          {/* Body gradient */}
          <linearGradient id={`${id}-bodyG`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={cLight} />
            <stop offset="100%" stopColor={color} />
          </linearGradient>
          {/* Head gradient */}
          <radialGradient id={`${id}-headG`} cx="0.4" cy="0.3">
            <stop offset="0%" stopColor={cLight} />
            <stop offset="80%" stopColor={color} />
          </radialGradient>
          {/* Shadow */}
          <radialGradient id={`${id}-shadow`} cx="0.5" cy="0.5">
            <stop offset="0%" stopColor="rgba(0,0,0,0.35)" />
            <stop offset="100%" stopColor="transparent" />
          </radialGradient>
        </defs>

        {/* Drop shadow */}
        <ellipse cx="0" cy="-2" rx="32" ry="8" fill={`url(#${id}-shadow)`} />

        {/* Body with breathing */}
        <g transform={`scale(1, ${b})`} style={{ transformOrigin: '0 0' }}>
          {/* Body */}
          <ellipse cx="0" cy="-38" rx="32" ry="44" fill={`url(#${id}-bodyG)`} stroke={color} strokeWidth="2.5" />

          {/* Shirt collar / neckline */}
          <path d="M-12,-72 L0,-64 L12,-72" fill="none" stroke={color} strokeWidth="2" opacity="0.5" />
        </g>

        {/* Head */}
        <circle cx="0" cy="-110" r="40" fill={`url(#${id}-headG)`} stroke={color} strokeWidth="2.5" />

        {/* Head highlight (3D feel) */}
        <ellipse cx="-10" cy="-120" rx="16" ry="12" fill="rgba(255,255,255,0.08)" />

        {/* Ears */}
        <ellipse cx="-38" cy="-110" rx="8" ry="10" fill={color} stroke={color} strokeWidth="2" />
        <ellipse cx="38" cy="-110" rx="8" ry="10" fill={color} stroke={color} strokeWidth="2" />

        {/* Eyebrows */}
        <line x1="-22" y1={-128 - browAngle} x2="-6" y2={-126 + browAngle * 0.5}
          stroke="#1e293b" strokeWidth="3" strokeLinecap="round" />
        <line x1="6" y1={-126 + browAngle * 0.5} x2="22" y2={-128 - browAngle}
          stroke="#1e293b" strokeWidth="3" strokeLinecap="round" />

        {/* Eyes with blink */}
        <g transform={`scale(1, ${eyeBlink})`} style={{ transformOrigin: '0 -110px' }}>
          {/* Eye whites */}
          <ellipse cx="-14" cy={-112 + eyeY} rx="8" ry={eyeH / 2 + 2} fill="white" stroke="#1e293b" strokeWidth="1.5" />
          <ellipse cx="14" cy={-112 + eyeY} rx="8" ry={eyeH / 2 + 2} fill="white" stroke="#1e293b" strokeWidth="1.5" />
          {/* Pupils */}
          <circle cx="-14" cy={-110 + eyeY} r="3.5" fill="#1e293b" />
          <circle cx="14" cy={-110 + eyeY} r="3.5" fill="#1e293b" />
          {/* Eye highlights */}
          <circle cx="-12" cy={-112 + eyeY} r="1.5" fill="white" />
          <circle cx="16" cy={-112 + eyeY} r="1.5" fill="white" />
        </g>

        {/* Nose */}
        <ellipse cx="0" cy="-100" rx="3" ry="2.5" fill={color} opacity="0.6" />

        {/* Mouth */}
        {expression === 'shocked' ? (
          <ellipse cx="0" cy="-88" rx="8" ry="10" fill="#1e293b" />
        ) : (
          <path d={mouth} transform="translate(0, -92)" fill="none" stroke="#1e293b" strokeWidth="2.5" strokeLinecap="round" />
        )}

        {/* Arms with sway */}
        <line x1="-30" y1="-55" x2={-50 + armSwayL} y2="-22"
          stroke={color} strokeWidth="12" strokeLinecap="round" />
        <line x1="30" y1="-55" x2={50 + armSwayR} y2="-22"
          stroke={color} strokeWidth="12" strokeLinecap="round" />
        {/* Hands (round mitts) */}
        <circle cx={-50 + armSwayL} cy="-18" r="8" fill={cLight} stroke={color} strokeWidth="2" />
        <circle cx={50 + armSwayR} cy="-18" r="8" fill={cLight} stroke={color} strokeWidth="2" />

        {/* ── Accessories ── */}
        {accessory === 'tie' && (
          <g>
            <polygon points="0,-70 -7,-60 0,-30 7,-60" fill="#ef4444" stroke="#b91c1c" strokeWidth="1.5" />
            <circle cx="0" cy="-62" r="3" fill="#b91c1c" />
          </g>
        )}
        {accessory === 'hat' && (
          <g>
            <rect x="-34" y="-150" width="68" height="8" rx="3" fill="#1e293b" />
            <rect x="-20" y="-178" width="40" height="30" rx="6" fill="#1e293b" />
            <rect x="-18" y="-175" width="36" height="6" rx="2" fill="#334155" opacity="0.4" />
          </g>
        )}
        {accessory === 'crown' && (
          <g>
            <polygon points="-24,-150 -20,-172 -10,-156 0,-176 10,-156 20,-172 24,-150"
              fill="#eab308" stroke="#ca8a04" strokeWidth="2" />
            <circle cx="-10" cy="-155" r="2.5" fill="#ef4444" />
            <circle cx="0" cy="-165" r="2.5" fill="#3b82f6" />
            <circle cx="10" cy="-155" r="2.5" fill="#22c55e" />
          </g>
        )}
        {accessory === 'glasses' && (
          <g>
            <rect x="-24" y={-120 + eyeY} width="18" height="14" rx="4" fill="none" stroke="#1e293b" strokeWidth="2.5" />
            <rect x="6" y={-120 + eyeY} width="18" height="14" rx="4" fill="none" stroke="#1e293b" strokeWidth="2.5" />
            <line x1="-6" y1={-113 + eyeY} x2="6" y2={-113 + eyeY} stroke="#1e293b" strokeWidth="2" />
            <line x1="-24" y1={-115 + eyeY} x2="-34" y2={-118 + eyeY} stroke="#1e293b" strokeWidth="2" />
            <line x1="24" y1={-115 + eyeY} x2="34" y2={-118 + eyeY} stroke="#1e293b" strokeWidth="2" />
            {/* Lens glare */}
            <rect x="-20" y={-118 + eyeY} width="5" height="3" rx="1" fill="rgba(255,255,255,0.15)" />
            <rect x="10" y={-118 + eyeY} width="5" height="3" rx="1" fill="rgba(255,255,255,0.15)" />
          </g>
        )}
        {accessory === 'keffiyeh' && (
          <g>
            <path d="M-36,-130 Q-38,-155 -25,-160 L25,-160 Q38,-155 36,-130" fill="#f8fafc" stroke="#cbd5e1" strokeWidth="1.5" />
            <line x1="-20" y1="-155" x2="-20" y2="-135" stroke="#ef4444" strokeWidth="1" opacity="0.6" />
            <line x1="0" y1="-158" x2="0" y2="-135" stroke="#ef4444" strokeWidth="1" opacity="0.6" />
            <line x1="20" y1="-155" x2="20" y2="-135" stroke="#ef4444" strokeWidth="1" opacity="0.6" />
          </g>
        )}
        {accessory === 'collar' && (
          <g>
            <path d="M-20,-75 L-15,-68 L0,-72 L15,-68 L20,-75" fill={color} stroke={color} strokeWidth="2" />
            <circle cx="0" cy="-72" r="2" fill="#eab308" />
          </g>
        )}
      </svg>

      {/* Label below character */}
      {label && (
        <div
          style={{
            textAlign: 'center',
            fontSize: 14,
            fontWeight: 700,
            color: color,
            letterSpacing: '0.06em',
            marginTop: 4,
            textShadow: `0 1px 4px rgba(0,0,0,0.5)`,
            transform: flip ? 'scaleX(-1)' : 'none',
          }}
        >
          {label}
        </div>
      )}
    </div>
  );
};
