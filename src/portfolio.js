import './portfolio.css';
import works from './data/works.json';

/* 작업물 추가 = src/data/works.json 배열에 항목 하나 추가.
   { title, description, type, url, details: { tools, intent, method, test } }
   details의 키 중 있는 것만 탭으로 표시된다. */

const TABS = [
  ['tools', '사용 툴'],
  ['intent', '기획의도'],
  ['method', '제작방법'],
  ['test', '테스트 방법'],
];

/* 값이 배열이면 번호 리스트로, 문자열이면 문단으로 표시 (줄바꿈 = 문단 나눔) */
const detailHTML = (value) =>
  Array.isArray(value)
    ? `<ol class="tab-steps">${value.map((s) => `<li>${s}</li>`).join('')}</ol>`
    : value
        .split('\n')
        .filter(Boolean)
        .map((p) => `<p>${p}</p>`)
        .join('');

const app = document.getElementById('app');

const isExternal = (url) => /^https?:\/\//.test(url);

function workItem(work, i) {
  const external = isExternal(work.url);
  const tabs = TABS.filter(([key]) => work.details?.[key]);
  return `
    <article class="work" data-work="${i}">
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

app.innerHTML = `
  <main class="portfolio">
    <header class="top">
      <img class="top-logo" src="/logos/easteregg_h.png" alt="이스터에그" />
    </header>

    <section class="hero">
      <h1 class="hero-title">작업물</h1>
      <p class="hero-sub">직접 기획하고 만든 웹사이트와 도구들입니다.<br />항목을 누르면 상세 정보가 열립니다.</p>
    </section>

    <section class="works" aria-label="작업물 목록">
      ${works.map(workItem).join('')}
    </section>

    <p class="works-note">원본 자료(로고 · 사업자등록증 · 병원 DB)는 전 작업물 공통으로 Google Drive에서 가져와 사용합니다.</p>
  </main>
`;

/* ---------- 아코디언 (한 번에 하나만 열림) ---------- */
function setOpen(article, open) {
  article.classList.toggle('open', open);
  article.querySelector('.work-row').setAttribute('aria-expanded', String(open));
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
      content.innerHTML = detailHTML(work.details[tab.dataset.tab] || '');
    });
  });
});
