import logging
import os
import asyncio
from sentence_transformers import SentenceTransformer
from constant import EMBED_MODEL_NAME

logger = logging.getLogger(__name__)

# Disable tokenizer parallelism and multiprocessing to prevent Windows issues
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"


class EmbeddingClient:

    def __init__(self):
        self.model_name = EMBED_MODEL_NAME
        # Load model with CPU explicitly to avoid multiprocessing issues
        self.model = SentenceTransformer(self.model_name, device="cpu")

    async def get_embedding(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("Text cannot be empty")

        try:
            # Run blocking model.encode in thread pool
            result = await asyncio.to_thread(
                self.model.encode,
                text,
                normalize_embeddings=True,
                show_progress_bar=False,
            )
            # Convert numpy array to list
            return result.tolist() if hasattr(result, 'tolist') else list(result)
        except Exception:
            logger.exception("Error occurred while generating embedding for text")
            raise

    async def get_batch_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            raise ValueError("Text list cannot be empty")

        if any(not isinstance(text, str) or not text.strip() for text in texts):
            raise ValueError("Text list cannot contain empty values")

        try:
            result = await asyncio.to_thread(
                self.model.encode,
                texts,
                normalize_embeddings=True,
                show_progress_bar=False,
            )
            return result.tolist()
        except Exception:
            logger.exception("Error occurred while generating embeddings for texts")
            raise


embedding = EmbeddingClient()
