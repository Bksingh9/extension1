import React from 'react';
import { useCurrentFrame } from 'remotion';
import { SceneContainer } from '../components/SceneContainer';
import { TitleBlock } from '../components/TitleBlock';
import { MetricStrip } from '../components/MetricStrip';
import { InfoCard } from '../components/InfoCard';
import { COLORS } from '../utils/theme';
import { SCENE } from '../utils/timings';
import { stagger } from '../utils/animation';

const metrics = [
  { label: 'Faster Iteration', value: '10x', color: COLORS.primary },
  { label: 'Reusable Scenes', value: '100%', color: COLORS.secondary },
  { label: 'Local Rendering', value: '4K', color: COLORS.success },
];

const benefits = [
  { title: 'Cleaner Workflow', icon: '⚡', subtitle: 'One tool, one command' },
  { title: 'Cinematic Output', icon: '🎥', subtitle: 'Production-quality motion' },
  { title: 'Full Control', icon: '🎛️', subtitle: 'Code-driven, version-controlled' },
];

export const BenefitsScene: React.FC = () => {
  return (
    <SceneContainer
      totalFrames={SCENE.benefits.duration}
      glowColor={COLORS.secondary}
      glowX="50%"
      glowY="40%"
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 36,
        }}
      >
        <TitleBlock text="Why This Matters" delay={5} fontSize={46} />

        <MetricStrip metrics={metrics} delay={15} />

        <div style={{ display: 'flex', gap: 24 }}>
          {benefits.map((b, i) => (
            <InfoCard
              key={i}
              title={b.title}
              subtitle={b.subtitle}
              icon={b.icon}
              delay={40 + stagger(i, 10)}
              accentColor={i === 0 ? COLORS.primary : i === 1 ? COLORS.secondary : COLORS.success}
              width={280}
            />
          ))}
        </div>
      </div>
    </SceneContainer>
  );
};
