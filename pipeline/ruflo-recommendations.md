# Ruflo plugin recommendations for The Dossier + The Long Light

> Ruflo (formerly Claude Flow) is a multi-agent orchestration plugin
> system for Claude Code — MIT, by ruvnet. 32+ plugins. Most are
> overkill for a content pipeline, but four of them genuinely fit
> what we're doing here. This doc tells you which to install, what
> each replaces or augments, and the install order.
>
> **Source:** https://github.com/ruvnet/ruflo

## TL;DR install (4 plugins, install in this order)

Run these slash commands in a fresh Claude Code session in the repo root:

```
/plugin marketplace add ruvnet/ruflo
/plugin install ruflo-core@ruflo
/plugin install ruflo-loop-workers@ruflo
/plugin install ruflo-rag-memory@ruflo
/plugin install ruflo-swarm@ruflo
```

Skip everything else (federation, intelligence, daa, sparc, jujutsu, security-audit, etc.) until you have a real reason. The first three episodes don't need them.

## Why these four (and not the other 28)

### `ruflo-core` — required base

The foundation. Everything else depends on it. ~5 MB, no hard runtime cost when idle.

### `ruflo-loop-workers` — replaces nothing yet, automates the weekly trend scan

We have `pipeline/prompts/weekly-trend-scan.md` ready to run every Monday. Nobody runs it. With `ruflo-loop-workers`, you set a cron-style trigger:

```
@cron 0 9 * * 1 use the prompt at pipeline/prompts/weekly-trend-scan.md
                and save findings to channel/trend-scan-YYYY-MM-DD.md
```

Now every Monday at 9:00 you find a fresh trend report waiting in your repo. **This is the single highest-leverage piece of Ruflo for us** — content channels live and die on trend velocity, and a manual weekly scan slips after week 3.

For a native equivalent that doesn't need the plugin installed, see `pipeline/loop-trend-scan.sh` (committed alongside this doc).

### `ruflo-rag-memory` — augments per-episode research

We have `episodes/NNN/research.md` per episode. None of them know what the others have already verified. When Episode 5 needs the Belavezha Accords date, it has to re-Playwright the same Wikipedia page.

`ruflo-rag-memory` provides hybrid (vector + graph) search across all our research files. Add a `mcp__ruflo__memory_search` call at the top of every new-episode prompt and the agent answers from prior research first, hits the web only for new facts. Saves time *and* enforces consistency (e.g. "we always cite Andreotti's 127 caches, not 139").

### `ruflo-swarm` — parallelize per-episode asset generation

Phase 2/3/5 of every episode produces three independent files: `voice-notes.md`, `image-prompts.md`, `thumbnail-prompts.md`. Right now I write them serially. With `ruflo-swarm` you fan out three agents in parallel, each given the script + the spec for one of the files. ~3× faster per episode.

Native equivalent: I can already do this in a single message with three `Agent` tool calls in parallel. Ruflo-swarm is mostly the *coordinator* — useful when the three agents need to talk to each other (e.g. the thumbnail agent reading the voice-notes agent's output mid-flight). For our episode workflow that's overkill; serial-with-a-cache covers it.

## What I'd skip and why

| Plugin | Why skip |
|---|---|
| ruflo-federation | Multi-machine agent comms. We have one machine. |
| ruflo-intelligence / ruflo-daa | Self-learning agent behavior. Adds complexity without clear ROI for content. |
| ruflo-sparc / ruflo-ddd / ruflo-adr | Software-engineering methodology plugins. Not relevant. |
| ruflo-testgen / ruflo-jujutsu | Test generation, git diff scoring. We have ~500 lines of Python; not the bottleneck. |
| ruflo-security-audit / ruflo-aidefence | Useful for code, not content. |
| ruflo-browser | Duplicates Playwright MCP we already have configured (when not blocked by sandbox network). |
| ruflo-knowledge-graph | Overlaps with rag-memory; pick one. rag-memory is enough. |
| ruflo-ruvllm / ruflo-agentdb / ruflo-ruvector | Local LLM routing + advanced vector search. Not the bottleneck. |
| ruflo-docs | Auto-generates docs. We hand-write our docs. |
| ruflo-goals | Goal tracking. We have a niche.md backlog; that's enough. |
| ruflo-autopilot | Run agents autonomously in a loop. Risky for a content channel — bad scripts ship. Don't enable. |

## Install caveats

- **Plugin installation runs in your interactive Claude Code session, not via Bash.** I can write this doc but I cannot run `/plugin install` from here. You install on the machine where you actually use Claude Code.
- Some of Ruflo's MCP servers spawn background processes. Watch your machine's load if you install many at once.
- The marketplace add command adds a *trust* relationship to ruvnet's repo. Read `https://github.com/ruvnet/ruflo` before granting that trust.

## After install — first concrete action

Configure `ruflo-loop-workers` to run the weekly trend scan:

```
@cron 0 9 * * 1
  Read pipeline/prompts/weekly-trend-scan.md.
  Run the prompt against the niches in channel/niche.md and the-long-light/niche.md.
  Save the result to channel/trend-scan-YYYY-MM-DD.md AND
                    the-long-light/trend-scan-YYYY-MM-DD.md.
  Commit with message "weekly trend scan, YYYY-MM-DD" but do not push.
```

The first run is the test of whether the install was worth it. If after week 3 the trend scans are producing topics we'd genuinely cover, the install paid for itself.
