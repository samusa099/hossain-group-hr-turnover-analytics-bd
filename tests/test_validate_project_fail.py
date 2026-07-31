"""Regression tests for safe validation failure output."""

from __future__ import annotations

import io
import unittest
from contextlib import redirect_stdout

from scripts.validate_project import FailureCategory, fail


class FailLoggingTests(unittest.TestCase):
    def test_all_categories_emit_only_allowlisted_output(self) -> None:
        for category in FailureCategory:
            with self.subTest(category=category):
                output = io.StringIO()
                with redirect_stdout(output):
                    result = fail(category)

                self.assertFalse(result)
                self.assertEqual(
                    output.getvalue(),
                    f"FAIL [{category.value}]: project validation failed.\n",
                )

    def test_raw_strings_are_rejected_before_logging(self) -> None:
        output = io.StringIO()
        with self.assertRaises(AttributeError), redirect_stdout(output):
            fail("employee-id=EMP-0001 token=secret")  # type: ignore[arg-type]

        self.assertEqual(output.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
