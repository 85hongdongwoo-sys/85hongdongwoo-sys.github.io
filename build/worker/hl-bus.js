// 홍라이프 셔틀 위치 공유 서버 (Cloudflare Worker + KV)
// 설정: Workers → hl-bus 만들기 → 이 코드 붙여넣기 → Settings → Bindings → KV namespace 추가 (변수 이름: BUS)
const ALLOW = ['https://honglife.co.kr', 'https://www.honglife.co.kr'];
const TTL = 60 * 60 * 10; // 10시간 뒤 자동 삭제

function cors(origin) {
  const o = ALLOW.includes(origin) || /^http:\/\/localhost(:\d+)?$/.test(origin || '') ? origin : ALLOW[0];
  return { 'Access-Control-Allow-Origin': o, 'Access-Control-Allow-Methods': 'GET,POST,OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type', 'Vary': 'Origin' };
}
function json(obj, status, origin) {
  return new Response(JSON.stringify(obj), { status: status || 200, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...cors(origin) } });
}
async function sha(s) {
  const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join('').slice(0, 32);
}
const num = (v, lo, hi) => (typeof v === 'number' && isFinite(v) && v >= lo && v <= hi ? Math.round(v * 1e6) / 1e6 : null);

export default {
  async fetch(req, env) {
    const url = new URL(req.url), origin = req.headers.get('Origin') || '';
    if (req.method === 'OPTIONS') return new Response(null, { headers: cors(origin) });
    const m = url.pathname.match(/^\/b\/([a-z0-9]{10,20})$/);
    if (!m) return json({ ok: true, service: 'hl-bus' }, 200, origin);
    const id = m[1], key = 'b:' + id;
    if (req.method === 'GET') {
      const v = await env.BUS.get(key, { type: 'json', cacheTtl: 30 });
      if (!v) return json({ none: true }, 404, origin);
      delete v.o; v.now = Date.now();
      return json(v, 200, origin);
    }
    if (req.method !== 'POST') return json({ err: 'method' }, 405, origin);
    if (origin && !ALLOW.includes(origin) && !/^http:\/\/localhost(:\d+)?$/.test(origin)) return json({ err: 'origin' }, 403, origin);
    let d; try { d = await req.json(); } catch (e) { return json({ err: 'json' }, 400, origin); }
    if (!/^[a-z0-9]{16,40}$/.test(d.k || '')) return json({ err: 'key' }, 400, origin);
    const o = await sha(d.k + ':' + id);
    const cur = await env.BUS.get(key, { type: 'json' });
    if (cur && cur.o !== o) return json({ err: 'owner' }, 403, origin);
    const v = cur || { o, start: Date.now() };
    if (d.name != null) v.name = String(d.name).slice(0, 40);
    if (Array.isArray(d.stops)) v.stops = d.stops.slice(0, 60).map(s => [num(s[0], 30, 45), num(s[1], 120, 135), String(s[2] || '').slice(0, 30)]).filter(s => s[0] && s[1]);
    const lat = num(d.lat, 30, 45), lng = num(d.lng, 120, 135);
    if (lat && lng) { v.lat = lat; v.lng = lng; v.t = Date.now(); }
    if (d.spd != null) v.spd = num(d.spd, 0, 60);
    if (d.ix != null) v.ix = Math.max(-1, Math.min(60, d.ix | 0));
    if (d.start) { v.start = Date.now(); v.end = 0; v.ix = -1; }
    if (d.end) v.end = Date.now();
    await env.BUS.put(key, JSON.stringify(v), { expirationTtl: TTL });
    return json({ ok: true }, 200, origin);
  }
};
