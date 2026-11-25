# Manifest validation

PSBBV Applications is a built-in Vita node. Its manifest is validated against the
pinned PSBBV Core Node Manifest contract before changes are accepted.

## Local check

Use Python 3.12 and the CI-pinned validator:

```sh
python -m pip install jsonschema==4.25.1
python tests/validate_manifest.py
```

The check validates the Draft 2020-12 schema, the current `psbbv-node.json`,
and negative fixtures for capability limits, permission uniqueness, identifier
syntax, unknown fields, runtime shape and unsupported manifest versions. It also
tests the permission `maxItems` bound independently from the current six-value
permission enum.

## Contract ownership

The schema in `schemas/psbbv-node-manifest.schema.json` is a pinned compatibility
copy, not an independently designed Applications schema. Its provenance and
upstream revision are recorded in [schemas/README.md](../schemas/README.md).
When Core changes the canonical contract, review the upstream diff, update the
pinned copy deliberately, and run this check before changing the node manifest.

## Scope boundary

This check validates node registration metadata only. It does not implement an
application catalogue, inspect VPK files, verify package signatures, install or
remove applications, or prove Vita hardware compatibility. Those remain
separate product milestones.
