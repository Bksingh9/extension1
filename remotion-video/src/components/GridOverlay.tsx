import React from 'react';
import { AbsoluteFill } from 'remotion';
import { COLORS } from '../utils/theme';

export const GridOverlay: React.FC = () => (
  <AbsoluteFill style={{ pointerEvents: 'none' }}>
    <div
      style={{
        width: '100%',
        height: '100%',
        backgroundImage: `
          linear-gradient(${COLORS.gridLine} 1px, transparent 1px),
          linear-gradient(90deg, ${COLORS.gridLine} 1px, transparent 1px)
        `,
        backgroundSize: '60px 60px',
        opacity: 0.5,
      }}
    />
  </AbsoluteFill>
);
