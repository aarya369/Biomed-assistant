### Loader Comparison

Two loaders were evaluated on the PubMed corpus:

**1. PyMuPDF (fitz)**

* Fast PDF loading and text extraction.
* Preserved page boundaries, which is important for later citation generation.
* Successfully extracted text from all documents.
* However, several PDFs produced heavily garbled text due to font encoding and image-based content.

**2. pdfplumber (Layout-Aware Loader)**

* Chosen because it is designed to preserve document structure and tables better than standard PDF text extraction tools.
* Successfully processed the documents.
* For the problematic PDFs, the extracted text remained garbled and showed no significant improvement over PyMuPDF.
* Did not recover meaningful structure from the affected documents.

**Comparison Results**

| Criterion                        | PyMuPDF | pdfplumber |
| -------------------------------- | ------- | ---------- |
| Processing Speed                 | Better  | Slower     |
| Page-Level Extraction            | Yes     | Yes        |
| Table/Layout Awareness           | Limited | Better     |
| Text Quality on Clean PDFs       | Good    | Good       |
| Text Quality on Problematic PDFs | Poor    | Poor       |
| Ease of Integration              | Better  | Moderate   |

For the provided corpus, the main limitation was the quality and encoding of the source PDFs rather than the extraction library itself. Both loaders performed similarly on problematic documents.
### Decision Journal – Loader Selection

**Decision:** Use PyMuPDF as the primary document loader.

**Alternatives Evaluated:** pdfplumber, pymupdf4llm, and unstructured.

**Evidence:**

* PyMuPDF successfully extracted page-by-page text from all documents.
* It preserved page numbers, which are required for citation grounding later in the project.
* pdfplumber produced extraction quality similar to PyMuPDF on the provided corpus.
* pymupdf4llm and unstructured did not significantly improve extraction quality for the problematic PDFs.
* Several PDFs contained image-heavy content or problematic font encodings, causing garbled text regardless of the extraction library used.

**Rationale:**
The observed failures were primarily caused by document quality rather than the loader. Since PyMuPDF provided comparable extraction quality while being faster, simpler, and easier to integrate, it was selected as the primary loader.

**Fallback Strategy:**
For future documents that contain complex tables or layouts, pdfplumber can be used as a fallback loader for targeted extraction and debugging.
### Raw Document Persistence

All processed documents were stored in `outputs/documents.json`.

Each document contains:

* document_id
* title
* authors
* source_url
* year
* page-by-page extracted text

Persisting the parsed documents avoids repeated PDF parsing during later stages such as chunking, embedding generation, retrieval, and evaluation.
