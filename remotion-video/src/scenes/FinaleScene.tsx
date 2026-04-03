import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { SceneContainer } from '../components/SceneContainer';
import { TitleBlock } from '../components/TitleBlock';
import { SubtitleBlock } from '../components/SubtitleBlock';
import { RenderSuccessBadge } from '../components/RenderSuccessBadge';
import { COLORS, FONT } from '../utils/theme';
import { SCENE } from '../utils/timings';
import { fadeIn } from '../utils/animation';

export const FinaleScene: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <SceneContainer
      totalFrames={SCENE.finale.duration}
      glowColor={COLORS.success}
      glowX="50%"
      glowY="50%"
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 24,
        }}
      >
        <TitleBlock
          text="From One Prompt"
          delay={5}
          fontSize={64}
          useSpring
        />
        <TitleBlock
          text="To One Rendered Video."
          delay={18}
          fontSize={64}
          color={COLORS.success}
          useSpring
        />

        <div
          style={{
            width: fadeIn(frame, 35, 20) * 120,
            height: 3,
            backgroundColor: COLORS.success,
            borderRadius: 2,
            marginTop: 8,
          }}
        />

        <div
          style={{
            opacity: fadeIn(frame, 40, 15),
            marginTop: 8,
          }}
        >
          <RenderSuccessBadge delay={40} label="final.mp4 — Render Complete" />
        </div>

        <div
          style={{
            opacity: fadeIn(frame, 60, 15),
            fontSize: 20,
            fontFamily: FONT.heading,
            fontWeight: 600,
            color: COLORS.textMuted,
            letterSpacing: '0.08em',
            marginTop: 12,
          }}
        >
          CLAUDE CODE + REMOTION
        </div>
      </div>
    </SceneContainer>
  );
};
