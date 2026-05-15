# Crear los embeddings (vectores numéricos) del texto.
# app/embeddings.py

import fasttext
import numpy as np


class Embeddings:

    def __init__(self,
                 model_path="models/cc.es.300.bin"):

        """
        Carga modelo FastText
        una sola vez
        """

        self.model = fasttext.load_model(
            model_path
        )


    def texto_a_vector(
            self,
            texto):

        """
        Convierte texto
        → embedding promedio
        """

        palabras = texto.split()


        if not palabras:

            return np.zeros(
                self.model.get_dimension()
            )


        vectores = [

            self.model.get_word_vector(
                palabra
            )

            for palabra in palabras

        ]


        embedding = np.mean(

            vectores,

            axis=0

        )


        return embedding.tolist()