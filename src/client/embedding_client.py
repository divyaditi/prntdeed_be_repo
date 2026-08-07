from sentence_transformers import SentenceTransformer
import logging


class EmbeddingClient:

    def __init__(self):
        self.model_name = "BAAI/bge-m3"
        self.model = SentenceTransformer(self.model_name)

    def get_embedding(self, text: str) -> list[float]:
       
       try: 
           result=self.model.encode(
            text,
            normalize_embeddings=True
            ).tolist()
           return result
       except Exception as e:
           logging.error(f"Error occurred while generating embedding for text: {text}", exc_info=True)
           return []

    def get_batch_embeddings(self, texts: list[str]) -> list[list[float]]:
        try:
            result=self.model.encode(
                texts,
                batch_size=32,
                normalize_embeddings=True
            ).tolist()
            return result
        except Exception as e:
            logging.error(f"Error occurred while generating embeddings for texts: {texts}", exc_info=True)
            return []


embedding = EmbeddingClient()

