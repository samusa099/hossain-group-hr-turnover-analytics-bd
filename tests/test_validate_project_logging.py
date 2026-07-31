"""Regression tests for privacy-safe project validation output."""

from __future__ import annotations

import io
import unittest
from contextlib import redirect_stdout

from scripts.validate_project import FailureCategory, fail


class FailLoggingTests(unittest.TestCase):
    """Ensure validation remains actionable without accepting caller data."""

    @staticmethod
    def capture_failure(category: FailureCategory) -> tuple[bool, str]:
        stream = io.StringIO()
        with redirect_stdout(stream):
            result = fail(category)
        return result, stream.getvalue()

    def test_employee_identifier_category_is_safe(self) -> None:
        result, output = self.capture_failure(FailureCategory.EMPLOYEE_ID)

        self.assertFalse(result)
        self.assertEqual(output, "FAIL [employee-id]: project validation failed.\n")
        self.assertNotIn("EMP-12712922", output)

    def test_secret_category_contains_no_value_or_path(self) -> None:
        result, output = self.capture_failure(FailureCategory.SECRET_PATTERN)

        self.assertFalse(result)
        self.assertEqual(output, "FAIL [secret-pattern]: project validation failed.\n")
        self.assertNotIn("/home/musa", output)
        self.assertNotIn("github_pat_", output)

    def test_every_category_has_deterministic_output(self) -> None:
        for category in FailureCategory:
            with self.subTest(category=category):
                result, output = self.capture_failure(category)
                self.assertFalse(result)
                self.assertEqual(
                    output,
                    f"FAIL [{category.value}]: project validation failed.\n",
                )

    def test_raw_message_is_rejected_before_logging(self) -> None:
        stream = io.StringIO()
        with self.assertRaises(AttributeError), redirect_stdout(stream):
            fail("Unexpected private diagnostic payload")  # type: ignore[arg-type]

        self.assertEqual(stream.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
