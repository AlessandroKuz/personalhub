# =============================================================================
# STAGE 1 — BUILDER
# Purpose: Install all dependencies using uv into a virtual environment.
# We use a separate stage so that uv itself and any build-time system packages
# never end up in the final production image.
# =============================================================================
FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS builder

# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc bytecode files.
# We don't need them in a container — they'd just add layer weight.
# PYTHONUNBUFFERED: Forces stdout/stderr to be unbuffered. Without this,
# your print() calls and log output may not appear in `docker logs` immediately,
# which makes debugging painful.
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

WORKDIR /app

# --- DEPENDENCY INSTALLATION (exploiting layer caching) ---
# We copy ONLY the dependency manifest files first, before copying
# any application code. This way, if you change views.py but not
# pyproject.toml / uv.lock, Docker reuses the cached layer below
# and skips the (slow) uv sync step entirely.
COPY pyproject.toml uv.lock ./

# Install production dependencies into a virtual environment at /app/.venv
# --frozen: Treats uv.lock as the source of truth. Fails if lock is outdated.
#           This guarantees reproducibility — you get exactly what was locked.
# --no-dev: Skips development dependencies (pytest, ruff, debug-toolbar, etc.)
# --no-install-project: Installs dependencies but not the project itself yet.
#                       We'll do that after copying the rest of the source code.
RUN uv sync --frozen --no-dev --no-install-project

# Now copy the full project source
COPY . .

# Install the project itself (makes your apps importable as a package if needed)
# The dependencies are already installed from the step above, so this is fast.
RUN uv sync --frozen --no-dev


# =============================================================================
# STAGE 2 — RUNTIME
# Purpose: A clean, minimal image that only contains what's needed to RUN
# the application. Build tools, uv itself, and temporary files are left behind.
# =============================================================================
FROM python:3.14-slim-trixie AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  # Tell Python to use our virtual environment's binaries by prepending
  # the .venv/bin directory to PATH. This means `python` and `uvicorn`
  # resolve to the venv versions, not the system Python.
  PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Create a non-root user for running the application.
# Running as root inside a container is a security risk — if an attacker
# escapes the container, they'd have root on the host. This is a standard
# hardening practice.
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy the entire application (code + installed .venv) from the builder stage.
# We do NOT copy uv — it's not needed at runtime.
COPY --from=builder --chown=appuser:appgroup /app /app

# Copy and prepare the entrypoint script.
# The entrypoint handles migrations and collectstatic before starting the server.
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN mkdir -p /srv/personalhub/staticfiles \
  && chown -R appuser:appgroup /srv/personalhub

USER appuser

# Document that the container listens on port 8000.
# EXPOSE is metadata only — it doesn't actually publish the port.
# Publishing happens in docker-compose via `ports:`.
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
