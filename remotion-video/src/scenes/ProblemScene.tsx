import React from 'react';
import { useCurrentFrame, interpolate, Easing } from 'remotion';
import { SceneContainer } from '../components/SceneContainer';
import { TitleBlock } from '../components/TitleBlock';
import { InfoCard } from '../components/InfoCard';
import { COLORS } from '../utils/theme';
import { SCENE } from '../utils/timings';
import { fadeIn, stagger } from '../utils/animation';

const problems = [
  { title: 'Script in Docs', icon: '📝', subtitle: 'Write the story somewhere' },
  { title: 'Design in Figma', icon: '🎨', subtitle: 'Mock up each frame' },
  { title: 'Animate in AE', icon: '🎬', subtitle: 'Keyframe everything' },
  { title: 'Render & Export', icon: '⏳', subtitle: 'Wait... and wait' },
];

export const ProblemScene: React.FC = () => {
  const frame = useCurrentFrame();

  // Fragmented arrows between cards
  const arrowOpacity = fadeIn(frame, 50, 15);

  return (
    <SceneContainer
      totalFrames={SCENE.problem.duration}
      glowColor={COLORS.danger}
      glowX="50%"
      glowY="55%"
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 40,
        }}
      >
        <TitleBlock
          text="The Old Workflow Is Fragmented"
          delay={5}
          fontSize={48}
          color={COLORS.textSecondary}
        />

        <div style={{ display: 'flex', gap: 24, alignItems: 'center' }}>
          {problems.map((p, i) => (
            <React.Fragment key={i}>
              <InfoCard
                title={p.title}
                subtitle={p.subtitle}
                icon={p.icon}
                delay={15 + stagger(i, 10)}
                accentColor={COLORS.warning}
                width={220}
              />
              {i < problems.length - 1 && (
                <div
                  style={{
                    opacity: arrowOpacity,
                    fontSize: 24,
                    color: COLORS.textMuted,
                  }}
                >
                  →
                </div>
              )}
            </React.Fragment>
          ))}
        </div>

        <div
          style={{
            opacity: fadeIn(frame, 80, 15),
            fontSize: 20,
            color: COLORS.danger,
            fontWeight: 600,
            letterSpacing: '0.04em',
            fontFamily: 'Inter, sans-serif',
          }}
        >
          Too many tools. Too slow. Too fragmented.
        </div>
      </div>
    </SceneContainer>
  );
};
