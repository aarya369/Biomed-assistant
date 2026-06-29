import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

from src.prompts import GROUNDING_PROMPT
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    api_key=groq_api_key,
    model="llama-3.3-70b-versatile",
    temperature=0
)
grounding_chain = (
    GROUNDING_PROMPT
    | llm
    | StrOutputParser()
)

def grounding_check(question, answer, context):
    response = grounding_chain.invoke(
        {
            "question": question,
            "answer": answer,
            "context": context
        }
    )
    return response.strip().upper()