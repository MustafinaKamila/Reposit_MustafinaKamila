"""Юнит-тесты для проверки валидации и расчётов варианта 14."""

import unittest
from unittest.mock import patch

import logger
from operations import cutting_speed, depth_class, feed_per_minute, material_removal_rate
from validation import input_chiszub, input_diameter, input_glubrez, input_number, input_podzub, validate_range


class TestValidateRange(unittest.TestCase):
    """Проверяет границы допустимых диапазонов."""

    def setUp(self) -> None:
        logger.clear()

    def test_inside(self):
        self.assertEqual(validate_range(5, 1, 10), (True, ""))

    def test_lower_boundary(self):
        self.assertEqual(validate_range(1, 1, 10), (True, ""))

    def test_upper_boundary(self):
        self.assertEqual(validate_range(10, 1, 10), (True, ""))

    def test_below(self):
        self.assertFalse(validate_range(0, 1, 10)[0])

    def test_above(self):
        self.assertFalse(validate_range(11, 1, 10)[0])


class TestInputFunctions(unittest.TestCase):
    """Проверяет циклический ввод параметров."""

    def setUp(self) -> None:
        logger.clear()

    @patch("validation.input", side_effect=["abc", "4", "50"])
    def test_input_diameter(self, _mock):
        self.assertEqual(input_diameter(), 50.0)

    @patch("validation.input", side_effect=["0", "21", "5"])
    def test_input_chiszub(self, _mock):
        self.assertEqual(input_chiszub(), 5.0)

    @patch("validation.input", side_effect=["0", "0.6", "0.1"])
    def test_input_podzub(self, _mock):
        self.assertEqual(input_podzub(), 0.1)

    @patch("validation.input", side_effect=["0", "11", "2"])
    def test_input_glubrez(self, _mock):
        self.assertEqual(input_glubrez(), 2.0)

    @patch("validation.input", side_effect=["bad", "5"])
    def test_input_number(self, _mock):
        self.assertEqual(input_number("число: ", 1, 10), 5.0)

    @patch("validation.input", side_effect=["5"])
    def test_input_diameter_boundary(self, _mock):
        self.assertEqual(input_diameter(), 5.0)

    @patch("validation.input", side_effect=["200"])
    def test_input_diameter_upper_boundary(self, _mock):
        self.assertEqual(input_diameter(), 200.0)


class TestOperations(unittest.TestCase):
    """Проверяет формулы скорости, подачи и производительности."""

    def test_cutting_speed(self):
        self.assertAlmostEqual(cutting_speed(80, 100), 254.6479, places=3)

    def test_feed_per_minute(self):
        self.assertAlmostEqual(feed_per_minute(0.1, 4, 500), 200.0)

    def test_material_removal_rate(self):
        self.assertAlmostEqual(material_removal_rate(2, 50, 200), 10.0)

    def test_depth_small(self):
        self.assertEqual(depth_class(0.5), "чистовая")

    def test_depth_boundary_lower(self):
        self.assertEqual(depth_class(1), "получистовая")

    def test_depth_middle(self):
        self.assertEqual(depth_class(2), "получистовая")

    def test_depth_boundary_upper(self):
        self.assertEqual(depth_class(3), "получистовая")

    def test_depth_large(self):
        self.assertEqual(depth_class(3.1), "черновая")


if __name__ == "__main__":
    unittest.main()
