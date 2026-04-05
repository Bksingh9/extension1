import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from 'remotion';
import { CartoonBg } from '../components/CartoonBg';
import { BigCaption } from '../components/BigCaption';
import { Character } from '../components/Character';
import { SpeechBubble } from '../components/SpeechBubble';
import { C, CFONT } from '../theme';

const reveals = [
  { official: 'Spreading democracy', hidden: 'Securing resources', icon: '🏛️' },
  { official: 'Humanitarian aid', hidden: 'Strategic influence', icon: '🤝' },
  { official: 'Free trade agreements', hidden: 'Economic dependence', icon: '📜' },
  { official: 'National security', hidden: 'Mass surveillance', icon: '🛡️' },
];

export const Scene5_WhatTheyDontTell: React.FC = () => {
  const frame = useCurrentFrame();
  const fadeIn = interpolate(frame, [0, 12], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const fadeOut = interpolate(frame, [165, 180], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ opacity: Math.min(fadeIn, fadeOut) }}>
      <CartoonBg color="#0d0619" />

      <div style={{ position: 'absolute', top: 25, left: 0, right: 0 }}>
        <BigCaption text="What They Don't Tell You" delay={5} color={C.danger} fontSize={48} />
      </div>

      {/* Two-column reveal */}
      <div
        style={{
          position: 'absolute',
          top: 140,
          left: 120,
          right: 120,
        }}
      >
        {/* Headers */}
        <div style={{ display: 'flex', marginBottom: 16 }}>
          <div style={{ flex: 1, textAlign: 'center' }}>
            <div
              style={{
                fontSize: 20,
                fontFamily: CFONT.title,
                color: C.charBlue,
                letterSpacing: '0.06em',
                opacity: interpolate(frame, [15, 25], [0, 1], {
                  extrapolateLeft: 'clamp',
                  extrapolateRight: 'clamp',
                }),
              }}
            >
              WHAT THEY SAY
            </div>
          </div>
          <div style={{ width: 80 }} />
          <div style={{ flex: 1, textAlign: 'center' }}>
            <div
              style={{
                fontSize: 20,
                fontFamily: CFONT.title,
                color: C.danger,
                letterSpacing: '0.06em',
                opacity: interpolate(frame, [15, 25], [0, 1], {
                  extrapolateLeft: 'clamp',
                  extrapolateRight: 'clamp',
                }),
              }}
            >
              WHAT REALLY HAPPENS
            </div>
          </div>
        </div>

        {/* Rows */}
        {reveals.map((r, i) => {
          const d = 25 + i * 24;
          const leftOp = interpolate(frame, [d, d + 10], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });
          const rightOp = interpolate(frame, [d + 12, d + 22], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });
          const arrowOp = interpolate(frame, [d + 8, d + 15], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });

          return (
            <div key={i} style={{ display: 'flex', alignItems: 'center', marginBottom: 14 }}>
              {/* Official story */}
              <div
                style={{
                  opacity: leftOp,
                  flex: 1,
                  padding: '14px 20px',
                  backgroundColor: `${C.charBlue}18`,
                  border: `2px solid ${C.charBlue}44`,
                  borderRadius: 12,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 12,
                }}
              >
                <span style={{ fontSize: 28 }}>{r.icon}</span>
                <span style={{ fontSize: 18, fontFamily: CFONT.body, fontWeight: 700, color: C.textWhite }}>
                  "{r.official}"
                </span>
              </div>

              {/* Arrow */}
              <div
                style={{
                  width: 80,
                  textAlign: 'center',
                  fontSize: 28,
                  color: C.glow,
                  opacity: arrowOp,
                }}
              >
                →
              </div>

              {/* Hidden truth */}
              <div
                style={{
                  opacity: rightOp,
                  flex: 1,
                  padding: '14px 20px',
                  backgroundColor: `${C.danger}18`,
                  border: `2px solid ${C.danger}44`,
                  borderRadius: 12,
                }}
              >
                <span style={{ fontSize: 18, fontFamily: CFONT.body, fontWeight: 700, color: C.danger }}>
                  {r.hidden}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Character */}
      <Character color={C.charOrange} x={850} y={730} size={0.65} delay={100} expression="shocked" accessory="glasses" />

      <SpeechBubble
        text="The narrative is always curated."
        x={700}
        y={560}
        delay={120}
        width={280}
        variant="thought"
      />

      <div
        style={{
          position: 'absolute',
          bottom: 35,
          left: 0,
          right: 0,
          textAlign: 'center',
          opacity: interpolate(frame, [140, 158], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        <div style={{ fontSize: 22, fontFamily: CFONT.title, color: C.glow, letterSpacing: '0.06em' }}>
          QUESTION EVERYTHING. RESEARCH EVERYTHING.
        </div>
      </div>
    </AbsoluteFill>
  );
};
