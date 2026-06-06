---
name: scrapecreators-api
description: >-
  Scrape and extract public data from 27+ social media platforms using the
  ScrapeCreators REST API. Covers TikTok, Instagram, YouTube, LinkedIn,
  Facebook, Twitter/X, Reddit, Threads, Bluesky, Pinterest, Snapchat, Twitch,
  Kick, Truth Social, TikTok Shop, Google, and link-in-bio services (Linktree,
  Komi, Pillar, Linkbio, Linkme, Amazon Shop). Use when the user asks to
  scrape, fetch, extract, search, or look up social media profiles, posts,
  videos, reels, comments, transcripts, followers, ads, hashtags, trending
  content, or engagement metrics from any social platform. Also use when user
  mentions ScrapeCreators, social media API, ad library, or creator data.
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

Scrape and extract public data from 27+ social media platforms. 110 endpoints available.

**Base URL:** `https://api.scrapecreators.com`

Get your API key at https://scrapecreators.com

## How to Call

All endpoints use GET requests. Pass query params in the URL and authenticate with the `x-api-key` header. Responses are JSON.

```bash
curl -s "https://api.scrapecreators.com/v1/tiktok/profile?handle=charlidamelio" \
  -H "x-api-key: $SCRAPECREATORS_API_KEY"
```

Or with `fetch`:

```javascript
const res = await fetch(
  "https://api.scrapecreators.com/v1/tiktok/profile?handle=charlidamelio",
  { headers: { "x-api-key": process.env.SCRAPECREATORS_API_KEY } }
);
const data = await res.json();
```

Endpoint paths use the pattern `/v1/platform/action`. The tables below list each endpoint path and its required params.

### API Spec

Each endpoint has its own OpenAPI spec at `https://docs.scrapecreators.com/{path}/openapi.json`.

For example: https://docs.scrapecreators.com/v1/tiktok/profile/openapi.json

**Important:** Once you've determined which endpoint(s) to call from the routing tables below, fetch the single-endpoint OpenAPI spec first to get the full parameter details, types, and example response before making the actual API call.

The full spec covering all endpoints is at https://docs.scrapecreators.com/openapi.json (large file — prefer the per-endpoint specs above).

## Intent Routing

Map user intent to the right endpoint. After selecting an endpoint, fetch its OpenAPI spec at `https://docs.scrapecreators.com/{path}/openapi.json` for full param details before calling.

### Profiles / User Info
| Platform | Endpoint | Primary Param | Example |
|----------|----------|---------------|---------|
| TikTok | `/v1/tiktok/profile` | handle | `stoolpresidente` |
| Instagram | `/v1/instagram/profile` | handle | `jane` |
| YouTube | `/v1/youtube/channel` | handle, channelId, or url | `ThePatMcAfeeShow` |
| LinkedIn (person) | `/v1/linkedin/profile` | url | `https://www.linkedin.com/in/parrsam/` |
| LinkedIn (company) | `/v1/linkedin/company` | url | `https://linkedin.com/company/shopify` |
| Facebook | `/v1/facebook/profile` | url | `https://www.facebook.com/mantraindianfolsom` |
| Twitter/X | `/v1/twitter/profile` | handle | `elonmusk` |
| Reddit | `/v1/reddit/subreddit/details` | subreddit or url | `AskReddit` |
| Threads | `/v1/threads/profile` | handle | `zuck` |
| Bluesky | `/v1/bluesky/profile` | handle | `jay.bsky.team` |
| Pinterest | `/v1/pinterest/user/boards` | handle | `pinterest` |
| Truth Social | `/v1/truthsocial/profile` | handle | `realDonaldTrump` |
| Twitch | `/v1/twitch/profile` | handle | `ninja` |
| Snapchat | `/v1/snapchat/profile` | handle | `djkhaled` |

### Posts / Content Feeds
| Platform | Endpoint | Primary Param | Example |
|----------|----------|---------------|---------|
| TikTok videos | `/v3/tiktok/profile/videos` | handle | `stoolpresidente` |
| Instagram posts | `/v2/instagram/user/posts` | handle | `jane` |
| Instagram reels | `/v1/instagram/user/reels` | handle or user_id | `jane` or `2700692569` |
| Instagram highlights | `/v1/instagram/user/highlights` | handle or user_id | `jane` or `2700692569` |
| YouTube videos | `/v1/youtube/channel/videos` | handle or channelId | `ThePatMcAfeeShow` |
| YouTube shorts | `/v1/youtube/channel/shorts` | handle or channelId | `starterstory` |
| YouTube playlist | `/v1/youtube/playlist` | playlist_id | `PLP32wGpgzmIlInfgKVFfCwVsxgGqZNIiS` |
| LinkedIn posts | `/v1/linkedin/company/posts` | url | `https://linkedin.com/company/shopify` |
| Facebook posts | `/v1/facebook/profile/posts` | url or pageId | `https://www.facebook.com/pacemorby` |
| Facebook reels | `/v1/facebook/profile/reels` | url | `https://www.facebook.com/Spurs` |
| Facebook photos | `/v1/facebook/profile/photos` | url | `https://www.facebook.com/Spurs` |
| Facebook group posts | `/v1/facebook/group/posts` | url or group_id | `742354120555345` |
| Twitter tweets | `/v1/twitter/user/tweets` | handle | `elonmusk` |
| Reddit posts | `/v1/reddit/subreddit` | subreddit | `AskReddit` |
| Threads posts | `/v1/threads/user/posts` | handle | `zuck` |
| Bluesky posts | `/v1/bluesky/user/posts` | handle or user_id | `jay.bsky.team` |
| Truth Social posts | `/v1/truthsocial/user/posts` | handle or user_id | `realDonaldTrump` |
| Pinterest board | `/v1/pinterest/board` | url | `https://www.pinterest.com/...` |

### Single Post / Video Details
| Platform | Endpoint | Primary Param | Example |
|----------|----------|---------------|---------|
| TikTok | `/v2/tiktok/video` | url | `https://www.tiktok.com/@randomspamvideos25/video/7251387037834595630` |
| Instagram | `/v1/instagram/post` | url | `https://www.instagram.com/reel/DOq6eV6iIgD` |
| Instagram highlight | `/v1/instagram/user/highlight/detail` | id | `18067016518767507` |
| YouTube | `/v1/youtube/video` | url | `https://www.youtube.com/watch?v=Y2Ah_DFr8cw` |
| YouTube community post | `/v1/youtube/community-post` | url | `https://www.youtube.com/post/Ugkxvj2KoApYAXoqLWnKVr6zZe5JjeHrQeP8` |
| LinkedIn | `/v1/linkedin/post` | url | `https://www.linkedin.com/pulse/being-father-has-made-me-better-leader...` |
| Facebook | `/v1/facebook/post` | url | `https://www.facebook.com/reel/1535656380759655` |
| Twitter/X | `/v1/twitter/tweet` | url | `https://twitter.com/elonmusk/status/...` |
| Twitter/X community | `/v1/twitter/community` | url | `https://twitter.com/i/communities/...` |
| Twitter/X community tweets | `/v1/twitter/community/tweets` | url | `https://twitter.com/i/communities/...` |
| Reddit | `/v1/reddit/post/comments` | url | `https://www.reddit.com/r/AskReddit/comments/...` |
| Threads | `/v1/threads/post` | url | `https://www.threads.net/@zuck/post/...` |
| Bluesky | `/v1/bluesky/post` | url | `https://bsky.app/profile/.../post/...` |
| Truth Social | `/v1/truthsocial/post` | url | `https://truthsocial.com/@realDonaldTrump/posts/...` |
| Pinterest | `/v1/pinterest/pin` | url | `https://www.pinterest.com/pin/...` |
| Twitch clip | `/v1/twitch/clip` | url | `https://clips.twitch.tv/...` |
| Kick clip | `/v1/kick/clip` | url | `https://kick.com/...` |

### Comments
| Platform | Endpoint | Primary Param | Example |
|----------|----------|---------------|---------|
| TikTok | `/v1/tiktok/video/comments` | url | `https://www.tiktok.com/@stoolpresidente/video/7499229683859426602` |
| Instagram | `/v2/instagram/post/comments` | url | `https://www.instagram.com/reel/DOq6eV6iIgD` |
| YouTube | `/v1/youtube/video/comments` | url | `https://www.youtube.com/watch?v=dQw4w9WgXcQ` |
| Facebook | `/v1/facebook/post/comments` | url or feedback_id | `https://www.facebook.com/reel/753347914167361` |
| Reddit | `/v1/reddit/post/comments` | url | `https://www.reddit.com/r/AskReddit/comments/...` |

### Transcripts
| Platform | Endpoint | Example | Note |
|----------|----------|---------|------|
| TikTok | `/v1/tiktok/video/transcript` | `url=https://www.tiktok.com/...&lang=en` | also via `/v2/tiktok/video` with get_transcript=true |
| Instagram | `/v2/instagram/media/transcript` | `url=https://www.instagram.com/reel/...` | AI-powered, 10-30s, under 2min |
| YouTube | `/v1/youtube/video/transcript` | `url=https://www.youtube.com/watch?v=bjVIDXPP7Uk` | also included in `/v1/youtube/video` response |
| Facebook | `/v1/facebook/post/transcript` | `url=https://www.facebook.com/reel/...` | under 2min only |
| Twitter/X | `/v1/twitter/tweet/transcript` | `url=https://twitter.com/...` | AI-powered, slow |

### Search
| Platform | Endpoint | Primary Param | Example |
|----------|----------|---------------|---------|
| TikTok users | `/v1/tiktok/search/users` | query | `funny` |
| TikTok videos (keyword) | `/v1/tiktok/search/keyword` | query | `funny` |
| TikTok videos (hashtag) | `/v1/tiktok/search/hashtag` | hashtag | `fyp` |
| TikTok top (photos+videos) | `/v1/tiktok/search/top` | query | `funny` |
| Instagram reels | `/v2/instagram/reels/search` | query | `dogs` |
| YouTube | `/v1/youtube/search` | query | `funny` |
| YouTube hashtag | `/v1/youtube/search/hashtag` | hashtag | `funny` |
| Reddit (all) | `/v1/reddit/search` | query | `best programming languages` |
| Reddit (in subreddit) | `/v1/reddit/subreddit/search` | subreddit + query | `AskReddit` + `funny` |
| Threads posts | `/v1/threads/search` | query | `AI` |
| Threads users | `/v1/threads/search/users` | query | `zuck` |
| Pinterest | `/v1/pinterest/search` | query | `home decor` |
| Google | `/v1/google/search` | query | `best restaurants in NYC` |

### Ad Libraries
| Platform | Endpoint | Primary Param | Example |
|----------|----------|---------------|---------|
| Facebook ads search | `/v1/facebook/adLibrary/search/ads` | query | `running` |
| Facebook company ads | `/v1/facebook/adLibrary/company/ads` | pageId or companyName | `Lululemon` |
| Facebook ad detail | `/v1/facebook/adLibrary/ad` | id or url | `702369045530963` |
| Facebook find companies | `/v1/facebook/adLibrary/search/companies` | query | `Nike` |
| Google company ads | `/v1/google/company/ads` | domain or advertiser_id | `nike.com` |
| Google ad detail | `/v1/google/ad` | url | `https://adstransparency.google.com/...` |
| Google find advertisers | `/v1/google/adLibrary/advertisers/search` | query | `Nike` |
| LinkedIn ads search | `/v1/linkedin/ads/search` | company or keyword | `Shopify` |
| LinkedIn ad detail | `/v1/linkedin/ad` | url | `https://www.linkedin.com/ad/...` |
| Reddit ads search | `/v1/reddit/ads/search` | query | `gaming` |
| Reddit ad detail | `/v1/reddit/ad` | id | `t3_abc123` |

### Trending / Popular
| Content | Endpoint | Param | Example |
|---------|----------|-------|---------|
| Trending feed | `/v1/tiktok/get-trending-feed` | region (required) | `US` |
| Popular videos | `/v1/tiktok/videos/popular` | | |
| Popular creators | `/v1/tiktok/creators/popular` | | |
| Popular hashtags | `/v1/tiktok/hashtags/popular` | | |
| Popular songs | `/v1/tiktok/songs/popular` | | |
| Song details | `/v1/tiktok/song` | clipId | `7439295283975702544` |
| Videos using song | `/v1/tiktok/song/videos` | clipId | `7439295283975702544` |
| Trending shorts (YT) | `/v1/youtube/shorts/trending` | | |

### Followers / Following / Live (TikTok only)
| Type | Endpoint | Example |
|------|----------|---------|
| Following | `/v1/tiktok/user/following` | `handle=stoolpresidente` |
| Followers | `/v1/tiktok/user/followers` | `handle=stoolpresidente` |
| Audience demographics | `/v1/tiktok/user/audience` (26 credits!) | `handle=shakira` |
| Live stream | `/v1/tiktok/user/live` | `handle=thejustalex` |

### TikTok Shop
| Type | Endpoint | Primary Param | Example |
|------|----------|---------------|---------|
| Search products | `/v1/tiktok/shop/search` | query | `shoes` |
| Store products | `/v1/tiktok/shop/products` | url | `https://www.tiktok.com/shop/store/goli-nutrition/7495794203056835079` |
| Product detail | `/v1/tiktok/product` | url | `https://www.tiktok.com/shop/pdp/goli-ashwagandha-gummies.../1729587769570529799` |
| Product reviews | `/v1/tiktok/shop/product/reviews` | url or product_id | `1731578642912612516` |
| User showcase | `/v1/tiktok/user/showcase` | handle | `mrtiktokreviews` |

### Link-in-Bio / Other
| Service | Endpoint | Param | Example |
|---------|----------|-------|---------|
| Linktree | `/v1/linktree` | url | `https://linktr.ee/...` |
| Komi | `/v1/komi` | url | `https://komi.io/...` |
| Pillar | `/v1/pillar` | url | `https://pillar.io/...` |
| Linkbio | `/v1/linkbio` | url | `https://linkbio.co/...` |
| Linkme | `/v1/linkme` | url | `https://linkme.bio/...` |
| Amazon Shop | `/v1/amazon/shop` | url | `https://www.amazon.com/shop/...` |
| Instagram basic profile | `/v1/instagram/basic/profile` | userId | `314216` |
| Instagram embed HTML | `/v1/instagram/user/embed` | handle | `jane` |
| Age/Gender detect | `/v1/detect/age-gender` | url (social profile) | `https://www.tiktok.com/@charlidamelio` |
| Credit balance | `/v1/credit/balance` | (none) | |

## Credit Costs

Most endpoints cost **1 credit** per request. Exceptions:

| Endpoint | Cost | Condition |
|----------|------|-----------|
| `/v1/tiktok/user/audience` | 26 credits | always |
| `/v1/tiktok/video/transcript` | +10 credits | when `use_ai_as_fallback=true` |
| `/v1/google/company/ads` | 25 credits | when `get_ad_details=true` |

Check balance with `/v1/credit/balance`. Warn users before calling expensive endpoints.

## Pagination

Paginated endpoints return a cursor/token in the response. Pass it back as a query param to get the next page.

| Cursor Field | Used By |
|-------------|---------|
| `cursor` | TikTok comments/search/song videos, Instagram comments, Reddit subreddit search, Pinterest, Bluesky, Facebook reels/photos/posts/comments, TikTok Shop products/user showcase |
| `max_cursor` | TikTok profile videos |
| `min_time` | TikTok following/followers |
| `continuationToken` | YouTube (all paginated endpoints) |
| `after` | Reddit posts, Reddit search |
| `next_max_id` | Instagram posts, Truth Social posts |
| `max_id` | Instagram reels |
| `page` | TikTok popular/shop, Instagram reels search, LinkedIn company posts, TikTok Shop reviews |
| `paginationToken` | LinkedIn ads |

## Common Optional Params

- **`trim`** (boolean): reduces response payload size. Use when you only need key metrics.
- **`region`** (string): 2-letter country code for proxy location. Does NOT filter by region -- just routes the request through that country's proxy.

## Known Limitations

- **Handles**: pass without the `@` symbol. Use `charlidamelio` not `@charlidamelio`. Applies to TikTok, Instagram, Twitter, Threads, Bluesky, Snapchat, Twitch, Pinterest, Truth Social
- **YouTube handles**: pass without the `@` symbol. Use `ThePatMcAfeeShow` not `@ThePatMcAfeeShow`. You can also pass a channelId (e.g. `UC-9-kyTW8ZkZNDHQJ6FgpwQ`) or full URL instead
- **Hashtags**: pass without the `#` symbol. Use `fyp` not `#fyp`. Applies to TikTok and YouTube hashtag search endpoints
- **Twitter**: returns ~100 most popular tweets, not chronological/latest
- **Threads**: only last 20-30 posts visible publicly
- **Facebook posts**: only 3 posts per page (API limitation)
- **Facebook group posts**: only 3 posts per page (same API limitation)
- **LinkedIn company posts**: max 7 pages
- **Instagram play counts**: IG-only views (excludes cross-posted FB views)
- **Truth Social**: only prominent users (Trump, Vance, etc.) work publicly
- **Instagram song reels**: deprecated (endpoint exists but non-functional)
- **Transcripts**: all transcript endpoints require video under 2 minutes
- **Reddit subreddit names**: case-sensitive! Use "AskReddit" not "askreddit"
