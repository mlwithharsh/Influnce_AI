import requests

def fetch_instagram_posts(user_id, token):
    url = f"https://graph.facebook.com/v17.0/{user_id}/media"
    params = {
        "fields": "id,caption,media_type,like_count,comments_count,timestamp",
        "access_token": token
    }
    return requests.get(url, params=params).json().get("data", [])