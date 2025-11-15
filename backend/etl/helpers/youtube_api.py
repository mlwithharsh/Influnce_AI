import requests


def fetch_youtube_stats(channel_id, api_key):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "channelId": channel_id,
        "maxResults": 50,
        "part": "snippet",
        "order": "date",
        "key": api_key
    }
    return requests.get(url, params=params).json().get("items", [])
