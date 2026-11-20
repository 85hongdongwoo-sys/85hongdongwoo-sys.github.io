"""공식 시험 링크 점검: 게시글마다 첫 파일 1개씩 실제로 받아지는지 확인(앞부분만 읽음).
결과는 build/exams/data/link_report.json — 깨진 링크 목록."""
import json, os, time, urllib.request

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
UA = {'User-Agent': 'Mozilla/5.0 (honglife.co.kr exam-link check)', 'Range': 'bytes=0-1023'}


def ok(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
            head = r.read(1024)
            ctype = r.headers.get('Content-Type', '')
            return r.status in (200, 206) and not (b'<html' in head.lower() and 'html' in ctype)
    except Exception:
        return False


def main():
    k = json.load(open(os.path.join(D, 'kice.json'), encoding='utf-8'))
    bad, n = [], 0
    for board, items in k['boards'].items():
        for it in items:
            if not it['files']:
                continue
            name, seq = it['files'][0]
            url = f'https://www.suneung.re.kr/boardCnts/fileDown.do?fileSeq={seq}'
            n += 1
            if not ok(url):
                bad.append({'board': board, 'y': it['y'], 'mon': it['mon'], 'area': it['area'], 'file': name, 'url': url})
            time.sleep(0.3)
    rep = {'checked': time.strftime('%Y-%m-%d'), 'tested': n, 'broken': bad}
    json.dump(rep, open(os.path.join(D, 'link_report.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('tested', n, 'broken', len(bad))


if __name__ == '__main__':
    main()
