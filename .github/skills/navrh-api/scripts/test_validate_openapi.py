import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import validate_openapi  # noqa: E402

VALID_SPEC = """\
openapi: 3.1.0
info:
  title: Smart Savings API
  version: 1.0.0
paths:
  /v1/savings-goals:
    get:
      operationId: listSavingsGoals
      summary: Seznam spořicích cílů
      responses:
        '200':
          description: Seznam cílů
"""

NEEDS_VALIDATOR = unittest.skipUnless(
    importlib.util.find_spec("openapi_spec_validator"),
    "openapi-spec-validator is not installed (pip install -r requirements.txt)",
)


@NEEDS_VALIDATOR
class ValidateTest(unittest.TestCase):
    def test_valid_spec_passes(self):
        self.assertEqual(validate_openapi.validate(VALID_SPEC), [])

    def test_invalid_yaml_is_reported(self):
        findings = validate_openapi.validate(VALID_SPEC + "  bad: [unclosed\n")
        self.assertTrue(any("yaml" in finding.lower() for finding in findings), findings)

    def test_document_that_is_not_a_mapping_is_reported(self):
        findings = validate_openapi.validate("- openapi: 3.1.0\n")
        self.assertEqual(len(findings), 1, findings)

    def test_missing_version_is_reported(self):
        findings = validate_openapi.validate(VALID_SPEC.replace("openapi: 3.1.0\n", ""))
        self.assertTrue(any("openapi" in finding for finding in findings), findings)

    def test_unquoted_version_number_is_reported(self):
        findings = validate_openapi.validate(VALID_SPEC.replace("openapi: 3.1.0", "openapi: 3.1"))
        self.assertTrue(any("openapi" in finding for finding in findings), findings)

    def test_schema_error_names_its_location(self):
        spec = VALID_SPEC.replace("        '200':", "        ok:")
        findings = validate_openapi.validate(spec)
        self.assertTrue(any("$.paths['/v1/savings-goals'].get.responses" in finding for finding in findings),
                        findings)

    def test_every_error_is_reported_not_just_the_first(self):
        spec = VALID_SPEC.replace("  version: 1.0.0\n", "").replace("        '200':", "        ok:")
        findings = validate_openapi.validate(spec)
        self.assertTrue(any(finding.startswith("$.info:") for finding in findings), findings)
        self.assertTrue(any(finding.startswith("$.paths") for finding in findings), findings)


class MainTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "docs" / "smart-savings").mkdir(parents=True)
        (self.root / "api").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def run_main(self, spec_text, name="smart-savings.openapi.yaml"):
        spec = self.root / "api" / name
        spec.write_text(spec_text, encoding="utf-8")
        return self.quiet_main(spec)

    def quiet_main(self, spec):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return validate_openapi.main([str(spec)], repo_root=self.root)

    @NEEDS_VALIDATOR
    def test_valid_spec_exits_zero(self):
        self.assertEqual(self.run_main(VALID_SPEC), 0)

    @NEEDS_VALIDATOR
    def test_invalid_spec_exits_one(self):
        self.assertEqual(self.run_main(VALID_SPEC.replace("  version: 1.0.0\n", "")), 1)

    def test_spec_without_matching_docs_project_exits_two(self):
        self.assertEqual(self.run_main(VALID_SPEC, name="jiny-projekt.openapi.yaml"), 2)

    def test_spec_outside_api_exits_two(self):
        stray = self.root / "smart-savings.openapi.yaml"
        stray.write_text(VALID_SPEC, encoding="utf-8")
        self.assertEqual(self.quiet_main(stray), 2)

    def test_missing_validator_exits_two_and_says_how_to_install(self):
        stderr = io.StringIO()
        with mock.patch.object(validate_openapi, "validator_missing", return_value=True), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(stderr):
            status = validate_openapi.main(["api/smart-savings.openapi.yaml"], repo_root=self.root)
        self.assertEqual(status, 2)
        self.assertIn("pip install -r requirements.txt", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
