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

  return (
    <AbsoluteFill>
      <CartoonBg color={bgColor} accentColor={titleColor} showGrid />
      <div style={{ padding: '40px 100px', height: '100%', display: 'flex', flexDirection: 'column' }}>
        {/* Title */}
        <div style={{
          opacity: fadeIn(frame, 0, 12),
          fontSize: 34,
          fontFamily: CFONT.display,
          fontWeight: 800,
          color: titleColor,
          letterSpacing: '0.02em',
          textTransform: 'uppercase',
          textShadow: SHADOW.text(titleColor),
          textAlign: 'center',
          marginBottom: 28,
        }}>
          {title}
        </div>

        {/* Facts timeline */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 8, justifyContent: 'center' }}>
          {facts.map((fact, i) => {
            const d = 18 + i * 30;
            const op = fadeIn(frame, d, 10);
            const xOff = slideRight(frame, d, 30, 14);
            const color = fact.color || C.textWhite;
            const connectorW = interpolate(frame, [d + 6, d + 22], [0, 50], {
              extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic),
            });
            const glow = glowPulse(frame, 0.4, 0.8, 0.04);

            return (
              <div key={i} style={{ opacity: op, transform: `translateX(${xOff}px)`, display: 'flex', alignItems: 'center', gap: 14 }}>
                {/* Year badge with gradient */}
                {fact.year && (
                  <div style={{
                    minWidth: 72,
                    padding: '5px 12px',
                    background: `linear-gradient(135deg, ${color}22, ${color}08)`,
                    border: `2px solid ${color}55`,
                    borderRadius: RAD.md,
                    fontSize: 13,
                    fontFamily: CFONT.mono,
                    fontWeight: 700,
                    color,
                    textAlign: 'center',
                    letterSpacing: '0.04em',
                    boxShadow: `0 0 ${12 * glow}px ${color}22`,
                  }}>
                    {fact.year}
                  </div>
                )}
                {/* Icon */}
                {fact.icon && <span style={{ fontSize: 24, filter: `drop-shadow(0 0 6px ${color}44)` }}>{fact.icon}</span>}
                {/* Connector line */}
                <div style={{ width: connectorW, height: 2, background: `linear-gradient(90deg, ${color}66, ${color}11)`, borderRadius: 1 }} />
                {/* Fact text */}
                <div style={{ flex: 1 }}>
                  <div style={{
                    fontSize: 18,
                    fontFamily: CFONT.body,
                    fontWeight: 700,
                    color: C.textWhite,
                    lineHeight: 1.35,
                  }}>
                    {fact.text}
                  </div>
                  {fact.detail && (
                    <div style={{
                      opacity: fadeIn(frame, d + 12, 10),
                      fontSize: 13,
                      fontFamily: CFONT.body,
                      fontWeight: 400,
                      color: C.textLight,
                      marginTop: 3,
                    }}>
                      {fact.detail}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Progress bar at bottom */}
        <div style={{ height: 2, background: C.outline, borderRadius: 1, marginTop: 16, overflow: 'hidden' }}>
          <div style={{
            height: '100%',
            width: `${(frame / 280) * 100}%`,
            background: `linear-gradient(90deg, ${titleColor}, ${titleColor}44)`,
            borderRadius: 1,
          }} />
        </div>
      </div>
    </AbsoluteFill>
  );
};
