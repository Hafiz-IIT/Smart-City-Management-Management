import unittest

from demo_data import fake_incidents


class SmartCitySmokeTests(unittest.TestCase):
    def test_demo_incident_generation(self):
        incidents = fake_incidents(3)
        self.assertEqual(len(incidents), 3)
        self.assertTrue(all(item.type for item in incidents))
        self.assertTrue(all(item.ward for item in incidents))


if __name__ == "__main__":
    unittest.main()
