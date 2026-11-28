/* Arttrip Studio — Masterpiece Budget Planner (.xlsx) built in the buyer's browser with ExcelJS.
   Works in Excel, Google Sheets (File > Import) and Numbers. All totals are live formulas. */
(function (root) {
  var TX = {
    en: { start: 'Start Here', settings: 'Settings', year: 'Year Overview', bills: 'Bills & Subscriptions', goals: 'Savings Goals', debt: 'Debt Payoff',
      months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
      mshort: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      title: 'Masterpiece Budget Planner', income: 'Income', expenses: 'Expenses', savings: 'Savings', left: 'Left to spend', planned: 'Planned', actual: 'Actual', diff: 'Difference', used: '% used',
      date: 'Date', source: 'Source', desc: 'Description', cat: 'Category', amount: 'Amount', paid: 'Paid?', notes: 'Notes', currency: 'Currency symbol', startBal: 'Starting balance', yearL: 'Year',
      incCats: ['Salary', 'Side income', 'Pension', 'Gifts', 'Other income'], expCats: ['Housing', 'Utilities', 'Groceries', 'Eating out', 'Transport', 'Phone & internet', 'Insurance', 'Health', 'Shopping', 'Kids & family', 'Pets', 'Gifts & giving', 'Entertainment', 'Subscriptions', 'Travel', 'Debt payments', 'Savings transfer', 'Other'],
      monthlyBudget: 'Monthly budget', catHead: 'Category budgets (edit the amounts)', incHead: 'Income categories', expHead: 'Expense categories',
      how: ['Welcome! This planner adds up everything for you. Only type in the white cells.', '1. Settings: pick your currency symbol, the year and your starting balance, then set a monthly budget for each category.', '2. Each month: add every payment you receive under Income and every purchase under Expenses. Choose the category from the drop-down list.', '3. The summary at the top of each month and the Year Overview update automatically.', '4. Bills & Subscriptions: list regular bills once and tick them off each month.', '5. Savings Goals and Debt Payoff: add your goals and debts to see your progress and payoff time.', 'Google Sheets: File > Import > Upload this file. Numbers: open the file directly.', 'Artworks: public-domain paintings from museum open-access collections.'],
      bill: 'Bill', due: 'Due day', freq: 'Frequency', auto: 'Autopay?', monthly: 'Monthly', goal: 'Goal', target: 'Target', saved: 'Saved so far', progress: 'Progress', tdate: 'Target date', perMonth: 'Needed per month', debtN: 'Debt', bal: 'Balance', rate: 'Interest % (yearly)', minp: 'Monthly payment', months2: 'Months to pay off', interest: 'Total interest', net: 'Net', total: 'Total', byCat: 'Spending by category', yes: 'Yes', no: 'No', artwork: 'This month\'s masterpiece' },
    ko: { start: '시작하기', settings: '설정', year: '연간 요약', bills: '고정지출·구독', goals: '저축 목표', debt: '빚 상환',
      months: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'], mshort: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
      title: '명화 가계부', income: '수입', expenses: '지출', savings: '저축', left: '남은 돈', planned: '계획', actual: '실제', diff: '차이', used: '사용률',
      date: '날짜', source: '내용', desc: '내용', cat: '분류', amount: '금액', paid: '지불', notes: '메모', currency: '화폐 기호', startBal: '시작 잔액', yearL: '연도',
      incCats: ['월급', '부수입', '연금', '용돈·선물', '기타 수입'], expCats: ['주거·관리비', '공과금', '식비(장보기)', '외식', '교통·차량', '통신', '보험', '병원·약', '쇼핑', '자녀·가족', '반려동물', '경조사·선물', '여가', '구독', '여행', '대출 상환', '저축 이체', '기타'],
      monthlyBudget: '한 달 예산', catHead: '분류별 예산 (금액을 고쳐 쓰세요)', incHead: '수입 분류', expHead: '지출 분류',
      how: ['환영해요! 이 가계부는 합계를 모두 자동으로 계산해요. 흰 칸에만 입력하세요.', '1. 설정: 화폐 기호, 연도, 시작 잔액을 적고 분류마다 한 달 예산을 정하세요.', '2. 매달: 받은 돈은 수입 표에, 쓴 돈은 지출 표에 적고 분류는 목록에서 고르세요.', '3. 각 달 위쪽 요약과 연간 요약이 자동으로 바뀌어요.', '4. 고정지출·구독: 매달 나가는 돈을 한 번 적어 두고 달마다 체크하세요.', '5. 저축 목표·빚 상환: 목표와 대출을 적으면 진행률과 다 갚는 데 걸리는 기간이 나와요.', '구글 시트: 파일 > 가져오기 > 업로드. 한셀·넘버스에서도 열려요.', '그림: 미술관이 저작권 없이 공개한 명화예요.'],
      bill: '항목', due: '납부일', freq: '주기', auto: '자동이체', monthly: '매월', goal: '목표', target: '목표 금액', saved: '모은 돈', progress: '진행률', tdate: '목표 날짜', perMonth: '매달 필요한 돈', debtN: '대출', bal: '남은 금액', rate: '연이율 %', minp: '월 상환액', months2: '다 갚는 데 걸리는 달', interest: '총 이자', net: '순저축', total: '합계', byCat: '분류별 지출', yes: '예', no: '아니요', artwork: '이달의 명화' },
    ja: { start: 'はじめに', settings: '設定', year: '年間まとめ', bills: '固定費・サブスク', goals: '貯金目標', debt: 'ローン返済',
      months: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'], mshort: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
      title: '名画の家計簿', income: '収入', expenses: '支出', savings: '貯金', left: '残り', planned: '予定', actual: '実績', diff: '差', used: '使用率',
      date: '日付', source: '内容', desc: '内容', cat: '分類', amount: '金額', paid: '支払', notes: 'メモ', currency: '通貨記号', startBal: '開始残高', yearL: '年',
      incCats: ['給与', '副収入', '年金', 'お祝い・贈与', 'その他の収入'], expCats: ['住居', '光熱費', '食費', '外食', '交通', '通信', '保険', '医療', '日用品・買い物', '子ども・家族', 'ペット', '交際費', '娯楽', 'サブスク', '旅行', 'ローン返済', '貯金', 'その他'],
      monthlyBudget: '月の予算', catHead: '分類ごとの予算（金額を書き換えてください）', incHead: '収入の分類', expHead: '支出の分類',
      how: ['ようこそ！合計はすべて自動で計算されます。白いセルだけに入力してください。', '1. 設定：通貨記号、年、開始残高を入れ、分類ごとに月の予算を決めます。', '2. 毎月：受け取ったお金は収入表に、使ったお金は支出表に入力し、分類はリストから選びます。', '3. 各月の上の集計と年間まとめは自動で更新されます。', '4. 固定費・サブスク：毎月の支払いを一度書き、月ごとにチェックします。', '5. 貯金目標・ローン返済：目標と借入を入れると進み具合と完済までの期間がわかります。', 'Googleスプレッドシート：ファイル > インポート > アップロード。', '絵：美術館がパブリックドメインで公開している名画です。'],
      bill: '項目', due: '支払日', freq: '頻度', auto: '自動引落', monthly: '毎月', goal: '目標', target: '目標額', saved: '貯めた額', progress: '進み具合', tdate: '目標日', perMonth: '毎月必要な額', debtN: '借入', bal: '残高', rate: '年利 %', minp: '毎月の返済額', months2: '完済までの月数', interest: '利息合計', net: '純貯金', total: '合計', byCat: '分類別の支出', yes: 'はい', no: 'いいえ', artwork: '今月の名画' }
  };
  var C = { ink: 'FF2B2622', head: 'FF3D5A6C', soft: 'FFF3EEE4', line: 'FFD9D0C1', inc: 'FF2E7D32', exp: 'FFB23A2E', sav: 'FF1F6F8B', white: 'FFFFFFFF', input: 'FFFFFFFF', calc: 'FFF7F3EC' };
  var ROWS_INC = 15, ROWS_EXP = 60;

  function build(ExcelJS, o) {
    var t = TX[o.lang] || TX.en, wb = new ExcelJS.Workbook(), fmt = '"$"#,##0.00';
    wb.creator = 'Arttrip Studio'; wb.created = new Date();
    var font = o.lang === 'en' ? 'Georgia' : o.lang === 'ja' ? 'Yu Gothic' : 'Malgun Gothic', body = o.lang === 'en' ? 'Calibri' : font;
    function cellStyle(c, s) { if (s.f) c.font = Object.assign({ name: body, size: 11 }, s.f); if (s.fill) c.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: s.fill } }; if (s.nf) c.numFmt = s.nf; if (s.al) c.alignment = s.al; if (s.b) c.border = s.b; }
    var thin = { style: 'thin', color: { argb: C.line } }, box = { top: thin, left: thin, bottom: thin, right: thin };
    function img(ws, k, tl, br) { if (!o.images || !o.images[k]) return; var id = wb.addImage({ base64: o.images[k].data, extension: 'jpeg' }); ws.addImage(id, { tl: tl, br: br, editAs: 'oneCell' }); }
    function title(ws, text, sub, colEnd) { ws.mergeCells(1, 1, 1, colEnd); var c = ws.getCell(1, 1); c.value = text; cellStyle(c, { f: { name: font, size: 22, bold: true, color: { argb: C.ink } } }); ws.getRow(1).height = 34; if (sub) { ws.mergeCells(2, 1, 2, colEnd); var s = ws.getCell(2, 1); s.value = sub; cellStyle(s, { f: { italic: true, color: { argb: 'FF7A7066' } } }); } }
    function header(ws, r, c0, labels, color) { labels.forEach(function (l, i) { var c = ws.getCell(r, c0 + i); c.value = l; cellStyle(c, { f: { bold: true, color: { argb: C.white } }, fill: color || C.head, al: { vertical: 'middle', horizontal: 'center', wrapText: true }, b: box }); }); ws.getRow(r).height = 22; }

    // ---- Settings
    var st = wb.addWorksheet(t.settings, { properties: { tabColor: { argb: C.head } } });
    st.columns = [{ width: 30 }, { width: 18 }, { width: 4 }, { width: 30 }, { width: 18 }];
    title(st, t.settings, t.title, 5);
    [[t.currency, o.currency || '$'], [t.yearL, o.year || 2027], [t.startBal, 0]].forEach(function (p, i) { var a = st.getCell(4 + i, 1), b = st.getCell(4 + i, 2); a.value = p[0]; cellStyle(a, { f: { bold: true } }); b.value = p[1]; cellStyle(b, { fill: C.input, b: box, nf: i === 2 ? fmt : undefined, al: { horizontal: 'center' } }); });
    header(st, 8, 1, [t.expHead, t.monthlyBudget]); header(st, 8, 4, [t.incHead, t.monthlyBudget], C.inc);
    t.expCats.forEach(function (n, i) { var a = st.getCell(9 + i, 1), b = st.getCell(9 + i, 2); a.value = n; b.value = (o.budgets && o.budgets[i]) || 0; cellStyle(a, { b: box }); cellStyle(b, { b: box, nf: fmt }); });
    t.incCats.forEach(function (n, i) { var a = st.getCell(9 + i, 4), b = st.getCell(9 + i, 5); a.value = n; b.value = 0; cellStyle(a, { b: box }); cellStyle(b, { b: box, nf: fmt }); });
    var EXP_N = t.expCats.length, INC_N = t.incCats.length, EXP_LIST = "'" + t.settings + "'!$A$9:$A$" + (8 + EXP_N), INC_LIST = "'" + t.settings + "'!$D$9:$D$" + (8 + INC_N);
    var tot = st.getCell(9 + EXP_N, 1); tot.value = t.total; cellStyle(tot, { f: { bold: true } }); var tv = st.getCell(9 + EXP_N, 2); tv.value = { formula: 'SUM(B9:B' + (8 + EXP_N) + ')' }; cellStyle(tv, { f: { bold: true }, nf: fmt, fill: C.calc });

    // ---- Months
    var monthNames = [];
    t.months.forEach(function (mName, m) {
      var ws = wb.addWorksheet(t.mshort[m], { properties: { tabColor: { argb: ['FF8FB3C9', 'FFB9D7A8', 'FFF2C57C', 'FFE7A39A'][Math.floor(m / 3)] } }, views: [{ state: 'frozen', ySplit: 3 }] });
      monthNames.push(t.mshort[m]);
      ws.columns = [{ width: 12 }, { width: 26 }, { width: 18 }, { width: 14 }, { width: 3 }, { width: 12 }, { width: 28 }, { width: 18 }, { width: 14 }, { width: 8 }, { width: 3 }, { width: 22 }, { width: 14 }, { width: 14 }, { width: 14 }, { width: 10 }];
      title(ws, mName + ' ' + (o.year || 2027), t.title, 10);
      var w = o.works && o.works[m]; if (w) { ws.mergeCells(2, 12, 2, 16); var cap = ws.getCell(2, 12); cap.value = t.artwork + ': ' + w.t + ' — ' + w.a; cellStyle(cap, { f: { italic: true, size: 9, color: { argb: 'FF7A7066' } }, al: { wrapText: true } }); ws.getRow(2).height = 28; img(ws, m, { col: 11.1, row: 3.2 }, { col: 16, row: 14 }); }
      // summary block A4:D8
      header(ws, 4, 1, ['', t.planned, t.actual, t.diff]);
      var rI = '$D$12:$D$' + (11 + ROWS_INC), rE = '$I$12:$I$' + (11 + ROWS_EXP);
      var lines = [[t.income, "SUM('" + t.settings + "'!$E$9:$E$" + (8 + INC_N) + ')', 'SUM(' + rI + ')', C.inc], [t.expenses, "SUM('" + t.settings + "'!$B$9:$B$" + (8 + EXP_N) + ')', 'SUM(' + rE + ')', C.exp], [t.left, 'B5-B6', 'C5-C6', C.sav]];
      lines.forEach(function (L, i) { var r = 5 + i, a = ws.getCell(r, 1); a.value = L[0]; cellStyle(a, { f: { bold: true, color: { argb: L[3] } }, b: box });
        [2, 3].forEach(function (cc, j) { var c = ws.getCell(r, cc); c.value = { formula: L[1 + j] }; cellStyle(c, { nf: fmt, fill: C.calc, b: box }); });
        var d = ws.getCell(r, 4); d.value = { formula: 'C' + r + '-B' + r }; cellStyle(d, { nf: fmt, fill: C.calc, b: box }); });
      // income table A11:D
      ws.mergeCells(10, 1, 10, 4); var hi = ws.getCell(10, 1); hi.value = t.income; cellStyle(hi, { f: { name: font, size: 14, bold: true, color: { argb: C.inc } } });
      header(ws, 11, 1, [t.date, t.source, t.cat, t.amount], C.inc);
      for (var r = 12; r < 12 + ROWS_INC; r++) { [1, 2, 3, 4].forEach(function (cc) { var c = ws.getCell(r, cc); cellStyle(c, { b: box, nf: cc === 1 ? 'yyyy-mm-dd' : cc === 4 ? fmt : undefined }); }); ws.getCell(r, 3).dataValidation = { type: 'list', allowBlank: true, formulae: [INC_LIST] }; }
      // expense table F11:J
      ws.mergeCells(10, 6, 10, 10); var he = ws.getCell(10, 6); he.value = t.expenses; cellStyle(he, { f: { name: font, size: 14, bold: true, color: { argb: C.exp } } });
      header(ws, 11, 6, [t.date, t.desc, t.cat, t.amount, t.paid], C.exp);
      for (r = 12; r < 12 + ROWS_EXP; r++) { [6, 7, 8, 9, 10].forEach(function (cc) { var c = ws.getCell(r, cc); cellStyle(c, { b: box, nf: cc === 6 ? 'yyyy-mm-dd' : cc === 9 ? fmt : undefined, al: cc === 10 ? { horizontal: 'center' } : undefined }); });
        ws.getCell(r, 8).dataValidation = { type: 'list', allowBlank: true, formulae: [EXP_LIST] }; ws.getCell(r, 10).dataValidation = { type: 'list', allowBlank: true, formulae: ['"' + t.yes + ',' + t.no + '"'] }; }
      // category summary L16:P
      var r0 = 16; ws.mergeCells(r0 - 1, 12, r0 - 1, 16); var hc = ws.getCell(r0 - 1, 12); hc.value = t.byCat; cellStyle(hc, { f: { name: font, size: 14, bold: true, color: { argb: C.head } } });
      header(ws, r0, 12, [t.cat, t.planned, t.actual, t.diff, t.used]);
      t.expCats.forEach(function (n, i) { var rr = r0 + 1 + i; var a = ws.getCell(rr, 12); a.value = { formula: "'" + t.settings + "'!A" + (9 + i) }; cellStyle(a, { b: box });
        var p = ws.getCell(rr, 13); p.value = { formula: "'" + t.settings + "'!B" + (9 + i) }; cellStyle(p, { nf: fmt, b: box, fill: C.calc });
        var ac = ws.getCell(rr, 14); ac.value = { formula: 'SUMIFS($I$12:$I$' + (11 + ROWS_EXP) + ',$H$12:$H$' + (11 + ROWS_EXP) + ',L' + rr + ')' }; cellStyle(ac, { nf: fmt, b: box, fill: C.calc });
        var df = ws.getCell(rr, 15); df.value = { formula: 'M' + rr + '-N' + rr }; cellStyle(df, { nf: fmt, b: box, fill: C.calc });
        var u = ws.getCell(rr, 16); u.value = { formula: 'IF(M' + rr + '=0,0,N' + rr + '/M' + rr + ')' }; cellStyle(u, { nf: '0%', b: box, fill: C.calc }); });
      var last = r0 + EXP_N;
      ws.addConditionalFormatting({ ref: 'P' + (r0 + 1) + ':P' + last, rules: [{ type: 'dataBar', cfvo: [{ type: 'num', value: 0 }, { type: 'num', value: 1 }], color: { argb: 'FF8FB3C9' } }] });
      ws.addConditionalFormatting({ ref: 'O' + (r0 + 1) + ':O' + last, rules: [{ type: 'cellIs', operator: 'lessThan', formulae: ['0'], style: { font: { color: { argb: C.exp }, bold: true } } }] });
      ws.pageSetup = { orientation: 'landscape', fitToPage: true, fitToWidth: 1, fitToHeight: 0, paperSize: 9 };
    });

    // ---- Year overview
    var yo = wb.addWorksheet(t.year, { properties: { tabColor: { argb: C.sav } } });
    yo.columns = [{ width: 22 }].concat(monthNames.map(function () { return { width: 12 }; })).concat([{ width: 14 }]);
    title(yo, t.year + ' ' + (o.year || 2027), t.title, 14);
    header(yo, 4, 1, [''].concat(monthNames).concat([t.total]));
    [[t.income, 'C5', C.inc], [t.expenses, 'C6', C.exp], [t.net, 'C7', C.sav]].forEach(function (L, i) { var r = 5 + i, a = yo.getCell(r, 1); a.value = L[0]; cellStyle(a, { f: { bold: true, color: { argb: L[2] } }, b: box });
      monthNames.forEach(function (mn, m) { var c = yo.getCell(r, 2 + m); c.value = { formula: "'" + mn + "'!" + L[1] }; cellStyle(c, { nf: fmt, fill: C.calc, b: box }); });
      var s = yo.getCell(r, 14); s.value = { formula: 'SUM(B' + r + ':M' + r + ')' }; cellStyle(s, { nf: fmt, f: { bold: true }, fill: C.calc, b: box }); });
    yo.getCell(9, 1).value = t.startBal + ' + ' + t.net; cellStyle(yo.getCell(9, 1), { f: { bold: true } });
    var eb = yo.getCell(9, 14); eb.value = { formula: "'" + t.settings + "'!B6+N7" }; cellStyle(eb, { nf: fmt, f: { bold: true }, fill: C.calc, b: box });
    header(yo, 11, 1, [t.byCat].concat(monthNames).concat([t.total]));
    t.expCats.forEach(function (n, i) { var r = 12 + i, a = yo.getCell(r, 1); a.value = { formula: "'" + t.settings + "'!A" + (9 + i) }; cellStyle(a, { b: box });
      monthNames.forEach(function (mn, m) { var c = yo.getCell(r, 2 + m); c.value = { formula: "'" + mn + "'!N" + (17 + i) }; cellStyle(c, { nf: fmt, b: box, fill: C.calc }); });
      var s = yo.getCell(r, 14); s.value = { formula: 'SUM(B' + r + ':M' + r + ')' }; cellStyle(s, { nf: fmt, f: { bold: true }, b: box, fill: C.calc }); });
    yo.addConditionalFormatting({ ref: 'N12:N' + (11 + EXP_N), rules: [{ type: 'dataBar', cfvo: [{ type: 'min' }, { type: 'max' }], color: { argb: 'FFE7A39A' } }] });
    yo.addConditionalFormatting({ ref: 'B7:M7', rules: [{ type: 'cellIs', operator: 'lessThan', formulae: ['0'], style: { font: { color: { argb: C.exp }, bold: true } } }] });

    // ---- Bills
    var bl = wb.addWorksheet(t.bills, { properties: { tabColor: { argb: 'FFB9D7A8' } } });
    bl.columns = [{ width: 26 }, { width: 10 }, { width: 14 }, { width: 12 }, { width: 10 }].concat(monthNames.map(function () { return { width: 7 }; }));
    title(bl, t.bills, t.title, 17);
    header(bl, 4, 1, [t.bill, t.due, t.amount, t.freq, t.auto].concat(monthNames));
    for (var b = 5; b < 35; b++) { for (var k = 1; k <= 17; k++) { var c = bl.getCell(b, k); cellStyle(c, { b: box, nf: k === 3 ? fmt : undefined, al: k > 3 ? { horizontal: 'center' } : undefined }); if (k > 5) c.dataValidation = { type: 'list', allowBlank: true, formulae: ['"✓"'] }; } bl.getCell(b, 5).dataValidation = { type: 'list', allowBlank: true, formulae: ['"' + t.yes + ',' + t.no + '"'] }; }
    var bt = bl.getCell(35, 2); bt.value = t.total; cellStyle(bt, { f: { bold: true } }); var bv = bl.getCell(35, 3); bv.value = { formula: 'SUM(C5:C34)' }; cellStyle(bv, { nf: fmt, f: { bold: true }, fill: C.calc });

    // ---- Savings goals
    var sg = wb.addWorksheet(t.goals, { properties: { tabColor: { argb: C.sav } } });
    sg.columns = [{ width: 26 }, { width: 14 }, { width: 14 }, { width: 12 }, { width: 14 }, { width: 16 }];
    title(sg, t.goals, t.title, 6);
    header(sg, 4, 1, [t.goal, t.target, t.saved, t.progress, t.tdate, t.perMonth]);
    for (var g = 5; g < 17; g++) { [1, 2, 3, 5].forEach(function (cc) { cellStyle(sg.getCell(g, cc), { b: box, nf: cc === 2 || cc === 3 ? fmt : cc === 5 ? 'yyyy-mm-dd' : undefined }); });
      var pg = sg.getCell(g, 4); pg.value = { formula: 'IF(B' + g + '=0,0,MIN(1,C' + g + '/B' + g + '))' }; cellStyle(pg, { nf: '0%', b: box, fill: C.calc });
      var pm = sg.getCell(g, 6); pm.value = { formula: 'IF(OR(B' + g + '=0,E' + g + '=""),0,MAX(0,(B' + g + '-C' + g + ')/MAX(1,DATEDIF(TODAY(),E' + g + ',"m"))))' }; cellStyle(pm, { nf: fmt, b: box, fill: C.calc }); }
    sg.addConditionalFormatting({ ref: 'D5:D16', rules: [{ type: 'dataBar', cfvo: [{ type: 'num', value: 0 }, { type: 'num', value: 1 }], color: { argb: 'FF8FC9A3' } }] });

    // ---- Debt payoff
    var dp = wb.addWorksheet(t.debt, { properties: { tabColor: { argb: C.exp } } });
    dp.columns = [{ width: 24 }, { width: 14 }, { width: 14 }, { width: 16 }, { width: 18 }, { width: 14 }];
    title(dp, t.debt, t.title, 6);
    header(dp, 4, 1, [t.debtN, t.bal, t.rate, t.minp, t.months2, t.interest]);
    for (var d = 5; d < 15; d++) { [1, 2, 3, 4].forEach(function (cc) { cellStyle(dp.getCell(d, cc), { b: box, nf: cc === 2 || cc === 4 ? fmt : cc === 3 ? '0.00' : undefined }); });
      var mo = dp.getCell(d, 5); mo.value = { formula: 'IF(OR(B' + d + '<=0,D' + d + '<=0),"",IF(C' + d + '=0,ROUNDUP(B' + d + '/D' + d + ',0),IF(D' + d + '<=B' + d + '*C' + d + '/1200,"—",ROUNDUP(NPER(C' + d + '/1200,-D' + d + ',B' + d + '),0))))' }; cellStyle(mo, { b: box, fill: C.calc, al: { horizontal: 'center' } });
      var it = dp.getCell(d, 6); it.value = { formula: 'IF(ISNUMBER(E' + d + '),MAX(0,E' + d + '*D' + d + '-B' + d + '),"")' }; cellStyle(it, { nf: fmt, b: box, fill: C.calc }); }

    // ---- Start here (first tab)
    var sh = wb.addWorksheet(t.start, { properties: { tabColor: { argb: C.ink } } });
    sh.columns = [{ width: 4 }, { width: 90 }];
    sh.mergeCells(2, 2, 2, 2); var ct = sh.getCell(2, 2); ct.value = (o.name || t.title) + ' ' + (o.year || 2027); cellStyle(ct, { f: { name: font, size: 26, bold: true, color: { argb: C.ink } } }); sh.getRow(2).height = 40;
    t.how.forEach(function (h, i) { var c = sh.getCell(4 + i, 2); c.value = h; cellStyle(c, { f: { size: 12 }, al: { wrapText: true, vertical: 'top' } }); sh.getRow(4 + i).height = 34; });
    if (o.works) o.works.forEach(function (w, i) { var c = sh.getCell(14 + i, 2); c.value = t.mshort[i] + ' — ' + w.t + ', ' + w.a + (w.d ? ' (' + w.d + ')' : ''); cellStyle(c, { f: { size: 10, color: { argb: 'FF7A7066' } } }); });
    img(sh, 12, { col: 2.6, row: 1 }, { col: 2.98, row: 12 });
    sh.getCell(27, 2).value = '© Arttrip Studio · arttripstudio.com'; cellStyle(sh.getCell(27, 2), { f: { size: 9, color: { argb: 'FF9A9088' } } });
    // order tabs: Start, Settings, months..., Year, Bills, Goals, Debt
    wb.worksheets.forEach(function (w) { w.orderNo = w.name === t.start ? 0 : w.name === t.settings ? 1 : w.id + 1; });
    // currency: replace "$" number format with the chosen symbol
    var sym = (o.currency || '$').replace(/"/g, ''); if (sym !== '$') wb.eachSheet(function (w) { w.eachRow(function (row) { row.eachCell(function (c) { if (c.numFmt === fmt) c.numFmt = '"' + sym + '"#,##0' + (sym === '₩' || sym === '¥' ? '' : '.00'); }); }); });
    return wb;
  }
  root.Budget = { build: build, TX: TX };
})(typeof window !== 'undefined' ? window : globalThis);
