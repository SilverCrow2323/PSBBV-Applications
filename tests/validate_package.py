"""Validation helpers for application package metadata; inspection only, never installs files."""
from pathlib import PurePosixPath
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def validate_package(package, schema):
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = list(validator.iter_errors(package))
    if errors:
        return errors
    seen = set()
    total = 0
    for index, entry in enumerate(package["files"]):
        raw = entry["path"]
        path = PurePosixPath(raw)
        if (path.is_absolute() or "\\" in raw or ":" in raw or
                any(part in ("", ".", "..") for part in raw.split("/")) or
                raw.startswith("/") or "\\x00" in raw):
            errors.append(ValueError(f"unsafe package path at files[{index}]: {raw!r}"))
        if raw in seen:
            errors.append(ValueError(f"duplicate package path: {raw}"))
        seen.add(raw)
        total += entry["sizeBytes"]
    if total > package["sizeBytes"]:
        errors.append(ValueError("declared file sizes exceed package sizeBytes"))
    return errors

def main():
    schema = load(ROOT / "schemas/application-package.schema.json")
    package = load(ROOT / "application-package.example.json")
    Draft202012Validator.check_schema(schema)
    errors = validate_package(package, schema)
    if errors:
        for error in errors:
            print(f"INVALID: {error}")
        return 1
    print(f"Application package metadata valid: {len(package['files'])} file entries; inspection only.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
