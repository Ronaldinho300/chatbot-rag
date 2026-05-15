# app/main.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import tempfile  # 🆕 para manejo de archivos temporales

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
# Configurar CORS (CORREGIDO)
# ==========================
# Permite cualquier origen, método y header
CORS(app, resources={r"/*": {"origins": "*"}})

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
# HEALTH CHECK (mejorado)
# ==========================
@app.route("/health", methods=["GET"])
def health():
    try:
        bot_instance = obtener_bot()
        bot_ready = bot_instance is not None
    except Exception:
        bot_ready = False
    return jsonify({"status": "healthy", "chatbot": bot_ready}), 200

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
# SUBIR ARCHIVO (CORREGIDO con tempfile)
# ==========================
@app.route("/upload", methods=["POST"])
def upload():
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

        # Guardar el archivo en un temporal (evita 502 por disco)
        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp:
            archivo.save(tmp.name)
            tmp_path = tmp.name

        nombre_base = os.path.splitext(archivo.filename)[0]

        try:
            chatbot.cargar_documento(tmp_path, nombre=nombre_base)
        finally:
            # Limpiar: borrar el archivo temporal después de procesarlo
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

        return jsonify({
            "mensaje": "Documento cargado",
            "archivo": archivo.filename
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================
# CHAT
# ==========================
@app.route("/chat", methods=["POST"])
def chat():
    try:
        chatbot = obtener_bot()

        datos = request.get_json()
        if not datos:
            return jsonify({"error": "JSON vacío"}), 400

        pregunta = datos.get("pregunta", "").strip()
        if pregunta == "":
            return jsonify({"error": "Pregunta vacía"}), 400

        documento = datos.get("documento", "documento")

        respuesta = chatbot.responder(pregunta, nombre=documento)

        return jsonify({
            "pregunta": pregunta,
            "respuesta": respuesta
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================
# ERROR 404
# ==========================
@app.errorhandler(404)
def error404(e):
    return jsonify({"error": "Ruta no encontrada"}), 404

# ==========================
# ERROR 500
# ==========================
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