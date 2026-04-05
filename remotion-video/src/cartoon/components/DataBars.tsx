import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from 'remotion';
import { CartoonBg } from './CartoonBg';
import { C, CFONT } from '../theme';

interface DataBar {
  label: string;
  value: number;
  maxValue: number;
  displayValue: string;
  color: string;
  icon?: string;
}

export const DataBars: React.FC<{
  title: string;
  titleColor?: string;
  bars: DataBar[];
  subtitle?: string;
  bgColor?: string;
}> = ({ title, titleColor = C.glow, bars, subtitle, bgColor = '#0d0619' }) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill>
      <CartoonBg color={bgColor} showStars={false} />
      <div style={{ padding: '40px 100px', height: '100%', display: 'flex', flexDirection: 'column' }}>
        <div style={{
          opacity: interpolate(frame, [0, 15], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
          fontSize: 36,
          fontFamily: CFONT.title,
          color: titleColor,
          textTransform: 'uppercase',
          letterSpacing: '0.04em',
          textShadow: `2px 2px 0px ${C.outline}`,
          textAlign: 'center',
          marginBottom: 8,
        }}>
          {title}
        </div>
        {subtitle && (
          <div style={{
            opacity: interpolate(frame, [10, 22], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }),
            fontSize: 18,
            fontFamily: CFONT.body,
            color: C.textLight,
            textAlign: 'center',
            marginBottom: 20,
          }}>
            {subtitle}
          </div>
        )}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 16 }}>
          {bars.map((bar, i) => {
            const delay = 15 + i * 18;
            const op = interpolate(frame, [delay, delay + 10], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
            const barPct = interpolate(frame, [delay + 5, delay + 35], [0, (bar.value / bar.maxValue) * 100], {
              extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic),
            });
            const valOp = interpolate(frame, [delay + 20, delay + 30], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

            return (
              <div key={i} style={{ opacity: op }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    {bar.icon && <span style={{ fontSize: 20 }}>{bar.icon}</span>}
                    <span style={{ fontSize: 18, fontFamily: CFONT.body, fontWeight: 700, color: C.textWhite }}>{bar.label}</span>
                  </div>
                  <span style={{ opacity: valOp, fontSize: 20, fontFamily: CFONT.title, color: bar.color, letterSpacing: '0.02em' }}>
                    {bar.displayValue}
                  </span>
                </div>
                <div style={{ height: 28, backgroundColor: `${C.outline}88`, borderRadius: 6, overflow: 'hidden', border: `2px solid ${C.outlineLight}` }}>
                  <div style={{
                    width: `${barPct}%`,
                    height: '100%',
                    backgroundColor: bar.color,
                    borderRadius: 4,
                    boxShadow: `0 0 12px ${bar.color}44`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'flex-end',
                    paddingRight: 8,
                  }} />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
