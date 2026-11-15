# PSBBV Applications

**SPDW Factory · The software shelf for your Vita.**

PSBBV Applications is the application catalogue and management node. It presents installed and approved application metadata and provides safe, transparent management workflows. PSBBV Core owns global navigation, focus, lifecycle, permissions and node registration.

## Scope

- Discover and display installed applications using supported Vita metadata.
- Catalogue approved homebrew applications and their version/source metadata.
- Show install state, version, update availability and compatibility notes.
- Provide user-confirmed install, update and uninstall workflows through supported system interfaces.
- Validate package metadata before presenting an action.
- Report operation progress, logs and actionable errors through the PSBBV Node API.

## Architecture rules

- Built-in PSBBV node first; no dynamic third-party code loading or Python runtime on Vita.
- Follow the versioned Node API and manifest contract in [PSBBV Core](https://github.com/SilverCrow2323/PSBBV).
- Separate catalogue providers, package inspection, transaction orchestration and UI.
- Require explicit user confirmation for destructive operations. Never silently remove user data or saves.
- Verify package identity, title ID, size and integrity before installation.
- Do not host or redistribute proprietary applications, keys or copyrighted payloads.

## Delivery order

1. Define application metadata schema and trusted catalogue source format.
2. Build fixture-driven parser and catalogue validator.
3. Implement installed-app inventory and detail view.
4. Add package inspection and compatibility warnings.
5. Integrate guarded install/update/uninstall operations with rollback-aware state reporting.
6. Test on physical Vita hardware, including interrupted operations and low-storage recovery.

## Quality gates

Malformed catalogue/package tests, path traversal and signature/integrity checks, transaction-state tests, VitaSDK build and physical install/update/uninstall validation. CI packaging is not proof that a package installs correctly on a Vita.

## Status

Repository bootstrap and product boundary only. Planned features are not yet implemented. English UI/docs and SPDW Factory identity are required.
