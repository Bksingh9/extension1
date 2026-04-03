import React from 'react';
import { useCurrentFrame } from 'remotion';
import { SceneContainer } from '../components/SceneContainer';
import { TitleBlock } from '../components/TitleBlock';
import { PromptPanel } from '../components/PromptPanel';
import { FileTreePanel } from '../components/FileTreePanel';
import { COLORS } from '../utils/theme';
import { SCENE } from '../utils/timings';
import { fadeIn, stagger } from '../utils/animation';

const fileTree = [
  { name: 'src/', indent: 0, isFolder: true },
  { name: 'scenes/', indent: 1, isFolder: true },
  { name: 'HookScene.tsx', indent: 2 },
  { name: 'ProblemScene.tsx', indent: 2 },
  { name: 'RemotionScene.tsx', indent: 2 },
  { name: 'FinaleScene.tsx', indent: 2 },
  { name: 'components/', indent: 1, isFolder: true },
  { name: 'TitleBlock.tsx', indent: 2 },
  { name: 'TerminalPanel.tsx', indent: 2 },
  { name: 'Root.tsx', indent: 1 },
];

export const PromptToPlanScene: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <SceneContainer
      totalFrames={SCENE.promptToPlan.duration}
      glowColor={COLORS.secondary}
      glowX="35%"
      glowY="50%"
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 30,
        }}
      >
        <TitleBlock
          text="Claude Code Structures the Idea"
          delay={5}
          fontSize={46}
          color={COLORS.primary}
        />

        <div style={{ display: 'flex', gap: 32, alignItems: 'flex-start' }}>
          <PromptPanel
            prompt="Create a 30-second motion graphics video about AI-powered video creation. Include a hook, problem statement, solution demo, terminal workflow, benefits, and strong finale."
            delay={15}
            width={560}
          />

          {/* Arrow */}
          <div
            style={{
              opacity: fadeIn(frame, 60, 15),
              fontSize: 32,
              color: COLORS.primary,
              marginTop: 80,
            }}
          >
            →
          </div>

          <FileTreePanel items={fileTree} delay={50} width={300} />
        </div>

        <div
          style={{
            display: 'flex',
            gap: 16,
            opacity: fadeIn(frame, 100, 15),
          }}
        >
          {['Idea → Script', 'Script → Scenes', 'Scenes → Components'].map((text, i) => (
            <div
              key={i}
              style={{
                opacity: fadeIn(frame, 100 + stagger(i, 8), 10),
                padding: '8px 20px',
                backgroundColor: COLORS.bgCard,
                border: `1px solid ${COLORS.primary}44`,
                borderRadius: 20,
                fontSize: 14,
                fontFamily: 'Inter, sans-serif',
                color: COLORS.primary,
                fontWeight: 600,
              }}
            >
              {text}
            </div>
          ))}
        </div>
      </div>
    </SceneContainer>
  );
};
