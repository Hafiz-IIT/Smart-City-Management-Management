import os
import unittest
from unittest.mock import patch
from fastapi import HTTPException
from pydantic import ValidationError
from App.API.auth import require_admin
from App.Core.Models import IncidentCreate, IncidentUpdate
class AdminAuthTests(unittest.TestCase):
    def test_fails_closed_without_config(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(HTTPException) as ctx: require_admin("Bearer token")
            self.assertEqual(ctx.exception.status_code, 503)
    def test_rejects_missing_and_wrong_tokens(self):
        with patch.dict(os.environ, {"ADMIN_API_TOKEN": "x" * 40}):
            for value in (None, "Basic abc", "Bearer wrong"):
                with self.subTest(value=value):
                    with self.assertRaises(HTTPException) as ctx: require_admin(value)
                    self.assertEqual(ctx.exception.status_code, 401)
    def test_accepts_correct_token(self):
        token = "x" * 40
        with patch.dict(os.environ, {"ADMIN_API_TOKEN": token}):
            self.assertIsNone(require_admin(f"Bearer {token}"))
class InputValidationTests(unittest.TestCase):
    def test_coordinates_are_bounded(self):
        with self.assertRaises(ValidationError):
            IncidentCreate(description="Pothole report", lat=120, lng=88.3)
    def test_patch_rejects_invalid_status(self):
        with self.assertRaises(ValidationError): IncidentUpdate(status="approved")
    def test_empty_patch_is_detectable(self):
        self.assertEqual(IncidentUpdate().model_fields_set, set())
if __name__ == "__main__": unittest.main()
