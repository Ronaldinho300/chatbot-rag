# app/LangChain.py

from langchain_google_generativeai import (
    ChatGoogleGenerativeAI
)

from langchain.chains import (
    RetrievalQA
)

from langchain.prompts import (
    PromptTemplate
)



def configurar_cadena_rag(

        vector_db):


    try:

        with open(

            "app/data/identidad_bot.txt",

            "r",

            encoding="utf-8"

        ) as archivo:


            instrucciones = (

                archivo.read()

            )


    except:

        instrucciones = (

            "Eres un asistente."

        )



    template = f"""

{instrucciones}


Contexto:

{{context}}


Pregunta:

{{question}}


Respuesta:

"""


    prompt = PromptTemplate(

        template=template,

        input_variables=[

            "context",

            "question"

        ]

    )



    llm = (

        ChatGoogleGenerativeAI(

            model=

            "gemini-1.5-flash",

            temperature=0

        )

    )



    chain = (

        RetrievalQA.from_chain_type(

            llm=llm,

            chain_type="stuff",

            retriever=

            vector_db.as_retriever(

                search_kwargs={

                    "k":3

                }

            ),

            chain_type_kwargs={

                "prompt":

                prompt

            }

        )

    )


    return chain