import React from 'react';
import { useCurrentFrame, interpolate, Easing } from 'remotion';
import { C, CFONT } from '../theme';

export const ComicPanel: React.FC<{
  children: React.ReactNode;
  title?: string;
  delay?: number;
  borderColor?: string;
}> = ({ children, title, delay = 0, borderColor = C.outline }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [delay, delay + 12], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const scale = interpolate(frame, [delay, delay + 15], [0.92, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  return (
    <div
      style={{
        opacity,
        transform: `scale(${scale})`,
        position: 'relative',
        width: '100%',
        height: '100%',
        border: `4px solid ${borderColor}`,
        borderRadius: 12,
        overflow: 'hidden',
        boxShadow: '6px 6px 0px rgba(0,0,0,0.3)',
      }}
    >
      {children}
      {title && (
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            padding: '8px 16px',
            background: `linear-gradient(180deg, ${C.captionBg}, transparent)`,
          }}
        >
          <div
            style={{
              fontSize: 16,
              fontFamily: CFONT.caption,
              fontStyle: 'italic',
              color: C.textLight,
              textAlign: 'center',
            }}
          >
            {title}
          </div>
        </div>
      )}
    </div>
  );
};
