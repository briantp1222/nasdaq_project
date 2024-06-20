import unittest
import pandas as pd
import numpy as np
from src.data_quality import check, clean

class TestDataQuality(unittest.TestCase):

    def setUp(self):
        # Set up a sample DataFrame for testing
        data = {
            'Date': pd.date_range(start='2020-01-01', periods=10, freq='D'),
            'Open': [100, 101, 102, 103, np.nan, 105, 106, 107, 108, 109],
            'Close': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
            'Daily_Return': [0.01, 0.01, -0.02, 0.03, np.nan, 0.02, 0.01, -0.03, 0.04, 0.05]
        }
        self.df = pd.DataFrame(data)

    def test_check_missing_values(self):
        missing_vals, _, _, _ = check(self.df)
        self.assertEqual(missing_vals['Open'], 1)
        self.assertEqual(missing_vals['Daily_Return'], 1)

    def test_check_outliers(self):
        _, outliers, _, _ = check(self.df)
        self.assertEqual(len(outliers), 1)

    def test_check_extreme_price_change(self):
        _, _, extreme_change, _ = check(self.df)
        self.assertEqual(len(extreme_change), 0)

    def test_check_duplicates(self):
        _, _, _, duplicates = check(self.df)
        self.assertEqual(duplicates, 0)

    def test_clean_missing_values(self):
        cleaned_df = clean(self.df)
        self.assertFalse(cleaned_df.isnull().values.any())

    def test_clean_duplicates(self):
        df_with_duplicates = self.df.append(self.df.iloc[0])
        cleaned_df = clean(df_with_duplicates)
        self.assertEqual(len(cleaned_df), len(self.df))

if __name__ == '__main__':
    unittest.main()
