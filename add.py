import decimal
from decimal import Decimal
from typing import Union
from unittest import TestCase


def add(a: Union[str, int, Decimal], b: Union[str, int, Decimal]) -> Decimal:
    """
        Returns the sum of two numbers
    """
    return Decimal(a) + Decimal(b)


class TestAddFunction(TestCase):
    def test_add(self):
        assert add(2, 2) == Decimal("4.00")

    def test_add_positive_numbers(self):
        assert add(2, 3) == Decimal("5.00")

    def test_add_signed_numbers(self):
        assert add(2, -2) == Decimal("0.00")

    def test_add_stringified_numbers(self):
        assert add("2", "3") == Decimal("5.00")

    def test_add_stringified_negative_numbers(self):
        assert add("-2", "3") == Decimal("1.00")

    def test_add_stringified_and_non_stringified_numbers(self):
        assert add("-2", 3) == Decimal("1.00")

    def test_add_with_decimals(self):
        assert add("2.5", "7.5") == Decimal("10.00")

    def test_cannot_add_words(self):
        try:
            add('patata', '2')
        except decimal.InvalidOperation as e:
            assert e is not None
