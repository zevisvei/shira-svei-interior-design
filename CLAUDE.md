# website/: Shira Svei Interior Design (Zevi's site)

Project-specific notes. The shared rules for both sites are in `../CLAUDE.md`.

- Whose site: Zevi's (GitHub zevisvei).
- Live: https://zevisvei.github.io/shira-svei-interior-design/
- Git repo: this folder is a clone of zevisvei/shira-svei-interior-design (branch `main`).
- Build: `python3 build.py` in this folder. It needs Python 3.12+ (`~/.local/bin/python3`, not `/usr/bin/python3`).
- Deploy: rebuild, then commit the generated files and push to `main`. GitHub Actions (`.github/workflows/pages.yml`) publishes `site/`.
- Local preview: launch config `website`, port 8765.

Read `PRODUCT.md` (business, voice) and `DESIGN.md` (visual system: olive, brass, Jost, Instrument Sans) before changing any page.

## Code

- `build.py` generates every HTML page in `site/` (including `site/projects/`, `404.html`, `sitemap.xml` and `robots.txt`) from one shared header, footer and set of helpers. **Never hand-edit the generated HTML.**
- These are hand-written and edited directly: `site/css/site.css`, `site/js/site.js` and `site/js/hero3d.js`.
- `site/vendor/` holds pinned local copies of three.js 0.170.0 and GSAP 3.12.5 + ScrollTrigger, loaded on the homepage only.
  - Don't switch them to a CDN.
  - Don't add a smooth-scroll library: Lenis made wheel scrolling unreliable.
- `404.html` uses absolute asset URLs (from `SITE_URL`).
- All assets are local. The only external requests are Google Fonts and, if configured, Google Analytics.
- The config at the top of `build.py`:
  - `SITE_URL`: no trailing slash.
  - `GA_ID`: the GA4 ID. Empty means no tag. The contact form fires `generate_lead`.
  - `GSC_VERIFICATION`: the Search Console token.

## Testing

The homepage hero is a scroll-driven three.js scene (see DESIGN.md). Test it:
- at several scroll positions
- with `prefers-reduced-motion: reduce`, where it must fall back to the photo hero
- at 390px

## Known gaps

- The contact form has no backend: it copies the text.
- `img/logo.png` is low-res and only works on dark backgrounds.
- `img/open-living.webp` is only 1250px wide.
- Still needed from the owner: prices, reply time, founder photo and About text, real testimonials, a WhatsApp number, a booking link.
