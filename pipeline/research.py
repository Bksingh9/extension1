"""Research stub.

The real research workflow runs through Claude Code + the Playwright MCP
server at episode-creation time (see pipeline/prompts/new-episode.md).
This file exists as a placeholder so episode automation can call into a
single entry point if you later want to script research outside Claude.
"""
from __future__ import annotations

import sys


def main(topic: str) -> None:
    print(f"Research stub for topic: {topic!r}")
    print("Run the new-episode prompt with Claude Code + Playwright MCP instead.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python pipeline/research.py <topic>")
    main(sys.argv[1])
