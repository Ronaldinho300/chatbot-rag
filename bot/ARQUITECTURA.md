# Referencia de Arquitectura del Chatbot RAG

## Estructura del Proyecto

```
chatbot-rag/
├── app/
│   ├── main.py              # API Flask - Punto de entrada
│   ├── chatbot.py           # Clase principal que orquesta todo
│   ├── loaders.py           # Carga documentos (PDF, TXT, DOCX)
│   ├── embeddings.py        # Vectorización de textos
│   ├── LangChain.py         # Configuración de cadena RAG
│   └── data/
│       ├── identidad_bot.txt        # Instrucciones del bot
│       ├── uploads/                 # Documentos subidos
│       └── vectorstores/
│           ├── vectorstore.py       # Gestión de FAISS
│           └── */                   # Almacenes de vectores por documento
└── test_notebook.ipynb      # Notebook de prueba
```

## Flujo de Funcionamiento

### 1. Inicio (main.py)
```
Flask inicia
  → Inicializa bot = Chatbot()
    → Carga identidad_bot.txt
    → Bot listo para recibir peticiones
```

### 2. Carga de Documento (/upload POST)
```
Usuario sube documento
  → Guardado en data/uploads/
  → Chatbot.cargar_documento(ruta)
    → Loader.cargar_archivo(ruta)
      → Extrae texto (PDF/TXT/DOCX)
    → VectorStore.guardar(textos, embeddings)
      → Embeddings.modelo crea vectores
      → FAISS almacena en data/vectorstores/
```

### 3. Respuesta (/chat POST)
```
Usuario hace pregunta
  → Chatbot.responder(pregunta)
    → VectorStore.cargar(embeddings)
      → Carga vectores de FAISS
    → Cadena RAG busca contexto similar
    → LLM (Gemini) responde con identidad del bot
    → Devuelve respuesta
```

## Componentes

### loaders.py
- **cargar_pdf()**: Lee archivos PDF con pypdf
- **cargar_txt()**: Lee archivos de texto plano
- **cargar_docx()**: Lee documentos Word con python-docx
- **cargar_archivo()**: Detecta tipo y carga automáticamente

### embeddings.py
- Usa `HuggingFaceEmbeddings` con modelo "all-MiniLM-L6-v2"
- Vectores de 384 dimensiones
- Función `__call__()` para acceder al modelo

### data/vectorstores/vectorstore.py
- **guardar()**: Crea índice FAISS y lo persiste
- **cargar()**: Carga índice FAISS existente
- Permite búsqueda semántica de documentos

### LangChain.py
- **configurar_cadena_rag()**: Configura la cadena RAG
- Carga identidad_bot.txt como instrucciones
- Usa `ChatGoogleGenerativeAI` (Gemini 1.5 Flash)
- Recupera top 3 documentos similares
- Usa `RetrievalQA` para responder basado en contexto

### chatbot.py
- **Clase Chatbot**: Orquesta todos los componentes
- `__init__()`: Inicializa loader, embeddings, vectorstore
- `cargar_documento()`: Procesa y almacena documentos
- `responder()`: Busca contexto y genera respuesta

### main.py
- **API REST con Flask**
- Ruta `/upload` (POST): Carga documentos
- Ruta `/chat` (POST): Responde preguntas
- Puerto: 5000
- Precarga el bot con identidad al iniciar

## Endpoints API

### POST /upload
```json
Request:
{
  "archivo": <archivo.pdf|txt|docx>
}

Response:
{
  "mensaje": "Documento procesado"
}
```

### POST /chat
```json
Request:
{
  "pregunta": "¿Qué es Python?"
}

Response:
{
  "respuesta": "Python es un lenguaje de programación..."
}
```

## Variables de Entorno Requeridas

- `GOOGLE_API_KEY`: Para autenticar con Gemini API

## Dependencias

- flask
- langchain
- langchain-community
- langchain-google-generativeai
- langchain-huggingface
- faiss-cpu (o faiss-gpu)
- pypdf
- python-docx
- sentence-transformers

## Ejecución

```bash
cd app
python main.py
```

API estará disponible en: `http://localhost:5000`

## Cambios Realizados

1. ✓ Corregido import de VectorStore en chatbot.py
2. ✓ Agregado sys.path a main.py para importaciones relativas
3. ✓ Cambio de `chain.run()` a `chain.invoke()` en chatbot.py
4. ✓ Precarga de bot con identidad en main.py
5. ✓ Limpieza de formato en embeddings.py
6. ✓ Creado notebook de prueba

## Verificación

Ejecuta `test_notebook.ipynb` para verificar:
- ✓ Carga de archivos de identidad
- ✓ Creación de embeddings
- ✓ Almacenamiento en vector store
- ✓ Configuración de cadena RAG
- ✓ Integración del chatbot
