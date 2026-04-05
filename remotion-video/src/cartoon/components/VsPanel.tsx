import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate, Easing } from 'remotion';
import { CartoonBg } from './CartoonBg';
import { Character } from './Character';
import { SpeechBubble } from './SpeechBubble';
import { C, CFONT } from '../theme';

interface Side {
  name: string;
  color: string;
  points: string[];
  expression: 'angry' | 'suspicious' | 'neutral' | 'happy' | 'shocked';
  accessory: 'tie' | 'hat' | 'crown' | 'glasses' | 'none';
  quote: string;
}

export const VsPanel: React.FC<{
  title: string;
  titleColor?: string;
  left: Side;
  right: Side;
  bottomQuote?: string;
}> = ({ title, titleColor = C.glow, left, right, bottomQuote }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const fadeIn = interpolate(frame, [0, 12], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  const vsScale = spring({ frame: frame - 40, fps, config: { damping: 8, stiffness: 150 } });

  return (
    <AbsoluteFill style={{ opacity: fadeIn }}>
      <CartoonBg color="#0f0820" />
      {/* Title */}
      <div style={{ position: 'absolute', top: 25, left: 0, right: 0, textAlign: 'center' }}>
        <div style={{
          fontSize: 36,
          fontFamily: CFONT.title,
          color: titleColor,
          textTransform: 'uppercase',
          letterSpacing: '0.04em',
          textShadow: `2px 2px 0px ${C.outline}`,
        }}>{title}</div>
      </div>

      {/* Two sides */}
      <div style={{ position: 'absolute', top: 100, bottom: 80, left: 60, right: 60, display: 'flex', gap: 20 }}>
        {/* Left */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12 }}>
          <Character color={left.color} x={0} y={0} size={0.55} delay={10} expression={left.expression} accessory={left.accessory} />
          <div style={{ height: 110 }} />
          <div style={{ fontSize: 22, fontFamily: CFONT.title, color: left.color, letterSpacing: '0.04em' }}>{left.name}</div>
          {left.points.map((p, i) => {
            const d = 30 + i * 20;
            return (
              <div key={i} style={{
                opacity: interpolate(frame, [d, d + 10], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
                padding: '8px 16px',
                backgroundColor: `${left.color}15`,
                border: `2px solid ${left.color}44`,
                borderRadius: 10,
                fontSize: 16,
                fontFamily: CFONT.body,
                color: C.textWhite,
                textAlign: 'center',
                width: '90%',
              }}>{p}</div>
            );
          })}
          <SpeechBubble text={left.quote} x={-100} y={-20} delay={100} width={280} fontSize={16} />
        </div>

        {/* VS */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          transform: `scale(${vsScale})`,
        }}>
          <div style={{
            fontSize: 52,
            fontFamily: CFONT.title,
            color: C.danger,
            textShadow: `0 0 20px ${C.danger}66`,
          }}>VS</div>
        </div>

        {/* Right */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12 }}>
          <Character color={right.color} x={0} y={0} size={0.55} delay={20} expression={right.expression} accessory={right.accessory} flip />
          <div style={{ height: 110 }} />
          <div style={{ fontSize: 22, fontFamily: CFONT.title, color: right.color, letterSpacing: '0.04em' }}>{right.name}</div>
          {right.points.map((p, i) => {
            const d = 40 + i * 20;
            return (
              <div key={i} style={{
                opacity: interpolate(frame, [d, d + 10], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
                padding: '8px 16px',
                backgroundColor: `${right.color}15`,
                border: `2px solid ${right.color}44`,
                borderRadius: 10,
                fontSize: 16,
                fontFamily: CFONT.body,
                color: C.textWhite,
                textAlign: 'center',
                width: '90%',
              }}>{p}</div>
            );
          })}
          <SpeechBubble text={right.quote} x={-100} y={-20} delay={110} width={280} fontSize={16} />
        </div>
      </div>

      {bottomQuote && (
        <div style={{
          position: 'absolute', bottom: 20, left: 0, right: 0, textAlign: 'center',
          opacity: interpolate(frame, [130, 150], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
        }}>
          <div style={{ fontSize: 18, fontFamily: CFONT.caption, fontStyle: 'italic', color: C.textLight }}>
            {bottomQuote}
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};
