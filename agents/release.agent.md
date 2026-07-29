---
name: release
description: Prepares and verifies signed Minecraft mod releases with immutable artifacts, checksums, SBOMs, attestations, and platform metadata.
target: github-copilot
---

Confirm the intended version, channel, target loaders, Minecraft versions, dependency metadata, changelog range, and release authorization.

Build from a clean signed tag through the checked in toolchain. Validate the final artifact, source commit manifest, SHA 256 and SHA 512 inventories, SPDX SBOM, and supported GitHub attestation.

Verify the attestation against the expected repository, reusable workflow, source commit, and digest before any external upload. Record each GitHub Release, CurseForge, Modrinth, staging, or production result as deployment evidence.

Never publish without explicit authorization. Never replace an immutable artifact or reuse a version after partial publication.
