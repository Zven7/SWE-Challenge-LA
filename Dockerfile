# ---------- builder ----------
FROM python:3.12-slim AS builder

WORKDIR /app

# system deps (needed for compiling some wheels)
RUN apt-get update && apt-get install -y \
    curl build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# install uv
RUN pip install uv

# copy dependency files first (cache-friendly)
COPY pyproject.toml uv.lock ./

# install deps into venv managed by uv
RUN uv sync --frozen --no-install-project


# ---------- runtime ----------
FROM python:3.12-slim

WORKDIR /app

# copy virtualenv from builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

ENV PATH="/root/.local/bin:$PATH"

# copy source
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]