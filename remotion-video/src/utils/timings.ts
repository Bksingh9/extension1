export const FPS = 30;

// Scene durations in frames
export const SCENE = {
  hook: { start: 0, duration: 105 },         // 3.5s
  problem: { start: 105, duration: 135 },     // 4.5s
  promptToPlan: { start: 240, duration: 165 },// 5.5s
  remotion: { start: 405, duration: 165 },    // 5.5s
  terminal: { start: 570, duration: 135 },    // 4.5s
  benefits: { start: 705, duration: 135 },    // 4.5s
  finale: { start: 840, duration: 105 },      // 3.5s
} as const;

export const TOTAL_FRAMES = 945; // 31.5 seconds
