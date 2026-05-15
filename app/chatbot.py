# app/chatbot.py

from loaders import Loader
from embeddings import Embeddings
from data.vectorstores.vectorstore import VectorStore
from LangChain import configurar_cadena_rag



class Chatbot:


    def __init__(self):


        self.loader = Loader()

        self.embedding = Embeddings()

        self.store = VectorStore()



    def cargar_documento(

            self,

            ruta,

            nombre="documento"):



        texto = (

            self.loader.cargar_archivo(

                ruta

            )

        )


        db = (

            self.store.guardar(

                textos=[texto],

                embeddings=self.embedding,

                nombre=nombre

            )

        )


        return db




    def responder(

            self,

            pregunta,

            nombre="documento"):



        vector_db = (

            self.store.cargar(

                self.embedding,

                nombre

            )

        )


        chain = (

            configurar_cadena_rag(

                vector_db

            )

        )


        respuesta = (

            chain.run(

                pregunta

            )

        )


        return respuesta