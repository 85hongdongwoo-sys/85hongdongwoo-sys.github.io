/* =====================================================================
   광고 설정 파일 (ads.js)
   - 쿠팡 파트너스 링크와 상품은 이 파일만 고치면 돼요.
   - 고친 뒤 GitHub에서 저장(Commit)하면 1~2분 뒤 사이트에 반영돼요.
   - 쉼표(,)와 따옴표(")를 지우지 않도록 조심하세요.

   상품 한 줄 모양:
   { url: "링크", title: "상품명", desc: "설명", img: "ads/사진.jpg", until: "2026-12-31" }
     · img   : 작은 상품 사진 (ads 폴더에 사진 파일을 올리고 이름을 적어요)
     · banner: 가로로 긴 배너 이미지를 쓸 때 img 대신 사용
     · until : 이 날짜가 지나면 자동으로 안 보여요 (선택)
     · off   : true 로 적으면 바로 숨겨요 (품절·종료 때)
   ===================================================================== */

const ADS = {
  coupang: {
    url: "",   // 쿠팡 파트너스 링크 (예: https://link.coupang.com/a/xxxxx)
    title: "투자 공부할 때 책상 위 필수템",
    desc: "재테크 책 · 공학용 계산기 · 모니터암",
    button: "쿠팡에서 보기",
    disclosure: "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다."
  },
  coupang_home: { url: "", title: "이사·입주 준비템", desc: "수납·청소·조명 같은 새집 필수템", button: "쿠팡에서 보기", disclosure: "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다." },
  coupang_book: { url: "", title: "재테크 공부 필수템", desc: "재테크 베스트셀러 · 공학용 계산기 · 가계부", button: "쿠팡에서 보기", disclosure: "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다." },
  /* 분야별 추천 칸 (계산 결과 아래에 자동으로 나와요). url을 비워 두면 아래 coupang_all 상품 중 하나가 대신 나와요. */
  coupang_car:    { url: "", title: "자동차 필수템", desc: "블랙박스 · 차량용 청소기 · 타이어 공기압 측정기", button: "쿠팡에서 보기", disclosure: "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다." },
  coupang_baby:   { url: "", title: "출산·육아 준비물", desc: "기저귀 · 물티슈 · 분유 · 아기 옷", button: "쿠팡에서 보기", disclosure: "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다." },
  coupang_health: { url: "", title: "건강 관리템", desc: "체중계 · 혈압계 · 영양제", button: "쿠팡에서 보기", disclosure: "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다." },
  coupang_study:  { url: "", title: "수험생 필수템", desc: "독서대 · 타이머 · 공학용 계산기", button: "쿠팡에서 보기", disclosure: "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다." },
  coupang_work:   { url: "", title: "직장인 필수템", desc: "노트북 거치대 · 무선 마우스 · 사무용 의자", button: "쿠팡에서 보기", disclosure: "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다." },
  coupang_all: { url: "", title: "", desc: "", button: "쿠팡에서 보기", disclosure: "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.",
    items: [
      { url: "https://link.coupang.com/a/hupgpGhQI0", title: "오늘의 쿠팡 특가", desc: "쿠팡 오늘의 특가 모아보기", banner: "ads/coupang_today.png" },
      { url: "https://link.coupang.com/a/hupk2WiOQ0", title: "로켓프레시 신선식품 새벽배송", desc: "쿠팡 로켓프레시 신선식품", banner: "ads/coupang_fresh.png" },
      { url: "https://link.coupang.com/a/hupFing8Um", title: "로켓배송 가격비교 필요없다", desc: "쿠팡 로켓배송 가전·디지털", banner: "ads/coupang_rocket.png" }
    ] }
};
/* 같은 분야에 상품이 여러 개면 items: [{url, title, desc, until:'YYYY-MM-DD'(선택, 이 날이 지나면 자동으로 빠짐), off:true(종료·품절로 뺀 것)}, ...] 로 넣어요. 페이지를 열거나 탭을 바꿀 때마다 그중 하나가 무작위로 나와요. */

/* 탭마다 어떤 광고를 보여줄지 */
const TAB_AD = { sell:'coupang_book', us:'coupang_book', div:'coupang_book', avg:'coupang_book', risk:'coupang_book', gold:'coupang_book', ipo:'coupang_book',
  int:'coupang_book', grow:'coupang_book', pen:'coupang_book', fire:'coupang_book', fin:'coupang_book', nhis:'coupang_book', yet:'coupang_book', nps:'coupang_book', sev:'coupang_book', eitc:'coupang_book',
  buy:'coupang_home', dsr:'coupang_home', score:'coupang_home', safe:'coupang_home', rent:'coupang_home', refi:'coupang_home', ptax:'coupang_book', gift:'coupang_book', yield:'coupang_home', auc:'coupang_home', dist:'coupang_book' };
