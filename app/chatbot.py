# Orquestar todo usando LangChain.
# Pregunta usuario

#↓
#Usa loaders.py (si necesita documentos)
#↓
#Usa embeddings.py
#↓
#Usa vectorstore.py
#↓
#Usa LangChain.py
#↓
#Genera respuesta 
# app/chatbot.py

from loaders import Loader
from embeddings import Embeddings
from vectorstore import VectorStore
from LangChain import LangChainConfig


class Chatbot:


    def __init__(self):

        self.loader = Loader()

        self.embedding = Embeddings()

        self.vectorstore = VectorStore()

        self.langchain = LangChainConfig()


        # personalidad fija bot

        with open(

            "data/identidad_bot.txt",

            "r",

            encoding="utf-8"

        ) as archivo:


            self.identidad = (

                archivo.read()

            )



    def cargar_documento(

            self,

            ruta_documento,

            nombre_vectorstore="documento"):


        texto = (

            self.loader.cargar_archivo(

                ruta_documento

            )

        )


        self.vectorstore.guardar(

            textos=[texto],

            embeddings=self.embedding,

            nombre=nombre_vectorstore

        )


        return (

            "Documento procesado"

        )



    def responder(

            self,

            pregunta,

            nombre_vectorstore="documento"):



        db = (

            self.vectorstore.cargar(

                self.embedding,

                nombre_vectorstore

            )

        )


        contexto = (

            self.vectorstore.buscar(

                db,

                pregunta

            )

        )


        respuesta = (

            self.langchain.generar_respuesta(

                pregunta=pregunta,

                contexto=contexto,

                personalidad=self.identidad

            )

        )


        self.guardar_historial(

            pregunta,

            respuesta

        )


        return respuesta



    def guardar_historial(

            self,

            pregunta,

            respuesta):


        with open(

            "history/conversaciones/chat.txt",

            "a",

            encoding="utf-8"

        ) as archivo:



            archivo.write(

f"""

Usuario:

{pregunta}


Bot:

{respuesta}


------------------------

"""

            )