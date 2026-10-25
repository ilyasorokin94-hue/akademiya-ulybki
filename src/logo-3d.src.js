// Объёмная «А» из логотипа «Академии улыбки» на первом экране: чёрный глянцевый акрил,
// как знак на стене клиники. Медленно вращается и чуть следует за курсором.
import * as THREE from 'three';
import { SVGLoader } from 'three/examples/jsm/loaders/SVGLoader.js';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';

(function () {
  var box = document.querySelector('.hx--a'), data = document.getElementById('logo-a');
  if (!box || !data) return;
  try {
    var c = document.createElement('canvas');
    if (!(c.getContext('webgl2') || c.getContext('webgl'))) return;
  } catch (e) { return; }
  var parts = JSON.parse(data.textContent);
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  box.appendChild(renderer.domElement);

  var scene = new THREE.Scene();
  var pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  var camera = new THREE.PerspectiveCamera(30, 1, 1, 5000);
  camera.position.set(0, 0, 1500);

  var key = new THREE.DirectionalLight(0xffffff, 2.2); key.position.set(500, 700, 900); scene.add(key);
  var rim = new THREE.DirectionalLight(0x9db7e0, 2.6); rim.position.set(-800, 200, -600); scene.add(rim);
  scene.add(new THREE.AmbientLight(0xffffff, 0.25));

  // Чёрный акрил: почти чёрная база с лаковым слоем, грани ловят синеватый контровой свет
  var mat = new THREE.MeshPhysicalMaterial({ color: 0x0c0d10, metalness: 0.15, roughness: 0.28, clearcoat: 1, clearcoatRoughness: 0.06, envMapIntensity: 1.25 });
  var svg = '<svg xmlns="http://www.w3.org/2000/svg">' + ['cap', 'a', 'thin', 'sw'].map(function (k) { return '<path d="' + parts[k] + '"/>'; }).join('') + '</svg>';
  var paths = new SVGLoader().parse(svg).paths;
  var group = new THREE.Group(), inner = new THREE.Group();
  paths.forEach(function (p) {
    SVGLoader.createShapes(p).forEach(function (sh) {
      var g = new THREE.ExtrudeGeometry(sh, { depth: 46, bevelEnabled: true, bevelThickness: 5, bevelSize: 3, bevelSegments: 4, curveSegments: 18 });
      inner.add(new THREE.Mesh(g, mat));
    });
  });
  inner.scale.set(1, -1, 1);
  var bb = new THREE.Box3().setFromObject(inner), ctr = bb.getCenter(new THREE.Vector3()), size = bb.getSize(new THREE.Vector3());
  inner.position.set(-ctr.x, -ctr.y, -ctr.z);
  group.add(inner); scene.add(group);

  // мягкая синяя тень-пятно под знаком
  var sh = new THREE.Mesh(new THREE.CircleGeometry(size.x * 0.42, 48), new THREE.MeshBasicMaterial({ color: 0x2b4c7e, transparent: true, opacity: 0.10 }));
  sh.rotation.x = -Math.PI / 2; sh.position.y = -size.y * 0.62; sh.scale.set(1, 0.32, 1); scene.add(sh);

  function fit() {
    var w = box.clientWidth, h = box.clientHeight; if (!w || !h) return;
    renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix();
    var dist = camera.position.z, vh = 2 * dist * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
    var k = Math.min((vh * 0.74) / size.y, (vh * camera.aspect * 0.78) / size.x);
    group.scale.setScalar(k); sh.scale.set(k, 0.32 * k, k);
  }
  fit(); addEventListener('resize', fit);

  var mx = 0, my = 0, tx = 0, ty = 0;
  addEventListener('pointermove', function (e) { mx = (e.clientX / innerWidth) * 2 - 1; my = (e.clientY / innerHeight) * 2 - 1; }, { passive: true });
  var visible = true;
  new IntersectionObserver(function (en) { visible = en[0].isIntersecting; }).observe(box);
  var clock = new THREE.Clock(), angle = -0.6, intro = 0;
  function tick() {
    requestAnimationFrame(tick);
    if (!visible) return;
    var dt = Math.min(clock.getDelta(), 0.05);
    intro = Math.min(1, intro + dt * 0.6);
    angle += dt * (reduce ? 0 : 0.42);
    tx += (mx - tx) * 0.05; ty += (my - ty) * 0.05;
    var e = 1 - Math.pow(1 - intro, 3);
    group.rotation.y = angle + tx * 0.35;
    group.rotation.x = 0.08 + ty * 0.12 + (1 - e) * 0.5;
    group.position.y = Math.sin(clock.elapsedTime * 0.9) * size.y * group.scale.y * 0.015;
    renderer.render(scene, camera);
  }
  tick();
  box.classList.add('is-ready');
})();
