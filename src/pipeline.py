from src.loader import build_documents
from src.prepare_embeddings import main as prepare_embeddings
from src.build_vector_store import build_vector


def run_ingestion_pipeline():
    """Run the complete ingestion pipeline."""

    print("=" * 60)
    print("Biomedical Assistant - Document Ingestion Pipeline")
    print("=" * 60)

    try:
        print("\n[1/3] Processing PDF documents...")
        build_documents()

        print("\n[2/3] Generating embeddings...")
        prepare_embeddings()

        print("\n[3/3] Building vector database...")
        build_vector()

        print("\n✅ Ingestion completed successfully!")
        print("The corpus is now ready for querying.")

    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    run_ingestion_pipeline()