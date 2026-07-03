#!/usr/bin/env python3
"""Scaffold a test file skeleton for a named subject.

Stdlib only -- no third-party dependencies (references/conventions.md).
Follows references/testing-strategy.md: test isolation (QA020), factories
over hand-copied fixtures (QA013), and mocking the boundary rather than
your own code (QA012) are left as TODOs for you to fill in with real
project-specific setup -- this generates structure, not working assertions.

Examples:
    python3 generate.py order --framework vitest --type unit --output ./my-app
    python3 generate.py orders_api --framework pytest --type integration --output ./my-app
    python3 generate.py checkout --framework playwright --output ./my-app
"""

import argparse
import re
from pathlib import Path

FRAMEWORKS = ["vitest", "jest", "pytest", "playwright"]
TYPES = ["unit", "integration", "e2e"]


def to_pascal(name: str) -> str:
    words = re.sub(r"[_\-\s]+", " ", name).strip().split(" ")
    return "".join(w.capitalize() for w in words if w)


def to_snake(name: str) -> str:
    name = re.sub(r"[_\-\s]+", "_", name).strip("_")
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


def render_vitest_jest(name: str, subject: str, test_type: str, framework: str) -> str:
    if framework == "vitest":
        import_line = 'import { describe, it, expect, beforeEach, vi } from "vitest";'
    else:
        # Jest's describe/it/expect are ambient globals by default; only import
        # from @jest/globals if this project has `injectGlobals: false` set.
        import_line = "// Jest globals (describe/it/expect) are ambient -- no import needed by default."
    body = {
        "unit": f"""// Test the {subject} logic in isolation (QA002) -- no real DB/HTTP, mock the boundary only (QA012).

describe("{subject}", () => {{
  beforeEach(() => {{
    // TODO: reset any shared state -- tests must be independent (QA020)
  }});

  it("does the expected thing given valid input", () => {{
    // TODO: arrange, act, assert
    expect(true).toBe(true);
  }});

  it("handles the expected error case", () => {{
    // TODO
  }});
}});
""",
        "integration": f"""// Integration test: exercises {subject} against a real test database/API,
// not a mock (QA006). Requires test infrastructure (test DB, Supertest, etc.)
// to be wired up in this project's test setup.

describe("{subject} (integration)", () => {{
  beforeEach(() => {{
    // TODO: seed/reset test database state
  }});

  it("persists and retrieves data correctly", async () => {{
    // TODO
    expect(true).toBe(true);
  }});
}});
""",
        "e2e": f"""// Note: for a full browser e2e test, prefer --framework playwright instead.
// This is a lighter-weight integration-style test for {subject}.

describe("{subject} (e2e-ish)", () => {{
  it("completes the expected flow", async () => {{
    // TODO
    expect(true).toBe(true);
  }});
}});
""",
    }[test_type]
    return f"{import_line}\n\n{body}"


def render_pytest(name: str, subject: str, test_type: str) -> str:
    body = {
        "unit": f'''"""Unit tests for {subject} -- isolated from framework/DB (QA002)."""

import pytest


def test_{name}_expected_behavior():
    # TODO: arrange, act, assert
    assert True


def test_{name}_handles_error_case():
    # TODO
    pass
''',
        "integration": f'''"""Integration tests for {subject} -- real test DB/TestClient, not a mock (QA006)."""

import pytest


@pytest.fixture
def {name}_fixture():
    # TODO: set up test data via a factory (QA013), not hand-copied objects
    yield None
    # TODO: teardown if not using transaction rollback (QA023)


def test_{name}_persists_correctly({name}_fixture):
    # TODO
    assert True
''',
        "e2e": f'''"""Note: for a full browser e2e test, prefer --framework playwright instead."""

def test_{name}_completes_expected_flow():
    # TODO
    assert True
''',
    }[test_type]
    return body


def render_playwright(name: str, subject: str) -> str:
    return f"""import {{ test, expect }} from "@playwright/test";

// E2E test for the {subject} flow. Reserve Playwright tests for genuinely
// critical journeys (QA011) -- signup, login, checkout, the core loop --
// not every page.

test("{subject} completes successfully", async ({{ page }}) => {{
  await page.goto("/"); // TODO: navigate to the real starting point

  // TODO: interact with the page the way a real user would
  // await page.getByRole("button", {{ name: "..." }}).click();

  // TODO: assert on the expected outcome
  await expect(page).toHaveURL(/.*/);
}});
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("subject", help="What's being tested, e.g. 'order' or 'checkout flow'")
    parser.add_argument("--framework", required=True, choices=FRAMEWORKS)
    parser.add_argument("--type", choices=TYPES, default="unit", help="Ignored for playwright (always e2e)")
    parser.add_argument("--output", type=Path, default=Path("./generated"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    snake = to_snake(args.subject)
    subject_label = args.subject.strip()

    if args.framework in ("vitest", "jest"):
        content = render_vitest_jest(snake, subject_label, args.type, args.framework)
        rel_path = f"src/__tests__/{snake}.test.ts"
    elif args.framework == "pytest":
        content = render_pytest(snake, subject_label, args.type)
        rel_path = f"tests/test_{snake}.py"
    else:  # playwright
        content = render_playwright(snake, subject_label)
        rel_path = f"e2e/{snake}.spec.ts"

    target = args.output / rel_path
    if args.dry_run:
        print(f"--- would write {target} ---")
        print(content)
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    print(f"wrote {target}")
    print("This is a structural skeleton -- fill in real arrange/act/assert logic before it's a real test (QA013, QA020).")


if __name__ == "__main__":
    main()
