# Shira Svei Interior Design

Static website for Shira Svei Interior Design: design support for American buyers of new-build apartments in Israel.

- `site/` is the website. Open `site/index.html`, or serve the folder: `cd site && python3 -m http.server`.
- `build.py` generates every page in `site/` from one template. Edit page content there, then run `python3 build.py`.

## Hosting and tracking

The site deploys to GitHub Pages on every push to `main` (`.github/workflows/pages.yml`).

At the top of `build.py`:

- `SITE_URL`: the live address. It sets canonical URLs, `sitemap.xml` and `robots.txt`.
- `GA_ID`: the Google Analytics 4 measurement ID (`G-...`). The contact form sends a `generate_lead` event.
- `GSC_VERIFICATION`: the Search Console HTML-tag verification token.

Run `python3 build.py` after changing them, then commit.
