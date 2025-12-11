from lib.ygo import Pyugioh
import unittest

class TestCardList(unittest.TestCase):

    def test_config_init(self):
        py = Pyugioh()
        with self.subTest():
            self.assertIsNotNone(py.config.api_path)
        with self.subTest():
            self.assertIsNotNone(py.config.deck_path)
        del py
        
if __name__=="__main__":
    unittest.main()