#!/usr/bin/env python3
"""Validate the Applications node against the pinned PSBBV Core contract."""

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def rejected_by(validator, instance, keyword: str) -> bool:
    return any(error.validator == keyword for error in validator.iter_errors(instance))


def main() -> int:
    schema = load(ROOT / "schemas" / "psbbv-node-manifest.schema.json")
    manifest = load(ROOT / "psbbv-node.json")
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)

    errors = sorted(
        validator.iter_errors(manifest),
        key=lambda error: list(map(str, error.absolute_path)),
    )
    if errors:
        for error in errors:
            location = ".".join(str(part) for part in error.absolute_path) or "<root>"
            print(f"INVALID {location}: {error.message}")
        return 1

    # Assert the bounded contract itself. The permissions enum currently has
    # exactly six values, so a seventh unique production value cannot isolate
    # maxItems from enum validation. The synthetic schema below does.
    limits = {
        "platforms": ("minItems", 1),
        "capabilities": ("maxItems", 16),
        "permissions": ("maxItems", 6),
    }
    for field, (keyword, expected) in limits.items():
        actual = schema["properties"][field].get(keyword)
        if actual != expected:
            print(f"INVALID schema.{field}.{keyword}: expected {expected}, got {actual}")
            return 1

    invalid_cases = []

    too_many_capabilities = copy.deepcopy(manifest)
    too_many_capabilities["capabilities"] = [f"node.capability{i}" for i in range(17)]
    invalid_cases.append(("capability maxItems", too_many_capabilities, "maxItems"))

    duplicate_permission = copy.deepcopy(manifest)
    duplicate_permission["permissions"] = ["network.client", "network.client"]
    invalid_cases.append(("permission uniqueItems", duplicate_permission, "uniqueItems"))

    malformed_capability = copy.deepcopy(manifest)
    malformed_capability["capabilities"] = ["Invalid.Capability"]
    invalid_cases.append(("capability pattern", malformed_capability, "pattern"))

    unknown_manifest_field = copy.deepcopy(manifest)
    unknown_manifest_field["unexpected"] = True
    invalid_cases.append(("unknown manifest property", unknown_manifest_field, "additionalProperties"))

    invalid_runtime_field = copy.deepcopy(manifest)
    invalid_runtime_field["runtime"]["shell"] = True
    invalid_cases.append(("unknown runtime property", invalid_runtime_field, "additionalProperties"))

    wrong_manifest_version = copy.deepcopy(manifest)
    wrong_manifest_version["manifestVersion"] = 2
    invalid_cases.append(("unsupported manifest version", wrong_manifest_version, "const"))

    for label, fixture, keyword in invalid_cases:
        if not rejected_by(validator, fixture, keyword):
            print(f"INVALID TEST: {label} was not rejected by {keyword}.")
            return 1

    # Isolate the permission array bound from its six-value enum.
    bounded_schema = copy.deepcopy(schema)
    bounded_schema["properties"]["permissions"]["items"]["enum"].append("test.extra")
    bounded_validator = Draft202012Validator(bounded_schema)
    too_many_permissions = copy.deepcopy(manifest)
    too_many_permissions["permissions"] = [
        "media.read", "media.write", "network.client",
        "storage.private", "storage.shared.read", "input.global", "test.extra"
    ]
    if not rejected_by(bounded_validator, too_many_permissions, "maxItems"):
        print("INVALID TEST: permission maxItems was not independently exercised.")
        return 1

    print(
        "PSBBV Applications manifest: valid; "
        f"{len(invalid_cases) + 1} negative contract cases rejected."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
