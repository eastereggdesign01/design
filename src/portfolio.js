import './portfolio.css';
import works from './data/works.json';
import company from './data/company.json';

/* 작업물 추가 = src/data/works.json 배열에 항목 하나 추가.
   { title, description, type, url } — url이 http로 시작하면 새 탭으로 연다. */

const app = document.getElementById('app');

const isExternal = (url) => /^https?:\/\//.test(url);

function workRow(work, i) {
  const external = isExternal(work.url);
  return `
    <a
      class="work-row"
      href="${work.url}"
      ${external ? 'target="_blank" rel="noopener noreferrer"' : ''}
    >
      <span class="work-num">${String(i + 1).padStart(2, '0')}</span>
      <span class="work-info">
        <span class="work-title">${work.title}</span>
        <span class="work-desc">${work.description || ''}</span>
      </span>
      ${work.type ? `<span class="work-type">${work.type}</span>` : ''}
      <svg class="work-arrow" width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M7 17L17 7M17 7H9M17 7v8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </a>
  `;
}

app.innerHTML = `
  <main class="portfolio">
    <header class="top">
      <img class="top-logo" src="/logos/easteregg_h.png" alt="이스터에그" />
      <a class="top-mail" href="mailto:easteregg.design01@gmail.com">easteregg.design01@gmail.com</a>
    </header>

    <section class="hero">
      <h1 class="hero-title">작업물</h1>
      <p class="hero-sub">직접 기획하고 만든 웹사이트와 도구들입니다.<br />항목을 누르면 해당 사이트가 열립니다.</p>
    </section>

    <section class="works" aria-label="작업물 목록">
      ${works.map(workRow).join('')}
    </section>

    <footer class="foot">
      <div class="foot-links">
        ${(company.links || [])
          .map(
            (l) =>
              `<a href="${l.url}" target="_blank" rel="noopener noreferrer">${l.label}</a>`
          )
          .join('<span class="foot-dot">·</span>')}
      </div>
      <span>© ${new Date().getFullYear()} 이스터에그</span>
    </footer>
  </main>
`;
