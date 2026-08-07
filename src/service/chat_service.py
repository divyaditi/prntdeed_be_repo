
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)


class Process_Chat:
    def __init__(self):
        pass

    async def process_chat(self, message: str):
        try:
            response = f"Processed user input: {message}"
            return {"response": response}
        except Exception:
            logger.error("Chat processing failed", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Something went wrong while processing the chat input.",
            )


process_chat = Process_Chat()