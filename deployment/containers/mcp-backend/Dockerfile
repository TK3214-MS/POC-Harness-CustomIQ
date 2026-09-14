# MCP Backend container image. Serves any Industry Pack selected via the
# IIQ_INDUSTRY_PACK environment variable; see services/mcp-backend/server.py.
#
# Build from the REPOSITORY ROOT (not this directory), since the image needs
# iq_platform/ and industry-packs/ alongside services/mcp-backend/:
#   docker build -f deployment/containers/mcp-backend/Dockerfile -t iiq-mcp-backend .

FROM python:3.12-slim AS base

# Never run as root (instruction section 24).
RUN groupadd --gid 1000 iiq && useradd --uid 1000 --gid iiq --shell /usr/sbin/nologin --create-home iiq

WORKDIR /app

# Install only runtime dependencies (no pytest/ruff in the production image).
COPY services/mcp-backend/requirements.txt /app/services/mcp-backend/requirements.txt
RUN pip install --no-cache-dir -r /app/services/mcp-backend/requirements.txt

# Copy only what the app needs at runtime.
COPY iq_platform/ /app/iq_platform/
COPY services/mcp-backend/ /app/services/mcp-backend/
COPY industry-packs/ /app/industry-packs/

ENV PYTHONPATH="/app:/app/services/mcp-backend" \
    IIQ_INDUSTRY_PACK="manufacturing" \
    IIQ_DATA_SCALE="demo" \
    IIQ_DATA_SEED="42" \
    PORT="8000"

USER iiq
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)" || exit 1

CMD ["python", "/app/services/mcp-backend/server.py"]
