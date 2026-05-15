# Envía respuesta:
# app/main.py

from flask import (
    Flask,
    request,
    jsonify
)

import os

from chatbot import Chatbot


app = Flask(__name__)

bot = Chatbot()


UPLOAD_FOLDER = (

    "data/uploads"

)


os.makedirs(

    UPLOAD_FOLDER,

    exist_ok=True

)


@app.route(

    "/upload",

    methods=["POST"]

)

def upload():


    archivo = (

        request.files["archivo"]

    )


    ruta = (

        os.path.join(

            UPLOAD_FOLDER,

            archivo.filename

        )

    )


    archivo.save(

        ruta

    )


    respuesta = (

        bot.cargar_documento(

            ruta

        )

    )


    return jsonify(

        {

            "mensaje":

            respuesta

        }

    )



@app.route(

    "/chat",

    methods=["POST"]

)

def chat():


    datos = (

        request.json

    )


    pregunta = (

        datos["pregunta"]

    )


    respuesta = (

        bot.responder(

            pregunta

        )

    )


    return jsonify(

        {

            "respuesta":

            respuesta

        }

    )



@app.route(

    "/history",

    methods=["GET"]

)

def history():


    ruta = (

        "history/conversaciones/chat.txt"

    )


    if not os.path.exists(

            ruta):


        return jsonify(

            {

                "historial":

                ""

            }

        )



    with open(

        ruta,

        "r",

        encoding="utf-8"

    ) as archivo:


        historial = (

            archivo.read()

        )


    return jsonify(

        {

            "historial":

            historial

        }

    )



if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )