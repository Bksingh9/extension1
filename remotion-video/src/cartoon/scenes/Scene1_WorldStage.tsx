import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from 'remotion';
import { CartoonBg } from '../components/CartoonBg';
import { WorldMap } from '../components/WorldMap';
import { Character } from '../components/Character';
import { SpeechBubble } from '../components/SpeechBubble';
import { BigCaption } from '../components/BigCaption';
import { C } from '../theme';

export const Scene1_WorldStage: React.FC = () => {
  const frame = useCurrentFrame();

  const fadeIn = interpolate(frame, [0, 12], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const fadeOut = interpolate(frame, [195, 210], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ opacity: Math.min(fadeIn, fadeOut) }}>
      <CartoonBg color={C.bgMap} />

      {/* Map in background */}
      <div style={{ position: 'absolute', inset: '80px 60px 120px 60px', opacity: 0.4 }}>
        <WorldMap
          delay={5}
          highlights={[
            { x: 200, y: 130, label: 'USA', color: C.charBlue },
            { x: 480, y: 110, label: 'EU', color: C.charGold },
            { x: 700, y: 100, label: 'CHINA', color: C.charRed },
            { x: 650, y: 170, label: 'INDIA', color: C.charGreen },
            { x: 560, y: 140, label: 'RUSSIA', color: C.charPurple },
          ]}
          connections={[
            { x1: 200, y1: 130, x2: 480, y2: 110, color: C.mapLine },
            { x1: 480, y1: 110, x2: 700, y2: 100, color: C.mapLine },
            { x1: 700, y1: 100, x2: 200, y2: 130, color: C.danger },
          ]}
        />
      </div>

      {/* Characters representing nations */}
      <Character color={C.charBlue} x={200} y={700} size={0.9} delay={20} expression="suspicious" accessory="tie" />
      <Character color={C.charRed} x={700} y={700} size={0.9} delay={30} expression="angry" accessory="hat" flip />
      <Character color={C.charGold} x={450} y={720} size={0.8} delay={40} expression="neutral" accessory="glasses" />
      <Character color={C.charPurple} x={1050} y={710} size={0.85} delay={50} expression="suspicious" accessory="hat" />
      <Character color={C.charGreen} x={1350} y={710} size={0.85} delay={55} expression="happy" accessory="crown" />

      {/* Speech bubbles */}
      <SpeechBubble text="We set the rules." x={120} y={420} delay={60} width={220} tailDirection="right" />
      <SpeechBubble text="We're rewriting them." x={620} y={410} delay={80} width={240} tailDirection="left" variant="shout" />

      {/* Caption */}
      <div style={{ position: 'absolute', top: 30, left: 0, right: 0 }}>
        <BigCaption text="The World Stage" delay={5} color={C.textAccent} fontSize={48} sub="Five powers. One chessboard. Zero trust." />
      </div>

      {/* Bottom bar */}
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          height: 50,
          backgroundColor: C.captionBg,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          opacity: interpolate(frame, [100, 115], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        <div style={{ fontSize: 18, fontFamily: 'Georgia, serif', fontStyle: 'italic', color: C.textLight }}>
          "In geo-politics, there are no friends — only interests."
        </div>
      </div>
    </AbsoluteFill>
  );
};
