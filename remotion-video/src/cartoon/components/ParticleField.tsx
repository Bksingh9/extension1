import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { noise2D } from '@remotion/noise';

/**
 * Noise-driven floating particle field
 * Creates organic, film-like dust/bokeh particles
 */
export const ParticleField: React.FC<{
  count?: number;
  color?: string;
  minSize?: number;
  maxSize?: number;
  speed?: number;
  opacity?: number;
}> = ({ count = 60, color = '#ffffff', minSize = 1, maxSize = 4, speed = 0.015, opacity = 0.15 }) => {
  const frame = useCurrentFrame();

  const particles = React.useMemo(() => {
    const p = [];
    for (let i = 0; i < count; i++) {
      const seed = i * 7919;
      p.push({
        baseX: (seed * 13) % 1920,
        baseY: (seed * 17) % 1080,
        size: minSize + (seed % 100) / 100 * (maxSize - minSize),
        phase: (seed % 628) / 100,
        depth: 0.3 + (seed % 70) / 100,
      });
    }
    return p;
  }, [count, minSize, maxSize]);

  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      {particles.map((p, i) => {
        const x = p.baseX + noise2D('px', frame * speed, i) * 40 * p.depth;
        const y = p.baseY + noise2D('py', i, frame * speed) * 30 * p.depth;
        const o = opacity * p.depth * (0.5 + 0.5 * Math.sin(frame * 0.03 + p.phase));
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: x,
              top: y,
              width: p.size,
              height: p.size,
              borderRadius: '50%',
              backgroundColor: color,
              opacity: o,
              filter: p.size > 2.5 ? 'blur(1px)' : 'none',
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};
