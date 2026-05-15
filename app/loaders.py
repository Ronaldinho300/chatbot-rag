# Leer documentos. Puede cargar:PDF, TXT, DOCX
# app/loaders.py

from pypdf import PdfReader
from docx import Document


class Loader:


    def cargar_pdf(
            self,
            ruta):

        texto = ""


        pdf = PdfReader(
            ruta
        )


        for pagina in pdf.pages:

            texto += (
                pagina.extract_text()
                + "\n"
            )


        return texto


    def cargar_txt(
            self,
            ruta):


        with open(

            ruta,

            "r",

            encoding="utf-8"

        ) as archivo:


            return archivo.read()



    def cargar_docx(
            self,
            ruta):


        doc = Document(
            ruta
        )


        texto = "\n".join(

            p.text

            for p in doc.paragraphs

        )


        return texto



    def cargar_archivo(
            self,
            ruta):


        if ruta.endswith(".pdf"):

            return self.cargar_pdf(
                ruta
            )


        elif ruta.endswith(".txt"):

            return self.cargar_txt(
                ruta
            )


        elif ruta.endswith(".docx"):

            return self.cargar_docx(
                ruta
            )


        else:

            raise ValueError(

                "Formato no soportado"

            )