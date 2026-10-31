/* =====================================================================
   광고 설정 파일 (ads.js)
   - 쿠팡 파트너스 / 토스쇼핑 쉐어링크 링크와 상품은 이 파일만 고치면 돼요.
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
  toss: {
    url: "",   // 토스 친구 초대·이벤트 링크
    title: "주식 계좌 아직 없다면",
    desc: "토스증권에서 계좌 개설하고 소수점 투자 시작하기",
    button: "토스로 열기",
    disclosure: "광고 · 이 링크로 가입하면 작성자가 혜택을 받을 수 있어요."
  },
  coupang_home: { url: "", title: "이사·입주 준비템", desc: "수납·청소·조명 같은 새집 필수템", button: "쿠팡에서 보기", disclosure: "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다." },
  coupang_book: { url: "", title: "재테크 공부 필수템", desc: "재테크 베스트셀러 · 공학용 계산기 · 가계부", button: "쿠팡에서 보기", disclosure: "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다." },
  toss_stock: { url: "", title: "주식 계좌 아직 없다면", desc: "토스증권 계좌 개설하고 소수점 투자 시작하기", button: "토스로 열기", disclosure: "광고 · 이 링크로 가입하면 작성자가 혜택을 받을 수 있어요." },
  toss_loan:  { url: "", title: "대출 금리 한 번에 비교", desc: "토스에서 여러 은행 대출 조건 비교하기", button: "토스로 열기", disclosure: "광고 · 이 링크로 가입하면 작성자가 혜택을 받을 수 있어요." },
  coupang_all: { url: "", title: "", desc: "", button: "쿠팡에서 보기", disclosure: "이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.",
    items: [
      { url: "https://link.coupang.com/a/hupgpGhQI0", title: "오늘의 쿠팡 특가", desc: "쿠팡 오늘의 특가 모아보기", banner: "ads/coupang_today.png" },
      { url: "https://link.coupang.com/a/hupk2WiOQ0", title: "로켓프레시 신선식품 새벽배송", desc: "쿠팡 로켓프레시 신선식품", banner: "ads/coupang_fresh.png" },
      { url: "https://link.coupang.com/a/hupFing8Um", title: "로켓배송 가격비교 필요없다", desc: "쿠팡 로켓배송 가전·디지털", banner: "ads/coupang_rocket.png" }
    ] },
  toss_shop: { url: "", title: "", desc: "", button: "토스쇼핑에서 보기", disclosure: "✱ 이 포스팅은 토스쇼핑 쉐어링크 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.",
    items: [
      { url: "https://toss.shopping/_m/L1ghjQG8", title: "경북 감홍사과 2kg", desc: "국내산 대과 2kg 1박스 · 10/1 기준 22,500원", img: "ads/apple.jpg" },
      { url: "https://toss.shopping/_m/jfzYO6a8", title: "제주감귤 9kg", desc: "대과 9kg 1박스 · 10/1 기준 18,200원", img: "ads/tangerine.jpg" },
      { url: "https://toss.shopping/_m/bTWPEmv3", title: "스파클 생수 2L 24개", desc: "무라벨 2L 24개 · 10/1 기준 7,400원", img: "ads/water2l.jpg" },
      { url: "https://toss.shopping/_m/JVABVFte", title: "스파클 생수 500ml 80개", desc: "무라벨 500ml 80개 · 10/1 기준 16,490원", img: "ads/water500.jpg" },
      { url: "https://toss.shopping/_m/TvCpTnHx", title: "을지로 연탄불고기 3팩", desc: "돼지불고기 250g 3개 · 10/1 기준 12,900원", img: "ads/bulgogi.jpg" },
      { url: "https://toss.shopping/_m/xjX44vV5", title: "아토워시 캡슐세제 200개", desc: "프렌치 라벤더 8g 200개입 · 10/1 기준 5,740원", img: "ads/atowash.jpg" }
    ] },
  toss_bank:  { url: "", title: "이자 많이 주는 통장 찾기", desc: "토스뱅크 통장·적금 이자 확인하기", button: "토스로 열기", disclosure: "광고 · 이 링크로 가입하면 작성자가 혜택을 받을 수 있어요." }
};
/* 같은 분야에 상품이 여러 개면 items: [{url, title, desc, until:'YYYY-MM-DD'(선택, 이 날이 지나면 자동으로 빠짐), off:true(종료·품절로 뺀 것)}, ...] 로 넣어요. 페이지를 열거나 탭을 바꿀 때마다 그중 하나가 무작위로 나와요. */

/* 탭마다 어떤 광고를 보여줄지 */
const TAB_AD = { sell:'toss_stock', us:'toss_stock', div:'toss_stock', avg:'coupang_book', risk:'coupang_book', gold:'toss_stock', ipo:'toss_stock',
  int:'toss_bank', grow:'toss_stock', pen:'toss_stock', fire:'coupang_book', fin:'toss_bank', nhis:'coupang_book', yet:'coupang_book', nps:'coupang_book', sev:'toss_stock', eitc:'toss_bank',
  buy:'coupang_home', dsr:'toss_loan', score:'coupang_home', safe:'coupang_home', rent:'coupang_home', refi:'toss_loan', ptax:'coupang_book', gift:'coupang_book', yield:'toss_loan', auc:'coupang_home', dist:'coupang_book' };
