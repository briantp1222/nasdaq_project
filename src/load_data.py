def download_data(source, ticker=None, **filters):
    """
    Download data from Nasdaq Data Link.
    
    Parameters:
    source (str): The data source or table name.
    ticker (str): The stock ticker symbol for the 'get' method (optional).
    **filters: Additional filters for the 'get_table' method.
    
    Returns:
    tuple: The source and the downloaded data as a DataFrame.
    """
    nas.ApiConfig.api_key = NASDAQ_API
    data = None
    
    try:
        #try to fetch data using get_table if ticker is not provided
        if ticker is None:
            data = nas.get_table(source, **filters)
        else:
            # Try to fetch data using get if ticker is provided
            data = nas.get(f'{source}/{ticker}')
    except Exception as e:
        print(f"Error downloading data from {source} with : {str(e)}")
        return None

    if data is not None:
        print(f"Data downloaded successfully from {source}")
    else:
        print(f"Failed to download data from {source}")

    return data
    
def update_data(engine, table_name, source, ticker=None, **filters):

    new_data = download_data(source, ticker, **filters)
    if new_data is not None:
        new_data.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        print(f"Data has been updated in the {table_name} table.")
    else:
        print(f"Failed to update data in the {table_name} table.")
        
def retrieve_data(engine, table_name):

    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, con=engine)
    return df
