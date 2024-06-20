import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, LargeBinary
import gzip
import pickle
from io import BytesIO

def store_df_to_db(df, engine, table_name):
    """
    Store DataFrame to the database.
    """
    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    print(f"DataFrame has been stored in the {table_name} table.")

def read_df_from_db(engine, table_name):
    return pd.read_sql_table(table_name, con=engine)#or use retrieve_data(engine, table_name)

#Compress and save the DataFrame to a specified file.
def compress_and_save_df(df, save_path='.', file_name='compressed_data.pkl.gz'):
    """
    Parameters:
    df (DataFrame): The DataFrame to compress and save.
    save_path (str): The directory path to save the file. Default is current directory.
    file_name (str): The name of the file. Default is 'compressed_data.pkl.gz'.
    
    Returns:
    bytes: The compressed data.
    """
    os.makedirs(save_path, exist_ok=True)
    file_path = os.path.join(save_path, file_name)
    
    with gzip.open(file_path, 'wb') as f:
        pickle.dump(df, f)
    
    print(f"DataFrame has been compressed and saved to {file_path}.")
    return file_path
    
    

def store_compressed_data_to_db(file_path, engine, table_name):

    with engine.connect() as conn:
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                data MEDIUMBLOB
            );
        """))#Make sure database columns are large enough to store compressed data

    metadata = sa.MetaData()
    compressed_table = sa.Table(table_name, metadata, autoload_with=engine)

    with open(file_path, 'rb') as f:
        compressed_data = f.read()
    print(f"Compressed data read from file: {len(compressed_data)} bytes")
    print(compressed_data)
    with engine.connect() as conn:
        insert_stmt = compressed_table.insert().values(data=compressed_data)
        result = conn.execute(insert_stmt)
        conn.commit()#used to commit the current transaction, ensuring that all changes to the database are persisted.
        record_id = result.inserted_primary_key[0]
    
    print(f"Compressed data has been stored in the {table_name} table with record ID {record_id}.")
    print(result)
    return record_id


def load_compressed_data_from_db(engine, table_name, record_id):
    """
    Load and decompress data from the database.
    
    Parameters:
    table_name (str): The name of the table where the compressed data is stored.
    record_id (int): The ID of the record to load.
    
    Returns:
    DataFrame: The decompressed DataFrame.
    """
        
    metadata = sa.MetaData()
    compressed_table = sa.Table(table_name, metadata, autoload_with=engine)
    
    with engine.connect() as conn:
        #Perform a raw SQL query
        query = f"SELECT data FROM {table_name} WHERE id = :record_id"
        result = conn.execute(sa.text(query), {"record_id": record_id}).fetchone()
        if result is None:
            raise ValueError(f"No record found with ID {record_id}")
        
        compressed_data = result[0]
        print(f"Compressed data length: {len(compressed_data)} bytes")  # Add debug print
    
    with gzip.open(BytesIO(compressed_data), 'rb') as f:
        df = pickle.load(f)
    
    return df
