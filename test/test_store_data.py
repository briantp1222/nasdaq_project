import unittest
from sqlalchemy import create_engine
import pandas as pd
from src.data_processing import store_df_to_db, read_df_from_db, store_compressed_data_to_db, load_compressed_data_from_db

class TestDataProcessing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        cls.df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        cls.file_path = 'data.pkl.gz'
        cls.table_name = 'test_table'

    def test_store_and_read_df(self):
        store_df_to_db(self.df, self.engine, self.table_name)
        df_read = read_df_from_db(self.engine, self.table_name)
        pd.testing.assert_frame_equal(self.df, df_read)

    def test_store_and_load_compressed_data(self):
        self.df.to_pickle(self.file_path, compression='gzip')
        record_id = store_compressed_data_to_db(self.file_path, self.engine, 'compressed_data')
        df_loaded = load_compressed_data_from_db(self.engine, 'compressed_data', record_id)
        pd.testing.assert_frame_equal(self.df, df_loaded)

if __name__ == '__main__':
    unittest.main()
