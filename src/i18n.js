// UI strings, themes and products in English and Korean.
export const LANGS = ['en', 'ko'];

export const T = {
  en: {
    site: 'Arttrip Studio', tagline: 'Masterpieces, ready to use.',
    nav: { col: 'Collections', art: 'Art', illus: 'Originals', studio: 'Studio', shop: 'Shop', account: 'Sign in', myAccount: 'My page', studio: 'Studio', pricing: 'Pricing' },
    heroTitle: 'Beautiful things to print and keep.', heroSub: 'Masterpieces, photographs, lettering and our own illustrations, made into calendars, posters, planners, puzzle books and templates you can use today.',
    browse: 'Browse the collection', shopNow: 'See the planners', themes: 'Themes', newIn: 'From the collection', allArt: 'All artworks',
    by: 'by', artworks: 'artworks', page: 'Page', prev: 'Previous', next: 'Next', related: 'More like this', sameArtist: 'More by',
    palette: 'Colour palette', paletteHint: 'Tap a colour to copy its code.', details: 'Details', artist: 'Artist', date: 'Date', medium: 'Medium', source: 'Source',
    sourceText: 'Art Institute of Chicago, public domain (CC0)', useIt: 'Make something with it', useItSub: 'Turn this artwork into a printable product in the Studio.',
    make: { calendar: 'Calendar', card: 'Greeting card', poster: 'Poster', wallpaper: 'Phone wallpaper' },
    download: 'High-resolution download', downloadSub: 'Print-ready files are included with a subscription.', subscribe: 'Subscribe',
    buy: 'Buy now', guest: 'No account needed', soon: 'Opening soon', instant: 'Instant download', price: 'Price', whatYouGet: 'What you get', products: 'Planners & printables',
    pricingTitle: 'One subscription. Every masterpiece.', pricingSub: 'Download print-ready files of every artwork and every printable. Cancel any time.',
    monthly: 'Monthly', yearly: 'Yearly', perMonth: '/month', perYear: '/year', bestValue: 'Best value',
    planPerks: ['Every artwork in high resolution', 'All planners, calendars and printables', 'Personal and small-shop commercial use', 'New artworks every week'],
    footer: 'Artworks are public-domain works from museum open-access collections. Designs and layouts © Arttrip Studio.',
    langName: 'English', switchTo: '한국어', notFound: 'Page not found', back: 'Back to home', copied: 'Copied',
    kindLabel: (k) => k, about: 'About', license: 'License', privacy: 'Privacy', terms: 'Terms',
  },
  ko: {
    site: '아트트립 스튜디오', tagline: '바로 쓰는 명화',
    nav: { col: '컬렉션', art: '명화', illus: '오리지널', studio: '스튜디오', shop: '상품', account: '로그인', myAccount: '내 정보', studio: '스튜디오', pricing: '구독' },
    heroTitle: '인쇄하고 간직하는 아름다운 디자인', heroSub: '명화, 사진, 글씨, 그리고 우리가 직접 그린 일러스트로 만든 달력, 포스터, 플래너, 퍼즐북, 템플릿을 지금 바로 쓰세요.',
    browse: '명화 둘러보기', shopNow: '플래너 보기', themes: '주제별 보기', newIn: '컬렉션에서', allArt: '전체 작품',
    by: '', artworks: '점', page: '페이지', prev: '이전', next: '다음', related: '비슷한 작품', sameArtist: '같은 화가의 작품',
    palette: '색상 팔레트', paletteHint: '색을 누르면 코드가 복사돼요.', details: '작품 정보', artist: '화가', date: '연도', medium: '재료', source: '출처',
    sourceText: '시카고 미술관, 퍼블릭 도메인(CC0)', useIt: '이 그림으로 만들기', useItSub: '스튜디오에서 이 그림으로 인쇄용 상품을 만들 수 있어요.',
    make: { calendar: '달력', card: '카드', poster: '포스터', wallpaper: '폰 배경화면' },
    download: '고해상도 다운로드', downloadSub: '인쇄용 원본 파일은 구독에 포함돼 있어요.', subscribe: '구독하기',
    buy: '구매하기', soon: '곧 오픈', instant: '즉시 다운로드', price: '가격', whatYouGet: '구성', products: '플래너·인쇄물',
    pricingTitle: '구독 하나로 모든 명화를', pricingSub: '모든 작품과 인쇄물을 인쇄용 파일로 내려받으세요. 언제든 해지할 수 있어요.',
    monthly: '월간', yearly: '연간', perMonth: '/월', perYear: '/년', bestValue: '가장 알뜰',
    planPerks: ['모든 작품 고해상도 원본', '모든 플래너·달력·인쇄물', '개인 및 소규모 상업적 이용', '매주 새 작품 추가'],
    footer: '작품은 미술관 오픈 액세스 컬렉션의 퍼블릭 도메인 작품입니다. 디자인과 레이아웃 © 아트트립 스튜디오.',
    langName: '한국어', switchTo: 'English', notFound: '페이지를 찾을 수 없어요', back: '홈으로', copied: '복사됨',
    kindLabel: (k) => ({ Painting: '회화', Print: '판화', Drawing: '드로잉', Textile: '직물', Book: '책' }[k] || k), about: '소개', license: '이용 범위', privacy: '개인정보', terms: '약관',
    payNote: '로그인 없이 바로 구매할 수 있어요. 해외 결제가 되는 국내 카드(비자·마스터)나 애플페이·구글페이로 결제하세요.',
    payKr: '국내 카드 결제', payKrNote: '국내 신용·체크카드 (원화)', payGlobal: '카드로 바로 구매', payGlobalNote: '비자·마스터 카드 · 애플페이 · 구글페이 (달러 결제)',
    guest: '회원가입 없이 구매 가능',
  },
};

export const THEMES = {
  flowers: { en: 'Flowers', ko: '꽃' }, sea: { en: 'By the Sea', ko: '바다' }, landscapes: { en: 'Landscapes', ko: '풍경' },
  'japanese-prints': { en: 'Japanese Prints', ko: '일본 목판화' }, winter: { en: 'Winter', ko: '겨울' }, cats: { en: 'Cats', ko: '고양이' },
  birds: { en: 'Birds', ko: '새' }, horses: { en: 'Horses', ko: '말' }, 'still-life': { en: 'Still Life', ko: '정물' },
  portraits: { en: 'Portraits', ko: '초상화' }, textiles: { en: 'Patterns & Textiles', ko: '문양·직물' }, masterpieces: { en: 'Masterpieces', ko: '명작' },
};

// Original hand-drawn character illustrations (made with AI tools, finished by hand). Categories and their topics.
export const IL_CATS = {
  everyday: { en: 'Everyday Life', ko: '일상·라이프스타일', topics: [['Cafe girl', '카페 소녀'], ['Reading girl', '책 읽는 소녀'], ['Planner girl', '플래너 쓰는 여성'], ['Working from home', '재택근무'], ['Baking', '요리·베이킹'], ['Shopping day', '쇼핑·외출']] },
  family: { en: 'Family & Baby', ko: '가족·육아', topics: [['Mom and baby', '엄마와 아기'], ['Dad and child', '아빠와 아이'], ['Pregnancy', '임신부'], ['Family picnic', '가족 나들이'], ['Siblings', '형제자매']] },
  wedding: { en: 'Wedding & Love', ko: '결혼·연애', topics: [['Bride and groom', '신랑신부'], ['Proposal', '프러포즈'], ['Date day', '커플 데이트'], ['Bridesmaids', '신부 들러리']] },
  work: { en: 'Jobs & Careers', ko: '직업', topics: [['Teacher', '선생님'], ['Nurse', '간호사'], ['Doctor', '의사'], ['Chef', '셰프'], ['Hairstylist', '미용사'], ['Office worker', '사무직']] },
  wellness: { en: 'Health & Fitness', ko: '건강·운동', topics: [['Yoga', '요가'], ['Running', '러닝'], ['Gym', '헬스'], ['Meditation', '명상']] },
  seasons: { en: 'Seasons & Holidays', ko: '계절·명절', topics: [['Winter girl', '겨울 소녀'], ['Christmas', '크리스마스'], ['Halloween', '할로윈'], ['Spring girl', '봄 소녀'], ['Summer beach', '여름 해변'], ['Autumn girl', '가을 소녀']] },
  fashion: { en: 'Fashion & Beauty', ko: '패션·뷰티', topics: [['Boho woman', '보헤미안 여성'], ['Street style', '패션 소녀'], ['Skincare', '스킨케어']] },
  school: { en: 'Kids & School', ko: '아이·학교', topics: [['Back to school', '학교 가는 아이'], ['Study time', '공부하는 학생'], ['Graduation', '졸업생'], ['Birthday party', '생일 파티 아이']] },
  hobbies: { en: 'Hobbies & Pets', ko: '취미·반려동물', topics: [['Gardening', '정원 가꾸기'], ['Painting', '그림 그리기'], ['Traveler', '여행자'], ['Dog walk', '강아지 산책'], ['Girl with cat', '고양이와 소녀']] },
  diverse: { en: 'Diverse Women', ko: '다양성 세트', topics: [['All skin tones', '다양한 피부색 여성'], ['Curvy women', '다양한 체형'], ['Senior couple', '노년 커플']] },
};
export const IL_STYLES = { en: 'Marker · Coloured pencil · Digital hand-drawn', ko: '마카 · 색연필 · 디지털 손그림' };

// Products. checkout: name of the env var holding the Polar checkout link.
export const PRODUCTS = [
  { slug: '2027-masterpiece-digital-planner', img: '/p/planner-2027.jpg', price: 24, checkout: 'POLAR_PLANNER_2027', payapp: 'PAYAPP_PLANNER_2027', cat: 'planners',
    en: { name: '2027 Digital Planner with 12 Masterpieces', short: 'Hyperlinked iPad planner for GoodNotes and Notability.',
      body: ['A full-year planner with a different masterpiece every month — Hokusai, Monet, Renoir and more.', 'Tap the side tabs to jump to any month; tap a day to open its week.'],
      get: ['101-page hyperlinked PDF (iPad portrait)', 'Year at a glance and 12 monthly calendars', '53 weekly spreads with to-do lists', 'Monthly habit tracker and budget page', 'Notes and dot-grid pages'] },
    ko: { name: '명화 12점이 담긴 2027 디지털 플래너', short: '굿노트·노타빌리티용 하이퍼링크 아이패드 플래너',
      body: ['달마다 다른 명화가 들어간 1년 플래너예요. 호쿠사이, 모네, 르누아르 등.', '옆 탭을 누르면 원하는 달로, 날짜를 누르면 그 주로 바로 이동해요.'],
      get: ['하이퍼링크 PDF 101페이지 (아이패드 세로)', '연간 달력과 월간 달력 12장', '할 일 목록이 있는 주간 페이지 53장', '달마다 습관 트래커와 가계부', '노트·모눈 페이지'] } },
  { slug: '2027-printable-calendar-flowers', img: '/p/calendar-flowers.jpg', price: 6.5, checkout: 'POLAR_CAL_FLOWERS', payapp: 'PAYAPP_CAL_FLOWERS', cat: 'calendars',
    en: { name: '2027 Printable Wall Calendar — Flowers in Art', short: 'A4 + US Letter PDF, 12 floral masterpieces plus a cover.',
      body: ['Print at home or at a copy shop. Weekends are marked and weeks start on Sunday.'], get: ['14-page PDF in A4 and US Letter, 300 dpi', 'Cover + January–December', 'Artwork credits on every page'] },
    ko: { name: '2027 인쇄용 벽걸이 달력 — 꽃 명화', short: 'A4·레터 PDF, 꽃 명화 12점과 표지',
      body: ['집이나 인쇄소에서 바로 인쇄하세요. 주말 표시, 일요일 시작이에요.'], get: ['14페이지 PDF, A4·미국 레터 두 가지, 300dpi', '표지 + 1월~12월', '모든 페이지에 작품 정보'] } },
  { slug: '2027-printable-calendar-sea', img: '/p/calendar-sea.jpg', price: 6.5, checkout: 'POLAR_CAL_SEA', payapp: 'PAYAPP_CAL_SEA', cat: 'calendars',
    en: { name: '2027 Printable Wall Calendar — By the Sea', short: 'A4 + US Letter PDF, 12 seascapes plus a cover.', body: ['Monet, Homer, Manet and more, one coast for every month.'], get: ['14-page PDF in A4 and US Letter, 300 dpi', 'Cover + January–December'] },
    ko: { name: '2027 인쇄용 벽걸이 달력 — 바다 명화', short: 'A4·레터 PDF, 바다 명화 12점과 표지', body: ['모네, 호머, 마네 등 달마다 다른 바다 풍경이에요.'], get: ['14페이지 PDF, A4·미국 레터 두 가지, 300dpi', '표지 + 1월~12월'] } },
  { slug: 'seamless-patterns-flowers', img: '/p/patterns-flowers.jpg', price: 7, checkout: 'POLAR_PATTERNS_FLOWERS', payapp: 'PAYAPP_PATTERNS_FLOWERS', cat: 'patterns',
    en: { name: 'Seamless Patterns from Flower Masterpieces', short: '3000 px repeat tiles for paper, fabric and print-on-demand.', body: ['Made from public-domain flower paintings and woodblock prints.'], get: ['3000 × 3000 px JPG tiles, 300 dpi', 'Personal and small-shop commercial use'] },
    ko: { name: '꽃 명화 반복 패턴 모음', short: '포장지·원단·굿즈용 3000px 반복 패턴', body: ['저작권이 끝난 꽃 그림과 목판화로 만들었어요.'], get: ['3000×3000px JPG, 300dpi', '개인 및 소규모 상업적 이용'] } },
  { slug: 'cozy-cafe-girl-clipart', img: '/p/cafe-girl-clipart.jpg', price: 6.5, checkout: 'POLAR_CLIPART_CAFE_GIRL', payapp: 'PAYAPP_CLIPART_CAFE_GIRL', cat: 'illustrations', il: 'everyday', topic: 0,
    en: { name: 'Cozy Cafe Girl Clipart — 22 Hand-Drawn PNGs', short: 'One sweet character, 22 coffee-day poses. Transparent PNG.',
      body: ['Sipping lattes, reading at a cafe table, working on her laptop, writing in her planner, cuddling a cat and more.', 'Marker-style illustrations created with the help of AI tools, then cleaned and prepared by hand.'],
      get: ['22 transparent PNG files, 300 dpi', 'Personal and small-shop commercial use (up to 500 physical items)', 'Instant download (ZIP)'] },
    ko: { name: '카페 소녀 클립아트 — 손그림 PNG 22종', short: '한 인물의 커피 타임 22가지 동작, 배경 투명 PNG',
      body: ['라테 마시기, 카페에서 책 읽기, 노트북 작업, 플래너 쓰기, 고양이 안기 등 22가지 동작이에요.', 'AI 도구의 도움을 받아 그린 뒤 손으로 다듬은 마카 스타일 일러스트예요.'],
      get: ['배경 투명 PNG 22장, 300dpi', '개인 및 소규모 상업적 이용 (실물 500개까지)', '즉시 다운로드 (ZIP)'] } },
  { slug: 'cozy-cafe-girl-printable-stickers', img: '/p/cafe-girl-stickers.jpg', price: 4.5, checkout: 'POLAR_STICKERS_CAFE_GIRL', payapp: 'PAYAPP_STICKERS_CAFE_GIRL', cat: 'illustrations', il: 'everyday', topic: 0,
    en: { name: 'Cozy Cafe Girl Printable Stickers', short: '22 die-cut stickers to print at home, plus GoodNotes stickers.',
      body: ['Print on sticker paper or use Cricut Print Then Cut. Digital PNG stickers for planner apps are included.', 'Illustrations created with the help of AI tools.'],
      get: ['2 US Letter sticker sheets (PDF + PNG, 300 dpi)', '22 digital stickers for GoodNotes', 'Instant download'] },
    ko: { name: '카페 소녀 인쇄용 스티커', short: '집에서 인쇄하는 스티커 22개 + 굿노트 스티커',
      body: ['스티커 용지에 인쇄하거나 크리컷으로 잘라 쓰세요. 플래너 앱용 디지털 스티커도 들어 있어요.', 'AI 도구의 도움을 받아 그린 일러스트예요.'],
      get: ['레터 용지 스티커 시트 2장 (PDF + PNG, 300dpi)', '굿노트용 디지털 스티커 22개', '즉시 다운로드'] } },
  { slug: 'cozy-days-2027-calendar', img: '/p/calendar-cozy-days.jpg', price: 6.5, checkout: 'POLAR_CAL_COZY_DAYS', payapp: 'PAYAPP_CAL_COZY_DAYS', cat: 'illustrations', il: 'seasons', topic: 0,
    en: { name: 'Cozy Days 2027 — Coloured Pencil Wall Calendar', short: 'Twelve hand-drawn seasonal scenes. A4 + US Letter PDF, print at home.',
      body: ['A gentle year in coloured pencil: hot cocoa in January, cherry blossoms in April, sunflowers in August, a Christmas tree in December.', 'Illustrations created with the help of AI tools, then laid out and finished by hand.'],
      get: ['14-page PDF (cover + 12 months) in A4 and US Letter, 300 dpi', 'Weeks start on Sunday', 'Instant download'] },
    ko: { name: '코지 데이즈 2027 — 색연필 손그림 벽걸이 달력', short: '계절마다 다른 손그림 장면 12장, A4·레터 인쇄용 PDF',
      body: ['1월 코코아, 4월 벚꽃, 8월 해바라기, 12월 크리스마스 트리까지, 색연필로 그린 포근한 1년이에요.', 'AI 도구의 도움을 받아 그린 뒤 손으로 다듬어 만든 달력이에요.'],
      get: ['14페이지 PDF (표지 + 12개월), A4·미국 레터 두 가지, 300dpi', '일요일 시작', '즉시 다운로드'] } },
  { slug: 'masterpiece-word-search-large-print', img: '/p/word-search-large-print.jpg', price: 7, checkout: 'POLAR_WORD_SEARCH', cat: 'puzzles',
    en: { name: 'Masterpiece Word Search: Large Print (Color PDF)', short: '40 large-print puzzles, each paired with a full-page masterpiece. 98-page printable PDF.',
      body: ['Every puzzle faces a great painting, from Monet\'s water lilies to Hokusai\'s Great Wave. Each word list is written to match its picture, and a gentle Look Closer question invites you to notice more.', 'Large, clear letters and easy directions only (across, down and diagonal). No backwards words. Full solutions at the back.'],
      get: ['98-page PDF, US Letter (prints on A4 too)', '40 word search puzzles in large print (21 pt grid letters)', '40 full-page masterpieces in color with title, artist and date', 'Complete solutions', 'Print as many copies as you like for personal use'] },
    ko: { name: '명화 큰 글씨 낱말 찾기 (컬러 PDF)', short: '명화 한 점과 짝을 이룬 큰 글씨 낱말 찾기 40개. 98쪽 인쇄용 PDF.',
      body: ['퍼즐마다 모네의 수련부터 호쿠사이의 큰 파도까지, 명화 한 점이 마주 보고 있어요. 단어 목록은 그림에 맞춰 골랐고, "자세히 보기" 질문이 그림을 한 번 더 보게 해 줘요.', '글자가 크고 또렷하며, 방향은 가로·세로·대각선만 써요. 거꾸로 쓴 단어는 없어요. 정답은 책 뒤에 있어요. (퍼즐은 영어 단어예요)'],
      get: ['98쪽 PDF, 미국 레터 크기 (A4로도 인쇄 가능)', '큰 글씨 낱말 찾기 40개 (격자 글자 21pt)', '컬러 명화 40점 (제목·화가·연도)', '전체 정답', '개인용으로 원하는 만큼 인쇄'] } },
  { slug: 'korean-word-search-large-print', img: '/p/word-search-ko.jpg', price: 7, checkout: 'POLAR_WS_KO', cat: 'puzzles',
    en: { name: 'Korean Word Search: Large Print (Color PDF)', short: '30 Hangul word search puzzles in large print, each with a full-page painting. 76-page PDF.', body: ['A word search book written entirely in Korean: every grid is made of Hangul syllables, every list is themed, and each puzzle faces a painting with its Korean title.', 'Large, clear letters and easy directions only (across, down and diagonal). Full solutions at the back.'], get: ['76-page PDF, US Letter (prints on A4 too)', '30 Hangul word search puzzles (24 pt grid letters)', '30 full-page paintings in color', 'Complete solutions'] },
    ko: { name: '명화 낱말 찾기: 큰 글씨 (컬러 PDF)', short: '한글 낱말 찾기 30개와 명화 30점. 76쪽 인쇄용 PDF.', body: ['처음부터 끝까지 한글로 만든 낱말 찾기 책이에요. 글자판은 한글 음절로, 낱말 목록은 주제별로 골랐고, 퍼즐마다 한글 제목이 달린 명화가 마주 보고 있어요.', '글자가 크고 또렷하며, 방향은 가로·세로·대각선만 써요. 정답은 책 뒤에 있어요. 부모님, 어르신 선물로 좋아요.'], get: ['76쪽 PDF, 미국 레터 크기 (A4로도 인쇄 가능)', '한글 낱말 찾기 30개 (글자판 24pt)', '컬러 명화 30점', '전체 정답'] } },
  { slug: 'japanese-word-search-large-print', img: '/p/word-search-ja.jpg', price: 7, checkout: 'POLAR_WS_JA', cat: 'puzzles',
    en: { name: 'Japanese Word Search: Large Print (Color PDF)', short: '30 katakana word search puzzles in large print, each with a full-page painting. 76-page PDF.', body: ['A word search book written in Japanese: katakana grids, themed word lists and Japanese instructions, with a full-page painting facing every puzzle.', 'Great for Japanese learners and native readers alike. Easy directions only and full solutions at the back.'], get: ['76-page PDF, US Letter (prints on A4 too)', '30 katakana word search puzzles (24 pt grid letters)', '30 full-page paintings in color', 'Complete solutions'] },
    ko: { name: '일본어 낱말 찾기: 큰 글씨 (컬러 PDF)', short: '가타카나 낱말 찾기 30개와 명화 30점. 76쪽 인쇄용 PDF.', body: ['일본어로 만든 낱말 찾기 책이에요. 가타카나 글자판, 주제별 낱말 목록, 일본어 설명에 퍼즐마다 명화 한 점이 마주 보고 있어요.', '일본어를 공부하는 분에게도, 일본어가 모국어인 분에게도 좋아요. 정답은 책 뒤에 있어요.'], get: ['76쪽 PDF, 미국 레터 크기 (A4로도 인쇄 가능)', '가타카나 낱말 찾기 30개 (글자판 24pt)', '컬러 명화 30점', '전체 정답'] } },
  { slug: 'latin-word-search-large-print', img: '/p/word-search-la.jpg', price: 7, checkout: 'POLAR_WS_LA', cat: 'puzzles',
    en: { name: 'Latin Word Search: Large Print (Color PDF)', short: '30 Latin puzzles with English meanings and a painting for every theme. 76-page PDF.', body: ['Learn Latin one painting at a time. Every puzzle has a Latin theme, from the garden and the sea to the stars and the old myths, and every word comes with its English meaning.', 'Nearly 400 Latin words in large, clear type. Easy directions only and full solutions at the back.'], get: ['76-page PDF, US Letter (prints on A4 too)', '30 Latin word search puzzles with English meanings', '30 full-page paintings in color', 'Complete solutions'] },
    ko: { name: '라틴어 낱말 찾기: 큰 글씨 (컬러 PDF)', short: '영어 뜻이 달린 라틴어 퍼즐 30개와 명화 30점. 76쪽 인쇄용 PDF.', body: ['명화 한 점씩 보며 라틴어를 익혀요. 정원, 바다, 별, 신화까지 주제마다 라틴어 낱말이 있고, 낱말마다 영어 뜻이 함께 있어요.', '라틴어 낱말 약 400개를 큰 글씨로 담았어요. 정답은 책 뒤에 있어요. (설명은 영어예요)'], get: ['76쪽 PDF, 미국 레터 크기 (A4로도 인쇄 가능)', '영어 뜻이 달린 라틴어 낱말 찾기 30개', '컬러 명화 30점', '전체 정답'] } },
  { slug: 'scripture-lettering-posters-kjv', img: '/p/lettering-kjv.jpg', price: 6, checkout: 'POLAR_LT_KJV', cat: 'originals', line: 'lettering',
    en: { name: 'Scripture Lettering Posters (KJV), 12 Designs', short: 'Twelve beloved verses from the King James Version, set as calm typographic posters.', body: ['Psalm 23, Isaiah 40:31, Jeremiah 29:11, John 3:16 and eight more favorites, each set in a quiet, modern layout with a soft palette of cream, sage, blush, navy and terracotta.', 'Every file is vector, so the same design prints crisp as a small card or a large wall poster.'], get: ['12 poster designs', 'Vector PDFs in 5 frame ratios: 2x3, 3x4, 4x5, 11x14 and ISO A (A5 to A1)', 'Prints sharp at any size, from 4x6 to 24x36 in', 'Personal use'] },
    ko: { name: '성경 말씀 포스터 (KJV 영어), 12종', short: '킹제임스 영어 성경의 사랑받는 말씀 12구절을 차분한 글씨 포스터로.', body: ['시편 23편, 이사야 40:31, 예레미야 29:11, 요한복음 3:16 등 12구절을 크림, 세이지, 블러시, 네이비, 테라코타 색으로 담았어요.', '모두 벡터 파일이라 작은 카드부터 큰 벽 포스터까지 선명하게 인쇄돼요.'], get: ['포스터 디자인 12종', '5가지 액자 비율의 벡터 PDF: 2x3, 3x4, 4x5, 11x14, ISO A (A5~A1)', '엽서 크기부터 24x36인치 대형까지 선명하게 인쇄', '개인 사용'] } },
  { slug: 'korean-scripture-posters', img: '/p/lettering-kor.jpg', price: 6, checkout: 'POLAR_LT_KOR', cat: 'originals', line: 'lettering',
    en: { name: 'Korean Scripture Posters, 12 Designs', short: 'Twelve verses in Korean (Korean Revised Version, 1961), set as modern Hangul typography.', body: ['Psalm 23:1, Joshua 1:9, Matthew 11:28, 1 Thessalonians 5:16-18 and more, in the classic 1961 Korean translation, which is now in the public domain.', 'A thoughtful gift for Korean churches, families and friends anywhere in the world.'], get: ['12 poster designs', 'Vector PDFs in 5 frame ratios: 2x3, 3x4, 4x5, 11x14 and ISO A (A5 to A1)', 'Prints sharp at any size, from 4x6 to 24x36 in', 'Personal use'] },
    ko: { name: '한글 성경 말씀 포스터 (개역한글), 12종', short: '개역한글 성경 말씀 12구절을 요즘 감성의 한글 글씨 포스터로.', body: ['시편 23:1, 여호수아 1:9, 마태복음 11:28, 데살로니가전서 5:16-18 등 사랑받는 말씀을 개역한글판(1961) 본문 그대로 담았어요.', '교회, 가정, 선물용으로 좋아요. 벡터 파일이라 크게 인쇄해도 선명해요.'], get: ['포스터 디자인 12종', '5가지 액자 비율의 벡터 PDF: 2x3, 3x4, 4x5, 11x14, ISO A (A5~A1)', '엽서 크기부터 24x36인치 대형까지 선명하게 인쇄', '개인 사용'] } },
  { slug: 'latin-lettering-posters', img: '/p/lettering-latin.jpg', price: 6, checkout: 'POLAR_LT_LATIN', cat: 'originals', line: 'lettering',
    en: { name: 'Latin Lettering Posters, 12 Designs', short: 'Carpe diem, Amor vincit omnia, Per aspera ad astra and nine more classic Latin phrases.', body: ['Twelve timeless Latin phrases set in elegant classical type, each with a small English translation underneath.', 'Perfect for a study, a classroom or a reading corner.'], get: ['12 poster designs', 'Vector PDFs in 5 frame ratios: 2x3, 3x4, 4x5, 11x14 and ISO A (A5 to A1)', 'Prints sharp at any size, from 4x6 to 24x36 in', 'Personal use'] },
    ko: { name: '라틴어 글씨 포스터, 12종', short: 'Carpe diem, Amor vincit omnia, Per aspera ad astra 등 고전 라틴어 문구 12개.', body: ['오래 사랑받아 온 라틴어 문구 12개를 고전적인 글씨로 담고, 아래에 작은 영어 뜻을 달았어요.', '서재, 교실, 책 읽는 공간에 잘 어울려요.'], get: ['포스터 디자인 12종', '5가지 액자 비율의 벡터 PDF: 2x3, 3x4, 4x5, 11x14, ISO A (A5~A1)', '엽서 크기부터 24x36인치 대형까지 선명하게 인쇄', '개인 사용'] } },
  { slug: 'hangul-typography-posters', img: '/p/lettering-hangul.jpg', price: 6, checkout: 'POLAR_LT_HANGUL', cat: 'originals', line: 'lettering',
    en: { name: 'Hangul Typography Posters, 12 Designs', short: 'Twelve warm Korean phrases in Hangul-only typography, from bold modern to handwritten.', body: ['Phrases like "It is okay to go slowly" and "Thank you, I love you", designed with Hangul letters alone, so they read as both words and pattern.', 'A beautiful way to bring Korean lettering into any home.'], get: ['12 poster designs', 'Vector PDFs in 5 frame ratios: 2x3, 3x4, 4x5, 11x14 and ISO A (A5 to A1)', 'Prints sharp at any size, from 4x6 to 24x36 in', 'Personal use'] },
    ko: { name: '한글 타이포그래피 포스터, 12종', short: '"천천히 가도 괜찮아", "고마워 사랑해" 등 한글만으로 만든 따뜻한 글씨 포스터 12종.', body: ['한글만으로 디자인해서 글자이면서 무늬처럼 보이는 포스터예요. 굵은 고딕부터 손글씨까지 여러 느낌으로 만들었어요.', '집, 카페, 선물용으로 좋아요. 벡터 파일이라 크게 인쇄해도 선명해요.'], get: ['포스터 디자인 12종', '5가지 액자 비율의 벡터 PDF: 2x3, 3x4, 4x5, 11x14, ISO A (A5~A1)', '엽서 크기부터 24x36인치 대형까지 선명하게 인쇄', '개인 사용'] } },
  { slug: 'timeless-quotes-lettering-posters', img: '/p/lettering-quotes.jpg', price: 6, checkout: 'POLAR_LT_QUOTES', cat: 'originals', line: 'lettering',
    en: { name: 'Timeless Quotes Lettering Posters, 12 Designs', short: 'Emerson, Van Gogh, Shakespeare, Marie Curie, Keats and more, each signed with its author.', body: ['Twelve well-documented sayings from writers, artists and scientists who lived long ago, set in warm editorial type with the author\'s name beneath.', 'From "Love all, trust a few, do wrong to none" to "The mountains are calling and I must go." Lovely for a living room, a study or a gift.'], get: ['12 poster designs', 'Vector PDFs in 5 frame ratios: 2x3, 3x4, 4x5, 11x14 and ISO A (A5 to A1)', 'Prints sharp at any size, from 4x6 to 24x36 in', 'Personal use'] },
    ko: { name: '영어 명언 레터링 포스터, 12종', short: '에머슨, 반 고흐, 셰익스피어, 마리 퀴리, 키츠 등. 모든 포스터에 말한 사람의 이름을 넣었어요.', body: ['오래전 작가, 화가, 과학자들이 남긴 출처가 분명한 명언 12개를 따뜻한 글씨로 담고, 아래에 말한 사람의 이름을 적었어요.', '"모두를 사랑하되 소수를 믿어라"부터 "산이 부르고 있으니 나는 가야 한다"까지. 거실, 서재, 선물용으로 좋아요.'], get: ['포스터 디자인 12종', '5가지 액자 비율의 벡터 PDF: 2x3, 3x4, 4x5, 11x14, ISO A (A5~A1)', '엽서 크기부터 24x36인치 대형까지 선명하게 인쇄', '개인 사용'] } },
  { slug: 'korean-quotes-lettering-posters', img: '/p/lettering-koquotes.jpg', price: 6, checkout: 'POLAR_LT_KOQ', cat: 'originals', line: 'lettering',
    en: { name: 'Korean Classic Quotes Posters, 12 Designs', short: 'Kim Gu, Yun Dong-ju, Ahn Jung-geun, Admiral Yi, Confucius and more, in Korean type.', body: ['Twelve beloved lines in Korean: Kim Gu\'s wish for "the most beautiful nation", the opening of Yun Dong-ju\'s Prelude, Kim Sowol\'s mountain flowers and more, each with its source.', 'A meaningful gift for Korean families and Hangul lovers.'], get: ['12 poster designs', 'Vector PDFs in 5 frame ratios: 2x3, 3x4, 4x5, 11x14 and ISO A (A5 to A1)', 'Prints sharp at any size, from 4x6 to 24x36 in', 'Personal use'] },
    ko: { name: '한글 명언 포스터, 12종', short: '김구, 윤동주, 안중근, 이순신, 공자, 김소월 등. 출처까지 함께 적은 한글 명언 12종.', body: ['"나는 우리나라가 세계에서 가장 아름다운 나라가 되기를 원한다", "죽는 날까지 하늘을 우러러", "하루라도 책을 읽지 않으면" 같은 오래 사랑받은 문장을 담았어요.', '모든 포스터에 누구의 말인지, 어디에 나온 말인지 함께 적었어요. 거실, 공부방, 선물용으로 좋아요.'], get: ['포스터 디자인 12종', '5가지 액자 비율의 벡터 PDF: 2x3, 3x4, 4x5, 11x14, ISO A (A5~A1)', '엽서 크기부터 24x36인치 대형까지 선명하게 인쇄', '개인 사용'] } },
  { slug: 'buddhist-sutra-lettering-posters', img: '/p/lettering-sutra.jpg', price: 6, checkout: 'POLAR_LT_SUTRA', cat: 'originals', line: 'lettering',
    en: { name: 'Buddhist Sutra Lettering Posters, 13 Designs', short: 'Twelve sutra verses in Korean with the classical Chinese, plus the full Heart Sutra in 260 characters.', body: ['Verses from the Diamond Sutra, the Heart Sutra, the Avatamsaka Sutra, the Dhammapada and the Sutta Nipata, in calm Korean type with the original Chinese beneath.', 'Includes a bonus poster of the complete Heart Sutra (Xuanzang\'s Chinese text) set in a 13 x 20 grid, like a hand-copied sutra.'], get: ['13 poster designs', 'Vector PDFs in 5 frame ratios: 2x3, 3x4, 4x5, 11x14 and ISO A (A5 to A1)', 'Prints sharp at any size, from 4x6 to 24x36 in', 'Personal use'] },
    ko: { name: '불경 글씨 포스터, 13종', short: '금강경, 반야심경, 화엄경, 법구경, 숫타니파타 구절 12종과 반야심경 260자 전문 포스터.', body: ['"모든 것은 오직 마음이 짓는다", "머무는 곳 없이 그 마음을 내어라", "무소의 뿔처럼 혼자서 가라" 같은 구절을 고요한 한글 글씨로 담고, 아래에 한문 원문과 출처를 적었어요.', '보너스로 반야심경 260자 전문을 사경처럼 13×20 칸에 담은 포스터가 들어 있어요.'], get: ['포스터 디자인 13종', '5가지 액자 비율의 벡터 PDF: 2x3, 3x4, 4x5, 11x14, ISO A (A5~A1)', '엽서 크기부터 24x36인치 대형까지 선명하게 인쇄', '개인 사용'] } },
  { slug: 'masterpiece-junk-journal-art-paper-kit', img: '/p/art-paper-kit.jpg', price: 8, checkout: 'POLAR_ART_PAPER_KIT', cat: 'planners', editor: 'botanical',
    en: { name: 'Masterpiece Junk Journal Art Paper Kit + Editor', short: '14 vintage art papers, stamps, tickets, tags and washi strips. Edit every page online.',
      body: ['Aged papers, museum tickets, postage stamps, tags, labels, postcards, journaling cards and printable washi strips, all made from public-domain masterpieces.', 'Every design opens in the Arttrip Editor: swap the paintings, add your own photos and words, change colours and paper, then download a print-ready PDF.'],
      get: ['14 designs × A4 and US Letter (28 pages, 300 dpi PDF)', 'Full-quality Arttrip Editor access (license key in your receipt)', 'Add your own photos and text, change any painting', 'Personal use and small craft projects'] },
    ko: { name: '명화 정크저널 아트페이퍼 키트 + 편집기', short: '빈티지 아트페이퍼, 우표, 티켓, 꼬리표, 마스킹 테이프 14종. 모든 페이지를 온라인에서 편집해요.',
      body: ['오래된 종이 질감의 아트페이퍼, 미술관 티켓, 우표, 꼬리표, 라벨, 엽서, 저널링 카드, 인쇄용 마스킹 테이프까지 모두 퍼블릭 도메인 명화로 만들었어요.', '모든 디자인은 아트트립 에디터에서 열려요. 그림을 바꾸고, 내 사진과 글을 넣고, 색과 종이를 바꾼 뒤 인쇄용 PDF로 받으세요.'],
      get: ['14가지 디자인 × A4·미국 레터 (28페이지, 300dpi PDF)', '아트트립 에디터 고화질 이용권 (영수증의 라이선스 키)', '내 사진·글 넣기, 그림 바꾸기 자유', '개인용·소규모 공예용'] } },
];

const COLOR_NAMES = [
  ['#000000', 'black', '검정'], ['#ffffff', 'white', '흰색'], ['#808080', 'grey', '회색'], ['#c0c0c0', 'silver', '은회색'], ['#f5f0e6', 'ivory', '아이보리'],
  ['#e8d8b8', 'sand', '모래색'], ['#c8a165', 'ochre', '황토색'], ['#8b5a2b', 'brown', '갈색'], ['#5c4033', 'umber', '암갈색'], ['#d2b48c', 'tan', '연갈색'],
  ['#b22222', 'red', '빨강'], ['#8b1a1a', 'crimson', '진홍'], ['#e9967a', 'salmon', '연어색'], ['#ff8c00', 'orange', '주황'], ['#ffd700', 'gold', '금색'],
  ['#f0e68c', 'pale yellow', '연노랑'], ['#556b2f', 'olive', '올리브'], ['#2e8b57', 'green', '초록'], ['#8fbc8f', 'sage', '세이지'], ['#20b2aa', 'teal', '청록'],
  ['#87ceeb', 'sky blue', '하늘색'], ['#4682b4', 'steel blue', '강철 파랑'], ['#1e3a8a', 'navy', '남색'], ['#191970', 'midnight blue', '짙은 남색'], ['#6a5acd', 'violet', '보라'],
  ['#d8bfd8', 'lilac', '라일락'], ['#ffc0cb', 'pink', '분홍'], ['#2f4f4f', 'slate', '짙은 회청색'],
];
export function colorName(hex, lang) {
  const p = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const c = p(hex); let best = null, bd = 1e9;
  for (const [h, en, ko] of COLOR_NAMES) { const q = p(h); const d = (c[0] - q[0]) ** 2 * 0.3 + (c[1] - q[1]) ** 2 * 0.59 + (c[2] - q[2]) ** 2 * 0.11; if (d < bd) { bd = d; best = lang === 'ko' ? ko : en; } }
  return best;
}

// Artist wall calendars (generated from /home/claude/artcal). Spread into PRODUCTS below.
export const ARTIST_CALS = [
 {
  "slug": "2027-claude-monet-wall-calendar",
  "img": "/p/cal-claude-monet.jpg",
  "price": 6.5,
  "checkout": "POLAR_CAL_CLAUDE_MONET",
  "payapp": "PAYAPP_CAL_CLAUDE_MONET",
  "cat": "artist-calendars",
  "artist_slug": "claude-monet",
  "en": {
   "name": "Claude Monet 2027 Wall Calendar",
   "short": "Twelve masterpieces by Claude Monet, one for every month. A4 + US Letter PDF.",
   "body": [
    "A full year with Claude Monet: twelve public-domain works from the Art Institute of Chicago, each with its title and date.",
    "Print at home or at a copy shop. Weeks start on Sunday."
   ],
   "get": [
    "14-page PDF (cover, 12 months, artwork list) in A4 and US Letter, 300 dpi",
    "Instant download",
    "Personal use and gifts"
   ]
  },
  "ko": {
   "name": "클로드 모네 2027 벽걸이 달력",
   "short": "클로드 모네의 명화 12점, 달마다 한 작품. A4·레터 PDF.",
   "body": [
    "클로드 모네의 작품 12점으로 채운 1년 달력이에요. 시카고 미술관이 공개한 퍼블릭 도메인 작품이고, 작품명과 연도가 함께 실려 있어요.",
    "집이나 인쇄소에서 바로 인쇄하세요. 일요일 시작이에요."
   ],
   "get": [
    "14페이지 PDF (표지, 12개월, 작품 목록), A4·미국 레터 두 가지, 300dpi",
    "즉시 다운로드",
    "개인 사용·선물용"
   ]
  }
 },
 {
  "slug": "2027-edouard-manet-wall-calendar",
  "img": "/p/cal-edouard-manet.jpg",
  "price": 6.5,
  "checkout": "POLAR_CAL_EDOUARD_MANET",
  "payapp": "PAYAPP_CAL_EDOUARD_MANET",
  "cat": "artist-calendars",
  "artist_slug": "edouard-manet",
  "en": {
   "name": "Édouard Manet 2027 Wall Calendar",
   "short": "Twelve masterpieces by Édouard Manet, one for every month. A4 + US Letter PDF.",
   "body": [
    "A full year with Édouard Manet: twelve public-domain works from the Art Institute of Chicago, each with its title and date.",
    "Print at home or at a copy shop. Weeks start on Sunday."
   ],
   "get": [
    "14-page PDF (cover, 12 months, artwork list) in A4 and US Letter, 300 dpi",
    "Instant download",
    "Personal use and gifts"
   ]
  },
  "ko": {
   "name": "에두아르 마네 2027 벽걸이 달력",
   "short": "에두아르 마네의 명화 12점, 달마다 한 작품. A4·레터 PDF.",
   "body": [
    "에두아르 마네의 작품 12점으로 채운 1년 달력이에요. 시카고 미술관이 공개한 퍼블릭 도메인 작품이고, 작품명과 연도가 함께 실려 있어요.",
    "집이나 인쇄소에서 바로 인쇄하세요. 일요일 시작이에요."
   ],
   "get": [
    "14페이지 PDF (표지, 12개월, 작품 목록), A4·미국 레터 두 가지, 300dpi",
    "즉시 다운로드",
    "개인 사용·선물용"
   ]
  }
 },
 {
  "slug": "2027-pierre-auguste-renoir-wall-calendar",
  "img": "/p/cal-pierre-auguste-renoir.jpg",
  "price": 6.5,
  "checkout": "POLAR_CAL_PIERRE_AUGUSTE_RENOIR",
  "payapp": "PAYAPP_CAL_PIERRE_AUGUSTE_RENOIR",
  "cat": "artist-calendars",
  "artist_slug": "pierre-auguste-renoir",
  "en": {
   "name": "Pierre-Auguste Renoir 2027 Wall Calendar",
   "short": "Twelve masterpieces by Pierre-Auguste Renoir, one for every month. A4 + US Letter PDF.",
   "body": [
    "A full year with Pierre-Auguste Renoir: twelve public-domain works from the Art Institute of Chicago, each with its title and date.",
    "Print at home or at a copy shop. Weeks start on Sunday."
   ],
   "get": [
    "14-page PDF (cover, 12 months, artwork list) in A4 and US Letter, 300 dpi",
    "Instant download",
    "Personal use and gifts"
   ]
  },
  "ko": {
   "name": "피에르 오귀스트 르누아르 2027 벽걸이 달력",
   "short": "피에르 오귀스트 르누아르의 명화 12점, 달마다 한 작품. A4·레터 PDF.",
   "body": [
    "피에르 오귀스트 르누아르의 작품 12점으로 채운 1년 달력이에요. 시카고 미술관이 공개한 퍼블릭 도메인 작품이고, 작품명과 연도가 함께 실려 있어요.",
    "집이나 인쇄소에서 바로 인쇄하세요. 일요일 시작이에요."
   ],
   "get": [
    "14페이지 PDF (표지, 12개월, 작품 목록), A4·미국 레터 두 가지, 300dpi",
    "즉시 다운로드",
    "개인 사용·선물용"
   ]
  }
 },
 {
  "slug": "2027-paul-cezanne-wall-calendar",
  "img": "/p/cal-paul-cezanne.jpg",
  "price": 6.5,
  "checkout": "POLAR_CAL_PAUL_CEZANNE",
  "payapp": "PAYAPP_CAL_PAUL_CEZANNE",
  "cat": "artist-calendars",
  "artist_slug": "paul-cezanne",
  "en": {
   "name": "Paul Cézanne 2027 Wall Calendar",
   "short": "Twelve masterpieces by Paul Cézanne, one for every month. A4 + US Letter PDF.",
   "body": [
    "A full year with Paul Cézanne: twelve public-domain works from the Art Institute of Chicago, each with its title and date.",
    "Print at home or at a copy shop. Weeks start on Sunday."
   ],
   "get": [
    "14-page PDF (cover, 12 months, artwork list) in A4 and US Letter, 300 dpi",
    "Instant download",
    "Personal use and gifts"
   ]
  },
  "ko": {
   "name": "폴 세잔 2027 벽걸이 달력",
   "short": "폴 세잔의 명화 12점, 달마다 한 작품. A4·레터 PDF.",
   "body": [
    "폴 세잔의 작품 12점으로 채운 1년 달력이에요. 시카고 미술관이 공개한 퍼블릭 도메인 작품이고, 작품명과 연도가 함께 실려 있어요.",
    "집이나 인쇄소에서 바로 인쇄하세요. 일요일 시작이에요."
   ],
   "get": [
    "14페이지 PDF (표지, 12개월, 작품 목록), A4·미국 레터 두 가지, 300dpi",
    "즉시 다운로드",
    "개인 사용·선물용"
   ]
  }
 },
 {
  "slug": "2027-vincent-van-gogh-wall-calendar",
  "img": "/p/cal-vincent-van-gogh.jpg",
  "price": 6.5,
  "checkout": "POLAR_CAL_VINCENT_VAN_GOGH",
  "payapp": "PAYAPP_CAL_VINCENT_VAN_GOGH",
  "cat": "artist-calendars",
  "artist_slug": "vincent-van-gogh",
  "en": {
   "name": "Vincent van Gogh 2027 Wall Calendar",
   "short": "Twelve masterpieces by Vincent van Gogh, one for every month. A4 + US Letter PDF.",
   "body": [
    "A full year with Vincent van Gogh: twelve public-domain works from the Art Institute of Chicago, each with its title and date.",
    "Print at home or at a copy shop. Weeks start on Sunday."
   ],
   "get": [
    "14-page PDF (cover, 12 months, artwork list) in A4 and US Letter, 300 dpi",
    "Instant download",
    "Personal use and gifts"
   ]
  },
  "ko": {
   "name": "빈센트 반 고흐 2027 벽걸이 달력",
   "short": "빈센트 반 고흐의 명화 12점, 달마다 한 작품. A4·레터 PDF.",
   "body": [
    "빈센트 반 고흐의 작품 12점으로 채운 1년 달력이에요. 시카고 미술관이 공개한 퍼블릭 도메인 작품이고, 작품명과 연도가 함께 실려 있어요.",
    "집이나 인쇄소에서 바로 인쇄하세요. 일요일 시작이에요."
   ],
   "get": [
    "14페이지 PDF (표지, 12개월, 작품 목록), A4·미국 레터 두 가지, 300dpi",
    "즉시 다운로드",
    "개인 사용·선물용"
   ]
  }
 },
 {
  "slug": "2027-camille-pissarro-wall-calendar",
  "img": "/p/cal-camille-pissarro.jpg",
  "price": 6.5,
  "checkout": "POLAR_CAL_CAMILLE_PISSARRO",
  "payapp": "PAYAPP_CAL_CAMILLE_PISSARRO",
  "cat": "artist-calendars",
  "artist_slug": "camille-pissarro",
  "en": {
   "name": "Camille Pissarro 2027 Wall Calendar",
   "short": "Twelve masterpieces by Camille Pissarro, one for every month. A4 + US Letter PDF.",
   "body": [
    "A full year with Camille Pissarro: twelve public-domain works from the Art Institute of Chicago, each with its title and date.",
    "Print at home or at a copy shop. Weeks start on Sunday."
   ],
   "get": [
    "14-page PDF (cover, 12 months, artwork list) in A4 and US Letter, 300 dpi",
    "Instant download",
    "Personal use and gifts"
   ]
  },
  "ko": {
   "name": "카미유 피사로 2027 벽걸이 달력",
   "short": "카미유 피사로의 명화 12점, 달마다 한 작품. A4·레터 PDF.",
   "body": [
    "카미유 피사로의 작품 12점으로 채운 1년 달력이에요. 시카고 미술관이 공개한 퍼블릭 도메인 작품이고, 작품명과 연도가 함께 실려 있어요.",
    "집이나 인쇄소에서 바로 인쇄하세요. 일요일 시작이에요."
   ],
   "get": [
    "14페이지 PDF (표지, 12개월, 작품 목록), A4·미국 레터 두 가지, 300dpi",
    "즉시 다운로드",
    "개인 사용·선물용"
   ]
  }
 },
 {
  "slug": "2027-mary-cassatt-wall-calendar",
  "img": "/p/cal-mary-cassatt.jpg",
  "price": 6.5,
  "checkout": "POLAR_CAL_MARY_CASSATT",
  "payapp": "PAYAPP_CAL_MARY_CASSATT",
  "cat": "artist-calendars",
  "artist_slug": "mary-cassatt",
  "en": {
   "name": "Mary Cassatt 2027 Wall Calendar",
   "short": "Twelve masterpieces by Mary Cassatt, one for every month. A4 + US Letter PDF.",
   "body": [
    "A full year with Mary Cassatt: twelve public-domain works from the Art Institute of Chicago, each with its title and date.",
    "Print at home or at a copy shop. Weeks start on Sunday."
   ],
   "get": [
    "14-page PDF (cover, 12 months, artwork list) in A4 and US Letter, 300 dpi",
    "Instant download",
    "Personal use and gifts"
   ]
  },
  "ko": {
   "name": "메리 카사트 2027 벽걸이 달력",
   "short": "메리 카사트의 명화 12점, 달마다 한 작품. A4·레터 PDF.",
   "body": [
    "메리 카사트의 작품 12점으로 채운 1년 달력이에요. 시카고 미술관이 공개한 퍼블릭 도메인 작품이고, 작품명과 연도가 함께 실려 있어요.",
    "집이나 인쇄소에서 바로 인쇄하세요. 일요일 시작이에요."
   ],
   "get": [
    "14페이지 PDF (표지, 12개월, 작품 목록), A4·미국 레터 두 가지, 300dpi",
    "즉시 다운로드",
    "개인 사용·선물용"
   ]
  }
 },
 {
  "slug": "2027-paul-gauguin-wall-calendar",
  "img": "/p/cal-paul-gauguin.jpg",
  "price": 6.5,
  "checkout": "POLAR_CAL_PAUL_GAUGUIN",
  "payapp": "PAYAPP_CAL_PAUL_GAUGUIN",
  "cat": "artist-calendars",
  "artist_slug": "paul-gauguin",
  "en": {
   "name": "Paul Gauguin 2027 Wall Calendar",
   "short": "Twelve masterpieces by Paul Gauguin, one for every month. A4 + US Letter PDF.",
   "body": [
    "A full year with Paul Gauguin: twelve public-domain works from the Art Institute of Chicago, each with its title and date.",
    "Print at home or at a copy shop. Weeks start on Sunday."
   ],
   "get": [
    "14-page PDF (cover, 12 months, artwork list) in A4 and US Letter, 300 dpi",
    "Instant download",
    "Personal use and gifts"
   ]
  },
  "ko": {
   "name": "폴 고갱 2027 벽걸이 달력",
   "short": "폴 고갱의 명화 12점, 달마다 한 작품. A4·레터 PDF.",
   "body": [
    "폴 고갱의 작품 12점으로 채운 1년 달력이에요. 시카고 미술관이 공개한 퍼블릭 도메인 작품이고, 작품명과 연도가 함께 실려 있어요.",
    "집이나 인쇄소에서 바로 인쇄하세요. 일요일 시작이에요."
   ],
   "get": [
    "14페이지 PDF (표지, 12개월, 작품 목록), A4·미국 레터 두 가지, 300dpi",
    "즉시 다운로드",
    "개인 사용·선물용"
   ]
  }
 },
 {
  "slug": "2027-henri-de-toulouse-lautrec-wall-calendar",
  "img": "/p/cal-henri-de-toulouse-lautrec.jpg",
  "price": 6.5,
  "checkout": "POLAR_CAL_HENRI_DE_TOULOUSE_LAUTREC",
  "payapp": "PAYAPP_CAL_HENRI_DE_TOULOUSE_LAUTREC",
  "cat": "artist-calendars",
  "artist_slug": "henri-de-toulouse-lautrec",
  "en": {
   "name": "Toulouse-Lautrec 2027 Wall Calendar",
   "short": "Twelve masterpieces by Toulouse-Lautrec, one for every month. A4 + US Letter PDF.",
   "body": [
    "A full year with Toulouse-Lautrec: twelve public-domain works from the Art Institute of Chicago, each with its title and date.",
    "Print at home or at a copy shop. Weeks start on Sunday."
   ],
   "get": [
    "14-page PDF (cover, 12 months, artwork list) in A4 and US Letter, 300 dpi",
    "Instant download",
    "Personal use and gifts"
   ]
  },
  "ko": {
   "name": "툴루즈 로트레크 2027 벽걸이 달력",
   "short": "툴루즈 로트레크의 명화 12점, 달마다 한 작품. A4·레터 PDF.",
   "body": [
    "툴루즈 로트레크의 작품 12점으로 채운 1년 달력이에요. 시카고 미술관이 공개한 퍼블릭 도메인 작품이고, 작품명과 연도가 함께 실려 있어요.",
    "집이나 인쇄소에서 바로 인쇄하세요. 일요일 시작이에요."
   ],
   "get": [
    "14페이지 PDF (표지, 12개월, 작품 목록), A4·미국 레터 두 가지, 300dpi",
    "즉시 다운로드",
    "개인 사용·선물용"
   ]
  }
 },
 {
  "slug": "2027-odilon-redon-wall-calendar",
  "img": "/p/cal-odilon-redon.jpg",
  "price": 6.5,
  "checkout": "POLAR_CAL_ODILON_REDON",
  "payapp": "PAYAPP_CAL_ODILON_REDON",
  "cat": "artist-calendars",
  "artist_slug": "odilon-redon",
  "en": {
   "name": "Odilon Redon 2027 Wall Calendar",
   "short": "Twelve masterpieces by Odilon Redon, one for every month. A4 + US Letter PDF.",
   "body": [
    "A full year with Odilon Redon: twelve public-domain works from the Art Institute of Chicago, each with its title and date.",
    "Print at home or at a copy shop. Weeks start on Sunday."
   ],
   "get": [
    "14-page PDF (cover, 12 months, artwork list) in A4 and US Letter, 300 dpi",
    "Instant download",
    "Personal use and gifts"
   ]
  },
  "ko": {
   "name": "오딜롱 르동 2027 벽걸이 달력",
   "short": "오딜롱 르동의 명화 12점, 달마다 한 작품. A4·레터 PDF.",
   "body": [
    "오딜롱 르동의 작품 12점으로 채운 1년 달력이에요. 시카고 미술관이 공개한 퍼블릭 도메인 작품이고, 작품명과 연도가 함께 실려 있어요.",
    "집이나 인쇄소에서 바로 인쇄하세요. 일요일 시작이에요."
   ],
   "get": [
    "14페이지 PDF (표지, 12개월, 작품 목록), A4·미국 레터 두 가지, 300dpi",
    "즉시 다운로드",
    "개인 사용·선물용"
   ]
  }
 },
 {
  "slug": "2027-katsushika-hokusai-wall-calendar",
  "img": "/p/cal-katsushika-hokusai.jpg",
  "price": 6.5,
  "checkout": "POLAR_CAL_KATSUSHIKA_HOKUSAI",
  "payapp": "PAYAPP_CAL_KATSUSHIKA_HOKUSAI",
  "cat": "artist-calendars",
  "artist_slug": "katsushika-hokusai",
  "en": {
   "name": "Katsushika Hokusai 2027 Wall Calendar",
   "short": "Twelve masterpieces by Katsushika Hokusai, one for every month. A4 + US Letter PDF.",
   "body": [
    "A full year with Katsushika Hokusai: twelve public-domain works from the Art Institute of Chicago, each with its title and date.",
    "Print at home or at a copy shop. Weeks start on Sunday."
   ],
   "get": [
    "14-page PDF (cover, 12 months, artwork list) in A4 and US Letter, 300 dpi",
    "Instant download",
    "Personal use and gifts"
   ]
  },
  "ko": {
   "name": "가쓰시카 호쿠사이 2027 벽걸이 달력",
   "short": "가쓰시카 호쿠사이의 명화 12점, 달마다 한 작품. A4·레터 PDF.",
   "body": [
    "가쓰시카 호쿠사이의 작품 12점으로 채운 1년 달력이에요. 시카고 미술관이 공개한 퍼블릭 도메인 작품이고, 작품명과 연도가 함께 실려 있어요.",
    "집이나 인쇄소에서 바로 인쇄하세요. 일요일 시작이에요."
   ],
   "get": [
    "14페이지 PDF (표지, 12개월, 작품 목록), A4·미국 레터 두 가지, 300dpi",
    "즉시 다운로드",
    "개인 사용·선물용"
   ]
  }
 },
 {
  "slug": "2027-utagawa-hiroshige-wall-calendar",
  "img": "/p/cal-utagawa-hiroshige.jpg",
  "price": 6.5,
  "checkout": "POLAR_CAL_UTAGAWA_HIROSHIGE",
  "payapp": "PAYAPP_CAL_UTAGAWA_HIROSHIGE",
  "cat": "artist-calendars",
  "artist_slug": "utagawa-hiroshige",
  "en": {
   "name": "Utagawa Hiroshige 2027 Wall Calendar",
   "short": "Twelve masterpieces by Utagawa Hiroshige, one for every month. A4 + US Letter PDF.",
   "body": [
    "A full year with Utagawa Hiroshige: twelve public-domain works from the Art Institute of Chicago, each with its title and date.",
    "Print at home or at a copy shop. Weeks start on Sunday."
   ],
   "get": [
    "14-page PDF (cover, 12 months, artwork list) in A4 and US Letter, 300 dpi",
    "Instant download",
    "Personal use and gifts"
   ]
  },
  "ko": {
   "name": "우타가와 히로시게 2027 벽걸이 달력",
   "short": "우타가와 히로시게의 명화 12점, 달마다 한 작품. A4·레터 PDF.",
   "body": [
    "우타가와 히로시게의 작품 12점으로 채운 1년 달력이에요. 시카고 미술관이 공개한 퍼블릭 도메인 작품이고, 작품명과 연도가 함께 실려 있어요.",
    "집이나 인쇄소에서 바로 인쇄하세요. 일요일 시작이에요."
   ],
   "get": [
    "14페이지 PDF (표지, 12개월, 작품 목록), A4·미국 레터 두 가지, 300dpi",
    "즉시 다운로드",
    "개인 사용·선물용"
   ]
  }
 },
 {
  "slug": "2027-kitagawa-utamaro-wall-calendar",
  "img": "/p/cal-kitagawa-utamaro.jpg",
  "price": 6.5,
  "checkout": "POLAR_CAL_KITAGAWA_UTAMARO",
  "payapp": "PAYAPP_CAL_KITAGAWA_UTAMARO",
  "cat": "artist-calendars",
  "artist_slug": "kitagawa-utamaro",
  "en": {
   "name": "Kitagawa Utamaro 2027 Wall Calendar",
   "short": "Twelve masterpieces by Kitagawa Utamaro, one for every month. A4 + US Letter PDF.",
   "body": [
    "A full year with Kitagawa Utamaro: twelve public-domain works from the Art Institute of Chicago, each with its title and date.",
    "Print at home or at a copy shop. Weeks start on Sunday."
   ],
   "get": [
    "14-page PDF (cover, 12 months, artwork list) in A4 and US Letter, 300 dpi",
    "Instant download",
    "Personal use and gifts"
   ]
  },
  "ko": {
   "name": "기타가와 우타마로 2027 벽걸이 달력",
   "short": "기타가와 우타마로의 명화 12점, 달마다 한 작품. A4·레터 PDF.",
   "body": [
    "기타가와 우타마로의 작품 12점으로 채운 1년 달력이에요. 시카고 미술관이 공개한 퍼블릭 도메인 작품이고, 작품명과 연도가 함께 실려 있어요.",
    "집이나 인쇄소에서 바로 인쇄하세요. 일요일 시작이에요."
   ],
   "get": [
    "14페이지 PDF (표지, 12개월, 작품 목록), A4·미국 레터 두 가지, 300dpi",
    "즉시 다운로드",
    "개인 사용·선물용"
   ]
  }
 },
 {
  "slug": "2027-winslow-homer-wall-calendar",
  "img": "/p/cal-winslow-homer.jpg",
  "price": 6.5,
  "checkout": "POLAR_CAL_WINSLOW_HOMER",
  "payapp": "PAYAPP_CAL_WINSLOW_HOMER",
  "cat": "artist-calendars",
  "artist_slug": "winslow-homer",
  "en": {
   "name": "Winslow Homer 2027 Wall Calendar",
   "short": "Twelve masterpieces by Winslow Homer, one for every month. A4 + US Letter PDF.",
   "body": [
    "A full year with Winslow Homer: twelve public-domain works from the Art Institute of Chicago, each with its title and date.",
    "Print at home or at a copy shop. Weeks start on Sunday."
   ],
   "get": [
    "14-page PDF (cover, 12 months, artwork list) in A4 and US Letter, 300 dpi",
    "Instant download",
    "Personal use and gifts"
   ]
  },
  "ko": {
   "name": "윈슬로 호머 2027 벽걸이 달력",
   "short": "윈슬로 호머의 명화 12점, 달마다 한 작품. A4·레터 PDF.",
   "body": [
    "윈슬로 호머의 작품 12점으로 채운 1년 달력이에요. 시카고 미술관이 공개한 퍼블릭 도메인 작품이고, 작품명과 연도가 함께 실려 있어요.",
    "집이나 인쇄소에서 바로 인쇄하세요. 일요일 시작이에요."
   ],
   "get": [
    "14페이지 PDF (표지, 12개월, 작품 목록), A4·미국 레터 두 가지, 300dpi",
    "즉시 다운로드",
    "개인 사용·선물용"
   ]
  }
 },
 {
  "slug": "2027-john-singer-sargent-wall-calendar",
  "img": "/p/cal-john-singer-sargent.jpg",
  "price": 6.5,
  "checkout": "POLAR_CAL_JOHN_SINGER_SARGENT",
  "payapp": "PAYAPP_CAL_JOHN_SINGER_SARGENT",
  "cat": "artist-calendars",
  "artist_slug": "john-singer-sargent",
  "en": {
   "name": "John Singer Sargent 2027 Wall Calendar",
   "short": "Twelve masterpieces by John Singer Sargent, one for every month. A4 + US Letter PDF.",
   "body": [
    "A full year with John Singer Sargent: twelve public-domain works from the Art Institute of Chicago, each with its title and date.",
    "Print at home or at a copy shop. Weeks start on Sunday."
   ],
   "get": [
    "14-page PDF (cover, 12 months, artwork list) in A4 and US Letter, 300 dpi",
    "Instant download",
    "Personal use and gifts"
   ]
  },
  "ko": {
   "name": "존 싱어 사전트 2027 벽걸이 달력",
   "short": "존 싱어 사전트의 명화 12점, 달마다 한 작품. A4·레터 PDF.",
   "body": [
    "존 싱어 사전트의 작품 12점으로 채운 1년 달력이에요. 시카고 미술관이 공개한 퍼블릭 도메인 작품이고, 작품명과 연도가 함께 실려 있어요.",
    "집이나 인쇄소에서 바로 인쇄하세요. 일요일 시작이에요."
   ],
   "get": [
    "14페이지 PDF (표지, 12개월, 작품 목록), A4·미국 레터 두 가지, 300dpi",
    "즉시 다운로드",
    "개인 사용·선물용"
   ]
  }
 }
];
PRODUCTS.push(...ARTIST_CALS);
