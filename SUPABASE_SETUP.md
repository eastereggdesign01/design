# Supabase 연동 설정 (팀 마스터키 + 즐겨찾기 동기화)

즐겨찾기를 기기에 상관없이 동기화하려면 Supabase 무료 프로젝트 하나만 만들면 됩니다.

## 1. 프로젝트 만들기

1. https://supabase.com → 로그인 → **New project**
2. 이름은 아무거나 (예: `brand-kit-hub`), 리전은 Northeast Asia (Seoul) 추천

## 2. 테이블 만들기

Supabase 대시보드 → **SQL Editor** → 아래 스크립트 붙여넣고 **Run**:

```sql
-- 마스터키 (원하는 값으로 바꿔서 실행)
create table if not exists app_keys (key text primary key);
insert into app_keys values ('여기에-원하는-마스터키') on conflict do nothing;

-- 즐겨찾기
create table if not exists favorites (
  master_key text not null,
  user_name  text not null,
  slug       text not null,
  created_at timestamptz default now(),
  primary key (master_key, user_name, slug)
);

alter table app_keys  enable row level security;
alter table favorites enable row level security;

create policy "public read keys"  on app_keys  for select using (true);
create policy "public favorites"  on favorites for all    using (true) with check (true);
```

## 3. 앱에 연결

대시보드 → **Settings → API** 에서 두 값을 복사:

- **Project URL** (예: `https://xxxx.supabase.co`)
- **anon public key**

`src/data/supabase.json` 에 붙여넣고 재배포:

```json
{
  "url": "https://xxxx.supabase.co",
  "anonKey": "eyJ..."
}
```

값이 비어 있으면 앱은 기존처럼 브라우저 저장(localStorage) 모드로만 동작하고,
"팀 로그인" 버튼도 표시되지 않습니다.

## 동작 방식

- 헤더의 **팀 로그인** 버튼 → 마스터키 입력 → 맞으면 로그인 상태 유지 (기기당 1회)
- 로그인 + 담당자 이름 설정 상태에서 별(★)을 누르면 Supabase에 저장 → 다른 기기에서도 동일하게 보임
- 마스터키 변경: SQL Editor에서 `update app_keys set key = '새키';`

## 보안 참고

내부 편의용 구조입니다. anon key로 favorites 테이블에 접근 가능하므로
민감한 데이터는 절대 이 테이블에 넣지 마세요. (즐겨찾기 슬러그만 저장)
