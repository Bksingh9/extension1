import React from 'react';
import { useCurrentFrame } from 'remotion';
import { COLORS, FONT, RADIUS, SHADOW, SPACING } from '../utils/theme';
import { fadeIn, slideRight, stagger } from '../utils/animation';

interface TreeItem {
  name: string;
  indent: number;
  isFolder?: boolean;
}

export const FileTreePanel: React.FC<{
  items: TreeItem[];
  delay?: number;
  width?: number;
}> = ({ items, delay = 0, width = 280 }) => {
  const frame = useCurrentFrame();
  const panelOpacity = fadeIn(frame, delay, 14);

  return (
    <div
      style={{
        opacity: panelOpacity,
        width,
        backgroundColor: COLORS.bgCard,
        borderRadius: RADIUS.lg,
        boxShadow: SHADOW.card,
        border: `1px solid ${COLORS.border}`,
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          padding: '10px 16px',
          borderBottom: `1px solid ${COLORS.border}`,
          fontSize: 12,
          fontFamily: FONT.mono,
          color: COLORS.textMuted,
        }}
      >
        EXPLORER
      </div>
      <div style={{ padding: `${SPACING.sm}px ${SPACING.md}px` }}>
        {items.map((item, i) => {
          const d = delay + 6 + stagger(i, 5);
          const opacity = fadeIn(frame, d, 8);
          const x = slideRight(frame, d, 20, 12);

          return (
            <div
              key={i}
              style={{
                opacity,
                transform: `translateX(${x}px)`,
                paddingLeft: item.indent * 16,
                fontSize: 14,
                fontFamily: FONT.mono,
                color: item.isFolder ? COLORS.primary : COLORS.textSecondary,
                lineHeight: 2,
                display: 'flex',
                alignItems: 'center',
                gap: 6,
              }}
            >
              <span style={{ fontSize: 12 }}>{item.isFolder ? '📁' : '📄'}</span>
              {item.name}
            </div>
          );
        })}
      </div>
    </div>
  );
};
