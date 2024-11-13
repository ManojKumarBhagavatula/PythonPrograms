import unittest
from math import add, subtract

class TestMain(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(5, 3), 8)
    
    def test_subtract(self):
        self.assertEqual(subtract(6, 4), 3)