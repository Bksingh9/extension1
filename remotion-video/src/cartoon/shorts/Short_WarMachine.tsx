import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { ShortHook, ShortFact, ShortCTA } from './ShortTemplate';
import { CartoonBg } from '../components/CartoonBg';
import { C } from '../theme';

export const Short_WarMachine: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#060310' }}>
    <Sequence from={0} durationInFrames={90}>
      <ShortHook text="$886 Billion Per Year" subtext="Somebody's making a killing. Literally." color={C.danger} />
    </Sequence>

    <Sequence from={90} durationInFrames={1260}>
      <AbsoluteFill>
        <CartoonBg color="#0a0618" accentColor={C.danger} showGrid />
        <div style={{ padding: '80px 50px', display: 'flex', flexDirection: 'column', justifyContent: 'center', height: '100%' }}>
          <ShortFact text="US: more than the next 10 countries combined" detail="$886B in 2023. For 'defense.' Sure." color={C.charBlue} icon="🇺🇸" delay={0} />
          <ShortFact text="F-35: $1.7 TRILLION lifetime cost" detail="A plane with software bugs. Agile development, military edition." color={C.danger} icon="💸" delay={150} />
          <ShortFact text="750+ military bases in 80+ countries" detail="That's not defense. That's a franchise." color={C.mystery} icon="🗺️" delay={330} />
          <ShortFact year="2001-21" text="Afghanistan: $2.3T. Taliban still in charge." detail="20 years. They waited it out with flip phones." color={C.danger} icon="🇦🇫" delay={510} />
          <ShortFact text="$8+ TRILLION on post-9/11 wars. 900K dead." detail="Brown University did the math. Pentagon didn't want them to." color={C.danger} icon="💀" delay={690} />
          <ShortFact text="1,700 Pentagon officials → arms companies" detail="Approve weapons. Retire. Sell weapons. Nice gig." color={C.mystery} icon="🚪" delay={870} />
        </div>
      </AbsoluteFill>
    </Sequence>

    <Sequence from={1350} durationInFrames={360}>
      <ShortCTA delay={5} />
    </Sequence>
  </AbsoluteFill>
);
