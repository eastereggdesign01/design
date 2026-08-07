import './portfolio.css';
import works from './data/works.json';
import manuscripts from './data/test-manuscripts.js';
import videos from './data/videos.json';

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

const app = document.getElementById('app');

const isExternal = (url) => /^https?:\/\//.test(url);

function workItem(work, i) {
  const external = isExternal(work.url);
  const tabs = TABS.filter(([key]) => work.details?.[key]);
  if (work.testKey && manuscripts[work.testKey]) tabs.push([TEST_TAB, '테스트']);
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

/* 영상 항목: 펼치면 플레이어가 나온다 (preload=none — 열기 전엔 내려받지 않음) */
function videoItem(video, i) {
  return `
    <article class="work">
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
            <video class="video-player" controls preload="none" src="${video.src}">
              브라우저가 영상 재생을 지원하지 않습니다.
            </video>
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

    <section aria-label="영상 목록">
      <h2 class="sec-title">영상</h2>
      <div class="works">
        ${videos.map(videoItem).join('')}
      </div>
    </section>

    <p class="works-note">원본 자료(로고 · 사업자등록증 · 병원 DB)는 전 작업물 공통으로 Google Drive에서 가져와 사용합니다.</p>
  </main>
`;

/* ---------- 아코디언 (한 번에 하나만 열림) ---------- */
function setOpen(article, open) {
  article.classList.toggle('open', open);
  article.querySelector('.work-row').setAttribute('aria-expanded', String(open));
  if (!open) article.querySelector('video')?.pause();
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
          : detailHTML(work.details[tab.dataset.tab] || '');
    });
  });

  /* 원고 클릭 → 복사 (탭 전환 때마다 다시 그려지므로 위임 방식) */
  article.addEventListener('click', (e) => {
    const box = e.target.closest('.copy-box');
    if (box) copyText(manuscripts[work.testKey], box.querySelector('[data-copy-btn]'));
  });
});

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
