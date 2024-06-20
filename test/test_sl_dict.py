import unittest
from src.sl_dict import load

class TestSLDict(unittest.TestCase):

    def test_load(self):
        data = load('data/info_dict.pkl')
        self.assertIsInstance(data, dict)

if __name__ == '__main__':
    unittest.main()
