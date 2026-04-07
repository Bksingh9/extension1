import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { ShortHook, ShortFact, ShortCTA } from './ShortTemplate';
import { CartoonBg } from '../components/CartoonBg';
import { C } from '../theme';

export const Short_Surveillance: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: '#060310' }}>
    <Sequence from={0} durationInFrames={90}>
      <ShortHook text="Your Phone is a Snitch" subtext="And you're paying for the privilege." color={C.mystery} />
    </Sequence>

    <Sequence from={90} durationInFrames={1260}>
      <AbsoluteFill>
        <CartoonBg color="#0a0618" accentColor={C.mystery} showGrid />
        <div style={{ padding: '80px 50px', display: 'flex', flexDirection: 'column', justifyContent: 'center', height: '100%' }}>
          <ShortFact year="1946" text="Five Eyes: 5 nations spy on everyone. Together." detail="The OG group chat. Still active. Reading yours." color={C.charBlue} icon="👁️" delay={0} />
          <ShortFact year="2013" text="Snowden: 'The NSA reads ALL your stuff'" detail="PRISM: direct access to Google, Apple, Meta servers." color={C.danger} icon="💥" delay={150} />
          <ShortFact text="XKeyscore: Google for spies. No warrant." detail="Search anyone's emails and browsing. Just trust them." color={C.danger} icon="🔍" delay={330} />
          <ShortFact text="China: 600M cameras. 1 per 2.4 citizens." detail="20M+ flights blocked by social credit. Black Mirror was a doc." color={C.charRed} icon="📷" delay={510} />
          <ShortFact text="Google: 8.5 BILLION searches per day" detail="They know what you want before you do." color={C.charBlue} icon="🔍" delay={690} />
          <ShortFact text="Data broker industry: $200B+/year" detail="The product is you. You're not getting a cut." color={C.danger} icon="🏢" delay={870} />
        </div>
      </AbsoluteFill>
    </Sequence>

    <Sequence from={1350} durationInFrames={360}>
      <ShortCTA delay={5} />
    </Sequence>
  </AbsoluteFill>
);
