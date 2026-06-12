---
name: content-repurposing
description: Use when the user wants to turn public social videos, transcripts, posts, or creator research into reusable content assets such as LinkedIn posts, X threads, short-form scripts, newsletters, blog outlines, carousels, or content calendars.
allowed-tools: Bash, Read, Write, WebFetch

version: 1.0.0
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
