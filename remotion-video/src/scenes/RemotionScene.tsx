import React from 'react';
import { useCurrentFrame } from 'remotion';
import { SceneContainer } from '../components/SceneContainer';
import { TitleBlock } from '../components/TitleBlock';
import { TimelinePanel } from '../components/TimelinePanel';
import { COLORS, FONT, RADIUS, SHADOW, SPACING } from '../utils/theme';
import { SCENE } from '../utils/timings';
import { fadeIn, slideUp } from '../utils/animation';

const tracks = [
  { label: 'Hook', color: COLORS.primary, widthPercent: 12, offsetPercent: 0 },
  { label: 'Problem', color: COLORS.warning, widthPercent: 15, offsetPercent: 12 },
  { label: 'Claude Code', color: COLORS.secondary, widthPercent: 18, offsetPercent: 27 },
  { label: 'Remotion', color: COLORS.primary, widthPercent: 18, offsetPercent: 45 },
  { label: 'Terminal', color: COLORS.success, widthPercent: 15, offsetPercent: 63 },
  { label: 'Benefits', color: '#f472b6', widthPercent: 12, offsetPercent: 78 },
  { label: 'Finale', color: COLORS.success, widthPercent: 10, offsetPercent: 90 },
];

export const RemotionScene: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <SceneContainer
      totalFrames={SCENE.remotion.duration}
      glowColor={COLORS.primary}
      glowX="60%"
      glowY="45%"
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
          text="Remotion Turns Scenes Into Motion"
          delay={5}
          fontSize={46}
          color={COLORS.textPrimary}
        />

        <div style={{ display: 'flex', gap: 28, alignItems: 'flex-start' }}>
          {/* Code preview panel */}
          <div
            style={{
              opacity: fadeIn(frame, 15, 14),
              transform: `translateY(${frame < 15 ? 30 : 0}px)`,
              width: 420,
              backgroundColor: '#0d1117',
              borderRadius: RADIUS.lg,
              boxShadow: SHADOW.card,
              border: `1px solid ${COLORS.border}`,
              padding: SPACING.md,
            }}
          >
            <div
              style={{
                fontSize: 11,
                fontFamily: FONT.mono,
                color: COLORS.textMuted,
                marginBottom: 12,
              }}
            >
              MainVideo.tsx
            </div>
            {[
              { text: '<Composition', color: COLORS.primary },
              { text: '  id="MainVideo"', color: COLORS.textSecondary },
              { text: '  width={1920}', color: COLORS.textSecondary },
              { text: '  height={1080}', color: COLORS.textSecondary },
              { text: '  fps={30}', color: COLORS.success },
              { text: '  durationInFrames={945}', color: COLORS.success },
              { text: '  component={MainVideo}', color: COLORS.primary },
              { text: '/>', color: COLORS.primary },
            ].map((line, i) => (
              <div
                key={i}
                style={{
                  opacity: fadeIn(frame, 20 + i * 5, 8),
                  fontSize: 15,
                  fontFamily: FONT.mono,
                  color: line.color,
                  lineHeight: 1.8,
                }}
              >
                {line.text}
              </div>
            ))}
          </div>

          <TimelinePanel tracks={tracks} delay={30} width={520} />
        </div>

        <div
          style={{
            opacity: fadeIn(frame, 90, 15),
            fontSize: 18,
            fontFamily: FONT.body,
            color: COLORS.textSecondary,
            textAlign: 'center',
          }}
        >
          Components + Timing + Transitions = Rendered Video
        </div>
      </div>
    </SceneContainer>
  );
};
