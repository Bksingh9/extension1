# Video 01: "I Built a Full Video With One AI Prompt"

**Duration**: 8-10 minutes
**Type**: Demo / Tutorial
**Thumbnail**: Thumb01-PromptToVideo

---

## HOOK (0:00 - 0:30)

[Screen: Terminal on dark background]

"What if I told you this entire video -- the motion graphics, the transitions, the scenes, the final MP4 -- was built from a single prompt?"

[Show the actual prompt being typed into Claude Code]

"No After Effects. No Premiere. No timeline dragging. Just one prompt, one AI, and one render command."

[Cut to: Rendered video playing]

"Let me show you exactly how."

---

## INTRO (0:30 - 0:35)

[5-second branded intro animation]

---

## PART 1: THE TOOLS (0:35 - 2:00)

"This workflow uses two tools. That's it."

[Screen: Split layout -- Claude Code on left, Remotion on right]

"Claude Code is Anthropic's AI coding assistant. You give it a prompt, and it writes real code -- full files, full projects, debugged and working."

"Remotion is a React framework for creating videos programmatically. Instead of a timeline, you write React components. Instead of keyframes, you use JavaScript. And instead of exporting from a clunky GUI, you run one terminal command."

"Together, they turn a text description into a rendered MP4."

---

## PART 2: THE PROMPT (2:00 - 3:30)

"Here's the exact prompt I used."

[Screen: Show the full prompt -- scroll through it slowly]

"I described what I wanted:
- A 30-second motion graphics video
- Dark background, electric blue accents
- Seven scenes with specific content
- Reusable components
- Clean architecture"

"That's it. I didn't write a single line of code myself. I described the outcome I wanted, and Claude Code figured out how to build it."

---

## PART 3: WHAT CLAUDE CODE BUILT (3:30 - 5:30)

"Let's look at what came out."

[Screen: VS Code file tree]

"Claude Code created 29 files:
- A complete theme system with colors, fonts, spacing
- 12 reusable components -- things like TitleBlock, TerminalPanel, MetricStrip
- 7 scene files, each self-contained
- A main composition that sequences everything
- Animation utilities with spring physics, fades, slides, stagger effects"

[Screen: Walk through 2-3 component files briefly]

"This isn't template code. Every component uses Remotion's interpolate() and spring() functions for smooth motion. The timing system uses frame-based constants so you can adjust any scene without breaking others."

[Screen: Show the timings.ts file]

"The whole video is 945 frames at 30fps -- exactly 31.5 seconds."

---

## PART 4: THE RENDER (5:30 - 6:30)

"Now the magic part."

[Screen: Terminal]

```
npx remotion render src/index.ts MainVideo out/final.mp4
```

"One command. Remotion spins up a headless browser, renders every frame as a screenshot, stitches them together with ffmpeg, and outputs an MP4."

[Show render progress in terminal]

"945 frames rendered in about 40 seconds. The output is a 3.7 megabyte MP4 at 1920x1080."

[Play the final video full-screen for 10 seconds]

---

## PART 5: WHY THIS MATTERS (6:30 - 8:00)

"Here's why this workflow changes things."

"First -- speed. I went from idea to rendered video in under 15 minutes. Not hours. Not days. Minutes."

"Second -- iteration. Want to change a scene? Edit one file. Want different colors? Change the theme. Want longer timing? Adjust a number. Re-render. Done."

"Third -- it's all code. That means version control, reusable components, and no vendor lock-in. Your video project is a React app."

"Fourth -- cost. This entire video cost about 30 cents in API calls. Compare that to hiring a motion designer or paying for After Effects."

---

## OUTRO (8:00 - 8:30)

"The prompt, the code, and the rendered video are all linked in the description. You can clone the repo and render it yourself in five minutes."

"If you want to see me build something more complex -- like a full AI agent simulation or a data visualization video -- let me know in the comments."

"Subscribe if you want to see more AI-powered creation workflows. I'll see you in the next one."

[8-second branded outro]

---

## DESCRIPTION (see templates file)
## TAGS: Claude Code, Remotion, AI video, programmatic video, React video, motion graphics AI, tutorial
