import React from 'react';
import { AbsoluteFill } from 'remotion';
import { COLORS, FONT } from '../utils/theme';

/**
 * Profile Picture: 800x800
 * Simple AR monogram on dark background with blue accent
 */
export const ProfilePicture: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg }}>
      {/* Subtle grid */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundImage: `
            linear-gradient(rgba(59,130,246,0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(59,130,246,0.05) 1px, transparent 1px)
          `,
          backgroundSize: '30px 30px',
        }}
      />

      {/* Glow behind logo */}
      <div
        style={{
          position: 'absolute',
          left: '50%',
          top: '50%',
          width: 400,
          height: 400,
          transform: 'translate(-50%, -50%)',
          borderRadius: '50%',
          background: `radial-gradient(circle, ${COLORS.primary}25 0%, transparent 70%)`,
          filter: 'blur(30px)',
        }}
      />

      {/* Main circle */}
      <div
        style={{
          position: 'absolute',
          left: '50%',
          top: '50%',
          transform: 'translate(-50%, -50%)',
          width: 320,
          height: 320,
          borderRadius: 160,
          backgroundColor: COLORS.primary,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: `0 0 80px ${COLORS.primary}44, inset 0 -4px 20px rgba(0,0,0,0.2)`,
        }}
      >
        <span
          style={{
            fontSize: 130,
            fontFamily: FONT.heading,
            fontWeight: 800,
            color: '#fff',
            letterSpacing: '-0.04em',
            textShadow: '0 2px 8px rgba(0,0,0,0.2)',
          }}
        >
          AR
        </span>
      </div>

      {/* Ring accent */}
      <div
        style={{
          position: 'absolute',
          left: '50%',
          top: '50%',
          transform: 'translate(-50%, -50%)',
          width: 360,
          height: 360,
          borderRadius: 180,
          border: `2px solid ${COLORS.primary}33`,
        }}
      />
    </AbsoluteFill>
  );
};
