---
name: content-repurposing
description: Use when the user wants to turn public social videos, transcripts, posts, or creator research into reusable content assets such as LinkedIn posts, X threads, short-form scripts, newsletters, blog outlines, carousels, or content calendars.
allowed-tools: Bash, Read, Write, WebFetch

version: 1.1.0
author: ScrapeCreators
license: MIT
homepage: https://scrapecreators.com
repository: https://github.com/ScrapeCreators/social-media-research-skills
metadata:
  openclaw:
    requires:
      env:
        - SCRAPECREATORS_API_KEY
    primaryEnv: SCRAPECREATORS_API_KEY
    homepage: https://scrapecreators.com
    tags:
      - social-media
      - research
      - scrapecreators
---

# Content Repurposing

## Overview

Turn social research and transcripts into reusable content. This skill works best after `transcript-intelligence`, `outlier-post-finder`, or `creator-profile-teardown`, but it can also start directly from URLs.

## Before You Start

- Data comes from ScrapeCreators. Load `scrapecreators-api` for endpoint details and run every call through its helper `scripts/sc.py`, which handles the balance check, cost dry-run, pagination (`--pages N`), caching and the credit budget.
- Locate the helper with `SC="$(ls {.claude,.agents,$HOME/.claude,$HOME/.agents}/skills/scrapecreators-api/scripts/sc.py 2>/dev/null | head -1)"`, then run `python3 "$SC" balance` first. If it reports a missing key, a blocked network or no credits, tell the user what to fix and stop the data part. Never fill gaps with invented posts, numbers or quotes.
- Cost: usually 0 to a few credits, because this skill mostly works on material the user already has. Only fetch transcripts or posts that are missing. Above ~25 credits for the whole job, give the user the estimate in one line and wait for a yes.
- Write the deliverable in the user's language. Keep quotes, hooks and comments verbatim in their original language.

## When to Use

Use this skill when the user asks to:

- turn videos or transcripts into posts
- repurpose TikToks, Reels, Shorts, podcasts, or webinars
- create LinkedIn posts, X threads, scripts, newsletters, or blog outlines
- build a content calendar from winning social ideas
- adapt a competitor/creator pattern without plagiarizing

## Workflow

1. Gather source material: URLs, transcripts, posts, or research report.
2. Extract content atoms: hooks, stories, claims, frameworks, examples, data points, CTAs.
3. Choose output formats and platform constraints.
4. Rewrite for the user's voice and audience.
5. Keep attribution/internal notes when ideas are inspired by a source.
6. Produce ready-to-use drafts plus optional variants.

## Output Format

```markdown
# Repurposed Content Pack

## Source Material
- [source](url)

## Content Atoms
| Atom | Source | Best format |
|---|---|---|

## LinkedIn Posts
1. ...

## X Threads
1. ...

## Short-Form Scripts
### Script 1
- Hook:
- Body:
- CTA:

## Newsletter / Blog Ideas
- ...
```

## Common Pitfalls

- Do not plagiarize. Adapt structure and insight, not unique wording unless quoting with attribution.
- Do not flatten every platform into the same format.
- Do not lose the original hook if it is the strongest part.
