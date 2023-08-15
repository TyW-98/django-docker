"""
Sample test
"""
from django.test import SimpleTestCase

from app import calc


class AddTests(SimpleTestCase):
    """AddTests

    Test for calc module
    """
    def test_add_number(self):
        """test_add_number
        Test sum of number
        """
        result = calc.add(5, 6)
        self.assertEqual(result, 11)

    def test_minus_number(self):
        """test_minus_number

        Test minus of number
        """
        result = calc.minus(10, 4)
        self.assertEqual(result, 6)

    def test_multiple_number(self):
        """test_multiple_number

        Test Multiplication of number
        """
        result = calc.multiply(10, 4)

        self.assertEqual(result, 40)
