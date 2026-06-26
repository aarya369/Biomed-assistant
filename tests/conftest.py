import pytest
@pytest.fixture
def sample_chunk():
    return {
        "id": "1",
        "text": "Amoxicillin is an antibiotic.",
        "metadata": {
            "document_id": "doc1",
            "page_number": 1,
            "chunk_index": 0
        },
        "distance": 0.9
    }
