# Claude Instructions

Use these skills as practical social media research workflows.

When a user asks for social research, prefer the narrow workflow skill that matches the job:

- Outlier performance -> `outlier-post-finder`
- Video/transcript analysis -> `transcript-intelligence`
- Comment/VOC mining -> `comment-mining`
- Competitor comparison -> `competitor-social-research`
- Ad library analysis -> `ad-library-teardown`
- Raw scraping/API lookup -> `scrapecreators-api`

If a workflow needs live public social data, use ScrapeCreators endpoints through the `scrapecreators-api` skill and the `SCRAPECREATORS_API_KEY` environment variable.
