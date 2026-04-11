import React from 'react';
import { AbsoluteFill } from 'remotion';
import { C, CFONT, GRADIENT } from '../theme';
import { CartoonBg } from '../components/CartoonBg';

/**
 * YouTube Thumbnail — 1280x720
 * MrBeast-style: huge text, bright color, shocked face energy
 */
export const Thumbnail: React.FC<{
  hook: string;              // Big shouty text
  sub?: string;              // Smaller supporting line
  stat?: string;             // Giant stat/number
  statLabel?: string;        // Label for stat
  badge?: string;            // Top-left badge
  color?: string;            // Main accent
  icon?: string;             // Big emoji on side
  bgColor?: string;
}> = ({
  hook,
  sub,
  stat,
  statLabel,
  badge = 'EXPOSED',
  color = C.danger,
  icon = '🌍',
  bgColor = '#050210',
}) => {
  return (
    <AbsoluteFill style={{ backgroundColor: bgColor }}>
      <CartoonBg color={bgColor} accentColor={color} particleColor={C.glow} particleCount={40} showGrid />

      {/* Big glow behind text */}
      <div style={{
        position: 'absolute',
        left: 0,
        top: '50%',
        transform: 'translateY(-50%)',
        width: '65%',
        height: '90%',
        background: `radial-gradient(ellipse at left, ${color}33 0%, transparent 60%)`,
        filter: 'blur(40px)',
      }} />

      {/* Top badge */}
      <div style={{
        position: 'absolute',
        top: 40,
        left: 60,
        padding: '10px 24px',
        backgroundColor: color,
        borderRadius: 4,
        fontSize: 28,
        fontFamily: CFONT.display,
        fontWeight: 800,
        color: '#fff',
        letterSpacing: '0.15em',
        textTransform: 'uppercase',
        boxShadow: `0 6px 24px ${color}88, 0 0 0 3px rgba(255,255,255,0.08)`,
        transform: 'rotate(-2deg)',
      }}>
        🔴 {badge}
      </div>

      {/* Giant stat on right (if provided) */}
      {stat && (
        <div style={{
          position: 'absolute',
          right: 40,
          top: 130,
          bottom: 120,
          width: 440,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 2,
        }}>
          <div style={{
            fontSize: stat.length > 5 ? 120 : 160,
            fontFamily: CFONT.display,
            fontWeight: 800,
            background: GRADIENT.goldOrange,
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            letterSpacing: '-0.03em',
            lineHeight: 0.9,
            textShadow: `6px 6px 0 ${C.outline}`,
            filter: `drop-shadow(0 0 40px ${C.glow}88)`,
            textAlign: 'center',
          }}>
            {stat}
          </div>
          {statLabel && (
            <div style={{
              fontSize: 22,
              fontFamily: CFONT.display,
              fontWeight: 700,
              color: C.textLight,
              letterSpacing: '0.08em',
              textTransform: 'uppercase',
              marginTop: 8,
              textShadow: '0 2px 8px rgba(0,0,0,0.8)',
              textAlign: 'center',
            }}>
              {statLabel}
            </div>
          )}
        </div>
      )}

      {/* Main hook text (left side, giant) */}
      <div style={{
        position: 'absolute',
        left: 50,
        top: 130,
        bottom: 120,
        width: stat ? 680 : 760,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        zIndex: 2,
      }}>
        <div style={{
          fontSize: stat ? 54 : 92,
          fontFamily: CFONT.display,
          fontWeight: 800,
          color: C.textWhite,
          letterSpacing: '-0.02em',
          lineHeight: 0.92,
          textTransform: 'uppercase',
          textShadow: `5px 5px 0 ${C.outline}, 0 0 50px ${color}66, 0 6px 16px rgba(0,0,0,0.7)`,
        }}>
          {hook}
        </div>
        {sub && (
          <div style={{
            fontSize: 28,
            fontFamily: CFONT.body,
            fontWeight: 700,
            color,
            marginTop: 14,
            textShadow: `2px 2px 0 ${C.outline}, 0 0 20px ${color}66`,
            letterSpacing: '0.01em',
          }}>
            {sub}
          </div>
        )}
      </div>

      {/* Big icon in corner (if no stat) */}
      {!stat && icon && (
        <div style={{
          position: 'absolute',
          right: 60,
          top: '50%',
          transform: 'translateY(-50%) rotate(-8deg)',
          fontSize: 220,
          filter: `drop-shadow(0 0 60px ${color}88) drop-shadow(0 10px 20px rgba(0,0,0,0.7))`,
          zIndex: 1,
        }}>
          {icon}
        </div>
      )}

      {/* Bottom accent bar */}
      <div style={{
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        height: 12,
        background: `linear-gradient(90deg, ${color}, ${C.glow}, ${C.charBlue})`,
      }} />

      {/* Bottom-left AR logo */}
      <div style={{
        position: 'absolute',
        bottom: 32,
        left: 60,
        display: 'flex',
        alignItems: 'center',
        gap: 10,
      }}>
        <div style={{
          width: 42,
          height: 42,
          borderRadius: 8,
          background: `linear-gradient(135deg, ${C.danger}, ${C.charPurple})`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 18,
          fontFamily: CFONT.display,
          fontWeight: 800,
          color: '#fff',
        }}>AR</div>
        <span style={{
          fontSize: 18,
          fontFamily: CFONT.display,
          fontWeight: 700,
          color: C.textLight,
          letterSpacing: '0.1em',
          textTransform: 'uppercase',
        }}>AI RENDER LAB</span>
      </div>
    </AbsoluteFill>
  );
};

// ──── Per-video thumbnail wrappers ────

export const Thumb_Documentary: React.FC = () => (
  <Thumbnail
    hook="WHO RUNS THE WORLD?"
    sub="(Spoiler: Not you.)"
    badge="DOCUMENTARY"
    color={C.danger}
    icon="🌍"
  />
);

export const Thumb_Petrodollar: React.FC = () => (
  <Thumbnail
    hook="DITCH THE DOLLAR = GET INVADED"
    stat="4/4"
    statLabel="COUNTRIES TRIED"
    badge="PATTERN"
    color={C.charGold}
  />
);

export const Thumb_ChipWar: React.FC = () => (
  <Thumbnail
    hook="ONE ISLAND. 90% OF CHIPS."
    sub="What could go wrong?"
    stat="90%"
    statLabel="TAIWAN CONTROLS"
    badge="CHIP WAR"
    color={C.charBlue}
  />
);

export const Thumb_NordStream: React.FC = () => (
  <Thumbnail
    hook="WHO BLEW UP NORD STREAM?"
    sub="Nobody knows. (Sure.)"
    stat="$11B"
    statLabel="PIPE · GONE"
    badge="MYSTERY"
    color={C.charOrange}
  />
);

export const Thumb_BRICS: React.FC = () => (
  <Thumbnail
    hook="CENTRAL BANKS ARE PANIC BUYING GOLD"
    stat="1,136"
    statLabel="TONNES · 2022"
    badge="DE-DOLLARIZATION"
    color={C.charGold}
  />
);

export const Thumb_Oil: React.FC = () => (
  <Thumbnail
    hook="OIL WENT NEGATIVE"
    sub="They paid you to take it."
    stat="-$37"
    statLabel="PER BARREL"
    badge="WAIT WHAT"
    color={C.charOrange}
  />
);

export const Thumb_Surveillance: React.FC = () => (
  <Thumbnail
    hook="YOUR PHONE IS A SNITCH"
    sub="It's been this way since 2013."
    stat="8.5B"
    statLabel="SEARCHES / DAY"
    badge="BIG BROTHER"
    color={C.mystery}
  />
);

export const Thumb_WarMachine: React.FC = () => (
  <Thumbnail
    hook="THE US SPENDS THIS MUCH ON WAR"
    stat="$886B"
    statLabel="PER YEAR"
    badge="WAR MACHINE"
    color={C.danger}
  />
);
