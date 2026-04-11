import React from 'react';
import { AbsoluteFill } from 'remotion';
import { C, CFONT, GRADIENT, SHADOW } from '../theme';
import { CartoonBg } from '../components/CartoonBg';

/**
 * Geo-Politics YouTube Channel Banner — 2560x1440
 * Safe zone for text: center 1546x423
 */
export const GeoPoliticsBanner: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#050210' }}>
      <CartoonBg color="#050210" accentColor={C.danger} particleColor={C.glow} particleCount={80} showGrid />

      {/* Big radial glow behind center */}
      <div style={{
        position: 'absolute',
        left: '50%',
        top: '50%',
        transform: 'translate(-50%, -50%)',
        width: 1600,
        height: 800,
        borderRadius: '50%',
        background: `radial-gradient(ellipse, ${C.danger}22 0%, transparent 70%)`,
        filter: 'blur(60px)',
      }} />

      {/* Content centered in safe zone */}
      <AbsoluteFill style={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        gap: 28,
      }}>
        {/* Top red badge */}
        <div style={{
          padding: '10px 32px',
          backgroundColor: C.danger,
          borderRadius: 6,
          fontSize: 22,
          fontFamily: CFONT.display,
          fontWeight: 800,
          color: '#fff',
          letterSpacing: '0.2em',
          textTransform: 'uppercase',
          boxShadow: `0 6px 30px ${C.danger}88, 0 0 0 2px rgba(255,255,255,0.1)`,
        }}>
          GEO-POLITICS · NO SUGAR COATING
        </div>

        {/* Main title - 3 lines */}
        <div style={{ textAlign: 'center' }}>
          <div style={{
            fontSize: 140,
            fontFamily: CFONT.display,
            fontWeight: 800,
            color: C.textWhite,
            letterSpacing: '-0.02em',
            lineHeight: 0.95,
            textShadow: `5px 5px 0 ${C.outline}, 0 0 60px ${C.danger}44`,
            textTransform: 'uppercase',
          }}>
            WHO ACTUALLY
          </div>
          <div style={{
            fontSize: 160,
            fontFamily: CFONT.display,
            fontWeight: 800,
            background: GRADIENT.goldOrange,
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            letterSpacing: '-0.02em',
            lineHeight: 0.95,
            textShadow: `5px 5px 0 ${C.outline}`,
            textTransform: 'uppercase',
            filter: `drop-shadow(0 0 40px ${C.glow}66)`,
          }}>
            RUNS THIS PLANET?
          </div>
        </div>

        {/* Subtitle */}
        <div style={{
          fontSize: 30,
          fontFamily: CFONT.body,
          fontWeight: 500,
          color: C.textLight,
          letterSpacing: '0.02em',
          textShadow: '0 2px 12px rgba(0,0,0,0.8)',
        }}>
          New uncomfortable facts every week · Fully sourced · 100% AI-generated
        </div>

        {/* Bottom row: handle + channel stats badges */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: 24,
          marginTop: 12,
        }}>
          {/* Logo */}
          <div style={{
            width: 72,
            height: 72,
            borderRadius: 16,
            background: `linear-gradient(135deg, ${C.danger}, ${C.charPurple})`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: 38,
            filter: `drop-shadow(0 0 20px ${C.danger}66)`,
          }}>
            🌍
          </div>

          {/* Handle */}
          <div style={{
            fontSize: 28,
            fontFamily: CFONT.mono,
            fontWeight: 700,
            color: C.glow,
            letterSpacing: '0.02em',
            textShadow: `0 0 20px ${C.glow}66`,
          }}>
            @AIRenderLab
          </div>

          {/* Divider */}
          <div style={{ width: 2, height: 36, backgroundColor: `${C.textMuted}66` }} />

          {/* Stat badges */}
          {['7 CHAPTERS', '205 SECONDS', '100% FACTS'].map((stat, i) => (
            <div key={i} style={{
              padding: '8px 18px',
              border: `2px solid ${C.glow}66`,
              borderRadius: 8,
              fontSize: 16,
              fontFamily: CFONT.mono,
              fontWeight: 700,
              color: C.glow,
              letterSpacing: '0.08em',
              backgroundColor: `${C.glow}08`,
            }}>
              {stat}
            </div>
          ))}
        </div>
      </AbsoluteFill>

      {/* Bottom gradient accent bar */}
      <div style={{
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        height: 8,
        background: `linear-gradient(90deg, transparent, ${C.danger}, ${C.glow}, ${C.charBlue}, transparent)`,
      }} />
    </AbsoluteFill>
  );
};
