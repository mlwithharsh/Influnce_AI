import requests
from fastapi import APIRouter , Request

@router.get('/instagram/insights')
def get_ig_insights(user_id: int):
    token = get_token_from_db(user_id, "instagram")
    url = f"https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,timestamp,like_count,comments_count&access_token={token}"
    res = requests.get(url)
    return {"posts": data.get("data", [])}

