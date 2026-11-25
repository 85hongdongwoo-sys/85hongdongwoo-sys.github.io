-- Members database (binding UDB). Run once: npx wrangler d1 execute arttrip-users --remote --file=schema-users.sql
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE NOT NULL, name TEXT DEFAULT '', picture TEXT DEFAULT '', google_sub TEXT, plan TEXT DEFAULT 'free', created INTEGER);
CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, user_id INTEGER NOT NULL, expires INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS designs (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, tool TEXT NOT NULL, title TEXT DEFAULT '', state TEXT NOT NULL, updated INTEGER);
CREATE INDEX IF NOT EXISTS designs_user ON designs(user_id, updated);
