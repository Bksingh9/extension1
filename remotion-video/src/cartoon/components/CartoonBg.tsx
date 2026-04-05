import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { C } from '../theme';

export const CartoonBg: React.FC<{
  color?: string;
  showStars?: boolean;
}> = ({ color = C.bgDark, showStars = true }) => {
  const frame = useCurrentFrame();

  // Generate deterministic "stars"
  const stars = React.useMemo(() => {
    const s = [];
    for (let i = 0; i < 40; i++) {
      const seed = i * 7919;
      s.push({
        x: (seed * 13) % 1920,
        y: (seed * 17) % 1080,
        size: 1.5 + (seed % 3),
        phase: (seed % 628) / 100,
      });
    }
    return s;
  }, []);

  return (
    <AbsoluteFill style={{ backgroundColor: color }}>
      {/* Radial vignette */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: 'radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.6) 100%)',
        }}
      />
      {/* Stars */}
      {showStars &&
        stars.map((star, i) => (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: star.x,
              top: star.y,
              width: star.size,
              height: star.size,
              borderRadius: '50%',
              backgroundColor: '#fff',
              opacity: 0.3 + Math.sin(frame * 0.05 + star.phase) * 0.25,
            }}
          />
        ))}
      {/* Halftone overlay for comic feel */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundImage:
            'radial-gradient(circle, rgba(255,255,255,0.03) 1px, transparent 1px)',
          backgroundSize: '12px 12px',
        }}
      />
    </AbsoluteFill>
  );
};
