import logging
import chromadb

from client.embedding_client import embedding
logger = logging.getLogger(__name__)


class VectorDBUtils:

    def __init__(self):
        self.embedding_client = embedding
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(name="printflow")

    def flatten_documents(self, documents):
        if not documents:
            return []

        if isinstance(documents, dict):
            flat_documents = []
            for file_name, chunks in documents.items():
                if not chunks:
                    continue

                for i, chunk in enumerate(chunks):
                    if hasattr(chunk, "metadata"):
                        chunk.metadata = chunk.metadata or {}
                        chunk.metadata.setdefault("file_name", file_name)
                        chunk.metadata.setdefault("chunk_id", f"{file_name}_{i}")
                    flat_documents.append(chunk)
            return flat_documents

        return list(documents)

    def add_documents(self, documents):
        try:
            documents = self.flatten_documents(documents)
            if not documents:
                logger.warning("No valid document chunks to add to Chroma.")
                return

            cleaned = []
            for index, document in enumerate(documents):
                text = getattr(document, "page_content", str(document)).strip()
                if not text:
                    continue

                metadata = dict(getattr(document, "metadata", {}) or {})
                metadata.setdefault("chunk_id", f"chunk_{index}")

                cleaned.append({
                    "id": metadata["chunk_id"],
                    "text": text,
                    "metadata": metadata,
                })

            if not cleaned:
                logger.warning("No valid document chunks to add to Chroma.")
                return

            logger.info(f"Starting embedding generation for {len(cleaned)} document chunks...")
            texts = [item["text"] for item in cleaned]
            embeddings = self.embedding_client.get_batch_embeddings(texts)

            if not embeddings or len(embeddings) != len(texts):
                raise ValueError("Embedding generation failed for the chunk list.")

            logger.info(f"Embedding generation complete. Adding {len(cleaned)} chunks to Chroma...")
            ids = [item["id"] for item in cleaned]
            metadatas = [item["metadata"] for item in cleaned]

            self.collection.add(
                ids=ids,
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
            )

            logger.info("Inserted %s chunks into Chroma.", len(cleaned))

        except Exception:
            logger.exception("Failed to add documents to Chroma")
            raise


vector_db = VectorDBUtils()