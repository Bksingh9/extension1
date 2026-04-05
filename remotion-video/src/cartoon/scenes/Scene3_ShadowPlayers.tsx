import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate, Easing } from 'remotion';
import { CartoonBg } from '../components/CartoonBg';
import { Character } from '../components/Character';
import { SpeechBubble } from '../components/SpeechBubble';
import { BigCaption } from '../components/BigCaption';
import { C, CFONT } from '../theme';

const shadowGroups = [
  { name: 'Think Tanks', desc: 'Write the policies that politicians sign', color: C.charPurple },
  { name: 'Defense Contractors', desc: 'Profit when conflicts escalate', color: C.danger },
  { name: 'Tech Giants', desc: 'Control the information pipeline', color: C.charBlue },
  { name: 'Energy Cartels', desc: 'Decide which economies rise or fall', color: C.charGold },
];

export const Scene3_ShadowPlayers: React.FC = () => {
  const frame = useCurrentFrame();
  const fadeIn = interpolate(frame, [0, 12], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const fadeOut = interpolate(frame, [195, 210], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ opacity: Math.min(fadeIn, fadeOut) }}>
      <CartoonBg color="#0f0820" />

      <div style={{ position: 'absolute', top: 30, left: 0, right: 0 }}>
        <BigCaption text="The Shadow Players" delay={5} color={C.mystery} fontSize={52} sub="The ones you never elected." />
      </div>

      {/* Shadow figure silhouettes behind a curtain effect */}
      <div
        style={{
          position: 'absolute',
          top: 160,
          left: 100,
          right: 100,
          display: 'flex',
          gap: 24,
          justifyContent: 'center',
        }}
      >
        {shadowGroups.map((group, i) => {
          const d = 20 + i * 18;
          const op = interpolate(frame, [d, d + 15], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });
          const y = interpolate(frame, [d, d + 18], [30, 0], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
            easing: Easing.out(Easing.cubic),
          });
          const glow = Math.sin((frame - d) * 0.06) * 0.3 + 0.7;

          return (
            <div
              key={i}
              style={{
                opacity: op,
                transform: `translateY(${y}px)`,
                width: 360,
                padding: '28px 24px',
                backgroundColor: `${group.color}12`,
                border: `3px solid ${group.color}55`,
                borderRadius: 16,
                textAlign: 'center',
                position: 'relative',
                overflow: 'hidden',
              }}
            >
              {/* Glow pulse */}
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  background: `radial-gradient(circle at center, ${group.color}15 0%, transparent 70%)`,
                  opacity: glow,
                }}
              />
              {/* Icon placeholder -- question mark */}
              <div
                style={{
                  fontSize: 48,
                  color: group.color,
                  marginBottom: 12,
                  textShadow: `0 0 20px ${group.color}66`,
                }}
              >
                ?
              </div>
              <div
                style={{
                  fontSize: 22,
                  fontFamily: CFONT.title,
                  color: group.color,
                  letterSpacing: '0.04em',
                  marginBottom: 8,
                }}
              >
                {group.name}
              </div>
              <div
                style={{
                  fontSize: 15,
                  fontFamily: CFONT.body,
                  color: C.textLight,
                  lineHeight: 1.4,
                }}
              >
                {group.desc}
              </div>
            </div>
          );
        })}
      </div>

      {/* Characters */}
      <Character color="#444" x={200} y={720} size={0.65} delay={80} expression="suspicious" accessory="hat" />
      <Character color="#444" x={1400} y={720} size={0.65} delay={90} expression="suspicious" accessory="glasses" flip />

      <SpeechBubble text="They fund both sides of every conflict." x={600} y={560} delay={110} width={320} variant="shout" />

      {/* Bottom quote */}
      <div
        style={{
          position: 'absolute',
          bottom: 40,
          left: 0,
          right: 0,
          textAlign: 'center',
          opacity: interpolate(frame, [150, 170], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        <div style={{ fontSize: 18, fontFamily: CFONT.caption, fontStyle: 'italic', color: C.textLight }}>
          "The real power doesn't need your vote."
        </div>
      </div>
    </AbsoluteFill>
  );
};
