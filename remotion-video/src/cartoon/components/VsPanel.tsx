import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate, Easing } from 'remotion';
import { CartoonBg } from './CartoonBg';
import { Character } from './Character';
import { C, CFONT, SHADOW, SPRING, RAD } from '../theme';
import { fadeIn, slideLeft, slideRight, glowPulse } from '../animation';

interface Side {
  name: string;
  color: string;
  colorLight?: string;
  points: string[];
  expression: 'angry' | 'suspicious' | 'neutral' | 'happy' | 'shocked' | 'thoughtful' | 'smug';
  accessory: 'tie' | 'hat' | 'crown' | 'glasses' | 'none' | 'keffiyeh' | 'collar';
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
  const vsScale = spring({ frame: frame - 45, fps, config: SPRING.bouncy });
  const vsGlow = glowPulse(frame, 0.5, 1, 0.08);

  return (
    <AbsoluteFill>
      <CartoonBg color="#0a0618" accentColor={titleColor} />
      {/* Title */}
      <div style={{ position: 'absolute', top: 28, left: 0, right: 0, textAlign: 'center' }}>
        <div style={{
          opacity: fadeIn(frame, 3, 12),
          fontSize: 32,
          fontFamily: CFONT.display,
          fontWeight: 800,
          color: titleColor,
          textTransform: 'uppercase',
          letterSpacing: '0.02em',
          textShadow: SHADOW.text(titleColor),
        }}>{title}</div>
      </div>

      {/* Two sides */}
      <div style={{ position: 'absolute', top: 90, bottom: 70, left: 60, right: 60, display: 'flex', gap: 20 }}>
        {/* Left side */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10, paddingTop: 20 }}>
          <div style={{ position: 'relative', width: 120, height: 160 }}>
            <Character color={left.color} colorLight={left.colorLight} x={-30} y={160} size={0.65} delay={8} expression={left.expression} accessory={left.accessory} />
          </div>
          <div style={{ fontSize: 20, fontFamily: CFONT.display, fontWeight: 800, color: left.color, letterSpacing: '0.03em', textShadow: SHADOW.text(left.color) }}>{left.name}</div>
          {left.points.map((p, i) => {
            const d = 25 + i * 14;
            const x = slideRight(frame, d, 30, 14);
            return (
              <div key={i} style={{
                opacity: fadeIn(frame, d, 8),
                transform: `translateX(${x}px)`,
                padding: '7px 16px',
                background: `linear-gradient(135deg, ${left.color}12, ${left.color}06)`,
                border: `1.5px solid ${left.color}44`,
                borderRadius: RAD.md,
                fontSize: 14,
                fontFamily: CFONT.body,
                fontWeight: 600,
                color: C.textWhite,
                textAlign: 'center',
                width: '92%',
              }}>{p}</div>
            );
          })}
          {/* Quote */}
          <div style={{
            opacity: fadeIn(frame, 100, 12),
            padding: '8px 14px',
            backgroundColor: 'rgba(255,255,255,0.95)',
            borderRadius: RAD.lg,
            border: `2px solid ${left.color}44`,
            boxShadow: '0 4px 16px rgba(0,0,0,0.3)',
            maxWidth: '85%',
          }}>
            <div style={{ fontSize: 13, fontFamily: CFONT.body, fontWeight: 600, color: C.speechText, textAlign: 'center', fontStyle: 'italic' }}>
              "{left.quote}"
            </div>
          </div>
        </div>

        {/* VS divider */}
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 12 }}>
          <div style={{ width: 2, height: 80, background: `linear-gradient(180deg, transparent, ${C.danger}44, transparent)` }} />
          <div style={{
            transform: `scale(${vsScale})`,
            fontSize: 48,
            fontFamily: CFONT.display,
            fontWeight: 900,
            color: C.danger,
            textShadow: `0 0 ${30 * vsGlow}px ${C.danger}66, 2px 2px 0 ${C.outline}`,
          }}>VS</div>
          <div style={{ width: 2, height: 80, background: `linear-gradient(180deg, transparent, ${C.danger}44, transparent)` }} />
        </div>

        {/* Right side */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10, paddingTop: 20 }}>
          <div style={{ position: 'relative', width: 120, height: 160 }}>
            <Character color={right.color} colorLight={right.colorLight} x={-30} y={160} size={0.65} delay={16} expression={right.expression} accessory={right.accessory} flip />
          </div>
          <div style={{ fontSize: 20, fontFamily: CFONT.display, fontWeight: 800, color: right.color, letterSpacing: '0.03em', textShadow: SHADOW.text(right.color) }}>{right.name}</div>
          {right.points.map((p, i) => {
            const d = 35 + i * 14;
            const x = slideLeft(frame, d, 30, 14);
            return (
              <div key={i} style={{
                opacity: fadeIn(frame, d, 8),
                transform: `translateX(${x}px)`,
                padding: '7px 16px',
                background: `linear-gradient(135deg, ${right.color}12, ${right.color}06)`,
                border: `1.5px solid ${right.color}44`,
                borderRadius: RAD.md,
                fontSize: 14,
                fontFamily: CFONT.body,
                fontWeight: 600,
                color: C.textWhite,
                textAlign: 'center',
                width: '92%',
              }}>{p}</div>
            );
          })}
          <div style={{
            opacity: fadeIn(frame, 108, 12),
            padding: '8px 14px',
            backgroundColor: 'rgba(255,255,255,0.95)',
            borderRadius: RAD.lg,
            border: `2px solid ${right.color}44`,
            boxShadow: '0 4px 16px rgba(0,0,0,0.3)',
            maxWidth: '85%',
          }}>
            <div style={{ fontSize: 13, fontFamily: CFONT.body, fontWeight: 600, color: C.speechText, textAlign: 'center', fontStyle: 'italic' }}>
              "{right.quote}"
            </div>
          </div>
        </div>
      </div>

      {/* Bottom quote */}
      {bottomQuote && (
        <div style={{
          position: 'absolute', bottom: 22, left: 0, right: 0, textAlign: 'center',
          opacity: fadeIn(frame, 130, 12),
        }}>
          <div style={{
            fontSize: 16,
            fontFamily: CFONT.body,
            fontStyle: 'italic',
            color: C.textLight,
            textShadow: '0 1px 4px rgba(0,0,0,0.5)',
          }}>{bottomQuote}</div>
        </div>
      )}
    </AbsoluteFill>
  );
};
