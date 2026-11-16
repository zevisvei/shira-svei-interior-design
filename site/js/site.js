document.querySelectorAll('.compare input').forEach(input => {
  const box = input.closest('.compare');
  input.addEventListener('input', () => box.style.setProperty('--pos', input.value + '%'));
});

const nav = document.querySelector('.nav');
const menuBtn = document.querySelector('.menu-btn');
if (nav && menuBtn) {
  menuBtn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', open);
    menuBtn.textContent = open ? 'Close' : 'Menu';
  });
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
      const err = document.getElementById(f.getAttribute('aria-describedby'));
      const bad = !f.value.trim();
      f.setAttribute('aria-invalid', bad);
      if (err) err.textContent = bad ? f.dataset.error : '';
      if (bad && ok) { f.focus(); ok = false; }
    });
    if (!ok) { status.textContent = ''; return; }
    const text = (field) => { const el = form[field]; return el.tagName === 'SELECT' ? (el.value ? el.selectedOptions[0].text : 'Not sure yet') : el.value.trim(); };
    const body = [
      `Name: ${text('name')}`,
      `Plans for the apartment: ${text('plans')}`,
      `Stage: ${text('stage')}`,
      `Package: ${text('package')}`,
      '',
      text('details')
    ].join('\n');
    preview.textContent = body;
    preview.classList.add('show');
    try {
      await navigator.clipboard.writeText(body);
      status.textContent = 'Inquiry copied. Paste it into an email or message to us.';
    } catch {
      status.textContent = 'Your inquiry is below. Select the text and copy it.';
    }
  });
}
