import * as THREE from '../vendor/three.module.min.js';

const section = document.querySelector('.hero3d');
const canvas = section?.querySelector('canvas');
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
if (window.gsap && window.ScrollTrigger) gsap.registerPlugin(ScrollTrigger);

function webglOK() {
  try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch { return false; }
}

if (section && canvas && !reduce && webglOK() && window.gsap && window.ScrollTrigger) start();

async function loadImage(src) {
  const img = new Image();
  img.src = src;
  await img.decode();
  return img;
}

// Wall runs: horizontal stretches of 4px cells that are almost fully dark in the plan drawing.
function wallRuns(img, cell = 4) {
  const w = img.naturalWidth, h = img.naturalHeight;
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  const x = c.getContext('2d', { willReadFrequently: true }); x.drawImage(img, 0, 0);
  const px = x.getImageData(0, 0, w, h).data;
  const cols = Math.floor(w / cell), rows = Math.floor(h / cell);
  const runs = [];
  for (let r = 0; r < rows; r++) {
    let startCol = -1;
    for (let col = 0; col <= cols; col++) {
      let wall = false;
      if (col < cols) {
        let dark = 0;
        for (let yy = 0; yy < cell; yy++) for (let xx = 0; xx < cell; xx++) {
          const i = ((r * cell + yy) * w + col * cell + xx) * 4;
          if (px[i] * .3 + px[i + 1] * .59 + px[i + 2] * .11 < 80) dark++;
        }
        wall = dark >= cell * cell * .85;
      }
      if (wall && startCol < 0) startCol = col;
      if (!wall && startCol >= 0) { runs.push([startCol, col - startCol, r]); startCol = -1; }
    }
  }
  // Merge identical runs in consecutive rows into one box, so a wall is one solid piece.
  const open = new Map(), boxes = [];
  for (const [c0, len, r] of runs) {
    const key = c0 + ':' + len, b = open.get(key);
    if (b && b.r1 === r - 1) b.r1 = r;
    else { const nb = { c0, len, r0: r, r1: r }; open.set(key, nb); boxes.push(nb); }
  }
  return { boxes, cols, rows };
}

const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const clamp01 = v => Math.min(1, Math.max(0, v));
const span = (p, a, b) => clamp01((p - a) / (b - a));

async function start() {
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
  } catch { return; }

  const plan = await loadImage(canvas.dataset.plan);
  const { boxes, cols, rows } = wallRuns(plan);

  section.classList.add('is-3d');
  ScrollTrigger.refresh();

  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.shadowMap.autoUpdate = false;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x38321f);

  const PW = 10, PH = PW * plan.naturalHeight / plan.naturalWidth;
  const cellW = PW / cols, cellH = PH / rows, WALL = 1.75;

  const tex = new THREE.Texture(plan);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
  tex.needsUpdate = true;

  const paper = new THREE.Mesh(new THREE.PlaneGeometry(PW + .6, PH + .6), new THREE.MeshStandardMaterial({ color: 0xe8e5da, roughness: 1 }));
  paper.rotation.x = -Math.PI / 2; paper.position.y = -.002; paper.receiveShadow = true;
  const sheet = new THREE.Mesh(new THREE.PlaneGeometry(PW, PH), new THREE.MeshStandardMaterial({ map: tex, roughness: .95 }));
  sheet.rotation.x = -Math.PI / 2; sheet.receiveShadow = true;
  scene.add(paper, sheet);

  const side = new THREE.MeshStandardMaterial({ color: 0xebe6da, roughness: .8 });
  const top = new THREE.MeshStandardMaterial({ color: 0x29261a, roughness: .9 });
  const walls = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), [side, side, top, side, side, side], boxes.length);
  walls.castShadow = true; walls.receiveShadow = true;
  scene.add(walls);

  const base = boxes.map(({ c0, len, r0, r1 }) => {
    const x = (c0 + len / 2) * cellW - PW / 2, z = ((r0 + r1 + 1) / 2) * cellH - PH / 2;
    return { x, z, w: len * cellW + .002, d: (r1 - r0 + 1) * cellH + .002, delay: Math.hypot(x, z) / Math.hypot(PW / 2, PH / 2) };
  });
  const m = new THREE.Matrix4(), pos = new THREE.Vector3(), quat = new THREE.Quaternion(), scl = new THREE.Vector3();
  let lastK = -1;
  function setWalls(k) {
    if (Math.abs(k - lastK) < 1e-4) return;
    lastK = k;
    renderer.shadowMap.needsUpdate = true;
    base.forEach((b, i) => {
      const h = Math.max(.0005, WALL * ease(clamp01((k - b.delay * .45) / .55)));
      pos.set(b.x, h / 2, b.z); scl.set(b.w, h, b.d);
      walls.setMatrixAt(i, m.compose(pos, quat, scl));
    });
    walls.instanceMatrix.needsUpdate = true;
  }

  scene.add(new THREE.HemisphereLight(0xffffff, 0x5a5236, 1.25));
  const sun = new THREE.DirectionalLight(0xfff3e2, 1.9);
  sun.position.set(-7, 12, 5);
  sun.castShadow = true;
  sun.shadow.mapSize.set(1536, 1536);
  Object.assign(sun.shadow.camera, { left: -8, right: 8, top: 8, bottom: -8, near: 1, far: 40 });
  sun.shadow.bias = -.0004;
  sun.shadow.radius = 4;
  scene.add(sun);

  const camera = new THREE.PerspectiveCamera(30, 1, .1, 200);
  const target = new THREE.Vector3(0, 0, 0);
  const sph = new THREE.Spherical();
  let W = 1, H = 1, fitR = 20;

  function resize() {
    W = canvas.clientWidth; H = canvas.clientHeight;
    renderer.setSize(W, H, false);
    camera.aspect = W / H;
    const wide = camera.aspect > 1;
    const frac = wide ? .42 : .84;
    const visW = 2 * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)) * camera.aspect;
    fitR = Math.max(PW / (frac * visW), (PH + 1) / (2 * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)) * (wide ? .7 : .42)));
    if (wide) camera.setViewOffset(W, H, -W * .25, -H * .02, W, H);
    else camera.setViewOffset(W, H, 0, -H * .3, W, H);
    camera.updateProjectionMatrix();
    draw();
  }

  const state = { p: 0, goal: 0, px: 0, py: 0, tx: 0, ty: 0 };
  const steps = section.querySelectorAll('.hero3d-steps li');
  const photo = section.querySelector('.hero3d-photo');
  const smooth = t => t * t * (3 - 2 * t);

  function draw() {
    const p = state.p;
    setWalls(span(p, .06, .6));
    const c = ease(span(p, .04, .66));
    const dive = smooth(span(p, .7, 1));
    sph.set(
      fitR * (1 - .2 * c - .38 * dive),
      THREE.MathUtils.degToRad(.5 + 52 * c + 16 * dive + state.py * 3 * c),
      THREE.MathUtils.degToRad(-38 * c - 14 * dive + state.px * 6 * c)
    );
    camera.position.setFromSpherical(sph).add(target);
    camera.lookAt(target);
    renderer.render(scene, camera);
    const show = smooth(span(p, .74, .96));
    photo.style.opacity = show.toFixed(3);
    photo.style.transform = `scale(${(1.12 - .12 * show).toFixed(4)})`;
    const active = p < .3 ? 0 : p < .74 ? 1 : 2;
    steps.forEach((li, i) => li.classList.toggle('on', i === active));
  }

  let raf = 0;
  function tick() {
    state.p += (state.goal - state.p) * .14;
    state.px += (state.tx - state.px) * .08;
    state.py += (state.ty - state.py) * .08;
    if (Math.abs(state.goal - state.p) < .0002) state.p = state.goal;
    draw();
    const moving = state.p !== state.goal || Math.abs(state.tx - state.px) + Math.abs(state.ty - state.py) > .001;
    raf = moving ? requestAnimationFrame(tick) : 0;
  }
  const kick = () => { if (!raf) raf = requestAnimationFrame(tick); };

  if (matchMedia('(pointer: fine)').matches) {
    section.addEventListener('pointermove', e => {
      state.tx = e.clientX / innerWidth * 2 - 1;
      state.ty = e.clientY / innerHeight * 2 - 1;
      kick();
    }, { passive: true });
  }

  ScrollTrigger.create({
    trigger: section, start: 'top top', end: 'bottom bottom',
    onUpdate: self => { state.goal = self.progress; kick(); }
  });

  canvas.addEventListener('webglcontextlost', e => { e.preventDefault(); section.classList.remove('is-3d'); ScrollTrigger.refresh(); });
  new ResizeObserver(resize).observe(canvas);
  resize();
}
