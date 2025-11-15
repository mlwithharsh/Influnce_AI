from perfect import task , flow
import os
import subprocess

@task
def run_dbt():
    return subprocess.run(
        ["dbt" , "run"],
        cwd = os.path.join(os.getcwd(), "etl/dbt_project"),
    )
@flow(name = "Run DBT Transformation")
def dbt_flow():
    run_dbt()

if __name__ == "__main__":
    dbt_flow()
