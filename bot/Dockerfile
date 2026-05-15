# ── Imagen base ────────────────────────────────────────────────
FROM python:3.11-slim

# ── Variables de entorno ───────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OMP_NUM_THREADS=1 \
    TOKENIZERS_PARALLELISM=false \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# ── Instalar dependencias Python ───────────────────────────────
# No necesitamos apt-get: todos los paquetes tienen wheels pre-compilados
COPY requirements.txt .

RUN pip install --upgrade pip --quiet && \
    pip install --no-cache-dir -r requirements.txt

# ── Copiar el proyecto ─────────────────────────────────────────
COPY . .

# ── Crear carpetas necesarias ──────────────────────────────────
RUN mkdir -p app/data/uploads app/data/vectorstores

EXPOSE 5000

CMD ["gunicorn", "-w", "1", "--timeout", "120", \
     "--bind", "0.0.0.0:5000", "app.main:app"]