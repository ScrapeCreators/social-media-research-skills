---
name: comment-mining
description: Use when the user wants to mine comments and replies for audience reactions, customer language, questions, objections, complaints, product ideas, buying intent, sentiment, or voice-of-customer insights from public social posts and videos.
allowed-tools: Bash, Read, Write, WebFetch

version: 1.0.0
author: ScrapeCreators
license: MIT
homepage: https://scrapecreators.com
repository: https://github.com/ScrapeCreators/social-research-skills
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
| Facebook comments | `/v1/facebook/post/comments` |
| Facebook replies | `/v1/facebook/post/comment/replies` |
| Reddit comments | `/v1/reddit/post/comments` |
| Rumble comments | `/v1/rumble/video/comments` |

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
