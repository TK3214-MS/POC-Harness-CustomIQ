"""Optional standalone server for the Manufacturing sample MCP Backend.

Useful for manually exercising the FastAPI app over real HTTP (e.g. with curl)
outside of the in-process test path.

Run with:
    PYTHONPATH=.:services/mcp-backend python3 services/mcp-backend/run_dev_server.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "services" / "mcp-backend"))

from mcp_backend.factory import build_app

from iq_platform.orchestration.industry_pack_loader import load_plugin_module

MANUFACTURING_PACK_DIR = REPO_ROOT / "industry-packs" / "manufacturing"


def main() -> None:
    import uvicorn

    generator = load_plugin_module(MANUFACTURING_PACK_DIR / "data" / "generator.py")
    dataset = generator.generate_dataset(seed=42, scale="demo")
    app = build_app(dataset, MANUFACTURING_PACK_DIR)
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
