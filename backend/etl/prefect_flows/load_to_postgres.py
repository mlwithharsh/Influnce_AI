from perfect import task
from etl.helpers.db import execute_insert

@task
def load_generic(table:str , payload:dict):
    execute_insert(table, payload)