import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { CARTOON_SCENES } from './theme';
import { IntroCard } from './scenes/IntroCard';
import { Scene1_WorldStage } from './scenes/Scene1_WorldStage';
import { Scene2_FollowMoney } from './scenes/Scene2_FollowMoney';
import { Scene3_ShadowPlayers } from './scenes/Scene3_ShadowPlayers';
import { Scene4_DominoEffect } from './scenes/Scene4_DominoEffect';
import { Scene5_WhatTheyDontTell } from './scenes/Scene5_WhatTheyDontTell';
import { OutroCard } from './scenes/OutroCard';

export const CartoonVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0518' }}>
      <Sequence from={CARTOON_SCENES.intro.start} durationInFrames={CARTOON_SCENES.intro.duration}>
        <IntroCard />
      </Sequence>

      <Sequence from={CARTOON_SCENES.scene1.start} durationInFrames={CARTOON_SCENES.scene1.duration}>
        <Scene1_WorldStage />
      </Sequence>

      <Sequence from={CARTOON_SCENES.scene2.start} durationInFrames={CARTOON_SCENES.scene2.duration}>
        <Scene2_FollowMoney />
      </Sequence>

      <Sequence from={CARTOON_SCENES.scene3.start} durationInFrames={CARTOON_SCENES.scene3.duration}>
        <Scene3_ShadowPlayers />
      </Sequence>

      <Sequence from={CARTOON_SCENES.scene4.start} durationInFrames={CARTOON_SCENES.scene4.duration}>
        <Scene4_DominoEffect />
      </Sequence>

      <Sequence from={CARTOON_SCENES.scene5.start} durationInFrames={CARTOON_SCENES.scene5.duration}>
        <Scene5_WhatTheyDontTell />
      </Sequence>

      <Sequence from={CARTOON_SCENES.outro.start} durationInFrames={CARTOON_SCENES.outro.duration}>
        <OutroCard />
      </Sequence>
    </AbsoluteFill>
  );
};
