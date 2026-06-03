# Superpowers Vendor Notice

This directory contains a curated source-material snapshot from Superpowers by Jesse Vincent.

- Upstream repository: https://github.com/obra/superpowers
- License: MIT
- License file: `LICENSE`
- Purpose in this repository: source material for Harness Skills workflow adaptations

This vendor tree is intentionally outside `.codex-plugin`'s exposed `./skills/` path. Installing the Harness Skills plugin should install Harness-owned skills only, not a second copy of Superpowers skills.

Do not edit vendor files as product workflow instructions. Adapt useful procedures into `skills/workflows/` and keep `agent-harness` plus local gates authoritative.
