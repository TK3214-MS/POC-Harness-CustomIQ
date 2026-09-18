# deployment/containers/

[![日本語](https://img.shields.io/badge/%E3%81%82-%E6%97%A5%E6%9C%AC%E8%AA%9E-5B6670?style=for-the-badge)](README.md) [![English](https://img.shields.io/badge/A-English-087F8C?style=for-the-badge)](README.en.md)

Container configuration for the MCP Backend and other services, including the Dockerfile and non-root execution settings.

`mcp-backend/Dockerfile` runs as a non-root user and installs only runtime dependencies. Verify the build in a real environment or CI.

Run the build from the repository root:

```bash
docker build -f deployment/containers/mcp-backend/Dockerfile -t iiq-mcp-backend .
```
