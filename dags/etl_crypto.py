from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from airflow.utils.dates import days_ago
import requests
import json
from datetime import date
import pandas as pd

target_domain = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
# 'X-CMC_PRO_API_KEY' = '4c9d87da-59d1-497f-8dfc-e0c6727ba06e'

POSTGRES_CONN_ID = 'postgres_default'
API_CONN_ID = 'crypto_api'

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

# DAG
with DAG(dag_id = 'crypto_etl_pipeline',
         default_args = default_args,
         schedule_interval = '@daily',
         catchup = False) as dags:

    @task()
    def extract_crypto_data():
        """
        This task retrieves crypto data from the Open Meteo API.
        """

        # headers = {
        #     'start':'1',
        #     'limit':'5000',
        #     'convert':'USD'
        # }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '4c9d87da-59d1-497f-8dfc-e0c6727ba06e',
        }

        http_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')
        endpoint=f'v1/cryptocurrency/listings/latest'

        ## Make the request via the HTTP Hook
        response=http_hook.run(endpoint, headers=headers)
        # print(response)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f'Failed to retrieve crypto data: {response.status_code}')


    

    @task()
    def transform_crypto_data(crypto_data):
        """
        This task transforms the retrieved crypto data.
        """
        transformed_data = []
        current_data = crypto_data['data']
        for i in range(50):
            temp = []
            temp.append(date.today())
            temp.append(current_data[i]['name'])
            temp.append(current_data[i]['symbol'])
            temp.append(current_data[i]['cmc_rank'])
            temp.append(current_data[i]['quote']['USD']['price'])
            temp.append(current_data[i]['quote']['USD']['market_cap'])
            temp.append(current_data[i]['quote']['USD']['volume_24h'])
            temp.append(current_data[i]['quote']['USD']['percent_change_24h'])
            transformed_data.append(temp)
        
        # df = pd.DataFrame(transformed_data)
        # df.to_excel('crypto.xlsx', index=False)

        return transformed_data


    @task()
    def load_crypto_data(transformed_data):
        """
        This task loads the transformed crypto data into a PostgreSQL database.
        """
        postgres_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = postgres_hook.get_conn()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS crypto_data (
            Date DATE,
            Cryptocurrency_Name VARCHAR(255),
            Symbol VARCHAR(255),
            CMC_Rank INTEGER,
            Current_Price_USD FLOAT,
            Market_Capital_USD FLOAT,
            _24_hour_Trading_Volume FLOAT,
            Price_Change_24_hour_percentage FLOAT,
            PRIMARY KEY (Date, CMC_Rank)
            );
            """)

        sql = "INSERT INTO crypto_data (Date, Cryptocurrency_Name, Symbol, CMC_Rank, Current_Price_USD, Market_Capital_USD, \
                    _24_hour_Trading_Volume, Price_Change_24_hour_percentage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        for data in transformed_data:  
            cursor.execute(sql, data)

        conn.commit()
        cursor.close()
        conn.close()


    # @task()
    # def load_data_to_excel(df, file_path, sheet_name='Sheet1'):
    #     with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
    #         df.to_excel(writer, index=False, sheet_name=sheet_name)



    crypto_data = extract_crypto_data()
    transformed_data = transform_crypto_data(crypto_data)
    load_crypto_data(transformed_data)
    # load_data_to_excel(transformed_data)



#     You may sort against any of the following:
# market_cap: CoinMarketCap's market cap rank as outlined in our methodology.
# market_cap_strict: A strict market cap sort (latest trade price x circulating supply).
# name: The cryptocurrency name.
# symbol: The cryptocurrency symbol.
# date_added: Date cryptocurrency was added to the system.
# price: latest average trade price across markets.
# circulating_supply: approximate number of coins currently in circulation.
# total_supply: approximate total amount of coins in existence right now (minus any coins that have been verifiably burned).
# max_supply: our best approximation of the maximum amount of coins that will ever exist in the lifetime of the currency.
# num_market_pairs: number of market pairs across all exchanges trading each currency.
# market_cap_by_total_supply_strict: market cap by total supply.
# volume_24h: rolling 24 hour adjusted trading volume.
# volume_7d: rolling 24 hour adjusted trading volume.
# volume_30d: rolling 24 hour adjusted trading volume.
# percent_change_1h: 1 hour trading price percentage change for each currency.
# percent_change_24h: 24 hour trading price percentage change for each currency.
# percent_change_7d: 7 day trading price percentage change for each currency.