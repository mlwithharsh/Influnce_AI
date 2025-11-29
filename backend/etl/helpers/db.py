import psycopg2
import json
import os
import pathlib

def _load_env():
    root_env = pathlib.Path(__file__).resolve().parents[3] / ".env"
    backend_env = pathlib.Path(__file__).resolve().parents[2] / ".env"
    for p in (root_env, backend_env):
        if p.exists():
            for line in p.read_text().splitlines():
                s = line.strip()
                if not s or s.startswith("#") or "=" not in s:
                    continue
                k, v = s.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

_load_env()

def conn():
    return psycopg2.connect(
        host = os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        port = os.getenv("DB_PORT"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASS")
    )

def insert_instagram_raw(posts):
    c = conn()
    cur = c.cursor()

    for p in posts :
        cur.execute("""
        INSERT INTO raw_instagram_posts (post_id, raw_json)
        VALUES (%s, %s)
        ON CONFLICT(post_id) DO NOTHING;
        """, (p["id"], json.dumps(p))
        )

    c.commit()
    c.close()


def insert_youtube_raw(rows):
    c = conn()
    cur = c.cursor()
    for r in rows :
        cur.execute("""
        INSERT INTO raw_youtube_stats (video_id, raw_json)
                VALUES (%s, %s)
                ON CONFLICT(video_id) DO NOTHING;
                """, (r["id"], json.dumps(r)))

    c.commit()
    c.close()

