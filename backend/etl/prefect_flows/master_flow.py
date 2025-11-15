from perfect import flow
from etl.prefect_flows.extract_instagram import extract_instagram_flow
from etl.prefect_flows.extract_youtube import extract_youtube_flow
from etl.prefect_flows.run_dbt import dbt_flow

@flow(name="Master Daily ETL")
def master_etl():
    extract_instagram_flow()
    extract_youtube_flow()
    dbt_flow()



if __name__ == "__main__":
    master_etl()