---
name: outlier-post-finder
description: Use when the user wants to find posts, videos, reels, shorts, tweets, or social content that overperformed versus a creator, brand, or competitor baseline. Finds outliers, explains why they worked, extracts hooks and formats, and produces a practical swipe file.
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

# Outlier Post Finder

## Overview

Find social posts that beat an account's normal performance. The goal is not just to sort by views. The goal is to identify posts that performed unusually well for that creator or brand, then explain the repeatable patterns.

Use ScrapeCreators as the data layer. Pull recent public posts, normalize engagement metrics, calculate each account's baseline, and produce an outlier report with source URLs and practical takeaways.

## When to Use

Use this skill when the user asks to:

- find outlier posts, viral posts, top posts, best reels, best shorts, best TikToks, or best tweets
- analyze why a creator's content is working
- find competitor posts worth copying or learning from
- build a swipe file from high-performing social posts
- compare performance across a creator's recent posts

Do not use this for raw endpoint lookup only. Use `scrapecreators-api` for direct API routing.

## Data Sources

Prefer the platform-specific feed endpoint, then enrich individual posts only when needed.

| Platform | Feed endpoint | Detail/enrichment endpoint |
|---|---|---|
| TikTok | `/v3/tiktok/profile/videos` | `/v2/tiktok/video`, `/v1/tiktok/video/transcript` |
| Instagram posts | `/v2/instagram/user/posts` | `/v1/instagram/post`, `/v2/instagram/media/transcript` |
| Instagram reels | `/v1/instagram/user/reels` | `/v1/instagram/post`, `/v2/instagram/media/transcript` |
| YouTube videos | `/v1/youtube/channel-videos` | `/v1/youtube/video`, `/v1/youtube/video/transcript` |
| YouTube Shorts | `/v1/youtube/channel/shorts` | `/v1/youtube/video`, `/v1/youtube/video/transcript` |
| Facebook | `/v1/facebook/profile/posts`, `/v1/facebook/profile/reels` | `/v1/facebook/post`, `/v1/facebook/post/transcript` |
| LinkedIn | `/v1/linkedin/company/posts` | `/v1/linkedin/post`, `/v1/linkedin/post/transcript` |
| X/Twitter | `/v1/twitter/user-tweets` | `/v1/twitter/tweet`, `/v1/twitter/tweet/transcript` |
| Threads | `/v1/threads/user/posts` | `/v1/threads/post` |
| Bluesky | `/v1/bluesky/user/posts` | `/v1/bluesky/post` |

Before calling an endpoint, fetch its docs or per-endpoint OpenAPI spec if parameter names or response fields are uncertain.

## Workflow

1. **Clarify scope only if needed**
   - Platform(s)
   - Handles or URLs
   - Time/post count window
   - Whether to include transcript/comment analysis

2. **Fetch recent posts**
   - Pull at least 20 posts when available. More is better for baseline confidence.
   - Paginate if the endpoint supports cursors and the user wants a larger window.
   - Keep source URLs for citations.

3. **Normalize metrics**
   - Capture whatever exists: views, plays, likes, comments, shares, reposts, saves.
   - Build a combined engagement score only after preserving raw metrics.
   - For video-first platforms, views/play count is usually the primary metric.
   - For text-first platforms, likes + replies/comments + reposts/shares is usually better.

4. **Calculate the account baseline**
   - Use median instead of mean so one viral post does not distort the baseline.
   - Calculate per-platform and per-account baselines separately.
   - If mixed formats exist, split by format when possible: reel vs carousel, short vs long video, text vs video.

5. **Score outliers**
   - `view_lift = post_views / median_views`
   - `engagement_lift = post_engagement / median_engagement`
   - Label posts as:
     - **Huge outlier:** 5x+ baseline
     - **Strong outlier:** 2x-5x baseline
     - **Mild outlier:** 1.5x-2x baseline
   - If sample size is under 10 posts, call confidence low.

6. **Enrich the winners**
   - Fetch post details for top outliers.
   - Fetch transcripts for video posts when useful.
   - Optionally fetch comments to understand audience reaction.

7. **Explain why they worked**
   Look for:
   - hook style
   - topic/category
   - format
   - emotional trigger
   - novelty/timeliness
   - creator proof or authority
   - controversy or debate
   - comments showing confusion, desire, or buying intent

## Output Format

```markdown
# Outlier Posts Report: {creator_or_brand}

## Summary
- Sample: {n} posts from {platforms}
- Window: {window}
- Baseline: median {primary_metric} = {value}
- Confidence: High/Medium/Low

## Biggest Outliers
| Rank | Post | Platform | Date | Primary Metric | Lift | Why it likely worked |
|---:|---|---|---|---:|---:|---|
| 1 | [title/hook](url) | TikTok | 2026-01-01 | 1.2M views | 8.4x | Contrarian hook + clear before/after |

## Repeatable Patterns
1. **Pattern name** — evidence and examples.
2. **Pattern name** — evidence and examples.

## Hooks to Steal
- "Exact hook from caption or transcript"
- "Exact hook from caption or transcript"

## Content Ideas Based on the Outliers
1. ...
2. ...

## Notes and Caveats
- Public data only.
- Small samples are directional, not definitive.
```

## Common Pitfalls

- Do not call the highest raw-view post the best outlier if a huge account is being compared with a small one. Use lift versus each account's own baseline.
- Do not average TikTok, Instagram, YouTube, and LinkedIn metrics into one baseline. Score each platform separately.
- Do not invent transcript quotes. Fetch transcripts or quote only visible captions/text.
- Do not overstate confidence from fewer than 10 posts.
- Do not ignore old viral posts if the user asked for recent performance. Respect the requested window.
