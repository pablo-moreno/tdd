import pytest
import decimal
from decimal import Decimal
from unittest import TestCase


def add(a, b):
    """
        Returns the sum of two numbers
    """
    return Decimal(a) + Decimal(b)


class TestAddFunction(TestCase):
    def test_add(self):
        assert add(2, 2) == 4

    def test_add_positive_numbers(self):
        assert add(2, 3) == 5

    def test_add_signed_numbers(self):
        assert add(2, -2) == 0

    def test_add_stringified_numbers(self):
        assert add("2", "3") == 5

    def test_add_stringified_negative_numbers(self):
        assert add("-2", "3") == 1

    def test_add_stringified_and_non_stringified_numbers(self):
        assert add("-2", 3) == 1

    def test_add_with_decimals(self):
        assert add("2.75", "7.5") == 10.25

    def test_cannot_add_words(self):
        with pytest.raises(decimal.InvalidOperation) as e:
            add('patata', '2')
            assert e is not None
