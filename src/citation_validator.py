def validate_citations(response):
    
    answer = response.get("answer", "").strip()
    citations = response.get("citations", [])

    if (
        answer
        and answer.lower() != "i don't know based on the provided context."
        and len(citations) == 0
    ):
        raise ValueError(
            "Answer rejected because it contains no citations."
        )

    return True