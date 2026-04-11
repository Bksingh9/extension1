import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from 'remotion';
import { CartoonBg } from './CartoonBg';
import { C, CFONT, SHADOW, GRADIENT, RAD } from '../theme';
import { fadeIn, slideRight, stagger, glowPulse } from '../animation';

interface Fact {
  year?: string;
  text: string;
  detail?: string;
  color?: string;
  icon?: string;
}

export const FactSequence: React.FC<{
  title: string;
  titleColor?: string;
  facts: Fact[];
  bgColor?: string;
}> = ({ title, titleColor = C.glow, facts, bgColor = '#0a0618' }) => {
  const frame = useCurrentFrame();
  const titleOp = fadeIn(frame, 0, 14);
  const titleScale = interpolate(frame, [0, 18], [0.92, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });
  const accentW = interpolate(frame, [10, 28], [0, 100], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });

  return (
    <AbsoluteFill>
      <CartoonBg color={bgColor} accentColor={titleColor} showGrid />

      {/* ── TITLE BLOCK ── */}
      <div style={{
        position: 'absolute',
        top: 48,
        left: 80,
        right: 80,
        opacity: titleOp,
        transform: `scale(${titleScale})`,
        textAlign: 'center',
      }}>
        <div style={{
          width: `${accentW}%`,
          maxWidth: 180,
          height: 4,
          background: `linear-gradient(90deg, transparent, ${titleColor}, transparent)`,
          margin: '0 auto 12px',
          borderRadius: 2,
        }} />
        <div style={{
          fontSize: 46,
          fontFamily: CFONT.display,
          fontWeight: 800,
          color: titleColor,
          textTransform: 'uppercase',
          letterSpacing: '0.03em',
          lineHeight: 1,
          textShadow: `3px 3px 0 ${C.outline}, 0 0 30px ${titleColor}66, 0 4px 12px rgba(0,0,0,0.5)`,
        }}>
          {title}
        </div>
      </div>

      {/* ── FACTS TIMELINE (FULL WIDTH) ── */}
      <div style={{
        position: 'absolute',
        top: 180,
        bottom: 60,
        left: 100,
        right: 100,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        gap: 14,
      }}>
        {facts.map((fact, i) => {
          const d = 22 + i * 18;
          const op = fadeIn(frame, d, 12);
          const xOff = slideRight(frame, d, 40, 16);
          const color = fact.color || C.textWhite;
          const connectorW = interpolate(frame, [d + 8, d + 26], [0, 60], {
            extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic),
          });
          const glow = glowPulse(frame, 0.4, 0.9, 0.05);

          return (
            <div
              key={i}
              style={{
                opacity: op,
                transform: `translateX(${xOff}px)`,
                display: 'flex',
                alignItems: 'center',
                gap: 18,
                width: '100%',
                padding: '10px 20px',
                background: `linear-gradient(90deg, ${color}0a 0%, transparent 70%)`,
                borderLeft: `3px solid ${color}aa`,
                borderRadius: '4px 12px 12px 4px',
              }}
            >
              {/* Year badge */}
              {fact.year && (
                <div style={{
                  minWidth: 96,
                  padding: '8px 14px',
                  background: `linear-gradient(135deg, ${color}33, ${color}0f)`,
                  border: `2px solid ${color}88`,
                  borderRadius: RAD.md,
                  fontSize: 16,
                  fontFamily: CFONT.mono,
                  fontWeight: 700,
                  color,
                  textAlign: 'center',
                  letterSpacing: '0.05em',
                  boxShadow: `0 0 ${16 * glow}px ${color}44, 0 2px 8px rgba(0,0,0,0.4)`,
                  textShadow: `0 0 12px ${color}88`,
                }}>
                  {fact.year}
                </div>
              )}
              {/* Icon */}
              {fact.icon && (
                <span style={{
                  fontSize: 32,
                  filter: `drop-shadow(0 0 10px ${color}66)`,
                  flexShrink: 0,
                }}>{fact.icon}</span>
              )}
              {/* Connector line */}
              <div style={{
                width: connectorW,
                height: 3,
                background: `linear-gradient(90deg, ${color}cc, ${color}22)`,
                borderRadius: 2,
                flexShrink: 0,
                boxShadow: `0 0 8px ${color}44`,
              }} />
              {/* Fact text */}
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{
                  fontSize: 24,
                  fontFamily: CFONT.body,
                  fontWeight: 700,
                  color: C.textWhite,
                  lineHeight: 1.3,
                  textShadow: '0 2px 8px rgba(0,0,0,0.6)',
                  letterSpacing: '0.005em',
                }}>
                  {fact.text}
                </div>
                {fact.detail && (
                  <div style={{
                    opacity: fadeIn(frame, d + 14, 12),
                    fontSize: 15,
                    fontFamily: CFONT.body,
                    fontWeight: 400,
                    color: C.textLight,
                    marginTop: 4,
                    textShadow: '0 1px 4px rgba(0,0,0,0.6)',
                    letterSpacing: '0.01em',
                  }}>
                    {fact.detail}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
