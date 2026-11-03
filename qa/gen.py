#!/usr/bin/env python3
"""Build /qa/ pages from qa/data.json.  Run from the site root:  python3 qa/gen.py
data.json: {"items":[{"id":"2026-11-04-1","cc":"kr","date":"2026-11-04","q":"...","a":"<p>...</p>","links":[["/yet.html","연말정산 환급 계산기"]]}]}
Answers are HTML (p, ul, li, b, a only). Questions are plain text (escaped here)."""
import json, html, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORM = "https://docs.google.com/forms/d/e/1FAIpQLSeA5Bh3_D1RpNUhxMn0aUQs7giD-BXIGXLWxNyWTmqidjKEvA/viewform"
ENTRY = "entry.1856189224"
C = [  # cc, form option, lang, flag, local name, hub link, hub label
 ("kr","한국 · Korea","ko","🇰🇷","한국","/","홍라이프 계산기"),
 ("us","미국 · United States","en","🇺🇸","United States","/us/","US calculators"),
 ("jp","일본 · Japan","ja","🇯🇵","日本","/jp/","日本の計算ツール"),
 ("uk","영국 · United Kingdom","en","🇬🇧","United Kingdom","/uk/","UK calculators"),
 ("ca","캐나다 · Canada","en","🇨🇦","Canada","/ca/","Canada calculators"),
 ("au","호주 · Australia","en","🇦🇺","Australia","/au/","Australia calculators"),
 ("de","독일 · Deutschland","de","🇩🇪","Deutschland","/de/","Rechner Deutschland"),
 ("fr","프랑스 · France","fr","🇫🇷","France","/fr/","Calculateurs France"),
 ("es","스페인 · España","es","🇪🇸","España","/es/","Calculadoras España"),
 ("it","이탈리아 · Italia","it","🇮🇹","Italia","/it/stipendio/","Calcolatori Italia"),
 ("mx","멕시코 · México","es","🇲🇽","México","/mx/","Calculadoras México"),
 ("br","브라질 · Brasil","pt","🇧🇷","Brasil","/br/","Calculadoras Brasil"),
 ("in","인도 · India","en","🇮🇳","India","/in/","India calculators"),
 ("ph","필리핀 · Philippines","en","🇵🇭","Philippines","/ph/","Philippines calculators"),
 ("pt","포르투갈 · Portugal","pt","🇵🇹","Portugal","/pt/salario/","Calculadoras Portugal"),
 ("nl","네덜란드 · Nederland","nl","🇳🇱","Nederland","/nl/salaris/","Rekenhulpen Nederland"),
 ("pl","폴란드 · Polska","pl","🇵🇱","Polska","/pl/wynagrodzenie/","Kalkulatory Polska"),
 ("id","인도네시아 · Indonesia","id","🇮🇩","Indonesia","/id/","Kalkulator Indonesia"),
 ("other","기타 국가 · Other country","en","🌐","Other countries","/en/","English calculators"),
]
T = {
 "ko":dict(t="{n} 세금·월급 Q&A",d="{n}의 세금·월급·연말정산·대출 질문과 답변. 질문을 남기면 보통 1~2일 안에 답변해요.",ask="질문 남기기",empty="아직 답변된 질문이 없어요. 첫 질문을 남겨 주세요.",q="질문",a="답변",asked="질문일",more="관련 계산기",note="답변은 일반 정보이며 세무·법률 자문이 아니에요. 개인정보는 지우고 공개해요.",home="홈",all="전체 Q&A",count="답변 {k}개"),
 "en":dict(t="{n} tax & salary Q&A",d="Questions and answers about tax, salary, refunds and loans in {n}. Ask yours — answers are usually posted within 1–2 days.",ask="Ask a question",empty="No answered questions yet. Be the first to ask.",q="Question",a="Answer",asked="Asked",more="Related calculators",note="General information only, not tax or legal advice. Personal details are removed before publishing.",home="Home",all="All Q&A",count="{k} answered"),
 "ja":dict(t="{n} 税金・給与 Q&A",d="{n}の税金・給与・年末調整・ローンに関する質問と回答。質問いただくと通常1〜2日以内に回答します。",ask="質問する",empty="まだ回答済みの質問はありません。最初の質問をどうぞ。",q="質問",a="回答",asked="質問日",more="関連する計算ツール",note="一般的な情報であり、税務・法律の助言ではありません。個人情報は削除して公開します。",home="ホーム",all="すべてのQ&A",count="回答 {k}件"),
 "de":dict(t="{n}: Fragen & Antworten zu Steuer und Gehalt",d="Fragen und Antworten zu Steuer, Gehalt, Weihnachtsgeld und Krediten in {n}. Antworten meist innerhalb von 1–2 Tagen.",ask="Frage stellen",empty="Noch keine beantworteten Fragen. Stellen Sie die erste.",q="Frage",a="Antwort",asked="Gefragt am",more="Passende Rechner",note="Allgemeine Informationen, keine Steuer- oder Rechtsberatung. Persönliche Daten werden vor der Veröffentlichung entfernt.",home="Start",all="Alle Fragen",count="{k} beantwortet"),
 "fr":dict(t="{n} : questions-réponses impôts et salaire",d="Questions et réponses sur l'impôt, le salaire, le chômage et les crédits en {n}. Réponse en général sous 1 à 2 jours.",ask="Poser une question",empty="Aucune question répondue pour l'instant. Posez la première.",q="Question",a="Réponse",asked="Posée le",more="Calculateurs utiles",note="Information générale, pas un conseil fiscal ou juridique. Les données personnelles sont retirées avant publication.",home="Accueil",all="Toutes les questions",count="{k} réponses"),
 "es":dict(t="{n}: preguntas y respuestas sobre impuestos y sueldo",d="Preguntas y respuestas sobre impuestos, sueldo, paga extra y préstamos en {n}. Solemos responder en 1–2 días.",ask="Hacer una pregunta",empty="Aún no hay preguntas respondidas. Sé el primero en preguntar.",q="Pregunta",a="Respuesta",asked="Fecha",more="Calculadoras relacionadas",note="Información general, no asesoramiento fiscal ni legal. Eliminamos los datos personales antes de publicar.",home="Inicio",all="Todas las preguntas",count="{k} respondidas"),
 "it":dict(t="{n}: domande e risposte su tasse e stipendio",d="Domande e risposte su tasse, stipendio, NASpI e prestiti in {n}. Di solito rispondiamo entro 1–2 giorni.",ask="Fai una domanda",empty="Ancora nessuna domanda con risposta. Fai la prima.",q="Domanda",a="Risposta",asked="Data",more="Calcolatori utili",note="Informazioni generali, non consulenza fiscale o legale. I dati personali vengono rimossi prima della pubblicazione.",home="Home",all="Tutte le domande",count="{k} risposte"),
 "pt":dict(t="{n}: perguntas e respostas sobre impostos e salário",d="Perguntas e respostas sobre impostos, salário e financiamento em {n}. Respondemos normalmente em 1–2 dias.",ask="Fazer uma pergunta",empty="Ainda não há perguntas respondidas. Faça a primeira.",q="Pergunta",a="Resposta",asked="Data",more="Calculadoras relacionadas",note="Informação geral, não é aconselhamento fiscal ou jurídico. Dados pessoais são removidos antes da publicação.",home="Início",all="Todas as perguntas",count="{k} respondidas"),
 "nl":dict(t="{n}: vragen en antwoorden over belasting en salaris",d="Vragen en antwoorden over belasting, salaris, WW en leningen in {n}. Meestal beantwoord binnen 1–2 dagen.",ask="Stel een vraag",empty="Nog geen beantwoorde vragen. Stel de eerste.",q="Vraag",a="Antwoord",asked="Gesteld op",more="Handige rekenhulpen",note="Algemene informatie, geen belasting- of juridisch advies. Persoonsgegevens worden verwijderd vóór publicatie.",home="Home",all="Alle vragen",count="{k} beantwoord"),
 "pl":dict(t="{n}: pytania i odpowiedzi o podatkach i wynagrodzeniu",d="Pytania i odpowiedzi o podatkach, wynagrodzeniu, zasiłku i kredytach w {n}. Odpowiadamy zwykle w ciągu 1–2 dni.",ask="Zadaj pytanie",empty="Brak jeszcze odpowiedzi. Zadaj pierwsze pytanie.",q="Pytanie",a="Odpowiedź",asked="Data",more="Przydatne kalkulatory",note="Informacje ogólne, nie porada podatkowa ani prawna. Dane osobowe usuwamy przed publikacją.",home="Start",all="Wszystkie pytania",count="{k} odpowiedzi"),
 "id":dict(t="{n}: tanya jawab pajak dan gaji",d="Tanya jawab seputar pajak, gaji, dan pinjaman di {n}. Biasanya dijawab dalam 1–2 hari.",ask="Ajukan pertanyaan",empty="Belum ada pertanyaan yang dijawab. Jadilah yang pertama.",q="Pertanyaan",a="Jawaban",asked="Tanggal",more="Kalkulator terkait",note="Informasi umum, bukan nasihat pajak atau hukum. Data pribadi dihapus sebelum dipublikasikan.",home="Beranda",all="Semua tanya jawab",count="{k} dijawab"),
}
HEAD = open(os.path.join(ROOT,"qa","_head.html"),encoding="utf-8").read()
E = html.escape
def prefill(opt):
    from urllib.parse import quote_plus
    return FORM+"?usp=pp_url&"+ENTRY+"="+quote_plus(opt)
def clean_answer(a):
    # allow only a small tag set
    return re.sub(r"<(?!/?(p|ul|ol|li|b|strong|a)(\s[^>]*)?>)[^>]*>","",a)
def page(path,lang,title,desc,body,ld,noindex=False):
    h = HEAD.replace("{LANG}",lang).replace("{TITLE}",E(title)).replace("{DESC}",E(desc)).replace("{URL}","https://honglife.co.kr"+path)
    h = h.replace("{ROBOTS}", '<meta name="robots" content="noindex,follow">' if noindex else "")
    h = h.replace("{LD}", "".join('<script type="application/ld+json">'+json.dumps(x,ensure_ascii=False)+"</script>\n" for x in ld))
    return h+body+'\n<script src="/assets/app.js" defer></script>\n<script src="/assets/share.js" defer></script>\n</body>\n</html>\n'
def build():
    data = json.load(open(os.path.join(ROOT,"qa","data.json"),encoding="utf-8"))
    items = sorted(data.get("items",[]), key=lambda x:(x["date"],x["id"]), reverse=True)
    by = {c[0]:[i for i in items if i["cc"]==c[0]] for c in C}
    out = []
    for cc,opt,lang,flag,name,hub,hublabel in C:
        L=T[lang]; lst=by[cc]; path="/qa/%s.html"%cc
        title=L["t"].format(n=name); desc=L["d"].format(n=name)
        cards=[]
        for it in lst:
            links="".join('<a href="%s">%s</a>'%(E(u),E(t)) for u,t in it.get("links",[]))
            cards.append('<article class="qa" id="%s"><p class="qq"><span>%s</span>%s</p><div class="qa-a"><span>%s</span>%s</div>%s<p class="qd">%s %s</p></article>'%(
                E(it["id"]),L["q"],E(it["q"]),L["a"],clean_answer(it["a"]),('<p class="ql">'+links+'</p>') if links else "",L["asked"],E(it["date"])))
        body=('<div class="brandbar"><div class="in"><a class="logo" href="/"><i>₩</i>홍라이프</a><span class="meta"><a href="/qa/">%s</a><a href="%s">%s</a></span></div></div>\n<div class="wrap">'
              '<nav class="crumb"><a href="/">%s</a> › <a href="/qa/">Q&amp;A</a> › <span>%s</span></nav>'
              '<header class="top"><p class="kicker">%s %s · %s</p><h1>%s</h1><p class="lead">%s</p><a class="btn" href="%s" target="_blank" rel="noopener">✍️ %s →</a></header>'
              '%s<p class="note">%s</p><p class="more"><a href="%s">%s →</a></p></div>')%(
              L["all"],hub,E(hublabel),L["home"],E(name),flag,E(name),L["count"].format(k=len(lst)),E(title),E(desc),E(prefill(opt)),L["ask"],
              ("".join(cards) if cards else '<p class="empty">%s</p>'%L["empty"]),L["note"],hub,E(hublabel))
        ld=[{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://honglife.co.kr/"},{"@type":"ListItem","position":2,"name":"Q&A","item":"https://honglife.co.kr/qa/"},{"@type":"ListItem","position":3,"name":name,"item":"https://honglife.co.kr"+path}]}]
        if lst:
            ld.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":it["q"],"acceptedAnswer":{"@type":"Answer","text":re.sub(r"<[^>]+>"," ",it["a"]).strip()}} for it in lst[:30]]})
        open(os.path.join(ROOT,path.lstrip("/")),"w",encoding="utf-8").write(page(path,lang,title,desc,body,ld,noindex=not lst))
        out.append(path)
    # hub
    L=T["ko"]
    tiles="".join('<a class="tile" href="/qa/%s.html"><b>%s %s</b><span>%s</span></a>'%(cc,flag,E(name),(T[lang]["count"].format(k=len(by[cc]))) ) for cc,opt,lang,flag,name,hub,hl in C)
    latest="".join('<li><a href="/qa/%s.html#%s">%s</a></li>'%(i["cc"],E(i["id"]),E(i["q"][:90])) for i in items[:10])
    body=('<div class="brandbar"><div class="in"><a class="logo" href="/"><i>₩</i>홍라이프 계산기</a><span class="meta"><a href="/">계산기 홈</a></span></div></div>\n<div class="wrap">'
          '<nav class="crumb"><a href="/">홈</a> › <span>Q&amp;A</span></nav>'
          '<header class="top"><p class="kicker">국가별 Q&amp;A · Ask in any language</p><h1>세금·월급 Q&amp;A <small>Tax &amp; salary Q&amp;A by country</small></h1>'
          '<p class="lead">나라를 고르고 궁금한 점을 남겨 주세요. 보통 1~2일 안에 답변을 달아 국가별 페이지에 공개해요. 이름·연락처 같은 개인정보는 적지 마세요.<br>Pick your country and ask anything about tax, salary, refunds or loans — in any language. Answers are posted within 1–2 days.</p>'
          '<a class="btn" href="%s" target="_blank" rel="noopener">✍️ 질문 남기기 · Ask a question →</a></header>'
          '<section class="card"><h2>국가별 Q&amp;A · By country</h2><div class="tiles">%s</div></section>%s'
          '<p class="note">답변은 일반 정보이며 세무·법률 자문이 아니에요. · General information only, not tax or legal advice.</p></div>')%(
          E(FORM),tiles,('<section class="card"><h2>최근 답변 · Latest answers</h2><ul class="latest">%s</ul></section>'%latest) if latest else "")
    ld=[{"@context":"https://schema.org","@type":"CollectionPage","name":"세금·월급 Q&A · Tax & salary Q&A by country","url":"https://honglife.co.kr/qa/"}]
    open(os.path.join(ROOT,"qa","index.html"),"w",encoding="utf-8").write(page("/qa/","ko","국가별 세금·월급 Q&A · Tax & salary Q&A by country | 홍라이프","나라별로 세금·월급·연말정산·대출 질문을 남기면 1~2일 안에 답변해요. Ask tax and salary questions by country in any language.",body,ld))
    answered=[c[0] for c in C if by[c[0]]]
    return ["/qa/"]+["/qa/%s.html"%c for c in answered]
if __name__=="__main__":
    urls=build(); print("indexable:",urls)
