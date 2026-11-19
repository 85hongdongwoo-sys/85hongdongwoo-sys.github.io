import json, sys, datetime
lang, i, hhmm = sys.argv[1], int(sys.argv[2]), sys.argv[3]
rows = json.load(open(f'/mnt/user-data/outputs/yt/{lang}_rows.json'))
r = dict(rows[i]); d = datetime.date(2026, 11, 18) + datetime.timedelta(days=i)
h, m = map(int, hhmm.split(':'))
r.update(date=f'{d.year}. {d.month}. {d.day}.', month=d.month, day=d.day, time=f"{'오전' if h < 12 else '오후'} {h % 12 or 12}:{m:02d}")
js = open('/home/claude/ytup/up2.js').read().replace('__ROW__', json.dumps({k: r[k] for k in ('title', 'description', 'tags', 'playlist', 'date', 'month', 'day', 'time')}, ensure_ascii=False))
open(f'/home/claude/ytup/run_{lang}_{i}.js', 'w').write(js); print(r['file'], r['date'], r['time'])
