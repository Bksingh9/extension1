import React from 'react';
import { useCurrentFrame, interpolate, Easing } from 'remotion';
import { SceneContainer } from '../components/SceneContainer';
import { TerminalPanel } from '../components/TerminalPanel';
import { RenderSuccessBadge } from '../components/RenderSuccessBadge';
import { COLORS } from '../utils/theme';
import { SCENE } from '../utils/timings';

const terminalLines = [
  { prefix: '$', text: 'npm install remotion @remotion/cli' },
  { text: '✓ 188 packages installed', color: COLORS.success, isOutput: true },
  { prefix: '$', text: 'npm run dev' },
  { text: '✓ Preview server running on port 3000', color: COLORS.success, isOutput: true },
  { prefix: '$', text: 'claude "Create a 30s motion graphics video"' },
  { text: '✓ 7 scenes generated, 12 components created', color: COLORS.success, isOutput: true },
  { prefix: '$', text: 'npx remotion render MainVideo out/final.mp4' },
  { text: '✓ Rendered 945 frames in 24.3s', color: COLORS.success, isOutput: true },
];

export const TerminalWorkflowScene: React.FC = () => {
  const frame = useCurrentFrame();

  // Progress bar at the bottom of the terminal
  const progressStart = 85;
  const progress = interpolate(frame, [progressStart, progressStart + 25], [0, 100], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.cubic),
  });

  return (
    <SceneContainer
      totalFrames={SCENE.terminal.duration}
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
        <TerminalPanel
          lines={terminalLines}
          delay={5}
          width={750}
          title="~/my-video — zsh"
        />

        {/* Progress bar */}
        <div
          style={{
            width: 750,
            height: 4,
            backgroundColor: COLORS.border,
            borderRadius: 2,
            overflow: 'hidden',
            opacity: frame > progressStart ? 1 : 0,
          }}
        >
          <div
            style={{
              width: `${progress}%`,
              height: '100%',
              backgroundColor: COLORS.success,
              borderRadius: 2,
              transition: 'none',
            }}
          />
        </div>

        {progress >= 100 && <RenderSuccessBadge delay={112} />}
      </div>
    </SceneContainer>
  );
};
