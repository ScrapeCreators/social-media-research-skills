---
name: trend-discovery
description: Use when the user wants to discover trending social topics, hashtags, sounds, posts, reels, shorts, creators, or formats in a niche. Searches public trend and discovery endpoints, ranks evidence, and turns trends into practical content angles.
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

# Trend Discovery

## Overview

Find trends worth acting on. This skill is for social media trend research across TikTok, Instagram, YouTube, Reddit, Pinterest, and other public sources. The output should separate real evidence from vague "this is trending" claims.

## Before You Start

- Data comes from ScrapeCreators. Load `scrapecreators-api` for endpoint details and run every call through its helper `scripts/sc.py`, which handles the balance check, cost dry-run, pagination (`--pages N`), caching and the credit budget.
- Locate the helper with `SC="$(ls {.claude,.agents,$HOME/.claude,$HOME/.agents}/skills/scrapecreators-api/scripts/sc.py 2>/dev/null | head -1)"`, then run `python3 "$SC" balance` first. If it reports a missing key, a blocked network or no credits, tell the user what to fix and stop the data part. Never fill gaps with invented posts, numbers or quotes.
- Cost: 1 credit per trend or search page. Two to four sources usually stay under 15 credits. Above ~25 credits for the whole job, give the user the estimate in one line and wait for a yes.
- Write the deliverable in the user's language. Keep quotes, hooks and comments verbatim in their original language.

## When to Use

Use this skill when the user asks to:

- find trends in a niche or category
- discover trending TikTok sounds, hashtags, creators, or videos
- find trending Instagram Reels or YouTube Shorts ideas
- build a weekly trend brief
- decide what content formats or angles to jump on

## Useful Sources

| Signal | Endpoint examples |
|---|---|
| TikTok trending feed | `/v1/tiktok/get-trending-feed` |
| TikTok popular hashtags | `/v1/tiktok/hashtags/popular` (`period`, `countryCode`, `industry`); on 404 fall back to `/v1/tiktok/search/hashtag` |
| TikTok sounds | sound IDs from trending or search results, then `/v1/tiktok/song` and `/v1/tiktok/song/videos` (`clipId`) |
| TikTok autocomplete | `/v1/tiktok/search/suggestions` |
| TikTok search | `/v1/tiktok/search/top`, `/v1/tiktok/search/keyword`, `/v1/tiktok/search/hashtag` |
| Instagram trends/search | `/v1/instagram/reels/trending`, `/v2/instagram/reels/search`, `/v1/instagram/search/hashtag`, `/v1/instagram/search/popular` |
| Instagram sounds | `/v1/instagram/audio/reels` (`audio_id`) |
| YouTube | `/v1/youtube/shorts/trending`, `/v1/youtube/search`, `/v1/youtube/search/hashtag`, `/v1/youtube/search/typeahead` |
| X / LinkedIn | `/v1/twitter/search/posts`, `/v1/linkedin/search/posts` (Google-indexed, not real-time) |
| Reddit | `/v1/reddit/search`, `/v1/reddit/subreddit`, `/v1/reddit/subreddit/search` |
| Pinterest | `/v1/pinterest/search`, `/v1/pinterest/topic` |

TikTok's old popular videos, creators and songs endpoints no longer exist. Do not call them.

## Workflow

1. Define niche, country/region, platform, and time sensitivity.
2. Pull trend/discovery/search results from 2-4 relevant sources.
3. Normalize evidence: post URL, creator, metric, date, topic, sound/hashtag if present.
4. Cluster into trends by topic, format, hook, sound, meme, or audience problem.
5. Rank trends by evidence strength and relevance, not raw views alone.
6. Translate each trend into content ideas the user can actually make.

## Output Format

```markdown
# Trend Discovery Brief: {niche}

## Trends Worth Acting On
| Trend | Platforms | Evidence | Why it matters | Content angle |
|---|---|---|---|---|

## Sounds / Hashtags / Formats
- ...

## Example Posts to Study
- [title/hook](url) — why it matters

## Content Ideas
1. ...
2. ...

## Caveats
- Public data only.
- Trend evidence is directional unless repeated across sources.
```

## Common Pitfalls

- Do not call something a trend from one post unless the user only asked for examples.
- Do not ignore region. TikTok trends can be highly country-specific.
- Do not recommend jumping on trends that do not fit the user's brand or audience.
