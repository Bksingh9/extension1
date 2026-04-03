import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { SCENE } from './utils/timings';
import { HookScene } from './scenes/HookScene';
import { ProblemScene } from './scenes/ProblemScene';
import { PromptToPlanScene } from './scenes/PromptToPlanScene';
import { RemotionScene } from './scenes/RemotionScene';
import { TerminalWorkflowScene } from './scenes/TerminalWorkflowScene';
import { BenefitsScene } from './scenes/BenefitsScene';
import { FinaleScene } from './scenes/FinaleScene';

export const MainVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#0a0a0f' }}>
      <Sequence from={SCENE.hook.start} durationInFrames={SCENE.hook.duration}>
        <HookScene />
      </Sequence>

      <Sequence from={SCENE.problem.start} durationInFrames={SCENE.problem.duration}>
        <ProblemScene />
      </Sequence>

      <Sequence from={SCENE.promptToPlan.start} durationInFrames={SCENE.promptToPlan.duration}>
        <PromptToPlanScene />
      </Sequence>

      <Sequence from={SCENE.remotion.start} durationInFrames={SCENE.remotion.duration}>
        <RemotionScene />
      </Sequence>

      <Sequence from={SCENE.terminal.start} durationInFrames={SCENE.terminal.duration}>
        <TerminalWorkflowScene />
      </Sequence>

      <Sequence from={SCENE.benefits.start} durationInFrames={SCENE.benefits.duration}>
        <BenefitsScene />
      </Sequence>

      <Sequence from={SCENE.finale.start} durationInFrames={SCENE.finale.duration}>
        <FinaleScene />
      </Sequence>
    </AbsoluteFill>
  );
};
