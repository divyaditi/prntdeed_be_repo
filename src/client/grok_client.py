
import os
import logging
import time
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

logger = logging.getLogger(__name__)


class GrokClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY") 
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"
        self.max_tokens = 1000
        self.temperature = 0.7
        self.stream = False
        self.retry_attempts = 3
        self.retry_delay = 1.0  #

    @staticmethod
    def _should_retry(exc: Exception) -> bool:
        status_code = getattr(exc, "status_code", None)
        msg = str(exc).lower()

        if status_code in {429, 500, 502, 503, 504}:
            return True

        return "rate limit" in msg or "too many requests" in msg or "throttl" in msg

    def invoke_model(self, messages,  ):
        for attempt in range(self.retry_attempts + 1):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_completion_tokens=self.max_tokens,
                    temperature=self.temperature,
                    stream=self.stream,
                )
                return completion
            except Exception as exc:
                if self._should_retry(exc) and attempt < self.retry_attempts:
                    delay = self.retry_delay * (2 ** attempt)
                    logger.warning(
                        "Rate limit or transient error hit for Groq model; retrying in %.2f seconds (attempt %s/%s)",
                        delay,
                        attempt + 1,
                        self.retry_attempts,
                    )
                    time.sleep(delay)
                    continue

                logger.error("Error invoking Grok model", exc_info=True)
                return {"error": "something went wrong, pls try again later"}


grok= GrokClient()
n


