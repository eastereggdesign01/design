# 이스터에그 사이트

두 개의 페이지로 구성됩니다.

- `/` — **작업물 모음(포트폴리오)**: 만든 프로젝트를 버튼으로 나열, 클릭 시 해당 사이트로 이동
- `/hub/` — **브랜드 키트 허브**: 병원별 브랜드 정보(로고 · 컬러 · 전화 · 진료과)를 한곳에서 찾아 쓰는 내부 도구.
  로고는 **로그인 없이 누구나 다운로드**할 수 있습니다.

## 작업물(포트폴리오 버튼) 추가

`src/data/works.json` 배열에 항목 하나를 추가하면 홈 화면에 버튼이 생깁니다.

```json
{
  "emoji": "🤖",
  "title": "프로젝트 이름",
  "description": "한 줄 설명",
  "tags": ["AI", "웹"],
  "url": "https://example.com"
}
```

- `url`이 `http(s)`로 시작하면 새 탭으로 열리고, `/hub/`처럼 내부 경로면 같은 탭에서 이동합니다.
- `emoji` · `tags` · `description`은 생략 가능합니다.

## 납품 실적(레퍼런스) 추가

`src/data/references.json` 에 항목 하나를 추가하면 "납품 실적" 카드가 생깁니다.
`slug`만 적으면 이름 · 진료과 · 대표 컬러 · 홈페이지 주소 · 로고를 `hospitals.json` 에서 자동으로 끌어옵니다.

```json
{ "slug": "yeilhang", "year": "2025" }
```

브랜드 키트에 없는 병원이면 직접 적습니다. 필요한 필드만 쓰면 됩니다.

```json
{
  "name": "연세히어로정형외과",
  "dept": ["정형외과"],
  "color": "#1F4E79",
  "url": "https://…",
  "year": "2025",
  "note": "카드 아래에 노란 메모로 표시됩니다",
  "shot": "/shots/yeonsehero.jpg"
}
```

- `shot` — 홈페이지 화면 캡처 경로. 넣으면 로고 자리가 캡처 이미지로 바뀝니다. (없으면 브랜드 컬러 배경 + 로고)
- "고객사" 로고 월은 `hospitals.json` 전체가 자동으로 들어갑니다. 따로 관리할 필요 없습니다.

## 인쇄물 추가

`src/data/prints.json` 의 `images` 배열에 경로를 넣으면 그대로 채워집니다.
비어 있으면 "이미지 준비 중" 자리만 잡아 둡니다.

```json
{
  "title": "명함 제작 모음",
  "description": "병원별 명함 디자인",
  "images": ["/prints/card-01.jpg", "/prints/card-02.jpg"]
}
```

## 분류 필터

상단 필터는 `전체 · 홈페이지 · 인쇄물 · 영상 · AI 도구` 다섯 개입니다.
작업물의 분류는 `works.json` 의 `category` 로 지정하고, 없으면 `type` 으로 갈음합니다
(`웹 도구` → AI 도구, 그 외 → 홈페이지). 항목이 하나도 없는 섹션은 자동으로 숨겨집니다.

## 실행 / 빌드

```bash
npm install
npm run dev      # 로컬 개발 서버
npm run build    # dist/ 폴더에 정적 파일 생성
```

## 배포

- **Netlify**: 저장소 연결 시 `netlify.toml` 설정을 자동으로 사용합니다. (build: `npm run build`, publish: `dist`)
- **Vercel**: Vite 프로젝트로 자동 인식됩니다.
- 드래그앤드롭 배포를 원하면 `npm run build` 후 `dist/` 폴더를 올리면 됩니다.

## 로고 추가 / 교체 (디자이너용)

1. `public/logos/` 폴더에 PNG 파일을 넣는다.
2. 파일명 규칙: `{슬러그}_{버전}.png`
   - 버전: `v` = 세로, `h` = 가로, `vw` = 세로 화이트, `hw` = 가로 화이트
   - 예: `365hang_v.png`, `samsungyu_hw.png`
3. 재배포하면 해당 버전의 "다운로드" 버튼이 자동으로 켜진다. (파일이 없는 버전은 회색 "없음" 처리)

병원마다 4종을 모두 넣을 필요는 없습니다. 있는 파일만 자동으로 감지됩니다.

## 병원 데이터 수정

`src/data/hospitals.json` 을 수정합니다. 항목 구조:

```json
{
  "slug": "365hang",              // 로고 파일명에 쓰는 영문 슬러그
  "name": "365항외과",
  "dept": ["항문·대장"],           // 진료과 태그 (필터에 자동 반영)
  "phone": "02-900-0365",
  "address": "…",
  "colors": [{ "label": "Main", "hex": "#F27B1F" }],
  "gradient": ["#FBB95B", "#EC1C29"],  // 없으면 null
  "hours": ["평일 09:00 – 20:00", "…"],
  "links": [                           // 선택 — 드로어의 "링크" 섹션에 버튼으로 표시
    { "label": "홈페이지", "url": "https://…" },
    { "label": "블로그", "url": "https://blog.naver.com/…" }
  ]
}
```

병원 추가 = 이 배열에 항목 하나 추가 + 로고 파일 넣기. 그게 전부입니다.

## 병원 슬러그 매핑

| 병원 | 슬러그 |
|---|---|
| 365항외과 | 365hang |
| JS항외과 | jshang |
| 검단항외과 | geomdanhang |
| 김혜은여성외과 | kimhyeeun |
| 맥스모외과 | maxmo |
| 미래항맥외과 | miraehangmaek |
| 부천맘편한외과 | bucheonmompyeonhan |
| 삼성유외과 | samsungyu |
| 새빛병원 | saebit |
| 서울유항외과 | seoulyuhang |
| 서울탑항맥외과 | seoultaphangmaek |
| 서울항앤하지외과 | seoulhanghaji |
| 세종365믿음정형외과 | sejong365mideum |
| 송도외과 | songdo |
| 여의유항외과 | yeouiyuhang |
| 예일항외과 | yeilhang |
| 조은아침예항외과 | joeunachim |
| 참편한여성의원 | champyeonhan |
| 항편한하지외과 | nowonhangpyeonhan |
| 데이웰 분당점 | daywell_bundang |
| 데이웰 대치점 | daywell_daechi |
| 데이웰 용산점 | daywell_yongsan |
| 데이웰 미사점 | daywell_misa |
| 아주항외과 | ajuhang |
| 채항외과 | chaehang |
| 스마일미치과 | smileme |
| 서울튼튼정형외과 | seoultunteun |
| 둔촌오세관정형외과 | osegwan |

데이웰 로고 매핑: 분당점 = "데이웰의원" 로고 / 대치점·용산점·미사점 = "데이웰가정의학과" 로고 (같은 파일을 슬러그별로 복사해 사용)

## 다음 확장 (자리만 잡아둠)

- 폰트 · 톤앤매너 블록: 국문/영문 지정 폰트, 톤 키워드
- 소재 아카이브 블록: 병원별 카드뉴스 · 인스타 · 포스터 모아보기
