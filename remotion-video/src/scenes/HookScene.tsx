import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { SceneContainer } from '../components/SceneContainer';
import { TitleBlock } from '../components/TitleBlock';
import { SubtitleBlock } from '../components/SubtitleBlock';
import { BackgroundGlow } from '../components/BackgroundGlow';
import { COLORS } from '../utils/theme';
import { SCENE } from '../utils/timings';
import { fadeIn } from '../utils/animation';

export const HookScene: React.FC = () => {
  const frame = useCurrentFrame();

  // Accent line that expands under the title
  const lineWidth = fadeIn(frame, 30, 20) * 200;

  return (
    <SceneContainer
      totalFrames={SCENE.hook.duration}
      glowColor={COLORS.primaryGlow}
      glowX="50%"
      glowY="45%"
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 20,
        }}
      >
        <TitleBlock text="One Idea." delay={5} fontSize={82} useSpring />
        <TitleBlock text="One Prompt." delay={18} fontSize={82} color={COLORS.primary} useSpring />
        <TitleBlock text="One Finished Video." delay={32} fontSize={82} useSpring />

        <div
          style={{
            width: lineWidth,
            height: 3,
            backgroundColor: COLORS.primary,
            borderRadius: 2,
            marginTop: 16,
            opacity: fadeIn(frame, 30, 10),
          }}
        />

        <SubtitleBlock
          text="Claude Code + Remotion"
          delay={50}
          fontSize={24}
        />
      </div>
    </SceneContainer>
  );
};
