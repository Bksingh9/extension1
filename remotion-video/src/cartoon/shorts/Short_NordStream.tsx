import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { ShortHook, ShortFact, ShortCTA } from './ShortTemplate';
import { CartoonBg } from '../components/CartoonBg';
import { C } from '../theme';

export const Short_NordStream: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#060310' }}>
    <Sequence from={0} durationInFrames={90}>
      <ShortHook text="Who Blew Up Nord Stream?" subtext="$18 billion destroyed. Nobody charged." color={C.charOrange} />
    </Sequence>

    <Sequence from={90} durationInFrames={1260}>
      <AbsoluteFill>
        <CartoonBg color="#0a0618" accentColor={C.charOrange} showGrid />
        <div style={{ padding: '80px 50px', display: 'flex', flexDirection: 'column', justifyContent: 'center', height: '100%' }}>
          <ShortFact year="2011" text="Nord Stream 1: $7.4B pipe under the Baltic" detail="Europe's addiction to cheap Russian gas: priceless." color={C.charBlue} icon="🔵" delay={0} />
          <ShortFact year="2021" text="Nord Stream 2: $11B. Never turned on." detail={"Germany \"suspended\" it. Most expensive paperweight ever."} color={C.charOrange} icon="🔴" delay={150} />
          <ShortFact year="SEP 22" text="3 of 4 pipelines EXPLODE" detail="Sabotage confirmed. US denies. Russia denies. Everyone sus." color={C.danger} icon="💣" delay={330} />
          <ShortFact text="Before: EU got 40-45% of gas from Russia" detail={"Germany: 55%. \"Energy dependency? Nah, partnership!\" 🤡"} color={C.charPurple} icon="🇪🇺" delay={510} />
          <ShortFact text="After: Russian gas dropped 80%" detail="Now buying expensive US LNG. Freedom gas isn't free." color={C.charGreen} icon="📉" delay={690} />
          <ShortFact text="Russia pivoted East. Made new friends." detail={"The West: \"We'll isolate them!\" Russia: *joins BRICS* \"K.\""} color={C.mystery} icon="🤝" delay={870} />
        </div>
      </AbsoluteFill>
    </Sequence>

    <Sequence from={1350} durationInFrames={360}>
      <ShortCTA delay={5} />
    </Sequence>
  </AbsoluteFill>
);
