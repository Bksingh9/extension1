import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { ShortHook, ShortFact, ShortCTA } from './ShortTemplate';
import { CartoonBg } from '../components/CartoonBg';
import { C } from '../theme';

export const Short_BRICS: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#060310' }}>
    <Sequence from={0} durationInFrames={90}>
      <ShortHook text="The Anti-Dollar Group Chat" subtext="BRICS is building a new world order." color={C.charGold} />
    </Sequence>

    <Sequence from={90} durationInFrames={1260}>
      <AbsoluteFill>
        <CartoonBg color="#0a0618" accentColor={C.charGold} showGrid />
        <div style={{ padding: '80px 50px', display: 'flex', flexDirection: 'column', justifyContent: 'center', height: '100%' }}>
          <ShortFact year="2006" text="BRIC formed — named by Goldman Sachs" detail="Wall Street named the club that wants to destroy Wall Street." color={C.charGold} icon="🤝" delay={0} />
          <ShortFact text="40% of world population. 26% of GDP." detail={"The \"global minority\" is actually the majority."} color={C.charGreen} icon="🌍" delay={150} />
          <ShortFact year="2014" text="They made their own World Bank" detail="In Shanghai. $50B capital. No strings attached." color={C.charBlue} icon="🏦" delay={330} />
          <ShortFact year="2024" text="Saudi, Iran, UAE, Egypt, Ethiopia join" detail="The cool kids table just got very crowded." color={C.charOrange} icon="📢" delay={510} />
          <ShortFact text="Central banks buying gold at RECORD rates" detail="1,136 tonnes in 2022. Like doomsday preppers with PhDs." color={C.charGold} icon="🥇" delay={690} />
          <ShortFact text="China dumped $525B in US Treasuries" detail="$1.3T → $775B. That's not diversification. That's a message." color={C.charRed} icon="📉" delay={870} />
        </div>
      </AbsoluteFill>
    </Sequence>

    <Sequence from={1350} durationInFrames={360}>
      <ShortCTA delay={5} />
    </Sequence>
  </AbsoluteFill>
);
