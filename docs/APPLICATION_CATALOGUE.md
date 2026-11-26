# PSBBV Applications catalogue contract

The first catalogue milestone defines a strict, source-aware metadata format. It is separate from the PSBBV node manifest: the node manifest describes what the node may do; this catalogue describes which applications it may present.

## Contract

- Catalogue identity, version and generation timestamp are explicit.
- Each entry has a stable unique application ID, display name, version, status, platform and category.
- Vita title IDs are validated and unique when present.
- Approved entries must carry a package record with an HTTPS URL, bounded non-zero size, format and SHA-256 digest.
- Planned/deprecated entries cannot masquerade as installable packages.
- Catalogue source declares its trust model: signed, pinned or manual-review.
- Unknown fields are rejected; list sizes and text lengths are bounded.

## Validate

```sh
python -m pip install jsonschema==4.25.1
python tests/validate_manifest.py
python tests/validate_catalogue.py
```

The example catalogue is an empty, non-deployable fixture using the reserved .invalid domain. No real homebrew is listed or endorsed by this milestone.

## Not implemented yet

This contract does not download catalogues, verify signatures, inspect VPK contents, discover installed applications or install/uninstall packages. Those remain separate milestones and must use explicit user confirmation and rollback-aware transactions.
