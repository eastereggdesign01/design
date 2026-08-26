import './portfolio.css';
import works from './data/works.json';
import manuscripts from './data/test-manuscripts.js';
import videos from './data/videos.json';
import hospitals from './data/hospitals.json';
import references from './data/references.json';
import prints from './data/prints.json';

/* 작업물 추가 = src/data/works.json 배열에 항목 하나 추가.
   { title, description, type, url, details: { tools, intent, method, test } }
   details의 키 중 있는 것만 탭으로 표시된다. */

const TABS = [
  ['tools', '사용 툴'],
  ['intent', '기획의도'],
  ['method', '제작방법'],
  ['cost', '비용'],
];

/* 테스트 탭: 원고를 클릭 한 번으로 복사해 실제 도구에서 써볼 수 있게 한다 */
const TEST_TAB = '__test';

/* 결과물 샘플 탭: 도구로 만든 결과 영상을 바로 재생 */
const SAMPLE_TAB = '__sample';

const carouselHTML = (set, small) => `
  <div class="sample-set${small ? ' small' : ''}">
    ${set.label ? `<p class="set-label">${set.label}</p>` : ''}
    <div class="sample-carousel">
      <div class="carousel-track" data-track>${set.images
        .map(
          (src, n) =>
            `<a href="${src}" target="_blank" rel="noopener"><img src="${src}" style="aspect-ratio:${set.ratio || '1 / 1'}" ${n === 0 ? '' : 'loading="lazy"'} alt="결과물 샘플 ${n + 1}" /></a>`
        )
        .join('')}</div>
      <button class="carousel-btn prev" data-dir="-1" aria-label="이전 이미지">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M15 18l-6-6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
      <button class="carousel-btn next" data-dir="1" aria-label="다음 이미지">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
      <div class="carousel-count" data-count></div>
    </div>
  </div>
`;

/* 이미지 세트: sampleSets([{label, images, ratio}]) 또는 단일 sampleImages */
const imageSets = (work) =>
  work.sampleSets ||
  (work.sampleImages?.length ? [{ images: work.sampleImages, ratio: work.sampleRatio }] : null);

const sampleHTML = (work) => {
  const sets = imageSets(work);
  const media = work.sampleVideo
    ? `<video class="video-player video-sample" controls preload="none" src="${work.sampleVideo}">브라우저가 영상 재생을 지원하지 않습니다.</video>`
    : sets
      ? sets.map((set) => carouselHTML(set, sets.length > 1)).join('')
      : '';
  const caption = work.sampleCaption
    ? `<div class="sample-caption">
        ${work.sampleCaption
          .split('\n')
          .filter(Boolean)
          .map((p) => `<p>${p}</p>`)
          .join('')}
        ${work.sampleTags ? `<p class="sample-tags">${work.sampleTags}</p>` : ''}
      </div>`
    : '';
  return `
    ${work.sampleNote ? `<p class="copy-guide">${work.sampleNote}</p>` : ''}
    <div class="sample-wrap">
      ${media}
      ${caption}
    </div>
  `;
};

const testHTML = (text) => `
  <p class="copy-guide">아래 원고를 클릭하면 복사됩니다. 사이트에 접속해 붙여넣으면 결과를 직접 확인할 수 있어요.</p>
  <div class="copy-box" role="button" tabindex="0" aria-label="테스트 원고 복사">
    <div class="copy-box-head">
      <span>테스트 원고</span>
      <span class="copy-btn" data-copy-btn>클릭하여 복사</span>
    </div>
    <div class="copy-box-text">${text}</div>
  </div>
`;

/* 값이 배열이면 번호 리스트로, 문자열이면 문단으로 표시 (줄바꿈 = 문단 나눔) */
const detailHTML = (value) =>
  Array.isArray(value)
    ? `<ol class="tab-steps">${value.map((s) => `<li>${s}</li>`).join('')}</ol>`
    : value
        .split('\n')
        .filter(Boolean)
        .map((p) => `<p>${p}</p>`)
        .join('');

/* ---------- 카테고리 ----------
   작업물 · 영상 · 실적 · 인쇄물을 한 줄 필터로 훑어볼 수 있게 한다.
   필터 대상 노드는 data-cat 을 달고, 섹션은 data-filter 를 단다.
   (섹션 안에 보이는 항목이 하나도 없으면 섹션째 숨긴다) */
const CATS = ['전체', '홈페이지', '인쇄물', '영상', 'AI 도구'];

/* works.json 에 category 가 없으면 type 으로 갈음한다 */
const workCat = (work) => work.category || (work.type === '웹 도구' ? 'AI 도구' : '홈페이지');

/* ---------- 로고 ----------
   public/logos/{슬러그}_{v·h·vw·hw}.png 규칙. 있는 파일만 골라 쓴다.
   (허브의 checkLogo 와 같은 방식 — Image 프리로드로 존재 확인) */
const logoCache = new Map();

function checkLogo(src) {
  if (logoCache.has(src)) {
    const hit = logoCache.get(src);
    return typeof hit === 'boolean' ? Promise.resolve(hit) : hit;
  }
  const p = new Promise((resolve) => {
    const img = new Image();
    img.onload = () => (logoCache.set(src, true), resolve(true));
    img.onerror = () => (logoCache.set(src, false), resolve(false));
    img.src = src;
  });
  logoCache.set(src, p);
  return p;
}

/* 컬러 로고 우선순위: 병원이 지정한 thumb → 가로 → 세로 */
async function firstLogo(slug, thumb) {
  for (const code of [...(thumb ? [thumb] : []), 'h', 'v']) {
    const src = `/logos/${slug}_${code}.png`;
    if (await checkLogo(src)) return src;
  }
  return null;
}

/* 로고 자리는 비워 두고 그린 뒤, 파일이 확인되면 채운다 */
function fillLogos(root) {
  root.querySelectorAll('[data-logo-slug]').forEach(async (box) => {
    const src = await firstLogo(box.dataset.logoSlug, box.dataset.logoThumb || '');
    if (!src) return;
    const img = new Image();
    img.loading = 'lazy';
    img.alt = box.dataset.logoAlt || '';
    img.src = src;
    box.replaceChildren(img);
    box.classList.add('has-logo');
  });
}

/* ---------- 납품 실적 ----------
   references.json 은 slug 만 적어 두면 hospitals.json 에서
   이름 · 진료과 · 대표 컬러 · 홈페이지 주소를 끌어온다. 개별 필드로 덮어쓸 수 있다.
   shot(화면 캡처) 이 들어오면 로고 자리를 캡처 이미지로 대체한다. */
const bySlug = Object.fromEntries(hospitals.map((h) => [h.slug, h]));

const resolveRef = (ref) => {
  const h = ref.slug ? bySlug[ref.slug] : null;
  return {
    slug: ref.slug || null,
    thumb: h?.thumb || '',
    name: ref.name || h?.name || '',
    dept: ref.dept || h?.dept || [],
    color: ref.color || h?.colors?.[0]?.hex || '#50C8FA',
    url: ref.url ?? h?.links?.find((l) => l.label === '홈페이지')?.url ?? null,
    year: ref.year || '',
    note: ref.note || '',
    shot: ref.shot || null,
  };
};

function refCard(ref) {
  const r = resolveRef(ref);
  const meta = [r.dept.join(' · '), r.year].filter(Boolean).join(' · ');
  const thumb = r.shot
    ? `<img class="ref-shot" src="${r.shot}" loading="lazy" alt="${r.name} 홈페이지 화면" />`
    : `<span class="ref-logo" data-logo-slug="${r.slug || ''}" data-logo-thumb="${r.thumb}" data-logo-alt="${r.name}">${
        r.slug ? '' : r.name
      }</span>`;
  const inner = `
    <span class="ref-thumb" style="--brand:${r.color}">${thumb}</span>
    <span class="ref-meta">
      <span class="ref-name">${r.name}</span>
      <span class="ref-dept">${meta}</span>
    </span>
    ${r.note ? `<span class="ref-note">${r.note}</span>` : ''}
  `;
  return r.url
    ? `<a class="ref-card" data-cat="홈페이지" href="${r.url}" target="_blank" rel="noopener noreferrer">${inner}</a>`
    : `<div class="ref-card is-flat" data-cat="홈페이지">${inner}</div>`;
}

/* 고객사 로고 월 — 브랜드 키트에 등록된 병원 전체 */
function clientLogo(h) {
  const url = h.links?.find((l) => l.label === '홈페이지')?.url;
  const inner = `<span class="client-logo" data-logo-slug="${h.slug}" data-logo-thumb="${h.thumb || ''}" data-logo-alt="${h.name}"><span class="client-name">${h.name}</span></span>`;
  return url
    ? `<a class="client-cell" href="${url}" target="_blank" rel="noopener noreferrer" title="${h.name}">${inner}</a>`
    : `<span class="client-cell" title="${h.name}">${inner}</span>`;
}

/* ---------- 인쇄물 ----------
   images 가 비어 있으면 자리(플레이스홀더)만 잡아 둔다.
   prints.json 의 images 에 경로를 넣으면 그대로 채워진다. */
function printItem(item) {
  const tiles = item.images.length
    ? item.images
        .map(
          (src, n) =>
            `<a class="print-tile" href="${src}" target="_blank" rel="noopener"><img src="${src}" loading="lazy" alt="${item.title} ${n + 1}" /></a>`
        )
        .join('')
    : Array.from({ length: 3 }, () => `<span class="print-tile empty">이미지 준비 중</span>`).join('');
  return `
    <article class="print" data-cat="인쇄물">
      <div class="print-head">
        <span class="print-title">${item.title}</span>
        <span class="print-desc">${item.description || ''}</span>
      </div>
      <div class="print-grid">${tiles}</div>
    </article>
  `;
}

const app = document.getElementById('app');

const isExternal = (url) => /^https?:\/\//.test(url);

function workItem(work, i) {
  const external = isExternal(work.url);
  const tabs = TABS.filter(([key]) => work.details?.[key]);
  if (work.sampleVideo || imageSets(work)) tabs.push([SAMPLE_TAB, '결과물 샘플']);
  if (work.testKey && manuscripts[work.testKey]) tabs.push([TEST_TAB, '테스트']);
  return `
    <article class="work" data-cat="${workCat(work)}" data-work="${i}">
      <div class="work-row" role="button" tabindex="0" aria-expanded="false" aria-controls="panel-${i}">
        <span class="work-num">${String(i + 1).padStart(2, '0')}</span>
        <span class="work-info">
          <span class="work-title">${work.title}</span>
          <span class="work-desc">${work.description || ''}</span>
        </span>
        ${work.type ? `<span class="work-type">${work.type}</span>` : ''}
        <a
          class="work-visit"
          href="${work.url}"
          ${external ? 'target="_blank" rel="noopener noreferrer"' : ''}
          aria-label="${work.title} 사이트 열기"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M7 17L17 7M17 7H9M17 7v8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </a>
        <svg class="work-chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <div class="work-panel" id="panel-${i}">
        <div class="work-panel-clip">
          <div class="work-panel-inner">
            <div class="tabs" role="tablist" aria-label="${work.title} 상세 정보">
              ${tabs
                .map(
                  ([key, label], t) =>
                    `<button class="tab${t === 0 ? ' active' : ''}" role="tab" aria-selected="${t === 0}" data-tab="${key}">${label}</button>`
                )
                .join('')}
            </div>
            <div class="tab-content" data-content>${detailHTML(work.details?.[tabs[0]?.[0]] || '')}</div>
            <a
              class="panel-visit"
              href="${work.url}"
              ${external ? 'target="_blank" rel="noopener noreferrer"' : ''}
            >사이트 바로가기
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M7 17L17 7M17 7H9M17 7v8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </a>
          </div>
        </div>
      </div>
    </article>
  `;
}

/* 영상 항목: 펼치면 플레이어가 나온다 (preload=none — 열기 전엔 내려받지 않음)
   embed 필드가 있으면 mp4 대신 HTML 연출물을 iframe으로 재생한다 (열 때만 로드) */
function videoItem(video, i) {
  const media = video.embed
    ? `<iframe class="video-embed" data-src="${video.embed}" title="${video.title}" allow="autoplay" scrolling="no"></iframe>`
    : `<video class="video-player" controls preload="none" src="${video.src}">브라우저가 영상 재생을 지원하지 않습니다.</video>`;
  return `
    <article class="work" data-cat="영상">
      <div class="work-row" role="button" tabindex="0" aria-expanded="false" aria-controls="video-panel-${i}">
        <span class="work-num">${String(i + 1).padStart(2, '0')}</span>
        <span class="work-info">
          <span class="work-title">${video.title}</span>
          <span class="work-desc">${video.description || ''}</span>
        </span>
        <svg class="work-chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <div class="work-panel" id="video-panel-${i}">
        <div class="work-panel-clip">
          <div class="work-panel-inner">
            ${media}
          </div>
        </div>
      </div>
    </article>
  `;
}

const refCount = references.length;
const clientCount = hospitals.length;

app.innerHTML = `
  <main class="portfolio">
    <header class="top">
      <img class="top-logo" src="/logos/easteregg_h.png" alt="이스터에그" />
    </header>

    <section class="hero">
      <h1 class="hero-title">작업물</h1>
      <p class="hero-sub">이스터에그 디자인팀이 만든 병의원 홈페이지와 디자인, 직접 기획해 만든 도구들입니다.<br />항목을 누르면 상세 정보가 열립니다.</p>
      <p class="hero-stat">고객사 ${clientCount}곳 · 병의원 홈페이지 ${refCount}건</p>
    </section>

    <nav class="filters" aria-label="분류 필터">
      ${CATS.map(
        (c, n) =>
          `<button class="filter${n === 0 ? ' active' : ''}" data-filter-btn="${c}" aria-pressed="${n === 0}">${c}</button>`
      ).join('')}
    </nav>

    <section class="section" data-filter aria-label="납품 실적">
      <h2 class="sec-title">납품 실적</h2>
      <p class="sec-note">실제 제작해 납품한 병의원 홈페이지입니다. 카드를 누르면 운영 중인 사이트로 이동합니다.</p>
      <div class="ref-grid">
        ${references.map(refCard).join('')}
      </div>
    </section>

    <section class="section" data-filter aria-label="고객사">
      <h2 class="sec-title">고객사</h2>
      <p class="sec-note">브랜드 키트에 등록해 관리 중인 병원 ${clientCount}곳입니다.</p>
      <div class="client-wall" data-cat="홈페이지">
        ${hospitals.map(clientLogo).join('')}
      </div>
    </section>

    <section class="section" data-filter aria-label="작업물 목록">
      <h2 class="sec-title">직접 만든 것</h2>
      <div class="works">
        ${works.map(workItem).join('')}
      </div>
    </section>

    <section class="section" data-filter aria-label="영상 목록">
      <h2 class="sec-title">영상</h2>
      <div class="works">
        ${videos.map(videoItem).join('')}
      </div>
    </section>

    <section class="section" data-filter aria-label="인쇄물">
      <h2 class="sec-title">인쇄물</h2>
      <p class="sec-note">명함 · 팝업 · 엑스배너 등 인쇄 · 배너 디자인입니다.</p>
      <div class="print-list">
        ${prints.map(printItem).join('')}
      </div>
    </section>

    <p class="works-note">원본 자료(로고 · 사업자등록증 · 병원 DB)는 전 작업물 공통으로 Google Drive에서 가져와 사용합니다.</p>
  </main>
`;

fillLogos(app);

/* ---------- 분류 필터 ---------- */
const filterButtons = [...app.querySelectorAll('[data-filter-btn]')];

function applyFilter(cat) {
  app.querySelectorAll('[data-cat]').forEach((node) => {
    node.classList.toggle('hidden', cat !== '전체' && node.dataset.cat !== cat);
  });
  app.querySelectorAll('[data-filter]').forEach((section) => {
    const items = section.querySelectorAll('[data-cat]');
    const visible = [...items].some((n) => !n.classList.contains('hidden'));
    section.classList.toggle('hidden', items.length > 0 && !visible);
  });
  filterButtons.forEach((b) => {
    const on = b.dataset.filterBtn === cat;
    b.classList.toggle('active', on);
    b.setAttribute('aria-pressed', String(on));
  });
}

filterButtons.forEach((btn) => {
  btn.addEventListener('click', () => applyFilter(btn.dataset.filterBtn));
});

/* ---------- 아코디언 (한 번에 하나만 열림) ---------- */
function setOpen(article, open) {
  article.classList.toggle('open', open);
  article.querySelector('.work-row').setAttribute('aria-expanded', String(open));
  if (!open) article.querySelector('video')?.pause();
  // iframe 연출물은 열 때 로드하고 닫으면 내려서 재생을 멈춘다
  const frame = article.querySelector('.video-embed');
  if (frame) {
    if (open && !frame.getAttribute('src')) frame.src = frame.dataset.src;
    if (!open) frame.removeAttribute('src');
  }
}

document.querySelectorAll('.work').forEach((article) => {
  const row = article.querySelector('.work-row');

  const toggle = () => {
    const willOpen = !article.classList.contains('open');
    document.querySelectorAll('.work.open').forEach((other) => setOpen(other, false));
    setOpen(article, willOpen);
  };

  row.addEventListener('click', (e) => {
    if (e.target.closest('.work-visit')) return; // 바로가기 링크는 그대로 이동
    toggle();
  });
  row.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      toggle();
    }
  });
});

/* ---------- 탭 전환 ---------- */
works.forEach((work, i) => {
  const article = document.querySelector(`[data-work="${i}"]`);
  const content = article.querySelector('[data-content]');
  article.querySelectorAll('.tab').forEach((tab) => {
    tab.addEventListener('click', () => {
      article.querySelectorAll('.tab').forEach((t) => {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
      });
      tab.classList.add('active');
      tab.setAttribute('aria-selected', 'true');
      content.innerHTML =
        tab.dataset.tab === TEST_TAB
          ? testHTML(manuscripts[work.testKey])
          : tab.dataset.tab === SAMPLE_TAB
            ? sampleHTML(work)
            : detailHTML(work.details[tab.dataset.tab] || '');
      // 샘플 탭은 이미지+텍스트 가로 배치를 위해 본문 폭 제한을 푼다
      content.classList.toggle('tab-content-wide', tab.dataset.tab === SAMPLE_TAB);
      if (tab.dataset.tab === SAMPLE_TAB) initCarousel(content);
    });
  });

  /* 원고 클릭 → 복사 (탭 전환 때마다 다시 그려지므로 위임 방식) */
  article.addEventListener('click', (e) => {
    const box = e.target.closest('.copy-box');
    if (box) copyText(manuscripts[work.testKey], box.querySelector('[data-copy-btn]'));
  });
});

/* 캐러셀: 좌우 버튼 · 스와이프로 한 장씩, 페이지 표시 갱신 (세트가 여러 개면 각각 초기화) */
function initCarousel(root) {
  root.querySelectorAll('.sample-carousel').forEach((carousel) => {
    const track = carousel.querySelector('[data-track]');
    const count = carousel.querySelector('[data-count]');
    const total = track.querySelectorAll('img').length;
    const update = () => {
      const i = Math.round(track.scrollLeft / track.clientWidth);
      count.textContent = `${Math.min(i + 1, total)} / ${total}`;
    };
    track.addEventListener('scroll', () => requestAnimationFrame(update), { passive: true });
    carousel.querySelectorAll('.carousel-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        track.scrollBy({ left: track.clientWidth * Number(btn.dataset.dir), behavior: 'smooth' });
      });
    });
    update();
  });
}

/* http 환경에서는 navigator.clipboard가 없어서 textarea 방식으로 폴백 */
function copyText(text, btn) {
  const done = () => {
    if (!btn) return;
    btn.textContent = '복사되었습니다 ✓';
    btn.classList.add('copied');
    setTimeout(() => {
      btn.textContent = '클릭하여 복사';
      btn.classList.remove('copied');
    }, 1800);
  };
  const fallback = () => {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    ta.remove();
    done();
  };
  if (navigator.clipboard?.writeText) {
    navigator.clipboard.writeText(text).then(done).catch(fallback);
  } else {
    fallback();
  }
}
