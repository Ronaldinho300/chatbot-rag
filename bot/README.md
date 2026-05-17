# 🤖 Chatbot RAG API

Una API REST de Chatbot basada en Recuperación Aumentada por Generación (RAG) que permite cargar documentos (PDF, TXT, DOCX) y responder preguntas basadas en su contenido usando Groq Llama 3.3.

## 🎯 Características

- ✅ Carga de documentos en múltiples formatos (PDF, TXT, DOCX)
- ✅ Vectorización automática usando embeddings de HuggingFace
- ✅ Búsqueda semántica con FAISS
- ✅ Respuestas generadas con Groq Llama 3.3
- ✅ API REST con documentación clara
- ✅ CORS habilitado para clientes web
- ✅ Manejo robusto de errores
- ✅ Health check y monitoreo

## 📋 Requisitos Previos

- Python 3.11 o superior
- Groq API Key (para Llama 3.3)
- pip o conda para gestión de paquetes

## 🚀 Instalación Local

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd chatbot-rag
```

### 2. Crear entorno virtual
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

Este proyecto usa paquetes modulares de LangChain en lugar del paquete completo para instalar solo lo necesario y reducir consumo de almacenamiento y recursos.

### 4. Configurar variables de entorno
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env y agregar tu Groq API Key
# GROQ_API_KEY=tu_clave_aqui
```

### 5. Ejecutar la API
```bash
python -m app.main

# O con gunicorn (como en producción)
gunicorn -w 4 -b 0.0.0.0:5000 app.main:app
```

La API estará disponible en `http://localhost:5000`

## 📡 Endpoints API

### 1. Health Check
```http
GET /health
```
**Respuesta (200):**
```json
{
  "status": "healthy",
  "bot_ready": true
}
```

### 2. Información de la API
```http
GET /
```
**Respuesta (200):**
```json
{
  "nombre": "Chatbot RAG API",
  "version": "1.0.0",
  "endpoints": {
    "health": "/health",
    "upload": "/upload (POST)",
    "chat": "/chat (POST)"
  }
}
```

### 3. Cargar Documento
```http
POST /upload
Content-Type: multipart/form-data

archivo: <archivo.pdf|txt|docx>
```

**Respuesta (200):**
```json
{
  "mensaje": "Documento procesado correctamente",
  "archivo": "documento.pdf",
  "tamaño": 45230
}
```

**Errores posibles:**
- `400` - No se envió archivo o extensión no permitida
- `500` - Error procesando el archivo
- `503` - Chatbot no inicializado

### 4. Chat/Preguntas
```http
POST /chat
Content-Type: application/json

{
  "pregunta": "¿Qué es Python?",
  "documento": "mi_documento"  // opcional
}
```

**Respuesta (200):**
```json
{
  "pregunta": "¿Qué es Python?",
  "respuesta": "Python es un lenguaje de programación...",
  "documento": "mi_documento"
}
```

**Errores posibles:**
- `400` - Pregunta vacía o JSON inválido
- `500` - Error generando respuesta
- `503` - Chatbot no inicializado

## 📦 Estructura del Proyecto

```
chatbot-rag/
├── app/
│   ├── main.py              # API Flask
│   ├── chatbot.py           # Orquestador principal
│   ├── loaders.py           # Cargadores de documentos
│   ├── embeddings.py        # Vectorización
│   ├── LangChain.py         # Cadena RAG
│   └── data/
│       ├── identidad_bot.txt       # Instrucciones del bot
│       ├── uploads/                # Documentos cargados
│       └── vectorstores/           # Bases de datos FAISS
├── requirements.txt         # Dependencias Python
├── Procfile                 # Configuración para Render
├── runtime.txt              # Versión de Python
├── .env.example             # Variables de entorno
├── .env                     # Variables reales (ignorado en git)
├── Dockerfile               # Configuración Docker
├── docker-compose.yml       # Orquestación Docker
└── README.md               # Esta documentación
```

## 🌐 Deployment en Render

### Opción 1: Render Web Service (Recomendado)

1. **Subir a GitHub**
   ```bash
   git add .
   git commit -m "Preparado para Render"
   git push origin main
   ```

2. **Conectar con Render**
   - Ve a https://render.com
   - Click en "New +"
   - Selecciona "Web Service"
   - Conecta tu repositorio de GitHub
   - Configura los settings:

   ```
   Name: chatbot-rag
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT app.main:app
   ```

3. **Agregar Variables de Entorno**
   - En la sección "Environment"
   - Agregar:
     ```
     GROQ_API_KEY=tu_clave_aqui
     FLASK_ENV=production
     ```

4. **Deploy**
   - Click en "Create Web Service"
   - Esperar a que se complete el deployment

### Opción 2: Render con Docker

1. **Crear archivo `render.yaml`:**
   ```yaml
   services:
     - type: web
       name: chatbot-rag
       env: docker
       dockerfilePath: ./Dockerfile
       envVars:
         - key: GROQ_API_KEY
           sync: false
   ```

2. **Subir a GitHub y conectar como arriba**

### Opción 3: Render Cron Job (para mantenimiento)

```yaml
services:
  - type: cron
    name: cleanup
    schedule: "0 0 * * 0"  # Cada domingo a medianoche
    dockerfilePath: ./Dockerfile
    command: "python scripts/cleanup.py"
```

## 🔐 Configuración de Groq Llama 3.3

1. **Obtener API Key:**
   - Ve a https://groq.com
   - Inicia sesión en tu cuenta de Groq
   - Crea una nueva clave de API
   - Cópiala en tu `.env`

2. **Configuración:**
   ```env
   GROQ_API_KEY=tu_clave_aqui
   ```

## 📝 Ejemplo de Uso

### Con cURL

```bash
# Cargar documento
curl -X POST http://localhost:5000/upload \
  -F "archivo=@documento.pdf"

# Hacer pregunta
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"pregunta": "¿De qué trata este documento?"}'
```

### Con Python

```python
import requests

api_url = "http://localhost:5000"

# Cargar documento
with open("documento.pdf", "rb") as f:
    files = {"archivo": f}
    response = requests.post(f"{api_url}/upload", files=files)
    print(response.json())

# Hacer pregunta
data = {"pregunta": "¿Cuál es el tema principal?"}
response = requests.post(f"{api_url}/chat", json=data)
print(response.json())
```

### Con JavaScript/Fetch

```javascript
const apiUrl = "http://localhost:5000";

// Cargar documento
const formData = new FormData();
formData.append("archivo", document.getElementById("fileInput").files[0]);

fetch(`${apiUrl}/upload`, {
  method: "POST",
  body: formData
})
.then(res => res.json())
.then(data => console.log(data));

// Hacer pregunta
fetch(`${apiUrl}/chat`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    pregunta: "¿De qué trata?"
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

## 🐳 Uso con Docker

```bash
# Build
docker build -t chatbot-rag .

# Run
docker run -p 5000:5000 \
  -e GROQ_API_KEY="tu_clave_aqui" \
  chatbot-rag

# Con Docker Compose
docker-compose up
```

## 🧪 Testing

```bash
# Health check
curl http://localhost:5000/health

# Info
curl http://localhost:5000/

# Cargar documento de prueba
curl -X POST http://localhost:5000/upload \
  -F "archivo=@test.txt"

# Preguntar
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"pregunta": "Hola"}'
```

## 📊 Límites y Configuración

- **Tamaño máximo de archivo**: 50MB (configurable en `.env`)
- **Máximo de documentos similares**: 3
- **Modelo LLM**: Groq Llama 3.3
- **Modelo de embeddings**: sentence-transformers/all-MiniLM-L6-v2

## ⚠️ Notas Importantes

1. **API Key**: Nunca commits la `.env` real. Siempre usa `.env.example`
2. **Límites de uso**: Groq Llama 3.3 tiene límites gratuitos y de rate.
3. **Almacenamiento**: Los documentos se guardan localmente. En producción, considera usar S3
4. **Escalabilidad**: Para múltiples usuarios, considera usar caché y cola de trabajos

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'google'"
```bash
pip install --upgrade -r requirements.txt
```

### Error: "GROQ_API_KEY not found"
```bash
# Verificar que .env está configurado correctamente
cat .env
```

### Error: "Port 5000 already in use"
```bash
# Cambiar puerto
export PORT=5001
python -m app.main
```

## 📞 Soporte

Para reportar problemas o sugerencias, crea un issue en el repositorio.

## 📄 Licencia

MIT License - ver archivo LICENSE

---

**Desarrollado con ❤️ usando Flask, paquetes modulares de LangChain y Groq Llama 3.3**
