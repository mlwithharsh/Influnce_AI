from perfect import flow , task
from etl.helpers.youtube_api import fetch_youtube_stats
from etl.helpers.db import inset_youtube_raw

@task
def extract(channel_id: str, api_key: str):
    data = fetch_youtube_stats(channel_id, api_key)

@task
def load(raw_data : dict):
    return inset_youtube_raw(raw_data)

@flow(name="Extract YouTube Analytics")
def extract_youtube_flow(channel_id: str, key: str):
    data = extract(channel_id, key)
    load(data)