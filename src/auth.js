// Members: Google Sign-In → session cookie, saved Studio designs, Polar subscription status.
// Needs env.UDB (D1, see schema-users.sql) and env.GOOGLE_CLIENT_ID. Without them member features say "coming soon".
const enc = new TextEncoder();
const hex = (buf) => [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
const b64u = (s) => Uint8Array.from(atob(s.replace(/-/g, '+').replace(/_/g, '/').padEnd(Math.ceil(s.length / 4) * 4, '=')), (c) => c.charCodeAt(0));
const json = (o, status = 200, extra = {}) => new Response(JSON.stringify(o), { status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', ...extra } });
export const membersReady = (env) => !!(env.UDB && env.GOOGLE_CLIENT_ID);

let certs = null, certsAt = 0;
async function googleKey(kid) {
  if (!certs || Date.now() - certsAt > 3600e3) { certs = (await (await fetch('https://www.googleapis.com/oauth2/v3/certs')).json()).keys; certsAt = Date.now(); }
  const k = certs.find((x) => x.kid === kid); if (!k) return null;
  return crypto.subtle.importKey('jwk', { kty: k.kty, n: k.n, e: k.e, alg: 'RS256', ext: true }, { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' }, false, ['verify']);
}
async function verifyGoogle(token, clientId) {
  const [h, p, s] = String(token).split('.'); if (!s) return null;
  const head = JSON.parse(new TextDecoder().decode(b64u(h))), body = JSON.parse(new TextDecoder().decode(b64u(p)));
  const key = await googleKey(head.kid); if (!key) return null;
  const ok = await crypto.subtle.verify('RSASSA-PKCS1-v1_5', key, b64u(s), enc.encode(h + '.' + p));
  if (!ok || body.aud !== clientId || !['accounts.google.com', 'https://accounts.google.com'].includes(body.iss) || body.exp * 1000 < Date.now() || !body.email_verified) return null;
  return body;
}
function cookie(req, name) { const m = (req.headers.get('cookie') || '').match(new RegExp('(?:^|;\\s*)' + name + '=([^;]+)')); return m ? m[1] : null; }
export async function currentUser(req, env) {
  if (!membersReady(env)) return null; const sid = cookie(req, 'sid'); if (!sid) return null;
  return env.UDB.prepare('SELECT u.id, u.email, u.name, u.picture, u.plan FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.id = ? AND s.expires > ?').bind(sid, Date.now()).first();
}
async function verifyPolar(req, body, secret) {
  const id = req.headers.get('webhook-id'), ts = req.headers.get('webhook-timestamp'), sig = req.headers.get('webhook-signature') || '';
  if (!id || !ts || Math.abs(Date.now() / 1000 - +ts) > 300) return false;
  const key = await crypto.subtle.importKey('raw', enc.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const mac = btoa(String.fromCharCode(...new Uint8Array(await crypto.subtle.sign('HMAC', key, enc.encode(id + '.' + ts + '.' + body)))));
  return sig.split(' ').some((x) => x.split(',')[1] === mac);
}

export async function api(p, req, env) {
  if (p === '/api/polar/webhook' && req.method === 'POST') {
    if (!env.POLAR_WEBHOOK_SECRET || !env.UDB) return json({ error: 'not configured' }, 501);
    const body = await req.text(); if (!(await verifyPolar(req, body, env.POLAR_WEBHOOK_SECRET))) return json({ error: 'bad signature' }, 401);
    const ev = JSON.parse(body), d = ev.data || {}, email = (d.customer?.email || d.user?.email || '').toLowerCase();
    if (email && /^subscription\./.test(ev.type)) {
      const plan = ['active', 'trialing'].includes(d.status) ? 'member' : 'free';
      await env.UDB.prepare('INSERT INTO users (email, plan, created) VALUES (?, ?, ?) ON CONFLICT(email) DO UPDATE SET plan = excluded.plan').bind(email, plan, Date.now()).run();
    }
    return json({ ok: true });
  }
  if (!membersReady(env)) return json({ error: 'members coming soon' }, 503);
  if (p === '/api/auth/google' && req.method === 'POST') {
    const { credential } = await req.json().catch(() => ({}));
    const g = await verifyGoogle(credential, env.GOOGLE_CLIENT_ID); if (!g) return json({ error: 'sign-in failed' }, 401);
    const email = g.email.toLowerCase();
    await env.UDB.prepare('INSERT INTO users (email, name, picture, google_sub, created) VALUES (?, ?, ?, ?, ?) ON CONFLICT(email) DO UPDATE SET name = excluded.name, picture = excluded.picture, google_sub = excluded.google_sub').bind(email, g.name || '', g.picture || '', g.sub, Date.now()).run();
    const u = await env.UDB.prepare('SELECT id FROM users WHERE email = ?').bind(email).first();
    const sid = hex(crypto.getRandomValues(new Uint8Array(32)));
    await env.UDB.prepare('INSERT INTO sessions (id, user_id, expires) VALUES (?, ?, ?)').bind(sid, u.id, Date.now() + 30 * 864e5).run();
    return json({ ok: true }, 200, { 'set-cookie': `sid=${sid}; Path=/; Max-Age=2592000; HttpOnly; Secure; SameSite=Lax` });
  }
  if (p === '/api/logout' && req.method === 'POST') {
    const sid = cookie(req, 'sid'); if (sid) await env.UDB.prepare('DELETE FROM sessions WHERE id = ?').bind(sid).run();
    return json({ ok: true }, 200, { 'set-cookie': 'sid=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax' });
  }
  const u = await currentUser(req, env);
  if (p === '/api/me') return json({ user: u ? { email: u.email, name: u.name, plan: u.plan } : null });
  if (!u) return json({ error: 'sign in first' }, 401);
  if (p === '/api/designs' && req.method === 'GET') return json({ designs: (await env.UDB.prepare('SELECT id, tool, title, updated FROM designs WHERE user_id = ? ORDER BY updated DESC LIMIT 200').bind(u.id).all()).results });
  if (p === '/api/designs' && req.method === 'POST') {
    const b = await req.json().catch(() => null); if (!b || !b.tool || !b.state) return json({ error: 'bad request' }, 400);
    const st = JSON.stringify(b.state); if (st.length > 20000) return json({ error: 'too large' }, 413);
    const cnt = (await env.UDB.prepare('SELECT COUNT(*) n FROM designs WHERE user_id = ?').bind(u.id).first()).n;
    if (!b.id && cnt >= (u.plan === 'member' ? 500 : 5)) return json({ error: 'limit', limit: u.plan === 'member' ? 500 : 5 }, 403);
    if (b.id) { await env.UDB.prepare('UPDATE designs SET state = ?, title = ?, tool = ?, updated = ? WHERE id = ? AND user_id = ?').bind(st, String(b.title || '').slice(0, 80), b.tool, Date.now(), b.id, u.id).run(); return json({ id: b.id }); }
    const r = await env.UDB.prepare('INSERT INTO designs (user_id, tool, title, state, updated) VALUES (?, ?, ?, ?, ?)').bind(u.id, b.tool, String(b.title || '').slice(0, 80), st, Date.now()).run();
    return json({ id: r.meta.last_row_id });
  }
  let m;
  if ((m = p.match(/^\/api\/designs\/(\d+)$/))) {
    if (req.method === 'DELETE') { await env.UDB.prepare('DELETE FROM designs WHERE id = ? AND user_id = ?').bind(+m[1], u.id).run(); return json({ ok: true }); }
    const d = await env.UDB.prepare('SELECT id, tool, title, state FROM designs WHERE id = ? AND user_id = ?').bind(+m[1], u.id).first();
    return d ? json({ ...d, state: JSON.parse(d.state) }) : json({ error: 'not found' }, 404);
  }
  return json({ error: 'not found' }, 404);
}
