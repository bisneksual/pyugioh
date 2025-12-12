from lib import ygo
import unittest

class TestCardList(unittest.TestCase):

    def test_config_init(self):
        pygo = ygo.Pyugioh()
        with self.subTest():
            self.assertIsNotNone(pygo.config.api_path)
        with self.subTest():
            self.assertIsNotNone(pygo.config.deck_path)
        del pygo
        
if __name__=="__main__":
    unittest.main()