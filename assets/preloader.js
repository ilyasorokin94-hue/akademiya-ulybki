/* Стартовая заставка «Академии улыбки»: логотип собирается из сегментов.
   «А» режется на диагональные полосы, полосы слетаются, росчерк прочерчивается,
   шапочка опускается сверху, затем подпись и раскрытие по линии росчерка. */
(function () {
  var d = document.documentElement, pl = document.getElementById('pl');
  var heroStart = null, released = false;
  // app.js вызывает старт анимации героя через этот хук, когда заставка уходит
  window.__auStart = function (fn) { if (released || !pl) fn(); else heroStart = fn; };
  function release() {
    if (released) return; released = true;
    d.classList.remove('au-loading');
    if (heroStart) heroStart();
  }
  if (!pl) { release(); return; }
  // заставка один раз за визит: при повторном открытии в той же вкладке сразу страница
  if (d.classList.contains('au-nopl')) { release(); pl.remove(); return; }
  try { sessionStorage.setItem('au-pl', '1'); } catch (e) {}
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !window.gsap) { release(); pl.remove(); return; }

  var NS = 'http://www.w3.org/2000/svg', svg = pl.querySelector('.pl__logo');
  var a = svg.querySelector('.pl-a'), thin = svg.querySelector('.pl-thin'), sw = svg.querySelector('.pl-sw'), cap = svg.querySelector('.pl-cap');
  var letters = svg.querySelectorAll('.pl-l'), defs = svg.querySelector('defs'), shards = svg.querySelector('.pl__shards');

  // Полосы идут параллельно росчерку (наклон около -0.62), как срезы одного камня
  var K = -0.62, N = 8, x0 = 230, x1 = 690, cTop = 455, cBot = 1030, step = (cBot - cTop) / N;
  var parts = [];
  for (var i = 0; i < N; i++) {
    var c0 = cTop + step * i - 0.6, c1 = cTop + step * (i + 1) + 0.6;
    var cp = document.createElementNS(NS, 'clipPath'); cp.id = 'pl-band-' + i;
    var poly = document.createElementNS(NS, 'polygon');
    poly.setAttribute('points', [x0, K * x0 + c0, x1, K * x1 + c0, x1, K * x1 + c1, x0, K * x0 + c1].join(' '));
    cp.appendChild(poly); defs.appendChild(cp);
    var g = document.createElementNS(NS, 'g'); g.setAttribute('clip-path', 'url(#pl-band-' + i + ')');
    [a, sw].forEach(function (src) { var p = src.cloneNode(); p.removeAttribute('class'); g.appendChild(p); });
    shards.appendChild(g); parts.push(g);
  }
  shards.removeAttribute('clip-path');

  // Золотой блик проходит по собранному знаку
  var glCp = document.createElementNS(NS, 'clipPath'); glCp.id = 'pl-glint-clip';
  var glRect = document.createElementNS(NS, 'rect');
  glRect.setAttribute('x', -60); glRect.setAttribute('y', 0); glRect.setAttribute('width', 70); glRect.setAttribute('height', 900);
  glRect.setAttribute('transform', 'translate(200 -40) rotate(28)');
  glCp.appendChild(glRect); defs.appendChild(glCp);
  var glint = document.createElementNS(NS, 'g'); glint.setAttribute('class', 'pl-glint'); glint.setAttribute('clip-path', 'url(#pl-glint-clip)'); glint.setAttribute('fill', 'url(#pl-gold)');
  [a, thin, sw].forEach(function (src) { var p = src.cloneNode(); p.removeAttribute('class'); p.style.opacity = 1; glint.appendChild(p); });
  svg.querySelector('.pl__mark').appendChild(glint);

  var num = pl.querySelector('[data-pl-num]'), counter = { v: 0 };
  var g = gsap, tl = g.timeline({ defaults: { ease: 'power3.out' } });
  g.set(a, { autoAlpha: 0 });
  g.set([thin, cap, sw], { autoAlpha: 0 });
  g.set('.pl__count', { autoAlpha: 1 });
  window.__plTl = tl;
  var dbg = /plpause/.test(location.search); if (dbg) tl.pause();

  tl.to(counter, { v: 100, duration: 3.1, ease: 'power1.inOut', onUpdate: function () { num.textContent = Math.round(counter.v); } }, 0)
    .from(parts, {
      x: function (k) { return (k % 2 ? 1 : -1) * (120 + k * 18); },
      y: function (k) { return (k - N / 2) * 46; },
      rotation: function (k) { return (k % 2 ? 1 : -1) * (14 + k * 2); },
      transformOrigin: '50% 50%', autoAlpha: 0, duration: 1.15, stagger: { each: 0.07, from: 'edges' }, ease: 'expo.out'
    }, 0.15)
    .to([a, sw], { autoAlpha: 1, duration: 0.2 }, 1.5)
    .set(shards, { autoAlpha: 0 }, 1.7)
    .fromTo(thin, { autoAlpha: 0, x: -40, y: 64 }, { autoAlpha: 1, x: 0, y: 0, duration: 0.6 }, 1.0)
    .fromTo(glRect, { attr: { x: -420 } }, { attr: { x: 560 }, duration: 1.1, ease: 'power2.inOut' }, 1.5)
    .fromTo(cap, { autoAlpha: 0, y: -170, rotation: -18, transformOrigin: '60% 50%' }, { autoAlpha: 1, y: 0, rotation: 0, duration: 0.9, ease: 'back.out(1.6)' }, 1.75)
    .fromTo(letters, { autoAlpha: 0, y: 26 }, { autoAlpha: 1, y: 0, duration: 0.6, stagger: 0.035 }, 2.15)
    .to('.pl__count', { autoAlpha: 0, duration: 0.3 }, 3.2)
    .fromTo('.pl__seam', { clipPath: 'inset(0% 100% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 0.45, ease: 'power2.inOut' }, 3.1)
    .to(svg, { scale: 0.86, autoAlpha: 0, duration: 0.6, ease: 'power2.in' }, 3.35)
    .add(release, 3.55)
    .to('.pl__half--a', { yPercent: -100, duration: 1.0, ease: 'expo.inOut' }, 3.55)
    .to('.pl__half--b', { yPercent: 100, duration: 1.0, ease: 'expo.inOut' }, 3.55)
    .to('.pl__seam', { autoAlpha: 0, duration: 0.3 }, 3.6)
    .add(function () { pl.remove(); });

  // если вкладка открыта в фоне, не держим страницу
  if (!dbg) setTimeout(function () { release(); if (pl.isConnected) pl.remove(); }, 5000);
})();
