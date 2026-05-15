# carga la con gemini ,orquestar internamente el flujo entre LLM + recuperación + memoria + prompts
from langchain_google_generativeai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

def configurar_cadena_rag(vector_db):
    # 1. Cargamos la identidad desde el archivo TXT
    try:
        with open('app/data/identidad_bot.txt', 'r', encoding='utf-8') as f:
            instrucciones_bot = f.read()
    except FileNotFoundError:
        # Por si el archivo no existe, dejamos un respaldo
        instrucciones_bot = "Eres un asistente experto."

    # 2. Creamos el Template usando las instrucciones cargadas
    template = f"""{instrucciones_bot}
    
    Contexto: {{context}}
    Pregunta: {{question}}
    
    Respuesta útil:"""
    
    PROMPT = PromptTemplate(
        template=template, input_variables=["context", "question"]
    )

    # 3. Configuramos el LLM y la cadena
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    return chain