import React from 'react';
import { AbsoluteFill } from 'remotion';
import { C, CFONT } from '../theme';

/**
 * Geo-Politics Channel Profile Picture — 800x800
 * Circular design with globe + conspiracy eye motif
 */
export const GeoPoliticsProfile: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#050210' }}>
      {/* Radial gradient bg */}
      <div style={{
        position: 'absolute',
        inset: 0,
        background: `radial-gradient(circle at 50% 40%, ${C.bgCard} 0%, #050210 70%)`,
      }} />

      {/* Outer glow ring */}
      <div style={{
        position: 'absolute',
        left: '50%',
        top: '50%',
        transform: 'translate(-50%, -50%)',
        width: 720,
        height: 720,
        borderRadius: '50%',
        background: `conic-gradient(from 0deg, ${C.danger}, ${C.charPurple}, ${C.charBlue}, ${C.glow}, ${C.danger})`,
        filter: 'blur(20px)',
        opacity: 0.4,
      }} />

      {/* Outer border ring */}
      <div style={{
        position: 'absolute',
        left: '50%',
        top: '50%',
        transform: 'translate(-50%, -50%)',
        width: 700,
        height: 700,
        borderRadius: '50%',
        border: `6px solid ${C.danger}`,
        boxShadow: `0 0 60px ${C.danger}88, inset 0 0 40px ${C.danger}44`,
      }} />

      {/* Inner circle (dark bg) */}
      <div style={{
        position: 'absolute',
        left: '50%',
        top: '50%',
        transform: 'translate(-50%, -50%)',
        width: 640,
        height: 640,
        borderRadius: '50%',
        backgroundColor: '#0a0518',
        border: `3px solid ${C.outlineLight}`,
        overflow: 'hidden',
      }}>
        {/* Grid texture */}
        <div style={{
          position: 'absolute',
          inset: 0,
          backgroundImage: `
            linear-gradient(${C.glow}15 1px, transparent 1px),
            linear-gradient(90deg, ${C.glow}15 1px, transparent 1px)
          `,
          backgroundSize: '40px 40px',
        }} />

        {/* Radial spotlight */}
        <div style={{
          position: 'absolute',
          inset: 0,
          background: `radial-gradient(circle at 50% 45%, ${C.glow}22 0%, transparent 60%)`,
        }} />
      </div>

      {/* Globe emoji (big center) */}
      <AbsoluteFill style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        <div style={{
          fontSize: 280,
          filter: `drop-shadow(0 0 40px ${C.glow}88) drop-shadow(0 10px 20px rgba(0,0,0,0.8))`,
          marginTop: -40,
        }}>
          🌍
        </div>
      </AbsoluteFill>

      {/* Bottom text */}
      <AbsoluteFill style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'flex-end',
        paddingBottom: 160,
      }}>
        <div style={{
          padding: '6px 22px',
          backgroundColor: C.danger,
          borderRadius: 4,
          fontSize: 22,
          fontFamily: CFONT.display,
          fontWeight: 800,
          color: '#fff',
          letterSpacing: '0.15em',
          textTransform: 'uppercase',
          boxShadow: `0 4px 20px ${C.danger}88`,
        }}>
          NO SUGAR COATING
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
