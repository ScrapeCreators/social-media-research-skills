---
name: scrapecreators-api
description: >-
  Scrape and extract public data from 25+ platforms using the ScrapeCreators
  REST API: TikTok, TikTok Shop, Instagram, YouTube, LinkedIn, Facebook
  (incl. Marketplace and events), Twitter/X, Reddit, Threads, Bluesky,
  Pinterest, Snapchat, Twitch, Kick, Rumble, Truth Social, Spotify, Apple
  Music, SoundCloud, GitHub, Kwai, Telegram, Google, Amazon Shop and
  link-in-bio services. Use when the user asks to scrape, fetch, extract,
  search, or look up social media profiles, posts, videos, reels, comments,
  transcripts, followers, ads, hashtags, trending content, or engagement
  metrics from any social platform. Also use when the user mentions
  ScrapeCreators, a social media API, an ad library, or creator data, and as
  the data layer for the other social research skills.
allowed-tools: Bash, Read, Write, WebFetch
homepage: https://scrapecreators.com
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      env:
        - SCRAPECREATORS_API_KEY
    primaryEnv: SCRAPECREATORS_API_KEY
    homepage: https://scrapecreators.com
    tags:
      - scraping
      - social-media
      - tiktok
      - instagram
      - youtube
      - linkedin
      - facebook
      - twitter
      - reddit
      - threads
      - bluesky
      - pinterest
      - snapchat
      - twitch
      - truth-social
      - tiktok-shop
      - google
      - ad-library
      - creator-data
      - transcripts
      - trending
---

# ScrapeCreators API

Public data from 25+ platforms through 189 GET endpoints. Base URL `https://api.scrapecreators.com`, auth header `x-api-key`. Every call spends credits, so this skill is built around one rule: **know the cost before you call, and never invent data when a call fails.**

Full endpoint list with required params, pagination and credits: [references/endpoints.md](references/endpoints.md) (generated from the official ScrapeCreators CLI config, v1.0.108, 2026-11-04).

## Step 0: Find the helper and check access

Use the bundled helper instead of raw curl. It validates params, follows pagination, enforces a credit budget, caches identical requests, refuses to follow redirects (so the key never leaks), and saves responses to files so large JSON never floods the conversation.

The helper sits in `scripts/sc.py` inside this skill's base directory (shown when the skill loads). If you do not know that path:

```bash
SC="$(ls {.claude,.agents,$HOME/.claude,$HOME/.agents}/skills/scrapecreators-api/scripts/sc.py 2>/dev/null | head -1)"
python3 "$SC" balance
```

`balance` is free. Read its result before anything else:

| Result | What to tell the user |
|---|---|
| `"ok": true, "creditCount": N` | Ready. Mention the balance if the job is large. |
| `missing_api_key` (exit 2) | They need a key from https://app.scrapecreators.com set as `SCRAPECREATORS_API_KEY`. In a Claude Code cloud session it goes into the environment settings, then a new session. Never ask them to paste the key in chat. |
| `network_blocked` (exit 4) | The environment's network policy blocks `api.scrapecreators.com`. They must allow that host in the network settings. |
| `http_401` | Key rejected. |
| `http_402` | Out of credits, top up at https://app.scrapecreators.com/billing. |

If access fails, stop the data part of the task and explain. Do not fall back to made-up numbers, remembered stats, or "example" data presented as real.

## Step 1: Pick the endpoint

Use the routing tables below. For anything not listed, search the bundled list:

```bash
python3 "$SC" find instagram comments
```

If a call returns 400 or a parameter is unclear, fetch the per-endpoint OpenAPI spec: `https://docs.scrapecreators.com/{path}/openapi.json` (for example `https://docs.scrapecreators.com/v1/tiktok/profile/openapi.json`).

## Step 2: Plan the cost

```bash
python3 "$SC" call /v3/tiktok/profile/videos handle=stoolpresidente --pages 5 --dry-run
```

`--dry-run` calls nothing and prints `credits_per_request` and `estimated_max_credits`. Then:

* Up to ~25 credits for the whole task: just run it.
* More than that: tell the user the estimate in one line and get a yes.
* The helper refuses any single request of 10+ credits (`needs_confirmation`, exit 3) until you add `--allow-expensive`. Only add it after the user agreed to that cost.
* The helper stops at a budget of 100 credits per output directory (`over_budget`). Raise it with `SC_BUDGET=...` only when the user asks.

## Step 3: Call

```bash
python3 "$SC" call /v1/tiktok/profile handle=charlidamelio
python3 "$SC" call /v3/tiktok/profile/videos handle=charlidamelio --pages 3
python3 "$SC" call /v1/youtube/video/transcript url="https://www.youtube.com/watch?v=bjVIDXPP7Uk"
```

Output is a short JSON summary: `files` (saved pages), `items`, `items_key`, `next_cursor`, `credits_charged`, `credits_remaining`, `top_level_keys`. Read the saved files with `jq` or a short Python snippet and pull only the fields you need. A leading `@` in `handle` and `#` in `hashtag` is stripped for you.

Responses go to `./scrapecreators-data/` (override with `SC_OUT`). Identical requests within 24 h are served from cache for 0 credits (`--no-cache` to force a fresh call). `python3 "$SC" spent` shows credits spent so far.

Raw HTTP is fine when the helper is not available:

```bash
curl -s "https://api.scrapecreators.com/v1/tiktok/profile?handle=charlidamelio" -H "x-api-key: $SCRAPECREATORS_API_KEY"
```

## Intent Routing

### Profiles
| Platform | Endpoint | Main param |
|---|---|---|
| TikTok | `/v1/tiktok/profile` | `handle` or `user_id` |
| TikTok region | `/v1/tiktok/profile/region` | `handle` |
| Instagram | `/v1/instagram/profile` | `handle` |
| Instagram by user id | `/v1/instagram/basic-profile` | `userId` |
| YouTube | `/v1/youtube/channel` | `handle`, `channelId` or `url` |
| LinkedIn person / company | `/v1/linkedin/profile`, `/v1/linkedin/company` | `url` |
| Facebook | `/v1/facebook/profile` | `url` |
| Twitter/X | `/v1/twitter/profile` | `handle` |
| Reddit subreddit | `/v1/reddit/subreddit/details` | `subreddit` or `url` |
| Threads / Bluesky / Truth Social | `/v1/threads/profile`, `/v1/bluesky/profile`, `/v1/truthsocial/profile` | `handle` |
| Twitch / Snapchat / Kwai | `/v1/twitch/profile`, `/v1/snapchat/profile`, `/v1/kwai/profile` | `handle` |
| Pinterest boards | `/v1/pinterest/user/boards` | `handle` |
| Telegram channel | `/v1/telegram/channel` | see spec |
| Linked socials of a creator | `/v1/find-social-profiles` (10 credits) | `platform` + `handle` |

### Posts and feeds
| Platform | Endpoint | Main param | Paging |
|---|---|---|---|
| TikTok videos | `/v3/tiktok/profile/videos` | `handle` | `max_cursor` |
| Instagram posts | `/v2/instagram/user/posts` | `handle` | `next_max_id` |
| Instagram reels | `/v1/instagram/user/reels` | `handle` or `user_id` | `max_id` |
| Instagram tagged posts | `/v1/instagram/user/tagged-posts` | `user_id` | `cursor` |
| YouTube videos | `/v1/youtube/channel-videos` | `handle` or `channelId` | `continuationToken` |
| YouTube shorts / lives / playlists | `/v1/youtube/channel/shorts`, `/v1/youtube/channel/lives`, `/v1/youtube/channel/playlists` | `handle` or `channelId` | `continuationToken` |
| YouTube community posts | `/v1/youtube/channel/community-posts` | `handle` or `channelId` | `continuationToken` |
| LinkedIn company posts | `/v1/linkedin/company/posts` | `url` | `page` (max 7) |
| Facebook posts / reels / photos | `/v1/facebook/profile/posts`, `/v1/facebook/profile/reels`, `/v1/facebook/profile/photos` | `url` or `pageId` | `cursor` |
| Facebook group posts | `/v1/facebook/group/posts` | `url` or `group_id` | `cursor` |
| Twitter/X | `/v1/twitter/user-tweets` | `handle` | none (~100 popular tweets) |
| Reddit subreddit posts | `/v1/reddit/subreddit` | `subreddit` (case-sensitive) | `after` |
| Threads / Bluesky / Truth Social | `/v1/threads/user/posts`, `/v1/bluesky/user/posts`, `/v1/truthsocial/user/posts` | `handle` | Bluesky `cursor`, Truth `next_max_id` |
| Rumble / Twitch / Kwai | `/v1/rumble/channel/videos`, `/v1/twitch/user/videos`, `/v1/kwai/user/posts` | `handle` or `url` (Twitch: `handle`) | Rumble, Kwai `cursor` |
| Telegram | `/v1/telegram/channel/posts` | `handle` | `cursor` |

### Single post or video
| Platform | Endpoint |
|---|---|
| TikTok | `/v2/tiktok/video` (`url`, add `get_transcript=true` for transcript) |
| Instagram | `/v1/instagram/post` |
| YouTube video / community post | `/v1/youtube/video`, `/v1/youtube/community-post` |
| YouTube sponsors in a video | `/v1/youtube/video/sponsors` |
| LinkedIn | `/v1/linkedin/post` |
| Facebook | `/v1/facebook/post` |
| Twitter/X tweet / community | `/v1/twitter/tweet`, `/v1/twitter/community`, `/v1/twitter/community/tweets` |
| Reddit post | `/v1/reddit/post` (comments: `/v1/reddit/post/comments`) |
| Threads / Bluesky / Truth Social | `/v1/threads/post`, `/v1/bluesky/post`, `/v1/truthsocial/post` |
| Pinterest pin / board | `/v1/pinterest/pin`, `/v1/pinterest/board` |
| Twitch / Kick clip | `/v1/twitch/clip`, `/v1/kick/clip` |
| Rumble / Snapchat Spotlight / Kwai / Telegram | `/v1/rumble/video`, `/v1/snapchat/spotlight`, `/v1/kwai/post`, `/v1/telegram/post` |

All take `url` unless the spec says otherwise.

### Comments
| Platform | Comments | Replies |
|---|---|---|
| TikTok | `/v1/tiktok/video/comments` (0 credits for empty pages) | `/v1/tiktok/video/comment/replies` |
| Instagram | `/v2/instagram/post/comments` | `/v1/instagram/post/comment/replies` |
| YouTube | `/v1/youtube/video/comments` | `/v1/youtube/video/comment/replies` |
| Facebook | `/v1/facebook/post/comments` | `/v1/facebook/post/comment/replies` |
| Reddit | `/v1/reddit/post/comments` | in the same response |
| Rumble / Snapchat | `/v1/rumble/video/comments`, `/v1/snapchat/spotlight/comments` | |

### Transcripts
| Platform | Endpoint | Notes |
|---|---|---|
| YouTube | `/v1/youtube/video/transcript` | public captions only, any length, 1 credit if returned, 0 if none, `language` param |
| TikTok | `/v1/tiktok/video/transcript` | native captions; `use_ai_as_fallback=true` for AI; param is `language`, not `lang` |
| Instagram | `/v2/instagram/media/transcript` | AI, carousels supported |
| Facebook / Facebook ad | `/v1/facebook/post/transcript`, `/v1/facebook/adLibrary/ad/transcript` | native first, then AI |
| Twitter/X | `/v1/twitter/tweet/transcript` | AI, slow |
| LinkedIn / Reddit / Rumble | `/v1/linkedin/post/transcript`, `/v1/reddit/post/transcript`, `/v1/rumble/video/transcript` | |
| Twitch / Kick clip | `/v1/twitch/clip/transcript`, `/v1/kick/clip/transcript` | |

AI transcription is 1 credit for videos up to 2 minutes. Longer videos need `allow_long_transcription=true`, which bills **10 credits per started minute for every successful AI transcript, short ones included**. Empty results cost 0. AI routes are synchronous and can take 30+ seconds.

### Search
| What | Endpoint | Main param |
|---|---|---|
| TikTok videos / top / hashtag / users | `/v1/tiktok/search/keyword`, `/v1/tiktok/search/top`, `/v1/tiktok/search/hashtag`, `/v1/tiktok/search/users` | `query` / `hashtag` |
| TikTok autocomplete | `/v1/tiktok/search/suggestions` | `query` |
| Instagram reels / profiles / hashtag / popular | `/v2/instagram/reels/search`, `/v1/instagram/search/profiles`, `/v1/instagram/search/hashtag`, `/v1/instagram/search/popular` | `query` (hashtag route: `hashtag`) |
| Instagram reels using a sound | `/v1/instagram/audio/reels` | `audio_id` |
| YouTube / hashtag / autocomplete | `/v1/youtube/search`, `/v1/youtube/search/hashtag`, `/v1/youtube/search/typeahead` | `query` / `hashtag` |
| Twitter/X posts | `/v1/twitter/search/posts` | `query` (Google-indexed, incomplete, cursor 1 to 11) |
| LinkedIn posts | `/v1/linkedin/search/posts` | `query` (Google-indexed, cursor 1 to 11) |
| Facebook videos / events / Marketplace | `/v1/facebook/search/videos`, `/v1/facebook/events/search`, `/v1/facebook/marketplace/search` | `query` |
| Reddit all / in subreddit | `/v1/reddit/search`, `/v1/reddit/subreddit/search` | `query` (+ `subreddit`) |
| Threads posts / users | `/v1/threads/search`, `/v1/threads/search/users` | `query` |
| Pinterest / Rumble / Google | `/v1/pinterest/search`, `/v1/rumble/search`, `/v1/google/search` | `query` |
| Spotify / Apple Music | `/v1/spotify/search`, `/v1/apple-music/search` | `query` |

### Ad libraries
| Platform | Endpoint | Main param |
|---|---|---|
| Meta search ads / find companies | `/v1/facebook/adLibrary/search/ads`, `/v1/facebook/adLibrary/search/companies` | `query` |
| Meta ads of a company / one ad | `/v1/facebook/adLibrary/company/ads`, `/v1/facebook/adLibrary/ad` | `pageId` or `companyName` / `id` or `url` |
| Google ads of a company | `/v1/google/company/ads` | `domain` or `advertiser_id` (25 credits with `get_ad_details=true`) |
| Google one ad / find advertiser | `/v1/google/ad`, `/v1/google/adLibrary/advertisers/search` | `url` / `query` |
| LinkedIn ads search / one ad | `/v1/linkedin/ads/search`, `/v1/linkedin/ad` | `company` or `keyword` / `url` |
| TikTok ads search / one ad | `/v1/tiktok/ad-library/search`, `/v1/tiktok/ad-library/ad` | `query` or `advertiser_name` / `ad_id` |

There is no Reddit ad library endpoint.

### Trending and discovery
| What | Endpoint | Param |
|---|---|---|
| TikTok trending feed | `/v1/tiktok/get-trending-feed` | `region` (required) |
| TikTok popular hashtags | `/v1/tiktok/hashtags/popular` | `period`, `countryCode`, `industry`, `page` |
| TikTok sound / videos using it | `/v1/tiktok/song`, `/v1/tiktok/song/videos` | `clipId` |
| Instagram trending reels | `/v1/instagram/reels/trending` | none |
| YouTube trending shorts | `/v1/youtube/shorts/trending` | |
| Pinterest topic | `/v1/pinterest/topic` | `url` |
| GitHub trending repos / developers | `/v1/github/trending/repositories`, `/v1/github/trending/developers` | `language`, `since` |

TikTok popular videos, creators and songs endpoints no longer exist. For those signals combine the trending feed, popular hashtags, `search/top` and `song/videos`.

`/v1/tiktok/hashtags/popular` is still in the official CLI catalog, but some users reported 404s for it. If it returns 404, fall back to `/v1/tiktok/search/hashtag` and hashtags seen in the trending feed.

### Audience, creators and commerce
| What | Endpoint | Cost |
|---|---|---|
| TikTok followers / following | `/v1/tiktok/user/followers`, `/v1/tiktok/user/following` | 1 per page, `min_time` paging |
| TikTok audience countries | `/v1/tiktok/user/audience` | **26** |
| Age and gender estimate from photo | `/v1/detect-age-gender` | 1, AI estimate |
| Public creator emails | `/v1/find-creator-emails` | 1 if none, **10** if any found |
| TikTok live / user live | `/v1/tiktok/live`, `/v1/tiktok/user/live` | 1 |
| TikTok Shop search / store / product / reviews / showcase | `/v1/tiktok/shop/search`, `/v1/tiktok/shop/products`, `/v1/tiktok/product`, `/v1/tiktok/shop/product/reviews`, `/v1/tiktok/user/showcase` | 1 |
| Link in bio | `/v1/linktree`, `/v1/komi`, `/v1/pillar`, `/v1/linkbio`, `/v1/linkme`, `/v1/amazon/shop` | 1 |
| Account usage | `/v1/account/credit-balance`, `/v1/account/get-api-usage`, `/v1/account/get-daily-usage-count`, `/v1/account/get-most-used-routes` | free |

## Credit costs

Default is 1 credit per successful request (per page). Known exceptions:

| Endpoint or flag | Cost |
|---|---|
| `/v1/tiktok/user/audience` | 26 |
| `/v1/google/company/ads` with `get_ad_details=true` | 25 |
| `/v1/find-social-profiles` | 10 |
| `/v1/find-creator-emails` | 10 with emails, 1 without |
| `allow_long_transcription=true` on any AI transcript route | 10 per started minute |
| Transcript routes with no transcript, TikTok comment pages with no comments | 0 |

Responses usually include `credits_charged` and `credits_remaining`; the helper reports both.

## Pagination

Pass the cursor from the previous response back as the same-named param. The helper does this with `--pages N` and stops when the cursor is missing, repeats, or `has_more` is false.

| Paging param | Used by |
|---|---|
| `cursor` | most comment, search, Facebook, Bluesky, Pinterest, TikTok song/hashtag/users, TikTok Shop products routes |
| `max_cursor` | TikTok profile videos (and TikTok collection videos, sent back as `cursor`) |
| `min_time` | TikTok followers and following |
| `continuationToken` | YouTube |
| `after` | Reddit subreddit posts and search |
| `next_max_id` | Instagram posts, Truth Social posts |
| `max_id` | Instagram reels |
| `paginationToken` | LinkedIn ads search |
| `page` (counter) | LinkedIn company posts, Google search, Instagram reels search, TikTok popular hashtags, TikTok Shop search and reviews |

## Common optional params

* `trim=true` shrinks the payload on endpoints that support it. Use it when you only need metrics.
* `region` (2-letter code) routes the request through a proxy in that country. It does **not** filter results, except where the spec says so (for example the TikTok trending feed).

## Known limitations

* Handles go without `@`, hashtags without `#` (the helper strips them).
* Reddit subreddit names are case-sensitive: `AskReddit`, not `askreddit`.
* Twitter/X profiles expose only ~100 of the most popular tweets, not the latest. For recent posts on a topic use `/v1/twitter/search/posts`, which is Google-indexed and incomplete.
* Threads shows only the last 20 to 30 posts publicly.
* Facebook profile and group posts come 3 per page.
* LinkedIn company posts stop at 7 pages. LinkedIn and X post search stop at cursor 11.
* Instagram play counts are Instagram-only views.
* Truth Social works for prominent public accounts only.
* TikTok profile videos can miss posts even after full pagination.
* Public data only. Private accounts, logged-in views and DMs are out of scope.

## Updating this skill

`references/endpoints.md` and `scripts/endpoints.json` are generated from `api-config/` in the official `ScrapeCreators/scrapecreators-cli` repo by `scripts/sync-endpoints.py` at the root of the `ScrapeCreators/social-media-research-skills` repo. When the API changes, rerun that script rather than editing rows by hand. Run `python3 scripts/test_sc.py` in this skill after changing the helper.
