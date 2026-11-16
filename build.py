import os
SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')

# Fill these in, then run `python3 build.py`. Empty values leave the tag out.
SITE_URL = 'https://zevisvei.github.io/shira-svei-interior-design'  # live address, e.g. 'https://www.example.com' (no trailing slash)
GA_ID = ''             # Google Analytics 4 measurement ID, e.g. 'G-XXXXXXXXXX'
GSC_VERIFICATION = ''  # Search Console HTML-tag token: the content="..." value only

PAGES = []


def tracking_tags(path, P):
    tags = []
    if SITE_URL:
        url = SITE_URL + '/' + ('' if path == 'index.html' else path)
        tags.append(f'<link rel="canonical" href="{url}">\n<meta property="og:url" content="{url}">\n<meta property="og:image" content="{SITE_URL}/img/open-living.webp">')
    else:
        tags.append(f'<meta property="og:image" content="{P}img/open-living.webp">')
    if GSC_VERIFICATION:
        tags.append(f'<meta name="google-site-verification" content="{GSC_VERIFICATION}">')
    if GA_ID:
        tags.append(f'''<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>''')
    return '\n'.join(tags)

NAV = [('index.html', 'Home'), ('process.html', 'How we work'), ('work.html', 'Our work'), ('packages.html', 'Packages')]


def head(title, desc, P, current, path):
    items = ''.join(
        f'<li><a href="{P}{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a></li>' for h, t in NAV)
    cta_cur = ' aria-current="page"' if current == 'contact.html' else ''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#38321f">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<link rel="icon" href="{P}img/logo.png">
{tracking_tags(path, P)}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@200;300;400&family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{P}css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top{' over' if current == 'index.html' else ''}">
  <div class="wrap">
    <a class="brand" href="{P}index.html" aria-label="Shira Svei Interior Design, home">
      <img src="{P}img/logo.png" alt="Shira Svei Interior Design: love your space" width="936" height="460">
    </a>
    <nav class="nav" aria-label="Main">
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
      <ul id="menu">{items}<li><a class="nav-cta" href="{P}contact.html"{cta_cur}>Let’s talk</a></li></ul>
    </nav>
  </div>
</header>
<main id="main">
'''


def foot(P, cta=None, home=False):
    extra_scripts = f'<script src="{P}vendor/gsap.min.js"></script>\n<script src="{P}vendor/ScrollTrigger.min.js"></script>\n<script type="module" src="{P}js/hero3d.js"></script>\n' if home else ''
    band = ''
    if cta:
        h, p, btn, href = cta
        band = f'''<section class="cta dark">
  <div class="wrap">
    <h2>{h}</h2>
    <p>{p}</p>
    <a class="btn btn-brass" href="{P}{href}">{btn}</a>
  </div>
</section>
'''
    return f'''{band}</main>
<footer class="site-foot dark">
  <div class="wrap">
    <span>Shira Svei Interior Design, new-build apartments in Israel</span>
    <nav aria-label="Footer">
      <a href="{P}process.html">How we work</a>
      <a href="{P}work.html">Our work</a>
      <a href="{P}packages.html">Packages</a>
      <a href="{P}contact.html">Contact</a>
    </nav>
  </div>
</footer>
{extra_scripts}<script src="{P}js/site.js"></script>
</body>
</html>
'''


TALK = ('Have a plan you’d like to discuss?', 'Tell us what you’re buying for and which decisions are coming up.', 'Tell us about your apartment', 'contact.html')


def page(path, title, desc, current, body, cta=TALK):
    P = '../' * path.count('/')
    PAGES.append(path)
    html = head(title, desc, P, current, path) + body.replace('{P}', P) + foot(P, cta, path == 'index.html')
    os.makedirs(os.path.dirname(os.path.join(SITE, path)), exist_ok=True)
    open(os.path.join(SITE, path), 'w').write(html)


def compare(before, after, ar, lb, la, label, w=None):
    return f'''<div class="compare" style="aspect-ratio:{ar}">
  <img src="{{P}}img/{before}" alt="{lb}">
  <div class="after"><img src="{{P}}img/{after}" alt="{la}"></div>
  <div class="handle"></div>
  <input type="range" min="0" max="100" value="50" aria-label="{label}">
</div>'''


def zoomfig(img, alt, cap, w, h, extra=''):
    return f'''<figure{extra}>
  <a class="zoom" href="{{P}}img/{img}"><img src="{{P}}img/{img}" alt="{alt}" width="{w}" height="{h}" loading="lazy"></a>
  <figcaption>{cap}</figcaption>
</figure>'''


def proj_hero(kind, h1, lede, img, alt, w, h, plan=False):
    return f'''<section class="page-hero dark">
  <div class="wrap">
    <div class="copy enter">
      <p class="crumb"><a href="{{P}}work.html">Our work</a> / {kind}</p>
      <h1>{h1}</h1>
      <p class="lede">{lede}</p>
    </div>
    <div class="hero-visual{' plan' if plan else ''}"><img src="{{P}}img/{img}" alt="{alt}" width="{w}" height="{h}" fetchpriority="high"></div>
  </div>
</section>
'''

# ---------------- HOME ----------------
home = '''<section class="hero3d">
  <div class="hero3d-stage">
    <canvas class="hero3d-canvas" data-plan="{P}img/furniture-1-sales.webp" aria-hidden="true"></canvas>
    <div class="hero3d-photo"><img src="{P}img/open-living.webp" alt="Living room opening onto a dining area and wood kitchen" width="1250" height="1284" fetchpriority="high"></div>
    <ol class="hero3d-steps" aria-hidden="true"><li>Sales plan</li><li>True scale</li><li>Your home</li></ol>
    <div class="wrap hero3d-wrap">
    <div class="copy enter">
      <h1>Your new&#8209;build apartment in Israel, handled from plan to move&#8209;in.</h1>
      <p class="lede">For American buyers who can’t be on site every week. We review the plans with you in English, speak with the contractor for you, and get the apartment ready to live in.</p>
      <div class="actions">
        <a class="btn btn-brass" href="{P}contact.html">Tell us about your apartment</a>
        <a class="link" href="#stages">See how we work</a>
      </div>
    </div>
    </div>
  </div>
</section>

<section class="section" id="stages">
  <div class="wrap">
    <div class="section-head">
      <h2>Four stages, one team on the ground</h2>
      <p>Buying off-plan happens in stages. Bring us in at any one of them, or have us with you through all four.</p>
    </div>

    <article class="stage">
      <div class="stage-mark" aria-hidden="true">1<small>When you get the prospectus</small></div>
      <div class="stage-text">
        <p class="when">When you get the prospectus</p>
        <h2>Is this the right apartment for you?</h2>
        <p>Before you commit, we review the contractor’s sales plan with you. We check real dimensions, furniture clearances, circulation and storage, so you know whether the space fits the way you live.</p>
      </div>
      <div class="stage-media">
        <div class="compare-card">
          <h3>A spacious living room. Or is it?</h3>
          <p>The sales plan makes the living and dining area look roomy. Drawn to scale, the dining chair overlaps the loveseat and blocks the way to the hallway. Drag to compare.</p>
          ''' + compare('living-area-sales.webp', 'living-area-scaled.webp', '394/388',
                        'Sales plan showing an apparent gap between the dining table and loveseat',
                        'The same plan with furniture drawn to scale: the dining chair overlaps the loveseat',
                        'Compare the sales plan with furniture drawn to scale') + '''
          <div class="compare-labels"><span><b>Sales plan</b></span><span><b>Drawn to scale</b></span></div>
          <a class="link" href="{P}projects/furniture-study.html">See the full study</a>
        </div>
      </div>
    </article>

    <article class="stage">
      <div class="stage-mark" aria-hidden="true">2<small>Once you’ve chosen the apartment</small></div>
      <div class="stage-text">
        <p class="when">Once you’ve chosen the apartment</p>
        <h2>Make the layout work for you.</h2>
        <p>We rethink the rooms around your family: room for another bedroom, a more open living area, more built-in storage. We draw the changes and take them to the contractor’s team.</p>
        <p class="note">Every contractor limits what can change. We know where the room to move is, and use it.</p>
      </div>
      <div class="stage-media pair">
        <a href="{P}projects/apartment-layout.html">
          <div class="plan-frame"><img src="{P}img/apartment-revised-sm.webp" alt="Revised plan with the former bedroom opened into the living area" loading="lazy"></div>
          <h3>A larger living area</h3><p>A bedroom opened up into more shared space.</p>
        </a>
        <a href="{P}projects/jerusalem-heights.html">
          <div class="plan-frame"><img src="{P}img/jh-plan-updated-sm.webp" alt="Revised plan showing the moved kitchen and a new third bedroom" loading="lazy"></div>
          <h3>Two bedrooms become three</h3><p>The kitchen moved to make room for a third bedroom.</p>
        </a>
      </div>
    </article>

    <article class="stage">
      <div class="stage-mark" aria-hidden="true">3<small>When selections are due</small></div>
      <div class="stage-text">
        <p class="when">When selections are due</p>
        <h2>Choose what goes into your home.</h2>
        <p>Tiles, the kitchen, air conditioning, doors and fixtures. We work with the contractor’s kitchen supplier or design the kitchen ourselves, and help you pick tiles in person or remotely.</p>
        <a class="link" href="{P}projects/bathrooms.html">See two bathrooms from plan to rendering</a>
      </div>
      <div class="stage-media photo-pair">
        <img class="reveal" src="{P}img/island.webp" alt="Stone kitchen island with wood cabinetry and slim pendant lights" width="602" height="774" loading="lazy">
        <img class="reveal" src="{P}img/backsplash.webp" alt="Wood kitchen cabinetry and a lit stone backsplash" width="834" height="1152" loading="lazy">
      </div>
    </article>

    <article class="stage">
      <div class="stage-mark" aria-hidden="true">4<small>Getting ready to move in</small></div>
      <div class="stage-text">
        <p class="when">Getting ready to move in</p>
        <h2>Furnish and style your home.</h2>
        <p>We plan and source furniture room by room, and design built-ins where they use the space better: a vanity fitted to the bathroom, storage set into a niche, a piece sized to keep a walkway clear. Then curtains, rugs, lighting, art and the last details.</p>
        <p>Our own local tradespeople and suppliers build and deliver it.</p>
        <a class="link" href="{P}packages.html#furnishing">Furnishing and styling</a>
      </div>
      <div class="stage-media wide-stack">
        <img class="reveal" src="{P}img/primary-bedroom-walnut.webp" alt="Bedroom rendering with walnut built-ins, a recessed bookshelf and floral pillows" width="1754" height="897" loading="lazy">
      </div>
    </article>
  </div>
</section>

<div class="band"><img class="reveal" src="{P}img/primary-bedroom-linen.webp" alt="Bedroom with linen curtains, fitted wardrobes and a reading chair" width="1756" height="895" loading="lazy"></div>

<section class="section stone film">
  <div class="wrap split">
    <div>
      <h2>We’re with you the whole way.</h2>
      <p style="margin-top:24px" class="muted">A revised drawing arrives, a supplier has a question, the contractor needs a decision by Thursday. We explain it in English and follow up with the team in Israel for you.</p>
      <a class="link" href="{P}packages.html#full-service">Full-service support</a>
    </div>
    <video controls preload="metadata" playsinline aria-label="Film: buying an apartment on paper">
      <source src="{P}film.mp4#t=0.5" type="video/mp4">
    </video>
  </div>
</section>
'''
page('index.html', 'Shira Svei Interior Design | New-build apartments in Israel',
     'Design support for American buyers of new-build apartments in Israel: plan review, layout changes, selections and furnishing, in English.',
     'index.html', home,
     ('Let’s talk about your new build.', 'Tell us where you are in the process and what’s coming up next.', 'Tell us about your apartment', 'contact.html'))

# ---------------- PROCESS ----------------
process = '''<section class="page-hero dark has-photo">
  <div class="wrap">
    <div class="copy enter">
      <h1>From sales plan to building plans</h1>
      <p class="lede">We work with buyers purchasing apartments on paper from Israeli contractors. Start while you’re still reviewing a sales plan, or after you’ve signed while changes are still possible. Send us the plan and your deadlines, and we’ll go through them together in English.</p>
    </div>
    <div class="hero-photo">
      <img src="{P}img/entry.webp" alt="Quiet neutral hallway with a dark wood door and recessed lighting" width="816" height="1210" fetchpriority="high">
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>Where we join you</h2>
      <p>Four points in an off-plan purchase where a decision is due. Each one closes for good once the contractor moves on.</p>
    </div>
    <ol class="rail">
      <li><span class="n">1</span><span class="t">Before you commit</span><h3>Review the prospectus</h3><p>We check the dimensions and draw furniture to scale, so you can see how the rooms, storage and clearances work before you choose the apartment.</p></li>
      <li><span class="n">2</span><span class="t">After you’ve chosen</span><h3>Adapt the layout</h3><p>We explore changes that fit the apartment to you, prepare the drawings and bring your requests to the contractor’s team.</p></li>
      <li><span class="n">3</span><span class="t">When selections are due</span><h3>Choose the details</h3><p>Tiles, kitchen design, air conditioning, doors and fixtures, with views of how your choices look in your own layout.</p></li>
      <li><span class="n">4</span><span class="t">Getting ready to move in</span><h3>Furnish and style</h3><p>We plan the furniture, source the pieces and add textiles, lighting, art and accessories, so the apartment is ready to live in.</p></li>
    </ol>
    <p class="aside-line">At every stage we explain the choices and deadlines in English, and act as your contact with the Israeli project team.</p>
  </div>
</section>

<section class="section stone">
  <div class="wrap split">
    <div>
      <h2>Downsizing from the U.S.: where will everything go?</h2>
      <p style="margin-top:24px" class="muted">In an Israeli apartment, coats, bulk groceries, luggage and seasonal things all need a place inside the living space. We look at what you use every day and where it makes sense to keep it. Sometimes moving a doorway frees a whole wall for storage and keeps the room easy to walk through.</p>
    </div>
    <div class="compare-us">
      <div>
        <h3>What you had in the U.S.</h3>
        <ul class="ticks"><li>A coat closet</li><li>A walk-in pantry</li><li>A basement or garage</li><li>A laundry room</li></ul>
      </div>
      <div>
        <h3>What we plan in its place</h3>
        <ul class="ticks"><li>A shallow cabinet near the entry</li><li>Full-height pantry storage</li><li>Wardrobes set into a niche</li><li>Cabinets above the washer and dryer</li></ul>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>What are you buying for?</h2>
      <p>The answer changes which decisions matter now and which can wait.</p>
    </div>
    <div class="options">
      <article><h3>Moving in at handover</h3><p>Plan the kitchen, storage, lighting and rooms around how your family lives today, so the apartment works from the day you get the keys.</p></article>
      <article><h3>A home for later</h3><p>Use the construction stage for the decisions that are hard to undo later, like walls, plumbing and electrical points, and keep the rest flexible.</p></article>
      <article><h3>An investment</h3><p>Weigh the contractor’s standard options against paid upgrades. For a rental, favor a practical layout, durable finishes and easy upkeep.</p></article>
    </div>
  </div>
</section>

<section class="section stone">
  <div class="wrap split">
    <div>
      <h2>What to send us from the U.S.</h2>
      <p style="margin-top:24px" class="muted">Tell us what you want to work better, whether that’s seating for Shabbos meals, kitchen storage or a bathroom layout.</p>
      <a class="btn btn-brass" style="margin-top:12px" href="{P}contact.html">Tell us about your apartment</a>
    </div>
    <ul class="ticks">
      <li>The sales plan, or the latest plan you received</li>
      <li>The developer’s list of standard finishes, if you have it</li>
      <li>Any deadline for submitting changes</li>
      <li>What you want to work better in the apartment</li>
    </ul>
  </div>
</section>
'''
page('process.html', 'How we work | Shira Svei Interior Design',
     'How we support buyers of new-build apartments in Israel, from the prospectus to move-in.',
     'process.html', process,
     ('Choose the support you need', 'Help with one decision, or a team with you as the apartment takes shape.', 'Compare packages', 'packages.html'))

# ---------------- PACKAGES ----------------
def pkg(id_, h, for_, items, btn, q):
    lis = ''.join(f'<li>{i}</li>' for i in items)
    return f'''<article class="pkg" id="{id_}">
      <div><h2>{h}</h2><p class="for">{for_}</p><a class="btn btn-olive" href="{{P}}contact.html?package={q}">{btn}</a></div>
      <ul class="ticks">{lis}</ul>
    </article>'''

packages = '''<section class="page-hero dark">
  <div class="wrap">
    <div class="copy enter">
      <h1>Design packages</h1>
      <p class="lede">Help with one decision, or one team with you from the first floor plan to the last cushion.</p>
    </div>
    <div class="duo">
      <img src="{P}img/daylight-kitchen.webp" alt="Daylit kitchen with walnut drawers and a stone countertop" width="490" height="820" fetchpriority="high">
      <img src="{P}img/kitchen-and-lounge.webp" alt="Light kitchen and living area with an island and tall windows" width="1046" height="1286">
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
''' + pkg('prospectus', 'Prospectus review', 'For buyers deciding whether a new-build apartment suits them, before they commit.',
          ['We go through the contractor’s sales plan and dimensions with you in English.',
           'We check furniture clearances, circulation, storage and how the layout fits your day.',
           'We point out the changes worth raising with the contractor.'],
          'Ask about a prospectus review', 'plan-review') + pkg(
    'selections', 'Tiles, bathrooms and kitchen', 'Your kitchen and bathroom decisions with one team, in person in Israel or remotely.',
    ['Floor and wall tiles chosen together with sinks, toilets, tubs and shower fittings.',
     'A kitchen planned around how you cook and host: layout, appliances, counters and storage.',
     'We work with the contractor’s kitchen supplier or an independent kitchen company, review the design with you and flag what to change.'],
    'Ask about selections', 'selections') + pkg(
    'furnishing', 'Furnishing and styling', 'For buyers who want the apartment furnished and ready to live in.',
    ['Furniture planned and sourced for each room, with custom cabinetry where the space calls for it.',
     'Our own local tradespeople and suppliers make and install the custom pieces.',
     'Rugs, curtains, lighting, art and accessories chosen to work together.',
     'The apartment styled so it feels finished when you arrive.'],
    'Ask about furnishing', 'furnishing') + '''
  </div>
</section>

<section class="pkg-full dark" id="full-service">
  <div class="wrap">
    <div>
      <h2>Full-service support</h2>
      <p style="margin-top:16px">One team on the ground in Israel, guiding you in English from the first floor plan through furnishing.</p>
      <a class="btn btn-brass" style="margin-top:12px" href="{P}contact.html?package=ongoing-support">Ask about full-service support</a>
    </div>
    <ul class="ticks">
      <li>We start with a plan review and set priorities and deadlines together.</li>
      <li>Layout changes, kitchen design, tile selection and every decision in between. We can also furnish and style the apartment.</li>
      <li>We speak with the contractor and suppliers for you, and follow up as questions come in.</li>
    </ul>
  </div>
</section>
'''
page('packages.html', 'Packages | Shira Svei Interior Design',
     'Design packages for new-build apartments in Israel: prospectus review, selections, furnishing and full-service support.',
     'packages.html', packages, None)

# ---------------- CONTACT ----------------
contact = '''<div class="contact-grid">
  <section class="contact-intro dark">
    <div class="enter">
      <h1>Let’s talk about your apartment.</h1>
      <p class="lede">Buying on paper from an Israeli contractor? Reach out while you’re reviewing the sales plan, or after you’ve signed while changes are still possible.</p>
      <p>Tell us what you’re buying for, what you need room for, and when your next decisions are due.</p>
    </div>
    <img src="{P}img/evening-kitchen.webp" alt="Open kitchen with dark pendant lights behind a gray sofa" width="800" height="1208">
  </section>
  <section class="contact-form" aria-labelledby="form-title">
    <h2 id="form-title">Your apartment inquiry</h2>
    <p class="muted">Fill this in and we’ll turn it into a message you can send us. A direct email address will be added here before launch.</p>
    <form id="inquiry" class="form" novalidate>
      <div class="field full">
        <label for="name">Your name</label>
        <input id="name" name="name" autocomplete="name" required aria-describedby="name-err" data-error="Add your name so we know who to reply to.">
        <p class="err" id="name-err"></p>
      </div>
      <div class="field">
        <label for="plans">Plans for the apartment</label>
        <select id="plans" name="plans"><option value="">Not sure yet</option><option>Move in at handover</option><option>Live there later</option><option>Buy as an investment</option></select>
      </div>
      <div class="field">
        <label for="stage">Where you are now</label>
        <select id="stage" name="stage"><option value="">Not sure yet</option><option>Reviewing the contractor’s sales plan</option><option>Signed, planning changes before construction</option><option>Choosing changes or finishes</option><option>Something else</option></select>
      </div>
      <div class="field full">
        <label for="package">Package</label>
        <select id="package" name="package"><option value="">Not sure yet</option><option value="plan-review">Prospectus review</option><option value="selections">Tiles, bathrooms and kitchen</option><option value="furnishing">Furnishing and styling</option><option value="ongoing-support">Full-service support</option></select>
      </div>
      <div class="field full">
        <label for="details">The project and upcoming decisions</label>
        <p class="hint" id="details-hint">The city, the contractor, the size of the apartment and any deadlines you’ve been given.</p>
        <textarea id="details" name="details" required aria-describedby="details-err" data-error="Tell us a little about the apartment and what’s coming up."></textarea>
        <p class="err" id="details-err"></p>
      </div>
      <div class="form-actions">
        <button class="btn btn-olive" type="submit">Copy my inquiry</button>
        <p class="status" role="status" aria-live="polite"></p>
      </div>
      <pre class="preview" aria-label="Your inquiry text"></pre>
    </form>
  </section>
</div>
'''
page('contact.html', 'Contact | Shira Svei Interior Design',
     'Tell us about your new-build apartment in Israel and which decisions are coming up.',
     'contact.html', contact, None)

# ---------------- WORK ----------------
def card(href, img, alt, kind, h, p, plan=False):
    return f'''<a href="{{P}}{href}"><div class="img{' plan' if plan else ''}"><img src="{{P}}img/{img}" alt="{alt}" loading="lazy"></div><span class="kind">{kind}</span><h2>{h}</h2><p>{p}</p></a>'''

work = '''<section class="page-hero dark">
  <div class="wrap">
    <div class="copy enter">
      <h1>Our work</h1>
      <p class="lede">Layouts we reworked, furniture studies, and bathrooms shown before a single tile was laid.</p>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap work-grid">
''' + card('projects/jerusalem-heights.html', 'jh-hero.webp', 'Open white kitchen looking across to the dining table', 'Jerusalem Heights, completed', 'Two bedrooms become three', 'The kitchen moved to the living room entrance, and the old kitchen became a bedroom.') \
    + card('projects/furniture-study.html', 'furniture-2-scaled.webp', '3D cutaway with furniture drawn to scale', 'Apartment 12, furniture study', 'A spacious living room. Or is it?', 'How much usable space is left once the furniture is drawn to scale.', True) \
    + card('projects/apartment-layout.html', 'apartment-revised-sm.webp', 'Revised apartment floor plan', 'Apartment redesign', 'A larger living area', 'The original and revised plans, side by side.', True) \
    + card('projects/bathrooms.html', 'tub-render-updated.webp', 'Rendering of a dark stone bathroom with a white tub', 'Two bathrooms', 'From bathroom plan to rendering', 'The chosen tile, vanity and lighting, seen together in the real layout.') + '''
  </div>
</section>
'''
page('work.html', 'Our work | Shira Svei Interior Design',
     'Apartment layouts, furniture studies and bathroom renderings for new-build apartments in Israel.',
     'work.html', work)

# ---------------- PROJECTS ----------------
fs = proj_hero('Apartment 12', 'A spacious living room. Or is it?',
               'The sales plan makes the living and dining area look roomy. Once we drew the furniture to scale, the end chair at the dining table overlapped the loveseat and blocked the way to the hallway. It’s the kind of detail worth checking before you choose an apartment.', 'furniture-2-scaled.webp', '3D cutaway with the furniture drawn to scale, showing the chair meeting the sofa', 1124, 724, True) + '''
<section class="proj-body">
  <div class="wrap">
    <div class="block">
      <h2>The plan</h2>
      ''' + compare('furniture-1-sales.webp', 'furniture-1-scaled.webp', '1126/756',
                    'Sales drawing suggesting open space between the dining table and the loveseat',
                    'Furniture drawn to scale: the end chair overlaps the loveseat and blocks the hallway',
                    'Compare the sales plan with furniture drawn to scale') + '''
      <div class="compare-labels"><span><b>Contractor’s sales plan</b>An apparent gap between table and loveseat</span><span style="text-align:right"><b>Furniture drawn to scale</b>The chair blocks the way to the hallway</span></div>
    </div>
    <div class="block">
      <h2>The same room in 3D</h2>
      ''' + compare('furniture-2-sales.webp', 'furniture-2-scaled.webp', '1126/724',
                    '3D cutaway of the sales layout showing the suggested gap',
                    '3D cutaway of the scaled layout showing the furniture blocking the hallway',
                    'Compare the 3D sales layout with the scaled layout') + '''
      <div class="compare-labels"><span><b>Sales layout</b></span><span><b>Scaled layout</b></span></div>
      <p style="margin-top:32px">We check clearances like these early, so you can decide whether to rearrange the room or ask the contractor to adjust the layout while it’s still possible.</p>
      <p class="small-print">The 3D views show furniture footprints. Heights and finishes are schematic.</p>
    </div>
  </div>
</section>
'''
page('projects/furniture-study.html', 'Furniture study, Apartment 12 | Shira Svei Interior Design',
     'A sales plan versus the same room with furniture drawn to scale.', 'work.html', fs)

al = proj_hero('Apartment redesign', 'A larger living area',
               'The revised plan opens the bedroom next to the living room into one larger shared space. It also reworks the walls and doorways around the main bedroom and its bathroom.', 'apartment-revised-sm.webp', 'Revised apartment floor plan', 1000, 749, True) + '''
<section class="proj-body">
  <div class="wrap">
    <h2>Original and revised plans</h2>
    ''' + compare('apartment-original.webp', 'apartment-revised.webp', '2439/1827',
                  'Original floor plan with an enclosed bedroom beside the living area',
                  'Revised floor plan with the bedroom wall removed and changes around the main bedroom and bathroom',
                  'Compare the original plan with the revised plan') + '''
    <div class="compare-labels"><span><b>Original contractor plan</b><a class="zoom link" href="{P}img/apartment-original.webp">Open full size</a></span><span style="text-align:right"><b>Revised plan</b><a class="zoom link" href="{P}img/apartment-revised.webp">Open full size</a></span></div>
  </div>
</section>
'''
page('projects/apartment-layout.html', 'Apartment redesign | Shira Svei Interior Design',
     'Original and revised plans of a new-build apartment with a larger living area.', 'work.html', al)

gal = [('jh-living.webp', 'Dining table and seating beside wide windows', 'Living and dining area'),
       ('jh-hero.webp', 'Open white kitchen looking across to the dining table and windows', 'Kitchen and dining area'),
       ('jh-kitchen.webp', 'White kitchen cabinets with a peninsula and two stools', 'Kitchen'),
       ('jh-bedroom.webp', 'Main bedroom with an upholstered headboard and tall window', 'Main bedroom'),
       ('jh-kids.webp', 'Built-in white bunk beds with storage drawers below', 'Children’s room'),
       ('jh-bathroom.webp', 'White floating vanity and glass shower against two-tone tile', 'Bathroom')]
jh = proj_hero('Jerusalem Heights, completed', 'How a two-bedroom apartment became a three-bedroom home',
               'The original plan had two bedrooms and a separate kitchen. We turned the kitchen into a third bedroom, then fitted a compact kitchen into the old laundry area and part of the living room entrance. The family gained a room, and the living and dining area stayed open.', 'jh-hero.webp', 'Open white kitchen looking across to the dining table and windows', 1500, 844) + '''
<section class="proj-body">
  <div class="wrap">
    <div class="block">
      <h2>Where the kitchen moved</h2>
      <div style="max-width:760px">''' + compare('jh-plan-original.webp', 'jh-plan-updated.webp', '1250/1345',
                    'Original developer plan with the separate kitchen on the right',
                    'Revised plan with a compact kitchen by the living room entrance and a bedroom in the old kitchen',
                    'Compare the original plan with our revised plan') + '''
      <div class="compare-labels"><span><b>Original developer plan</b>The kitchen was the room off the living area.</span><span style="text-align:right"><b>Our revised plan</b>The new kitchen sits by the living room entrance.</span></div></div>
    </div>
    <div class="block">
      <h2>The finished apartment</h2>
      <div class="gallery">
''' + '\n'.join(zoomfig(i, a, c, 1024, 576) for i, a, c in gal) + '''
      </div>
      <p class="small-print">Photos from the Shisha Realty listing.</p>
    </div>
  </div>
</section>
'''
page('projects/jerusalem-heights.html', 'Jerusalem Heights | Shira Svei Interior Design',
     'A two-bedroom new-build apartment in Jerusalem reworked into a three-bedroom home.', 'work.html', jh)


def bath(id_, h, p, pre, tile_w, tile_h, van_w, van_h, rend, rw, rh, plan_w, plan_h, alts):
    return f'''<article class="bath" id="{id_}">
      <header><h2>{h}</h2><p>{p}</p></header>
      <div class="selection">
        {zoomfig(pre + '-plan.webp', alts[0], 'Bathroom plan', plan_w, plan_h)}
        <div class="materials">
          {zoomfig(pre + '-tile.webp', alts[1], 'Chosen tile', tile_w, tile_h)}
          {zoomfig(pre + '-vanity.webp', alts[2], 'Chosen vanity', van_w, van_h)}
        </div>
        {zoomfig(rend, alts[3], 'Photorealistic rendering', rw, rh, ' class="render"')}
      </div>
    </article>'''

bt = proj_hero('Two bathrooms', 'From bathroom plan to rendering',
               'We take your bathroom plan and photos of the tile and vanity you chose, and build a photorealistic view of the room. You see how it all looks together in your own layout before work starts.', 'tub-render-updated.webp', 'Rendering of a dark stone bathroom with a white tub', 1135, 928) + '''
<section class="proj-body">
  <div class="wrap">
    ''' + bath('walk-in-shower', 'A walk-in shower', 'Beige tile and a fluted wood vanity with a white basin, seen from the doorway.', 'shower',
               494, 283, 1150, 623, 'shower-render.webp', 990, 1589, 606, 972,
               ['Dimensioned plan of the walk-in shower bathroom', 'Beige tile chosen for the shower bathroom',
                'Fluted wood vanity with a white basin', 'Rendering of the walk-in shower bathroom from the doorway']) + \
    bath('tub', 'A bathroom with a tub', 'Dark stone-look tile and a charcoal vanity, with the white tub and warm lighting in the planned layout.', 'tub',
         380, 255, 1150, 811, 'tub-render-updated.webp', 1135, 928, 822, 776,
         ['Dimensioned plan of the bathroom with a tub', 'Dark stone-look tile chosen for the tub bathroom',
          'Charcoal vanity with timber trim', 'Rendering of the dark tiled bathroom with a white tub']) + '''
  </div>
</section>
'''
page('projects/bathrooms.html', 'Bathroom renderings | Shira Svei Interior Design',
     'Two bathrooms shown from plan and chosen materials to photorealistic rendering.', 'work.html', bt)
print('ok')

robots = 'User-agent: *\nAllow: /\n'
if SITE_URL:
    robots += f'\nSitemap: {SITE_URL}/sitemap.xml\n'
    urls = ''.join(f'  <url><loc>{SITE_URL}/{"" if p == "index.html" else p}</loc></url>\n' for p in PAGES)
    open(os.path.join(SITE, 'sitemap.xml'), 'w').write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
open(os.path.join(SITE, 'robots.txt'), 'w').write(robots)
