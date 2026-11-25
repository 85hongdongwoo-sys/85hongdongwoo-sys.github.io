# Arttrip Studio — 사이트 코드

명화 작품 페이지를 **요청이 올 때 즉석에서 만드는** Cloudflare Workers 사이트예요. 영어가 기본이고 `/ko/` 아래 한국어판이 있어요.

## 구성
- `src/index.js` — 모든 페이지(홈, 갤러리, 주제·화가별 목록, 작품, 상품, 구독, 사이트맵)
- `src/i18n.js` — 영어/한국어 문구, 주제, 상품 목록, 색 이름
- `public/` — 그림(`img/`), 상품 이미지(`p/`), CSS·JS, 스튜디오(`studio/`)
- `schema.sql` — 데이터베이스 표, `data/seed.sql` — 작품 322점
- `tools/ingest.py` — 작품 JSON + 한국어 번역 + 색상 팔레트 → `seed.sql`

## 언어
- 한국어 브라우저로 처음 들어오면 `/ko/...`로 자동 이동 (검색 로봇은 이동시키지 않음)
- 오른쪽 위 버튼으로 언제든 전환, 선택은 쿠키로 기억
- 모든 페이지에 hreflang(영어·한국어) 표시

## 처음 올리는 방법 (Cloudflare 가입 후)
```
npm install
npx wrangler login
npx wrangler d1 create arttrip            # 나온 database_id를 wrangler.toml에 붙여넣기
npx wrangler d1 execute arttrip --remote --file=schema.sql
npx wrangler d1 execute arttrip --remote --file=data/seed.sql
npx wrangler deploy
```
그다음 Cloudflare 대시보드에서 도메인(arttripstudio.com)을 이 Worker에 연결하고,
`wrangler.toml`의 `[vars]`에 `SITE_ORIGIN = "https://arttripstudio.com"`과 Polar 결제 링크를 넣어요.

## 결제 (Polar)
`wrangler.toml` `[vars]`에 상품별 Polar 결제 링크를 넣으면 "곧 오픈" 버튼이 "구매하기"로 바뀌어요.
- `POLAR_PLANNER_2027`, `POLAR_CAL_FLOWERS`, `POLAR_CAL_SEA`, `POLAR_PATTERNS_FLOWERS`
- `POLAR_SUB_MONTHLY`, `POLAR_SUB_YEARLY`

## 수십만 페이지로 늘릴 때
- 작품 데이터는 D1에만 추가하면 페이지·사이트맵이 자동으로 늘어나요(파일 수 제한 없음).
- 그림 파일이 많아지면 `public/img` 대신 Cloudflare R2에 두고 이미지 주소만 바꿔요.
- 사이트맵은 4만5천 개씩 자동으로 나뉘어요. 서치 콘솔에는 `/sitemap.xml` 하나만 제출하면 돼요.
