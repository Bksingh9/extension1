import React from 'react';
import { COLORS, FONT } from '../theme';

export const TerminalSnippet: React.FC<{
  lines: string[];
  width?: number;
}> = ({ lines, width = 380 }) => (
  <div
    style={{
      width,
      backgroundColor: '#0d1117',
      borderRadius: 12,
      border: `1px solid ${COLORS.border}`,
      overflow: 'hidden',
      boxShadow: '0 8px 32px rgba(0,0,0,0.5)',
    }}
  >
    <div
      style={{
        display: 'flex',
        gap: 6,
        padding: '10px 14px',
        borderBottom: `1px solid ${COLORS.border}`,
      }}
    >
      <div style={{ width: 10, height: 10, borderRadius: 5, backgroundColor: '#ff5f57' }} />
      <div style={{ width: 10, height: 10, borderRadius: 5, backgroundColor: '#febc2e' }} />
      <div style={{ width: 10, height: 10, borderRadius: 5, backgroundColor: '#28c840' }} />
    </div>
    <div style={{ padding: '14px 18px' }}>
      {lines.map((line, i) => (
        <div
          key={i}
          style={{
            fontSize: 15,
            fontFamily: FONT.mono,
            color: line.startsWith('✓') ? COLORS.success : COLORS.textPrimary,
            lineHeight: 1.7,
          }}
        >
          {!line.startsWith('✓') && !line.startsWith(' ') && (
            <span style={{ color: COLORS.success, marginRight: 6 }}>$</span>
          )}
          {line}
        </div>
      ))}
    </div>
  </div>
);
