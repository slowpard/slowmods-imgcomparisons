// Comparison page: OpenSeadragon (zoom, pan, touch) with the curtain-sync plugin (the slider).
// This file only wires the page around them: scene tabs, picking the two images, number keys to show one image,
// labels, the divider line, full screen and the address (#<scene>/<left>-<right>, numbers in the scene's image order).
(() => {
  const C = JSON.parse(document.getElementById('data').textContent);
  const root = document.body.dataset.root;
  const $ = id => document.getElementById(id);
  const box = $('viewer'), wrap = $('wrap'), line = $('line'), labA = $('labA'), labB = $('labB');
  const selA = $('left'), selB = $('right');
  const key = i => 'img' + i;

  let view = Math.max(C.views.findIndex(v => v.slug === C.main_view), 0);
  let a, b;
  let solo = null;              // image shown on its own (number keys), or null for the pair
  let viewer = null;
  const ims = () => C.views[view].images;

  function readHash() {
    const [s, p] = decodeURIComponent(location.hash.slice(1)).split('/');
    const vi = C.views.findIndex(v => v.slug === s);
    if (vi >= 0) view = vi;
    [a, b] = C.views[view].pair.map(x => x - 1);
    const m = /^(\d+)-(\d+)$/.exec(p || '');
    if (m) { a = +m[1] - 1; b = +m[2] - 1; }
  }

  // The plugin draws the shown images in list order and clips the second one from the divider to the right,
  // so the list starts with the left image, then the right one; the others are there for the number keys.
  function build(keepZoom) {
    const zoom = keepZoom && viewer ? viewer.getZoom() : null, pan = keepZoom && viewer ? viewer.getPan() : null;
    const split = viewer ? viewer.mode.clipFactorX : 0.5;   // keep the divider where it was; start in the middle
    if (viewer) viewer.mode.destroy();
    box.innerHTML = '';
    const list = ims(), order = [a, b, ...list.map((_, i) => i).filter(i => i !== a && i !== b)];
    viewer = new CurtainSyncViewer({
      container: box,
      mode: 'curtain',
      images: order.map(i => ({ key: key(i), tileSource: { type: 'image', url: root + list[i].src }, shown: i === a || i === b })),
      osdOptions: {
        drawer: 'canvas',         // the plugin's clipping needs it
        maxZoomPixelRatio: 4,
        minZoomImageRatio: 1,
        visibilityRatio: 1,
        gestureSettingsMouse: { clickToZoom: false },
      },
    });
    viewer.mode.clipFactorX = split;
    if (zoom) { viewer.setZoom(zoom); viewer.setPan(pan); }
    viewer.mode.viewer.addHandler('viewport-change', drawLine);
    show();
  }

  function show() {
    const list = ims();
    list.forEach((_, i) => viewer.setImageShown(key(i), solo === null ? (i === a || i === b) : i === solo));
    labA.textContent = solo === null ? list[a].label : `${solo + 1}. ${list[solo].label}`;
    labB.textContent = list[b].label;
    labB.hidden = solo !== null;
    drawLine();
  }

  function drawLine() {
    line.hidden = solo !== null;
    line.style.left = (viewer.mode.clipFactorX * 100) + '%';
  }
  box.addEventListener('pointermove', () => requestAnimationFrame(drawLine));

  // newScene: rebuild the tabs and lists and start unzoomed; otherwise only the pair changed
  function refresh(newScene) {
    const n = ims().length;
    a = Math.min(Math.max(a, 0), n - 1); b = Math.min(Math.max(b, 0), n - 1);
    if (a === b) b = a === 0 ? 1 : 0;
    solo = null;
    if (newScene) {
      $('views').innerHTML = '';
      C.views.forEach((v, i) => {
        const btn = document.createElement('button');
        btn.textContent = v.name; btn.className = i === view ? 'on' : '';
        btn.onclick = () => { if (i !== view) { view = i; [a, b] = v.pair.map(x => x - 1); refresh(true); } };
        $('views').appendChild(btn);
      });
      for (const sel of [selA, selB]) {
        sel.innerHTML = '';
        ims().forEach((im, i) => sel.add(new Option(`${i + 1}. ${im.label}`, i)));
      }
    }
    selA.value = a; selB.value = b;
    build(!newScene);
    history.replaceState(null, '', '#' + C.views[view].slug + '/' + (a + 1) + '-' + (b + 1));
  }

  selA.onchange = () => { a = +selA.value; refresh(false); };
  selB.onchange = () => { b = +selB.value; refresh(false); };

  // full screen; where the browser refuses (iPhone, embedded browsers) the viewer fills the window instead
  $('full').onclick = () => {
    const fill = () => wrap.classList.add('fullpage');
    if (wrap.requestFullscreen) wrap.requestFullscreen().catch(fill); else fill();
  };
  const exitFull = () => {
    if (document.fullscreenElement) document.exitFullscreen();
    wrap.classList.remove('fullpage');
  };
  $('exitfull').onclick = exitFull;

  document.addEventListener('keydown', e => {
    if (e.target.tagName === 'SELECT' || e.ctrlKey || e.metaKey || e.altKey) return;
    const n = parseInt(e.key, 10);
    if (n >= 1 && n <= ims().length) { solo = n - 1; show(); }
    else if (e.key === '0') { solo = null; show(); }
    else if (e.key === 'Escape') { if (wrap.classList.contains('fullpage')) exitFull(); else { solo = null; show(); } }
  });
  window.addEventListener('hashchange', () => { readHash(); refresh(true); });

  readHash(); refresh(true);
})();
