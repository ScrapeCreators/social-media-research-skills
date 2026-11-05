# ScrapeCreators endpoint reference

Generated from the official `scrapecreators-cli` api-config (v1.0.108, synced 2026-11-04).
189 endpoints, all `GET`, base URL `https://api.scrapecreators.com`, header `x-api-key`.

How to read this table:

* **Required** must be sent. When a row lists alternatives in Optional (for example `handle` or `user_id`), one of them is usually enough; check the per-endpoint OpenAPI spec if a call returns 400.
* **Pagination** is the param you pass on the next call. Its value comes from the same-named field in the previous response, unless the row shows `param ← response field`. `page` is a plain counter.
* **Credits** is per successful request (per page for paginated calls). Default is 1.
* Per-endpoint OpenAPI spec: `https://docs.scrapecreators.com/{path}/openapi.json`.

Regenerate this file when the CLI config changes instead of editing rows by hand.

## TikTok

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/tiktok/ad-library/ad` | `ad_id` | - | - | 1 | Gets details for a TikTok ad from either Creative Center Top Ads or TikTok's public Ads Library. |
| `/v1/tiktok/ad-library/search` | - | `query`, `advertiser_name`, `adv_biz_ids`, `cursor` | `cursor` | 1 | Search TikTok's public Ads Library by general query or advertiser name. |
| `/v1/tiktok/collection/videos` | `url` | `cursor` | `cursor` ← response `max_cursor` | 1 | Scrapes the videos in a public TikTok collection. |
| `/v1/tiktok/get-trending-feed` | `region` | `trim` | - | 1 | Get the trending feed from TikTok. |
| `/v1/tiktok/hashtags/popular` | - | `period`, `page`, `countryCode`, `newOnBoard`, `industry` | `page` (1, 2, 3…) | 1 | Get popular hashtags from TikTok. |
| `/v1/tiktok/live` | `room_id`, `user_id` | - | - | 1 | Gets info for a TikTok live room, including like count. |
| `/v1/tiktok/product` | `url` | `region` | - | 1 | Get details for a TikTok Shop product. |
| `/v1/tiktok/profile` | - | `handle`, `user_id` | - | 1 | Scrapes a public TikTok profile |
| `/v1/tiktok/profile/region` | `handle` | - | - | 1 | Gets the region/country code for a TikTok profile. |
| `/v1/tiktok/search/hashtag` | `hashtag` | `region`, `cursor`, `trim` | `cursor` | 1 | Search TikTok videos by hashtag. |
| `/v1/tiktok/search/keyword` | `query` | `date_posted`, `sort_by`, `region`, `cursor`, `trim` | `cursor` | 1 | Search TikTok videos by keyword. |
| `/v1/tiktok/search/suggestions` | `query` | `region` | - | 1 | Gets TikTok autocomplete search suggestions for a query. |
| `/v1/tiktok/search/top` | `query` | `publish_time`, `sort_by`, `region`, `cursor` | `cursor` | 1 | Search TikTok Top results for videos and photo carousels; keyword search returns videos only. |
| `/v1/tiktok/search/users` | `query` | `cursor`, `trim` | `cursor` | 1 | Scrapes TikTok users matching a search query |
| `/v1/tiktok/shop/product/reviews` | - | `url`, `product_id`, `region`, `page` | `page` (1, 2, 3…) | 1 | Get a product's reviews |
| `/v1/tiktok/shop/products` | `url` | `cursor`, `sort_by`, `region` | `cursor` | 1 | Get products from a TikTok Shop for 1 credit per request. |
| `/v1/tiktok/shop/search` | `query` | `page`, `region` | `page` (1, 2, 3…) | 1 | Search TikTok Shop products by keyword. |
| `/v1/tiktok/song` | `clipId` | - | - | 1 | Get details for a TikTok sound or song. |
| `/v1/tiktok/song/videos` | - | `clipId`, `cursor` | `cursor` | 1 | Get the TikToks using a song |
| `/v1/tiktok/user/audience` | `handle` | - | - | 26 | Get audience countries for a TikTok user. |
| `/v1/tiktok/user/followers` | - | `handle`, `user_id`, `min_time`, `trim` | `min_time` | 1 | Scrapes followers of a TikTok account |
| `/v1/tiktok/user/following` | `handle` | `min_time`, `trim` | `min_time` | 1 | Scrapes accounts that a TikTok user follows |
| `/v1/tiktok/user/live` | `handle` | - | - | 1 | Checks TikTok live status and room details. |
| `/v1/tiktok/user/showcase` | `handle` | `region`, `cursor` | `cursor` | 1 | Get products from a TikTok user's public showcase. |
| `/v1/tiktok/video/comment/replies` | `comment_id`, `'url'` | `cursor` | `cursor` | 1 | Scrapes replies to a TikTok comment |
| `/v1/tiktok/video/comments` | `url` | `cursor`, `trim` | `cursor` | 1 (1 credit per page with comments; 0 credits for empty pages) | Get comments on public TikTok videos or slideshows. |
| `/v1/tiktok/video/transcript` | `url` | `language`, `use_ai_as_fallback` | - | 1 (native or AI <=2 min), 10/started min with allow_long_transcription=true, 0 if empty | Get native captions or an opt-in AI transcript with timestamp segments from a TikTok video. |
| `/v2/tiktok/video` | `url` | `get_transcript`, `region`, `trim`, `download_media` | - | 1 | Get a public TikTok video or slideshow. |
| `/v3/tiktok/profile/videos` | `handle` | `user_id`, `sort_by`, `max_cursor`, `region`, `include_pinned`, `trim` | `max_cursor` | 1 | Get posts from a TikTok profile. |

## Instagram

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/instagram/audio/reels` | `audio_id` | `cursor` | `cursor` | 1 | Get public reels associated with an Instagram audio ID. |
| `/v1/instagram/basic-profile` | - | `userId` | - | 1 | Get profile details without posts using a numeric userId. |
| `/v1/instagram/post` | `url` | `region`, `trim`, `download_media`, `include_play_count` | - | 1 | Get public post or reel details. |
| `/v1/instagram/post/comment/replies` | `url`, `comment_id` | `cursor` | `cursor` | 1 | Get replies to an Instagram comment. |
| `/v1/instagram/profile` | `handle` | `trim` | - | 1 | Get public profile details, recent posts, and related accounts. |
| `/v1/instagram/profile/post-count` | `handle` | `allow_estimated` | - | 1 | Get a profile's post count. |
| `/v1/instagram/reels/trending` | - | - | - | 1 | Get popular reels from the last seven days, not an official global ranking. |
| `/v1/instagram/search` | `query` | - | - | 1 | Find users, hashtags, and places with Instagram search. |
| `/v1/instagram/search/hashtag` | `hashtag` | `date_posted`, `media_type`, `cursor` | `cursor` | 1 | Find Google-indexed public posts by exact hashtag, with date filters and pagination. |
| `/v1/instagram/search/popular` | `query` | `cursor` | `cursor` | 1 | Explore an Instagram topic with its description, sources, suggested terms, media count, and paginated posts. |
| `/v1/instagram/search/profiles` | `query` | - | - | 1 | Find ranked profiles with Instagram search, without Google. |
| `/v1/instagram/user/embed` | `handle` | - | - | 1 | Get the HTML embed for an Instagram profile. |
| `/v1/instagram/user/highlight/detail` | - | `id` | - | 1 | Get a story highlight's details and stories. |
| `/v1/instagram/user/highlights` | - | `user_id`, `handle` | - | 1 | Get up to 10 story highlights visible without signing in. |
| `/v1/instagram/user/reels` | - | `user_id`, `handle`, `max_id`, `require_play_counts`, `trim` | `max_id` | 1 | Get public reels by user_id or handle. |
| `/v1/instagram/user/tagged-posts` | `user_id` | `cursor` | `cursor` | 1 | Get public posts that tag an Instagram user. |
| `/v2/instagram/media/transcript` | `url` | - | - | 1 (AI <=2 min), 10/started min with allow_long_transcription=true, 0 if empty | Get AI transcripts with timestamp segments for videos in an Instagram post or reel. |
| `/v2/instagram/post/comments` | `url` | `cursor`, `include_replies` | `cursor` | 1 | Get post or reel comments; expect about 90% success. |
| `/v2/instagram/reels/search` | `query` | `date_posted`, `page` | `page` (1, 2, 3…) | 1 | Find Google-indexed reels by keyword, with date filters and pagination. |
| `/v2/instagram/user/posts` | `handle` | `next_max_id`, `require_play_counts`, `trim` | `next_max_id` | 1 | Get public posts and reels with pagination. |

## YouTube

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/youtube/channel` | - | `channelId`, `handle`, `url` | - | 1 | Get YouTube channel details and stats by channelId, handle, or URL. |
| `/v1/youtube/channel-videos` | - | `channelId`, `handle`, `sort`, `continuationToken`, `includeExtras` | `continuationToken` | 1 | Get paginated videos from a YouTube channel by channelId or handle. |
| `/v1/youtube/channel/community-posts` | - | `channelId`, `handle`, `continuationToken` | `continuationToken` | 1 | Get community posts from a YouTube channel. |
| `/v1/youtube/channel/lives` | - | `channelId`, `handle`, `continuationToken` | `continuationToken` | 1 | Get live streams and past streams from a YouTube channel. |
| `/v1/youtube/channel/playlists` | - | `channelId`, `handle`, `continuationToken` | `continuationToken` | 1 | Get playlists from a YouTube channel. |
| `/v1/youtube/channel/shorts` | - | `handle`, `channelId`, `sort`, `continuationToken` | `continuationToken` | 1 | Get channel Shorts. |
| `/v1/youtube/community-post` | `url` | - | - | 1 | Get the details of a community post |
| `/v1/youtube/playlist` | `playlist_id` | `continuationToken` | `continuationToken` | 1 | Get a paginated list of videos in a YouTube playlist |
| `/v1/youtube/search` | `query` | `uploadDate`, `sortBy`, `type`, `duration`, `region`, `continuationToken`, `includeExtras` | `continuationToken` | 1 | Search YouTube videos, channels, playlists, Shorts and live streams. |
| `/v1/youtube/search/hashtag` | `hashtag` | `continuationToken`, `type` | `continuationToken` | 1 | Search YouTube and get matching videos, channels, and playlists |
| `/v1/youtube/search/typeahead` | `query` | - | - | 1 | Get the live autocomplete suggestions shown in YouTube's search dropdown. |
| `/v1/youtube/shorts/trending` | - | - | - | 1 | Get about 48 trending Shorts per request. |
| `/v1/youtube/video` | `url` | `language` | - | 1 | Get YouTube video or Short details, description cards, AI disclosures, owner/uploader identities, paid-promot… |
| `/v1/youtube/video/comment/replies` | `continuationToken` | - | `continuationToken` | 1 | Get replies to a specific comment on a YouTube video. |
| `/v1/youtube/video/comments` | `url` | `continuationToken`, `order` | `continuationToken` | 1 | Get comments from a video. |
| `/v1/youtube/video/sponsors` | `url` | `language` | - | 1 | Experimental: infer possible video sponsors from public evidence, not an official YouTube sponsor field. |
| `/v1/youtube/video/transcript` | `url` | `language`, `original_audio` | - | 1 | Get publicly available captions or a transcript from a YouTube video or Short |

## Facebook

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/facebook/adLibrary/ad` | - | `get_transcript`, `id`, `url`, `trim` | - | 1 | Get Facebook Ad Library details by ID or URL. |
| `/v1/facebook/adLibrary/ad/transcript` | - | `id`, `url` | - | 1 (native or AI <=2 min), 10/started min with allow_long_transcription=true, 0 if empty | Get native captions or an AI transcript from a Facebook video ad. |
| `/v1/facebook/adLibrary/company/ads` | - | `pageId`, `companyName`, `country`, `status`, `media_type`, `language`, `sort_by`, `start_date`, `end_date`, `cursor`, `trim` | `cursor` | 1 | Get a company's running ads. |
| `/v1/facebook/adLibrary/search/ads` | `query` | `sort_by`, `search_type`, `ad_type`, `country`, `language`, `status`, `media_type`, `start_date`, `end_date`, `cursor`, `trim` | `cursor` | 1 | Search Meta Ad Library by keyword. |
| `/v1/facebook/adLibrary/search/companies` | `query` | - | - | 1 | Search for companies by name and get their ad library page id |
| `/v1/facebook/event/details` | - | `id`, `url` | - | 1 | Get a specific event by its URL or id |
| `/v1/facebook/events` | `url` | `time`, `cursor` | `cursor` | 1 | Get events from a city's Facebook Events page. |
| `/v1/facebook/events/search` | `query` | `cursor` | `cursor` | 1 | Search public Facebook events by name. |
| `/v1/facebook/group` | - | `url`, `group_id` | - | 1 | Get the public About-page information for a Facebook group. |
| `/v1/facebook/group/posts` | - | `url`, `group_id`, `sort_by`, `cursor` | `cursor` | 1 | Get public Facebook group posts, with shared_post_id and shared_post_url when exposed. |
| `/v1/facebook/marketplace/item` | - | `id`, `url` | - | 1 | Get a Facebook Marketplace item, including rental listing_date_text and availability_text when Facebook expos… |
| `/v1/facebook/marketplace/location/search` | `query` | - | - | 1 | Searches Facebook Marketplace locations/cities and returns coordinates you can use with the Marketplace Searc… |
| `/v1/facebook/marketplace/search` | `lat`, `lng` | `query`, `category_id`, `radius_km`, `min_price`, `max_price`, `sort_by`, `delivery_method`, `condition`, `date_listed`, `availability`, `cursor` | `cursor` | 1 | Search Facebook Marketplace listings |
| `/v1/facebook/post` | `url` | `get_transcript` | - | 1 | Get a public Facebook post or Reel, with shared_post_id and shared_post_url when exposed. |
| `/v1/facebook/post/comment/replies` | `feedback_id`, `expansion_token` | `cursor` | `cursor` | 1 | Get the replies to a comment, including image, GIF, video and sticker attachments when available. |
| `/v1/facebook/post/comments` | - | `url`, `feedback_id`, `cursor` | `cursor` | 1 | Get the comments of a Facebook post or reel, including image, GIF, video and sticker attachments when availab… |
| `/v1/facebook/post/transcript` | `url` | - | - | 1 (native or AI <=2 min), 10/started min with allow_long_transcription=true, 0 if empty | Get native captions or an AI transcript from a Facebook video or Reel. |
| `/v1/facebook/profile` | `url` | `get_business_hours`, `include_gated_profile` | - | 1 | Get public Facebook profile information |
| `/v1/facebook/profile/events` | `url` | `cursor` | `cursor` | 1 | Get the events of a public Facebook page |
| `/v1/facebook/profile/photos` | `url` | `next_page_id`, `cursor` | `cursor` | 1 | Get a public Facebook page's photos. |
| `/v1/facebook/profile/posts` | - | `url`, `pageId`, `cursor` | `cursor` | 1 | Get public Facebook profile posts visible without login, 3 per page, with available link previews and video d… |
| `/v1/facebook/profile/reels` | `url` | `next_page_id`, `cursor` | `cursor` | 1 | Get up to 10 page Reels. |
| `/v1/facebook/search/videos` | `query` | `cursor` | `cursor` | 1 | Search public Facebook videos and Reels by keyword, not text or photo posts. |

## LinkedIn

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/linkedin/ad` | `url` | - | - | 1 | Get ad details and native media variants where available. |
| `/v1/linkedin/ads/search` | - | `company`, `keyword`, `companyId`, `countries`, `startDate`, `endDate`, `paginationToken` | `paginationToken` | 1 | Search the LinkedIn Ad Library with native media variants where available. |
| `/v1/linkedin/company` | `url` | - | - | 1 | Get a LinkedIn company page |
| `/v1/linkedin/company/posts` | `url` | `page` | `page` (1, 2, 3…) | 1 | Get LinkedIn company or school posts by /company/ or /school/ URL. |
| `/v1/linkedin/post` | `url` | - | - | 1 | Get a LinkedIn post or article. |
| `/v1/linkedin/post/transcript` | `url` | - | - | 1 | Get a LinkedIn post video's native transcript when available. |
| `/v1/linkedin/profile` | `url` | - | - | 1 | Get a public LinkedIn profile and recent posts as seen without login. |
| `/v1/linkedin/search/posts` | `query` | `date_posted`, `cursor` | `cursor` | 1 | Search for public LinkedIn posts by keyword. |

## Twitter / X

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/twitter/community` | `url` | - | - | 1 | Get X/Twitter Community details. |
| `/v1/twitter/community/tweets` | `url` | - | - | 1 | Get tweets from an X/Twitter Community. |
| `/v1/twitter/profile` | `handle` | - | - | 1 | Get Twitter profile information including stats and metadata |
| `/v1/twitter/search/posts` | `query` | `cursor` | `cursor` | 1 (1 credit per successful page, including empty results. Failed requests and terminal cursor replays are not charged) | Search public X/Twitter posts by keyword using Google-indexed results, then fetch the post details without a… |
| `/v1/twitter/tweet` | `url` | `trim` | - | 1 | Get detailed information about a specific tweet including engagement |
| `/v1/twitter/tweet/transcript` | `url` | - | - | 1 (native or AI <=2 min), 10/started min with allow_long_transcription=true, 0 if empty | Get an AI transcript from a video tweet. |
| `/v1/twitter/user-tweets` | `handle` | `trim` | - | 1 | Get up to 100 popular tweets from a user's public profile, not their latest tweets. |

## Reddit

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/reddit/post` | `url` | - | - | 1 | Get information from a Reddit post without comments |
| `/v1/reddit/post/comments` | `url` | `cursor`, `trim` | `cursor` | 1 | Get Reddit post details and comments. |
| `/v1/reddit/post/transcript` | `url` | `language` | - | 1 | Get the transcript from a Reddit video post |
| `/v1/reddit/search` | `query` | `filter`, `sort`, `timeframe`, `after`, `trim` | `after` | 1 | Search Reddit for posts or comments. |
| `/v1/reddit/subreddit` | `subreddit` | `timeframe`, `sort`, `after`, `trim` | `after` | 1 | Get recent posts from a subreddit with engagement metrics |
| `/v1/reddit/subreddit/details` | - | `subreddit`, `url` | - | 1 | Get details about a subreddit. |
| `/v1/reddit/subreddit/search` | `subreddit` | `query`, `sort`, `timeframe`, `cursor` | `cursor` | 1 | Search within a subreddit for posts, comments, or media matching a query |

## Threads

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/threads/post` | `url` | `trim` | - | 1 | Get a post by url. |
| `/v1/threads/profile` | `handle` | - | - | 1 | Get Threads profile info |
| `/v1/threads/search` | `query` | `start_date`, `end_date`, `trim` | - | 1 | Search public Threads posts by keyword, up to 10 results per request. |
| `/v1/threads/search/users` | `query` | - | - | 1 | Search for users by username |
| `/v1/threads/user/posts` | `handle` | `trim` | - | 1 | Get a user's public Threads posts, limited to roughly the latest 20–30 posts. |

## Bluesky

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/bluesky/post` | `url` | - | - | 1 | Get Bluesky post |
| `/v1/bluesky/profile` | `handle` | - | - | 1 | Get Bluesky profile info |
| `/v1/bluesky/user/posts` | - | `handle`, `user_id` | `cursor` | 1 | Get Bluesky user posts. |

## Pinterest

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/pinterest/board` | `url` | `cursor`, `trim` | `cursor` | 1 | Get pins from a Pinterest board. |
| `/v1/pinterest/pin` | `url` | `trim` | - | 1 | Get Pinterest pin |
| `/v1/pinterest/search` | `query` | `cursor`, `trim` | `cursor` | 1 | Search Pinterest |
| `/v1/pinterest/topic` | `url` | - | - | 1 | Get a Pinterest topic's search-interest count, last-updated time, and refinement chips from its ideas URL. |
| `/v1/pinterest/user/boards` | `handle` | `trim` | `cursor` | 1 | Get a user's boards |

## Truth Social

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/truthsocial/post` | `url` | `download_media` | - | 1 | Get Truth Social post |
| `/v1/truthsocial/profile` | `handle` | - | - | 1 | Get Truth Social profile info |
| `/v1/truthsocial/user/posts` | - | `handle`, `user_id`, `next_max_id`, `trim` | `next_max_id` | 1 | Get posts from prominent public Truth Social accounts, such as Trump and Vance. |

## Twitch

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/twitch/clip` | see spec | - | - | 1 | Get Twitch clip |
| `/v1/twitch/clip/transcript` | `url` | `use_ai_as_fallback` | - | 1 (native or AI <=2 min), 10/started min with allow_long_transcription=true, 0 if empty | Get native captions from a Twitch clip. |
| `/v1/twitch/profile` | `handle` | - | - | 1 | Get Twitch profile |
| `/v1/twitch/user/schedule` | `handle` | - | - | 1 | Get Twitch user schedule |
| `/v1/twitch/user/videos` | `handle` | `filter_by`, `sort_by` | - | 1 | Get Twitch user videos |

## Kick

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/kick/clip` | `url` | - | - | 1 | Get Kick clip |
| `/v1/kick/clip/transcript` | `url` | `use_ai_as_fallback` | - | 1 (native or AI <=2 min), 10/started min with allow_long_transcription=true, 0 if empty | Get native captions from a Kick clip. |

## Snapchat

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/snapchat/profile` | `handle` | - | - | 1 | Get Snapchat user profile |
| `/v1/snapchat/spotlight` | `url` | - | - | 1 | Get Snapchat Spotlight video data by URL |
| `/v1/snapchat/spotlight/comments` | `url` | `cursor` | `cursor` | 1 | Get comments from a Snapchat Spotlight URL |

## Rumble

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/rumble/channel/videos` | - | `handle`, `url`, `cursor` | `cursor` | 1 | Gets videos from a Rumble channel by handle or URL. |
| `/v1/rumble/search` | `query` | `cursor` | `cursor` | 1 | Searches Rumble videos by keyword. |
| `/v1/rumble/video` | `url` | - | - | 1 | Gets Rumble video details by URL. |
| `/v1/rumble/video/comments` | `url` | - | - | 1 | Gets all top level comments for a Rumble video by URL. |
| `/v1/rumble/video/transcript` | `url` | - | - | 1 | Gets a Rumble video's transcript when captions are available. |

## Google

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/google/ad` | `url` | - | - | 1 | Get Google ad details. |
| `/v1/google/adLibrary/advertisers/search` | `query` | `region` | - | 1 | Search the Google Ad Transparency Library for advertisers to get their advertiser id. |
| `/v1/google/company/ads` | - | `domain`, `advertiser_id`, `topic`, `region`, `start_date`, `end_date`, `platform`, `format`, `get_ad_details`, `cursor` | `cursor` | 1; 25 with get_ad_details=true | Get public company ads with dates when available (1 credit). |
| `/v1/google/search` | `query` | `region`, `date_posted`, `page` | `page` (1, 2, 3…) | 1 | Search Google |

## Spotify

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/spotify/album` | - | `id`, `url` | - | 1 | Get Spotify album |
| `/v1/spotify/artist` | - | `id`, `url` | - | 1 | Get Spotify artist |
| `/v1/spotify/playlist` | - | `id`, `url`, `cursor` | `cursor` | 1 | Get a Spotify playlist and its tracks |
| `/v1/spotify/podcast` | - | `id`, `url` | - | 1 | Get Spotify podcast |
| `/v1/spotify/podcast/episodes` | - | `id`, `url`, `cursor` | `cursor` | 1 | Get Spotify podcast episodes |
| `/v1/spotify/search` | `query` | - | - | 1 | Search Spotify |
| `/v1/spotify/track` | - | `id`, `url` | - | 1 | Get Spotify track |

## Apple Music

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/apple-music/album` | - | `id`, `url` | - | 1 | Get Apple Music album |
| `/v1/apple-music/artist` | - | `id`, `url` | - | 1 | Get Apple Music artist |
| `/v1/apple-music/search` | `query` | `type` | - | 1 | Search Apple Music |
| `/v1/apple-music/track` | - | `id`, `url` | - | 1 | Get Apple Music track |

## SoundCloud

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/soundcloud/artist` | - | `handle`, `url` | - | 1 | Get SoundCloud artist details and follower counts by handle or URL. |
| `/v1/soundcloud/artist/tracks` | - | `handle`, `url`, `cursor` | `cursor` | 1 | Gets tracks/songs for a SoundCloud artist by handle or URL. |
| `/v1/soundcloud/track` | `url` | - | - | 1 | Gets detailed information about a SoundCloud track/song by URL. |

## GitHub

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/github/repository` | `url` | - | - | 1 | Get public metadata for one GitHub repository. |
| `/v1/github/trending/developers` | - | `language`, `since` | - | 1 | Get GitHub trending developers. |
| `/v1/github/trending/repositories` | - | `language`, `since`, `spoken_language_code` | - | 1 | Get GitHub trending repositories. |
| `/v1/github/user` | - | `handle`, `url` | - | 1 | Get public GitHub user details for a user. |
| `/v1/github/user/activity` | - | `handle`, `url`, `year`, `cursor` | `cursor` | 1 | Get public GitHub profile contribution activity for a user. |
| `/v1/github/user/contributions` | - | `handle`, `url`, `year` | - | 1 | Get a user's GitHub contribution graph for a year. |
| `/v1/github/user/followers` | - | `handle`, `url`, `cursor` | `cursor` | 1 | Get public followers for a GitHub user. |
| `/v1/github/user/following` | - | `handle`, `url`, `cursor` | `cursor` | 1 | Get public accounts a GitHub user follows. |
| `/v1/github/user/pull-requests` | `handle` | `since`, `until`, `cursor` | `cursor` | 1 | Get public pull requests authored by a GitHub user. |
| `/v1/github/user/repositories` | - | `handle`, `url`, `type`, `sort`, `direction`, `cursor` | `cursor` | 1 | Get public repositories for a GitHub user. |

## Kwai

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/kwai/post` | - | `url` | - | 1 | Get public Kwai post details from a post URL. |
| `/v1/kwai/profile` | - | `handle`, `url` | - | 1 | Get public Kwai profile info from a handle or profile URL. |
| `/v1/kwai/user/posts` | - | `handle`, `url`, `cursor`, `count` | `cursor` | 1 | Get public posts from a Kwai handle or profile URL. |

## Telegram

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/telegram/channel` | see spec | - | - | 1 | Get public Telegram channel or group details from its web preview. |
| `/v1/telegram/channel/posts` | `handle` | `cursor` | `cursor` | 1 | Get one page of recent public posts from a Telegram channel or group. |
| `/v1/telegram/post` | see spec | - | - | 1 | Get one public Telegram post by URL. |

## Amazon

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/amazon/shop` | `url` | `pageToken` | - | 1 | Get products and other details from a creator's Amazon Shop page |

## Link-in-bio

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/komi` | `url` | - | - | 1 | Komi page |
| `/v1/linkbio` | `url` | - | - | 1 | Linkbio (lnk.bio) page |
| `/v1/linkme` | `url` | - | - | 1 | Get Linkme profile info by URL |
| `/v1/linktree` | `url` | - | - | 1 | Linktree page |
| `/v1/pillar` | `url` | - | - | 1 | Pillar page |

## Account and utilities

| Endpoint | Required | Optional | Pagination | Credits | What it returns |
|---|---|---|---|---|---|
| `/v1/account/credit-balance` | - | - | - | 1 | Get your remaining credit balance. |
| `/v1/account/get-api-usage` | - | `page`, `endpoint`, `statusCode` | `page` (1, 2, 3…) | 1 | View your recent API request history |
| `/v1/account/get-daily-usage-count` | - | - | - | 1 | Get your daily credit and request counts |
| `/v1/account/get-most-used-routes` | - | `start_time`, `end_time` | - | 1 | See which endpoints you use the most |
| `/v1/detect-age-gender` | `url` | - | - | 1 | Estimate a creator's age and gender from their profile photo using AI. |
| `/v1/find-creator-emails` | `platform`, `handle` | - | - | 10 (1 credit with no emails; 10 credits with any email (live lookups)) | Find public creator emails. |
| `/v1/find-social-profiles` | `platform`, `handle` | - | - | 10 | Find a creator's linked social profiles from a platform and handle. |
