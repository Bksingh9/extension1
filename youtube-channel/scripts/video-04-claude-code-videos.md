# Video 04: "Claude Code Builds Entire Videos -- Here's How"

**Duration**: 10-12 minutes
**Type**: Deep Dive / Tutorial
**Thumbnail**: Thumb04-ClaudeCode

---

## HOOK (0:00 - 0:30)

[Screen: Split -- prompt on left, rendered video on right]

"I gave Claude Code a 200-word description of a video I wanted. It created 29 files, 12 reusable components, 7 animated scenes, a full theme system, and a working Remotion project."

"Then I ran one command and got a rendered MP4."

"This is the most productive creative workflow I've ever used. Let me break it down."

---

## INTRO (0:30 - 0:35)

[Branded intro]

---

## PART 1: WHY AI + VIDEO WORKS (0:35 - 2:00)

"Video creation has always had a high barrier. You need design skills, animation skills, timeline knowledge, and expensive software."

"But here's the thing -- motion graphics are just math. Opacity goes from 0 to 1. Elements move from point A to point B. Colors, timing, easing curves. It's all numbers."

"And numbers are exactly what AI is good at generating."

"Claude Code doesn't just suggest code. It writes complete, working files. It creates folder structures, handles imports, debugs errors, and renders output."

"So the question isn't 'can AI help with video?' It's 'how much can you get out of a single prompt?'"

---

## PART 2: THE PROMPT ENGINEERING (2:00 - 4:30)

"The quality of your output depends entirely on the quality of your prompt."

"Here's what I include in every video prompt:"

[Screen: Annotated prompt breakdown]

"1. VIDEO SPEC -- resolution, fps, duration, composition name"
"2. STORY STRUCTURE -- every scene with purpose, message, visuals, duration"
"3. STYLE SYSTEM -- colors, fonts, spacing, motion style"
"4. COMPONENT LIST -- what reusable pieces to build"
"5. QUALITY RULES -- no placeholders, no dead code, no monolithic files"

"The more specific you are about architecture, the better the output. Don't just say 'make it look good.' Say 'dark background #0a0a0f, primary accent #3b82f6, spring animations for entrances, 60px safe margins.'"

"Think of the prompt as a creative brief for a senior developer. Clear constraints produce better results."

---

## PART 3: LIVE BUILD (4:30 - 8:00)

[Screen: Claude Code terminal -- real-time]

"Let me build a brand new video right now. Live."

[Type prompt into Claude Code]

"I'm asking for a 20-second product launch teaser. Three scenes: logo reveal, feature showcase, CTA."

[Show Claude Code working -- creating files, installing deps]

"Watch -- it's creating the theme first, then components, then scenes, then wiring the composition."

[Show file tree growing in real-time]

"Now let's render it."

```
npx remotion render src/index.ts ProductTeaser out/teaser.mp4
```

[Show render completing]

"20 seconds of polished motion graphics. Total time from prompt to MP4: about 8 minutes. Total cost: about 40 cents in API calls."

---

## PART 4: EDITING AND ITERATING (8:00 - 10:00)

"The real power is iteration."

"Don't like the timing? Open timings.ts, adjust the frame counts, re-render."
"Want different colors? Change theme.ts. Every component reads from it."
"Need a new scene? Ask Claude Code to add one. It knows the existing architecture."

"Because everything is code, you can also:
- Git commit each version
- A/B test different visual approaches
- Create variants for different platforms (16:9, 9:16, 1:1)
- Parameterize content for template-based generation"

"This is video creation with a developer's workflow."

---

## OUTRO (10:00 - 10:30)

"The prompt template I use is linked in the description. Modify it for your own videos."

"Next week: building a full YouTube thumbnail generator with Remotion. Subscribe to see that."

[Branded outro]

---

## TAGS: Claude Code, AI video creation, Remotion AI, prompt engineering, AI motion graphics, Claude Anthropic
