/* =====================================================================
   스크롤 등장 모션 (선택) · 붙여넣는 곳: 코드 삽입 → body 닫는 태그 직전
   형식: script 태그로 감싸서 (여는 태그 … 이 파일 전체 … 닫는 태그)
   ===================================================================== */
(function () {
  if (!('IntersectionObserver' in window)) return;
  document.documentElement.classList.add('eg-js');
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });
  function bind() {
    document.querySelectorAll('.eg-reveal:not(.is-in)').forEach(function (el, i) {
      el.style.transitionDelay = Math.min(i % 6, 5) * 60 + 'ms';
      io.observe(el);
    });
  }
  bind();
  // 아임웹이 위젯을 지연 렌더링할 때를 대비해 한 번 더
  window.addEventListener('load', bind);
})();
