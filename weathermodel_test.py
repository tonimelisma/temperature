import unittest

class TestModel(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(1, 1, "should be true")

if __name__ == '__main__':
    unittest.main()