import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from 'remotion';
import { CartoonBg } from '../components/CartoonBg';
import { BigCaption } from '../components/BigCaption';
import { C, CFONT } from '../theme';

const dominoes = [
  { label: 'Trade War', color: C.charRed, icon: '⚔️' },
  { label: 'Currency Crash', color: C.charGold, icon: '📉' },
  { label: 'Energy Crisis', color: C.charOrange, icon: '⛽' },
  { label: 'Food Shortage', color: C.charGreen, icon: '🌾' },
  { label: 'Social Unrest', color: C.danger, icon: '🔥' },
  { label: 'New World Order?', color: C.mystery, icon: '🌐' },
];

export const Scene4_DominoEffect: React.FC = () => {
  const frame = useCurrentFrame();
  const fadeIn = interpolate(frame, [0, 12], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const fadeOut = interpolate(frame, [195, 210], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ opacity: Math.min(fadeIn, fadeOut) }}>
      <CartoonBg color="#15091f" />

      <div style={{ position: 'absolute', top: 30, left: 0, right: 0 }}>
        <BigCaption text="The Domino Effect" delay={5} color={C.danger} fontSize={52} sub="One event triggers a chain reaction." />
      </div>

      {/* Domino chain */}
      <div
        style={{
          position: 'absolute',
          top: 200,
          left: 80,
          right: 80,
          display: 'flex',
          alignItems: 'flex-end',
          justifyContent: 'center',
          gap: 20,
        }}
      >
        {dominoes.map((d, i) => {
          const delay = 25 + i * 20;
          const tilt = interpolate(frame, [delay, delay + 15], [0, 15 + i * 3], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.in(Easing.cubic),
          });
          const op = interpolate(frame, [delay - 10, delay], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });
          const isFalling = frame >= delay;
          const isLast = i === dominoes.length - 1;

          return (
            <div
              key={i}
              style={{
                opacity: op,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: 8,
              }}
            >
              {/* Arrow connecting dominoes */}
              {i > 0 && (
                <div
                  style={{
                    position: 'absolute',
                    left: 80 + i * (230 + 20) - 25,
                    top: 340,
                    fontSize: 24,
                    color: C.glow,
                    opacity: isFalling ? 1 : 0.3,
                  }}
                >
                  →
                </div>
              )}

              {/* Domino piece */}
              <div
                style={{
                  width: 200,
                  height: 300,
                  backgroundColor: C.bgPanel,
                  border: `3px solid ${d.color}`,
                  borderRadius: 12,
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: 12,
                  transform: `rotate(${isFalling ? tilt : 0}deg)`,
                  transformOrigin: 'bottom center',
                  boxShadow: isFalling
                    ? `0 0 20px ${d.color}44, 4px 4px 0px rgba(0,0,0,0.3)`
                    : '4px 4px 0px rgba(0,0,0,0.3)',
                }}
              >
                <div style={{ fontSize: 42 }}>{d.icon}</div>
                <div
                  style={{
                    fontSize: 18,
                    fontFamily: CFONT.title,
                    color: d.color,
                    textAlign: 'center',
                    letterSpacing: '0.03em',
                    padding: '0 8px',
                  }}
                >
                  {d.label}
                </div>
                {isLast && (
                  <div
                    style={{
                      fontSize: 28,
                      color: C.mystery,
                      opacity: interpolate(frame, [delay + 15, delay + 30], [0, 1], {
                        extrapolateLeft: 'clamp',
                        extrapolateRight: 'clamp',
                      }),
                    }}
                  >
                    ?
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Bottom quote */}
      <div
        style={{
          position: 'absolute',
          bottom: 40,
          left: 0,
          right: 0,
          textAlign: 'center',
          opacity: interpolate(frame, [160, 180], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        <div style={{ fontSize: 26, fontFamily: CFONT.title, color: C.glow, letterSpacing: '0.06em' }}>
          EVERY CRISIS IS CONNECTED
        </div>
      </div>
    </AbsoluteFill>
  );
};
