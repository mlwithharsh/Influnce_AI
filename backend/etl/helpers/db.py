import psycopg2
import json
import os

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

