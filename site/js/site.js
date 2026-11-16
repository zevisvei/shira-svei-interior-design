const header = document.querySelector('.top');
if (header) {
  const onScroll = () => header.classList.toggle('scrolled', scrollY > 40);
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

if (document.documentElement.classList.contains('js-reveal')) {
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -12% 0px' });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));

  // Section headings rise line by line, once.
  const splitLines = h => {
    const text = h.textContent.trim().replace(/\s+/g, ' ');
    h.textContent = '';
    const words = text.split(' ').map((w, i) => {
      const span = document.createElement('span');
      span.textContent = (i ? ' ' : '') + w;
      h.append(span);
      return span;
    });
    const lines = [];
    words.forEach(w => {
      const last = lines[lines.length - 1];
      if (last && Math.abs(last.top - w.offsetTop) < 4) last.words.push(w.textContent);
      else lines.push({ top: w.offsetTop, words: [w.textContent.trimStart()] });
    });
    h.textContent = '';
    h.setAttribute('aria-label', text);
    lines.forEach((l, i) => {
      const ln = document.createElement('span'), inner = document.createElement('span');
      ln.className = 'ln'; ln.setAttribute('aria-hidden', 'true');
      inner.textContent = l.words.join('');
      inner.style.transitionDelay = i * 90 + 'ms';
      ln.append(inner); h.append(ln);
    });
    h.classList.add('lines');
  };
  (document.fonts ? document.fonts.ready : Promise.resolve()).then(() => {
    document.querySelectorAll('main h2:not(.compare-card h2)').forEach(h => {
      if (h.children.length) return;
      splitLines(h);
      io.observe(h);
    });
  });

  // Large photographs drift slightly inside their frames while scrolling.
  const drift = [...document.querySelectorAll('[data-parallax]')];
  if (drift.length) {
    let ticking = false;
    const update = () => {
      ticking = false;
      drift.forEach(img => {
        const r = img.parentElement.getBoundingClientRect();
        if (r.bottom < -100 || r.top > innerHeight + 100) return;
        const t = (r.top + r.height / 2 - innerHeight / 2) / (innerHeight / 2 + r.height / 2);
        img.style.transform = `translate3d(0, ${(t * -6).toFixed(2)}%, 0) scale(1.12)`;
      });
    };
    addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    addEventListener('resize', update);
    update();
  }
}

document.querySelectorAll('.compare input').forEach(input => {
  const box = input.closest('.compare');
  input.addEventListener('input', () => box.style.setProperty('--pos', input.value + '%'));
});

const nav = document.querySelector('.nav');
const menuBtn = document.querySelector('.menu-btn');
if (nav && menuBtn) {
  const setMenu = open => {
    nav.classList.toggle('open', open);
    menuBtn.setAttribute('aria-expanded', open);
    menuBtn.textContent = open ? 'Close' : 'Menu';
    document.documentElement.style.overflow = open ? 'hidden' : '';
  };
  menuBtn.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); menuBtn.focus(); } });
}

const zooms = document.querySelectorAll('a.zoom');
if (zooms.length) {
  const dlg = document.createElement('dialog');
  dlg.className = 'lightbox';
  dlg.innerHTML = '<button type="button">Close</button><img alt=""><p></p>';
  document.body.append(dlg);
  const img = dlg.querySelector('img'), cap = dlg.querySelector('p');
  dlg.querySelector('button').addEventListener('click', () => dlg.close());
  dlg.addEventListener('click', e => { if (e.target === dlg) dlg.close(); });
  zooms.forEach(a => a.addEventListener('click', e => {
    e.preventDefault();
    const inner = a.querySelector('img');
    img.src = a.getAttribute('href');
    img.alt = inner ? inner.alt : '';
    const fc = a.closest('figure')?.querySelector('figcaption');
    cap.textContent = fc ? fc.textContent.trim() : '';
    cap.hidden = !fc;
    dlg.showModal();
  }));
}

const form = document.querySelector('#inquiry');
if (form) {
  const pkg = new URLSearchParams(location.search).get('package');
  if (pkg && form.package.querySelector(`option[value="${CSS.escape(pkg)}"]`)) form.package.value = pkg;
  const status = form.querySelector('.status');
  const preview = form.querySelector('.preview');
  form.addEventListener('submit', async e => {
    e.preventDefault();
    let ok = true;
    form.querySelectorAll('[required]').forEach(f => {
      const err = document.getElementById(f.getAttribute('aria-describedby').split(' ')[0]);
      const bad = !f.value.trim();
      f.setAttribute('aria-invalid', bad);
      if (err) err.textContent = bad ? f.dataset.error : '';
      if (bad && ok) { f.focus(); ok = false; }
    });
    if (!ok) { status.textContent = ''; return; }
    const lines = [...form.querySelectorAll('input, select, textarea')].filter(f => f.id !== 'details').map(f => {
      const label = form.querySelector(`label[for="${f.id}"]`).textContent.trim();
      const value = f.tagName === 'SELECT' ? (f.value || f.selectedOptions[0].text !== 'Choose one' ? f.selectedOptions[0].text : 'Not given') : (f.value.trim() || 'Not given');
      return `${label}: ${value}`;
    });
    const body = [...lines, '', form.details.value.trim()].join('\n');
    preview.textContent = body;
    preview.classList.add('show');
    if (typeof gtag === 'function') gtag('event', 'generate_lead', { form: 'inquiry' });
    try {
      await navigator.clipboard.writeText(body);
      status.textContent = 'Inquiry copied. Paste it into an email or message to us.';
    } catch {
      status.textContent = 'Your inquiry is below. Select the text and copy it.';
    }
  });
}
