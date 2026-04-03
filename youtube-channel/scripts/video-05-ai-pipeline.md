# Video 05: "The AI Video Pipeline: Idea → Script → Scenes → Rendered MP4"

**Duration**: 12-15 minutes
**Type**: Workflow / Systems
**Thumbnail**: Thumb05-Workflow

---

## HOOK (0:00 - 0:30)

"Most people think AI video means typing a prompt into RunwayML and hoping the output looks okay."

"I built something different. A pipeline where AI handles every stage -- writing the script, structuring scenes, generating code, and rendering the final video. And I control every step."

"Here's the full pipeline."

---

## INTRO (0:30 - 0:35)

[Branded intro]

---

## PART 1: THE FOUR STAGES (0:35 - 2:30)

"Every video goes through four stages:"

[Screen: Pipeline diagram animated]

"Stage 1: IDEATION -- one sentence describing what the video should be"
"Stage 2: STRUCTURING -- Claude Code turns the idea into scenes, timing, and architecture"
"Stage 3: GENERATION -- Claude Code writes all React components and animation code"
"Stage 4: RENDERING -- Remotion compiles everything into a final MP4"

"Most AI video tools only do stage 3 or 4. They skip the structuring entirely, which is why the output feels random and uncontrolled."

"The secret is that stage 2 -- structuring -- is the most important. A well-structured plan produces a well-structured video."

---

## PART 2: STAGE 1 — IDEATION (2:30 - 3:30)

"Start with one sentence."

"Examples:
- 'A 30-second launch video for a developer tool'
- 'An explainer showing how AI agents simulate markets'
- 'A channel intro with motion graphics and terminal aesthetics'"

"One sentence is enough because the AI will expand it. But make sure it captures the core message and audience."

---

## PART 3: STAGE 2 — STRUCTURING (3:30 - 6:00)

"This is where Claude Code earns its keep."

"I give it my one-sentence idea plus a structuring prompt:"

[Screen: Show structuring prompt]

"The output is a complete video architecture:
- Scene breakdown with purposes and durations
- Component list
- Theme and style tokens
- Timing constants
- Story arc with narrative flow"

"This takes about 2 minutes and costs pennies."

"Here's what makes this different from just asking an AI to 'make a video': I can review the structure before any code is written. I can say 'make scene 3 longer' or 'add a benefits section.' I'm directing, not just prompting."

---

## PART 4: STAGE 3 — GENERATION (6:00 - 9:00)

"Once the structure is locked, Claude Code generates the full project."

[Screen: Watch files being created]

"It follows Remotion best practices automatically:
- AbsoluteFill for layout
- interpolate() and spring() for motion
- Sequence for scene management
- Clean imports and exports
- No dead code"

"The typical output for a 30-second video:
- 25-30 files
- 10-15 reusable components
- 5-8 scenes
- 1 theme file, 1 timing file, 1 animation utilities file
- 1 main composition that wires everything together"

"Total generation time: 5-8 minutes."

---

## PART 5: STAGE 4 — RENDERING (9:00 - 10:30)

"The simplest stage."

```
npx remotion render src/index.ts MainVideo out/final.mp4
```

"Remotion renders each frame with headless Chrome, encodes with ffmpeg."

"30-second video at 30fps: ~40 seconds to render"
"60-second video at 30fps: ~90 seconds to render"
"Same videos at 60fps: roughly double"

"The output is a standard MP4 you can upload anywhere."

---

## PART 6: THE NUMBERS (10:30 - 12:00)

[Screen: Metric comparison table]

"Let's compare this pipeline to traditional motion graphics:"

"| Metric | Traditional | AI Pipeline |"
"| Time to first draft | 2-5 days | 15 minutes |"
"| Cost per video | $500-5000 | $0.30-3.00 |"
"| Iteration speed | Hours | Minutes |"
"| Version control | No | Git |"
"| Reusable components | Sometimes | Always |"
"| Render control | Software-dependent | Terminal command |"

"I'm not saying this replaces professional motion designers for high-end work. But for YouTube content, product demos, social clips, and educational videos? This pipeline is faster, cheaper, and more controllable."

---

## PART 7: BUILDING YOUR OWN PIPELINE (12:00 - 13:30)

"Here's how to start:"

"1. Install Claude Code and Remotion"
"2. Use my prompt template (linked below) for your first video"
"3. Start with a simple 15-second video to learn the system"
"4. Build your own component library over time"
"5. Create templates for recurring video types"

"After 3-4 videos, you'll have a reusable library of components. New videos become faster because you're assembling, not building from scratch."

---

## OUTRO (13:30 - 14:00)

"The full pipeline -- templates, components, example projects -- is on GitHub. Link in the description."

"If you want to see me build a specific type of video with this pipeline, comment below."

"Subscribe for more AI-powered creation workflows."

[Branded outro]

---

## TAGS: AI video pipeline, automated video creation, Claude Code Remotion, AI workflow, programmatic video, video automation
