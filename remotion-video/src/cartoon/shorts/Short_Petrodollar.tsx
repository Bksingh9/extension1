import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { ShortHook, ShortFact, ShortCTA } from './ShortTemplate';
import { CartoonBg } from '../components/CartoonBg';
import { C } from '../theme';

export const Short_Petrodollar: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#060310' }}>
    {/* HOOK: 0-90 frames (3s) */}
    <Sequence from={0} durationInFrames={90}>
      <ShortHook
        text="Every Country That Ditched the Dollar..."
        subtext="Got invaded. Let that sink in."
        color={C.danger}
      />
    </Sequence>

    {/* FACTS: 90-1350 frames (42s) */}
    <Sequence from={90} durationInFrames={1260}>
      <AbsoluteFill>
        <CartoonBg color="#0a0618" accentColor={C.charGold} showGrid />
        <div style={{ padding: '80px 50px', display: 'flex', flexDirection: 'column', justifyContent: 'center', height: '100%' }}>
          <ShortFact year="2000" text="Iraq switches oil to euros" detail={"\"I'll use euros.\" — Saddam. This was a mistake."} color={C.charOrange} icon="🇮🇶" delay={0} />
          <ShortFact year="2003" text="US invades. Oil back to dollars." detail={"\"WMDs\" never found. Dollar restored. Coincidence?"} color={C.danger} icon="💣" delay={90} />
          <ShortFact year="2011" text="Libya proposes gold African currency" detail={"Gaddafi: \"Africa deserves its own money!\""} color={C.charGold} icon="🇱🇾" delay={210} />
          <ShortFact year="2011" text="NATO intervenes. Gaddafi killed." detail="Gold dinar dies with him. See a pattern?" color={C.danger} icon="⚔️" delay={360} />
          <ShortFact year="2017" text="Venezuela prices oil in yuan" detail="Sanctioned into the shadow realm. Immediately." color={C.charPurple} icon="🇻🇪" delay={510} />
          <ShortFact year="NOW" text="Iran trades oil in euros" detail={"Has been on America's naughty list since 1979."} color={C.mystery} icon="🇮🇷" delay={660} />
        </div>
      </AbsoluteFill>
    </Sequence>

    {/* CTA: 1350-1710 frames (12s) */}
    <Sequence from={1350} durationInFrames={360}>
      <ShortCTA delay={5} />
    </Sequence>
  </AbsoluteFill>
);
