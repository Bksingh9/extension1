import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from 'remotion';
import { CartoonBg } from './CartoonBg';
import { C, CFONT, SHADOW, RAD } from '../theme';
import { fadeIn, stagger, countUp } from '../animation';

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
}> = ({ title, titleColor = C.glow, bars, subtitle, bgColor = '#080414' }) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill>
      <CartoonBg color={bgColor} accentColor={titleColor} showGrid />
      <div style={{ padding: '40px 100px', height: '100%', display: 'flex', flexDirection: 'column' }}>
        <div style={{
          opacity: fadeIn(frame, 0, 12),
          fontSize: 32,
          fontFamily: CFONT.display,
          fontWeight: 800,
          color: titleColor,
          textTransform: 'uppercase',
          textShadow: SHADOW.text(titleColor),
          textAlign: 'center',
          marginBottom: 6,
        }}>{title}</div>
        {subtitle && (
          <div style={{
            opacity: fadeIn(frame, 8, 12),
            fontSize: 16,
            fontFamily: CFONT.body,
            color: C.textLight,
            textAlign: 'center',
            marginBottom: 24,
          }}>{subtitle}</div>
        )}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 14 }}>
          {bars.map((bar, i) => {
            const d = 12 + stagger(i, 16);
            const op = fadeIn(frame, d, 8);
            const barPct = interpolate(frame, [d + 4, d + 32], [0, (bar.value / bar.maxValue) * 100], {
              extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.exp),
            });
            const valOp = fadeIn(frame, d + 18, 8);

            return (
              <div key={i} style={{ opacity: op }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6, alignItems: 'center' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    {bar.icon && <span style={{ fontSize: 18, filter: `drop-shadow(0 0 4px ${bar.color}44)` }}>{bar.icon}</span>}
                    <span style={{ fontSize: 15, fontFamily: CFONT.body, fontWeight: 600, color: C.textWhite }}>{bar.label}</span>
                  </div>
                  <span style={{
                    opacity: valOp,
                    fontSize: 18,
                    fontFamily: CFONT.display,
                    fontWeight: 800,
                    color: bar.color,
                    letterSpacing: '-0.01em',
                    textShadow: `0 0 8px ${bar.color}33`,
                  }}>
                    {bar.displayValue}
                  </span>
                </div>
                {/* Bar track */}
                <div style={{
                  height: 26,
                  backgroundColor: `${C.outline}88`,
                  borderRadius: RAD.sm,
                  overflow: 'hidden',
                  border: `1px solid ${C.outlineLight}44`,
                  position: 'relative',
                }}>
                  {/* Grid lines */}
                  {[25, 50, 75].map(pct => (
                    <div key={pct} style={{
                      position: 'absolute',
                      left: `${pct}%`,
                      top: 0,
                      bottom: 0,
                      width: 1,
                      backgroundColor: `${C.outlineLight}33`,
                    }} />
                  ))}
                  {/* Gradient bar fill */}
                  <div style={{
                    width: `${barPct}%`,
                    height: '100%',
                    background: `linear-gradient(90deg, ${bar.color}cc, ${bar.color})`,
                    borderRadius: RAD.sm - 1,
                    boxShadow: `0 0 16px ${bar.color}33, inset 0 1px 0 rgba(255,255,255,0.15)`,
                    position: 'relative',
                  }}>
                    {/* Highlight line on top of bar */}
                    <div style={{
                      position: 'absolute',
                      top: 2,
                      left: 4,
                      right: 4,
                      height: 3,
                      background: 'rgba(255,255,255,0.12)',
                      borderRadius: 2,
                    }} />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
