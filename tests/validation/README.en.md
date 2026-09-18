# tests/validation/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](README.en.md)

Tests for link consistency across documentation. Wraps `scripts/validation/check_doc_links.py` (a script that extracts relative links from every Markdown file in the repository and verifies that each link target exists) so it also runs from the regular test suite and CI.

**Status: Implemented.** Run with `pytest tests/validation/ -v`.
