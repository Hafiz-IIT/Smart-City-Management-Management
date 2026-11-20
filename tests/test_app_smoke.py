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

    def test_admin_incident_updates_require_a_key(self):
        from App.API.incidents import update_item
        from App.Core.Auth import require_admin

        route = next(
            route for route in app.routes
            if getattr(route, "path", None) == "/api/incidents/{incident_id}"
        )
        self.assertTrue(
            any(dependency.call == require_admin for dependency in route.dependant.dependencies)
        )

    def test_incident_classifier_does_not_default_unknown_text_to_garbage(self):
        from App.API.incidents import classify

        self.assertEqual(classify("garbage is overflowing near the market"), "garbage")
        self.assertIsNone(classify("hello, I have a general question"))


if __name__ == "__main__":
    unittest.main()
