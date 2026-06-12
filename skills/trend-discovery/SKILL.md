---
name: trend-discovery
description: Use when the user wants to discover trending social topics, hashtags, sounds, posts, reels, shorts, creators, or formats in a niche. Searches public trend and discovery endpoints, ranks evidence, and turns trends into practical content angles.
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

# Trend Discovery

## Overview

Find trends worth acting on. This skill is for social media trend research across TikTok, Instagram, YouTube, Reddit, Pinterest, and other public sources. The output should separate real evidence from vague "this is trending" claims.

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
| TikTok popular hashtags/songs/videos/creators | `/v1/tiktok/hashtags/popular`, `/v1/tiktok/songs/popular`, `/v1/tiktok/videos/popular`, `/v1/tiktok/creators/popular` |
| TikTok search | `/v1/tiktok/search/top`, `/v1/tiktok/search/keyword`, `/v1/tiktok/search/hashtag` |
| Instagram trends/search | `/v1/instagram/reels/trending`, `/v2/instagram/reels/search`, `/v1/instagram/search/hashtag` |
| YouTube | `/v1/youtube/shorts/trending`, `/v1/youtube/search`, `/v1/youtube/search/hashtag` |
| Reddit | `/v1/reddit/search`, `/v1/reddit/subreddit`, `/v1/reddit/subreddit/search` |
| Pinterest | `/v1/pinterest/search` |

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
