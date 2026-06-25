
from retriever import retrieve_chunks
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

# Load variables from .env
load_dotenv()

# Read the API key
groq_api_key = os.getenv("GROQ_API_KEY")

# Load the LLM
llm = ChatGroq(
    api_key=groq_api_key,
    model="llama-3.3-70b-versatile",
    temperature=0
)

SYSTEM_PROMPT = """You are a biomedical research assistant.
Answer the user's question using ONLY the retrieved context provided by the user.
Do not use your own knowledge.
If the retrieved context does not contain enough information to answer the question, reply exactly:
"I don't know based on the provided context."
Do not guess, infer, or use outside knowledge.

Return ONLY a valid JSON object.
Do not include markdown.
Do not include ```json.
Do not include any explanation outside the JSON.

Your response MUST contain exactly these fields:
1. answer: a string containing the answer.
2. citations: a list of objects with document_id, page_number, and chunk_index.
3. confidence: exactly one of low, medium, high.
Only include citations for chunks actually used to answer the question.
Do not use the field name citation. Always use citations."""


def clean_context_text(text):
    return "".join(
        char for char in text
        if char == "\n" or char == "\t" or ord(char) >= 32
    )


def answer_question(question):

    # Step 1: Retrieve relevant chunks
    chunks = retrieve_chunks(question)

    context = ""
    for chunk in chunks:
        content = clean_context_text(chunk["text"])
        context += f"""
        Document ID: {chunk["metadata"]["document_id"]}
        Page Number: {chunk["metadata"]["page_number"]}
        Chunk Index: {chunk["metadata"]["chunk_index"]}
        Content:
{content}
        ----------------------------------------
"""

    human_prompt = f"""Retrieved context:
{context}

Question:
{question}"""

    # print("=" * 80)
    # print("SYSTEM MESSAGE:")
    # print(SYSTEM_PROMPT)
    # print("\nHUMAN MESSAGE:")
    # print(human_prompt)
    # print("=" * 80)

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=human_prompt),
    ])
    return response.content

    # # Step 4: Ask the LLM
    # print("=" * 100)
    # print("FINAL PROMPT")
    # print(prompt)
    # print("=" * 100)
    
    # print("\nRAW RESPONSE:")
    # print(response.content)
    # print("=" * 80)

    # match = re.search(r"\{.*\}", response.content, re.DOTALL)

#     if not match:
#         raise ValueError("No JSON object found in LLM response.")

#     response_json = json.loads(match.group())
#     validated_response = RAGResponse.model_validate(
#     response_json
# )

    



   
