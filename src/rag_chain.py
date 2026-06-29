

import os, json
import uuid
from src.retriever import retrieve_chunks
from src.prompts import SYSTEM_PROMPT
from src.input_guardrails import validate_input
from src.citation_validator import validate_citations
from src.grounding_checker import grounding_check
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import time

# Load variables from .env
# Load variables from .env
load_dotenv()
def get_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile",
        temperature=0
    )

def clean_context_text(text):
    return "".join(
        char for char in text
        if char == "\n" or char == "\t" or ord(char) >= 32
    )

def save_trace(trace):
    os.makedirs("traces", exist_ok = True)
    filepath = os.path.join("traces",f"{trace['trace_id']}.json")
    with open(filepath, "w", encoding = "utf-8") as f:
        json.dump(trace, f, indent = 4, ensure_ascii = False)

def answer_question(question):
    trace_id = str(uuid.uuid4())
    trace = {
        "trace_id": trace_id,
        "question": question,
        "latency": {},
        "retrieved_chunks": []
    }
    total_start = time.perf_counter()

    # Step 1: Retrieve relevant chunks
    try:
        validate_input(question)
    except ValueError as e:
        trace["latency"]["total"] = time.perf_counter() - total_start
        save_trace(trace)
        return str(e)
    
    retrieve_start = time.perf_counter()
    chunks = retrieve_chunks(question, k = 10)
    retrieve_time = time.perf_counter() - retrieve_start
    trace["latency"] = {
        "retrieve": retrieve_time
    }
    trace["retrieved_chunks"] = chunks
    THRESHOLD = 0.6
    if(len(chunks) == 0) or chunks[0]["distance"] > THRESHOLD:
        trace["latency"]["total"] = time.perf_counter() - total_start
        save_trace(trace)
        return {
            "answer": "I could not find this in the available literature.",
            "citations": [],
            "confidence": "low"
        }

    context = ""
    for chunk in chunks:
        content = clean_context_text(chunk["text"])
        context += f"""
        Document Title: {chunk["metadata"]["document_title"]}
        Page Number: {chunk["metadata"]["page_number"]}
        Chunk Index: {chunk["metadata"]["chunk_index"]}
        Content: {content}
        ----------------------------------------
        """

    human_prompt = f"""Retrieved context: {context} , Question: {question}"""
    trace["prompt"] = {
        "system": SYSTEM_PROMPT,
        "user": human_prompt
    }
    llm = get_llm()
    for i in range(2):
        generate_start = time.perf_counter()
        response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=human_prompt),
    ])
        usage = response.response_metadata.get("token_usage", {})

        trace["cost"] = {
            "input_tokens": usage.get("prompt_tokens", 0),
            "output_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "dollar_cost": 0.0
            }
        print(trace["cost"])
        generate_time = time.perf_counter() - generate_start
        trace["latency"]["generate"] = generate_time
        try:
            response_json = json.loads(response.content)
            trace["llm_response"] = response_json
        except json.JSONDecodeError:
            if i == 0:
                continue
            else:
                trace["latency"]["total"] = time.perf_counter() - total_start
                save_trace(trace)
                return {
            "answer": "The model returned an invalid response format.",
            "citations": [],
            "confidence": "low"
        }
        try:
            validate_citations(response_json)
        except ValueError:
            trace["latency"]["total"] = time.perf_counter() - total_start
            save_trace(trace)
            return {
                "answer": "Response rejected since no citations were given",
                "citations": [],
                "confidence": "low"
        }

        ground_start = time.perf_counter()
        status = grounding_check(question,response_json["answer"],context)
        ground_time = time.perf_counter() - ground_start
        trace["latency"]["grounding"] = ground_time
        trace["grounding_verdict"] = status
        if status == "GROUNDED":
            response_json["retrieved_chunks"] = chunks
            response_json["trace_id"] = trace_id
            trace["latency"]["total"] = time.perf_counter() - total_start
            save_trace(trace)
            
            return response_json
        elif status == "PARTIAL":
            response_json["retrieved_chunks"] = chunks
            response_json["trace_id"] = trace_id
            response_json["answer"] = ("The answer is only partially supported by the retrieved literature.\n\n" + response_json["answer"])
            response_json["confidence"] = "medium"
            trace["latency"]["total"] = time.perf_counter() - total_start
            save_trace(trace)
            return response_json
        else:
            if i == 0:
                continue
            else:
                trace["latency"]["total"] = time.perf_counter() - total_start
                save_trace(trace)
                return {
                    "answer": "The generated answer could not be verified against the retrieved literature.",
                    "citations": [],
                    "confidence": "low"
                    }


    



   
