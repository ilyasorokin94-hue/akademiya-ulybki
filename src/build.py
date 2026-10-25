# Собирает index.html «Академии улыбки» из вёрстки vaitis-preview (эталон Lava Dental):
# та же структура и классы, новый контент, палитра и прелоадер.
import re, json, html, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(ROOT, 'src/vaitis-index.html'), encoding='utf-8').read()

PHONE = '+7 920 955-03-50'
TEL = '+79209550350'
ADDR = 'ул. Попова, 4а'
HOURS = 'Ежедневно с 9:00 до 21:00'
YA = 'https://yandex.ru/maps/org/akademiya_ulybki/8207640702/'
GIS = 'https://2gis.ru/ryazan/firm/70000001099908866'
ROUTE = 'https://yandex.ru/maps/?rtext=~54.624018,39.772021'
TG = 'https://t.me/academy_smile62'
WA = 'https://wa.me/79209550350'
VK = 'https://vk.com/smile_academy_rzn'
MAX = 'https://max.ru/u/f9LHodD0cOJ-0xkX-e2JlawQE-uWEU88N5JX8HnRrMTPe0pvKjp-WaLVzNk'
MAIL = 'academy_smile@mail.ru'
ARROW = '<svg viewBox="0 0 60 60"><path d="M24 36 36 24M27 24h9v9"/></svg>'


def block(start, end_tag, new, src=None):
    """Заменяет фрагмент от start до ближайшего end_tag включительно."""
    global s
    i = s.index(start)
    j = s.index(end_tag, i) + len(end_tag)
    s = s[:i] + new + s[j:]


# Кадры, которые нужно согласовать с клиникой: на сайте у них плашка «уточнить»
ASK = {
    'images/doctors/lazarev.webp': 'Фото из прошлой клиники, уточнить',
    'images/real/old-mikroskop.webp': 'Прошлая клиника, уточнить',
    'images/real/old-modeli.webp': 'Прошлая клиника, уточнить',
    'images/real/old-implant.webp': 'Прошлая клиника, уточнить',
    'images/real/old-vrach.webp': 'Прошлая клиника, уточнить',
}


def img(path, alt='', cls='', style='', extra=''):
    if not path:
        return ''
    a = f'<img src="{path}" alt="{html.escape(alt)}" loading="lazy" decoding="async" onerror="umImg(this)"'
    if cls: a += f' class="{cls}"'
    if style: a += f' style="{style}"'
    if extra: a += ' ' + extra
    a += '>'
    if path in ASK:
        a += f'<span class="au-ask" title="{ASK[path]}">уточнить</span>'
    return a


# ---------- HEAD ----------
TITLE = 'Стоматология «Академия улыбки» в Рязани: лечение под микроскопом, импланты, дети'
DESC = '5,0 на Яндекс Картах. Лечение зубов под микроскопом, имплантация и All-on-4, коронки из циркония, детская стоматология. Рязань, ул. Попова, 4а, ежедневно с 9:00 до 21:00. Консультация и снимок бесплатно.'
head_end = s.index('</head>')
head = s[:head_end]
head = re.sub(r'<title>.*?</title>', f'<title>{TITLE}</title>', head)
head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', head)
head = re.sub(r'<link rel="canonical"[^>]*>\n', '', head)
head = re.sub(r'<meta property="og:[^>]*>\n', '', head)
head = head.replace('<meta name="theme-color" content="#ffffff">',
                    f'<meta property="og:type" content="website">\n<meta property="og:title" content="{TITLE}">\n<meta property="og:description" content="{DESC}">\n<meta property="og:locale" content="ru_RU">\n<meta name="theme-color" content="#15171c">')
head = re.sub(r'<link rel="apple-touch-icon"[^>]*>\n', '', head)
head = head.replace('<link rel="stylesheet" href="assets/styles.css?v=d847b31c">',
                    '<link rel="stylesheet" href="assets/styles.css?v=au2">\n<link rel="stylesheet" href="assets/akademiya.css?v=au3">')
# свой прелоадер вместо интро Вайтис: js-intro не ставим, держим страницу под заставкой
head = head.replace('if(d.dataset.page==="home"&&!sessionStorage.getItem("um2-intro"))d.classList.add("js-intro")',
                    'd.classList.add("au-loading")')
head = re.sub(r'<script type="application/ld\+json">.*?</script>\n', '', head, flags=re.S)
LD = {"@context": "https://schema.org", "@type": "Dentist", "name": "Стоматология «Академия улыбки»",
      "telephone": PHONE, "email": MAIL,
      "address": {"@type": "PostalAddress", "streetAddress": "ул. Попова, 4а", "addressLocality": "Рязань", "postalCode": "390006", "addressCountry": "RU"},
      "geo": {"@type": "GeoCoordinates", "latitude": 54.624018, "longitude": 39.772021},
      "openingHours": "Mo-Su 09:00-21:00", "sameAs": [YA, GIS, VK, TG]}
head = head.replace('</script>\n<script src="assets/vendor/gsap.min.js"',
                    '</script>\n<script src="assets/vendor/gsap.min.js"', 1)
head += '<script type="application/ld+json">' + json.dumps(LD, ensure_ascii=False) + '</script>\n'
head = head.replace('<script src="assets/cookie.js?v=886e3f70" data-privacy="privacy/" data-ym="" defer></script>',
                    '<script src="assets/cookie.js?v=886e3f70" data-privacy="#" data-ym="" defer></script>')
head = re.sub(r'<script src="assets/hero-3d.js[^"]*" defer></script>\n', '<script src="assets/logo-3d.js?v=au1" defer></script>\n', head)
head = head.replace('<script src="assets/app.js?v=9b97a404" defer></script>', '<script src="assets/preloader.js?v=au1" defer></script>\n<script src="assets/app.js?v=au1" defer></script>')
s = head + s[head_end:]

# ---------- демо-плашка, прелоадер ----------
logo = json.load(open(os.path.join(ROOT, 'logo_parts.json')))
segs = ''
# «А» и росчерк режем на сегменты clip-path'ами в CSS; здесь отдаём части как отдельные пути
segs += f'<path class="pl-seg pl-a" d="{logo["a"]}"/>'
segs += f'<path class="pl-seg pl-thin" d="{logo["thin"]}"/>'
segs += f'<path class="pl-seg pl-sw" d="{logo["sw"]}"/>'
segs += f'<path class="pl-seg pl-cap" d="{logo["cap"]}"/>'
letters = ''.join(f'<path class="pl-l" style="--i:{i}" fill-rule="evenodd" d="{d}"/>' for i, d in enumerate(logo['letters']))
PRELOADER = f'''<div class="pl" id="pl" aria-hidden="true">
  <div class="pl__half pl__half--a"></div><div class="pl__half pl__half--b"></div><svg class="pl__seam" viewBox="0 0 100 100" preserveAspectRatio="none"><line x1="-2" y1="77.05" x2="102" y2="35.45" pathLength="1"/></svg>
  <svg class="pl__logo" viewBox="190 30 540 670">
    <defs>
      <clipPath id="pl-clip-a"><path d="{logo["a"]}"/></clipPath>
      <linearGradient id="pl-gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#dbe7f7"/><stop offset=".5" stop-color="#7d9cc9"/><stop offset="1" stop-color="#1d3557"/></linearGradient>
    </defs>
    <g class="pl__shards" clip-path="url(#pl-clip-a)"></g>
    <g class="pl__mark">{segs}</g>
    <g class="pl__word">{letters}</g>
  </svg>
  <div class="pl__count"><span data-pl-num>0</span>%</div>
</div>'''
s = s.replace('<div class="demo-bar">Демонстрационный макет нового сайта стоматологии «Вайтис». Заявки из форм пока никуда не отправляются.</div>',
              '<div class="demo-bar">Демонстрационный макет нового сайта стоматологии «Академия улыбки». Заявки из форм пока никуда не отправляются.</div>')
s = s.replace('<div class="intro" aria-hidden="true"><div class="intro__bg"></div><img class="intro__mark" src="images/brand/header-logo-light.svg" alt=""></div>', PRELOADER)

# ---------- шапка и меню ----------
s = s.replace('aria-label="Вайтис. Стоматология в Одинцово, на главную"', 'aria-label="Академия улыбки. Стоматология в Рязани, на главную"')
s = s.replace('<span class="logo__text">Вайтис<small>стоматология в Одинцово</small></span>', '<span class="logo__text">Академия улыбки<small>стоматология в Рязани</small></span>')
s = s.replace('<span class="logo__unit">Стоматология</span>', '<span class="logo__unit">Стоматология · Рязань</span>')
s = s.replace('tel:+79037977688', 'tel:' + TEL).replace('+7 903 797-76-88', PHONE)
s = s.replace('<a class="nav__link" href="ceny/">Цены</a>', '<a class="nav__link" href="#prices">Цены</a>')
s = s.replace('<a class="mnav__link" href="ceny/">Цены</a>', '<a class="mnav__link" href="#prices">Цены</a>')
s = re.sub(r'<details class="menu__svc">.*?</details>',
           '<a href="#services">Услуги</a>', s, flags=re.S)
s = s.replace('<a href="ceny/">Цены</a><a href="#akcii">Акции</a>', '<a href="#prices">Цены</a><a href="#akcii">Акции</a>')

# ---------- HERO ----------
def rot(lines):
    out = ''
    for words in lines:
        out += '<span aria-hidden="true">' + ' '.join(f'<span class="sw"><span style="--i:{i}">{w}</span></span>' for i, w in enumerate(words)) + '</span>'
    return out
ROT = [['Лечим', 'под микроскопом', 'и бинокулярами.'],
       ['Рязань,', 'ул. Попова, 4а,', 'с 9:00', 'до 21:00.'],
       ['Консультация,', 'план лечения', 'и снимок', 'бесплатно.']]
LOGO_A = json.dumps({k: logo[k] for k in ('cap', 'a', 'thin', 'sw')})
HERO = f'''<section class="hero hero--v hero--v1" aria-labelledby="h1"><div class="hx--a" aria-hidden="true"></div><script type="application/json" id="logo-a">{LOGO_A}</script><div class="wrap hero__in">
  <div class="hero__text">
    <h1 id="h1"><span data-split>Ваша улыбка</span> <span class="hv__l2" data-split>главный предмет Академии.</span></h1>
    <p class="hv__rot"><span class="sr">Лечим под микроскопом и бинокулярами. Рязань, ул. Попова, 4а, ежедневно с 9:00 до 21:00. Консультация, план лечения и снимок бесплатно.</span>{rot(ROT)}</p>
    <div class="hero__actions"><a class="btn btn--lg" href="zapis" data-modal="book" data-magnet>Записаться на бесплатную консультацию</a></div>
  </div>
</div></section>'''
block('<section class="hero hero--v', '</section>', HERO)
# зуб Вайтис и переключатель его вариантов убираем
s = re.sub(r'<div class="hx hx--tooth".*?</div>\n', '', s, count=1)
s = re.sub(r'<div class="hx-switch".*?</div>\n', '', s, count=1)

# ---------- врачи ----------
DOCS = [
    dict(slug='lazareva', fam='Лазарева', name='Элина', otch='Вячеславовна', ini='ЭЛ', role='Терапевт, детский стоматолог',
         short='Терапевт', exp='Стаж 5 лет', focus='Эстетические реставрации, лечение постоянных и молочных зубов, восстановление под коронку, гигиена и отбеливание',
         tags='lechenie-zubov detskaya estetika gigiena', chief=True),
    dict(slug='lazarev', fam='Лазарев', name='Виктор', otch='Викторович', ini='ВЛ', role='Ортопед, хирург',
         short='Ортопед', exp='Стаж 35 лет', focus='Протезирование на имплантах All-on-4 и All-on-6, виниры, коронки из циркония и керамики, съёмные и несъёмные протезы',
         tags='protezirovanie implantaciya estetika hirurgiya', chief=False),
    dict(slug='gerasimova', fam='Герасимова', name='Елизавета', otch='Витальевна', ini='ЕГ', role='Гигиенист',
         short='Гигиенист', exp='', focus='Профессиональная гигиена полости рта и отбеливание',
         tags='gigiena estetika', chief=False),
]
def doc_photo(d):
    # фото Герасимовой пока нет: в карточке остаются инициалы
    return f'images/doctors/{d["slug"]}.webp' if d['slug'] != 'gerasimova' else ''


trio = ''.join(f'<li><a href="#team" aria-label="{d["short"]}: {d["name"]} {d["fam"]}"><span class="hero__face" data-ph><span class="doc__initials" aria-hidden="true">{d["ini"]}</span>{img(doc_photo(d), d["name"] + " " + d["fam"])}</span><b>{d["short"]}</b><span>{d["name"]}<br>{d["fam"]}</span></a></li>' for d in DOCS)
SLOGAN_T = 'Учим улыбаться заново.'
SLOGAN = f'''<section class="slogan on-dark" aria-label="{SLOGAN_T}">
  <div class="marquee" aria-hidden="true"><div class="marquee__track">{''.join(f'<span class="marquee__item">{SLOGAN_T} <em>{SLOGAN_T}</em></span>' for _ in range(4))}</div></div>
  <div class="slogan__head" aria-hidden="true"><p class="slogan__title"><span class="line">{SLOGAN_T}</span></p></div>
  <div class="slogan__more"><div class="wrap"><ul class="hero__trio" aria-label="Врачи клиники">{trio}</ul></div></div>
</section>'''
block('<section class="slogan on-dark"', '</section>', SLOGAN)

# ---------- КЛИНИКА (тур) ----------
# Реальные фото новой клиники из чатов с Элиной (Max, Telegram, видео фасада)
CL = [
    ('images/real/fasad-vecher.webp', 'Здание клиники на Попова, 4а', 'tall'),
    ('images/real/kabinet.webp', 'Лечебный кабинет', 'tall'),
    ('images/real/holl-3.webp', 'Холл и ресепшен', ''),
    ('images/real/logo-stena.webp', 'Добро пожаловать в «Академию»', ''),
    ('images/real/kabinet-2.webp', 'Кабинет с видом на город', ''),
    ('images/real/lestnica.webp', 'Лестница на второй этаж', 'tall'),
]
CL2 = [
    ('images/real/holl.webp', 'Зона ожидания', ''),
    ('images/real/fasad-noch.webp', 'Вечером здание подсвечено', 'tall'),
    ('images/real/elina-kabinet.webp', 'Элина Вячеславовна в кабинете', 'tall'),
    ('images/real/holl-2.webp', 'Холл с диванами', ''),
    ('images/real/vitrina.webp', 'Витрины первого этажа', 'tall'),
]
def tfig(p, alt, kind, hidden=False):
    return f'<figure class="tfig{" tfig--tall" if kind == "tall" else ""}"{" aria-hidden=\"true\"" if hidden else ""}><span class="tfig__img">{img(p, alt)}</span><figcaption>{alt}</figcaption></figure>'
row1 = ''.join(tfig(*c) for c in CL) + ''.join(tfig(*c, hidden=True) for c in CL)
row2 = ''.join(tfig(*c) for c in CL2) + ''.join(tfig(*c, hidden=True) for c in CL2)
TOUR_P = 'Отдельное здание в Театральном районе Рязани: светлые кабинеты, мраморный холл, своя парковка и вход без ступенек. Каждый зуб лечим под микроскопом или бинокулярами.'
def pwin(p, alt, ar, p0, p1, pos, cls=''):
    return f'<div class="ptour__item{cls}"><div class="ptour__win" style="--ar:{ar};--p0:{p0};--p1:{p1}"><span class="ptour__rail">{img(p, alt, "ptour__img", "object-position:" + pos)}</span></div><p class="ptour__cap" aria-hidden="true">{alt}</p></div>'
def pfig(p, alt, r, par=False):
    return f'<figure class="ptour__fig"{" data-par" if par else ""} style="--r:{r}"><span class="ptour__pic">{img(p, alt)}</span><figcaption>{alt}</figcaption></figure>'
TOUR = f'''<section class="tour on-dark" id="clinic" aria-labelledby="tr-title">
  <div class="tour__pin">
    <div class="tour__frame">{img("images/real/old-vrach.webp", "Виктор Викторович Лазарев на приёме", style="object-position:60% 40%")}</div>
    <div class="tour__title wrap"><span class="label label--light">Клиника</span><h2 id="tr-title" data-split>Здесь учат улыбаться</h2><p>{TOUR_P}</p><a class="btn btn--light" href="{ROUTE}" target="_blank" rel="noopener">Построить маршрут</a></div>
  </div>
  <p class="tour__lead wrap">{TOUR_P}</p>
  <div class="tour__rows" aria-label="Фото клиники">
    <div class="tour__row" data-dir="-1">{row1}</div><div class="tour__row" data-dir="1">{row2}</div>
  </div>
  <div class="ptour">
    <div class="ptour__car"><div class="ptour__items">
      <div class="ptour__item ptour__item--empty"></div>
      {pwin("images/real/fasad-vecher-2.webp", "Здание клиники", "3 / 4", .1, .6, "50% 40%")}{pwin("images/real/kabinet-3.webp", "Лечебный кабинет", "1 / 1", .1, .6, "50% 50%")}{pwin("images/real/holl-2.webp", "Холл", "3 / 2", .2, .7, "45% 60%", " ptour__item--left")}
      <div class="ptour__item ptour__item--main">{img("images/real/old-vrach.webp", "Виктор Викторович Лазарев на приёме", "ptour__img", "object-position:60% 40%")}<span class="ptour__shade"></span>
        <div class="ptour__slogan"><span class="label label--light"><span class="w" style="--i:0">Клиника</span></span><h2 class="ptour__title"><span class="w" style="--i:1">Здесь</span> <span class="w" style="--i:2">учат</span> <span class="w" style="--i:3">улыбаться</span></h2></div></div>
      <div class="ptour__item ptour__item--right">{img("images/real/elina-kabinet.webp", "Элина Вячеславовна в кабинете", "ptour__img", "object-position:50% 40%")}<p class="ptour__cap" aria-hidden="true">Кабинет терапевта</p></div>
    </div></div>
    <div class="ptour__spacer"></div>
    <div class="ptour__after">
      <div class="ptour__grid">{pfig("images/real/fasad-noch-2.webp", "Вечером здание подсвечено", "410 / 628")}{pfig("images/real/kabinet-4.webp", "Лечебный кабинет", "1 / 1", True)}{pfig("images/real/logo-stena-3.webp", "Логотип у лестницы", "410 / 628")}{pfig("images/real/holl-3.webp", "Холл и ресепшен", "520 / 416", True)}{pfig("images/real/kabinet-2.webp", "Кабинет с видом на город", "520 / 362")}{pfig("images/real/old-mikroskop.webp", "Лечение под бинокулярами", "410 / 628", True)}</div>
      <div class="ptour__text"><p>{TOUR_P}</p><a class="btn btn--light" href="{ROUTE}" target="_blank" rel="noopener">Построить маршрут</a></div>
    </div>
  </div>
</section>'''
block('<section class="tour on-dark"', '</section>', TOUR)

# ---------- ПОЧЕМУ МЫ ----------
FEAT = [
    ('5,0', '63 оценки на Яндекс Картах', '97% отзывов хвалят качество лечения. В 2ГИС 4,9 по 50 оценкам.'),
    ('100%', 'лечения под увеличением', 'Микроскоп и бинокуляры на каждом приёме: врач видит каждый канал и трещину.'),
    ('35', 'лет стажа у ортопеда', 'Виктор Викторович Лазарев ведёт All-on-4, виниры и коронки из циркония.'),
    ('0 ₽', 'консультация всех врачей', 'План лечения и прицельный снимок зуба бесплатно.'),
    ('7/7', 'без выходных', 'Ежедневно с 9:00 до 21:00. Своя парковка у входа.'),
]
feat = ''.join(f'<article class="fcard"><div class="fcard__body"><b class="fcard__big">{a}</b><h3>{b}</h3><p>{c}</p></div></article>' for a, b, c in FEAT)
FOIL = f'''<section class="foil on-dark" id="path" aria-labelledby="ph-title">
  <div class="foil__bg"></div>
  <div class="feat"><div class="feat__pin"><div class="feat__track">
    <div class="fcard fcard--intro"><span class="label">Почему нам доверяют</span><h2 id="ph-title" data-split>Отличники по отзывам пациентов</h2><p>Только то, что можно проверить в открытых источниках и на приёме.</p></div>
    {feat}
  </div><div class="wrap cta-strip"><p>Консультация, план лечения и снимок бесплатно. Ни к чему не обязывает.</p><a class="btn btn--light btn--lg" href="zapis" data-modal="book" data-magnet>Записаться на бесплатную консультацию</a></div></div></div>
</section>'''
block('<section class="foil on-dark"', '</section>', FOIL)

# ---------- УСЛУГИ ----------
SV = [
    ('implantaciya', 'Имплантация и All-on-4', ['Имплант с коронкой под ключ 63 900 ₽', 'All-on-4 от 300 000 ₽', 'All-on-6 330 000 ₽', 'Синус-лифтинг'], '50% 34%'),
    ('lechenie-zubov', 'Лечение под микроскопом', ['Кариес от 5 000 ₽', 'Пульпит от 11 000 ₽', 'Перелечивание каналов'], ''),
    ('detskaya', 'Детская стоматология', ['Лечение молочного зуба 4 500 ₽', 'Удаление молочного зуба 1 500 ₽', 'Детская чистка 3 500 ₽'], ''),
    ('protezirovanie', 'Коронки и протезы', ['Коронки из диоксида циркония', 'Керамика и металлокерамика', 'Съёмные и несъёмные протезы'], ''),
    ('estetika', 'Виниры и реставрация', ['Виниры от 35 000 ₽', 'Реставрация от 5 500 ₽', 'Отбеливание'], ''),
]
cards = ''.join(f'''
    <a class="svl-card" href="#prices" style="--delay:{i * .3:.1f}s">
      {img(f"images/uslugi/{k}.webp", "", "svl-card__img", ("object-position:" + pos) if pos else "")}
      <span class="svl-card__in"><span class="svl-card__top"><span class="svl-go" aria-hidden="true">{ARROW}</span></span><h3 class="svl-card__title">{t}</h3><span class="svl-card__sub">{''.join(f"<span>{x}</span>" for x in sub)}</span></span>
    </a>''' for i, (k, t, sub, pos) in enumerate(SV))
ROWS = ['Профессиональная гигиена и отбеливание', 'Удаление зубов, в том числе мудрости', 'Прицельный снимок и диагностика', 'Лечение дёсен и пародонтоза']
rows = ''.join(f'\n    <a class="svl-row" href="#prices" style="--delay:{i * .3:.1f}s"><h3 class="svl-row__title">{t}</h3><span class="svl-row__act"><span class="svl-go" aria-hidden="true">{ARROW}</span></span></a>' for i, t in enumerate(ROWS))
SERV = f'''<section class="section section--sage svs" id="services" aria-labelledby="sv-title">
<div class="svl">
  <div class="svl__head"><div class="wrap"><h2 id="sv-title" data-split>Услуги</h2><span class="svl__links"><a class="link" href="#prices">Весь прайс</a></span></div></div>
  <div class="svl__top"><div class="wrap"><div class="svl-grid" data-svl>{cards}
  </div></div></div>
  <div class="svl__bottom"><div class="wrap"><div class="svl-list" data-svl>{rows}
  </div><div class="svl__more"><a class="btn btn--light btn--lg" href="#prices">Смотреть цены</a></div></div></div>
</div>
</section>'''
block('<section class="section section--sage svs"', '</section>', SERV)

# ---------- АКЦИИ ----------
PR = [
    ('real/old-mikroskop', 'Виктор Викторович лечит под бинокулярами', 'Бесплатно', 'Консультация и снимок', '0 ₽', 'Осмотр любого врача, план лечения с ценой и прицельный снимок зуба', 'Записаться бесплатно', 'бесплатная консультация и снимок'),
    ('uslugi/implantaciya', 'Имплант с коронкой', 'Имплантация', 'Имплант под ключ', '63 900 ₽', 'Имплант и коронка по одной цене. Ведёт ортопед-хирург со стажем 35 лет', 'Записаться на консультацию', 'имплант под ключ 63 900 ₽'),
    ('tp/kost', 'Модель челюсти с имплантами', 'Все зубы за раз', 'All-on-4', 'от 300 000 ₽', 'Вся челюсть на 4 имплантах за одну операцию. Металлокерамика от 300 000 до 350 000 ₽, диоксид циркония 450 000 ₽', 'Узнать подробнее', 'All-on-4 от 300 000 ₽'),
    ('akcii/kids-gift', 'Мальчик с подарком в кабинете', 'Детям', 'Без слёз и страха', '4 500 ₽', 'Лечение молочного зуба. Врач договаривается с ребёнком, а не торопит', 'Записать ребёнка', 'детский приём'),
]
# Из чего складывается цена: пациент видит, за что платит
INCL = [
    [('Осмотр врача', '0 ₽'), ('Прицельный снимок зуба', '0 ₽'), ('План лечения с ценой каждого этапа', '0 ₽')],
    [('Установка импланта', '29 000 ₽'), ('Формирователь десны и абатмент', '4 900 ₽'), ('Коронка на имплант', '30 000 ₽')],
    [('Снимки и план операции', 'входит'), ('4 импланта с установкой', 'входит'), ('Несъёмный протез на 12 зубов', 'входит'), ('Примерки, фиксация, контроль', 'входит')],
    [('Анестезия', 'входит'), ('Лечение кариеса', 'входит'), ('Пломба', 'входит')],
]
pr = ''.join(f'''<article class="pr4-card" style="--i:{i}">
    <span class="pr4-card__pic">{img(f"images/{p}.webp", alt)}</span>
    <div class="pr4-card__text">
      <span class="label pr-tag">{tag}</span>
      <h3 class="pr-title">{t}</h3>
      <p class="pr-price"><b>{price}</b></p>
      <p class="pr-gift">{gift}</p>
      <div class="au-incl"><p class="au-incl__t">Из чего складывается цена</p><ul>{''.join(f'<li><span>{a}</span><i aria-hidden="true"></i><b>{b}</b></li>' for a, b in INCL[i])}</ul></div>
      <a class="btn btn--lg" href="zapis" data-modal="book" data-promo="{promo}">{btn}</a>
    </div>
  </article>''' for i, (p, alt, tag, t, price, gift, btn, promo) in enumerate(PR))
AL = [('Консультация', 'Осмотр, план лечения и снимок зуба', '0 ₽'), ('Прицельный снимок', 'Если нужен отдельно', '350 ₽'),
      ('Рассрочка', 'Лечение можно оплатить частями', 'Частями'), ('Подарочный сертификат', 'Здоровая улыбка в подарок близким', 'Подарок'),
      ('Парковка', 'Своя, есть места для людей с инвалидностью', 'Бесплатно'), ('Без выходных', 'Ежедневно с 9:00 до 21:00', '7/7')]
alv = ''.join(f'<li data-reveal><span class="alv4__l"><span class="alv__t">{a}</span><span class="alv__d">{b}</span></span><i aria-hidden="true"></i><b class="alv__n">{c}</b></li>' for a, b, c in AL)
alp = ''.join(f'<li data-reveal><b>{a} <em class="pr-al__n">{c}</em></b><span>{b}</span></li>' for a, b, c in AL)
AKCII = f'''<section class="section pr on-dark" id="akcii" aria-labelledby="pr-title"><div class="wrap">
  <div class="section__head"><div><span class="label label--light">Акции</span><h2 id="pr-title" data-split>Честные цены и выгодные условия</h2></div><p>Назовите акцию, когда администратор перезвонит.</p></div>
  <div class="pr4">{pr}</div>
  <div class="alx"><div class="alx__desk"><div class="alv4"><h3 class="pr-al__title">Выгодно всегда</h3><ul class="alv4__list">{alv}</ul></div></div><div class="alx__phone"><div class="pr-al"><h3 class="pr-al__title">Выгодно всегда</h3><ul class="pr-al__list">{alp}</ul></div></div></div>
</div></section>'''
block('<section class="section pr on-dark"', '</div></section>', AKCII)

# ---------- ПРАЙС (секция в стиле FAQ-аккордеона, ставим перед врачами) ----------
PRICE = [
    ('Диагностика', [('Консультация любого врача с планом лечения', 'Бесплатно'), ('Прицельный снимок зуба', '350 ₽')]),
    ('Лечение зубов', [('Поверхностный кариес', '5 000 ₽'), ('Средний кариес', '5 500 ₽'), ('Глубокий кариес', '6 500 ₽'), ('Эстетическая реставрация зуба', 'от 5 500 до 7 700 ₽'),
                       ('Пульпит, 1 канал', '11 000 ₽'), ('Пульпит, 2 канала', '16 500 ₽'), ('Пульпит, 3 канала', '22 000 ₽'), ('Пульпит, 4 канала', '27 500 ₽'), ('Лечение периодонтита и кисты', 'от 16 000 ₽')]),
    ('Гигиена', [('Профессиональная гигиена (ультразвук + Air Flow)', '4 500 ₽'), ('Гигиена при пародонтозе', '5 500 ₽'), ('Герметизация фиссур', '4 500 ₽')]),
    ('Протезирование', [('Коронка на зуб', '18 000 ₽'), ('Коронка на имплант', '30 000 ₽'), ('Виниры', 'от 35 000 ₽'), ('Съёмный протез', 'от 20 000 ₽'),
                        ('All-on-4, металлокерамика', 'от 300 000 до 350 000 ₽'), ('All-on-4, диоксид циркония', '450 000 ₽'), ('All-on-6', '330 000 ₽')]),
    ('Имплантация и хирургия', [('Имплантация под ключ (имплант + коронка)', '63 900 ₽'), ('Установка импланта', '29 000 ₽'), ('Синус-лифтинг', 'от 13 000 ₽'),
                                ('Простое удаление зуба', '2 110 ₽'), ('Сложное удаление зуба', '3 660 ₽'), ('Удаление зуба мудрости', '8 650 ₽')]),
    ('Детям', [('Лечение молочного зуба', '4 500 ₽'), ('Удаление молочного зуба', '1 500 ₽'), ('Профессиональная чистка зубов', '3 500 ₽')]),
]
def price_group(i, name, items):
    li = ''.join(f'<li data-reveal><span class="alv4__l"><span class="alv__t">{a}</span></span><i aria-hidden="true"></i><b class="alv__n">{b}</b></li>' for a, b in items)
    return f'<details class="faqt"{" open" if i == 0 else ""} data-reveal><summary><h3>{name}</h3><i aria-hidden="true"></i></summary><div class="faqt__body"><ul class="alv4__list au-price">{li}</ul></div></details>'
PRICES = f'''<section class="section faqv au-prices" id="prices" aria-labelledby="pc-title"><div class="wrap">
  <h2 id="pc-title" class="section__title faqv__title" data-split>Цены без сюрпризов. Итог врач назовёт до начала лечения.</h2>
  <div class="faqv__main">{''.join(price_group(i, n, it) for i, (n, it) in enumerate(PRICE))}</div>
  <p class="au-prices__note">Цены указаны по данным клиники, не являются публичной офертой. Всё лечение выполняется с микроскопом и бинокулярами.</p>
</div></section>

'''

# ---------- ВРАЧИ ----------
def doc_card(d, col):
    full = f'{d["fam"]} {d["name"]} {d["otch"]}'
    role = d['role'] + (f' · {d["exp"]}' if d['exp'] else '')
    return f'''<article class="doc{" doc--chief" if d["chief"] else ""}" data-tags="{d["tags"]}" data-col="{col}">
  <div class="doc__photo" data-ph><span class="doc__initials" aria-hidden="true">{d["ini"]}</span>{img(doc_photo(d), full, extra='sizes="auto, (max-width: 760px) 80vw, 30vw"')}
    <a class="doc__cover" href="zapis?doctor={d["slug"]}" data-modal="book" data-doctor="{d["slug"]}" tabindex="-1" aria-hidden="true"></a>
    <a class="doc__go" href="zapis?doctor={d["slug"]}" data-modal="book" data-doctor="{d["slug"]}" aria-label="Записаться: {d["name"]} {d["fam"]}">{ARROW}</a></div>
  <h3><a href="zapis?doctor={d["slug"]}" data-modal="book" data-doctor="{d["slug"]}">{full}</a></h3>
  <p class="doc__role{" doc__role--chief" if d["chief"] else ""}">{role}</p>
  <p class="doc__focus">{d["focus"]}</p>
  <a class="btn btn--ghost btn--sm doc__cta" href="zapis?doctor={d["slug"]}" data-modal="book" data-doctor="{d["slug"]}">Записаться к врачу</a>
</article>'''
TEAM = f'''<section class="section section--sage" id="team" aria-labelledby="tm-title"><div class="wrap">
  <div class="section__head"><div><span class="label">Врачи</span><h2 id="tm-title" data-split>Кто будет вас лечить</h2></div><p>Семейная команда выпускников РязГМУ: терапевт и детский стоматолог, ортопед-хирург со стажем 35 лет и гигиенист.</p></div>
  <div class="team__grid team__grid--lava">{''.join(doc_card(d, "lr"[i % 2]) for i, d in enumerate(DOCS))}</div>
</div></section>'''
i = s.index('<section class="section section--sage" id="team"')
j = s.index('</div></section>', s.index('</article></div>', i)) + len('</div></section>')
s = s[:i] + PRICES + TEAM + s[j:]

# ---------- ОТЗЫВЫ ----------
STAR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 2.5 2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z"/></svg>'
Q = [  # дословно из отзывов в 2ГИС
    ('«Всегда обращаемся к Элине Вячеславовне, лучший семейный доктор!»', '«Всегда обращаемся к Элине Вячеславовне, <b>лучший семейный доктор</b>!»', 'mid'),
    ('«И дочка и маленький сын без опаски идут лечить зубки.»', '«И дочка и маленький сын <b>без опаски идут лечить зубки</b>.»', 'mid'),
    ('«Врач Лазарев Виктор Викторович действительно профессионал своего дела»', '«Врач Лазарев Виктор Викторович <b>действительно профессионал своего дела</b>»', 'mid'),
    ('«Пролечили кариес без единой слезинки.»', '«Пролечили кариес <b>без единой слезинки</b>.»', 'short'),
    ('«Великолепная клиника, где безболезненно лечат зубы.»', '«Великолепная клиника, где <b>безболезненно лечат зубы</b>.»', 'short'),
    ('«Интерьер очень приятный, все зоны рассчитаны логично и лаконично.»', '«<b>Интерьер очень приятный</b>, все зоны рассчитаны логично и лаконично.»', 'mid'),
    ('«очень понравилась врач Лазарева Элина Вячеславовна и ее чудесный ассистент Елизавета»', '«очень понравилась врач Лазарева Элина Вячеславовна и <b>ее чудесный ассистент Елизавета</b>»', 'mid'),
]
def rvrow(items, d):
    one = ''.join(f'<figure class="rv{" rv--short" if k == "short" else ""}"><blockquote>{q}</blockquote></figure>' for q, _, k in items)
    hid = one.replace('<figure class="rv', '<figure aria-hidden="true" class="rv')
    return f'<div class="rv__row" data-dir="{d}">{one}{one}{hid}{hid}</div>'
tones = ['ink', 'green', 'sage', 'white', 'ink', 'green', 'sage']
REV = f'''<section class="section reviews" id="reviews" aria-labelledby="rv-title">
  <div class="wrap section__head"><div><span class="label">Отзывы</span><h2 id="rv-title" data-split>113 оценок, и почти все на пятёрку</h2></div></div>
  <div class="wrap"><div class="rt" aria-label="Оценки клиники на площадках" data-reveal>
    <div class="rt-avg">
      <div class="rt-avg__num" data-count="5,0">5,0</div>
      <div class="rt-stars" role="img" aria-label="5 из 5">{STAR * 5}</div>
      <p class="rt-avg__cap">Оценка на Яндекс Картах по 63 оценкам. 97% отзывов о качестве лечения положительные</p>
    </div>
    <div class="rt-sites">
      <a class="rt-site" href="{YA}reviews/" target="_blank" rel="noopener" data-goal="reviews_yandex">
        <span class="rt-site__top"><span class="rt-mark rt-mark--ya"><img src="images/brand/yandex-maps.svg" alt="" loading="lazy" decoding="async"></span><span class="rt-site__val">5,0{STAR}</span></span>
        <span><span class="rt-site__name">Яндекс Карты</span><span class="rt-site__count">63 оценки, 54 отзыва</span></span>
        <span class="rt-site__link">Смотреть отзывы</span>
      </a><a class="rt-site" href="{GIS}/tab/reviews" target="_blank" rel="noopener" data-goal="reviews_2gis">
        <span class="rt-site__top"><span class="rt-mark rt-mark--2gis"><img src="images/brand/2gis.webp" alt="" loading="lazy" decoding="async"></span><span class="rt-site__val">4,9{STAR}</span></span>
        <span><span class="rt-site__name">2ГИС</span><span class="rt-site__count">50 оценок, 49 отзывов</span></span>
        <span class="rt-site__link">Смотреть отзывы</span>
      </a>
    </div>
    <div class="rt-pd au-rt-quote">
      <div class="rt-pd__text">
        <p class="rt-pd__quote">«Основная причина моего выбора: профессионализм врача Лазаревой Элины Вячеславовны.»</p>
        <a class="link rt-pd__link" href="{GIS}/tab/reviews" target="_blank" rel="noopener">Екатерина К., отзыв в 2ГИС</a>
      </div>
    </div>
  </div></div>
  <div class="rv__rows">
    {rvrow(Q[:4], -1)}{rvrow(Q[3:], 1)}
  </div>
  <div class="rvm rvm--stack">
    <div class="rvs" role="group" aria-label="Отзывы пациентов">
      {''.join(f'<figure class="rvs__card rvs__card--{k}" data-tone="{tones[n]}"><blockquote>{b}</blockquote></figure>' for n, (_, b, k) in enumerate(Q))}
    </div>
    <div class="rvs__bar"><p class="rvs__hint">Смахните отзыв, чтобы прочитать следующий</p><button class="btn btn--sm rvs__next" type="button">Следующий</button></div>
  </div>
</section>'''
block('<section class="section reviews"', '</section>', REV)

# ---------- FAQ ----------
FAQ = [
    ('Цена и оплата', [
        ('Сколько стоит лечение и когда я узнаю точную цену?', 'Цены на основные услуги есть в прайсе выше: кариес от 5 000 ₽, пульпит от 11 000 ₽, имплант под ключ 63 900 ₽. Точную цену врач назовёт на бесплатной консультации, до начала лечения.'),
        ('Консультация правда бесплатная?', 'Да. Консультация любого врача бесплатная, в неё входит план лечения и прицельный снимок зуба.'),
        ('Есть ли рассрочка?', 'Да, лечение можно оплатить частями. Оплата картой, наличными, по QR-коду и бесконтактно.')]),
    ('Лечение и боль', [
        ('Больно ли лечить зубы?', 'Перед лечением врач делает анестезию. В отзывах пациенты чаще всего пишут именно про безболезненное лечение.'),
        ('Зачем лечить под микроскопом?', 'Под увеличением врач видит все каналы и микротрещины. Поэтому лечение точнее, а зуб, который предлагали удалить, чаще удаётся сохранить. У нас так проходит всё лечение.'),
        ('Болит зуб. Что делать до приёма?', 'Не грейте щёку и не кладите на зуб таблетку. Примите обычное обезболивающее и позвоните нам, администратор запишет на ближайшее время.')]),
    ('Дети', [
        ('С какого возраста можно прийти?', 'С первых зубов. Первый визит начинается со знакомства с врачом и креслом.'),
        ('Ребёнок боится. Что делать?', 'Скажите об этом при записи. Элина Вячеславовна лечит и детей, и взрослых: не торопит, объясняет и договаривается с ребёнком.'),
        ('Нужно ли лечить молочные зубы?', 'Да. Кариес молочного зуба переходит на соседние и на зачаток постоянного. Лечение молочного зуба 4 500 ₽.')]),
    ('Импланты и протезы', [
        ('Что такое All-on-4?', 'Несъёмный протез всей челюсти на четырёх имплантах. Подходит, когда зубов почти не осталось. Металлокерамика от 300 000 до 350 000 ₽, диоксид циркония 450 000 ₽.'),
        ('Какую коронку выбрать?', 'Чаще всего из диоксида циркония: выглядит естественно и выдерживает жевательную нагрузку. Врач подскажет на консультации.'),
        ('Кто ставит импланты и протезы?', 'Виктор Викторович Лазарев, ортопед и хирург со стажем 35 лет. Он ведёт лечение от плана до готовых зубов.')]),
    ('Запись и визит', [
        ('Работаете в выходные?', 'Да, ежедневно с 9:00 до 21:00.'),
        ('Где вы находитесь?', 'Рязань, ул. Попова, 4а. Рядом своя парковка, есть места для людей с инвалидностью, вход без ступенек.'),
        ('Можно написать в мессенджер?', 'Да: WhatsApp, Telegram и MAX. Ссылки внизу страницы.')]),
]
faq_html = ''
for gi, (g, qs) in enumerate(FAQ):
    qh = ''.join(f'<details class="faqq"{" open" if gi == 0 and qi == 0 else ""}><summary><span>{q}</span><i aria-hidden="true"></i></summary><div class="faqq__a"><p>{a}</p></div></details>' for qi, (q, a) in enumerate(qs))
    faq_html += f'<details class="faqt"{" open" if gi == 0 else ""} data-reveal><summary><h3>{g}</h3><i aria-hidden="true"></i></summary><div class="faqt__body"><div class="faqt__list">{qh}</div></div></details>'
FAQS = f'''<section class="section faqv" id="faq" aria-labelledby="fq-title"><div class="wrap">
  <h2 id="fq-title" class="section__title faqv__title" data-split>Прежде чем прийти, вам, возможно, захочется узнать больше.</h2>
  <div class="faqv__main">{faq_html}</div>
</div></section>'''
block('<section class="section faqv" id="faq"', '</div></section>', FAQS)

# ---------- КОНТАКТЫ ----------
CONT = f'''<section class="section ctum" id="contacts" aria-labelledby="ct-title"><div class="wrap">
  <div class="section__head"><div><span class="label">Контакты</span><h2 id="ct-title" data-split>Театральный район: Попова, 4а</h2></div><p>Ежедневно с 9:00 до 21:00. Своя парковка у здания, есть места для людей с инвалидностью. Вход без ступенек, есть парковка для велосипедов.</p></div>
  <div class="place">
    <div class="place__map place__map--img" data-clip>{img("images/map/map.svg", "Карта: стоматология «Академия улыбки» на Попова, 4а", "place__img")}<span class="place__pin" aria-hidden="true">Академия улыбки</span><iframe title="Карта: стоматология «Академия улыбки», Рязань" data-src="https://yandex.ru/map-widget/v1/org/akademiya_ulybki/8207640702/" loading="lazy"></iframe><button class="place__unlock" type="button">Нажмите, чтобы двигать карту</button></div>
    <div class="place__info" data-reveal>
      <h3>Стоматология «Академия улыбки»</h3>
      <dl class="place__list">
        <div><dt>Адрес</dt><dd>г. Рязань, ул. Попова, 4а</dd></div>
        <div><dt>Телефон</dt><dd><a href="tel:{TEL}">{PHONE}</a><br><a href="tel:+74912426062">+7 (4912) 42-60-62</a></dd></div>
        <div><dt>Часы работы</dt><dd>{HOURS}<span class="place__status" data-open-status></span></dd></div>
        <div><dt>Удобства</dt><dd>Парковка, вход без ступенек, Wi-Fi</dd></div>
      </dl>
      <div class="place__btns"><a class="btn btn--sm" href="{ROUTE}" target="_blank" rel="noopener">Построить маршрут</a><a class="btn btn--ghost btn--sm" href="{GIS}" target="_blank" rel="noopener">Маршрут в 2ГИС</a><a class="btn btn--ghost btn--sm" href="tel:{TEL}">Позвонить</a></div>
      <button class="way__link place__share" type="button" data-share data-share-text="Рязань, ул. Попова, 4а. {HOURS}. {PHONE}" data-share-url="{YA}">Отправить адрес</button>
    </div>
  </div>
</div></section>'''
block('<section class="section ctum"', '</div></section>', CONT)

# ---------- ПОДВАЛ ----------
f0 = s.index('<footer'); f1 = s.index('</footer>') + len('</footer>')
foot = s[f0:f1]
foot = foot.replace('Администратор перезвонит с номера ' + PHONE, 'Администратор перезвонит с номера ' + PHONE)
foot = foot.replace('https://t.me/wtdent', TG)
foot = re.sub(r'<span class="footer__word">Вайтис</span>', '<span class="footer__word">Академия улыбки</span>', foot)
foot = re.sub(r'<div class="fstage__info".*?</div>\n  </div>\n  <div class="footer__legal">', lambda m: f'''<div class="fstage__info">
      <div class="fstage__group">
        <h3>Контакты</h3>
        <a class="fstage__big" href="tel:{TEL}">{PHONE}</a>
        <a class="fstage__big" href="tel:+74912426062">+7 (4912) 42-60-62</a>
        <a class="fstage__big fstage__big--mail" href="mailto:{MAIL}">{MAIL}</a>
      </div>
      <div class="fstage__group">
        <h3>Адрес</h3>
        <p class="fstage__addr">г. Рязань, ул. Попова, 4а</p>
        <p class="fstage__links"><a href="{ROUTE}" target="_blank" rel="noopener">Маршрут в Яндекс Картах</a><a href="{GIS}" target="_blank" rel="noopener">Открыть в 2ГИС</a></p>
      </div>
      <div class="fstage__group">
        <h3>Часы работы</h3>
        <p class="fstage__text">{HOURS}</p>
      </div>
      <nav class="fstage__group" aria-label="Услуги">
        <h3>Услуги</h3>
        <p class="fstage__list fstage__list--1">{''.join(f'<a href="#services">{t}</a>' for _, t, _, _ in SV)}{''.join(f'<a href="#services">{t}</a>' for t in ROWS[:2])}<a href="#prices">Все цены</a></p>
      </nav>
      <nav class="fstage__group" aria-label="Клиника">
        <h3>Клиника</h3>
        <p class="fstage__list fstage__list--2"><a href="#clinic">О клинике</a><a href="#prices">Цены</a><a href="#akcii">Акции</a><a href="#team">Врачи</a><a href="#reviews">Отзывы</a><a href="#faq">Вопросы</a><a href="#contacts">Контакты</a></p>
      </nav>
      <div class="fstage__group">
        <h3>Пациентам</h3>
        <p class="fstage__list fstage__list--2">
          <a href="zapis" data-modal="book">Бесплатная консультация</a>
          <a href="#faq">Рассрочка</a>
          <a href="#akcii">Подарочные сертификаты</a>
        </p>
      </div>
      <div class="fstage__group">
        <h3>На связи</h3>
        <p class="fstage__list fstage__list--2">
          <a href="{WA}" target="_blank" rel="noopener">WhatsApp</a>
          <a href="{TG}" target="_blank" rel="noopener">Telegram</a>
          <a href="{MAX}" target="_blank" rel="noopener">MAX</a>
          <a href="{VK}" target="_blank" rel="noopener">ВКонтакте</a>
        </p>
      </div>
    </div>
  </div>
  <div class="footer__legal">''', foot, flags=re.S)
foot = re.sub(r'<span>© 2026 ООО «ВАЙТИС».*?</span>', '<span>© 2026 ООО «Академия улыбки», ИНН 6200008671, ОГРН 1246200007525. 390027, г. Рязань, пл. Попова, д. 4а. Лицензия на медицинскую деятельность: номер будет указан на рабочем сайте.</span>', foot, flags=re.S)
foot = re.sub(r'<span class="footer__docs">.*?</span>', '<span class="footer__docs"><a href="#">Политика конфиденциальности</a><a href="#">Согласие на обработку персональных данных</a><a href="#" data-cookie-settings>Настройки cookie</a></span>', foot, flags=re.S)
s = s[:f0] + foot + s[f1:]

# ---------- модалки и хвост ----------
s = re.sub(r'<script type="application/json" id="um-docs">.*?</script>',
           '<script type="application/json" id="um-docs">' + json.dumps({d['slug']: f'{d["name"]} {d["fam"]}' for d in DOCS}, ensure_ascii=False) + '</script>', s, flags=re.S)
s = s.replace('https://t.me/wtdent', TG).replace('https://max.ru/+79661723378', MAX).replace('https://wa.me/79037977688', WA)
s = s.replace('Консультация по All-on-4</h2><p class="modal__sub">Хирург, ортопед и терапевт осмотрят вас вместе, сделаем КТ.', 'Консультация по All-on-4</h2><p class="modal__sub">Ортопед-хирург осмотрит вас и составит план.')
# ссылки на внутренние страницы Вайтис ведут на якоря главной
s = re.sub(r'href="(privacy|soglasie|soglashenie|svedeniya|gosudarstvennye-garantii)/[^"]*"', 'href="#"', s)
s = re.sub(r'href="(uslugi|implantaciya|lechenie-zubov|detskaya|ortodontiya|protezirovanie|gigiena|estetika|hirurgiya|diagnostika)/"', 'href="#services"', s)
s = s.replace('href="ceny/"', 'href="#prices"').replace('href="vrachi/"', 'href="#team"')
s = s.replace('action="spasibo/"', 'action="#"')
s = re.sub(r'стоматология в\W*Одинцово', 'стоматология в Рязани', s)
s = s.replace('Хирург, ортопед и терапевт осмотрят вас вместе, сделаем КТ.', 'Ортопед-хирург осмотрит вас, сделаем снимок и составим план.')
inv = ''.join(f'<li><span class="invite__pic" data-ph><span class="doc__initials" aria-hidden="true">{d["ini"]}</span>{img(doc_photo(d), d["name"] + " " + d["fam"])}</span><b>{d["short"]}</b><span>{d["name"]}<br>{d["fam"]}</span></li>' for d in DOCS)
s = re.sub(r'<ul class="invite__docs">.*?</ul>', '<ul class="invite__docs">' + inv + '</ul>', s, flags=re.S)
s = re.sub(r'\+7\W903\W797-76-88', PHONE, s)
s = s.replace('images/brand/header-logo-light.svg', 'images/brand/header-logo.svg')
s = s.replace('Вайтис', 'Академия улыбки').replace('White Teeth', 'Академия улыбки')

open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(s)
left = [w for w in ['Одинцов', 'Одинбург', 'Северная', 'Гвиниашвили', 'Чилингарян', 'Казарян', 'wtdent', '79037977688', 'Смирнов', 'Ткачук'] if w in s]
print('OK', len(s), 'leftovers:', left)
