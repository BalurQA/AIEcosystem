# AI Companies & Models Ecosystem Tracker

Interactive static HTML tracker with:
- searchable/filterable company cards
- clickable company detail drawer
- model/product catalog
- latest-updates timeline
- daily automated news discovery
- original source links
- no frontend framework required

## Run locally

Use a local web server because the page loads `data.json`:

```bash
python -m http.server 8000
```

Open `http://localhost:8000`.

## Daily updates

The included GitHub Actions workflow runs every day and executes `update.py`.
The updater uses Google News RSS with site restrictions to discover new articles,
then prepends them to `data.json`.

For the strongest data quality, keep the company/model catalog curated and use
the daily feed as the discovery layer. This avoids treating rumors or third-party
articles as confirmed model releases.

## GitHub Pages

Create a GitHub repository, upload all files, enable Pages for the repository,
and the `index.html` page becomes the interactive tracker. Enable Actions so the
daily workflow can commit `data.json` updates.

## Important

Daily news discovery is automated, but a news article is not automatically a
confirmed model release. The UI therefore keeps the curated model catalog
separate from the automatically discovered news timeline.
