from unittest.mock import patch

from src.rag_chain import answer_question


@patch("src.rag_chain.retrieve_chunks")
def test_out_of_corpus(mock_retrieve):

    # Simulate no retrieved chunks
    mock_retrieve.return_value = []

    response = answer_question(
        "What is Alzheimer's disease?"
    )
    print(response)
    assert response["answer"] == "I could not find this in the available literature."
    assert response["citations"] == []
    assert response["confidence"] == "low"