from rag_chain import answer_question

question = "Tell me the names of  all the courses in which Aarya Mehta got 'B' grade "

print(question)
response = answer_question(question)
print("\nRESPONSE:\n")
print(response)