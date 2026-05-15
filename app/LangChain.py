# app/LangChain.py
import google.generativeai as genai
import os

def configurar_cadena_rag(vector_db):
    """Configura la cadena RAG con búsqueda semántica simple"""
    
    # Ruta absoluta al archivo de identidad (dentro del paquete app)
    base_dir = os.path.dirname(__file__)
    ruta_identidad = os.path.join(base_dir, "data", "identidad_bot.txt")
    
    try:
        with open(ruta_identidad, "r", encoding="utf-8") as archivo:
            instrucciones = archivo.read()
    except FileNotFoundError:
        instrucciones = "Eres un asistente útil."
    
    # Configurar API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
    
    class CadenaRAG:
        """Cadena RAG simple sin RetrievalQA"""
        
        def __init__(self, vector_db, instrucciones):
            self.vector_db = vector_db
            self.instrucciones = instrucciones
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        
        def run(self, pregunta):
            """Ejecutar consulta RAG"""
            try:
                docs = self.vector_db.similarity_search(pregunta, k=3)
                contexto = "\n".join([doc.page_content for doc in docs])
                
                prompt = f"""{self.instrucciones}

Contexto:
{contexto}

Pregunta:
{pregunta}

Respuesta:
"""
                response = self.model.generate_content(prompt)
                return response.text if response else "No se pudo generar respuesta"
            except Exception as e:
                return f"Error: {str(e)}"
        
        def invoke(self, inputs):
            """Compatibilidad con LangChain"""
            query = inputs.get("query", "")
            return {"result": self.run(query)}
    
    return CadenaRAG(vector_db, instrucciones)