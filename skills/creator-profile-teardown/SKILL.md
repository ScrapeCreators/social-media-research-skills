---
name: creator-profile-teardown
description: Use when the user wants to analyze a creator, influencer, founder, or brand social account and understand positioning, content pillars, outlier posts, hooks, format choices, audience reaction, and what can be copied or tested.
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

# Creator Profile Teardown

## Overview

Create a practical teardown of a creator or brand account. Explain what the account is about, why the content appears to work, what patterns repeat, and what the user should copy, adapt, or avoid.

## When to Use

Use this skill when the user asks to:

- analyze a creator or brand profile
- explain why an account is growing or performing
- create a swipe file from one creator
- identify content pillars, hooks, CTAs, and formats
- learn what to copy from a competitor or creator

## Workflow

1. Pull profile metadata and public links.
2. Pull recent posts and identify outliers.
3. Fetch transcripts/comments for the best examples if needed.
4. Identify positioning, promise, niche, audience, and recurring topics.
5. Extract hooks, formats, series, CTAs, and visual patterns.
6. Summarize lessons and recommended tests.

## Output Format

```markdown
# Creator Profile Teardown: {creator}

## Positioning
- Who they serve:
- Promise:
- Personality/voice:

## Content Pillars
| Pillar | Evidence | Example posts |
|---|---|---|

## Outlier Posts
| Post | Metric | Lift/why it matters | Pattern |
|---|---:|---|---|

## Hooks and Formats to Steal
- ...

## What Not to Copy
- ...

## Tests for Us
1. ...
```

## Common Pitfalls

- Do not reduce the teardown to a profile summary. Find repeatable mechanics.
- Do not copy personal details or private information.
- Do not assume causation from performance. Say what the evidence suggests.
