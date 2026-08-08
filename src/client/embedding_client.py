import logging
from sentence_transformers import SentenceTransformer
from constant import EMBED_MODEL_NAME

logger = logging.getLogger(__name__)


class EmbeddingClient:

    def __init__(self):
        self.model_name = EMBED_MODEL_NAME
        self.model = SentenceTransformer(self.model_name)

    def get_embedding(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("Text cannot be empty")

        try:
            result = self.model.encode(
                text,
                normalize_embeddings=True,
            ).tolist()
            return result
        except Exception:
            logger.exception("Error occurred while generating embedding for text")
            raise

    def get_batch_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            raise ValueError("Text list cannot be empty")

        if any(not isinstance(text, str) or not text.strip() for text in texts):
            raise ValueError("Text list cannot contain empty values",exc_info=True)

        try:
            result = self.model.encode(
                texts,
                batch_size=32,
                normalize_embeddings=True,
            ).tolist()
            return result
        except Exception:
            logger.exception("Error occurred while generating embeddings for texts", exc_info=True)
            raise


embedding = EmbeddingClient()

