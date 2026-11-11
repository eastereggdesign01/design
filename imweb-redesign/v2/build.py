#!/usr/bin/env python3
"""이스터에그 자사 홈페이지 v2 — 4페이지 정적 사이트 생성기.
python3 build.py  →  index.html / marketing.html / design.html / contact.html / style.css
원고 출처: ../기획안-v2.md, ../마케팅-업무-공개용-정리.md
"""
import pathlib
OUT = pathlib.Path(__file__).resolve().parent

CSS = r"""
@font-face{font-family:'Pretendard';font-weight:400;font-display:swap;src:url('fonts/Pretendard-Regular.woff2') format('woff2')}
@font-face{font-family:'Pretendard';font-weight:500;font-display:swap;src:url('fonts/Pretendard-Medium.woff2') format('woff2')}
@font-face{font-family:'Pretendard';font-weight:600;font-display:swap;src:url('fonts/Pretendard-SemiBold.woff2') format('woff2')}
@font-face{font-family:'Pretendard';font-weight:700;font-display:swap;src:url('fonts/Pretendard-Bold.woff2') format('woff2')}
:root{--ink:#1d1d1f;--sub:#6e6e73;--line:#e8e8ed;--bg:#fff;--bg2:#f5f5f7;--dark:#0b0f14;--blue:#0f9bd6;--sky:#50c8fa;--wrap:1120px;--gutter:24px}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{font-family:'Pretendard',-apple-system,BlinkMacSystemFont,system-ui,sans-serif;color:var(--ink);background:var(--bg);line-height:1.5;-webkit-font-smoothing:antialiased;word-break:keep-all;letter-spacing:-0.01em}
a{color:inherit;text-decoration:none}
img{max-width:100%;display:block}
.wrap{max-width:var(--wrap);margin:0 auto;padding:0 var(--gutter)}
.narrow{max-width:760px;margin:0 auto}
section{padding:140px 0}
section.tight{padding:96px 0}
.bg2{background:var(--bg2)}
.dark{background:var(--dark);color:#fff}
.dark .sub,.dark .eyebrow{color:rgba(255,255,255,.6)}
.center{text-align:center}
/* type */
h1{font-size:clamp(42px,6vw,76px);font-weight:700;letter-spacing:-0.035em;line-height:1.06}
h2{font-size:clamp(32px,4.2vw,54px);font-weight:700;letter-spacing:-0.03em;line-height:1.1}
h3{font-size:clamp(22px,2.4vw,28px);font-weight:600;letter-spacing:-0.02em;line-height:1.25}
.lead{font-size:clamp(18px,1.8vw,22px);line-height:1.55;color:var(--sub);font-weight:400;margin-top:20px}
.sub{font-size:17px;line-height:1.65;color:var(--sub)}
.eyebrow{font-size:14px;font-weight:600;color:var(--blue);letter-spacing:.02em;margin-bottom:16px;display:block}
.head{max-width:760px;margin:0 auto 64px;text-align:center}
.head.left{margin-left:0;text-align:left}
.blue{color:var(--blue)}
.dark .blue{color:var(--sky)}
/* buttons */
.btn{display:inline-flex;align-items:center;gap:8px;height:50px;padding:0 24px;border-radius:999px;font-size:16px;font-weight:500;background:var(--ink);color:#fff;transition:transform .15s,opacity .15s}
.btn:hover{opacity:.85;transform:translateY(-1px)}
.btn.light{background:#fff;color:var(--ink)}
.btn.outline{background:transparent;border:1px solid var(--line);color:var(--ink)}
.dark .btn.outline{border-color:rgba(255,255,255,.3);color:#fff}
.link{font-size:17px;font-weight:500;color:var(--blue)}
.link::after{content:' ›'}
.actions{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:36px}
/* nav */
nav{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.8);backdrop-filter:saturate(180%) blur(20px);-webkit-backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid rgba(0,0,0,.06)}
nav .wrap{height:52px;display:flex;align-items:center;gap:32px}
nav .logo{font-weight:700;font-size:17px;letter-spacing:-0.02em}
nav .logo b{color:var(--blue)}
nav .menu{display:flex;gap:28px;margin-left:auto;font-size:14px;color:#424245}
nav .menu a.on{color:var(--ink);font-weight:600}
nav .cta{height:34px;padding:0 16px;font-size:13px;font-weight:600;border-radius:999px;background:var(--ink);color:#fff;display:inline-flex;align-items:center}
/* stage: product-shot container */
.stage{background:var(--bg2);border-radius:28px;padding:clamp(28px,5vw,72px);display:flex;align-items:center;justify-content:center;overflow:hidden}
.card{background:#fff;border-radius:20px;box-shadow:0 1px 2px rgba(0,0,0,.04),0 24px 60px -20px rgba(0,0,0,.18);padding:28px;width:100%}
.card.sm{padding:22px;border-radius:16px}
/* grids */
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}
.split{display:grid;grid-template-columns:1fr 1fr;gap:72px;align-items:center}
/* tiles */
.tile{background:var(--bg2);border-radius:28px;padding:44px;display:flex;flex-direction:column;min-height:520px;transition:transform .2s}
.tile:hover{transform:translateY(-4px)}
.tile .visual{flex:1;display:flex;align-items:center;justify-content:center;margin:32px 0}
.tile h3{font-size:30px}
.tile .tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:16px}
.tag{font-size:13px;padding:6px 12px;border-radius:999px;background:#fff;border:1px solid var(--line);color:#424245}
.dark .tag{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.12);color:rgba(255,255,255,.85)}
/* list rows */
.rows{border-top:1px solid var(--line)}
.row{display:grid;grid-template-columns:72px 1fr;gap:24px;padding:32px 0;border-bottom:1px solid var(--line)}
.row .n{font-size:15px;font-weight:600;color:var(--blue);padding-top:5px}
.row h3{font-size:24px}
.row p{margin-top:10px;color:var(--sub);font-size:17px;line-height:1.6}
.dark .rows,.dark .row{border-color:rgba(255,255,255,.12)}
/* quotes */
.bubble{background:#fff;border-radius:20px;padding:24px 26px;font-size:19px;font-weight:500;line-height:1.45;position:relative}
.bubble small{display:block;margin-top:12px;font-size:13px;color:var(--sub);font-weight:400}
/* journey chips */
.journey{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin-top:40px}
.journey span{padding:12px 20px;border-radius:999px;background:#fff;border:1px solid var(--line);font-size:16px;font-weight:500;color:var(--sub)}
.journey span.hot{background:var(--ink);color:#fff;border-color:var(--ink)}
.journey i{align-self:center;color:#c7c7cc;font-style:normal}
/* mock ui bits */
.mock{font-size:13px;color:#424245}
.mock .t{font-size:12px;font-weight:600;color:var(--sub);letter-spacing:.04em;text-transform:uppercase}
.mock .h{font-size:20px;font-weight:700;letter-spacing:-0.02em;margin-top:6px}
.mock .kv{display:flex;justify-content:space-between;align-items:baseline;padding:12px 0;border-bottom:1px solid var(--line)}
.mock .kv:last-child{border-bottom:0}
.mock .kv b{font-size:22px;font-weight:700;letter-spacing:-0.02em}
.mock .up{color:#1a9e5a;font-weight:600}
.mock .rank{display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:10px}
.mock .rank.on{background:#e9f7fe}
.mock .rank b{width:22px;height:22px;border-radius:50%;background:#fff;border:1px solid var(--line);display:inline-flex;align-items:center;justify-content:center;font-size:12px}
.mock .rank.on b{background:var(--blue);border-color:var(--blue);color:#fff}
.mock .note{margin-top:14px;padding:14px;border-radius:12px;background:var(--bg2);font-size:13.5px;line-height:1.5;color:#424245}
.big{font-size:clamp(44px,5vw,64px);font-weight:700;letter-spacing:-0.035em;line-height:1}
.big small{font-size:.45em;font-weight:600;color:var(--sub);margin-left:4px;letter-spacing:0}
/* checklist */
.check{list-style:none;display:grid;gap:14px}
.check li{display:flex;gap:14px;font-size:18px;line-height:1.5}
.check li::before{content:'';flex:none;width:22px;height:22px;border-radius:50%;background:var(--ink);margin-top:4px;-webkit-mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='12' fill='black'/%3E%3Cpath d='M7 12.5l3.2 3.2L17 9' stroke='white' stroke-width='2.2' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/contain no-repeat;mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='12' fill='black'/%3E%3Cpath d='M7 12.5l3.2 3.2L17 9' stroke='white' stroke-width='2.2' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/contain no-repeat}
.dark .check li::before{background:var(--sky)}
/* table */
table.clean{width:100%;border-collapse:collapse;font-size:17px}
table.clean th,table.clean td{text-align:left;padding:18px 12px;border-bottom:1px solid var(--line);vertical-align:top}
table.clean th{font-weight:600;color:var(--sub);font-size:14px;letter-spacing:.02em}
table.clean td:first-child{font-weight:600;white-space:nowrap}
table.clean td.g{color:var(--blue);font-weight:600;white-space:nowrap}
/* cta band */
.cta{padding:120px 0}
.cta h2{font-size:clamp(30px,4vw,48px)}
/* footer */
footer{padding:56px 0 40px;border-top:1px solid var(--line);font-size:13px;color:var(--sub);line-height:1.8}
footer .cols{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;margin-bottom:28px}
footer .cols a{margin-right:20px;color:#424245;font-weight:500}
footer b{color:var(--ink);font-weight:600}
/* form */
.form{display:grid;gap:18px}
.form label{display:block;font-size:14px;font-weight:600;margin-bottom:8px}
.form input,.form select,.form textarea{width:100%;height:50px;border:1px solid var(--line);border-radius:12px;padding:0 16px;font:inherit;font-size:16px;background:#fff}
.form textarea{height:140px;padding:14px 16px;resize:vertical}
.form input:focus,.form select:focus,.form textarea:focus{outline:none;border-color:var(--ink)}
.form .two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.form .radios{display:flex;gap:8px}
.form .radios label{display:inline-flex;align-items:center;gap:8px;height:44px;padding:0 16px;border:1px solid var(--line);border-radius:999px;font-weight:500;margin:0;cursor:pointer}
.form .agree{font-size:14px;color:var(--sub);font-weight:400;display:flex;align-items:center;gap:8px}
.form .btn{width:100%;height:54px;justify-content:center}
/* faq */
details{border-bottom:1px solid var(--line)}
details summary{list-style:none;cursor:pointer;padding:22px 0;font-size:19px;font-weight:600;display:flex;justify-content:space-between;align-items:center}
details summary::-webkit-details-marker{display:none}
details summary::after{content:'+';font-weight:400;color:var(--sub);font-size:22px}
details[open] summary::after{content:'−'}
details p{padding:0 0 22px;color:var(--sub);font-size:17px;line-height:1.65;max-width:680px}
/* reveal */
.r{opacity:0;transform:translateY(16px);transition:opacity .7s ease,transform .7s ease}
.r.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.r{opacity:1;transform:none;transition:none}}
/* banner mock */
.xb{width:150px;height:380px;border-radius:6px;background:linear-gradient(#111,#1d1d1f);color:#fff;padding:22px 16px;display:flex;flex-direction:column;box-shadow:0 30px 50px -24px rgba(0,0,0,.5);position:relative}
.xb::before,.xb::after{content:'';position:absolute;width:6px;height:6px;border-radius:50%;background:#fff;opacity:.5;top:8px;left:8px}
.xb::after{left:auto;right:8px}
.xb .top{font-size:11px;color:var(--sky);font-weight:600}
.xb .main{font-size:26px;font-weight:700;line-height:1.1;letter-spacing:-0.02em;margin-top:10px}
.xb .foot{margin-top:auto;font-size:11px;color:rgba(255,255,255,.7)}
.print{background:#fff;border-radius:10px;box-shadow:0 10px 30px -14px rgba(0,0,0,.25);padding:16px;font-size:11px;color:#6e6e73;display:flex;flex-direction:column;gap:6px}
.print b{color:var(--ink);font-size:12px}
.print i{display:block;height:6px;border-radius:3px;background:#eaeaef}
.chat{display:grid;gap:10px;max-width:420px}
.chat .m{padding:12px 16px;border-radius:18px;font-size:15px;line-height:1.45;max-width:85%}
.chat .m.us{background:var(--blue);color:#fff;justify-self:end;border-bottom-right-radius:6px}
.chat .m.dr{background:#fff;border:1px solid var(--line);border-bottom-left-radius:6px}
@media (max-width:860px){
  section{padding:88px 0}
  .grid2,.grid3,.grid4,.split{grid-template-columns:1fr}
  .split{gap:36px}
  .tile{min-height:0;padding:28px}
  .row{grid-template-columns:48px 1fr;gap:14px;padding:24px 0}
  nav .menu{display:none}
  .head{margin-bottom:40px}
  .form .two{grid-template-columns:1fr}
  table.clean{font-size:15px}
  table.clean th,table.clean td{padding:12px 8px}
}
"""

JS = """
(function(){if(!('IntersectionObserver' in window))return;var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.08,rootMargin:'0px 0px -8% 0px'});document.querySelectorAll('.r').forEach(function(el,i){el.style.transitionDelay=(i%4)*60+'ms';io.observe(el)})})();
"""

def nav(active):
    items = [('marketing.html','마케팅'),('design.html','디자인'),('#','247'),('contact.html','문의')]
    m = ''.join(f'<a href="{h}" class="{"on" if h==active else ""}">{t}</a>' for h,t in items)
    return f'''<nav><div class="wrap"><a class="logo" href="index.html">이스터에그<b>.</b></a><div class="menu">{m}</div><a class="cta" href="contact.html">상담 문의</a></div></nav>'''

def cta():
    return '''<section class="cta dark"><div class="wrap center"><h2 class="r">우리 병원에 맞는 방법이 궁금하다면,<br>30분 진단 미팅부터.</h2><p class="lead r">현재 네이버 노출 상태와 유입 경로를 보고, 지금 바꾸면 효과가 큰 것 세 가지를 먼저 말씀드립니다.</p><div class="actions r"><a class="btn light" href="contact.html">상담 문의하기</a><a class="btn outline" href="tel:032-710-2258">032-710-2258</a></div></div></section>'''

def footer():
    return '''<footer><div class="wrap"><div class="cols"><div><b>이스터에그</b> &nbsp; 병의원 전문 마케팅 · 디자인</div><div><a href="marketing.html">마케팅</a><a href="design.html">디자인</a><a href="#">247</a><a href="contact.html">문의</a><a href="https://design.easteregg247.com/" target="_blank" rel="noopener">포트폴리오</a><a href="https://blog.naver.com/easteregg_blog" target="_blank" rel="noopener">블로그</a></div></div>
<div><b>주식회사 이스터에그</b> · 대표 김소연 · 사업자등록번호 116-86-02909 · 통신판매업신고 2024-충북청주-0953<br>본사 충청북도 청주시 청원구 오창읍 오창중앙로 123-12, 1동 402호 C23호 · 인천지사 인천 연수구 인천타워대로 323, 송도센트로드 A동 1811호<br>TEL 032-710-2258 · easteregg.medi@gmail.com · <a href="#">개인정보처리방침</a><br>© 2026 Easter Egg Inc.</div></div></footer>'''

def page(title, desc, active, body):
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><meta name="description" content="{desc}"><link rel="stylesheet" href="style.css"></head><body>{nav(active)}{body}{cta()}{footer()}<script>{JS}</script></body></html>'''

# ---------- 차트 ----------
def chart_growth():
    # B병원: 첫 달 2,000 → 매달 +1,000 → 2022.11 4,103 (팜플렛 p.13 기준 근사)
    pts=[(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0.15),(7,0.5),(8,0.68),(9,0.8),(10,0.9),(11,1.0)]
    W,H=520,200
    d=' '.join(f'{"M" if i==0 else "L"}{20+x*(W-40)/11:.0f},{H-20-y*(H-50):.0f}' for i,(x,y) in enumerate(pts))
    return f'''<svg viewBox="0 0 {W} {H}" width="100%" style="display:block"><path d="{d}" fill="none" stroke="#1d1d1f" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="{W-20}" cy="30" r="5" fill="#0f9bd6"/><text x="{W-26}" y="22" font-size="13" font-weight="700" text-anchor="end" fill="#1d1d1f">4,103명</text><g font-size="11" fill="#6e6e73"><text x="20" y="{H-4}">11월</text><text x="{W/2:.0f}" y="{H-4}" text-anchor="middle">개원</text><text x="{W-20}" y="{H-4}" text-anchor="end">11월</text></g></svg>'''

def chart_compare():
    a=[139,148,210,125,173]; b=[217,188,235,200,212]
    W,H=520,200; lo,hi=100,250
    def path(v): return ' '.join(f'{"M" if i==0 else "L"}{40+i*(W-80)/4:.0f},{H-30-(x-lo)/(hi-lo)*(H-60):.0f}' for i,x in enumerate(v))
    labels=''.join(f'<text x="{40+i*(W-80)/4:.0f}" y="{H-8}" font-size="11" fill="#6e6e73" text-anchor="middle">{i+1}월</text>' for i in range(5))
    return f'''<svg viewBox="0 0 {W} {H}" width="100%" style="display:block"><path d="{path(a)}" fill="none" stroke="#c7c7cc" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><path d="{path(b)}" fill="none" stroke="#0f9bd6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>{labels}<g font-size="12" font-weight="600"><text x="{W-40}" y="{H-30-(212-lo)/(hi-lo)*(H-60)-10:.0f}" text-anchor="end" fill="#0f9bd6">2024</text><text x="{W-40}" y="{H-30-(173-lo)/(hi-lo)*(H-60)+18:.0f}" text-anchor="end" fill="#8e8e93">2023</text></g></svg>'''

# ---------- 메인 ----------
def index():
    hero = f'''<section style="padding-top:96px;padding-bottom:0"><div class="wrap center"><h1>홍보, 신환, 매출에 대한<br>'고민'은 저희가 하겠습니다.</h1><p class="lead narrow">인천 송도의 병의원 전문 마케팅 · 디자인 팀. 검색에서 먼저 보이게 하고, 매달 숫자마다 이유와 다음 달 계획을 함께 드립니다.</p><div class="actions"><a class="btn" href="contact.html">상담 문의하기</a><a class="link" href="marketing.html" style="display:inline-flex;align-items:center;padding:0 8px">어떻게 일하는지 보기</a></div></div>
<div class="wrap r" style="margin-top:72px"><div class="stage" style="padding-bottom:0;border-radius:28px 28px 0 0"><div class="card mock" style="max-width:720px;border-radius:20px 20px 0 0;box-shadow:0 -1px 0 rgba(0,0,0,.02),0 -30px 80px -40px rgba(0,0,0,.2)"><div class="t">10월 성과 보고서 · OO외과</div><div class="h">이번 달, 플레이스 유입이 늘었습니다.</div><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:18px"><div class="kv" style="display:block;border:1px solid var(--line);border-radius:12px;padding:14px"><div class="t">메인 키워드 · PC</div><b>1위</b></div><div class="kv" style="display:block;border:1px solid var(--line);border-radius:12px;padding:14px"><div class="t">메인 키워드 · 모바일</div><b>1위</b></div><div class="kv" style="display:block;border:1px solid var(--line);border-radius:12px;padding:14px"><div class="t">플레이스 유입</div><b>892 <span class="up" style="font-size:13px">+62%</span></b></div></div><div class="note"><b>핵심 코멘트</b> &nbsp;① 블로그 지역 키워드 3개가 1페이지에 들어오면서 지도 유입이 함께 올랐습니다. ② 다음 달은 비수기 진입 전이라 양성종양 키워드를 보강합니다. ③ 결정 필요: 일요일 진료 노출 여부.</div></div></div></div></section>'''
    greet = '''<section class="bg2"><div class="wrap"><div class="head"><span class="eyebrow">원장님은 '진료'에만 집중하세요</span><h2>환자는 일곱 단계를 거쳐<br>병원을 고릅니다.</h2><p class="lead">사거리에 현수막만 걸면 환자가 찾아오던 시대는 끝났습니다. 우리 병원은 이 여정의 어디에 닻을 내려야 할까요?</p></div><div class="journey r"><span>주의</span><i>›</i><span>흥미</span><i>›</i><span class="hot">검색</span><i>›</i><span class="hot">비교</span><i>›</i><span class="hot">검토</span><i>›</i><span>구매</span><i>›</i><span>공유</span></div><p class="sub center r" style="max-width:720px;margin:56px auto 0;font-size:19px;line-height:1.7">"5년 전에 개원한 선배 병원은 이렇게 했더니 잘됐다"는 말은 마케팅 트렌드가 두세 번 바뀐 구전에 가깝습니다. 기존에 하던 대로 반복하는 것이 아니라, <b style="color:var(--ink)">지금 이 시점에 가장 유효한 방법을 찾아드리는 것</b>이 마케팅 회사의 존재 가치라고 믿습니다.</p></div></section>'''
    what = f'''<section><div class="wrap"><div class="head"><h2>우리가 하는 일은<br>두 가지입니다.</h2><p class="lead">병원이 검색에서 보이게 만드는 일, 그리고 그 병원이 어떻게 보일지 만드는 일.</p></div><div class="grid2">
<a class="tile r" href="marketing.html"><span class="eyebrow">Marketing</span><h3>검색 결과에서<br>먼저 보이게.</h3><div class="visual"><div class="card sm mock" style="max-width:360px"><div class="rank on"><b>1</b><span>강남구 외과</span></div><div class="rank"><b>2</b><span>강남 항문외과</span></div><div class="rank"><b>3</b><span>역삼 치질</span></div><div class="note" style="margin-top:10px">지역 + 진료과 메인 키워드 1페이지</div></div></div><div class="tags"><span class="tag">네이버 플레이스</span><span class="tag">공식 블로그</span><span class="tag">키워드 전략</span><span class="tag">검색광고</span><span class="tag">리뷰 관리</span><span class="tag">월간 보고서</span></div><span class="link" style="margin-top:20px">자세히 보기</span></a>
<a class="tile r" href="design.html"><span class="eyebrow">Design</span><h3>병원마다<br>다르게 만듭니다.</h3><div class="visual"><div style="display:flex;gap:16px;align-items:flex-end"><div class="xb" style="transform:rotate(-4deg)"><div class="top">OO정형외과</div><div class="main">B동 4층<br>엘리베이터를<br>이용해 주세요</div><div class="foot">T. 032-000-0000</div></div><div class="print" style="width:150px;height:200px"><b>접수증</b><i></i><i style="width:70%"></i><i></i><i style="width:50%"></i><span style="margin-top:auto">OO외과</span></div></div></div><div class="tags"><span class="tag">홈페이지</span><span class="tag">엑스배너</span><span class="tag">접수증</span><span class="tag">명함</span><span class="tag">포스터</span><span class="tag">전단지</span><span class="tag">안내문</span></div><span class="link" style="margin-top:20px">자세히 보기</span></a></div></div></section>'''
    cases = f'''<section class="bg2"><div class="wrap"><div class="head"><span class="eyebrow">우리 병원이라면 어떨까?</span><h2>말 대신 숫자로.</h2><p class="lead">어렵게 설명하지 않고 세 가지 사례를 먼저 보여드립니다.</p></div><div class="grid3">
<div class="card r"><div class="mock t">부천 B병원 · 외과</div><h3 style="margin-top:10px">한 번 망한 자리에서도<br>개원 3주 전 선점.</h3><div style="margin:24px 0 8px">{chart_growth()}</div><div class="big">4,103<small>명 / 월</small></div><p class="sub" style="margin-top:8px">블로그 순방문자. 45개 키워드를 개원 3주 전부터 노출.</p></div>
<div class="card r"><div class="mock t">S병원 · 외과</div><h3 style="margin-top:10px">원장님의 철학을<br>콘텐츠로 전달.</h3><div style="margin:24px 0 8px">{chart_compare()}</div><div class="big">1<small>위 메인 키워드</small></div><p class="sub" style="margin-top:8px">1~5월 신환, 전년 같은 달 대비 전 구간 증가.</p></div>
<div class="card r"><div class="mock t">Y병원 · 정형외과</div><h3 style="margin-top:10px">모든 프로젝트를<br>성공시킨 것은 아닙니다.</h3><p class="sub" style="margin-top:24px;line-height:1.7">H병원은 상단 노출이 잘 되는데도 3개월간 성과가 없었습니다. 원인은 연령대. 노인 인구가 많은 지역이라 온라인만으로는 한계가 있었습니다.</p><p class="sub" style="margin-top:12px;line-height:1.7">그 경험으로 Y병원은 지역 연령대를 먼저 조사하고, 엘리베이터·버스 정류장·지하철역 광고를 함께 썼습니다.</p><div class="tags" style="margin-top:20px"><span class="tag">온라인</span><span class="tag">+ 오프라인</span><span class="tag">연령대 조사</span></div></div></div><p class="center r" style="margin-top:40px"><a class="link" href="marketing.html#cases">사례 자세히 보기</a></p></div></section>'''
    voice = '''<section><div class="wrap"><div class="head"><span class="eyebrow">똑똑한 마케팅만 했을 뿐입니다</span><h2>재계약률 95%</h2></div><div class="grid2" style="max-width:900px;margin:0 auto"><div class="bubble r" style="background:var(--bg2)">"신환이 많이 늘었어요!"<small>OO외과 원장</small></div><div class="bubble r" style="background:var(--bg2)">"지인에게 추천하고 싶은데 OO과도 마케팅 하시나요?"<small>OO정형외과 원장</small></div><div class="bubble r" style="background:var(--bg2)">"바로 처리해주셔서 큰 도움이 됩니다."<small>OO의원 실장</small></div><div class="bubble r" style="background:var(--bg2)">"발전하는 병원 이미지 구축 정말 감사합니다!"<small>OO외과 원장</small></div></div></div></section>'''
    promise = '''<section class="dark"><div class="wrap"><div class="head"><h2>마케팅 다 똑같단 편견,<br><span class="blue">이스터에그로 깨트려보세요.</span></h2><p class="lead">계약 전에 먼저 드리는, 여섯 가지 약속.</p></div><div class="grid3">
<div class="r"><div class="eyebrow">01</div><h3>담당자 공백이 없습니다</h3><p class="sub" style="margin-top:8px">병원마다 담당자와 서브담당자가 있고 팀장이 전체를 봅니다.</p></div>
<div class="r"><div class="eyebrow">02</div><h3>숫자에는 이유가 붙습니다</h3><p class="sub" style="margin-top:8px">왜 늘고 줄었는지, 다음 달엔 무엇을 바꿀지를 함께 보고합니다.</p></div>
<div class="r"><div class="eyebrow">03</div><h3>의료법을 먼저 봅니다</h3><p class="sub" style="margin-top:8px">글 하나가 나가기 전에 다섯 가지 기준으로 검수합니다.</p></div>
<div class="r"><div class="eyebrow">04</div><h3>한 채널만 보고 판단하지 않습니다</h3><p class="sub" style="margin-top:8px">블로그·플레이스·광고·신환을 나눠 보고 합쳐서 진단합니다.</p></div>
<div class="r"><div class="eyebrow">05</div><h3>범위를 미리 말씀드립니다</h3><p class="sub" style="margin-top:8px">할 수 있는 것과 없는 것을 계약 전에 적어 드립니다.</p></div>
<div class="r"><div class="eyebrow">06</div><h3>비수기는 전년과 비교합니다</h3><p class="sub" style="margin-top:8px">전월 단순 비교로 성과를 포장하지 않습니다.</p></div></div><p class="sub center" style="margin-top:48px;font-size:13px;opacity:.6">※ 여섯 가지 약속 문장은 초안입니다. 현재 사이트 문장으로 교체 예정.</p></div></section>'''
    return page('이스터에그 | 병원 마케팅 에이전시, 인천 송도','마케팅과 디자인 한 팀이 병원의 방향을 기획하고 실행합니다. 숫자마다 설명이 붙는 월간 리포트. 032-710-2258','index.html', hero+greet+what+cases+voice+promise)

# ---------- 마케팅 ----------
def marketing():
    hero = '''<section style="padding-top:96px;padding-bottom:0"><div class="wrap center"><span class="eyebrow">Marketing</span><h1>검색 결과에서<br>먼저 보이게.</h1><p class="lead narrow">네이버 플레이스, 공식 블로그, 검색광고, 리뷰까지 한 사람이 끝까지 맡습니다. 매달 숫자와 이유, 다음 달 계획을 보고서로 드립니다.</p><div class="actions"><a class="btn" href="contact.html">상담 문의하기</a></div></div></section>'''
    secretary = '''<section><div class="wrap"><div class="split"><div><span class="eyebrow">Hi, easteregg!</span><h2>우리 병원만의<br>마케팅 비서</h2><p class="lead">여러 전문가가 우리 병원을 전담하는 소통 방식으로, 똑똑한 비서의 특별 관리를 받는 것처럼 진행합니다.</p><p class="sub" style="margin-top:24px">병원마다 담당자와 서브담당자가 있고 팀장이 전체를 봅니다. 담당자가 자리를 비워도 업무는 멈추지 않습니다.</p></div><div class="rows r"><div class="row"><div class="n">01</div><div><h3>빠른 대응</h3><p>문의는 담당자가 바로 받습니다.</p></div></div><div class="row"><div class="n">02</div><div><h3>해결책을 제시하는 결과 보고</h3><p>숫자 나열이 아니라, 원인과 다음 행동까지.</p></div></div><div class="row"><div class="n">03</div><div><h3>병원 모니터링</h3><p>리뷰, 경쟁 병원, 검색 순위를 매주 봅니다.</p></div></div><div class="row"><div class="n">04</div><div><h3>A/B식 제안</h3><p>고민을 줄여드리기 위해 선택지를 둘로 좁혀 드립니다.</p></div></div></div></div><div class="grid3" style="margin-top:72px"><div class="center r"><h3>담당자 배치</h3><p class="sub" style="margin-top:8px">병원마다 전담 담당자와 서브담당자</p></div><div class="center r"><h3>키워드 관리</h3><p class="sub" style="margin-top:8px">환자가 실제로 오는 동선 기준으로 선정</p></div><div class="center r"><h3>맞춤 콘텐츠</h3><p class="sub" style="margin-top:8px">병원 톤에 맞춰 기획하고 검수</p></div></div><p class="center sub r" style="margin-top:20px;font-size:19px">→ 종합 관리가 가능한 마케팅의 실현</p></div></section>'''
    cases = f'''<section class="bg2" id="cases"><div class="wrap"><div class="head"><span class="eyebrow">우리 병원이라면 어떨까?</span><h2>세 가지 사례</h2></div>
<div class="split r" style="margin-bottom:96px"><div><div class="tags"><span class="tag">#불리한_입지</span><span class="tag">#여의사</span><span class="tag">#네이버_상단노출</span></div><h3 style="margin-top:20px;font-size:32px">한 번 망한 자리에서도<br>잘된 부천 'B병원'</h3><p class="sub" style="margin-top:20px;font-size:18px">기존 병원도 망했을 만큼 입지가 좋지 않았습니다. 지하철역 인근으로 접근성은 좋았으나 눈에 띄지 않는 건물이 문제였죠. 이렇게 입지에 단점이 있을 땐 <b style="color:var(--ink)">속도가 중요합니다.</b></p><p class="sub" style="margin-top:14px;font-size:18px">내원 가능 지역·여의사·주요 과목으로 45개 키워드를 추출해 개원 3주 전부터 블로그 상단에 노출했습니다. 여성 환자가 원하는 따뜻하고 섬세한 여의사가 메인 이미지가 되도록 컨셉 포토를 촬영했습니다.</p></div><div class="card"><div class="mock t">공식 블로그 순방문자 · 2022.11</div>{chart_growth()}<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-top:16px"><div><div class="big" style="font-size:34px">4,103</div><div class="mock t">월 순방문자</div></div><div><div class="big" style="font-size:34px">45</div><div class="mock t">키워드 · 개원 3주 전</div></div><div><div class="big" style="font-size:34px">74<small>%</small></div><div class="mock t">여성 방문자</div></div></div><div class="note mock" style="margin-top:16px">첫 달 조회 2,000 달성 후 매달 1,000씩 성장. 네이버 지도 주요 키워드 1페이지 진입.</div></div></div>
<div class="split r" style="margin-bottom:96px"><div class="card" style="order:1"><div class="mock t">신환 수 · 2023 vs 2024 (1~5월)</div>{chart_compare()}<div class="mock" style="margin-top:12px"><div class="rank on"><b>1</b><span>항문외과 (메인 키워드)</span></div><div class="rank"><b>4</b><span>강남항문외과</span></div><div class="rank"><b>5</b><span>하지정맥류병원</span></div></div></div><div style="order:2"><div class="tags"><span class="tag">#과한마케팅_사절</span><span class="tag">#진료철학</span><span class="tag">#메인키워드</span></div><h3 style="margin-top:20px;font-size:32px">원장님의 철학을<br>콘텐츠로 전달한 'S병원'</h3><p class="sub" style="margin-top:20px;font-size:18px">대대적인 홍보가 아닌 확고한 진료 철학을 진정성 있게 전달하는 마케팅을 원하셨습니다.</p><p class="sub" style="margin-top:14px;font-size:18px">원장님이 직접 쓰신 글과 학회 활동을 소스로, 솔직하고 전문적인 모습을 환자가 매력적으로 느끼도록 이미지화했습니다. 계절별 환자 흐름에 맞춰 기획안을 먼저 드리고 검수 후 제작했습니다.</p></div></div>
<div class="split r"><div><div class="tags"><span class="tag">#실패사례</span><span class="tag">#지역_연령대</span><span class="tag">#온오프라인</span></div><h3 style="margin-top:20px;font-size:32px">모든 프로젝트를<br>성공시킨 것은 아닙니다.</h3><p class="sub" style="margin-top:20px;font-size:18px">'H병원'은 검색·상단 노출이 문제없이 되는데도 3개월 동안 눈에 띄는 성과가 없었습니다. 원인은 내원 환자 연령대. 노인 인구가 많은 지역이라 온라인만으로는 신환 모객에 한계가 있었습니다.</p><p class="sub" style="margin-top:14px;font-size:18px">그 경험을 토대로 정형외과 Y병원은 진행 전 지역 내 연령대를 조사했습니다. 60~70대가 많은 지역에는 오프라인 광고를 병행해 단계적으로 유입을 높였습니다.</p><p style="margin-top:20px;font-size:18px;font-weight:600">실패한 사례가 있었기에 그 다음 단계로 성장할 수 있었습니다.</p></div><div class="card"><div class="mock t">Y병원 채널 조합</div><div class="grid2" style="gap:12px;margin-top:16px"><div><div class="mock t" style="color:var(--blue)">오프라인</div><div class="tags" style="margin-top:8px"><span class="tag">엘리베이터 영상</span><span class="tag">버스 정류장</span><span class="tag">지하철역 전광판</span></div></div><div><div class="mock t" style="color:var(--blue)">온라인</div><div class="tags" style="margin-top:8px"><span class="tag">검색 광고</span><span class="tag">지도 · 블로그</span><span class="tag">카페 · 당근</span></div></div></div><div class="note mock" style="margin-top:20px">60~70대 인구가 많은 동 단위 연령 분포를 먼저 조사한 뒤 채널을 정했습니다.</div></div></div></div></section>'''
    channels = '''<section><div class="wrap"><div class="head"><h2>우리 병원에 맞는<br>마케팅은?</h2><p class="lead">모든 병원에 같은 채널을 권하지 않습니다. 진료과, 지역, 환자 연령대에 따라 조합합니다.</p></div><table class="clean r"><tr><th>분류</th><th>채널</th><th>무엇을 합니까</th></tr>
<tr><td class="g">검색 노출</td><td>네이버 플레이스</td><td>지역+병원 검색 시 가장 우선 노출되는 지도 영역. 이미지·순위·예약·광고를 관리합니다.</td></tr>
<tr><td></td><td>공식 블로그</td><td>매달 키워드 계획을 세우고 검수를 거쳐 발행합니다.</td></tr>
<tr><td></td><td>언론 보도</td><td>원장님의 전문성을 보여주는 뉴스 기사.</td></tr>
<tr><td class="g">바이럴</td><td>네이버 카페</td><td>맘카페·뷰티카페 제휴와 이벤트.</td></tr>
<tr><td></td><td>리뷰</td><td>리뷰에 답하고, 실제 후기가 쌓이도록 이벤트를 설계합니다.</td></tr>
<tr><td class="g">웹배너</td><td>당근마켓</td><td>지역 기반 광고와 쿠폰.</td></tr>
<tr><td></td><td>카카오톡</td><td>환자와 소통하는 채널과 타깃 광고.</td></tr></table></div></section>'''
    month = '''<section class="bg2"><div class="wrap"><div class="head"><span class="eyebrow">한 달의 일</span><h2>진단부터 보고까지,<br>매달 이렇게 돌아갑니다.</h2></div><div class="rows r" style="max-width:860px;margin:0 auto">
<div class="row"><div class="n">매달 초</div><div><h3>데이터를 먼저 봅니다</h3><p>전월 신환이 어느 지역에서 왔는지, 블로그·플레이스·광고 수치가 어떻게 움직였는지 채널별로 나눠 봅니다. 한 채널만 보고 판단하지 않습니다.</p></div></div>
<div class="row"><div class="n">매달 초</div><div><h3>보고서를 보냅니다</h3><p>메인 키워드의 PC·모바일 노출 순위 캡처, 광고 요약, 그리고 "왜 그랬는지"와 "다음 달엔 무엇을 바꿀지"를 담은 핵심 코멘트 2~3개. 원장님이 요약만 봐도 이해되는 구조로 씁니다.</p></div></div>
<div class="row"><div class="n">매달 말</div><div><h3>다음 달 계획을 짭니다</h3><p>키워드를 네 종류(지역+진료과 메인 / 인근 생활권 서브 / 계절·이슈 트렌드 / 병원 소식 브랜드)로 나눠 발행 계획표를 만들고, 담당자가 1차, 팀장이 2차로 검토합니다.</p></div></div>
<div class="row"><div class="n">매주 월요일</div><div><h3>순위를 점검합니다</h3><p>그 주에 발행한 키워드의 검색 노출 순위를 확인하고, 목표보다 낮은 키워드는 추가 콘텐츠로 보강합니다.</p></div></div></div><p class="sub center r" style="margin-top:40px">매일: 리뷰 확인과 답글 · 플레이스 순위 확인 · 광고 노출 확인 · 발행 전 검수</p></div></section>'''
    review = '''<section><div class="wrap"><div class="split"><div><span class="eyebrow">의료광고 심의, 함께 봅니다</span><h2>글 하나가 나가기 전에<br>다섯 가지를 봅니다.</h2><p class="lead">하나라도 걸리면 발행을 멈추고 고친 뒤 다시 검토합니다. 심의가 필요한 소재는 신청부터 수정까지 대신 합니다.</p></div><ul class="check r"><li>의료법 제56조 — 시술 효과 단정, 타 병원 비교 표현이 없는지</li><li>병원의 톤앤매너와 맞는지</li><li>의학 용어와 오탈자</li><li>이미지 저작권</li><li>연락처·진료시간 같은 사실관계</li></ul></div>
<div style="margin-top:96px"><h3 class="center">자주 바꿔 쓰는 표현</h3><table class="clean r" style="max-width:760px;margin:24px auto 0"><tr><th>쓰지 않는 표현</th><th>바꿔 쓰는 표현</th></tr><tr><td>전문병원 · 전문</td><td>병의원 · 질환 + 클리닉</td></tr><tr><td>최고 · 최초 · 유일</td><td>사용하지 않음</td></tr><tr><td>완치 · 해결</td><td>사용하지 않음</td></tr><tr><td>부작용 없이</td><td>최소화 · 거의 없는</td></tr><tr><td>안전한</td><td>안심할 수 있는 · 편안한</td></tr><tr><td>당일 수술 · 당일 퇴원</td><td>당일 수술 지향</td></tr></table><p class="center" style="margin-top:24px"><a class="link" href="#">전체 표현 24개 보기 (247)</a></p></div></div></section>'''
    welcome = '''<section class="bg2"><div class="wrap"><div class="head"><span class="eyebrow">welcome easteregg!</span><h2>이스터에그가 처음인<br>원장님을 위한 웰컴 혜택</h2></div><div class="grid4">
<div class="card r"><div class="eyebrow">혜택 1</div><h3>홍보용 뉴스기사</h3><p class="sub" style="margin-top:10px">전문성을 보여주는 홍보 수단으로 원고 작성과 송출 2건 무료</p></div>
<div class="card r"><div class="eyebrow">혜택 2</div><h3>브랜딩 글</h3><p class="sub" style="margin-top:10px">원장님의 진료 철학을 담아 우리 병원만의 차별점을 보여주는 콘텐츠 2건 무료</p></div>
<div class="card r"><div class="eyebrow">혜택 3</div><h3>네이버 광고 세팅</h3><p class="sub" style="margin-top:10px">소재 제작부터 번거로운 의료 심의, 효율적인 운영을 위한 세팅까지</p></div>
<div class="card r"><div class="eyebrow">혜택 4</div><h3>3사 지도 등록</h3><p class="sub" style="margin-top:10px">카카오 · 구글 · 네이버 어디서나 우리 병원이 검색될 수 있도록</p></div></div><p class="sub center" style="margin-top:28px;font-size:13px">※ 혜택 내용은 2024년 기준. 최신 조건 확인 후 게시.</p></div></section>'''
    return page('병원 마케팅 · 네이버 플레이스 · 개원 마케팅 | 이스터에그','검색에서 먼저 보이고 예약으로 이어지게. 플레이스·블로그·검색광고·리뷰를 한 사람이 끝까지 운영합니다.','marketing.html', hero+secretary+cases+channels+month+review+welcome)

# ---------- 디자인 ----------
def design():
    hero = '''<section style="padding-top:96px;padding-bottom:0"><div class="wrap center"><span class="eyebrow">Design</span><h1>디자인 업체,<br>별도로 찾지 않으셔도 됩니다.</h1><p class="lead narrow">홈페이지부터 원내 인쇄물까지, 병원의 톤을 한 벌로 맞춥니다. 마케팅과 같은 팀이 만들기 때문에 전략과 화면이 어긋나지 않습니다.</p><div class="actions"><a class="btn" href="https://design.easteregg247.com/" target="_blank" rel="noopener">포트폴리오 보러가기</a><a class="btn outline" href="contact.html">디자인 문의</a></div></div></section>'''
    together = '''<section><div class="wrap"><div class="split"><div><h2>함께<br>고민합니다.</h2><p class="lead">병원의 입장과 환자의 입장을 모두 고려하며, 빠른 의사결정을 위한 선택지와 디자이너의 견해를 함께 전달드립니다.</p></div><div class="stage r"><div class="chat"><div class="m us">원장님 의견 반영하여 '위치 강조'로 디자인 수정했습니다.</div><div class="m us">역에서 가깝다는 것을 강조하는 게 목적이시라면 역 출구를 시각화한 2번 시안을 추천드립니다.</div><div class="m dr">2번 좋아요. 그렇게 진행해주세요.</div></div></div></div></div></section>'''
    web = '''<section class="bg2"><div class="wrap"><div class="head"><span class="eyebrow">홈페이지</span><h2>공장형 홈페이지가<br>아닙니다.</h2><p class="lead">병원을 검색하시면서 비슷한 홈페이지 보신 적 없으신가요? 하나의 폼을 돌려쓰는 업체가 많습니다. 각각의 차별점을 살려 그 병원만의 홈페이지를 제작합니다.</p></div><div class="grid2"><div class="card r"><div class="eyebrow">Option 1 · Basic</div><h3>스크롤 형</h3><p class="sub" style="margin-top:10px">표준적인 홈페이지로, 스크롤하며 아래로 읽어 나가는 형식.</p></div><div class="card r"><div class="eyebrow">Option 2 · Full Screen</div><h3>풀스크린 형</h3><p class="sub" style="margin-top:10px">스크롤하면 자동으로 다음 페이지로 넘어가는, 한 장씩 끊어 읽는 홈페이지. (PC)</p></div></div>
<div class="rows r" style="margin-top:64px;max-width:860px;margin-left:auto;margin-right:auto"><div class="row"><div class="n">Point 1</div><div><h3>저작권 걱정 없는 이미지</h3><p>유료 이미지를 사용하고, 필요한 아이콘은 직접 제작합니다.</p></div></div><div class="row"><div class="n">Point 2</div><div><h3>죽어있는 홈페이지처럼 보이지 않게</h3><p>팝업·공지사항을 수시로 업데이트합니다.</p></div></div><div class="row"><div class="n">Point 3</div><div><h3>제작하고 끝나는 게 아닙니다</h3><p>이후 수정 보완과 유지 보수를 진행합니다.</p></div></div></div></div></section>'''
    banner = '''<section><div class="wrap"><div class="split"><div class="stage r" style="min-height:460px"><div class="xb" style="transform:rotate(-3deg)"><div class="top">OO정형외과</div><div class="main">B동 4층<br>엘리베이터를<br>이용해 주세요</div><div class="foot">문의 032-000-0000</div></div></div><div><span class="eyebrow">엑스배너</span><h2>의도된<br>디자인을 합니다.</h2><div class="rows" style="margin-top:32px"><div class="row" style="grid-template-columns:90px 1fr"><div class="n">#TEXT</div><div><p style="margin:0;color:var(--ink)">강조할 한 가지만 크게.</p></div></div><div class="row" style="grid-template-columns:90px 1fr"><div class="n">#COLOR</div><div><p style="margin:0;color:var(--ink)">설치 장소의 주변색과 대조되는 배경색.</p></div></div><div class="row" style="grid-template-columns:90px 1fr"><div class="n">#CHECK</div><div><p style="margin:0;color:var(--ink)">모서리 구멍 여유 공간까지 계산.</p></div></div></div></div></div></div></section>'''
    prints = '''<section class="bg2"><div class="wrap"><div class="head"><span class="eyebrow">원내 인쇄물</span><h2>환자가 손에 쥐는 것까지.</h2><p class="lead">디자인 시안과 인쇄용 파일까지 제작합니다. 인쇄·간판 시공은 제휴 업체를 안내해 드립니다.</p></div><div class="grid3 r">
<div class="print" style="height:200px"><b>접수증</b><i></i><i style="width:70%"></i><i></i><i style="width:50%"></i><i style="width:80%"></i></div>
<div class="print" style="height:200px"><b>명함</b><i style="width:40%"></i><i style="width:30%"></i><span style="margin-top:auto">OO외과 · 원장</span></div>
<div class="print" style="height:200px"><b>포스터</b><i style="height:60px;border-radius:8px"></i><i style="width:60%"></i></div>
<div class="print" style="height:200px"><b>전단지</b><i></i><i></i><i style="width:60%"></i><i style="height:40px;border-radius:8px"></i></div>
<div class="print" style="height:200px"><b>안내문</b><span>수술 후 주의사항</span><i></i><i></i><i style="width:70%"></i></div>
<div class="print" style="height:200px"><b>봉투 · 서식</b><i style="width:50%"></i><span style="margin-top:auto">리뷰 이벤트 포스터 · 홈페이지 팝업 배너</span></div></div>
<div class="center" style="margin-top:56px"><a class="btn" href="https://design.easteregg247.com/" target="_blank" rel="noopener">디자인 포트폴리오 보러가기</a><p class="sub" style="margin-top:16px">첫 계약 시 엑스배너 디자인 5개 무료 (약 10만 원 상당, 거치대 별도) ※ 최신 조건 확인</p></div></div></section>'''
    return page('병원 홈페이지 제작 · 엑스배너 · 사인물 | 이스터에그','로고부터 홈페이지, 엑스배너, 접수증, 명함, 포스터까지 병원 브랜드를 한 벌로 설계합니다.','design.html', hero+together+web+banner+prints)

# ---------- 문의 ----------
def contact():
    body = '''<section style="padding-top:96px"><div class="wrap"><div class="head left" style="max-width:none"><span class="eyebrow">똑똑한 마케팅만 합니다</span><h1>EGG 컨설팅,<br>바로 문의하기</h1><p class="lead" style="max-width:640px">바로 통화가 어려우시다면 아래 양식을 남겨 주세요. 영업일 기준 1일 내에 확인하고 연락드립니다.</p></div><div class="split" style="align-items:start"><div><div class="rows"><div class="row" style="grid-template-columns:90px 1fr"><div class="n">TEL</div><div><h3><a href="tel:032-710-2258">032-710-2258</a></h3></div></div><div class="row" style="grid-template-columns:90px 1fr"><div class="n">EMAIL</div><div><h3 style="font-size:20px">easteregg.medi@gmail.com</h3></div></div><div class="row" style="grid-template-columns:90px 1fr"><div class="n">OFFICE</div><div><p style="margin:0;color:var(--ink)">인천 연수구 인천타워대로 323,<br>송도센트로드 A동 1811호</p><a class="link" href="https://map.naver.com/p/search/송도센트로드" target="_blank" rel="noopener" style="font-size:15px">네이버 지도에서 보기</a></div></div><div class="row" style="grid-template-columns:90px 1fr"><div class="n">HOURS</div><div><p style="margin:0;color:var(--ink)">평일 10:00–18:00 · 주말·공휴일 휴무</p></div></div></div><div class="card" style="margin-top:32px;background:var(--bg2);box-shadow:none"><b>문의 후 진행</b><ol style="margin:12px 0 0 18px;color:var(--sub);line-height:1.9"><li>담당자 전화 (영업일 1일 내)</li><li>진단 미팅 30분 — 방문 또는 화상</li><li>제안서 · 견적 (미팅 후 1주 내)</li></ol></div></div>
<form class="form card r" onsubmit="return false"><div class="two"><div><label>병원명 · 직책</label><input placeholder="OO외과 · 원장"></div><div><label>연락처</label><input type="tel" placeholder="010-0000-0000"></div></div><div><label>진료과</label><select><option>외과</option><option>정형외과</option><option>가정의학과</option><option>치과</option><option>기타</option></select></div><div><label>개원 여부</label><div class="radios"><label><input type="radio" name="o" checked> 운영 중</label><label><input type="radio" name="o"> 개원 예정</label></div></div><div><label>문의 내용</label><textarea placeholder="현재 상황과 궁금한 점을 적어 주세요. 개원 예정이면 예정 시기도 함께."></textarea></div><label class="agree"><input type="checkbox"> 개인정보 수집·이용에 동의합니다. <a href="#" class="link" style="font-size:14px">내용 보기</a></label><button class="btn">문의 보내기</button></form></div></div></section>
<section class="bg2 tight"><div class="wrap"><div class="narrow"><h2 style="font-size:34px;margin-bottom:24px">자주 묻는 질문</h2><details><summary>효과는 보통 언제부터 보이나요?</summary><p>플레이스·리뷰 정비처럼 바로 반영되는 항목은 첫 달에, 블로그·콘텐츠처럼 쌓이는 항목은 보통 3개월 전후부터 유입 변화가 보입니다. 첫 보고서에서 항목별 예상 시점을 적어 드립니다.</p></details><details><summary>의료광고 심의는 어떻게 하나요?</summary><p>심의 대상이 되는 소재는 제작 단계에서 걸러내고, 필요한 건은 절차에 맞춰 신청부터 수정까지 대신 합니다. 치료 효과 보장·비교 표현은 처음부터 쓰지 않습니다.</p></details><details><summary>원장님이 해야 할 일은 얼마나 되나요?</summary><p>월 1회 보고서 브리핑과 글 검수가 전부입니다. 촬영이 있는 달에는 반나절 정도 시간을 내 주시면 됩니다.</p></details><details><summary>인천 외 지역도 가능한가요?</summary><p>네. 인천 송도에서 시작했지만 지금은 서울·경기·세종·부산 등 전국 병원과 일하고 있습니다. 첫 미팅은 방문하고, 월간 브리핑은 화상으로도 진행합니다.</p></details></div></div></section>'''
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>상담 문의 | 이스터에그</title><meta name="description" content="영업일 1일 내 연락, 30분 진단 미팅부터 시작합니다. 032-710-2258"><link rel="stylesheet" href="style.css"></head><body>{nav('contact.html')}{body}{footer()}<script>{JS}</script></body></html>'''

(OUT/'style.css').write_text(CSS.strip()+'\n', encoding='utf-8')
(OUT/'index.html').write_text(index(), encoding='utf-8')
(OUT/'marketing.html').write_text(marketing(), encoding='utf-8')
(OUT/'design.html').write_text(design(), encoding='utf-8')
(OUT/'contact.html').write_text(contact(), encoding='utf-8')
print('built')
