# app/main.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import tempfile

# ==========================
# Cargar variables .env
# ==========================
load_dotenv()

# ==========================
# Import chatbot
# ==========================
from chatbot import Chatbot

# ==========================
# Crear aplicación Flask
# ==========================
app = Flask(__name__)

# ==========================
# CONFIGURAR CORS
# ✅ FIX: Se usa flask_cors con origins="*" para evitar
#    bloqueos en Render (el proxy ya gestiona TLS).
#    Si se quiere restringir, cambiar "*" por la URL exacta
#    del frontend y asegurarse de que coincida byte a byte.
# ==========================
CORS(
    app,
    origins="*",
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=False   # ← DEBE ser False cuando origins="*"
)

# ==========================
# Headers manuales CORS
# ✅ FIX: Un solo origen, sin duplicar con flask_cors.
#    Se responde "*" para máxima compatibilidad en Render.
# ==========================
@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response

# ==========================
# Configuración uploads
# ==========================
UPLOAD_FOLDER = os.path.abspath(
    os.getenv("UPLOAD_FOLDER", "app/data/uploads")
)

MAX_CONTENT_LENGTH = int(
    os.getenv("MAX_CONTENT_LENGTH", 52428800)
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

# ==========================
# Lazy loading chatbot
# ==========================
bot = None

def obtener_bot():
    global bot
    if bot is None:
        print("[INFO] Inicializando chatbot...")
        bot = Chatbot()
        print("[INFO] Chatbot listo")
    return bot

# ==========================
# HEALTH CHECK
# ==========================
@app.route("/health", methods=["GET", "OPTIONS"])
def health():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200
    try:
        bot_instance = obtener_bot()
        bot_ready = bot_instance is not None
    except Exception as e:
        print("[ERROR HEALTH]", str(e))
        bot_ready = False

    return jsonify({
        "status": "healthy",
        "chatbot": bot_ready
    }), 200

# ==========================
# INDEX
# ==========================
@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "nombre": "Chatbot RAG API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "upload": "/upload",
            "chat": "/chat"
        }
    }), 200

# ==========================
# SUBIR ARCHIVO
# ==========================
@app.route("/upload", methods=["POST", "OPTIONS"])
def upload():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    try:
        chatbot = obtener_bot()

        if "archivo" not in request.files:
            return jsonify({"error": "Archivo no enviado"}), 400

        archivo = request.files["archivo"]

        if archivo.filename == "":
            return jsonify({"error": "Archivo vacío"}), 400

        extensiones = {".pdf", ".txt", ".docx"}
        extension = os.path.splitext(archivo.filename)[1].lower()

        if extension not in extensiones:
            return jsonify({"error": "Formato no permitido"}), 400

        # Archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp:
            archivo.save(tmp.name)
            tmp_path = tmp.name

        nombre_base = os.path.splitext(archivo.filename)[0]

        try:
            chatbot.cargar_documento(tmp_path, nombre=nombre_base)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        return jsonify({
            "mensaje": "Documento cargado",
            "archivo": archivo.filename
        }), 200

    except Exception as e:
        print("[ERROR UPLOAD]", str(e))
        return jsonify({"error": str(e)}), 500

# ==========================
# CHAT
# ==========================
@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    try:
        print("[INFO] Petición /chat")
        chatbot = obtener_bot()
        datos = request.get_json()
        print("[INFO] Datos:", datos)

        if not datos:
            return jsonify({"error": "JSON vacío"}), 400

        pregunta = datos.get("pregunta", "").strip()

        if pregunta == "":
            return jsonify({"error": "Pregunta vacía"}), 400

        # documento es opcional: si no viene, el bot responde
        # sólo con su identidad (sin RAG)
        documento = datos.get("documento", None)

        respuesta = chatbot.responder(pregunta, nombre=documento)

        return jsonify({
            "pregunta": pregunta,
            "respuesta": respuesta
        }), 200

    except Exception as e:
        print("[ERROR CHAT]", str(e))
        return jsonify({"error": str(e)}), 500

# ==========================
# ERROR 404 / 500
# ==========================
@app.errorhandler(404)
def error404(e):
    return jsonify({"error": "Ruta no encontrada"}), 404

@app.errorhandler(500)
def error500(e):
    return jsonify({"error": "Error interno servidor"}), 500

# ==========================
# EJECUTAR
# ==========================
if __name__ == "__main__":
    debug = os.getenv("FLASK_ENV", "production") == "development"
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=debug
    )