import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { ShortHook, ShortFact, ShortCTA } from './ShortTemplate';
import { CartoonBg } from '../components/CartoonBg';
import { C } from '../theme';

export const Short_Oil: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#060310' }}>
    <Sequence from={0} durationInFrames={90}>
      <ShortHook text="Oil Went NEGATIVE" subtext="They literally paid you to take it." color={C.warning} />
    </Sequence>

    <Sequence from={90} durationInFrames={1260}>
      <AbsoluteFill>
        <CartoonBg color="#0a0618" accentColor={C.charOrange} showGrid />
        <div style={{ padding: '80px 50px', display: 'flex', flexDirection: 'column', justifyContent: 'center', height: '100%' }}>
          <ShortFact year="APR 20" text="-$37.63 per barrel" detail="Storage was full. Traders crying. Beautiful chaos." color={C.danger} icon="📉" delay={0} />
          <ShortFact year="JUN 22" text="$120/barrel. OPEC pops champagne." detail="Your gas bill tripled. Their yacht collection doubled." color={C.charGold} icon="📈" delay={150} />
          <ShortFact year="OCT 22" text="OPEC+ cuts 2M barrels/day" detail={"Biden: \"Please pump more.\" OPEC: \"New phone who dis?\""} color={C.charOrange} icon="✂️" delay={330} />
          <ShortFact text="OPEC controls 40% production, 80% reserves" detail="A cartel by any other name would smell as profitable." color={C.glow} icon="⚡" delay={510} />
          <ShortFact year="2019" text="Aramco IPO: $25.6B — biggest EVER" detail="$2.4 TRILLION valuation. Your entire country is worth less." color={C.charGold} icon="💰" delay={690} />
          <ShortFact text="China brokered Saudi-Iran peace" detail="In Beijing. While America wasn't looking. Awkward." color={C.charRed} icon="🤝" delay={870} />
        </div>
      </AbsoluteFill>
    </Sequence>

    <Sequence from={1350} durationInFrames={360}>
      <ShortCTA delay={5} />
    </Sequence>
  </AbsoluteFill>
);
