#Guardar embeddings y hacer búsqueda semántica.
# app/vectorstore.py# app/vectorstore.py

from langchain_community.vectorstores import FAISS

import os


class VectorStore:


    def guardar(

            self,

            textos,

            embeddings,

            nombre):


        db = FAISS.from_texts(

            texts=textos,

            embedding=embeddings.modelo

        )


        ruta = (

            f"data/vectorstores/{nombre}"

        )


        db.save_local(

            ruta

        )


        return ruta



    def cargar(

            self,

            embeddings,

            nombre):


        ruta = (

            f"data/vectorstores/{nombre}"

        )


        if not os.path.exists(

                ruta):


            return None


        db = FAISS.load_local(

            ruta,

            embeddings.modelo,

            allow_dangerous_deserialization=True

        )


        return db



    def buscar(

            self,

            db,

            pregunta,

            k=3):


        resultados = (

            db.similarity_search(

                pregunta,

                k=k

            )

        )


        return resultados