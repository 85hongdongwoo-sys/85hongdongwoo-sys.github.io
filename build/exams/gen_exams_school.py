"""대학별 고사·특수학교·경찰소방 기출 페이지 (배포 때 실행, gen_exams_more.py 다음).
- /ipsi/gichul/nonsul.html        대학 논술 기출 (선행학습 영향평가·대학별 고사자료) 45개 대학 × 5개 학년도
- /ipsi/gichul/sagwan.html        사관학교·경찰대학 1차 시험 기출
- /ipsi/gichul/police-fire.html   경찰·소방·해양경찰·군무원 채용 필기 기출
파일은 우리 서버에 두지 않고 대입정보포털 어디가·각 기관 공식 게시판으로만 연결한다 (2026-11-26 확인).
사용: python3 build/exams/gen_exams_school.py _site"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_exams as GE
from gen_exams import E, SITE, page, crumb, faq_ld, faq_html

root = GE.root
CHECKED = '2026-11-26'
ADIGA = 'https://www.adiga.kr/ucp/uvt/uni/univDetail.do?menuId=PCUVTINF2000&unvCd={c}&searchSyr={y}'
XCSS = ('<style id="gc-sch">.ns-t{width:100%;border-collapse:collapse;font-size:14px}.ns-t th,.ns-t td{border-bottom:1px solid var(--line-s,#E3E7EE);padding:8px 6px;text-align:left;vertical-align:middle}'
        '.ns-t th{font-size:12.5px;color:var(--muted,#5B6B82);font-weight:700}.ns-t td b{font-size:15px;color:var(--head,#111);white-space:nowrap}'
        '.ns-y{display:flex;flex-wrap:wrap;gap:5px}.ns-y a,.ns-y span{display:inline-block;padding:5px 8px;border-radius:8px;font-size:12.5px;text-decoration:none;white-space:nowrap}'
        '.ns-y a{background:#EEF4FF;color:#1D4ED8;border:1px solid #D6E4FD}.ns-y a.s{background:#F4F6F9;color:#334155;border-color:#E3E7EE}.ns-y span{color:#9AA4B2;background:#F8FAFC}'
        '.ns-home{font-size:12.5px;white-space:nowrap}.ns-key{display:flex;flex-wrap:wrap;gap:10px;font-size:13px;color:var(--muted,#5B6B82);margin:6px 0 10px}'
        '.ns-q{width:100%;box-sizing:border-box;padding:10px 12px;border:1px solid #D9DDE3;border-radius:10px;font:inherit;font-size:15px;margin:4px 0 10px}'
        '.lk{list-style:none;padding:0;margin:0;display:grid;gap:8px}.lk a{display:block;padding:12px 14px;border:1px solid var(--line-s,#E3E7EE);border-radius:12px;text-decoration:none;color:inherit;background:#fff}'
        '.lk a b{display:block;font-size:15.5px;color:var(--head,#111);overflow-wrap:anywhere}.lk a span{display:block;font-size:13px;color:var(--muted,#5B6B82);margin-top:3px;overflow-wrap:anywhere}'
        '@media(max-width:640px){.ns-t thead{display:none}.ns-t tr{display:block;border-bottom:1px solid var(--line-s,#E3E7EE);padding:8px 0}.ns-t td{display:block;border:0;padding:3px 0}}</style>')
SRCH = ('<script>(function(){var q=document.getElementById("ns-q");if(!q)return;var rs=[].slice.call(document.querySelectorAll(".ns-t tbody tr"));'
        'q.addEventListener("input",function(){var v=q.value.replace(/\\s+/g,"");rs.forEach(function(r){r.hidden=v&&r.getAttribute("data-n").indexOf(v)<0})})})();</script>')


def rel(*skip):
    items = [('/ipsi/gichul/nonsul.html', '대학 논술 기출문제 (45개 대학)', '선행학습 영향평가·논술 고사자료 5개 학년도'),
             ('/ipsi/gichul/sagwan.html', '사관학교·경찰대 1차 시험 기출', '국어·영어·수학 문제와 정답 공식 게시판'),
             ('/ipsi/gichul/police-fire.html', '경찰·소방·해경·군무원 기출', '채용 필기시험 문제·정답 공식 공개처'),
             ('/ipsi/gichul/', '수능·모의평가 기출 전체', '평가원 공식 PDF, 학년도별'),
             ('/ipsi/gongmuwon/', '공무원 기출문제 PDF', '9급·7급 국가직·지방직'),
             ('/ipsi/hanneung.html', '한국사능력검정시험', '시험 일정·급수·기출 공식 연결')]
    return ('<section class="card rel"><h2>다른 기출문제</h2><ul class="tlist">' + ''.join(
        f'<li><a href="{u}"><b>{t}</b><span>{d}</span></a></li>' for u, t, d in items if u not in skip) + '</ul></section>')


def nonsul():
    D = json.load(open(os.path.join(HERE, 'data', 'nonsul_adiga.json'), encoding='utf-8'))
    U = D['univ']
    ys = ['2027', '2026', '2025', '2024', '2023']
    nG = sum(1 for u in U for y in ys if 'G' in u[3][y])
    rows = []
    for n, c, adm, yy in U:
        cells = []
        for y in ys:
            f = yy[y]
            if f == '--':
                cells.append(f'<span title="어디가에 파일 없음">{y}</span>')
            else:
                cells.append(f'<a class="{"" if "G" in f else "s"}" href="{ADIGA.format(c=c, y=y)}" rel="noopener" target="_blank">{y}{" 논술" if "G" in f else " 보고서"}</a>')
        a = adm if adm.startswith('http') else 'https://' + adm
        rows.append(f'<tr data-n="{E(n)}"><td><b>{E(n)}</b> <a class="ns-home" href="{E(a)}" rel="noopener" target="_blank">입학처 ↗</a></td>'
                    f'<td><div class="ns-y">{"".join(cells)}</div></td></tr>')
    title = '대학 논술 기출문제 모음 (2023~2027학년도) · 45개 대학 선행학습 영향평가·논술 고사자료'
    desc = ('논술전형을 뽑는 45개 대학·캠퍼스의 논술 기출문제를 5개 학년도로 모았어요. 대학이 대입정보포털 어디가에 올린 선행학습 영향평가 보고서(문제·출제 의도·예시 답안)와 '
            '대학별 고사자료(논술)로 바로 연결하고, 각 대학 입학처 주소도 함께 있어요.')
    cr, crld = crumb(('대학 논술 기출', ''))
    ans = (f'<b>45개 대학·캠퍼스</b>의 논술 기출을 2023~2027학년도로 정리했어요. 파란 버튼(논술)은 어디가에 <b>대학별 고사자료(논술)</b>와 <b>선행학습 영향평가 보고서</b>가 모두 있는 해, '
           f'회색 버튼(보고서)은 보고서만 있는 해예요. 논술 자료가 있는 칸은 모두 {nG}개예요 ({GE.fmt_date(CHECKED)} 확인).')
    qa = [('논술 기출문제는 어디서 받나요?', '대학은 해마다 3월 무렵 <b>선행학습 영향평가 보고서</b>를 입학처와 대입정보포털 어디가에 올려요. 이 보고서에 지난해 논술 문제, 출제 의도, 채점 기준, 예시 답안이 들어 있어요. 이 페이지의 버튼은 그 어디가 화면으로 바로 연결돼요.'),
          ('버튼을 눌렀는데 파일이 바로 안 받아져요.', '어디가 대학 정보 화면이 열려요. 화면 가운데 자료 칸에서 <b>선행학습 영향평가</b> 또는 <b>대학별 고사자료(논술/적성)</b> 버튼을 누르면 대학이 올린 파일이 받아져요.'),
          ('학년도 버튼(2027, 2026…)은 무슨 뜻인가요?', '어디가에서 그 학년도를 골랐을 때 보이는 자료예요. 해마다 대학이 새로 올리는 보고서·고사자료가 학년도별로 나뉘어 있어요. 최근 3개 학년도부터 풀어 보는 것을 많이 권해요.'),
          ('회색 ‘보고서’만 있는 해는 논술 문제가 없나요?', '그 해에는 어디가에 대학별 고사자료(논술) 파일이 따로 없다는 뜻이에요. 선행학습 영향평가 보고서 안에 논술 문항이 들어 있는 경우가 많으니 보고서를 열어 보세요. 대학 입학처의 기출·자료실 게시판도 함께 확인하세요.'),
          ('고려대는 왜 보고서만 있나요?', '어디가의 고려대(서울) 화면에는 2023~2027학년도 모두 선행학습 영향평가 보고서만 올라와 있어요. 논술 문제는 보고서와 고려대 입학처 게시판에서 확인하세요.'),
          ('논술 기출을 인쇄해서 써도 되나요?', '개인 공부용으로 받아 인쇄하는 건 괜찮아요. 저작권은 각 대학에 있으니 다른 사람에게 나눠 주거나 팔면 안 돼요.')]
    main = (XCSS + f'<header class="top hub">{cr}<h1>대학 논술 기출문제 모음</h1>'
            '<p class="lead">논술전형 대학 45곳의 논술 기출을 5개 학년도로 모았어요. 대학 이름을 찾아 학년도 버튼을 누르면 대학이 올린 공식 자료 화면이 열려요.</p>'
            f'<p class="gc-ans">{ans}</p></header>'
            '<section class="card"><h2>대학별 논술 기출 (2023~2027학년도)</h2>'
            '<input id="ns-q" class="ns-q" type="search" placeholder="대학 이름으로 찾기 (예: 중앙대)" aria-label="대학 이름으로 찾기">'
            '<div class="ns-key"><span><b style="color:#1D4ED8">파란 버튼</b> 논술 고사자료 + 보고서</span><span><b>회색 버튼</b> 보고서만</span><span style="color:#9AA4B2">흐린 숫자: 자료 없음</span></div>'
            '<table class="ns-t"><thead><tr><th>대학 · 입학처</th><th>학년도별 자료 (어디가)</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table>'
            f'<p class="gc-src" style="margin-top:10px">자료: 대입정보포털 어디가(한국대학교육협의회) 대학 정보 화면, {GE.fmt_date(CHECKED)} 확인. 2027학년도 논술 실시 대학은 기사마다 42~44곳으로 세는데, 이 표는 캠퍼스를 나눠 45곳이에요.</p></section>'
            '<section class="card"><h2>논술 기출, 이렇게 공부해요</h2><ol>'
            '<li><b>가고 싶은 대학 최근 3년치</b>를 먼저 받아요. 출제 형식(인문 제시문형, 수리 논술, 약술형)이 대학마다 달라요.</li>'
            '<li>실제 시험 시간에 맞춰 답안을 써 봐요. 시간은 대학 모집요강에 나와 있어요.</li>'
            '<li>보고서의 <b>채점 기준·예시 답안</b>과 비교해 빠진 내용을 고쳐요.</li>'
            '<li>같은 대학의 다른 계열(인문·자연) 문제도 훑어보면 출제 흐름이 보여요.</li></ol>'
            '<h3>선행학습 영향평가 보고서란?</h3><p>대학이 논술·면접 같은 대학별 고사를 고등학교 교육과정 안에서 냈는지 스스로 점검해 공개하는 보고서예요. 그래서 <b>문제, 출제 의도, 문항 해설, 예시 답안</b>이 함께 실려 있어 사실상 공식 기출 해설집이에요.</p></section>'
            + faq_html(qa) + rel('/ipsi/gichul/nonsul.html'))
    ld = [crld, faq_ld(qa), {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": SITE + '/ipsi/gichul/nonsul.html', "description": desc, "inLanguage": "ko"}]
    return page('/ipsi/gichul/nonsul.html', title + ' | 홍라이프 도구', desc, main, ld, SRCH)


def linklist(items):
    return '<ul class="lk">' + ''.join(f'<li><a href="{E(u)}" rel="noopener" target="_blank"><b>{t}</b><span>{d}</span></a></li>' for t, d, u in items) + '</ul>'


def sagwan():
    title = '사관학교·경찰대학 1차 시험 기출문제 (육사·해사·공사·국간사·경찰대) · 공식 게시판 모음'
    desc = ('육군·해군·공군사관학교와 국군간호사관학교 1차 시험(공동 출제)과 경찰대학 1차 시험 기출문제·정답을 공식 게시판으로 연결해요. 경찰대는 2020~2027학년도 기출과 확정답안을 공개하고 있어요.')
    cr, crld = crumb(('사관학교·경찰대 기출', ''))
    pol = [('경찰대학 신입학 1차 시험 기출문제', '2020~2027학년도 1차 시험 문제·확정답안 (경찰대학 입학 게시판)', 'https://www.police.ac.kr/police/police/master/62/boardList.do?mdex=police59'),
           ('경찰대학 편입학 기출문제', '편입학 시험 기출 게시판', 'https://www.police.ac.kr/police/police/master/367/boardList.do?mdex=police64')]
    afa = [('공군사관학교 입학 ‧ 1차시험 기출문제', '공사 입학 누리집의 기출문제(답안 포함) 게시판', 'https://www.afa.ac.kr/user/indexSub.action?codyMenuSeq=48090&siteId=enter&menuUIType=top')]
    qa = [('사관학교 1차 시험은 학교마다 다른가요?', '아니요. 육군·해군·공군사관학교와 국군간호사관학교는 <b>같은 날 같은 문제지</b>로 1차 시험을 봐요. 국어·영어·수학 3과목이에요. 그래서 한 학교 게시판의 기출이 네 학교 모두의 기출이에요.'),
          ('경찰대학 1차 시험은 사관학교와 같나요?', '다른 시험이에요. 과목은 국어·영어·수학으로 같지만 문제와 배점이 다르고, 수학은 경찰대가 수학Ⅰ·Ⅱ(공통)에서만 내요. 사관학교는 공통에 선택과목(확률과 통계·미적분·기하 중 1개)도 봐요.'),
          ('경찰대 기출에 국어 문제가 없어요.', '경찰대학은 게시판 공지에서 저작권 문제로 국어는 정답만 올리고, 수학·영어는 문제도 공개한다고 안내하고 있어요.'),
          ('기출은 몇 년 치를 풀어야 하나요?', '최근 5개 학년도를 시간에 맞춰 풀어 보는 방법을 많이 써요. 국어·영어는 50분, 수학은 100분(사관학교 기준)이에요.')]
    main = (XCSS + f'<header class="top hub">{cr}<h1>사관학교·경찰대 1차 시험 기출</h1>'
            '<p class="lead">사관학교 4곳과 경찰대학 1차 시험의 기출문제·정답을 학교 공식 게시판으로 바로 연결해요.</p>'
            '<p class="gc-ans">경찰대학은 <b>2020~2027학년도</b> 1차 시험 문제와 확정답안을 입학 게시판에 공개하고 있어요. 사관학교 4곳은 1차 시험을 <b>같은 문제지</b>로 치러요 (2026-11-26 확인).</p></header>'
            '<section class="card"><h2>경찰대학</h2>' + linklist(pol) + '</section>'
            '<section class="card"><h2>사관학교 (육사·해사·공사·국간사 공동 1차 시험)</h2>' + linklist(afa) +
            '<p class="note" style="margin-top:10px">육군사관학교·해군사관학교·국군간호사관학교도 같은 1차 시험을 봐요. 학교별 모집요강과 최신 기출 공지는 각 학교 입학 누리집 공지사항에서 확인하세요.</p></section>'
            '<section class="card"><h2>1차 시험 한눈에</h2><div style="overflow-x:auto"><table class="gc-t"><thead><tr><th>구분</th><th>사관학교 4곳</th><th>경찰대학</th></tr></thead><tbody>'
            '<tr><td>과목</td><td>국어·영어·수학</td><td>국어·영어·수학</td></tr>'
            '<tr><td>수학 범위</td><td>공통(수학Ⅰ·Ⅱ) + 선택 1과목</td><td>공통(수학Ⅰ·Ⅱ)</td></tr>'
            '<tr><td>문제지</td><td>4개 학교 같은 문제</td><td>경찰대 자체 문제</td></tr></tbody></table></div></section>'
            + faq_html(qa) + rel('/ipsi/gichul/sagwan.html'))
    ld = [crld, faq_ld(qa), {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": SITE + '/ipsi/gichul/sagwan.html', "description": desc, "inLanguage": "ko"}]
    return page('/ipsi/gichul/sagwan.html', title + ' | 홍라이프 도구', desc, main, ld)


def police_fire():
    title = '경찰·소방·해양경찰·군무원 채용 필기 기출문제 · 공식 공개처 모음 (문제지·정답)'
    desc = ('경찰공무원(순경), 소방공무원, 해양경찰공무원, 군무원 채용 필기시험 기출문제와 정답을 공식 기관 공개처로 바로 연결해요. 해양경찰은 2019~2025년, 소방은 2025년 문제지·가답안 등 기관이 올린 자료를 모았어요.')
    cr, crld = crumb(('경찰·소방·해경·군무원 기출', ''))
    police = [('경찰청 인터넷 원서접수 (경찰공무원 채용)', '순경 공채·경채, 경찰간부후보생 시험 공고와 문제·정답 공개처', 'https://gosi.police.go.kr')]
    fire = [('소방청 — 2025년 소방공무원 채용시험 문제지 및 가 답안 공개', '공채·경채 문제지 ZIP과 가답안 ZIP (소방청 채용 게시판)', 'https://www.nfa.go.kr/nfa/news/job/nfajob/?boardId=bbs_0000000000000012&mode=view&cntId=426'),
            ('119고시 시험공고 게시판', '중앙소방학교 원서접수 누리집 — 지난 회차 문제·정답가안 공개 글', 'http://119gosi.kr/bbs/board.php?bo_table=040301')]
    kcg = [('2025년 하반기 해양경찰공무원 채용 필기 기출문제·정답안', '2025년 10월 25일 시험, 문제 ZIP·정답 PDF', 'https://www.kcg.go.kr/kcg/na/ntt/selectNttInfo.do?nttSn=65797'),
           ('2024년 하반기 해양경찰 채용 필기 기출문제·답안', '문제·답안 ZIP', 'https://www.kcg.go.kr/kcg/na/ntt/selectNttInfo.do?nttSn=57731'),
           ('2021~2023년 해양경찰 채용 필기 기출문제·답안', '3년치 ZIP 한 번에', 'https://www.kcg.go.kr/kcg/na/ntt/selectNttInfo.do?nttSn=52908')]
    army = [('국방부 군무원 채용관리 누리집', '일반군무원 필기시험 문제·정답가안 공개, 시험 공고', 'https://recruit.mnd.go.kr:470/main.do')]
    qa = [('경찰 순경 기출문제는 어디서 받나요?', '경찰청 인터넷 원서접수 누리집(gosi.police.go.kr)이 채용 공고와 시험 자료를 올리는 공식 창구예요. 시험이 끝나면 문제와 정답가안, 이의제기 뒤 확정답안이 차례로 올라와요.'),
          ('소방공무원 기출문제는 어디에 있나요?', '소방청 누리집 채용 게시판과 119고시 누리집에 올라와요. 2025년 시험은 소방청 게시판에 문제지와 가답안이 ZIP 파일로 올라왔어요.'),
          ('해양경찰 기출은 몇 년 치가 있나요?', '해양경찰청 누리집에 2019~2020년, 2021~2023년 묶음과 2024년·2025년 하반기 시험 자료가 따로 올라와 있어요. 이 페이지에는 그중 최근 자료를 연결했어요.'),
          ('군무원 기출문제도 공개하나요?', '국방부는 일반군무원 필기시험이 끝나면 군무원 채용관리 누리집에 문제와 정답가안을 올려요. 공개 과목은 해마다 공지로 안내해요.'),
          ('기출을 인쇄해서 나눠 줘도 되나요?', '저작권은 각 기관에 있어요. 개인 공부용으로 받는 건 괜찮지만 복제해서 배포·판매하면 안 돼요.')]
    main = (XCSS + f'<header class="top hub">{cr}<h1>경찰·소방·해경·군무원 기출</h1>'
            '<p class="lead">경찰·소방·해양경찰·군무원 채용 필기시험의 기출문제와 정답을 기관 공식 공개처로 바로 연결해요.</p>'
            '<p class="gc-ans">해양경찰은 <b>2019~2025년</b> 채용 필기 기출을, 소방청은 <b>2025년</b> 문제지·가답안을, 국방부는 군무원 필기 문제·정답가안을 공식 누리집에 올려요 (2026-11-26 확인).</p></header>'
            '<section class="card"><h2>경찰공무원 (순경·경찰간부)</h2>' + linklist(police) + '</section>'
            '<section class="card"><h2>소방공무원</h2>' + linklist(fire) + '</section>'
            '<section class="card"><h2>해양경찰공무원</h2>' + linklist(kcg) + '</section>'
            '<section class="card"><h2>군무원</h2>' + linklist(army) + '</section>'
            '<section class="card"><h2>기출 공부 순서</h2><ol><li>최근 3년치를 시험 시간에 맞춰 풀어요.</li><li>틀린 문제는 법령·이론 근거를 찾아 표시해요.</li><li>가답안과 확정답안이 다를 수 있으니 <b>확정답안</b>으로 채점해요.</li></ol></section>'
            + faq_html(qa) + rel('/ipsi/gichul/police-fire.html'))
    ld = [crld, faq_ld(qa), {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": SITE + '/ipsi/gichul/police-fire.html', "description": desc, "inLanguage": "ko"}]
    return page('/ipsi/gichul/police-fire.html', title + ' | 홍라이프 도구', desc, main, ld)


def register(paths):
    sm = os.path.join(root, 'sitemap.xml'); s = open(sm, encoding='utf-8').read()
    add = ''.join(f'<url><loc>{SITE}{p}</loc><lastmod>{CHECKED}</lastmod></url>\n' for p in paths if f'{SITE}{p}<' not in s)
    if add: open(sm, 'w', encoding='utf-8').write(s.replace('</urlset>', add + '</urlset>', 1))
    idx = os.path.join(root, 'index.html'); s = open(idx, encoding='utf-8').read()
    TRIP = '"u":"/trip/"}'
    ent = [{"t": "대학 논술 기출문제 모음 (45개 대학)", "d": "선행학습 영향평가·논술 고사자료 2023~2027학년도", "k": "논술 기출 논술 기출문제 대학 논술 수리논술 인문논술 약술형 논술 선행학습 영향평가 논술 예시답안 중앙대 논술 경희대 논술 성균관대 논술 한양대 논술 연세대 논술", "c": "입시·시험", "u": "/ipsi/gichul/nonsul.html"},
           {"t": "사관학교·경찰대 1차 시험 기출", "d": "육사·해사·공사·국간사·경찰대 기출문제·정답", "k": "사관학교 기출 육사 기출 해사 기출 공사 기출 국군간호사관학교 기출 경찰대 기출 사관학교 1차 시험 경찰대 1차 시험 정답", "c": "입시·시험", "u": "/ipsi/gichul/sagwan.html"},
           {"t": "경찰·소방·해경·군무원 기출", "d": "채용 필기시험 문제·정답 공식 공개처", "k": "경찰 기출 순경 기출 경찰공무원 기출문제 소방 기출 소방공무원 기출문제 해양경찰 기출 해경 기출 군무원 기출 가답안 확정답안", "c": "입시·시험", "u": "/ipsi/gichul/police-fire.html"}]
    ent = [e for e in ent if e['u'] in paths and f'"u":"{e["u"]}"' not in s]
    if ent and TRIP in s:
        open(idx, 'w', encoding='utf-8').write(s.replace(TRIP, TRIP + ',' + ','.join(json.dumps(x, ensure_ascii=False, separators=(',', ':')) for x in ent), 1))
    p = os.path.join(root, 'ipsi', 'index.html'); s = open(p, encoding='utf-8').read()
    if 'id="exam-list"' in s and '/ipsi/gichul/nonsul.html' not in s:
        li = ('<li><a href="/ipsi/gichul/nonsul.html"><b>대학 논술 기출문제 (45개 대학)</b><span>선행학습 영향평가·논술 고사자료 5개 학년도</span></a></li>'
              '<li><a href="/ipsi/gichul/sagwan.html"><b>사관학교·경찰대 1차 시험 기출</b><span>육사·해사·공사·국간사 공동 시험, 경찰대 2020~2027</span></a></li>'
              '<li><a href="/ipsi/gichul/police-fire.html"><b>경찰·소방·해경·군무원 기출</b><span>채용 필기 문제·정답 공식 공개처</span></a></li>')
        i = s.find('</ul>', s.find('id="exam-list"'))
        s = s[:i] + li + s[i:]; open(p, 'w', encoding='utf-8').write(s)
    # 수능 기출 허브에도 연결
    p = os.path.join(root, 'ipsi', 'gichul', 'index.html')
    if os.path.exists(p):
        s = open(p, encoding='utf-8').read()
        if '/ipsi/gichul/nonsul.html' not in s:
            s = s.replace('<li><a href="/ipsi/"><b>입시·시험 도구 모음</b>',
                          '<li><a href="/ipsi/gichul/nonsul.html"><b>대학 논술 기출 (45개 대학)</b><span>선행학습 영향평가·논술 고사자료</span></a></li>'
                          '<li><a href="/ipsi/gichul/sagwan.html"><b>사관학교·경찰대 기출</b><span>1차 시험 문제·정답</span></a></li>'
                          '<li><a href="/ipsi/"><b>입시·시험 도구 모음</b>', 1)
            open(p, 'w', encoding='utf-8').write(s)
    print('school exam pages:', paths, 'sitemap +', add.count('<url>'))


if __name__ == '__main__':
    made = [nonsul(), sagwan(), police_fire()]
    register(made)
