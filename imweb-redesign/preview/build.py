#!/usr/bin/env python3
"""섹션 코드를 페이지별로 이어 붙여 미리보기 HTML을 만듭니다. (아임웹에 올리는 파일이 아님)
사용: python3 preview/build.py  → preview/*.html 생성"""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
site_css = (root/'global/site.css').read_text(encoding='utf-8')
reveal_js = (root/'global/reveal.js').read_text(encoding='utf-8')
board_css = (root/'05-247/board.css').read_text(encoding='utf-8')
footer = None
cta = None

def mock_header(active):
    items = ['MARKETING','DESIGN','247','CONTACT']
    nav = ''.join(f'<a href="{i}.html" class="{"on" if i==active else ""}">{i}</a>' for i in items)
    return f'''<header class="pv-header"><div class="pv-wrap"><a class="pv-logo" href="index.html"><svg width="120" height="22" viewBox="0 0 120 22"><text x="0" y="17" font-family="Pretendard Variable,Pretendard,sans-serif" font-weight="800" font-size="19" letter-spacing="-0.5">EASTER EGG</text></svg></a><nav>{nav}</nav><a class="pv-cta" href="CONTACT.html">상담 문의</a></div></header>'''

pv_css = '''
/* 미리보기 전용: 아임웹 헤더 모사 + 플레이스홀더 이미지 처리 */
.pv-header{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.86);backdrop-filter:saturate(180%) blur(12px);border-bottom:1px solid rgba(17,20,24,.06);font-family:var(--eg-font)}
.pv-wrap{max-width:1200px;margin:0 auto;padding:0 24px;height:68px;display:flex;align-items:center;gap:32px}
.pv-logo{color:#111417;display:flex}
.pv-header nav{display:flex;gap:28px;margin-left:auto}
.pv-header nav a{font-size:14px;font-weight:600;letter-spacing:.04em;color:#111417;text-decoration:none}
.pv-header nav a.on{color:#0f9bd6}
.pv-cta{height:40px;padding:0 18px;border-radius:999px;background:#111417;color:#fff;font-size:14px;font-weight:700;text-decoration:none;display:inline-flex;align-items:center}
@media(max-width:800px){.pv-header nav{display:none}}
img[src^="["]{opacity:0}
.pv-tag{position:absolute;left:12px;top:10px;z-index:5;font:600 11px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.02em;color:#fff;background:rgba(15,155,214,.92);padding:6px 9px;border-radius:6px;pointer-events:none;opacity:.9}
.eg{position:relative}
.pv-note{position:fixed;right:14px;bottom:14px;z-index:60;background:#111417;color:#fff;font:500 12.5px/1.5 var(--eg-font);padding:12px 14px;border-radius:12px;max-width:300px;box-shadow:0 12px 32px rgba(0,0,0,.25)}
.pv-note b{color:#50c8fa}
.pv-ph{position:absolute;inset:0;display:grid;place-items:center;font-size:12px;color:rgba(0,0,0,.35);pointer-events:none}
'''

def page(name, title, parts, extra_css='', active=''):
    body = '\n'.join(parts)
    # 플레이스홀더 이미지에 안내 라벨 표시
    body = re.sub(r'<img src="\[([^"]*)\]"([^>]*)>', lambda m: f'<img src="[{m.group(1)}]"{m.group(2)}><span class="pv-ph">이미지 자리: {m.group(1)[:28]}</span>', body)
    html = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<style>{site_css}</style><style>{extra_css}</style><style>{pv_css}</style></head><body>
{mock_header(active)}
{body}
<div class="pv-note"><b>시안 미리보기</b> · 회색 박스는 이미지 자리, [대괄호]는 교체할 문구입니다. 각 섹션 왼쪽 위 파란 라벨이 코드 파일명이에요. 수정 요청은 그 라벨 이름으로 말씀해 주세요.</div>
<script>{reveal_js}</script>
<script>document.querySelectorAll('.eg-reveal').forEach(e=>e.classList.add('is-in'))</script>
</body></html>'''
    (root/'preview'/f'{name}.html').write_text(html, encoding='utf-8')

def rd(p):
    html=(root/p).read_text(encoding='utf-8')
    tag=f'<span class="pv-tag">{p}</span>'
    return re.sub(r'(<(section|footer)\b[^>]*>)', lambda m: m.group(1)+tag, html, count=1)
footer = rd('06-contact/03-footer.html')
cta = rd('01-home/09-cta.html')

def all_in(d): return [rd(str(p.relative_to(root))) for p in sorted((root/d).glob('*.html')) if not p.name.startswith('_')]

mock_form = '''<form onsubmit="return false" style="display:grid;gap:14px;font-family:var(--eg-font)"><div style="display:grid;grid-template-columns:1fr 1fr;gap:12px"><label style="font-size:13.5px;font-weight:700">병원명<input style="margin-top:8px;width:100%;height:52px;border:1px solid #e6e8eb;border-radius:12px;padding:0 16px;font:inherit" placeholder="OO외과"></label><label style="font-size:13.5px;font-weight:700">진료과<input style="margin-top:8px;width:100%;height:52px;border:1px solid #e6e8eb;border-radius:12px;padding:0 16px;font:inherit" placeholder="외과 / 정형외과 …"></label></div><label style="font-size:13.5px;font-weight:700">연락처<input style="margin-top:8px;width:100%;height:52px;border:1px solid #e6e8eb;border-radius:12px;padding:0 16px;font:inherit" placeholder="010-0000-0000"></label><label style="font-size:13.5px;font-weight:700">관심 서비스<div style="margin-top:8px;display:flex;gap:6px;flex-wrap:wrap"><span class="eg-chip">마케팅</span><span class="eg-chip">디자인</span><span class="eg-chip">미디어</span><span class="eg-chip">개원 패키지</span></div></label><label style="font-size:13.5px;font-weight:700">문의 내용<textarea style="margin-top:8px;width:100%;height:140px;border:1px solid #e6e8eb;border-radius:12px;padding:14px 16px;font:inherit" placeholder="현재 상황과 궁금한 점을 적어 주세요."></textarea></label><label style="font-size:13px;color:#697180"><input type="checkbox"> 개인정보 수집·이용에 동의합니다.</label><button class="eg-btn eg-btn--primary" style="width:100%;height:56px">문의 보내기</button></form>'''
def contact_block():
    return rd('06-contact/01-page-hero.html').replace('<!-- ▼ 아임웹 폼 위젯 자리 (코드 위젯이 아닌 아임웹 폼 위젯을 2단 컬럼 우측에 배치) -->', mock_form)

home_order=['01-hero','02-stats','03-services','05-cases','09-cta','06-portfolio','04-difference','07-process','08-insights']
page('index', '홈 미리보기', [rd(f'01-home/{n}.html') for n in home_order] + [contact_block(), footer], active='')
page('MARKETING', 'MARKETING 미리보기', all_in('02-marketing') + [cta, footer], active='MARKETING')
page('DESIGN', 'DESIGN 미리보기', all_in('03-design') + [cta, footer], active='DESIGN')
# 247: 게시판 목록은 아임웹 위젯이므로 목업 카드로 대체
mock_board = '''<section class="eg" style="padding-top:0"><div class="eg-wrap"><div style="display:flex;gap:6px;margin-bottom:28px"><a class="eg-btn eg-btn--primary eg-btn--sm" href="#">전체</a><a class="eg-btn eg-btn--ghost eg-btn--sm" href="#">인사이트</a><a class="eg-btn eg-btn--ghost eg-btn--sm" href="#">사례</a><a class="eg-btn eg-btn--ghost eg-btn--sm" href="#">공지</a></div>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:24px">''' + ''.join(f'''<a href="#" style="text-decoration:none;color:inherit"><div style="aspect-ratio:16/9;border-radius:14px;background:#e9edf1;position:relative"><span class="pv-ph">아임웹 게시판 썸네일</span></div><div style="margin-top:12px;font-size:12.5px;color:#697180">인사이트 · 2026.0{i}.0{i}</div><div style="margin-top:6px;font-size:17px;font-weight:700;letter-spacing:-.015em;line-height:1.45">[글 제목 {i}] — 아임웹 게시판 위젯(갤러리형)에 board.css 적용 시 이런 모습</div></a>''' for i in range(1,7)) + '</div></div></section>'
page('247', '247 미리보기', [rd('05-247/01-page-hero.html'), mock_board, cta, footer], extra_css=board_css, active='247')
contact = contact_block()
page('CONTACT', 'CONTACT 미리보기', [contact, footer], active='CONTACT')
print('built:', sorted(p.name for p in (root/'preview').glob('*.html')))
