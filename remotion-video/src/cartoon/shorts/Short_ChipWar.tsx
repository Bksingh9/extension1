import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { ShortHook, ShortFact, ShortCTA } from './ShortTemplate';
import { CartoonBg } from '../components/CartoonBg';
import { C } from '../theme';

export const Short_ChipWar: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#060310' }}>
    <Sequence from={0} durationInFrames={90}>
      <ShortHook text="One Island Makes 90% of ALL Chips" subtext="And two superpowers want to control it." color={C.charBlue} />
    </Sequence>

    <Sequence from={90} durationInFrames={1260}>
      <AbsoluteFill>
        <CartoonBg color="#080418" accentColor={C.charBlue} showGrid />
        <div style={{ padding: '80px 50px', display: 'flex', flexDirection: 'column', justifyContent: 'center', height: '100%' }}>
          <ShortFact text="TSMC in Taiwan makes 90% of advanced chips" detail="Every phone, laptop, missile, and AI you use." color={C.danger} icon="🇹🇼" delay={0} />
          <ShortFact year="2019" text="US bans Huawei from all American tech" detail="Translation: they were about to beat us at 5G." color={C.charBlue} icon="🚫" delay={120} />
          <ShortFact year="2022" text="CHIPS Act: $52.7B taxpayer money" detail="Corporate welfare is fine when you call it national security." color={C.charGold} icon="🏭" delay={300} />
          <ShortFact year="2023" text="Huawei builds 7nm chip ANYWAY" detail={"Analysts: \"Impossible!\" Huawei: \"Hold my baijiu.\" 🍶"} color={C.charRed} icon="🔥" delay={480} />
          <ShortFact text="China owns 60% of rare earths, processes 90%" detail="Awkward when your rival makes your weapons." color={C.charRed} icon="⛏️" delay={660} />
          <ShortFact text="$500B in annual trade. Can't break up." detail="It's complicated. Very, very complicated." color={C.charOrange} icon="💔" delay={840} />
        </div>
      </AbsoluteFill>
    </Sequence>

    <Sequence from={1350} durationInFrames={360}>
      <ShortCTA delay={5} />
    </Sequence>
  </AbsoluteFill>
);
