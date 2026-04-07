import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { noise2D } from '@remotion/noise';
import { C } from '../theme';
import { ParticleField } from './ParticleField';

/**
 * Production-grade layered background
 * - Animated gradient base with hue shift
 * - 3-layer parallax star field (150 stars)
 * - Noise-driven grain overlay
 * - Particle dust field
 * - Tinted vignette
 * - Subtle animated grid lines
 */
export const CartoonBg: React.FC<{
  color?: string;
  showStars?: boolean;
  accentColor?: string;
  showGrid?: boolean;
  particleColor?: string;
  particleCount?: number;
}> = ({
  color = C.bgDark,
  showStars = true,
  accentColor = C.charBlue,
  showGrid = false,
  particleColor = '#ffffff',
  particleCount = 50,
}) => {
  const frame = useCurrentFrame();

  // Subtle hue shift on background
  const hueShift = Math.sin(frame * 0.008) * 5;

  // Stars in 3 depth layers
  const stars = React.useMemo(() => {
    const layers: Array<{ x: number; y: number; size: number; phase: number; layer: number }[]> = [[], [], []];
    for (let i = 0; i < 150; i++) {
      const seed = i * 7919;
      const layer = i % 3;
      layers[layer].push({
        x: (seed * 13) % 1920,
        y: (seed * 17) % 1080,
        size: layer === 0 ? 1 : layer === 1 ? 1.8 : 2.8,
        phase: (seed % 628) / 100,
        layer,
      });
    }
    return layers;
  }, []);

  return (
    <AbsoluteFill>
      {/* Base gradient layer with animated hue */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: `linear-gradient(${170 + hueShift}deg, ${color} 0%, ${C.bgMap} 50%, ${color} 100%)`,
        }}
      />

      {/* Accent glow in center */}
      <div
        style={{
          position: 'absolute',
          left: '50%',
          top: '40%',
          width: 900,
          height: 900,
          transform: 'translate(-50%, -50%)',
          borderRadius: '50%',
          background: `radial-gradient(circle, ${accentColor}08 0%, transparent 70%)`,
          filter: 'blur(40px)',
        }}
      />

      {/* Parallax star layers */}
      {showStars && stars.map((layer, li) => {
        const parallaxOffset = frame * (li === 0 ? 0.02 : li === 1 ? 0.05 : 0.1);
        return (
          <AbsoluteFill key={li} style={{ transform: `translateY(${parallaxOffset}px)`, pointerEvents: 'none' }}>
            {layer.map((star, si) => (
              <div
                key={si}
                style={{
                  position: 'absolute',
                  left: star.x,
                  top: star.y,
                  width: star.size,
                  height: star.size,
                  borderRadius: '50%',
                  backgroundColor: li === 2 ? accentColor : '#fff',
                  opacity: (li === 0 ? 0.2 : li === 1 ? 0.35 : 0.5)
                    * (0.5 + 0.5 * Math.sin(frame * 0.04 + star.phase)),
                  boxShadow: li === 2 ? `0 0 4px ${accentColor}44` : 'none',
                }}
              />
            ))}
          </AbsoluteFill>
        );
      })}

      {/* Animated grid */}
      {showGrid && (
        <div
          style={{
            position: 'absolute',
            inset: 0,
            backgroundImage: `
              linear-gradient(${accentColor}06 1px, transparent 1px),
              linear-gradient(90deg, ${accentColor}06 1px, transparent 1px)
            `,
            backgroundSize: '80px 80px',
            opacity: 0.4 + 0.1 * Math.sin(frame * 0.02),
          }}
        />
      )}

      {/* Film grain via noise */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundImage:
            'radial-gradient(circle, rgba(255,255,255,0.025) 1px, transparent 1px)',
          backgroundSize: '8px 8px',
          opacity: 0.6,
          mixBlendMode: 'overlay',
        }}
      />

      {/* Floating particles */}
      <ParticleField count={particleCount} color={particleColor} opacity={0.12} speed={0.012} />

      {/* Tinted vignette */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: `radial-gradient(ellipse at center, transparent 40%, ${color}cc 100%)`,
        }}
      />
    </AbsoluteFill>
  );
};
