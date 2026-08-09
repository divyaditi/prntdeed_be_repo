import logging
import os
import asyncio
from sentence_transformers import SentenceTransformer
from constant import EMBED_MODEL_NAME, TOKENIZERS_PARALLELISM, OMP_NUM_THREADS, OPENBLAS_NUM_THREADS, MKL_NUM_THREADS, NUMEXPR_NUM_THREADS

logger = logging.getLogger(__name__)

# Disable tokenizer parallelism and multiprocessing to prevent Windows issues
os.environ["TOKENIZERS_PARALLELISM"] = TOKENIZERS_PARALLELISM
os.environ["OMP_NUM_THREADS"] = OMP_NUM_THREADS
os.environ["OPENBLAS_NUM_THREADS"] = OPENBLAS_NUM_THREADS
os.environ["MKL_NUM_THREADS"] = MKL_NUM_THREADS
os.environ["NUMEXPR_NUM_THREADS"] = NUMEXPR_NUM_THREADS


class EmbeddingClient:

    def __init__(self):
        self.model_name = EMBED_MODEL_NAME
        self.model = SentenceTransformer(self.model_name, device="cpu")

    async def get_embedding(self, text: str) -> list[float]:
        """Generate embedding for a single text asynchronously."""
        if not text.strip():
            raise ValueError("Text cannot be empty")

        try:
            # Run blocking model.encode in thread pool to avoid blocking async loop
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
        """Generate embeddings for multiple texts asynchronously."""
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

