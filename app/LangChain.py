# carga la con gemini ,orquestar internamente el flujo entre LLM + recuperación + memoria + prompts
from langchain_google_generativeai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

def configurar_cadena_rag(vector_db):
    # 1. Configuramos el Modelo de Lenguaje (LLM)
    # Usamos Gemini 1.5 Flash por su rapidez y precisión
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

    # 2. Creamos un "Prompt" personalizado (Instrucciones para la IA)
    template = """Eres un asistente experto de SENATI. Utiliza únicamente el siguiente contexto para responder la pregunta. 
    Si no sabes la respuesta, di que no lo sabes, no inventes información.
    
    Contexto: {context}
    Pregunta: {question}
    
    Respuesta útil y técnica:"""
    
    PROMPT = PromptTemplate(
        template=template, input_variables=["context", "question"]
    )

    # 3. Orquestamos el flujo con RetrievalQA
    # Esto une el LLM + El Recuperador (Base Vectorial) + El Prompt
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 3}), # Recupera los 3 fragmentos más relevantes
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    return chain