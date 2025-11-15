select
    (raw_json->>'id') as post_id,
    (raw_json->>'caption') as caption,
    (raw_json->>'comments_count')::int as comments,
    (raw_json->>'like_count')::int as likes,
    (raw_json->>'timestamp')::timestamp as posted_at
from raw_instagram_posts
