CREATE TABLE IF NOT EXISTS artworks (
  id TEXT PRIMARY KEY, slug TEXT UNIQUE NOT NULL, title TEXT NOT NULL, title_ko TEXT, artist TEXT, artist_ko TEXT, artist_slug TEXT,
  date TEXT, medium TEXT, credit TEXT, kind TEXT, theme TEXT, w INTEGER, h INTEGER, palette TEXT, added_at INTEGER DEFAULT (unixepoch())
);
CREATE INDEX IF NOT EXISTS idx_art_theme ON artworks(theme);
CREATE INDEX IF NOT EXISTS idx_art_artist ON artworks(artist_slug);
