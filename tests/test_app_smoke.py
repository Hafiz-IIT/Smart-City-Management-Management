import unittest

from App.main import app


class ApplicationSmokeTests(unittest.TestCase):
    def test_application_and_routes_load(self):
        self.assertEqual(app.title, "Smart City Twin")
        paths = {route.path for route in app.routes}
        expected = {
            "/", "/incidents", "/admin",
            "/api/incidents", "/api/predict", "/api/stream",
        }
        self.assertTrue(expected.issubset(paths))


if __name__ == "__main__":
    unittest.main()
