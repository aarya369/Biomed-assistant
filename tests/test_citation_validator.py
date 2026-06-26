import pytest

from src.citation_validator import validate_citations


def test_valid_citations():
    response = {
        "answer": "Sample answer",
        "citations": [
            {
                "document_id": "doc1",
                "page_number": 1,
                "chunk_index": 0
            }
        ],
        "confidence": "high"
    }

    # Should not raise an exception
    validate_citations(response)


def test_missing_citations():
    response = {
        "answer": "Sample answer",
        "citations": [],
        "confidence": "high"
    }

    with pytest.raises(ValueError):
        validate_citations(response)