# Social Media Research Skills Repo

This repo contains agent skills for practical social media research workflows powered by ScrapeCreators.

## Authoring Guidelines

- Skills live in `skills/<skill-name>/SKILL.md`.
- Keep skills workflow-first. Avoid turning every skill into an endpoint dump.
- Use `scrapecreators-api` as the raw endpoint-routing skill.
- Customer-facing wording should be simple and informal.
- Prefer examples that produce a concrete artifact: report, table, CSV, swipe file, teardown, or brief.
- Do not promise private/logged-in data. ScrapeCreators works with public data.
- When a workflow needs current endpoint parameters, fetch the endpoint docs or OpenAPI spec before calling the API.

## Validation

For docs-only changes, lightweight verification is enough:

```bash
git diff --check
python3 scripts/validate-skills.py
```

Do not run heavy builds unless code behavior or packaging changes.
