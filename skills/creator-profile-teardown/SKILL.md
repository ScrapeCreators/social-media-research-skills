---
name: creator-profile-teardown
description: Use when the user wants to analyze a creator, influencer, founder, or brand social account and understand positioning, content pillars, outlier posts, hooks, format choices, audience reaction, and what can be copied or tested.
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

# Creator Profile Teardown

## Overview

Create a practical teardown of a creator or brand account. Explain what the account is about, why the content appears to work, what patterns repeat, and what the user should copy, adapt, or avoid.

## Before You Start

- Data comes from ScrapeCreators. Load `scrapecreators-api` for endpoint details and run every call through its helper `scripts/sc.py`, which handles the balance check, cost dry-run, pagination (`--pages N`), caching and the credit budget.
- Locate the helper with `SC="$(ls {.claude,.agents,$HOME/.claude,$HOME/.agents}/skills/scrapecreators-api/scripts/sc.py 2>/dev/null | head -1)"`, then run `python3 "$SC" balance` first. If it reports a missing key, a blocked network or no credits, tell the user what to fix and stop the data part. Never fill gaps with invented posts, numbers or quotes.
- Cost: about 1 credit for the profile, 1 to 3 for recent posts, plus 1 per transcript or comment page for the top posts. `/v1/find-social-profiles` costs 10. Above ~25 credits for the whole job, give the user the estimate in one line and wait for a yes.
- Write the deliverable in the user's language. Keep quotes, hooks and comments verbatim in their original language.

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

## Useful Endpoints

- Profile and feed endpoints per platform from `scrapecreators-api` (for example `/v1/tiktok/profile` + `/v3/tiktok/profile/videos`, `/v1/instagram/profile` + `/v2/instagram/user/posts`, `/v1/youtube/channel` + `/v1/youtube/channel-videos`)
- `/v1/find-social-profiles` (10 credits) to find the creator's other platforms from one handle
- Link-in-bio routes (`/v1/linktree`, `/v1/komi`, `/v1/pillar`, `/v1/linkbio`, `/v1/linkme`) and `/v1/tiktok/user/showcase` or `/v1/amazon/shop` for offers and monetization
- Transcript and comment routes for the top posts only

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
