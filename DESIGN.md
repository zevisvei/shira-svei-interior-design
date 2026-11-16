# Design system

Direction: a modern interior design studio. Photographs of finished rooms lead; floor plans prove the expertise. The palette comes from the logo (dark olive ground, brass-yellow mark, sage script).

## Color (tokens in `site/css/site.css` `:root`)

| Token | Hex | Role |
|---|---|---|
| `--olive` | `#38321f` | Header, footer, dark bands, primary buttons on light |
| `--olive-2` | `#463f29` | Hover on olive |
| `--olive-line` | `#5a5236` | Dividers on dark |
| `--brass` | `#e9c84b` | Primary button on dark, focus ring on dark, active nav |
| `--stone` | `#e8e7de` | Alternate light section, card behind the compare slider |
| `--paper` | `#f6f5f0` | Page background |
| `--ink` / `--muted` | `#29261a` / `#5f5b4b` | Text |
| `--on-dark` / `--on-dark-muted` | `#efeadb` / `#bdb69f` | Text on olive |

Brass is the only accent. Never add new hues. Avoid two dark sections back to back: alternate paper, stone and olive.

## Type

- Headings: **Jost** 300 (h3 400), tracking -0.015em, `text-wrap: balance`. Sentence case.
- Body: **Instrument Sans** 400/500/600, 17px, line-height 1.65, max 62ch.
- No script font, no all-caps labels, no monospace.

## Layout

- `.wrap`: max 1240px, gutter `clamp(16px, 5vw, 72px)`.
- Sections: `.section` with `--section` vertical padding; `.section-head` puts the h2 left and a one-line intro right.
- Homepage hero (`.hero3d`, `js/hero3d.js`): the real Apartment 12 sales plan lies on an olive ground. Scrolling through a 330svh pinned section raises its walls (detected from the drawing's dark pixels, merged into boxes, dark poché tops), tilts the camera from top-down to a 3/4 view, then opens the finished-room photo in a growing circle. Three step labels track progress (desktop only). The plan sits right of the copy on desktop and below it on mobile, with an olive scrim behind the text.
- The static hero is the fallback: full-bleed photo with olive scrim. It shows when WebGL fails, before JS runs, and under reduced motion. The header overlays it (`.top.over`).
- Inner pages: olive `.page-hero` with copy left and a photo or plan right (`.hero-visual`, add `.plan` for drawings on white).
- Closing `.cta` band: olive over the evening-kitchen photo, centered heading and one brass button.

## Components

- `.compare`: before/after slider for plans (range input over two stacked images). This is the signature element; use it whenever two images show the same plan before and after.
- `a.zoom` around an image opens the shared `<dialog class="lightbox">`; a sibling `figcaption` becomes the caption.
- `.ticks`: ruled list with a short dash marker.
- Stage timeline (home `.stage`, process `.rail`): numbers only because the four stages are a real sequence.
- Header: fixed; shrinks to 76px and turns solid after 40px of scroll (`.top.scrolled`). On mobile the menu is a full-screen olive sheet with large Jost links.
- Footer: logo and one-line description, Studio and Projects link columns, an inquiry button, then © and Back to top.
- `.closes`: dot-and-line timeline on olive for the order in which changes close. `.faq`: `<details>` list with a plus that turns into ×.
- Buttons: `.btn-brass` on dark, `.btn-olive` on light; 52px tall, 2px radius. `.link` is the text link with a 1px underline, 44px tap height.

## Motion

One entrance per page: hero copy rises (`.enter`), the brass rule draws. The homepage adds the scroll-driven 3D hero (GSAP ScrollTrigger, scrub 0.6) and a one-time clip-path unveil on photographs marked `.reveal`. The 3D scene renders only on scroll or pointer change, caps pixel ratio at 2, and adds a small pointer parallax on fine pointers. Everything else moves only in response to the user (slider, lightbox, hover zoom 1.025 on linked images). Lenis smooth scroll runs on every page; `.reveal` photographs unveil with a clip-path wipe (IntersectionObserver); pages cross-fade via the View Transitions API. All motion is off under `prefers-reduced-motion`.

## Don't

Eyebrow labels above headings, middle-dot meta strings, cards for everything, gradient text, glows, decorative script lines, colored side borders thicker than 1px, scroll-triggered fade-ins.
