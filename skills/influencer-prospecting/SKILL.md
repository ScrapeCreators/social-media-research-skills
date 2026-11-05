---
name: influencer-prospecting
description: Use when the user wants to find creators, influencers, affiliates, or social accounts in a niche for outreach, partnerships, sponsorships, UGC, seeding, or competitive research. Produces scored prospect lists from public social data.
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

# Influencer Prospecting

## Overview

Build practical creator prospect lists from public social data. The goal is to find accounts that fit the niche, have enough reach, and show evidence of relevant content or audience fit.

## Before You Start

- Data comes from ScrapeCreators. Load `scrapecreators-api` for endpoint details and run every call through its helper `scripts/sc.py`, which handles the balance check, cost dry-run, pagination (`--pages N`), caching and the credit budget.
- Locate the helper with `SC="$(ls {.claude,.agents,$HOME/.claude,$HOME/.agents}/skills/scrapecreators-api/scripts/sc.py 2>/dev/null | head -1)"`, then run `python3 "$SC" balance` first. If it reports a missing key, a blocked network or no credits, tell the user what to fix and stop the data part. Never fill gaps with invented posts, numbers or quotes.
- Cost: 1 credit per search page and per profile checked. `/v1/find-creator-emails` costs 10 per creator when an email is found, so run it only on the final shortlist and only with the user's OK. Above ~25 credits for the whole job, give the user the estimate in one line and wait for a yes.
- Write the deliverable in the user's language. Keep quotes, hooks and comments verbatim in their original language.

## When to Use

Use this skill when the user asks to:

- find influencers or creators in a niche
- build a UGC, affiliate, sponsorship, or seeding list
- find micro-influencers with strong engagement
- identify creators who already talk about a product category
- export prospects as CSV

## Useful Sources

- TikTok: `/v1/tiktok/search/users`, `/v1/tiktok/search/keyword` and `/v1/tiktok/search/hashtag` (find creators through the content they post), `/v1/tiktok/profile`, `/v3/tiktok/profile/videos`, `/v1/tiktok/user/audience` (26 credits)
- Instagram: `/v1/instagram/search/profiles`, `/v1/instagram/search/hashtag`, `/v2/instagram/reels/search`, `/v1/instagram/profile`, `/v2/instagram/user/posts`, `/v1/instagram/user/reels`
- YouTube: `/v1/youtube/search`, `/v1/youtube/channel`, `/v1/youtube/channel-videos`
- Cross-platform: `/v1/find-social-profiles` (10 credits) and `/v1/find-creator-emails` (10 credits when an email is found, 1 when not)
- Link-in-bio services: Linktree, Komi, Pillar, Linkbio, Linkme
- Amazon Shop and TikTok Shop showcase where relevant

## Scoring Framework

Score each prospect 1-5 on:

- **Niche fit** — content clearly matches the category
- **Audience fit** — country/language/platform fit when public data supports it
- **Reach** — followers/subscribers and recent views
- **Engagement quality** — comments look real and relevant
- **Brand safety** — obvious controversy or mismatch risk
- **Contactability** — public business email, booking link or contact path the creator published

## Output Format

```markdown
# Influencer Prospect List: {niche}

| Creator | Platform | Followers | Recent views | Fit | Contact path | Notes |
|---|---|---:|---:|---:|---|---|

## Best Fits
1. ...

## Outreach Angles
- ...

## CSV
```csv
creator,platform,profile_url,followers,recent_views,fit_score,contact_path,notes
```
```

## Common Pitfalls

- Do not equate large follower count with good fit.
- Do not scrape or expose private contact data. Use public links only.
- Do not hide uncertainty when profiles have limited public data.
- Do not run email lookups over a long list. Build and score the list first, then look up contacts for the shortlist the user picks.
- Emails of individual creators are personal data under GDPR (EU/UK) and similar laws. Keep only contacts the creator published for business, store the source URL next to each one, keep the list minimal, and remind the user that outreach needs a clear opt-out.
- Empty email results do not prove a creator has no public contact. Say "not found", not "none".
