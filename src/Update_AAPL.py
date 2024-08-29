import pandas as pd
from sqlalchemy import create_engine, inspect
from prefect import task, flow
from prefect.task_runners import SequentialTaskRunner
import nasdaqdatalink as nas


NASDAQ_API = 'UCizQTvgM6noERXudhrx'
DATABASE_URL = 'mysql+mysqlconnector://root:NIdeshengri200!@localhost/nasdaq_data'

nas.ApiConfig.api_key = NASDAQ_API

def get_existing_data(table_name):
    engine = create_engine(DATABASE_URL)
    query = f"SELECT * FROM {table_name}"
    existing_data = pd.read_sql(query, engine)
    return existing_data

def find_new_rows(existing_data, new_data):
    if new_data is None:
        return None
    if existing_data is None:
        return new_data
    new_rows = new_data[~new_data.apply(tuple, 1).isin(existing_data.apply(tuple, 1))]
    return new_rows

def create_table_if_not_exists(table_name, data_sample):
    engine = create_engine(DATABASE_URL)
    inspector = inspect(engine)
    if not inspector.has_table(table_name):
        if data_sample is not None and not data_sample.empty:
            data_sample.head(0).to_sql(table_name, engine, if_exists='replace', index=False)
            print(f"Table {table_name} created in the database.")
        else:
            print(f"Data sample is empty or None, table {table_name} not created.")
    else:
        print(f"Table {table_name} already exists in the database.")

def insert_new_rows(table_name, new_rows):
    engine = create_engine(DATABASE_URL)
    if new_rows is None or new_rows.empty:
        return
    new_rows.to_sql(table_name, engine, if_exists='append', index=False)

def download_data(source, ticker=None, **filters):

    nas.ApiConfig.api_key = NASDAQ_API
    data = None
    
    try:
        # Try to fetch data using get_table if ticker is not provided
        if ticker is None:
            data = nas.get_table(source, **filters)
        else:
            # Try to fetch data using get if ticker is provided
            data = nas.get(f'{source}/{ticker}')
    except Exception as e:
        print(f"Error downloading data from {source} with ticker {ticker}: {str(e)}")
        # Fallback to using get method without filters
        try:
            data = nas.get(f'{source}/{ticker}')
        except Exception as e:
            print(f"Fallback error downloading data from {source} with ticker {ticker}: {str(e)}")
            return source, None

    if data is not None:
        print(f"Data downloaded successfully from {source} with ticker {ticker}")
    else:
        print(f"Failed to download data from {source} with ticker {ticker}")

    return source, data

@task(retries=2)
def update_data(source, ticker):
    source, data = download_data(source, ticker)
    table_name = f'{source}_{ticker}'.replace('/', '_').lower()
    create_table_if_not_exists(table_name, data)
    existing_data = get_existing_data(table_name)
    new_rows = find_new_rows(existing_data, data)
    insert_new_rows(table_name, new_rows)

@flow(name="Update AAPL Market Data", task_runner=SequentialTaskRunner())
def update_aapl_data_flow():
    source = 'WIKI'
    ticker = 'AAPL'
    update_data(source, ticker)

if __name__ == "__main__":
    update_aapl_data_flow()