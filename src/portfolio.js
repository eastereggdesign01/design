import './portfolio.css';
import works from './data/works.json';

/* 작업물 추가 = src/data/works.json 배열에 항목 하나 추가.
   { emoji, title, description, tags, url } — url이 http로 시작하면 새 탭으로 연다. */

const app = document.getElementById('app');

const isExternal = (url) => /^https?:\/\//.test(url);

function workCard(work) {
  const external = isExternal(work.url);
  return `
    <a
      class="work-card"
      href="${work.url}"
      ${external ? 'target="_blank" rel="noopener noreferrer"' : ''}
      aria-label="${work.title} 사이트로 이동"
    >
      <div class="work-emoji" aria-hidden="true">${work.emoji || '✨'}</div>
      <div class="work-body">
        <h2 class="work-title">${work.title}</h2>
        <p class="work-desc">${work.description || ''}</p>
        ${
          work.tags?.length
            ? `<div class="work-tags">${work.tags.map((t) => `<span class="tag">${t}</span>`).join('')}</div>`
            : ''
        }
      </div>
      <div class="work-go">
        <span>바로가기</span>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M5 12h14M13 5l7 7-7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
    </a>
  `;
}

app.innerHTML = `
  <div class="bg-glow" aria-hidden="true"></div>
  <main class="portfolio">
    <header class="hero">
      <p class="hero-eyebrow">EASTER EGG · WORKS</p>
      <h1 class="hero-title">이스터에그 작업물 모음</h1>
      <p class="hero-sub">직접 만든 프로젝트들입니다. 버튼을 누르면 해당 사이트로 이동합니다.</p>
    </header>

    <section class="works" aria-label="작업물 목록">
      ${works.map(workCard).join('')}
    </section>

    <footer class="foot">
      <span>© ${new Date().getFullYear()} Easter Egg</span>
      <a href="mailto:easteregg.design01@gmail.com">easteregg.design01@gmail.com</a>
    </footer>
  </main>
`;
