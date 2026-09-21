# Security Documentation

This page is the index for security documentation. [SECURITY.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/SECURITY.md) is the authoritative source for general repository policy and vulnerability reporting. The [MCP Security Guide](../mcp/MCP-Security-Guide.md) is the authoritative source for controls specific to the MCP Backend.

Secret scanning is implemented by [scan_secrets.py](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/scripts/security/scan_secrets.py) and runs in CI. The container runs as non-root. See the [Dockerfile](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/deployment/containers/mcp-backend/Dockerfile). For the baseline policy, see [SECURITY.md](https://github.com/TK3214-MS/POC-Harness-CustomIQ/blob/main/SECURITY.md).
