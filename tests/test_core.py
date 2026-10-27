import unittest
from studio_core import modulo_walk, check_episode_plan


class CoreChecks(unittest.TestCase):
    def test_integer_identity_across_wraps_and_negative_steps(self):
        for modulus in range(2, 25):
            for start in (-25, -1, 0, 10, 25):
                for steps in (-24, -5, 0, 5, 24):
                    result = modulo_walk(start, steps, modulus)
                    self.assertEqual(result["final"]["total"], start + steps)
                    for item in result["positions"]:
                        self.assertEqual(item["total"], item["quotient"] * modulus + item["residue"])
                        self.assertTrue(0 <= item["residue"] < modulus)

    def test_demo_example(self):
        self.assertEqual(modulo_walk()["final"], {"index": 5, "total": 15, "quotient": 1, "residue": 3})

    def test_bounds_and_types(self):
        for args in ((0, 25, 12), (0, 1, 0), (True, 1, 12), (0, 1, 25)):
            with self.assertRaises(ValueError):
                modulo_walk(*args)

    def test_missing_fields_do_not_imply_verification(self):
        result = check_episode_plan({"question": "Why?"})
        self.assertFalse(result["required_fields_present"])
        self.assertFalse(result["scientific_claims_verified"])
        self.assertIn("sources", result["missing"])


if __name__ == "__main__":
    unittest.main()
