---
name: product-demand-research
description: Use when the user wants to validate a product idea, find pain points, mine demand signals, discover objections, or gather voice-of-customer language from Reddit, social posts, video transcripts, and comments. Produces evidence-backed product research.
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

# Product Demand Research

## Overview

Use public social data to understand whether people actually complain about, ask for, buy, hack around, or recommend solutions in a product category. The output should help founders and marketers decide what to build, position, or test.

## Before You Start

- Data comes from ScrapeCreators. Load `scrapecreators-api` for endpoint details and run every call through its helper `scripts/sc.py`, which handles the balance check, cost dry-run, pagination (`--pages N`), caching and the credit budget.
- Locate the helper with `SC="$(ls {.claude,.agents,$HOME/.claude,$HOME/.agents}/skills/scrapecreators-api/scripts/sc.py 2>/dev/null | head -1)"`, then run `python3 "$SC" balance` first. If it reports a missing key, a blocked network or no credits, tell the user what to fix and stop the data part. Never fill gaps with invented posts, numbers or quotes.
- Cost: 1 credit per search page and per comment or transcript page. A solid pass is typically 15 to 40 credits. Above ~25 credits for the whole job, give the user the estimate in one line and wait for a yes.
- Write the deliverable in the user's language. Keep quotes, hooks and comments verbatim in their original language.

## When to Use

Use this skill when the user asks to:

- validate a startup or product idea
- find pain points in a niche
- mine Reddit/TikTok/YouTube comments for product ideas
- find buyer language and objections
- understand alternatives people use today
- create messaging from demand evidence

## Signals to Extract

- repeated complaints
- "I wish" / "is there a tool" / "how do I" phrases
- workarounds and spreadsheets/manual processes
- comparison and alternative mentions
- buying intent
- objections to existing solutions
- exact words people use for the problem

## Useful Sources

- Reddit: `/v1/reddit/search`, `/v1/reddit/subreddit/search`, `/v1/reddit/post/comments` (best for pain points and workarounds)
- TikTok and YouTube: `/v1/tiktok/search/keyword`, `/v1/youtube/search`, then comments and transcripts of the strongest videos
- Autocomplete as demand phrasing: `/v1/tiktok/search/suggestions`, `/v1/youtube/search/typeahead`
- Existing products: `/v1/tiktok/shop/search` and `/v1/tiktok/shop/product/reviews` for what people already buy and complain about
- `/v1/google/search` when the conversation lives outside social platforms

## Workflow

1. Turn the idea into search queries and synonyms.
2. Search Reddit and relevant social platforms.
3. Pull comments/transcripts for promising posts/videos.
4. Cluster pains, triggers, alternatives, and desired outcomes.
5. Score demand by frequency, intensity, recency, and willingness-to-pay hints.
6. Produce messaging and product implications.

## Output Format

```markdown
# Product Demand Research: {idea/category}

## Verdict
- Demand signal: Strong/Medium/Weak
- Confidence: High/Medium/Low
- Why:

## Pain Points
| Pain | Evidence | Exact language | Source |
|---|---|---|---|

## Existing Alternatives / Workarounds
- ...

## Objections and Barriers
- ...

## Messaging Angles
- "..."

## Product Ideas / Tests
1. ...
2. ...
```

## Common Pitfalls

- Do not claim market validation from a handful of comments.
- Do not ignore negative evidence or existing alternatives.
- Do not paraphrase away the best customer language.
