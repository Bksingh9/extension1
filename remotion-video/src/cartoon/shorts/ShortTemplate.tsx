import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate, Easing } from 'remotion';
import { C, CFONT, SHADOW, SPRING, GRADIENT, RAD } from '../theme';
import { fadeIn, slideUp, glowPulse, stagger } from '../animation';
import { CartoonBg } from '../components/CartoonBg';
import { ParticleField } from '../components/ParticleField';

/**
 * Reusable YouTube Shorts template (1080x1920, 60s max)
 * Structure: Hook (3s) → Facts (45s) → CTA (12s)
 */

// ─── Hook Section (first 3 seconds) ───
export const ShortHook: React.FC<{
  text: string;
  subtext?: string;
  color?: string;
  bgColor?: string;
}> = ({ text, subtext, color = C.danger, bgColor = '#060310' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({ frame: frame - 3, fps, config: SPRING.bouncy });

  return (
    <AbsoluteFill>
      <CartoonBg color={bgColor} accentColor={color} particleCount={20} />
      <AbsoluteFill style={{
        display: 'flex', flexDirection: 'column', justifyContent: 'center',
        alignItems: 'center', padding: '80px 60px', gap: 20,
      }}>
        <div style={{
          transform: `scale(${scale})`,
          fontSize: 64,
          fontFamily: CFONT.display,
          fontWeight: 800,
          color,
          textAlign: 'center',
          lineHeight: 1.15,
          textTransform: 'uppercase',
          textShadow: `3px 3px 0 ${C.outline}, ${SHADOW.text(color)}`,
        }}>{text}</div>
        {subtext && (
          <div style={{
            opacity: fadeIn(frame, 20, 10),
            fontSize: 22,
            fontFamily: CFONT.body,
            fontWeight: 400,
            color: C.textLight,
            textAlign: 'center',
          }}>{subtext}</div>
        )}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ─── Fact Card (for vertical layout) ───
export const ShortFact: React.FC<{
  year?: string;
  text: string;
  detail?: string;
  color?: string;
  icon?: string;
  delay?: number;
}> = ({ year, text, detail, color = C.textWhite, icon, delay = 0 }) => {
  const frame = useCurrentFrame();
  const op = fadeIn(frame, delay, 10);
  const y = slideUp(frame, delay, 30, 14);

  return (
    <div style={{
      opacity: op,
      transform: `translateY(${y}px)`,
      padding: '16px 24px',
      background: `linear-gradient(135deg, ${color}10, ${color}05)`,
      border: `1.5px solid ${color}33`,
      borderRadius: RAD.lg,
      marginBottom: 12,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 6 }}>
        {icon && <span style={{ fontSize: 28 }}>{icon}</span>}
        {year && (
          <div style={{
            padding: '3px 10px',
            backgroundColor: `${color}22`,
            border: `1px solid ${color}44`,
            borderRadius: RAD.sm,
            fontSize: 13,
            fontFamily: CFONT.mono,
            fontWeight: 700,
            color,
          }}>{year}</div>
        )}
      </div>
      <div style={{
        fontSize: 22,
        fontFamily: CFONT.body,
        fontWeight: 700,
        color: C.textWhite,
        lineHeight: 1.35,
      }}>{text}</div>
      {detail && (
        <div style={{
          opacity: fadeIn(frame, delay + 10, 8),
          fontSize: 15,
          fontFamily: CFONT.body,
          fontWeight: 400,
          color: C.textLight,
          marginTop: 6,
          lineHeight: 1.4,
        }}>{detail}</div>
      )}
    </div>
  );
};

// ─── CTA Section (last 12 seconds) ───
export const ShortCTA: React.FC<{
  delay?: number;
}> = ({ delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({ frame: frame - delay, fps, config: SPRING.bouncy });
  const pulse = glowPulse(frame, 0.95, 1.05, 0.1);

  return (
    <AbsoluteFill>
      <CartoonBg color="#060310" accentColor={C.danger} particleCount={15} />
      <AbsoluteFill style={{
        display: 'flex', flexDirection: 'column', justifyContent: 'center',
        alignItems: 'center', gap: 28, padding: '80px 60px',
      }}>
        <div style={{
          opacity: fadeIn(frame, delay, 12),
          fontSize: 44,
          fontFamily: CFONT.display,
          fontWeight: 800,
          color: C.textWhite,
          textAlign: 'center',
          textShadow: `2px 2px 0 ${C.outline}`,
        }}>Want more?</div>

        <div style={{
          transform: `scale(${scale * pulse})`,
          padding: '18px 48px',
          backgroundColor: C.danger,
          borderRadius: 10,
          fontSize: 28,
          fontFamily: CFONT.display,
          fontWeight: 800,
          color: '#fff',
          letterSpacing: '0.04em',
          textTransform: 'uppercase',
          boxShadow: `0 6px 30px ${C.danger}66`,
        }}>SUBSCRIBE</div>

        <div style={{
          opacity: fadeIn(frame, delay + 20, 12),
          fontSize: 18,
          fontFamily: CFONT.body,
          color: C.textLight,
          textAlign: 'center',
        }}>New uncomfortable facts every week.</div>

        <div style={{
          opacity: fadeIn(frame, delay + 30, 12),
          display: 'flex', alignItems: 'center', gap: 10,
        }}>
          <div style={{
            width: 40, height: 40, borderRadius: 20,
            backgroundColor: C.info,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 16, fontFamily: CFONT.display, fontWeight: 800, color: '#fff',
          }}>AR</div>
          <span style={{ fontSize: 18, fontFamily: CFONT.display, fontWeight: 600, color: C.textLight }}>
            AI RENDER LAB
          </span>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
