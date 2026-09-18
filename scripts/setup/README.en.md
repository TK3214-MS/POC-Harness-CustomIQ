# scripts/setup/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](README.en.md)

Environment setup script (`setup` command, instruction §28).

**Status: Implemented.** [setup.sh](setup.sh) creates `.venv` and runs `pip install -e ".[dev]"`, `ruff check .`, and `pytest tests/ -q`. The Python executable can be specified with `PYTHON_BIN`. A network connection is required.
