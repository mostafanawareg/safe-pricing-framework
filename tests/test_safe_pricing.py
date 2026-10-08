"""Unit tests — run with:  python -m unittest discover -s tests"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from safe_pricing import (  # noqa: E402
    anchor_price,
    safe_price,
    calculate_safe_price,
    calculate_break_even,
)


class TestAnchor(unittest.TestCase):
    def test_even_integer_kept(self):
        self.assertEqual(anchor_price(1250000), 1250000)

    def test_odd_integer_raised_to_even(self):
        self.assertEqual(anchor_price(999), 1000)

    def test_decimal_rounded_up_to_even(self):
        self.assertEqual(anchor_price(998.2), 1000)
        self.assertEqual(anchor_price(997.5), 998)


class TestSafePrice(unittest.TestCase):
    def test_ninety_percent_odd(self):
        self.assertEqual(safe_price(1000), 899)   # 900 -> even -> 899
        self.assertEqual(safe_price(650), 585)    # 585 is already odd

    def test_minimum_one(self):
        self.assertEqual(safe_price(1), 1)

    def test_always_odd(self):
        for m in range(2, 5000, 7):
            self.assertEqual(safe_price(m) % 2, 1)


class TestFullCalculation(unittest.TestCase):
    def test_example(self):
        r = calculate_safe_price(1250000, 980000, 700000, "EV sedan")
        self.assertEqual(r.anchor, 1250000)
        self.assertEqual(r.safe_price, 881999)
        self.assertEqual(r.customer_saving, 368001)
        self.assertEqual(r.discount_pct, 29)
        self.assertEqual(r.safe_zone, (881999, 980000))

    def test_validation(self):
        with self.assertRaises(ValueError):
            calculate_safe_price(0, 100, 50, "x")
        with self.assertRaises(ValueError):
            calculate_safe_price(100, 90, 50, "  ")


class TestBreakEven(unittest.TestCase):
    def test_example(self):
        b = calculate_break_even(585, 50000, 120)
        self.assertEqual(b.units, 108)            # ceil(50000 / 465)
        self.assertEqual(b.contribution_margin, 465)
        self.assertEqual(b.contribution_pct, 79.5)
        self.assertEqual(b.revenue, 108 * 585)

    def test_negative_contribution(self):
        with self.assertRaises(ValueError):
            calculate_break_even(100, 1000, 100)


if __name__ == "__main__":
    unittest.main()
