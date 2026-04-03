import React from 'react';
import { AbsoluteFill } from 'remotion';
import { COLORS } from '../theme';

export const ThumbnailBase: React.FC<{
  children: React.ReactNode;
  glowColor?: string;
  glowX?: string;
  glowY?: string;
}> = ({ children, glowColor = COLORS.primaryGlow, glowX = '50%', glowY = '50%' }) => (
  <AbsoluteFill
    style={{
      backgroundColor: COLORS.bg,
      overflow: 'hidden',
    }}
  >
    {/* Grid overlay */}
    <div
      style={{
        position: 'absolute',
        inset: 0,
        backgroundImage: `
          linear-gradient(rgba(59,130,246,0.04) 1px, transparent 1px),
          linear-gradient(90deg, rgba(59,130,246,0.04) 1px, transparent 1px)
        `,
        backgroundSize: '40px 40px',
      }}
    />
    {/* Glow */}
    <div
      style={{
        position: 'absolute',
        left: glowX,
        top: glowY,
        width: 500,
        height: 500,
        transform: 'translate(-50%, -50%)',
        borderRadius: '50%',
        background: `radial-gradient(circle, ${glowColor}30 0%, transparent 70%)`,
        filter: 'blur(30px)',
      }}
    />
    {/* Content */}
    <div style={{ position: 'relative', width: '100%', height: '100%', padding: '40px 50px' }}>
      {children}
    </div>
    {/* Channel badge */}
    <div
      style={{
        position: 'absolute',
        bottom: 30,
        right: 40,
        display: 'flex',
        alignItems: 'center',
        gap: 8,
        padding: '8px 16px',
        backgroundColor: 'rgba(10,10,15,0.8)',
        border: `1px solid ${COLORS.border}`,
        borderRadius: 8,
      }}
    >
      <div
        style={{
          width: 24,
          height: 24,
          borderRadius: 12,
          backgroundColor: COLORS.primary,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 11,
          fontWeight: 800,
          color: '#fff',
          fontFamily: 'Inter, sans-serif',
        }}
      >
        AR
      </div>
      <span
        style={{
          fontSize: 13,
          fontFamily: 'Inter, sans-serif',
          fontWeight: 600,
          color: COLORS.textSecondary,
          letterSpacing: '0.03em',
        }}
      >
        AI RENDER LAB
      </span>
    </div>
  </AbsoluteFill>
);
