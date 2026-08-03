import './style.css';
import hospitals from './data/hospitals.json';

/* 로고 파일 규칙: public/logos/{슬러그}_{버전}.png
   버전 — v: 세로 / h: 가로 / vw: 세로 화이트 / hw: 가로 화이트
   파일이 존재하는 버전만 다운로드 버튼이 켜진다(Image 프리로드로 확인). */
const VARIANTS = [
  { code: 'v', label: '세로', dark: false },
  { code: 'h', label: '가로', dark: false },
  { code: 'vw', label: '세로 화이트', dark: true },
  { code: 'hw', label: '가로 화이트', dark: true },
];

const logoPath = (slug, code) => `/logos/${slug}_${code}.png`;

// 경로별 존재 여부 캐시: true/false 또는 pending Promise
const logoCache = new Map();

function checkLogo(src) {
  if (logoCache.has(src)) {
    const hit = logoCache.get(src);
    return typeof hit === 'boolean' ? Promise.resolve(hit) : hit;
  }
  const p = new Promise((resolve) => {
    const img = new Image();
    img.onload = () => {
      logoCache.set(src, true);
      resolve(true);
    };
    img.onerror = () => {
      logoCache.set(src, false);
      resolve(false);
    };
    img.src = src;
  });
  logoCache.set(src, p);
  return p;
}

/* ---------- 상태 ---------- */
let query = '';
let dept = '전체';

const DEPTS = ['전체', ...new Set(hospitals.flatMap((h) => h.dept))];

/* ---------- 뼈대 ---------- */
const app = document.getElementById('app');
app.innerHTML = `
  <header class="header">
    <div class="header-inner">
      <div class="header-top">
        <div class="brand">
          <h1>브랜드 키트 허브</h1>
          <span class="sub">이스터에그 · 병원 브랜드 자산 모음</span>
        </div>
        <div class="search">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
          <input id="search-input" type="search" placeholder="병원명·전화·주소 검색" autocomplete="off" />
        </div>
      </div>
      <div class="chips" id="chips"></div>
    </div>
  </header>
  <main class="main">
    <p class="count" id="count"></p>
    <div class="grid" id="grid"></div>
  </main>
  <footer class="footer">로고 추가: public/logos/{슬러그}_{v·h·vw·hw}.png 규칙으로 파일을 넣고 재배포하면 버튼이 자동으로 켜집니다.</footer>
  <div class="overlay" id="overlay"></div>
  <aside class="drawer" id="drawer" role="dialog" aria-modal="true"></aside>
  <div class="toast" id="toast"></div>
`;

const $grid = document.getElementById('grid');
const $chips = document.getElementById('chips');
const $count = document.getElementById('count');
const $overlay = document.getElementById('overlay');
const $drawer = document.getElementById('drawer');
const $toast = document.getElementById('toast');

/* ---------- 필터 칩 ---------- */
function renderChips() {
  $chips.innerHTML = '';
  DEPTS.forEach((d) => {
    const btn = document.createElement('button');
    btn.className = 'chip' + (d === dept ? ' on' : '');
    btn.textContent = d;
    btn.onclick = () => {
      dept = d;
      renderChips();
      renderGrid();
    };
    $chips.appendChild(btn);
  });
}

/* ---------- 그리드 ---------- */
function filtered() {
  const q = query.trim().toLowerCase();
  return hospitals.filter((h) => {
    if (dept !== '전체' && !h.dept.includes(dept)) return false;
    if (!q) return true;
    return [h.name, h.slug, h.phone, h.address, ...h.dept]
      .join(' ')
      .toLowerCase()
      .includes(q);
  });
}

function cardLogoEl(h) {
  const wrap = document.createElement('div');
  wrap.className = 'card-logo';
  const fallback = document.createElement('div');
  fallback.className = 'logo-fallback';
  fallback.style.background = h.colors[0]?.hex || '#9aa1ab';
  fallback.textContent = h.name.slice(0, 1);
  wrap.appendChild(fallback);

  // 가로형 우선, 없으면 세로형 컬러 로고를 썸네일로 사용
  (async () => {
    for (const code of ['h', 'v']) {
      const src = logoPath(h.slug, code);
      if (await checkLogo(src)) {
        const img = document.createElement('img');
        img.src = src;
        img.alt = `${h.name} 로고`;
        wrap.replaceChildren(img);
        return;
      }
    }
  })();
  return wrap;
}

function renderGrid() {
  const list = filtered();
  $count.textContent = `${list.length}개 병원`;
  $grid.innerHTML = '';

  if (!list.length) {
    const div = document.createElement('div');
    div.className = 'empty';
    div.textContent = '검색 결과가 없습니다.';
    div.style.gridColumn = '1 / -1';
    $grid.appendChild(div);
    return;
  }

  list.forEach((h) => {
    const card = document.createElement('button');
    card.className = 'card';
    card.onclick = () => openDrawer(h);

    card.appendChild(cardLogoEl(h));

    const name = document.createElement('div');
    name.className = 'card-name';
    name.textContent = h.name;
    card.appendChild(name);

    const meta = document.createElement('div');
    meta.className = 'card-meta';

    const tags = document.createElement('div');
    tags.className = 'tags';
    h.dept.forEach((d) => {
      const t = document.createElement('span');
      t.className = 'tag';
      t.textContent = d;
      tags.appendChild(t);
    });
    meta.appendChild(tags);

    const dots = document.createElement('div');
    dots.className = 'dots';
    h.colors.slice(0, 3).forEach((c) => {
      const dot = document.createElement('span');
      dot.className = 'dot';
      dot.style.background = c.hex;
      dots.appendChild(dot);
    });
    meta.appendChild(dots);

    card.appendChild(meta);
    $grid.appendChild(card);
  });
}

/* ---------- 클립보드 + 토스트 ---------- */
let toastTimer;
function showToast(msg, colorHex) {
  $toast.innerHTML = '';
  if (colorHex) {
    const d = document.createElement('span');
    d.className = 'dot-preview';
    d.style.background = colorHex;
    $toast.appendChild(d);
  }
  $toast.appendChild(document.createTextNode(msg));
  $toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => $toast.classList.remove('show'), 1600);
}

async function copyText(text, label, colorHex) {
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    const ta = document.createElement('textarea');
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    ta.remove();
  }
  showToast(label || `복사됨 · ${text}`, colorHex);
}

/* ---------- 드로어 ---------- */
function section(title, node) {
  const sec = document.createElement('section');
  sec.className = 'section';
  const h3 = document.createElement('h3');
  h3.textContent = title;
  sec.appendChild(h3);
  sec.appendChild(node);
  return sec;
}

function logoSection(h) {
  const grid = document.createElement('div');
  grid.className = 'logo-grid';

  VARIANTS.forEach((v) => {
    const slot = document.createElement('div');
    slot.className = 'logo-slot' + (v.dark ? ' dark' : '');

    const preview = document.createElement('div');
    preview.className = 'preview';
    slot.appendChild(preview);

    const foot = document.createElement('div');
    foot.className = 'slot-foot';
    const label = document.createElement('span');
    label.className = 'slot-label';
    label.textContent = v.label;
    foot.appendChild(label);
    slot.appendChild(foot);

    const src = logoPath(h.slug, v.code);
    checkLogo(src).then((ok) => {
      if (ok) {
        const img = document.createElement('img');
        img.src = src;
        img.alt = `${h.name} ${v.label} 로고`;
        preview.appendChild(img);

        const a = document.createElement('a');
        a.className = 'dl-btn';
        a.href = src;
        a.download = `${h.slug}_${v.code}.png`;
        a.innerHTML =
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12"/><path d="m6 11 6 6 6-6"/><path d="M4 21h16"/></svg>다운로드';
        foot.appendChild(a);
      } else {
        slot.classList.add('missing');
        const none = document.createElement('span');
        none.className = 'none';
        none.textContent = '파일 없음';
        preview.appendChild(none);
        const noneTxt = document.createElement('span');
        noneTxt.className = 'none-txt';
        noneTxt.textContent = '없음';
        foot.appendChild(noneTxt);
      }
    });

    grid.appendChild(slot);
  });

  return section('로고 다운로드', grid);
}

function colorSection(h) {
  const wrap = document.createElement('div');
  wrap.className = 'swatches';

  if (!h.colors.length && !h.gradient) {
    const div = document.createElement('div');
    div.className = 'placeholder';
    div.style.flex = '1';
    div.textContent = '컬러 미지정';
    wrap.appendChild(div);
    return section('브랜드 컬러', wrap);
  }

  h.colors.forEach((c) => {
    const btn = document.createElement('button');
    btn.className = 'swatch';
    btn.title = '클릭하면 HEX가 복사됩니다';
    btn.onclick = () => copyText(c.hex, `복사됨 · ${c.hex}`, c.hex);

    const box = document.createElement('span');
    box.className = 'chipbox';
    box.style.background = c.hex;
    btn.appendChild(box);

    const hex = document.createElement('span');
    hex.className = 'hex';
    hex.textContent = c.hex;
    btn.appendChild(hex);

    const lbl = document.createElement('span');
    lbl.className = 'lbl';
    lbl.textContent = c.label;
    btn.appendChild(lbl);

    wrap.appendChild(btn);
  });

  if (h.gradient) {
    const css = `linear-gradient(90deg, ${h.gradient[0]}, ${h.gradient[1]})`;
    const btn = document.createElement('button');
    btn.className = 'swatch';
    btn.title = '클릭하면 그라데이션 CSS가 복사됩니다';
    btn.onclick = () => copyText(css, '복사됨 · 그라데이션 CSS', h.gradient[0]);

    const box = document.createElement('span');
    box.className = 'chipbox';
    box.style.background = css;
    btn.appendChild(box);

    const hex = document.createElement('span');
    hex.className = 'hex';
    hex.textContent = `${h.gradient[0]} → ${h.gradient[1]}`;
    hex.style.fontSize = '10px';
    btn.appendChild(hex);

    const lbl = document.createElement('span');
    lbl.className = 'lbl';
    lbl.textContent = 'Gradient';
    btn.appendChild(lbl);

    wrap.appendChild(btn);
  }

  return section('브랜드 컬러 · 클릭 복사', wrap);
}

function infoSection(h) {
  const list = document.createElement('div');
  list.className = 'info-list';

  const row = (k, vNode, copyValue) => {
    const r = document.createElement('div');
    r.className = 'info-row';
    const key = document.createElement('span');
    key.className = 'k';
    key.textContent = k;
    r.appendChild(key);
    const val = document.createElement('span');
    val.className = 'v';
    val.appendChild(vNode);
    r.appendChild(val);
    if (copyValue) {
      const btn = document.createElement('button');
      btn.className = 'copy-mini';
      btn.textContent = '복사';
      btn.onclick = () => copyText(copyValue, `복사됨 · ${copyValue}`);
      r.appendChild(btn);
    }
    list.appendChild(r);
  };

  const tel = document.createElement('a');
  tel.href = `tel:${h.phone.replace(/[^0-9]/g, '')}`;
  tel.textContent = h.phone;
  row('전화', tel, h.phone);

  row('주소', document.createTextNode(h.address), h.address);

  const ul = document.createElement('ul');
  ul.className = 'hours';
  h.hours.forEach((line) => {
    const li = document.createElement('li');
    li.textContent = line;
    ul.appendChild(li);
  });
  row('진료시간', ul, null);

  row('진료과', document.createTextNode(h.dept.join(' · ')), null);

  return section('기본 정보', list);
}

function placeholderSection(title, desc) {
  const div = document.createElement('div');
  div.className = 'placeholder';
  div.textContent = desc;
  return section(title, div);
}

function linkSection(h) {
  const links = h.links || [];
  if (!links.length) {
    return placeholderSection('링크', '등록된 링크가 없습니다 — hospitals.json의 links에 추가하세요.');
  }
  const wrap = document.createElement('div');
  wrap.className = 'links';
  links.forEach((l) => {
    const a = document.createElement('a');
    a.className = 'link-btn';
    a.href = l.url;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    a.innerHTML =
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1.5 1.5"/><path d="M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1.5-1.5"/></svg>';
    a.appendChild(document.createTextNode(l.label));
    wrap.appendChild(a);
  });
  return section('링크', wrap);
}

function openDrawer(h) {
  $drawer.innerHTML = '';

  const head = document.createElement('div');
  head.className = 'drawer-head';
  head.innerHTML = `
    <div class="titles">
      <h2></h2>
      <div class="slug"></div>
    </div>
    <button class="close-btn" aria-label="닫기">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M5 5l14 14M19 5 5 19"/></svg>
    </button>
  `;
  head.querySelector('h2').textContent = h.name;
  head.querySelector('.slug').textContent = h.slug;
  head.querySelector('.close-btn').onclick = closeDrawer;
  $drawer.appendChild(head);

  const body = document.createElement('div');
  body.className = 'drawer-body';
  body.appendChild(logoSection(h));
  body.appendChild(colorSection(h));
  body.appendChild(infoSection(h));
  body.appendChild(linkSection(h));
  body.appendChild(
    placeholderSection('폰트 · 톤앤매너', '준비 중 — 국문/영문 지정 폰트, 톤 키워드가 들어갈 자리입니다.')
  );
  $drawer.appendChild(body);

  $drawer.classList.add('open');
  $overlay.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeDrawer() {
  $drawer.classList.remove('open');
  $overlay.classList.remove('open');
  document.body.style.overflow = '';
}

$overlay.onclick = closeDrawer;
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeDrawer();
});

/* ---------- 검색 ---------- */
document.getElementById('search-input').addEventListener('input', (e) => {
  query = e.target.value;
  renderGrid();
});

renderChips();
renderGrid();
