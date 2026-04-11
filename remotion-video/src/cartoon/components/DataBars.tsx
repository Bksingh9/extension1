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
  const titleOp = fadeIn(frame, 0, 14);
  const titleScale = interpolate(frame, [0, 18], [0.92, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });
  const accentW = interpolate(frame, [10, 28], [0, 100], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });

  return (
    <AbsoluteFill>
      <CartoonBg color={bgColor} accentColor={titleColor} showGrid />

      {/* ── TITLE BLOCK (prominent top bar) ── */}
      <div style={{
        position: 'absolute',
        top: 48,
        left: 80,
        right: 80,
        opacity: titleOp,
        transform: `scale(${titleScale})`,
        textAlign: 'center',
      }}>
        {/* Accent line above */}
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
        }}>{title}</div>
        {subtitle && (
          <div style={{
            opacity: fadeIn(frame, 12, 14),
            fontSize: 18,
            fontFamily: CFONT.body,
            fontWeight: 500,
            color: C.textLight,
            marginTop: 10,
            textShadow: '0 2px 8px rgba(0,0,0,0.6)',
          }}>{subtitle}</div>
        )}
      </div>

      {/* ── BARS AREA (full width) ── */}
      <div style={{
        position: 'absolute',
        top: 220,
        bottom: 60,
        left: 80,
        right: 80,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        gap: 18,
      }}>
        {bars.map((bar, i) => {
          const d = 20 + stagger(i, 14);
          const op = fadeIn(frame, d, 10);
          const slideX = interpolate(frame, [d, d + 16], [-30, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });
          const barPct = interpolate(frame, [d + 6, d + 36], [0, (bar.value / bar.maxValue) * 100], {
            extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.exp),
          });
          const valOp = fadeIn(frame, d + 22, 10);

          return (
            <div key={i} style={{ opacity: op, transform: `translateX(${slideX}px)` }}>
              {/* Label row */}
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, alignItems: 'center' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  {bar.icon && (
                    <span style={{
                      fontSize: 26,
                      filter: `drop-shadow(0 0 8px ${bar.color}66)`,
                    }}>{bar.icon}</span>
                  )}
                  <span style={{
                    fontSize: 20,
                    fontFamily: CFONT.body,
                    fontWeight: 700,
                    color: C.textWhite,
                    textShadow: '0 2px 6px rgba(0,0,0,0.6)',
                    letterSpacing: '0.01em',
                  }}>{bar.label}</span>
                </div>
                <span style={{
                  opacity: valOp,
                  fontSize: 26,
                  fontFamily: CFONT.display,
                  fontWeight: 800,
                  color: bar.color,
                  letterSpacing: '-0.01em',
                  textShadow: `0 0 16px ${bar.color}66, 2px 2px 0 ${C.outline}`,
                }}>
                  {bar.displayValue}
                </span>
              </div>
              {/* Bar track */}
              <div style={{
                height: 32,
                backgroundColor: `${C.outline}aa`,
                borderRadius: RAD.sm,
                overflow: 'hidden',
                border: `1px solid ${C.outlineLight}66`,
                position: 'relative',
                boxShadow: 'inset 0 2px 6px rgba(0,0,0,0.4)',
              }}>
                {/* Grid lines */}
                {[25, 50, 75].map(pct => (
                  <div key={pct} style={{
                    position: 'absolute',
                    left: `${pct}%`,
                    top: 0,
                    bottom: 0,
                    width: 1,
                    backgroundColor: `${C.outlineLight}44`,
                  }} />
                ))}
                {/* Gradient bar fill */}
                <div style={{
                  width: `${barPct}%`,
                  height: '100%',
                  background: `linear-gradient(90deg, ${bar.color}aa 0%, ${bar.color} 50%, ${bar.color}ee 100%)`,
                  borderRadius: RAD.sm - 1,
                  boxShadow: `0 0 24px ${bar.color}55, inset 0 2px 0 rgba(255,255,255,0.25), inset 0 -2px 4px rgba(0,0,0,0.25)`,
                  position: 'relative',
                }}>
                  {/* Highlight line */}
                  <div style={{
                    position: 'absolute',
                    top: 3,
                    left: 6,
                    right: 6,
                    height: 4,
                    background: 'linear-gradient(90deg, rgba(255,255,255,0.3), rgba(255,255,255,0.05))',
                    borderRadius: 2,
                  }} />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
