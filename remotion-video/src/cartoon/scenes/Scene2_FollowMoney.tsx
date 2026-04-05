import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from 'remotion';
import { CartoonBg } from '../components/CartoonBg';
import { Character } from '../components/Character';
import { SpeechBubble } from '../components/SpeechBubble';
import { BigCaption } from '../components/BigCaption';
import { C, CFONT } from '../theme';

const moneyTrails = [
  { from: 'Central Banks', to: 'Governments', amount: '$13T', color: C.charGold },
  { from: 'Governments', to: 'Military', amount: '$2.2T', color: C.danger },
  { from: 'Corporations', to: 'Politicians', amount: '$4.1B', color: C.charPurple },
  { from: 'Offshore', to: '???', amount: '$36T', color: C.mystery },
];

export const Scene2_FollowMoney: React.FC = () => {
  const frame = useCurrentFrame();
  const fadeIn = interpolate(frame, [0, 12], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const fadeOut = interpolate(frame, [225, 240], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ opacity: Math.min(fadeIn, fadeOut) }}>
      <CartoonBg color="#1a0f25" showStars={false} />

      <div style={{ position: 'absolute', top: 30, left: 0, right: 0 }}>
        <BigCaption text="Follow The Money" delay={5} color={C.glow} fontSize={52} sub="Where does it all really go?" />
      </div>

      {/* Money flow diagram */}
      <div
        style={{
          position: 'absolute',
          top: 180,
          left: 120,
          right: 120,
          display: 'flex',
          flexDirection: 'column',
          gap: 20,
        }}
      >
        {moneyTrails.map((trail, i) => {
          const d = 30 + i * 25;
          const op = interpolate(frame, [d, d + 15], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });
          const barW = interpolate(frame, [d + 10, d + 35], [0, 100], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.out(Easing.cubic),
          });

          return (
            <div key={i} style={{ opacity: op, display: 'flex', alignItems: 'center', gap: 16 }}>
              {/* From */}
              <div
                style={{
                  width: 180,
                  padding: '10px 16px',
                  backgroundColor: C.bgPanel,
                  border: `2px solid ${trail.color}66`,
                  borderRadius: 10,
                  fontSize: 17,
                  fontFamily: CFONT.body,
                  fontWeight: 700,
                  color: C.textWhite,
                  textAlign: 'center',
                }}
              >
                {trail.from}
              </div>

              {/* Arrow bar */}
              <div style={{ flex: 1, position: 'relative', height: 30 }}>
                <div
                  style={{
                    width: `${barW}%`,
                    height: 8,
                    backgroundColor: trail.color,
                    borderRadius: 4,
                    position: 'absolute',
                    top: 11,
                    left: 0,
                    boxShadow: `0 0 12px ${trail.color}44`,
                  }}
                />
                {/* Amount label */}
                <div
                  style={{
                    position: 'absolute',
                    top: -4,
                    left: `${barW / 2}%`,
                    transform: 'translateX(-50%)',
                    fontSize: 22,
                    fontFamily: CFONT.title,
                    fontWeight: 800,
                    color: trail.color,
                    textShadow: `0 0 8px ${trail.color}66`,
                    opacity: barW > 50 ? 1 : 0,
                  }}
                >
                  {trail.amount}
                </div>
              </div>

              {/* To */}
              <div
                style={{
                  width: 180,
                  padding: '10px 16px',
                  backgroundColor: trail.to === '???' ? C.mystery + '33' : C.bgPanel,
                  border: `2px solid ${trail.to === '???' ? C.mystery : trail.color}66`,
                  borderRadius: 10,
                  fontSize: 17,
                  fontFamily: CFONT.body,
                  fontWeight: 700,
                  color: trail.to === '???' ? C.mystery : C.textWhite,
                  textAlign: 'center',
                }}
              >
                {trail.to}
              </div>
            </div>
          );
        })}
      </div>

      {/* Characters reacting */}
      <Character color={C.charBlue} x={150} y={680} size={0.7} delay={80} expression="suspicious" accessory="tie" />
      <Character color={C.charOrange} x={1500} y={680} size={0.7} delay={90} expression="happy" accessory="crown" flip />

      <SpeechBubble text="$36 trillion offshore... and nobody asks where?" x={700} y={530} delay={140} width={340} variant="thought" />

      {/* Mystery question */}
      <div
        style={{
          position: 'absolute',
          bottom: 50,
          left: 0,
          right: 0,
          textAlign: 'center',
          opacity: interpolate(frame, [170, 190], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        <div style={{ fontSize: 28, fontFamily: CFONT.title, color: C.glow, letterSpacing: '0.06em' }}>
          WHO CONTROLS THE MONEY CONTROLS THE GAME
        </div>
      </div>
    </AbsoluteFill>
  );
};
