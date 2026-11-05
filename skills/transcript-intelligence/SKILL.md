---
name: transcript-intelligence
description: Use when the user wants to summarize, analyze, or repurpose transcripts from TikTok, Instagram, YouTube, Facebook, X/Twitter, LinkedIn, Rumble, or Reddit video posts. Extracts hooks, claims, quotes, content atoms, themes, and reusable scripts.
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

# Transcript Intelligence

## Overview

Turn public video transcripts into useful research and content assets. This skill is for extracting signal from spoken social video: hooks, claims, stories, objections, examples, CTAs, and reusable content angles.

## Before You Start

- Data comes from ScrapeCreators. Load `scrapecreators-api` for endpoint details and run every call through its helper `scripts/sc.py`, which handles the balance check, cost dry-run, pagination (`--pages N`), caching and the credit budget.
- Locate the helper with `SC="$(ls {.claude,.agents,$HOME/.claude,$HOME/.agents}/skills/scrapecreators-api/scripts/sc.py 2>/dev/null | head -1)"`, then run `python3 "$SC" balance` first. If it reports a missing key, a blocked network or no credits, tell the user what to fix and stop the data part. Never fill gaps with invented posts, numbers or quotes.
- Cost: 1 credit per transcript. AI transcripts of videos over 2 minutes need `allow_long_transcription=true`, which bills 10 credits per started minute, so confirm before using it. Above ~25 credits for the whole job, give the user the estimate in one line and wait for a yes.
- Write the deliverable in the user's language. Keep quotes, hooks and comments verbatim in their original language.

## When to Use

Use this skill when the user asks to:

- summarize a video, reel, short, TikTok, podcast clip, or social video
- analyze a creator's hooks or speaking style
- extract quotes, claims, examples, and CTAs from transcripts
- turn transcripts into social posts, scripts, newsletters, or content ideas
- compare what multiple creators say about a topic

## Transcript Sources

| Platform | Endpoint | Notes |
|---|---|---|
| YouTube | `/v1/youtube/video/transcript`, `/v1/youtube/video` | public captions only, any length, 0 credits when none |
| TikTok | `/v1/tiktok/video/transcript` | native captions; `use_ai_as_fallback=true` for AI; language param is `language` |
| Instagram | `/v2/instagram/media/transcript` | AI, works on carousels |
| Facebook | `/v1/facebook/post/transcript` | native first, then AI |
| Facebook ad | `/v1/facebook/adLibrary/ad/transcript` | |
| X/Twitter | `/v1/twitter/tweet/transcript` | AI, slow |
| LinkedIn | `/v1/linkedin/post/transcript` | |
| Rumble | `/v1/rumble/video/transcript` | |
| Reddit video | `/v1/reddit/post/transcript` | |
| Twitch / Kick clips | `/v1/twitch/clip/transcript`, `/v1/kick/clip/transcript` | |

AI transcription covers videos up to 2 minutes for 1 credit. Longer videos need `allow_long_transcription=true`, billed at 10 credits per started minute for every successful AI transcript, short ones included. Empty results cost 0.

If a detail endpoint already includes transcript text, use it. If transcript is unavailable, say so and fall back to title/caption/description only.

## Workflow

1. **Collect URLs or discover videos**
   - If URLs are provided, fetch each transcript directly.
   - If a creator/channel is provided, first fetch recent posts/videos, then choose relevant videos.

2. **Extract transcript text**
   - Preserve timestamps if provided.
   - Keep source URL with each transcript.
   - Do not hallucinate missing captions.

3. **Segment the transcript**
   Break into:
   - hook/opening
   - setup/context
   - main claim or lesson
   - evidence/examples
   - payoff
   - CTA

4. **Analyze the content**
   Extract:
   - exact hooks
   - claims and contrarian takes
   - stories
   - frameworks
   - objections addressed
   - emotional language
   - quotable lines
   - content atoms that stand alone

5. **Synthesize across multiple transcripts**
   - Cluster by topic and angle.
   - Count recurring themes.
   - Identify repeated hook formulas.
   - Flag the strongest examples with citations.

## Output Format

```markdown
# Transcript Intelligence Report

## TL;DR
- Main themes:
- Strongest hooks:
- Best reusable ideas:

## Transcript-by-Transcript Notes
### [Video title or URL](url)
- Hook: "..."
- Core idea: ...
- Best quote: "..."
- CTA: ...
- Content atoms:
  1. ...

## Patterns Across the Set
| Pattern | Evidence | Example URLs |
|---|---|---|

## Hooks Swipe File
- "..."
- "..."

## Repurposing Ideas
- LinkedIn post:
- X thread:
- Short-form script:
- Newsletter section:
```

## Common Pitfalls

- Do not summarize from the title alone if the user asked for transcript analysis. Fetch transcripts first.
- Do not lose exact wording. Hooks and quotes are more valuable verbatim.
- Do not treat AI-generated transcript text as perfect. If wording seems garbled, mark it as approximate.
- Do not mix source attribution. Every quote should trace back to a URL.
- Do not switch on `allow_long_transcription=true` for a batch without telling the user the per-minute cost. A ten-minute video costs 100 credits.
