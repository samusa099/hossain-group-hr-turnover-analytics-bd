"""Regression tests for privacy-safe project validation output."""

from __future__ import annotations

import io
import unittest
from contextlib import redirect_stdout

from scripts.validate_project import fail


class FailLoggingTests(unittest.TestCase):
    """Ensure validation remains actionable without exposing caller data."""

    @staticmethod
    def capture_failure(message: str) -> tuple[bool, str]:
        stream = io.StringIO()
        with redirect_stdout(stream):
            result = fail(message)
        return result, stream.getvalue()

    def test_employee_identifier_is_not_logged(self) -> None:
        result, output = self.capture_failure("Duplicate Employee_ID: EMP-12712922")

        self.assertFalse(result)
        self.assertEqual(output, "FAIL [employee-id]: project validation failed.\n")
        self.assertNotIn("EMP-12712922", output)

    def test_secret_like_value_and_path_are_not_logged(self) -> None:
        secret = "ghp_abcdefghijklmnopqrstuvwxyz1234567890"
        message = f"Potential GitHub classic token in /home/musa/secrets.txt: {secret}"
        result, output = self.capture_failure(message)

        self.assertFalse(result)
        self.assertEqual(output, "FAIL [secret-pattern]: project validation failed.\n")
        self.assertNotIn(secret, output)
        self.assertNotIn("/home/musa", output)

    def test_unknown_message_uses_safe_fallback(self) -> None:
        result, output = self.capture_failure("Unexpected private diagnostic payload")

        self.assertFalse(result)
        self.assertEqual(output, "FAIL [validation]: project validation failed.\n")
        self.assertNotIn("private diagnostic payload", output)


if __name__ == "__main__":
    unittest.main()
