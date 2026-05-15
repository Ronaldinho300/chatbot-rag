#Guardar embeddings y hacer búsqueda semántica.
# app/vectorstore.py

import numpy as np
import os


class VectorStore:


    def guardar_vectores(

            self,

            nombre,

            vectores):


        ruta = (

            f"data/vectorstores/{nombre}.npy"

        )


        np.save(

            ruta,

            vectores

        )


        return ruta



    def cargar_vectores(

            self,

            nombre):


        ruta = (

            f"data/vectorstores/{nombre}.npy"

        )


        if not os.path.exists(

                ruta):

            return None


        return np.load(

            ruta,

            allow_pickle=True

        )