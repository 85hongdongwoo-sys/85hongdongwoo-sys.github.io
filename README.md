# 홍라이프 투자계산기 — 사이트 올리기 안내

## 들어 있는 파일
- `index.html` — 계산기 28가지 (메인 페이지)
- `about.html` — 사이트 소개 + 문의처 (애드센스 심사에 필요)
- `privacy.html` — 개인정보처리방침 (애드센스 심사에 필요)
- `ads.js` — 광고 링크·상품 설정 (자주 고치는 파일)
- `ads/` — 광고 상품 사진
- `robots.txt`, `sitemap.xml` — 검색엔진 등록용

## 올리기 전에 바꿀 것
1. 모든 파일의 `YOUR-DOMAIN` → 실제 주소 (예: `hongcalc.github.io` 또는 구매한 도메인)
2. `about.html`의 "문의용 이메일" 자리 → 공개해도 되는 문의용 이메일
3. `ads.js` → 쿠팡 파트너스·토스쇼핑 링크와 상품 (이 파일만 고치면 모든 광고 칸에 반영)

## GitHub Pages로 무료 배포 (약 10분)
1. github.com 가입 → 새 저장소(New repository) 만들기, Public 선택
2. "Add file → Upload files"로 이 폴더의 파일을 모두 올리기
3. Settings → Pages → Branch를 `main` / `/ (root)`로 저장
4. 몇 분 뒤 `https://아이디.github.io/저장소이름/` 주소로 열림

## 검색 등록
- 구글 서치콘솔: 사이트 추가 → 소유 확인 → `sitemap.xml` 제출
- 네이버 서치어드바이저: 사이트 등록 → 소유 확인 → 사이트맵 제출

## 애드센스
- 방문자가 조금 생긴 뒤 신청
- 승인 코드(ca-pub-…)를 받으면 `index.html` 상단의 주석 처리된 애드센스 줄을 풀고 번호 교체
- 승인 후 사이트 루트에 `ads.txt` 파일을 추가 (애드센스 화면에서 내용 제공)

## 주의

- 환율·은행 금리는 `index.html` 안의 `CONFIG` 블록에서 고치면 전체에 반영돼요.
