# ── Imagen base ────────────────────────────────────────────────
FROM python:3.11-slim

# ── Variables de entorno ───────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OMP_NUM_THREADS=1 \
    TOKENIZERS_PARALLELISM=false \
    PIP_NO_CACHE_DIR=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# ── Instalar dependencias del sistema (necesarias para algunos paquetes Python) ──
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ── Instalar dependencias Python ───────────────────────────────
COPY requirements.txt .

RUN pip install --upgrade pip --quiet && \
    pip install --no-cache-dir -r requirements.txt

# ── Copiar el proyecto ─────────────────────────────────────────
COPY . .

# ── Crear carpetas necesarias y establecer permisos ────────────
RUN mkdir -p app/data/uploads app/data/vectorstores && \
    chmod -R 755 app/data

# ── Healthcheck ────────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import sys, urllib.request; sys.exit(0 if urllib.request.urlopen('http://localhost:5000/health').getcode() == 200 else 1)"

EXPOSE 5000

# ── Usar usuario no-root para seguridad ────────────────────────
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

CMD ["gunicorn", "-w", "1", "--timeout", "120", "--bind", "0.0.0.0:5000", "app.main:app"]
