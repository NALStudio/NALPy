import unittest

from nalpy import math


class BasicFunctionality(unittest.TestCase):
    def test_index(self):
        v = math.Vector2(3.5, 7.25)
        self.assertEqual(v[0], 3.5)
        self.assertEqual(v[1], 7.25)
        self.assertRaises(IndexError, lambda: v[3])

    def test_xy(self):
        v = math.Vector2(3.5, 7.25)
        self.assertEqual(v.x, 3.5)
        self.assertEqual(v.y, 7.25)
        self.assertRaises(AttributeError, lambda: v.z) # type: ignore

    def test_equals(self):
        v = math.Vector2(3.0, 3.0)
        self.assertEqual(v, math.Vector2(3.0, 3.0))
        self.assertNotEqual(v, math.Vector2(2.0, 3.0))
        self.assertNotEqual(v, math.Vector2(3.0, 2.0))
        self.assertNotEqual(v, math.Vector2(2.0, 2.0))

        # self.assertRaises(TypeError, lambda: v == (3.0, 3.0))

        self.assertEqual(math.Vector2(3, 3), math.Vector2(3.0, 3.0))
        self.assertEqual(math.Vector2(5, 2.5), math.Vector2(5.0, 2.5))
        self.assertNotEqual(math.Vector2(5, 2), math.Vector2(5.0, 2.5))

    def test_constants(self):
        self.assertEqual(math.Vector2.zero,  math.Vector2(0.0, 0.0))
        self.assertEqual(math.Vector2.one,   math.Vector2(1.0, 1.0))
        self.assertEqual(math.Vector2.up,    math.Vector2(0.0, 1.0))
        self.assertEqual(math.Vector2.down,  math.Vector2(0.0, -1.0))
        self.assertEqual(math.Vector2.left,  math.Vector2(-1.0, 0.0))
        self.assertEqual(math.Vector2.right, math.Vector2(1.0, 0.0))

    def test_repr(self):
        self.assertEqual(repr(math.Vector2(2.0, 2.0)), f"Vector2(2.0, 2.0)")
        self.assertEqual(repr(math.Vector2(2.4, 3.075)), f"Vector2(2.4, 3.075)")

        self.assertEqual(repr(math.Vector2(2.0, 2.0)), str(math.Vector2(2.0, 2.0)))
        self.assertEqual(repr(math.Vector2(2.4, 3.075)), str(math.Vector2(2.4, 3.075)))

    def test_addsub(self):
        b: math.Vector2 = math.Vector2.one
        self.assertEqual(b + math.Vector2(2.5, 2.5), math.Vector2(3.5, 3.5))
        self.assertEqual(b + math.Vector2(0.0, 1.75), math.Vector2(1.0, 2.75))

        self.assertEqual(b - math.Vector2(2.5, 2.5), math.Vector2(-1.5, -1.5))
        self.assertEqual(b - math.Vector2(0.0, 1.75), math.Vector2(1.0, -0.75))

    def test_mult(self):
        b: math.Vector2 = math.Vector2.one
        self.assertEqual(b * 2, math.Vector2(2.0, 2.0))
        self.assertEqual(2 * b, math.Vector2(2.0, 2.0))
        self.assertEqual(b * 2.0, math.Vector2(2.0, 2.0))
        self.assertEqual(2.0 * b, math.Vector2(2.0, 2.0))

        self.assertEqual(math.Vector2(3, 4) * b, math.Vector2(3.0, 4.0))
        self.assertEqual(b * math.Vector2(3, 4), math.Vector2(3.0, 4.0))
        self.assertEqual(math.Vector2(3.0, 4.0) * b, math.Vector2(3.0, 4.0))
        self.assertEqual(b * math.Vector2(3.0, 4.0), math.Vector2(3.0, 4.0))

    def test_divmod(self):
        self.assertEqual(math.Vector2(9, 9.0) / 3, math.Vector2(3.0, 3))
        self.assertEqual(math.Vector2(9, 9.0) / math.Vector2(3, 6), math.Vector2(3.0, 1.5))
        self.assertEqual(math.Vector2(10, 10.0) // 3, math.Vector2(3.0, 3))
        self.assertEqual(math.Vector2(10, 10.0) // math.Vector2(3, 6), math.Vector2(3.0, 1))

        self.assertEqual(math.Vector2(10, 10.0) % 3, math.Vector2(1.0, 1))
        self.assertEqual(math.Vector2(10, 10.0) % math.Vector2(3, 5), math.Vector2(1.0, 0))
        self.assertEqual(divmod(math.Vector2(10, 10.0), 3), (math.Vector2(3.0, 3), math.Vector2(1.0, 1)))
        self.assertEqual(divmod(math.Vector2(10, 10.0), math.Vector2(3, 5)), (math.Vector2(3.0, 2.0), math.Vector2(1.0, 0.0)))

    def test_rest_operators(self):
        self.assertEqual(-math.Vector2.one, math.Vector2(-1, -1))
        self.assertEqual(-math.Vector2.zero, math.Vector2.zero)
        self.assertEqual(-math.Vector2(-3, -3.0), math.Vector2(3.0, 3))

        self.assertEqual(abs(math.Vector2(-2, -2)), math.Vector2(2, 2))
        self.assertEqual(abs(math.Vector2(2, -2)), math.Vector2(2, 2))
        self.assertEqual(abs(math.Vector2(-2, 2)), math.Vector2(2, 2))
        self.assertEqual(abs(math.Vector2(2, 2)), math.Vector2(2, 2))

    def test_properties(self):
        self.assertEqual(math.Vector2(3, 6).magnitude, 6.70820393249936908923)
        self.assertEqual(math.Vector2(7, 12).magnitude, 13.89244398944980450843)
        self.assertEqual(math.Vector2(0.15, 0.75).magnitude, 0.7648529270389177245)

        unnormalized = math.Vector2(4.5, 3.42)
        self.assertEqual(unnormalized.magnitude, 5.65211464851872940138)
        normalized = unnormalized.normalized
        self.assertEqual(normalized.magnitude, 1.0)
        self.assertEqual(normalized.x, 0.79616219412310251879)
        self.assertEqual(normalized.y, 0.60508326753355791428)

    def test_math(self):
        a = math.Vector2(3.4, 7.6)
        a_perpendic = math.Vector2.perpendicular(a)

        b = math.Vector2(5.77, 3.22)

        self.assertEqual(math.Vector2.dot(a, b), 44.09)

        self.assertEqual(a_perpendic.x, -a.y)
        self.assertEqual(a_perpendic.y, a.x)
        self.assertEqual(math.Vector2.dot(a, a_perpendic), 0)

        self.assertAlmostEqual(math.Vector2.distance(a, b), 4.9800903606259997258)
        self.assertEqual(math.Vector2.distance(math.Vector2(3.0, 0.0), math.Vector2(0.0, 2.0)), 3.60555127546398929312)

    def test_angle(self):
        a = math.Vector2.right
        b1 = math.Vector2.up
        b2 = math.Vector2.down
        b3 = math.Vector2(1.0, -1.0)

        self.assertEqual(math.Vector2.angle(a, b1), 90)
        self.assertEqual(math.Vector2.angle(a, b2), 90)
        self.assertEqual(math.Vector2.signed_angle(a, b1), 90)
        self.assertEqual(math.Vector2.signed_angle(a, b2), -90)

        self.assertAlmostEqual(math.Vector2.angle(a, b3), 45)
        self.assertAlmostEqual(math.Vector2.signed_angle(a, b3), -45)

    def test_converters_and_constructors(self):
        a = math.Vector2(2.0, 5.0)
        b1 = math.Vector2(3.0, 4.0)
        b2 = math.Vector2(1.0, 7.0)
        b3 = math.Vector2(0.0, 0.0)
        b4 = math.Vector2(10, 10)

        self.assertEqual(math.Vector2.min(a, b1), math.Vector2(2.0, 4.0))
        self.assertEqual(math.Vector2.min(a, b2), math.Vector2(1.0, 5.0))
        self.assertEqual(math.Vector2.min(a, b3), math.Vector2(0.0, 0.0))
        self.assertEqual(math.Vector2.min(a, b4), math.Vector2(2.0, 5.0))

        self.assertEqual(math.Vector2.max(a, b1), math.Vector2(3.0, 5.0))
        self.assertEqual(math.Vector2.max(a, b2), math.Vector2(2.0, 7.0))
        self.assertEqual(math.Vector2.max(a, b3), math.Vector2(2.0, 5.0))
        self.assertEqual(math.Vector2.max(a, b4), math.Vector2(10.0, 10.0))

    def test_interpolation(self):
        a = math.Vector2(2, 4)
        b = math.Vector2(14.5, 7.85)

        lerp75 = math.Vector2.lerp(a, b, 0.75)
        lerpuncl75 = math.Vector2.lerp_unclamped(a, b, 0.75)
        res75 = math.Vector2(11.375, 6.8875)

        self.assertEqual(math.Vector2.lerp(a, b, 0.5), math.Vector2(8.25, 5.925))
        self.assertEqual(math.Vector2.lerp(a, b, 0.25), math.Vector2(5.125, 4.9625))
        self.assertAlmostEqual(lerp75.x, res75.x)
        self.assertAlmostEqual(lerp75.y, res75.y)
        self.assertEqual(math.Vector2.lerp(a, b, 0.0), a)
        self.assertEqual(math.Vector2.lerp(a, b, -10.0), a)
        self.assertEqual(math.Vector2.lerp(a, b, 1.0), b)
        self.assertEqual(math.Vector2.lerp(a, b, 10.0), b)

        self.assertEqual(math.Vector2.lerp_unclamped(a, b, 0.5), math.Vector2(8.25, 5.925))
        self.assertEqual(math.Vector2.lerp_unclamped(a, b, 0.25), math.Vector2(5.125, 4.9625))
        self.assertAlmostEqual(lerpuncl75.x, res75.x)
        self.assertAlmostEqual(lerpuncl75.y, res75.y)
        self.assertEqual(math.Vector2.lerp_unclamped(a, b, 0.0), a)
        self.assertEqual(math.Vector2.lerp_unclamped(a, b, -10.0), math.Vector2(-123, -34.5))
        self.assertEqual(math.Vector2.lerp_unclamped(a, b, 1.0), b)
        self.assertEqual(math.Vector2.lerp_unclamped(a, b, 10.0), math.Vector2(127, 42.5))

        # move_towards checks are generated.
        self.assertEqual(math.Vector2.move_towards(math.Vector2(29.431186908718228, 33.6621820548442), math.Vector2(23.120215968907857, 59.38576299316706), 66.61514209773944), math.Vector2(23.120215968907857, 59.38576299316706))
        self.assertEqual(math.Vector2.move_towards(math.Vector2(33.79504419784424, 15.245959830973579), math.Vector2(29.8970235981436, 56.87761092723505), 45.60931683390097), math.Vector2(29.8970235981436, 56.87761092723505))
        self.assertEqual(math.Vector2.move_towards(math.Vector2(36.967494011692054, 48.05636806402712), math.Vector2(64.7026491150305, 10.799301027132651), 22.62248852523597), math.Vector2(50.476173519781156, 29.90994789303563))
        self.assertEqual(math.Vector2.move_towards(math.Vector2(36.967494011692054, 48.05636806402712), math.Vector2(64.7026491150305, 10.799301027132651), 22.62248852523597), math.Vector2(50.476173519781156, 29.90994789303563))
        self.assertEqual(math.Vector2.move_towards(math.Vector2(17.304290257053363, 70.00883344211574), math.Vector2(25.30328000212717, 62.156384285746164), 73.68637824328094), math.Vector2(25.30328000212717, 62.156384285746164))
        self.assertEqual(math.Vector2.move_towards(math.Vector2(7.345439149536899, 27.733716913826783), math.Vector2(43.81449326240699, 53.65251153801417), 0.53), math.Vector2(7.7774480048922054, 28.04074842506724))

        # Max delta over the moveable distance
        self.assertEqual(math.Vector2.move_towards(math.Vector2(8.657950152375955, 4.180694783383892), math.Vector2(60.89320793752563, 64.02011771066626), 84948.51669138268), math.Vector2(60.89320793752563, 64.02011771066626))

if __name__ == '__main__':
    unittest.main()
