---
name: ad-library-teardown
description: Use when the user wants to analyze active ads from Meta/Facebook, Google, or LinkedIn ad libraries; tear down a competitor's messaging; extract hooks, offers, CTAs, video transcripts, landing page claims, and test ideas from public ads.
allowed-tools: Bash, Read, Write, WebFetch

version: 1.0.0
author: ScrapeCreators
license: MIT
homepage: https://scrapecreators.com
repository: https://github.com/ScrapeCreators/agent-skills
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

# Ad Library Teardown

## Overview

Analyze public ads to understand a competitor's messaging, offers, creative strategy, and testing angles. The output should be a practical teardown marketers can use to write better ads or decide what to test.

## When to Use

Use this skill when the user asks to:

- analyze a competitor's active ads
- search Meta/Facebook, Google, or LinkedIn ad libraries
- extract ad hooks, CTAs, claims, offers, and landing page angles
- compare ad messaging across competitors
- summarize video ad transcripts
- generate ad test ideas from competitor ads

## Data Sources

| Ad library | Search/list endpoint | Detail endpoint | Transcript endpoint |
|---|---|---|---|
| Meta/Facebook | `/v1/facebook/adLibrary/search/ads`, `/v1/facebook/adLibrary/company/ads`, `/v1/facebook/adLibrary/search/companies` | `/v1/facebook/adLibrary/ad` | `/v1/facebook/adLibrary/ad/transcript` |
| Google | `/v1/google/adLibrary/advertisers/search`, `/v1/google/company/ads` | `/v1/google/ad` | n/a |
| LinkedIn | `/v1/linkedin/ads/search` | `/v1/linkedin/ad` | n/a |

## Workflow

1. **Find the advertiser**
   - Use company search endpoints when the user provides only a brand name.
   - Use domain/advertiser/page IDs when available.

2. **Fetch active ads**
   - Prefer active ads unless the user asks for historical analysis.
   - Capture platform, advertiser/page, ad ID, start date, creative type, text, headline, CTA, destination URL, and source URL.

3. **Fetch details for representative ads**
   - Enrich the ads with detail endpoints.
   - For video Meta ads, fetch transcripts when available.

4. **Cluster messaging**
   Group ads by:
   - pain point
   - persona
   - offer
   - proof/social proof
   - feature/benefit
   - objection handled
   - comparison/alternative angle
   - urgency/discount

5. **Extract swipeable elements**
   - hooks
   - headlines
   - primary text patterns
   - CTAs
   - claims
   - offers
   - visual/creative concepts

6. **Recommend tests**
   Suggest tests based on repeated patterns and gaps, not random ideas.

## Output Format

```markdown
# Ad Library Teardown: {brand}

## Summary
- Ads analyzed: {count}
- Platforms: Meta / Google / LinkedIn
- Main positioning:
- Strongest repeated offer:

## Messaging Angles
| Angle | Evidence | Example ads | Notes |
|---|---|---|---|

## Hooks and Headlines Swipe File
- "..."
- "..."

## Offers and CTAs
| Offer | CTA | Platform | Example |
|---|---|---|---|

## Video Transcript Notes
- [Ad](url): summary, hook, best quote

## What They Appear to Be Testing
1. ...
2. ...

## Recommended Tests for Us
1. ...
2. ...
3. ...

## Sources
- [Ad](url)
```

## Common Pitfalls

- Do not claim an ad is winning just because it is active. Say it is active or repeated; performance is not public unless the endpoint returns it.
- Do not ignore repeated ads. Repetition is often a useful signal.
- Do not invent spend, conversion rate, or targeting unless public data includes it.
- Do not skip video transcripts when the user asks for hooks or messaging from video ads.
