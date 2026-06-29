import re, os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from src.prompts import SECURITY_PROMPT, OFFTOPIC_PROMPT
load_dotenv()


groq_api_key = os.getenv("GROQ_API_KEY")

# Load the LLM
llm = ChatGroq(
    api_key=groq_api_key,
    model="llama-3.1-8b-instant",
    temperature=0
)
security_chain = (SECURITY_PROMPT | llm | StrOutputParser())
def llm_security_check(question):
    response = security_chain.invoke(
        {"question": question}
    )
    response = response.strip().upper()
    if response == "UNSAFE":
        raise ValueError("Unsafe input detected")
    return True

offtopic_chain = (OFFTOPIC_PROMPT | llm | StrOutputParser())
def off_topic_check(question):
    response = offtopic_chain.invoke(
        {"question": question}
    )
    response = response.strip().upper()
    if response == "OUT_OF_SCOPE":
        raise ValueError("Question is out of scope")
    return True

PROMPT_INJECTION = [

    "ignore previous",
    "ignore all",
    "ignore prior",
    "forget previous",
    "forget all",

    "system prompt",
    "developer prompt",
    "hidden prompt",
    "internal prompt",

    "reveal prompt",
    "show prompt",

    "list all chunks",
    "list every chunk",
    "show all chunks",
    "dump all chunks",

    "print context",
    "print retrieved context",

    "override instructions",
    "bypass instructions",
]
def detect_injection(question):
    q = question.lower()
    for pattern in PROMPT_INJECTION:
        if pattern in q:
            raise ValueError("Prompt injection detected")
    return True

JAILBREAK = [

    "pretend you are",
    "act as",
    "roleplay as",

    "without restrictions",
    "without limitations",
    "without safeguards",

    "ignore safety",
    "disable safety",
    "disable guardrails",

    "you are now",
    "new role",

    "jailbreak",
    "bypass safety",

    "do anything",

    "developer mode",
    "god mode"

]
def detect_jailbreak(question):
    q = question.lower()
    for pattern in JAILBREAK:
        if pattern in q:
            raise ValueError("Jailbreak attempt detected")
    return True

def validate_input(question):
    detect_injection(question)
    detect_jailbreak(question)
    llm_security_check(question)
    off_topic_check(question)

    return True
