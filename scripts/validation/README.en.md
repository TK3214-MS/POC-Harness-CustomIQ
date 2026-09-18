# scripts/validation/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](README.en.md)

Industry Pack schema validation and synthetic data validation (real-name denylist, email/phone pattern scanning, and more; instruction §23).

**Status: Implemented.** [validate_synthetic_data.py](validate_synthetic_data.py) scans files under `industry-packs/` for real names on the denylist, non-reserved email domains, phone-number-like patterns, and SSN-like patterns (runs in CI). This is a heuristic check, not a complete guarantee.
