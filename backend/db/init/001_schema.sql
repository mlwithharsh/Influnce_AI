CREATE TABLE IF NOT EXISTS raw_instagram_posts (
  post_id TEXT PRIMARY KEY,
  raw_json JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS raw_youtube_stats (
  video_id TEXT PRIMARY KEY,
  raw_json JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username TEXT,
  email TEXT
);

CREATE TABLE IF NOT EXISTS user_tokens (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  access_token TEXT NOT NULL,
  platform TEXT NOT NULL,
  expires_in INTEGER
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_user_tokens_user_platform ON user_tokens(user_id, platform);