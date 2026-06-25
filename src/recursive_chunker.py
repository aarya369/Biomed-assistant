import json
from langchain_text_splitters import RecursiveCharacterTextSplitter

INPUT_FILE = "outputs/documents.json"
OUTPUT_FILE = "outputs/recursive_chunks.json"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
splitter = RecursiveCharacterTextSplitter(
    chunk_size = CHUNK_SIZE,
    chunk_overlap = CHUNK_OVERLAP,
    separators = [
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)
with open(INPUT_FILE, "r", encoding = "utf-8") as f:
    documents = json.load(f)
all_chunks = []
for document in documents:
    document_id = document["document_id"]
    for page in document["pages"]:
        page_number = page["page_number"]
        text = page["text"]
        chunks = splitter.split_text(text)
        for idx, chunk_text in enumerate(chunks):
            all_chunks.append({
                "document_id": document_id,
                "page_number": page_number,
                "chunk_index": idx,
                "source_text": chunk_text
            })

        
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    json.dump(
        all_chunks,
        f,
        indent=2,
        ensure_ascii=False
    )

print(f"Total Recursive Chunks: {len(all_chunks)}")
print(f"Saved to: {OUTPUT_FILE}")