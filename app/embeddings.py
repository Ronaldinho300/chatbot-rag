# Crear los embeddings (vectores numéricos) del texto.# app/embeddings.py

from langchain_huggingface import (
    HuggingFaceEmbeddings
)


class Embeddings:


    def __init__(self):

        self.modelo = (

            HuggingFaceEmbeddings(

                model_name=

                "sentence-transformers/all-MiniLM-L6-v2"

            )

        )



    def texto_a_vector(

            self,

            texto):


        vector = (

            self.modelo.embed_query(

                texto

            )

        )


        return vector



    def textos_a_vectores(

            self,

            textos):


        vectores = (

            self.modelo.embed_documents(

                textos

            )

        )


        return vectores