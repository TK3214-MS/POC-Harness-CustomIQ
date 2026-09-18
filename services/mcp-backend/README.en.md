# services/mcp-backend/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](README.en.md)

MCP Backend implemented with FastAPI (Integration and Action Layer).

**Status: Implemented.** It consists of `mcp_backend/registry.py` (generic `MCPToolResponse` wrapper), `mcp_backend/app.py` (FastAPI application), and `mcp_backend/factory.py` (dynamically loads an Industry Pack's `tools/*.py` files and assembles the application).

You can use `services/mcp-backend/run_dev_server.py` to start an HTTP server with the sample dataset. After deployment to Azure, connect the generic MCP tool in Copilot Studio to `/mcp`.

The internal Python package name is `mcp_backend`. The directory name `mcp-backend` is retained as the deployment container name.

Each of the five Industry Packs exposes its own business tools. Add tools through each pack's `manifest.yaml` and `tools/*.py`; the Backend itself does not need to change.
