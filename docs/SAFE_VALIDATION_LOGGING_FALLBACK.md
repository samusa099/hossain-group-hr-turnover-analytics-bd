# Safe Validation Logging: Primary Design and Fallback Runbook

## Purpose

This runbook preserves actionable CI diagnostics without allowing employee identifiers, secrets, file content, local paths, exception text, or other caller-controlled values to reach repository logs.

It documents the approved implementation from PR #46 and defines safe fallback options for future maintenance or incident recovery.

> **Security invariant:** no fallback may reintroduce caller-controlled text into the logging sink.

---

## Approved primary design

The validator uses a typed, allow-listed diagnostic boundary:

```python
fail(FailureCategory.EMPLOYEE_ID)
```

`fail()` accepts only `FailureCategory` values and emits a deterministic category-level message:

```text
FAIL [employee-id]: project validation failed.
```

This is preferred over message parsing, regex replacement, or downstream log filtering because sensitive data is never accepted by the sink.

### Required properties

- `FailureCategory` remains an allow-listed enum.
- Every validator call site passes a fixed enum member.
- Raw strings, formatted strings, exception messages, paths, identifiers, and file values are not passed to `fail()`.
- Regression tests verify deterministic output and rejection of raw messages.
- CodeQL and repository security checks remain required before merge.

---

## Safe fallback hierarchy

Use the first available option. Do not skip directly to a weaker option for convenience.

### Fallback 1 — static emergency diagnostic

If the typed category implementation is temporarily unavailable or suspected to be unsafe, replace dynamic diagnostics with one constant message:

```python
def fail(_value: object) -> bool:
    print("FAIL: project validation failed.")
    return False
```

This reduces observability but preserves the security boundary. Use it only as a short-lived emergency containment measure.

### Fallback 2 — fixed category at the call site

When a new validator check is introduced, add a new enum member and pass it directly:

```python
class FailureCategory(str, Enum):
    NEW_POLICY = "new-policy"


def validate_new_policy() -> bool:
    if policy_failed:
        return fail(FailureCategory.NEW_POLICY)
    return True
```

Do not derive the category from free-form error text.

### Fallback 3 — workflow-level containment

If a suspected logging regression cannot be fixed immediately:

1. block the affected workflow or validation path from publishing artifacts;
2. retain a generic non-sensitive job failure;
3. open a focused security PR from the latest `main`;
4. restore typed categories and regression coverage;
5. require fresh CodeQL and validation runs before merge.

Workflow containment must not print captured exceptions, environment variables, file contents, or raw validation output.

---

## Patterns that are not acceptable fallbacks

Do not use any of the following as the final security boundary:

```python
fail(f"Duplicate Employee_ID: {employee_id}")
fail(str(exception))
print(sanitize_for_log(message))
print(re.sub(pattern, "[REDACTED]", message))
```

These patterns allow caller-controlled or sensitive text to reach the logging path before, during, or after attempted sanitization.

Regex redaction may be used as defence in depth for unrelated application logs, but it must not replace the typed allow-list boundary in this validator.

---

## Future change procedure

When adding or changing validation diagnostics:

1. Start a fresh topic branch from the current `main`.
2. Add or reuse a narrowly scoped `FailureCategory` member.
3. Update the relevant call site without passing raw details.
4. Add or update regression tests.
5. Confirm there are no `fail(f"...")`, `fail(str(...))`, or raw-string `fail(...)` call sites.
6. Run Python compilation and unit tests.
7. Open a focused pull request.
8. Require CodeQL, security validation, dependency review, and repository validation.
9. Resolve all actionable review threads.
10. Squash merge after the required checks pass.

After a squash merge, do not reuse the old long-running head branch for follow-up work. Create a new branch from the updated `main` so previous commits are not reintroduced into comparisons.

---

## Verification checklist

- [ ] `fail()` accepts only `FailureCategory`.
- [ ] All call sites pass enum members.
- [ ] No employee ID, path, token, exception, or file content is logged.
- [ ] Raw messages are rejected before output.
- [ ] Safe-output regression tests pass.
- [ ] CodeQL passes.
- [ ] Security and project validation passes.
- [ ] Dependency review passes.
- [ ] No unresolved review thread remains.

Recommended commands:

```bash
python -m compileall -q scripts tests
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/validate_project.py
```

---

## Final verdict and decision record

**Original review record:** Worked for 3m 9s.

Best-practice remediation was implemented and merged through PR #46 after review of GitHub CodeQL guidance, OWASP, CWE, Stack Overflow discussions, public DevOps and Reddit discussions, and Slack developer-security guidance.

### কেন PR #46-এর সমাধানটি সঠিক

আগের substring বা regex design-এ free-form message logging boundary পর্যন্ত যেত:

```python
fail("Duplicate Employee_ID: EMP-123")
```

Message সরাসরি print না হলেও sensitive value function boundary পর্যন্ত পৌঁছে যেত এবং পরবর্তী parsing বা redaction-এর উপর নিরাপত্তা নির্ভর করত।

বর্তমান design:

```python
fail(FailureCategory.EMPLOYEE_ID)
```

এখানে `fail()` কেবল typed, allow-listed enum গ্রহণ করে। Employee ID, path, exception, token বা অন্য caller-controlled text function-এ পাঠানো হয় না।

এই design CodeQL-এর sensitive data log না করার নির্দেশনা, OWASP logging guidance এবং CWE-532-এর সঙ্গে সামঞ্জস্যপূর্ণ।

### Community findings

Stack Overflow এবং public engineering discussions দেখায় যে final `str.replace()` বা regex redaction যথেষ্ট নাও হতে পারে, কারণ secret আগে থেকেই exception message বা traceback-এর মধ্যে থাকতে পারে। তাই downstream filtering-এর চেয়ে source-to-sink prevention শক্তিশালী।

Public DevOps discussions-এ accidental token বা session-data logging-এর পরে sanitization, safer middleware এবং CI regression checks যোগ করার pattern দেখা যায়। Slack-এর developer-security guidance-ও logs থেকে tokens, passwords এবং PII বাদ রাখতে বলে।

### Git specialist recommendation

PR #43 squash-merge হওয়ার পর অনুসরণ করা clean workflow:

1. latest `main` থেকে fresh topic branch;
2. focused change;
3. dedicated PR;
4. required CodeQL এবং CI checks;
5. squash merge.

PR #46 এই workflow অনুসরণ করে merge হয়েছে।

### Completed result

- Typed `FailureCategory` enum
- Raw strings rejected by the logging boundary
- All `fail()` call sites converted to fixed categories
- Regression tests added
- CodeQL passed
- Security and project validation passed
- Dependency review passed
- Safe logging regression passed
- PR #46 merged into `main`
- Independent security audit recorded on PR #46

**Conclusion:** The current implementation is stronger than regex masking and substring categorization while preserving actionable, privacy-safe CI diagnostics. No code fallback should weaken this boundary.

---

## References

- [GitHub CodeQL: Clear-text logging of sensitive information](https://codeql.github.com/codeql-query-help/python/py-clear-text-logging-sensitive-data/)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [CWE-532: Insertion of Sensitive Information into Log File](https://cwe.mitre.org/data/definitions/532.html)
- [GitHub pull request merge methods](https://docs.github.com/en/pull-requests/reference/pull-request-merges)
- [Slack security practices for apps](https://slack.dev/security-practices-for-slack-apps/)
- [PR #43](https://github.com/samusa099/hossain-group-hr-turnover-analytics-bd/pull/43)
- [PR #46](https://github.com/samusa099/hossain-group-hr-turnover-analytics-bd/pull/46)
- Merge commit: `93edd1d0c77df88314a1e05132829343ae69f01a`
