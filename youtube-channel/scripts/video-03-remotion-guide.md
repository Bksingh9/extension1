# Video 03: "Remotion in 20 Minutes -- Complete Beginner Guide"

**Duration**: 18-22 minutes
**Type**: Tutorial
**Thumbnail**: Thumb03-RemotionGuide

---

## HOOK (0:00 - 0:25)

"By the end of this video, you'll be able to create, animate, and render production-quality videos using nothing but React and TypeScript."

"No video editing software. No timeline. Just code."

[Quick montage of 5 different Remotion outputs]

---

## INTRO (0:25 - 0:30)

[Branded intro]

---

## PART 1: WHAT IS REMOTION? (0:30 - 2:00)

"Remotion is a framework that lets you create videos using React components."

"Think of it this way: every frame of your video is a React component rendered at a specific point in time. Frame 0 is your first frame. Frame 30 is one second in at 30fps. You use the frame number to control everything -- opacity, position, scale, color."

"Why would you want this?"

"Because code is infinitely more flexible than a GUI timeline. You can loop things, randomize things, pull in data, create templates, version control your videos, and render them from a terminal."

---

## PART 2: SETUP (2:00 - 4:00)

[Screen: Terminal]

"Let's build a project from scratch."

```
npm init -y
npm install remotion @remotion/cli react react-dom typescript
```

"Create your entry point:"

[Walk through: src/index.ts, src/Root.tsx, basic Composition]

"Key concepts:
- Composition: defines your video's dimensions, fps, and duration
- component: the React component that renders each frame
- durationInFrames: total frames (fps × seconds)"

```
npx remotion studio src/index.ts
```

"This opens the Remotion Studio -- a browser preview where you can scrub through your video frame by frame."

---

## PART 3: YOUR FIRST ANIMATION (4:00 - 8:00)

"The two most important functions in Remotion:"

"1. `useCurrentFrame()` -- returns the current frame number"
"2. `interpolate()` -- maps a frame range to an output range"

[Live code: fade-in example]

```tsx
const frame = useCurrentFrame();
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateRight: 'clamp',
});
```

"Frame 0 → opacity 0. Frame 30 → opacity 1. Everything in between is interpolated."

[Live code: slide-up example, scale example]

"For bouncy, physical motion, use `spring()`:"

```tsx
const scale = spring({ frame, fps, config: { damping: 12 } });
```

"Springs feel natural. They overshoot slightly and settle. Use them for entrances and emphasis."

---

## PART 4: SEQUENCING SCENES (8:00 - 12:00)

"Real videos have multiple scenes. Remotion handles this with `<Sequence>`."

[Build a 3-scene video live]

```tsx
<Sequence from={0} durationInFrames={90}>
  <IntroScene />
</Sequence>
<Sequence from={90} durationInFrames={120}>
  <MainScene />
</Sequence>
<Sequence from={210} durationInFrames={90}>
  <OutroScene />
</Sequence>
```

"Each Sequence resets the frame counter for its children. So inside MainScene, frame 0 is the start of that scene, not the start of the video."

"Pro tip: define your timings in a separate file as constants. That way you can adjust pacing without hunting through components."

---

## PART 5: BUILDING COMPONENTS (12:00 - 16:00)

"The real power of Remotion is reusable components."

[Build these live:]
- TitleBlock with spring entrance
- TerminalPanel with typing effect
- InfoCard with staggered reveal

"The pattern: every component takes a `delay` prop, uses `useCurrentFrame()`, and offsets its animations by the delay. This gives you stagger effects for free."

---

## PART 6: RENDERING (16:00 - 18:00)

"Preview looks good? Let's render."

```
npx remotion render src/index.ts MyVideo out/video.mp4
```

"Remotion opens a headless Chrome, screenshots every frame, and encodes with ffmpeg."

"Options:
- `--quality` for JPEG quality (affects file size)
- `--scale` for resolution multiplier
- `--codec` for h264, h265, vp8, vp9
- `--concurrency` for parallel frame rendering"

"A 30-second video at 30fps renders in about 30-60 seconds on a modern machine."

---

## PART 7: TIPS AND PATTERNS (18:00 - 20:00)

"Things I wish I knew when I started:"

"1. Always use `extrapolateLeft: 'clamp', extrapolateRight: 'clamp'` with interpolate. Otherwise values go outside your range."

"2. AbsoluteFill is your friend. It fills the entire composition area. Stack them for layered effects."

"3. Build a theme file early. Colors, fonts, spacing. Reference them everywhere."

"4. Test with fewer frames first. Set durationInFrames to 30 while building, then increase for the final render."

"5. Remotion supports Stills too. Use them for generating thumbnails, social cards, and OG images."

---

## OUTRO (20:00 - 20:30)

"The full project code is in the description. Clone it, modify it, render it."

"Next video: I'll show you how to use Claude Code to generate entire Remotion projects from a single prompt."

[Branded outro]

---

## TAGS: Remotion tutorial, React video, programmatic video, TypeScript animation, Remotion beginner guide, code to video
