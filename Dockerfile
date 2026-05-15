# Imagen base Python
FROM python:3.11-slim


# Variables entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Directorio trabajo
WORKDIR /app


# Instalar dependencias Linux
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && apt-get clean


# Copiar requirements
COPY requirements.txt .


# Actualizar pip
RUN pip install --upgrade pip


# Instalar dependencias Python
RUN pip install -r requirements.txt


# Copiar proyecto
COPY . .


# Exponer puerto Flask
EXPOSE 5000


# Ejecutar API
CMD ["python", "app/main.py"]