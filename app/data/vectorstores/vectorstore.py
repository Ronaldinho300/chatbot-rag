#Guardar embeddings y hacer búsqueda semántica.
# app/vectorstore.py# app/vectorstore.py
# app/vectorstore.py

from langchain_community.vectorstores import FAISS

import os



class VectorStore:



    def guardar(

            self,

            textos,

            embeddings,

            nombre):



        db = (

            FAISS.from_texts(

                textos,

                embeddings.modelo

            )

        )


        ruta = (

f"app/data/vectorstores/{nombre}"

        )


        db.save_local(

            ruta

        )


        return db



    def cargar(

            self,

            embeddings,

            nombre):



        ruta = (

f"app/data/vectorstores/{nombre}"

        )


        if not os.path.exists(

                ruta):


            return None



        return (

            FAISS.load_local(

                ruta,

                embeddings.modelo,

                allow_dangerous_deserialization=True

            )

        )