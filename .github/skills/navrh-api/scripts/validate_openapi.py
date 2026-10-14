# Checks that an API design is a valid OpenAPI document: validate_openapi.py api/<project>.openapi.yaml [...]
#
# Uses openapi-spec-validator, which picks the schema by the `openapi` field (3.0, 3.1, 3.2),
# and reports every error with its location. Whether the API matches the user stories
# is the reviewer's job, not this script's.
#
# Requires: pip install -r requirements.txt
# Exit codes: 0 = valid, 1 = findings, 2 = usage error or missing dependency.
import importlib.util
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[3]
SUFFIX = ".openapi.yaml"


def validator_missing():
    return importlib.util.find_spec("openapi_spec_validator") is None


def validate(text):
    import yaml
    from openapi_spec_validator.shortcuts import get_validator_cls
    from openapi_spec_validator.validation.exceptions import ValidatorDetectError

    try:
        spec = yaml.safe_load(text)
    except yaml.YAMLError as error:
        return [f"Not valid YAML: {error}"]
    if not isinstance(spec, dict):
        return ["The document is not a YAML mapping."]

    if not isinstance(spec.get("openapi"), str):
        return ["Missing `openapi` version string, e.g. `openapi: 3.1.0`."]
    try:
        validator_cls = get_validator_cls(spec)
    except ValidatorDetectError:
        return [f"Unsupported `openapi` version: {spec['openapi']}"]

    return [f"{error.json_path}: {error.message}" for error in validator_cls(spec).iter_errors()]


def project_of(spec_path, repo_root):
    try:
        parts = spec_path.resolve().relative_to(repo_root.resolve()).parts
    except ValueError:
        return None
    if len(parts) == 2 and parts[0] == "api" and parts[1].endswith(SUFFIX):
        return parts[1][: -len(SUFFIX)]
    return None


def main(argv, repo_root=REPO_ROOT):
    if not argv:
        print("Usage: validate_openapi.py api/<project>.openapi.yaml [...]", file=sys.stderr)
        return 2
    if validator_missing():
        print("openapi-spec-validator is not installed: pip install -r requirements.txt", file=sys.stderr)
        return 2

    status = 0
    for argument in argv:
        spec_path = Path(argument)
        project = project_of(spec_path, repo_root)
        if project is None or not (repo_root / "docs" / project).is_dir() or not spec_path.is_file():
            print(f"{argument}: expected an existing file api/<project>{SUFFIX} with a matching docs/<project>/.",
                  file=sys.stderr)
            return 2

        findings = validate(spec_path.read_text(encoding="utf-8"))
        if findings:
            status = 1
            print(f"{argument}: {len(findings)} finding(s)")
            for finding in findings:
                print(f"  - {finding}")
        else:
            print(f"{argument}: OK")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
