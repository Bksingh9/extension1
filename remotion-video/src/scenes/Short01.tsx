import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring, Easing } from 'remotion';
import { COLORS, FONT } from '../utils/theme';
import { GridOverlay } from '../components/GridOverlay';
import { BackgroundGlow } from '../components/BackgroundGlow';

/**
 * YouTube Short #1: "Prompt → Video in 60 Seconds"
 * Vertical format: 1080x1920, 30fps, ~55 seconds (1650 frames)
 */

const PHASES = {
  titleIn: { start: 0, end: 40 },
  promptShow: { start: 50, end: 220 },
  arrowTransition: { start: 230, end: 260 },
  fileGen: { start: 270, end: 550 },
  renderCmd: { start: 560, end: 850 },
  progressBar: { start: 860, end: 1050 },
  resultShow: { start: 1060, end: 1350 },
  ctaEnd: { start: 1360, end: 1650 },
};

export const Short01: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fade = (start: number, dur = 15) =>
    interpolate(frame, [start, start + dur], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });

  const slideUp = (start: number, dist = 40, dur = 18) =>
    interpolate(frame, [start, start + dur], [dist, 0], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
      easing: Easing.out(Easing.cubic),
    });

  const typeText = (text: string, start: number, speed = 0.5) => {
    const chars = Math.floor(
      interpolate(frame, [start, start + text.length / speed], [0, text.length], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
      })
    );
    return text.slice(0, chars);
  };

  // Progress bar
  const progress = interpolate(frame, [PHASES.progressBar.start, PHASES.progressBar.end], [0, 100], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.cubic),
  });

  const cursorBlink = Math.sin(frame * 0.3) > 0 ? 1 : 0;

  const files = [
    'src/Root.tsx',
    'src/scenes/HookScene.tsx',
    'src/scenes/ProblemScene.tsx',
    'src/scenes/RemotionScene.tsx',
    'src/scenes/FinaleScene.tsx',
    'src/components/TitleBlock.tsx',
    'src/components/TerminalPanel.tsx',
    'src/utils/theme.ts',
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.bg }}>
      <GridOverlay />
      <BackgroundGlow color={COLORS.primaryGlow} x="50%" y="30%" size={400} />
      <BackgroundGlow color={COLORS.success} x="50%" y="80%" size={300} pulse={false} />

      <div style={{ padding: '80px 50px', height: '100%', display: 'flex', flexDirection: 'column' }}>

        {/* TITLE */}
        <div
          style={{
            opacity: fade(PHASES.titleIn.start),
            transform: `translateY(${slideUp(PHASES.titleIn.start)}px) scale(${spring({ frame, fps, config: { damping: 12 } })})`,
            fontSize: 52,
            fontFamily: FONT.heading,
            fontWeight: 800,
            color: COLORS.textPrimary,
            lineHeight: 1.15,
            letterSpacing: '-0.03em',
            textAlign: 'center',
            marginBottom: 20,
          }}
        >
          One Prompt.
          <br />
          <span style={{ color: COLORS.primary }}>One Video.</span>
        </div>

        {/* Subtitle */}
        <div
          style={{
            opacity: fade(25),
            fontSize: 18,
            fontFamily: FONT.body,
            color: COLORS.textSecondary,
            textAlign: 'center',
            marginBottom: 40,
          }}
        >
          Watch it happen in 60 seconds
        </div>

        {/* PROMPT PANEL */}
        {frame >= PHASES.promptShow.start && (
          <div
            style={{
              opacity: fade(PHASES.promptShow.start),
              transform: `translateY(${slideUp(PHASES.promptShow.start, 30)}px)`,
              backgroundColor: COLORS.bgCard,
              border: `1px solid ${COLORS.primary}44`,
              borderRadius: 16,
              overflow: 'hidden',
              marginBottom: 24,
            }}
          >
            <div
              style={{
                padding: '10px 16px',
                borderBottom: `1px solid ${COLORS.border}`,
                fontSize: 13,
                fontFamily: FONT.mono,
                color: COLORS.textMuted,
                display: 'flex',
                alignItems: 'center',
                gap: 8,
              }}
            >
              <span style={{ color: COLORS.primary }}>{'>'}</span> prompt
            </div>
            <div style={{ padding: 20 }}>
              <span style={{ fontSize: 16, fontFamily: FONT.mono, color: COLORS.textPrimary, lineHeight: 1.6 }}>
                {typeText('Create a 30-second motion graphics video about AI video creation with 7 scenes', PHASES.promptShow.start + 10, 0.8)}
              </span>
              <span
                style={{
                  display: 'inline-block',
                  width: 8,
                  height: 18,
                  backgroundColor: COLORS.primary,
                  marginLeft: 2,
                  opacity: cursorBlink,
                  verticalAlign: 'text-bottom',
                }}
              />
            </div>
          </div>
        )}

        {/* ARROW */}
        {frame >= PHASES.arrowTransition.start && (
          <div
            style={{
              opacity: fade(PHASES.arrowTransition.start, 10),
              textAlign: 'center',
              fontSize: 32,
              color: COLORS.primary,
              marginBottom: 24,
              transform: `scale(${spring({ frame: frame - PHASES.arrowTransition.start, fps, config: { damping: 10 } })})`,
            }}
          >
            ↓
          </div>
        )}

        {/* FILE GENERATION */}
        {frame >= PHASES.fileGen.start && (
          <div
            style={{
              opacity: fade(PHASES.fileGen.start),
              backgroundColor: COLORS.bgCard,
              border: `1px solid ${COLORS.border}`,
              borderRadius: 16,
              padding: 20,
              marginBottom: 24,
            }}
          >
            <div
              style={{
                fontSize: 12,
                fontFamily: FONT.mono,
                color: COLORS.textMuted,
                marginBottom: 12,
                letterSpacing: '0.05em',
              }}
            >
              CLAUDE CODE GENERATING FILES
            </div>
            {files.map((file, i) => {
              const fileDelay = PHASES.fileGen.start + 15 + i * 28;
              const fileOpacity = fade(fileDelay, 10);
              const checkOpacity = fade(fileDelay + 18, 8);
              return (
                <div
                  key={i}
                  style={{
                    opacity: fileOpacity,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    fontSize: 15,
                    fontFamily: FONT.mono,
                    color: COLORS.textSecondary,
                    lineHeight: 2.2,
                  }}
                >
                  <span>{file}</span>
                  <span style={{ opacity: checkOpacity, color: COLORS.success }}>✓</span>
                </div>
              );
            })}
          </div>
        )}

        {/* RENDER COMMAND */}
        {frame >= PHASES.renderCmd.start && (
          <div
            style={{
              opacity: fade(PHASES.renderCmd.start),
              transform: `translateY(${slideUp(PHASES.renderCmd.start, 20)}px)`,
              backgroundColor: '#0d1117',
              borderRadius: 16,
              border: `1px solid ${COLORS.border}`,
              overflow: 'hidden',
              marginBottom: 24,
            }}
          >
            <div style={{ display: 'flex', gap: 6, padding: '10px 14px', borderBottom: `1px solid ${COLORS.border}` }}>
              <div style={{ width: 10, height: 10, borderRadius: 5, backgroundColor: '#ff5f57' }} />
              <div style={{ width: 10, height: 10, borderRadius: 5, backgroundColor: '#febc2e' }} />
              <div style={{ width: 10, height: 10, borderRadius: 5, backgroundColor: '#28c840' }} />
            </div>
            <div style={{ padding: 20 }}>
              <div style={{ fontSize: 15, fontFamily: FONT.mono, color: COLORS.textPrimary, lineHeight: 1.8 }}>
                <span style={{ color: COLORS.success }}>$ </span>
                {typeText('npx remotion render MainVideo out/final.mp4', PHASES.renderCmd.start + 15, 0.7)}
                <span style={{ display: 'inline-block', width: 8, height: 18, backgroundColor: COLORS.primary, marginLeft: 2, opacity: cursorBlink, verticalAlign: 'text-bottom' }} />
              </div>
              {frame >= PHASES.progressBar.start && (
                <div style={{ marginTop: 16 }}>
                  <div style={{ fontSize: 13, fontFamily: FONT.mono, color: COLORS.textMuted, marginBottom: 8 }}>
                    Rendering... {Math.round(progress)}%
                  </div>
                  <div style={{ height: 6, backgroundColor: COLORS.border, borderRadius: 3, overflow: 'hidden' }}>
                    <div style={{ width: `${progress}%`, height: '100%', backgroundColor: COLORS.success, borderRadius: 3 }} />
                  </div>
                </div>
              )}
              {progress >= 100 && (
                <div style={{ opacity: fade(PHASES.progressBar.end + 5, 10), fontSize: 15, fontFamily: FONT.mono, color: COLORS.success, marginTop: 12, lineHeight: 1.8 }}>
                  ✓ Rendered 945 frames in 24.3s
                  <br />
                  ✓ out/final.mp4 — 3.7MB
                </div>
              )}
            </div>
          </div>
        )}

        {/* RESULT / SUCCESS */}
        {frame >= PHASES.resultShow.start && (
          <div
            style={{
              opacity: fade(PHASES.resultShow.start),
              transform: `scale(${spring({ frame: frame - PHASES.resultShow.start, fps, config: { damping: 10 } })})`,
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              gap: 12,
              padding: '18px 32px',
              backgroundColor: `${COLORS.success}15`,
              border: `1px solid ${COLORS.success}44`,
              borderRadius: 20,
              alignSelf: 'center',
              marginBottom: 30,
            }}
          >
            <div
              style={{
                width: 28,
                height: 28,
                borderRadius: 14,
                backgroundColor: COLORS.success,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 16,
                color: '#fff',
                fontWeight: 700,
              }}
            >
              ✓
            </div>
            <span style={{ fontSize: 22, fontFamily: FONT.heading, fontWeight: 700, color: COLORS.success }}>
              Render Complete
            </span>
          </div>
        )}

        {/* CTA */}
        {frame >= PHASES.ctaEnd.start && (
          <div
            style={{
              opacity: fade(PHASES.ctaEnd.start),
              flex: 1,
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'center',
              alignItems: 'center',
              gap: 16,
            }}
          >
            <div
              style={{
                fontSize: 36,
                fontFamily: FONT.heading,
                fontWeight: 800,
                color: COLORS.textPrimary,
                textAlign: 'center',
                lineHeight: 1.2,
              }}
            >
              Full tutorial
              <br />
              <span style={{ color: COLORS.primary }}>on the channel</span>
            </div>
            <div
              style={{
                width: 52,
                height: 52,
                borderRadius: 26,
                backgroundColor: COLORS.primary,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 20,
                fontFamily: FONT.heading,
                fontWeight: 800,
                color: '#fff',
                boxShadow: `0 0 30px ${COLORS.primary}44`,
              }}
            >
              AR
            </div>
            <div style={{ fontSize: 16, fontFamily: FONT.heading, fontWeight: 600, color: COLORS.textSecondary }}>
              AI RENDER LAB
            </div>
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
