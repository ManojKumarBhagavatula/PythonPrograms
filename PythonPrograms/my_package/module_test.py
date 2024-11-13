import unittest

from module1 import greet_user, square_number
class TestModule(unittest.TestCase):
    def test_greet_user(self):
        self.assertEqual(greet_user("Alice"), "Hello, Alice! Welcome!")
        self.assertEqual(greet_user("Bob"), "Hello, Bob! Welcome!")
        self.assertEqual(greet_user(""), "Hello, ! Welcome!")  # Testing for empty string
    
    def test_square_number(self):
        self.assertEqual(square_number(5), 25)
        self.assertEqual(square_number(0), 0)
        self.assertEqual(square_number(-2), 4)
        self.assertEqual(square_number(100), 10000)  # Testing for large numbers

if __name__ == "__main__":
    unittest.main()
