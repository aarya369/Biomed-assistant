from unittest.mock import MagicMock, patch

from src.rag_chain import answer_question
@patch("src.rag_chain.grounding_check")
@patch("src.rag_chain.validate_citations")
@patch("src.rag_chain.retrieve_chunks")
@patch("src.rag_chain.llm")
def test_mock_llm(
    mock_llm,
    mock_retrieve,
    mock_validate,
    mock_grounding,
    sample_chunk
):
    mock_retrieve.return_value = [sample_chunk]

    mock_grounding.return_value = "GROUNDED"

    mock_response = MagicMock()
    mock_response.content = """
    {
        "answer": "Amoxicillin is an antibiotic.",
        "citations": [
            {
                "document_id":"doc1",
                "page_number":1,
                "chunk_index":0
            }
        ],
        "confidence":"high"
    }
    """

    mock_response.response_metadata = {
        "token_usage": {}
    }

    mock_llm.invoke.return_value = mock_response

    response = answer_question(
        "What is amoxicillin?"
    )

    assert response["answer"] == "Amoxicillin is an antibiotic."