from perfect import flow , task
from etl.helpers.instagram_api import fetch_instagram_post
from etl.helpers.db import insert_instagram_raw

@task
def extract(user_id: str ,  access_token: str):
    return fetch_instagram_post(user_id, access_token)

@task
def load(raw_data):
    return insert_instagram_raw(raw_data)

@flow (name="extract_instagram_analysis")
def extract_instagram_flow(user_id: str, tokens : str):
    data = extract(user_id, tokens)
    load(data)



if __name__ == "__main__":
    extract_instagram_flow()