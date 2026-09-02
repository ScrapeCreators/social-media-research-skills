---
name: tiktok-transcript-content-brief
description: Use when the user has public TikTok video URLs and wants an auditable content brief with source-backed hook patterns, themes, evidence, and original ideas without copying creators' scripts.
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
      - tiktok
      - transcript
      - content-research
      - social-media
      - scrapecreators
---

# TikTok Transcript to Content Brief

## Use This When

Use this skill when someone has public TikTok video URLs and wants to understand what is being said without manually watching every clip. It is for content research and briefing, not copying scripts or claiming that a format will perform.

The concrete output is a compact content brief: sources reviewed, observed patterns with evidence, original content angles, and review flags.

## Inputs

```json
{
  "video_urls": ["https://www.tiktok.com/@creator/video/123"],
  "language": "en",
  "goal": "Find useful hook and topic patterns for original content",
  "max_videos": 12,
  "audience": "Optional target audience or customer"
}
```

Process no more than 12 URLs in one pass. If the requester gives more, ask them to prioritize or sample the most relevant videos. Use public URLs only.

## Data Source

Use the `scrapecreators-api` skill to make the request and confirm current parameters when needed. The transcript route is:

```text
GET /v1/tiktok/video/transcript?url={tiktok_video_url}&language={language}
```

All requests use `https://api.scrapecreators.com` with an `x-api-key` header held in `SCRAPECREATORS_API_KEY`. Never put the key in this skill, a prompt, browser code, or the report.

The endpoint returns `id`, `url`, and `transcript` as WEBVTT. It works with public TikTok videos. If needed for one shortlisted video under two minutes, add `use_ai_as_fallback=true`; disclose that it was used because it adds 10 credits.

## Workflow

1. Canonicalize and dedupe supplied URLs. Keep the original URL as the source of record.
2. Request one transcript for each unique URL. Do not use AI fallback in the first pass.
3. Remove WEBVTT timestamps and obvious repeated fragments for analysis, while retaining the raw transcript in the research record.
4. For each usable transcript, identify:
   - the opening hook or question,
   - the promise or outcome,
   - main steps, proof, or examples,
   - audience questions or objections, and
   - phrases useful as themes but not to copy verbatim.
5. Group patterns across the sample. A pattern needs support from at least two videos; otherwise label it a single-source observation.
6. Draft three to five original content angles. Each must name the audience problem it addresses and how it differs from the source material.
7. Flag claims requiring fact-checking, regulated advice, unclear context, or a transcript that may be inaccurate.

## Missing or Weak Transcripts

If a transcript is unavailable, return `transcript_status: unavailable`. Do not infer spoken content from a thumbnail, appearance, or caption.

Only if the requester approves it and the public video is under two minutes, retry once with `use_ai_as_fallback=true`. Mark that fallback in the output.

## Output

Return this structure:

```markdown
# TikTok Content Brief

## Sources Reviewed
| Source URL | Transcript status | Language | Notes |
|---|---|---|---|

## Observed Patterns
| Pattern | Evidence | Supporting videos | Source URLs |
|---|---|---:|---|

## Original Content Angles
1. **Title** — Audience problem, suggested structure, and how this differs from the source material.

## Review Flags
- Missing transcripts, claims to verify, limitations, and fallback use.
```

Use this shape for every source observation:

```json
{
  "source_url": "https://www.tiktok.com/@creator/video/123",
  "transcript_status": "available",
  "hook_pattern": "Starts with a specific everyday problem.",
  "evidence": "Faithful short paraphrase of the spoken opening.",
  "theme": "time-saving routine",
  "confidence": "medium",
  "review_flags": []
}
```

## Rules

- Public data only.
- Never fabricate transcript text, sources, or performance claims.
- Do not copy a creator's script, unique phrasing, or sequence of examples.
- Do not infer sensitive traits from content or appearance.
- Keep source URLs with every observation.
- Treat content angles as hypotheses for human review, not a guarantee of views.
