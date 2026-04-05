import React from 'react';
import { useCurrentFrame, interpolate, Easing } from 'remotion';
import { C } from '../theme';

/**
 * Simplified stylized world map using SVG paths
 * Shows major landmasses as recognizable cartoon shapes
 */
export const WorldMap: React.FC<{
  delay?: number;
  highlights?: { x: number; y: number; label: string; color: string }[];
  connections?: { x1: number; y1: number; x2: number; y2: number; color: string }[];
}> = ({ delay = 0, highlights = [], connections = [] }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [delay, delay + 20], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%', opacity }}>
      <svg viewBox="0 0 1000 500" style={{ width: '100%', height: '100%' }}>
        {/* Ocean background */}
        <rect width="1000" height="500" fill={C.mapOcean} rx="12" />

        {/* Simplified continents */}
        {/* North America */}
        <path
          d="M150,80 L200,70 L250,80 L280,120 L270,180 L240,200 L200,220 L160,190 L140,150 L130,120 Z"
          fill={C.mapLand}
          stroke={C.outlineLight}
          strokeWidth="1.5"
        />
        {/* South America */}
        <path
          d="M220,240 L260,230 L280,270 L290,320 L270,380 L240,400 L210,370 L200,310 L210,270 Z"
          fill={C.mapLand}
          stroke={C.outlineLight}
          strokeWidth="1.5"
        />
        {/* Europe */}
        <path
          d="M440,80 L480,70 L520,80 L530,110 L510,140 L480,150 L450,140 L430,110 Z"
          fill={C.mapLand}
          stroke={C.outlineLight}
          strokeWidth="1.5"
        />
        {/* Africa */}
        <path
          d="M450,170 L500,160 L530,190 L540,260 L520,340 L480,370 L440,340 L430,270 L440,210 Z"
          fill={C.mapLand}
          stroke={C.outlineLight}
          strokeWidth="1.5"
        />
        {/* Asia */}
        <path
          d="M550,60 L650,50 L750,70 L800,110 L780,160 L730,190 L660,180 L600,170 L560,140 L540,100 Z"
          fill={C.mapLand}
          stroke={C.outlineLight}
          strokeWidth="1.5"
        />
        {/* Russia extension */}
        <path
          d="M530,50 L550,40 L700,35 L800,45 L820,60 L800,70 L650,50 L550,60 Z"
          fill={C.mapLand}
          stroke={C.outlineLight}
          strokeWidth="1.5"
        />
        {/* Australia */}
        <path
          d="M760,310 L820,300 L850,330 L840,370 L800,380 L770,360 L750,340 Z"
          fill={C.mapLand}
          stroke={C.outlineLight}
          strokeWidth="1.5"
        />

        {/* Animated connection lines */}
        {connections.map((conn, i) => {
          const lineDelay = delay + 20 + i * 12;
          const dashOffset = interpolate(frame, [lineDelay, lineDelay + 30], [200, 0], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.out(Easing.cubic),
          });
          return (
            <line
              key={`c-${i}`}
              x1={conn.x1}
              y1={conn.y1}
              x2={conn.x2}
              y2={conn.y2}
              stroke={conn.color}
              strokeWidth="2.5"
              strokeDasharray="8 4"
              strokeDashoffset={dashOffset}
              opacity={0.8}
            />
          );
        })}

        {/* Highlight points */}
        {highlights.map((h, i) => {
          const pDelay = delay + 15 + i * 8;
          const pScale = interpolate(frame, [pDelay, pDelay + 12], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });
          const pulse = 1 + Math.sin((frame - pDelay) * 0.1) * 0.15;
          return (
            <g key={`h-${i}`} transform={`translate(${h.x}, ${h.y}) scale(${pScale * pulse})`}>
              <circle r="14" fill={h.color} opacity="0.3" />
              <circle r="8" fill={h.color} stroke="#fff" strokeWidth="2" />
              <text
                y="28"
                textAnchor="middle"
                fill="#fff"
                fontSize="13"
                fontWeight="bold"
                fontFamily="Impact, sans-serif"
              >
                {h.label}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};
