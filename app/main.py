# app/main.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Importar chatbot
from chatbot import Chatbot


# ======================
# Cargar .env
# ======================

load_dotenv()


# ======================
# Crear app Flask
# ======================

app = Flask(__name__)


# ======================
# Configurar CORS
# ======================

CORS(

    app,

    origins=os.getenv(

        "CORS_ORIGINS",

        "*"

    ).split(",")

)


# ======================
# Configuración archivos
# ======================

UPLOAD_FOLDER = os.path.abspath(

    os.getenv(

        "UPLOAD_FOLDER",

        "app/data/uploads"

    )

)


MAX_CONTENT_LENGTH = int(

    os.getenv(

        "MAX_CONTENT_LENGTH",

        52428800

    )

)


os.makedirs(

    UPLOAD_FOLDER,

    exist_ok=True

)


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


# ======================
# Inicializar chatbot
# ======================

print(

"[INFO] Inicializando chatbot..."

)


try:


    bot = Chatbot()


    print(

        "[INFO] Chatbot listo"

    )


except Exception as e:


    print(

        f"[ERROR] {e}"

    )


    bot = None


# ======================
# HEALTH
# ======================

@app.route(

"/health",

methods=["GET"]

)

def health():

    return jsonify(

        {

            "status":

            "healthy",

            "bot_ready":

            bot is not None

        }

    ),200


# ======================
# INDEX
# ======================

@app.route(

"/",

methods=["GET"]

)

def index():

    return jsonify(

        {

            "nombre":

            "Chatbot RAG API",

            "version":

            "1.0.0",


            "endpoints":

            {

                "health":

                "/health",


                "upload":

                "/upload",


                "chat":

                "/chat"

            }

        }

    )


# ======================
# SUBIR ARCHIVOS
# ======================

@app.route(

"/upload",

methods=["POST"]

)

def upload():


    try:


        if bot is None:


            return jsonify(

                {

                    "error":

                    "Chatbot no iniciado"

                }

            ),503



        if "archivo" not in request.files:


            return jsonify(

                {

                    "error":

                    "Archivo no enviado"

                }

            ),400



        archivo = request.files[

            "archivo"

        ]



        if archivo.filename=="":


            return jsonify(

                {

                    "error":

                    "Archivo vacío"

                }

            ),400



        extensiones = {

            ".pdf",

            ".txt",

            ".docx"

        }



        extension = os.path.splitext(

            archivo.filename

        )[1].lower()



        if extension not in extensiones:


            return jsonify(

                {

                    "error":

                    "Formato no permitido"

                }

            ),400



        ruta = os.path.join(

            UPLOAD_FOLDER,

            archivo.filename

        )



        archivo.save(

            ruta

        )



        bot.cargar_documento(

            ruta,

            nombre=

            os.path.splitext(

                archivo.filename

            )[0]

        )



        return jsonify(

            {

                "mensaje":

                "Documento procesado",


                "archivo":

                archivo.filename

            }

        ),200



    except Exception as e:


        return jsonify(

            {

                "error":

                str(

                    e

                )

            }

        ),500


# ======================
# CHAT
# ======================

@app.route(

"/chat",

methods=["POST"]

)

def chat():



    try:



        if bot is None:


            return jsonify(

                {

                    "error":

                    "Chatbot no iniciado"

                }

            ),503



        datos = request.get_json()



        if not datos:


            return jsonify(

                {

                    "error":

                    "JSON vacío"

                }

            ),400



        pregunta = datos.get(

            "pregunta",

            ""

        ).strip()



        if pregunta=="":


            return jsonify(

                {

                    "error":

                    "Pregunta vacía"

                }

            ),400



        documento = datos.get(

            "documento",

            "documento"

        )



        respuesta = bot.responder(

            pregunta,

            nombre=documento

        )



        return jsonify(

            {

                "pregunta":

                pregunta,


                "respuesta":

                respuesta

            }

        ),200



    except Exception as e:


        return jsonify(

            {

                "error":

                str(

                    e

                )

            }

        ),500


# ======================
# ERRORS
# ======================

@app.errorhandler(

404

)

def error404(

e

):


    return jsonify(

        {

            "error":

            "Ruta no encontrada"

        }

    ),404



@app.errorhandler(

500

)

def error500(

e

):


    return jsonify(

        {

            "error":

            "Error servidor"

        }

    ),500


# ======================
# EJECUTAR
# ======================

if __name__=="__main__":


    debug = (

        os.getenv(

            "DEBUG",

            "False"

        ).lower()

        ==

        "true"

    )



    host = os.getenv(

        "HOST",

        "0.0.0.0"

    )



    port = int(

        os.getenv(

            "PORT",

            5000

        )

    )



    app.run(

        host=host,

        port=port,

        debug=debug

    )