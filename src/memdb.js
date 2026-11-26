// In-memory stand-in for D1, used when no DB binding exists. Handles exactly the queries index.js makes.
import ROWS from './data.js';
const hash = (id) => Number((BigInt(parseInt(id, 10)) * 2654435761n) % 1000n);
function run(sql, a) {
  const s = sql.replace(/\s+/g, ' ').trim();
  let m;
  if ((m = s.match(/^SELECT \* FROM artworks WHERE id IN \((.+)\)$/))) { const ids = m[1].match(/'(\d+)'/g).map((x) => x.slice(1, -1)); return ROWS.filter((r) => ids.includes(r.id)); }
  if (s.startsWith('SELECT theme, COUNT(*) n, MIN(id) id')) { const g = {}; for (const r of ROWS) { (g[r.theme] ||= { theme: r.theme, n: 0, id: r.id }); g[r.theme].n++; if (r.id < g[r.theme].id) g[r.theme].id = r.id; } return Object.values(g).sort((x, y) => y.n - x.n); }
  if (s.startsWith('SELECT theme, id FROM artworks WHERE id IN (SELECT MIN(id)')) { const g = {}; for (const r of ROWS) if (!g[r.theme] || r.id < g[r.theme].id) g[r.theme] = { theme: r.theme, id: r.id }; return Object.values(g); }
  if ((m = s.match(/^SELECT COUNT\(\*\) n FROM artworks WHERE (.+)$/))) return [{ n: filt(m[1], a).length }];
  if (s === 'SELECT COUNT(*) n FROM artworks') return [{ n: ROWS.length }];
  if ((m = s.match(/^SELECT \* FROM artworks WHERE (.+) ORDER BY CASE WHEN title_ko <> '' THEN 0 ELSE 1 END, rowid LIMIT \? OFFSET \?$/))) { const n = (m[1].match(/\?/g) || []).length; const r = filt(m[1], a.slice(0, n)); const sorted = [...r.filter((x) => x.title_ko), ...r.filter((x) => !x.title_ko)]; return sorted.slice(a[n + 1], a[n + 1] + a[n]); }
  if (s === 'SELECT * FROM artworks WHERE slug = ?') return ROWS.filter((r) => r.slug === a[0]);
  if (s.startsWith('SELECT * FROM artworks WHERE artist_slug = ? AND id <> ?')) return ROWS.filter((r) => r.artist_slug === a[0] && r.id !== a[1]).slice(0, 8);
  if (s.startsWith('SELECT * FROM artworks WHERE theme = ? AND id <> ? AND artist_slug <> ?')) return ROWS.filter((r) => r.theme === a[0] && r.id !== a[1] && r.artist_slug !== a[2]).sort((x, y) => hash(x.id) - hash(y.id)).slice(0, 8);
  if (s.startsWith('SELECT artist_slug s, COUNT(*) c')) { const g = {}; for (const r of ROWS) g[r.artist_slug] = (g[r.artist_slug] || 0) + 1; return Object.entries(g).filter(([, c]) => c >= 2).map(([s2, c]) => ({ s: s2, c })); }
  if (s === 'SELECT slug FROM artworks ORDER BY rowid LIMIT ? OFFSET ?') return ROWS.slice(a[1], a[1] + a[0]).map((r) => ({ slug: r.slug }));
  const pick = (r) => ({ id: r.id, t: r.title, tk: r.title_ko, a: r.artist, ak: r.artist_ko, w: r.w, h: r.h, theme: r.theme });
  if (s.startsWith("SELECT id, title t, title_ko tk, artist a, artist_ko ak, w, h, theme FROM artworks WHERE title_ko <> ''")) return ROWS.filter((r) => r.title_ko).slice(0, 120).map(pick);
  if (s.startsWith('SELECT id, title t, title_ko tk, artist a, artist_ko ak, w, h, theme FROM artworks WHERE id = ?')) return ROWS.filter((r) => r.id === a[0]).map(pick);
  if (s === 'SELECT id, title t, title_ko tk, artist a, artist_ko ak, artist_slug "as", w, h, theme FROM artworks ORDER BY rowid') return ROWS.map((r) => ({ ...pick(r), as: r.artist_slug }));
  throw new Error('memdb: unsupported query: ' + s);
}
function filt(where, a) {
  const w = where.trim();
  if (w === '1=1' || w === '1') return ROWS;
  if (w === 'theme = ?') return ROWS.filter((r) => r.theme === a[0]);
  if (w === 'artist_slug = ?') return ROWS.filter((r) => r.artist_slug === a[0]);
  throw new Error('memdb: unsupported where: ' + w);
}
export const memdb = { prepare: (sql) => ({ bind: (...a) => ({ all: async () => ({ results: run(sql, a) }), first: async () => run(sql, a)[0] ?? null }) }) };
