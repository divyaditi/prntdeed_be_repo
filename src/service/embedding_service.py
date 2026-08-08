import logging

from utils.chunking_utils import chunk_svc
from utils.v_db_utils import vector_db

logger = logging.getLogger(__name__)


class EmbeddingService:

    def create_vector_store(self):
        try:
            if vector_db.collection.count() > 0:
                return {"status": "already_indexed"}

            chunk_svc.load_files()
            documents = chunk_svc.prepare_chunks()

            if not documents:
                logger.warning("No document chunks were found to index.")
                return {"status": "no_documents"}

            vector_db.add_documents(documents)
            return {"status": "success"}

        except Exception:
            logger.exception("Embedding creation failed")
            return {"status": "error", "message": "Failed to create embeddings"}


embedding_service = EmbeddingService()