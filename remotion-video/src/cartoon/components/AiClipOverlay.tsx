import React from 'react';
import { AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame } from 'remotion';
import { fadeIn } from '../animation';

/**
 * Overlays AI-generated video clips as cinematic B-roll behind data components.
 * Falls back gracefully if the clip file doesn't exist (shows nothing).
 *
 * Usage:
 *   <AiClipOverlay chapterId="ch1_petrodollar" opacity={0.35} />
 *
 * Generate clips with:
 *   python scripts/ai-video-gen.py --chapter ch1_petrodollar --model wan2.2
 */
export const AiClipOverlay: React.FC<{
  chapterId: string;
  opacity?: number;
  blendMode?: string;
  blur?: number;
  delay?: number;
}> = ({ chapterId, opacity = 0.35, blendMode = 'normal', blur = 2, delay = 0 }) => {
  const frame = useCurrentFrame();
  const op = fadeIn(frame, delay, 20) * opacity;

  // Try to load the AI-generated clip
  // If the file doesn't exist, Remotion will show an error in dev but skip in prod
  const src = staticFile(`ai-clips/${chapterId}.mp4`);

  return (
    <AbsoluteFill
      style={{
        opacity: op,
        mixBlendMode: blendMode as any,
        filter: blur > 0 ? `blur(${blur}px)` : 'none',
      }}
    >
      <OffthreadVideo
        src={src}
        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        muted
      />
    </AbsoluteFill>
  );
};
