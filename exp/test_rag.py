from src.rag_chain import answer_question

question = "Tell me everything about intra vaginal rings"

print(question)
response = answer_question(question)
print("\nRESPONSE:\n")
print(response)