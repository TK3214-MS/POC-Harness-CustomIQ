"""Production entrypoint for the MCP Backend container (Phase 5).

Unlike run_dev_server.py (hardcoded to Manufacturing, for local ad-hoc testing),
this reads its Industry Pack selection from environment variables so the same
container image can serve any pack without a code change or rebuild - see
docs/decisions/0010-industry-pack-plugin-loading.md /
docs/decisions/0011-generic-orchestrator-and-semantic-adapter.md.

Environment variables:
    IIQ_INDUSTRY_PACK   Industry Pack id under industry-packs/ (default: manufacturing)
    IIQ_DATA_SCALE      "demo" or "realistic" (default: demo)
    IIQ_DATA_SEED       Integer seed for the synthetic data generator (default: 42)
    PORT                TCP port to listen on (default: 8000)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "services" / "mcp-backend"))

from mcp_backend.factory import build_app

from iq_platform.orchestration.industry_pack_loader import load_plugin_module

ALL_PACK_IDS = ["manufacturing", "financial-services", "retail", "healthcare", "public-sector"]


def create_app():
    pack_id = os.environ.get("IIQ_INDUSTRY_PACK", "manufacturing")
    if pack_id not in ALL_PACK_IDS:
        raise ValueError(f"Unknown IIQ_INDUSTRY_PACK '{pack_id}'; expected one of {ALL_PACK_IDS}")
    scale = os.environ.get("IIQ_DATA_SCALE", "demo")
    seed = int(os.environ.get("IIQ_DATA_SEED", "42"))

    pack_dir = REPO_ROOT / "industry-packs" / pack_id
    generator = load_plugin_module(pack_dir / "data" / "generator.py")
    dataset = generator.generate_dataset(seed=seed, scale=scale)
    return build_app(dataset, pack_dir)


# Module-level ASGI app object for `uvicorn server:app` / container CMD.
app = create_app()


def main() -> None:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))


if __name__ == "__main__":
    main()
