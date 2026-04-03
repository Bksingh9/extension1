import React from 'react';
import { useCurrentFrame } from 'remotion';
import { COLORS, FONT, RADIUS, SHADOW, SPACING } from '../utils/theme';
import { fadeIn, slideUp, stagger } from '../utils/animation';
import { interpolate } from 'remotion';

interface TerminalLine {
  prefix?: string;
  text: string;
  color?: string;
  isOutput?: boolean;
}

export const TerminalPanel: React.FC<{
  lines: TerminalLine[];
  delay?: number;
  width?: number;
  title?: string;
}> = ({ lines, delay = 0, width = 700, title = 'terminal' }) => {
  const frame = useCurrentFrame();
  const panelOpacity = fadeIn(frame, delay, 14);
  const panelY = slideUp(frame, delay, 30, 16);

  return (
    <div
      style={{
        opacity: panelOpacity,
        transform: `translateY(${panelY}px)`,
        width,
        backgroundColor: '#0d1117',
        borderRadius: RADIUS.lg,
        boxShadow: SHADOW.card,
        border: `1px solid ${COLORS.border}`,
        overflow: 'hidden',
      }}
    >
      {/* Title bar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          padding: '12px 16px',
          borderBottom: `1px solid ${COLORS.border}`,
          backgroundColor: '#161b22',
        }}
      >
        <div style={{ width: 12, height: 12, borderRadius: 6, backgroundColor: '#ff5f57' }} />
        <div style={{ width: 12, height: 12, borderRadius: 6, backgroundColor: '#febc2e' }} />
        <div style={{ width: 12, height: 12, borderRadius: 6, backgroundColor: '#28c840' }} />
        <span
          style={{
            marginLeft: 12,
            fontSize: 13,
            fontFamily: FONT.mono,
            color: COLORS.textMuted,
          }}
        >
          {title}
        </span>
      </div>
      {/* Lines */}
      <div style={{ padding: SPACING.md }}>
        {lines.map((line, i) => {
          const lineDelay = delay + stagger(i, 12);
          const lineOpacity = fadeIn(frame, lineDelay, 8);
          const charCount = line.text.length;
          const typedChars = Math.floor(
            interpolate(frame, [lineDelay, lineDelay + charCount * 0.6], [0, charCount], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            })
          );
          const displayText = line.isOutput ? line.text : line.text.slice(0, typedChars);
          const showCursor = !line.isOutput && typedChars < charCount && frame >= lineDelay;

          return (
            <div
              key={i}
              style={{
                opacity: lineOpacity,
                fontFamily: FONT.mono,
                fontSize: 16,
                lineHeight: 1.8,
                color: line.color || COLORS.textPrimary,
                display: 'flex',
              }}
            >
              {line.prefix && (
                <span style={{ color: COLORS.success, marginRight: 8 }}>{line.prefix}</span>
              )}
              <span>{displayText}</span>
              {showCursor && (
                <span
                  style={{
                    display: 'inline-block',
                    width: 8,
                    height: 18,
                    backgroundColor: COLORS.primary,
                    marginLeft: 2,
                    opacity: Math.sin(frame * 0.3) > 0 ? 1 : 0,
                  }}
                />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
