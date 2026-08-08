
import json
import logging
from fastapi import HTTPException
from client.grok_client import grok
from utils.prompt_utils import prompt

logger = logging.getLogger(__name__)


class ProcessChat:

    def __init__(self):
        self.llm_client = grok

    def _normalize_response(self, response):
        content = getattr(response, "content", response)
        if not isinstance(content, str):
            return str(content)

        content = content.strip()
        try:
            payload = json.loads(content)
            return payload.get("response", content)
        except (TypeError, ValueError):
            return content

    async def process_chat(self, message: str) -> dict:

        try:
            response = await self.llm_client.invoke(message)

            return {
                "response": self._normalize_response(response)
            }

        except Exception:
            logger.exception("Chat processing failed", exc_info=True)
            raise

chat_svc= ProcessChat()

