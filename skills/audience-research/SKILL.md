---
name: audience-research
description: Use when the user wants to evaluate a creator, influencer, or brand audience using public profile signals, TikTok audience demographics, follower/following data, comments, geography, language, and content fit. Helps judge sponsorship and market fit.
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

# Audience Research

## Overview

Evaluate whether a creator or social account reaches the right audience. This skill combines available public profile metrics, TikTok audience demographics, regional signals, follower/following data when available, comments, language, and content topics.

## Before You Start

- Data comes from ScrapeCreators. Load `scrapecreators-api` for endpoint details and run every call through its helper `scripts/sc.py`, which handles the balance check, cost dry-run, pagination (`--pages N`), caching and the credit budget.
- Locate the helper with `SC="$(ls {.claude,.agents,$HOME/.claude,$HOME/.agents}/skills/scrapecreators-api/scripts/sc.py 2>/dev/null | head -1)"`, then run `python3 "$SC" balance` first. If it reports a missing key, a blocked network or no credits, tell the user what to fix and stop the data part. Never fill gaps with invented posts, numbers or quotes.
- Cost: 1 credit per profile, feed or comment page. `/v1/tiktok/user/audience` costs 26 per creator. Above ~25 credits for the whole job, give the user the estimate in one line and wait for a yes.
- Write the deliverable in the user's language. Keep quotes, hooks and comments verbatim in their original language.

## When to Use

Use this skill when the user asks to:

- check if a creator's audience fits a market
- compare audience fit across creators
- find US-heavy, country-specific, or niche-specific creators
- evaluate sponsorship/influencer opportunities
- understand who appears to engage with an account

## Useful Sources

- `/v1/tiktok/user/audience`: audience countries, **26 credits** per creator
- `/v1/tiktok/profile/region`: the creator's own country
- `/v1/detect-age-gender`: AI estimate of the creator's age range and gender from the profile photo (not the audience)
- profile endpoints across platforms
- `/v1/tiktok/user/followers` and `/v1/tiktok/user/following` (paginate with `min_time`) for spot checks of follower quality
- comments on recent posts
- link-in-bio pages and creator shops for niche signals

## Workflow

1. Pull profile and available audience/demographic data.
2. Pull recent content and comments if audience intent matters.
3. Extract region, language, niche, product/category, and community signals.
4. Score audience fit against the user's target market.
5. Label confidence based on the strength of public data.

## Output Format

```markdown
# Audience Research: {creator}

## Fit Summary
- Target market:
- Fit score: High/Medium/Low
- Confidence: High/Medium/Low

## Evidence
| Signal | Evidence | Source |
|---|---|---|

## Audience Notes
- Geography:
- Language:
- Niche/content fit:
- Comment quality:

## Sponsorship Recommendation
- Good fit / Maybe / Poor fit
- Why:
```

## Common Pitfalls

- Do not infer exact demographics from vibes. Use available evidence and label assumptions.
- Do not overpromise audience details for platforms that do not expose them publicly.
- Do not ignore mismatch between creator location and audience location.
- Do not present `/v1/detect-age-gender` output as fact. It is an AI guess from one photo, about the creator, not the audience.
- Never infer sensitive traits such as ethnicity, health, religion, politics or sexual orientation.
- When comparing many creators, ask before running the 26-credit audience call on each one. Start with free-ish signals (profile region, comment language) and buy demographics only for the shortlist.
