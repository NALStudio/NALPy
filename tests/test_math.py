import unittest

from nalpy import math


class BasicMathFunctions(unittest.TestCase):
    def test_cbrt(self):
        self.assertAlmostEqual(math.cbrt(64), 4)
        self.assertAlmostEqual(math.cbrt(27), 3)
        self.assertAlmostEqual(math.cbrt(8), 2)
        self.assertAlmostEqual(math.cbrt(-8), -2)
        self.assertAlmostEqual(math.cbrt(0), 0)
        self.assertAlmostEqual(math.cbrt(1), 1)
        self.assertAlmostEqual(math.cbrt(-1), -1)

        self.assertAlmostEqual(math.cbrt(9), 2.08008382305190411453)
        self.assertAlmostEqual(math.cbrt(0.5), 0.79370052598409973738)
        self.assertAlmostEqual(math.cbrt(69), 4.10156592970234752185)
        self.assertAlmostEqual(math.cbrt(420), 7.48887238721850719787)

    def test_sign(self):
        self.assertEqual(math.sign(0), 0)
        self.assertEqual(math.sign(1), 1)
        self.assertEqual(math.sign(-1), -1)

        self.assertEqual(math.sign(69), 1)
        self.assertEqual(math.sign(69.420), 1)
        self.assertEqual(math.sign(420.69), 1)

        self.assertEqual(math.sign(-69), -1)
        self.assertEqual(math.sign(-69.420), -1)
        self.assertEqual(math.sign(-420.69), -1)

    def test_is_positive_inf(self):
        self.assertEqual(math.is_positive_inf(float("inf")), True)
        self.assertEqual(math.is_positive_inf(float("-inf")), False)
        self.assertEqual(math.is_positive_inf(float("nan")), False)
        self.assertEqual(math.is_positive_inf(69), False)
        self.assertEqual(math.is_positive_inf(420), False)
        self.assertEqual(math.is_positive_inf(-420), False)
        self.assertEqual(math.is_positive_inf(-69), False)

    def test_is_negative_inf(self):
        self.assertEqual(math.is_negative_inf(float("inf")), False)
        self.assertEqual(math.is_negative_inf(float("-inf")), True)
        self.assertEqual(math.is_negative_inf(float("nan")), False)
        self.assertEqual(math.is_negative_inf(69), False)
        self.assertEqual(math.is_negative_inf(420), False)
        self.assertEqual(math.is_negative_inf(-420), False)
        self.assertEqual(math.is_negative_inf(-69), False)

    def test_delta_angle(self):
        self.assertAlmostEqual(math.delta_angle(69420, 42069), 9)
        self.assertAlmostEqual(math.delta_angle(42069, 69420), -9)
        self.assertAlmostEqual(math.delta_angle(-69420, -42069), -9)
        self.assertAlmostEqual(math.delta_angle(-42069, -69420), 9)
        self.assertAlmostEqual(math.delta_angle(-69420, 42069), -111)
        self.assertAlmostEqual(math.delta_angle(-42069, 69420), -111)

        self.assertAlmostEqual(math.delta_angle(360, 180), 180)
        self.assertAlmostEqual(math.delta_angle(180, 360), 180)

        self.assertAlmostEqual(math.delta_angle(53, 225), 172)
        self.assertAlmostEqual(math.delta_angle(225, 53), -172)

        self.assertAlmostEqual(math.delta_angle(33, 99), 66)
        self.assertAlmostEqual(math.delta_angle(444, 99), 15)

        self.assertAlmostEqual(math.delta_angle(0, 0), 0)
        self.assertAlmostEqual(math.delta_angle(1324, 1324), 0)
        self.assertAlmostEqual(math.delta_angle(-1324, -1324), 0)

        self.assertNotAlmostEqual(math.delta_angle(69, 69), 420)
        self.assertNotAlmostEqual(math.delta_angle(333, 122), 333)
        self.assertNotAlmostEqual(math.delta_angle(122, 122), 122)


class ValueManipulation(unittest.TestCase):
    def test_clamp(self):
        self.assertEqual(math.clamp(0, 0, 1), 0)
        self.assertEqual(math.clamp(-1, 0, 1), 0)
        self.assertEqual(math.clamp(-69, 0, 1), 0)
        self.assertEqual(math.clamp(1, 0, 1), 1)
        self.assertEqual(math.clamp(69, 0, 1), 1)

        self.assertEqual(math.clamp(0.5, 0, 1), 0.5)
        self.assertEqual(math.clamp(-1.22, 0, 1), 0)
        self.assertEqual(math.clamp(3.14159, 0, 1), 1)
        self.assertEqual(math.clamp(0.5555934, 0, 1), 0.5555934)
        self.assertEqual(math.clamp(0.12111, 0, 1), 0.12111)

        self.assertEqual(math.clamp(100000, 42069, 69420), 69420)
        self.assertEqual(math.clamp(100000, 42069, 1000000), 100000)
        self.assertEqual(math.clamp(10000, 4206900, 1000000), 4206900)

    def test_clamp01(self):
        self.assertEqual(math.clamp(0, 0, 1), math.clamp01(0))
        self.assertEqual(math.clamp(-1, 0, 1), math.clamp01(-1))
        self.assertEqual(math.clamp(-69, 0, 1), math.clamp01(-69))
        self.assertEqual(math.clamp(1, 0, 1), math.clamp01(1))
        self.assertEqual(math.clamp(69, 0, 1), math.clamp01(69))
        self.assertEqual(math.clamp(0.5, 0, 1), math.clamp01(0.5))
        self.assertEqual(math.clamp(-1.22, 0, 1), math.clamp01(-1.22))
        self.assertEqual(math.clamp(3.14159, 0, 1), math.clamp01(3.14159))
        self.assertEqual(math.clamp(0.5555934, 0, 1), math.clamp01(0.5555934))
        self.assertEqual(math.clamp(0.12111, 0, 1), math.clamp01(0.12111))

    def test_remap(self):
        self.assertAlmostEqual(math.remap(0.5, 0, 1, 1, 0), 0.5)
        self.assertAlmostEqual(math.remap(0.75, 0, 1, 1, 0), 0.25)

        self.assertAlmostEqual(math.remap(0.5, 0, 1, 0, 2), 1)
        self.assertAlmostEqual(math.remap(0.5, 0, 1, 0, 4), 2)

        self.assertAlmostEqual(math.remap(4, 0, 2, 0, 1), 2)
        self.assertAlmostEqual(math.remap(4, 0, 4, 0, 1), 1)
        self.assertAlmostEqual(math.remap(-4, 0, 4, 0, 1), -1)
        self.assertAlmostEqual(math.remap(-16, 0, 4, 0, 1), -4)
        self.assertAlmostEqual(math.remap(0.25, 0, 4, 0, 1), 0.0625)

    def test_remap01(self):
        self.assertAlmostEqual(math.remap(4, 0, 2, 0, 1), math.remap01(4, 0, 2))
        self.assertAlmostEqual(math.remap(4, 0, 4, 0, 1), math.remap01(4, 0, 4))
        self.assertAlmostEqual(math.remap(-4, 0, 4, 0, 1), math.remap01(-4, 0, 4))
        self.assertAlmostEqual(math.remap(-16, 0, 4, 0, 1), math.remap01(-16, 0, 4))
        self.assertAlmostEqual(math.remap(0.25, 0, 4, 0, 1), math.remap01(0.25, 0, 4))


class Rounding(unittest.TestCase):
    def test_round_away_from_zero(self):
        self.assertAlmostEqual(math.round_away_from_zero(0.5), 1)
        self.assertAlmostEqual(math.round_away_from_zero(1), 1)
        self.assertAlmostEqual(math.round_away_from_zero(5), 5)
        self.assertAlmostEqual(math.round_away_from_zero(15), 15)
        self.assertAlmostEqual(math.round_away_from_zero(15.1), 15)
        self.assertAlmostEqual(math.round_away_from_zero(15.25), 15)
        self.assertAlmostEqual(math.round_away_from_zero(15.5), 16)
        self.assertAlmostEqual(math.round_away_from_zero(15.51), 16)
        self.assertAlmostEqual(math.round_away_from_zero(15.75), 16)
        self.assertAlmostEqual(math.round_away_from_zero(69.420), 69)

        self.assertAlmostEqual(math.round_away_from_zero(-0.5), -1)
        self.assertAlmostEqual(math.round_away_from_zero(-1), -1)
        self.assertAlmostEqual(math.round_away_from_zero(-5), -5)
        self.assertAlmostEqual(math.round_away_from_zero(-15), -15)
        self.assertAlmostEqual(math.round_away_from_zero(-15.1), -15)
        self.assertAlmostEqual(math.round_away_from_zero(-15.25), -15)
        self.assertAlmostEqual(math.round_away_from_zero(-15.5), -16)
        self.assertAlmostEqual(math.round_away_from_zero(-15.51), -16)
        self.assertAlmostEqual(math.round_away_from_zero(-15.75), -16)
        self.assertAlmostEqual(math.round_away_from_zero(-69.420), -69)


if __name__ == '__main__':
    unittest.main()
