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
    window.lenis?.[open ? 'stop' : 'start']();
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
  dlg.addEventListener('close', () => window.lenis?.start());
  zooms.forEach(a => a.addEventListener('click', e => {
    e.preventDefault();
    const inner = a.querySelector('img');
    img.src = a.getAttribute('href');
    img.alt = inner ? inner.alt : '';
    const fc = a.closest('figure')?.querySelector('figcaption');
    cap.textContent = fc ? fc.textContent.trim() : '';
    cap.hidden = !fc;
    dlg.showModal();
    window.lenis?.stop();
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
