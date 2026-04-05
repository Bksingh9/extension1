import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from 'remotion';
import { CartoonBg } from './CartoonBg';
import { C, CFONT } from '../theme';

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
}> = ({ title, titleColor = C.glow, facts, bgColor = '#0f0820' }) => {
  const frame = useCurrentFrame();
  const titleOp = interpolate(frame, [0, 15], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill>
      <CartoonBg color={bgColor} showStars={false} />
      <div style={{ padding: '40px 80px', height: '100%', display: 'flex', flexDirection: 'column' }}>
        {/* Title */}
        <div style={{
          opacity: titleOp,
          fontSize: 38,
          fontFamily: CFONT.title,
          color: titleColor,
          letterSpacing: '0.04em',
          textTransform: 'uppercase',
          textShadow: `2px 2px 0px ${C.outline}`,
          marginBottom: 24,
          textAlign: 'center',
        }}>
          {title}
        </div>

        {/* Timeline of facts */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 10, justifyContent: 'center' }}>
          {facts.map((fact, i) => {
            const delay = 20 + i * 35;
            const op = interpolate(frame, [delay, delay + 12], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
            const x = interpolate(frame, [delay, delay + 15], [-40, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });
            const color = fact.color || C.textWhite;
            const barW = interpolate(frame, [delay + 8, delay + 28], [0, 60], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });

            return (
              <div key={i} style={{ opacity: op, transform: `translateX(${x}px)`, display: 'flex', alignItems: 'center', gap: 16 }}>
                {/* Year badge */}
                {fact.year && (
                  <div style={{
                    minWidth: 80,
                    padding: '6px 12px',
                    backgroundColor: `${color}22`,
                    border: `2px solid ${color}55`,
                    borderRadius: 8,
                    fontSize: 16,
                    fontFamily: CFONT.title,
                    color,
                    textAlign: 'center',
                    letterSpacing: '0.03em',
                  }}>
                    {fact.year}
                  </div>
                )}
                {fact.icon && <span style={{ fontSize: 26 }}>{fact.icon}</span>}
                {/* Connector bar */}
                <div style={{ width: barW, height: 3, backgroundColor: color, borderRadius: 2, opacity: 0.5 }} />
                {/* Fact content */}
                <div style={{ flex: 1 }}>
                  <div style={{
                    fontSize: 20,
                    fontFamily: CFONT.body,
                    fontWeight: 700,
                    color: C.textWhite,
                    lineHeight: 1.3,
                  }}>
                    {fact.text}
                  </div>
                  {fact.detail && (
                    <div style={{
                      opacity: interpolate(frame, [delay + 15, delay + 25], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
                      fontSize: 15,
                      fontFamily: CFONT.body,
                      color: C.textLight,
                      marginTop: 4,
                    }}>
                      {fact.detail}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
