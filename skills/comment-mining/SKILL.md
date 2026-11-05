---
name: comment-mining
description: Use when the user wants to mine comments and replies for audience reactions, customer language, questions, objections, complaints, product ideas, buying intent, sentiment, or voice-of-customer insights from public social posts and videos.
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

# Comment Mining

## Overview

Mine public comments for what people actually ask, complain about, want, misunderstand, or repeat. The output should help with product research, content ideas, copywriting, objection handling, and audience understanding.

## Before You Start

- Data comes from ScrapeCreators. Load `scrapecreators-api` for endpoint details and run every call through its helper `scripts/sc.py`, which handles the balance check, cost dry-run, pagination (`--pages N`), caching and the credit budget.
- Locate the helper with `SC="$(ls {.claude,.agents,$HOME/.claude,$HOME/.agents}/skills/scrapecreators-api/scripts/sc.py 2>/dev/null | head -1)"`, then run `python3 "$SC" balance` first. If it reports a missing key, a blocked network or no credits, tell the user what to fix and stop the data part. Never fill gaps with invented posts, numbers or quotes.
- Cost: 1 credit per comment page (TikTok pages with no comments cost 0). A few hundred comments is usually 10 to 25 pages. Above ~25 credits for the whole job, give the user the estimate in one line and wait for a yes.
- Write the deliverable in the user's language. Keep quotes, hooks and comments verbatim in their original language.

## When to Use

Use this skill when the user asks to:

- analyze comments on a TikTok, YouTube video, Instagram Reel, Facebook post, Reddit post, or Rumble video
- find audience questions, objections, complaints, or buying intent
- extract voice-of-customer language
- find content ideas from comments
- understand sentiment around a post, creator, product, or topic

## Comment Sources

| Platform | Endpoint |
|---|---|
| TikTok comments | `/v1/tiktok/video/comments` |
| TikTok replies | `/v1/tiktok/video/comment/replies` |
| YouTube comments | `/v1/youtube/video/comments` |
| YouTube replies | `/v1/youtube/video/comment/replies` |
| Instagram comments | `/v2/instagram/post/comments` |
| Instagram replies | `/v1/instagram/post/comment/replies` |
| Facebook comments | `/v1/facebook/post/comments` |
| Facebook replies | `/v1/facebook/post/comment/replies` |
| Reddit comments | `/v1/reddit/post/comments` |
| Rumble comments | `/v1/rumble/video/comments` |
| Snapchat Spotlight comments | `/v1/snapchat/spotlight/comments` |

Comment endpoints are paginated with `cursor` (YouTube: `continuationToken`). Use `--pages N` in the helper instead of looping by hand.

## Workflow

1. **Fetch comments**
   - Use the post/video URL whenever possible.
   - Paginate when the endpoint supports it and the user wants depth.
   - Preserve comment text, author if public, like/upvote count, timestamp, and source URL.

2. **Clean lightly**
   - Remove obvious spam/duplicates.
   - Keep slang, misspellings, and emotional wording if it is useful customer language.
   - Do not over-normalize exact quotes.

3. **Classify each useful comment**
   Use these buckets:
   - questions
   - objections
   - complaints/pain points
   - praise
   - confusion
   - requests/feature ideas
   - buying intent
   - controversy/debate
   - jokes/memes/culture signals

4. **Cluster themes**
   - Group similar comments.
   - Score themes by frequency and intensity.
   - Highlight exact quotes for each theme.

5. **Turn insights into actions**
   Depending on the user's goal, produce:
   - content ideas
   - FAQ ideas
   - landing page copy angles
   - product ideas
   - objection-handling bullets
   - sales/support notes

## Output Format

```markdown
# Comment Mining Report

## Summary
- Source(s): {urls}
- Comments analyzed: {count}
- Confidence: High/Medium/Low

## Top Themes
| Theme | Type | Frequency | Intensity | Representative quote |
|---|---|---:|---|---|

## Audience Questions
- "..."

## Objections and Concerns
- **Objection:** ...
  - Evidence: "..."
  - Response angle: ...

## Buying Intent / Demand Signals
- "..."

## Exact Language to Reuse
- "..."
- "..."

## Content Ideas From Comments
1. ...
2. ...
```

## Quality Guardrails

- Label sample size and confidence.
- Separate one loud comment from a repeated pattern.
- Preserve exact quotes for useful language.
- Avoid claiming broad market sentiment from one post's comments.
- Call out moderation/platform bias when relevant.

## Common Pitfalls

- Do not flatten comments into generic sentiment. The value is in questions, objections, and exact wording.
- Do not include personally identifying details unless they are already public and necessary.
- Do not treat bot/spam comments as audience signal.
- Do not skip Reddit post context. For Reddit, read both the original post and comments.
