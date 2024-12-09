# import requests
# import json
# from airflow import DAG
# from airflow.providers.http.hooks.http import HttpHook
# from airflow.providers.postgres.hooks.postgres import PostgresHook
# from airflow.decorators import task
# from airflow.utils.dates import days_ago

# API_CONN_ID = '4c9d87da-59d1-497f-8dfc-e0c6727ba06e'
# headers = {
#             'start':'1',
#             'limit':'5000',
#             'convert':'USD'
#         }
#         # headers = {
#         #     'Accepts': 'application/json',
#         #     'X-CMC_PRO_API_KEY': '4c9d87da-59d1-497f-8dfc-e0c6727ba06e',
#         # }

# http_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')
# endpoint=f'v1/cryptocurrency/listings/latest'

# ## Make the request via the HTTP Hook
# response=http_hook.run(endpoint, headers=headers)
# print(response)
# # if response.status_code == 200:
# #     return response.json()
# # else:
# #     raise ValueError(f'Failed to retrieve crypto data: {response.status_code}')

from datetime import date

print(date.today())