import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { IntroScene } from './scenes/IntroScene';
import { HookScene } from './scenes/HookScene';
import { ProblemScene } from './scenes/ProblemScene';
import { PromptToPlanScene } from './scenes/PromptToPlanScene';
import { RemotionScene } from './scenes/RemotionScene';
import { TerminalWorkflowScene } from './scenes/TerminalWorkflowScene';
import { BenefitsScene } from './scenes/BenefitsScene';
import { FinaleScene } from './scenes/FinaleScene';
import { OutroScene } from './scenes/OutroScene';
import { SCENE } from './utils/timings';

// Full video: Intro (150f) + Main (945f) + Outro (240f) = 1335f = 44.5s
const INTRO_FRAMES = 150;
const MAIN_OFFSET = INTRO_FRAMES;
const OUTRO_OFFSET = INTRO_FRAMES + 945;

export const FullVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0f' }}>
      {/* Channel Intro */}
      <Sequence from={0} durationInFrames={INTRO_FRAMES}>
        <IntroScene />
      </Sequence>

      {/* Main Video Scenes */}
      <Sequence from={MAIN_OFFSET + SCENE.hook.start} durationInFrames={SCENE.hook.duration}>
        <HookScene />
      </Sequence>
      <Sequence from={MAIN_OFFSET + SCENE.problem.start} durationInFrames={SCENE.problem.duration}>
        <ProblemScene />
      </Sequence>
      <Sequence from={MAIN_OFFSET + SCENE.promptToPlan.start} durationInFrames={SCENE.promptToPlan.duration}>
        <PromptToPlanScene />
      </Sequence>
      <Sequence from={MAIN_OFFSET + SCENE.remotion.start} durationInFrames={SCENE.remotion.duration}>
        <RemotionScene />
      </Sequence>
      <Sequence from={MAIN_OFFSET + SCENE.terminal.start} durationInFrames={SCENE.terminal.duration}>
        <TerminalWorkflowScene />
      </Sequence>
      <Sequence from={MAIN_OFFSET + SCENE.benefits.start} durationInFrames={SCENE.benefits.duration}>
        <BenefitsScene />
      </Sequence>
      <Sequence from={MAIN_OFFSET + SCENE.finale.start} durationInFrames={SCENE.finale.duration}>
        <FinaleScene />
      </Sequence>

      {/* Channel Outro */}
      <Sequence from={OUTRO_OFFSET} durationInFrames={240}>
        <OutroScene />
      </Sequence>
    </AbsoluteFill>
  );
};
