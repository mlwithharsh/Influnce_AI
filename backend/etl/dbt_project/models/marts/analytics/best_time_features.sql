select
    post_id,
    extract(hour from posted_at) as hour,
    extract(dow from posted_at) as weekday,
    (likes + comments) as engagement
from {{ ref('stg_instagram_posts') }}
