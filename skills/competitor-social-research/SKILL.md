---
name: competitor-social-research
description: Use when the user wants to research competitors' social media strategy, compare brands or creators, find what content is working in a niche, identify content gaps, or produce a practical social strategy brief from public social data.
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

# Competitor Social Research

## Overview

Analyze what competitors are doing on social and what appears to be working. This skill combines profile data, recent posts, outlier analysis, transcripts, and optionally comments to produce a practical competitor brief.

## Before You Start

- Data comes from ScrapeCreators. Load `scrapecreators-api` for endpoint details and run every call through its helper `scripts/sc.py`, which handles the balance check, cost dry-run, pagination (`--pages N`), caching and the credit budget.
- Locate the helper with `SC="$(ls {.claude,.agents,$HOME/.claude,$HOME/.agents}/skills/scrapecreators-api/scripts/sc.py 2>/dev/null | head -1)"`, then run `python3 "$SC" balance` first. If it reports a missing key, a blocked network or no credits, tell the user what to fix and stop the data part. Never fill gaps with invented posts, numbers or quotes.
- Cost: per competitor and platform about 1 credit for the profile plus 1 per feed page; transcripts and comments for the winners add 1 each. Above ~25 credits for the whole job, give the user the estimate in one line and wait for a yes.
- Write the deliverable in the user's language. Keep quotes, hooks and comments verbatim in their original language.

## When to Use

Use this skill when the user asks to:

- compare competitors on TikTok, Instagram, YouTube, LinkedIn, Facebook, X, Threads, or other social platforms
- find what content is working in a niche
- benchmark posting frequency, formats, topics, and engagement
- identify content gaps or opportunities
- build a social strategy from competitor research

## Workflow

1. **Define competitors and platforms**
   - Use provided handles/URLs.
   - If only company names are provided, search profiles first and confirm likely matches when ambiguity matters.

2. **Fetch profile snapshots**
   - Followers/subscribers
   - Bio/positioning
   - Links
   - Verification/public metadata

3. **Fetch recent content**
   - Pull comparable recent windows per competitor.
   - Track source URLs, dates, captions, formats, and metrics.

4. **Find outliers per competitor**
   - Use each account's own median baseline.
   - Do not compare raw views between a huge brand and a small brand without context.

5. **Analyze content strategy**
   - Content pillars
   - Formats
   - Hook styles
   - Posting cadence
   - Offers/CTAs
   - Use of founder/creator personality
   - Community/comment patterns

6. **Find gaps and opportunities**
   Look for:
   - topics competitors avoid
   - formats that overperform but few competitors use
   - unanswered audience questions
   - weak hooks or repetitive content
   - platform whitespace

## Useful ScrapeCreators Endpoints

Use the relevant profile/feed/detail/transcript/comment endpoints from `scrapecreators-api`. Common routes include:

- TikTok: `/v1/tiktok/profile`, `/v3/tiktok/profile/videos`
- Instagram: `/v1/instagram/profile`, `/v2/instagram/user/posts`, `/v1/instagram/user/reels`
- YouTube: `/v1/youtube/channel`, `/v1/youtube/channel-videos`, `/v1/youtube/channel/shorts`
- LinkedIn: `/v1/linkedin/company`, `/v1/linkedin/company/posts`
- Facebook: `/v1/facebook/profile`, `/v1/facebook/profile/posts`, `/v1/facebook/profile/reels`
- X/Twitter: `/v1/twitter/profile`, `/v1/twitter/user-tweets`
- Threads: `/v1/threads/profile`, `/v1/threads/user/posts`
- Bluesky: `/v1/bluesky/profile`, `/v1/bluesky/user/posts`
- Finding the right accounts: `/v1/tiktok/search/users`, `/v1/instagram/search/profiles`, `/v1/youtube/search`, or `/v1/find-social-profiles` (10 credits) to map one known handle to the brand's other platforms
- Paid side: hand off to `ad-library-teardown` when the user also wants the competitors' ads

## Output Format

```markdown
# Competitor Social Research Brief

## Executive Summary
- Biggest opportunity:
- Competitor to study closest:
- Content format to test first:

## Competitor Snapshot
| Competitor | Platforms | Audience size | Posting cadence | Best-performing format | Notes |
|---|---|---:|---|---|---|

## What Is Working
### Competitor A
- Content pillars:
- Outlier examples:
- Hooks/formats:

## Cross-Competitor Patterns
1. ...
2. ...

## Gaps and Opportunities
| Opportunity | Evidence | Suggested test |
|---|---|---|

## Recommended Content Tests
1. ...
2. ...
3. ...

## Sources
- [Post/profile/ad](url)
```

## Common Pitfalls

- Do not compare competitors only by follower count. Engagement and outlier lift matter more.
- Do not mix platforms without platform context. A good LinkedIn post and good TikTok are different artifacts.
- Do not assume a profile match from a company name if multiple brands share the name.
- Do not present competitor strategy as fact when it is inferred from public content. Say "appears to" or "suggests".
