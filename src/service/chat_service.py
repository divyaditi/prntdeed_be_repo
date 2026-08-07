
import logging
from fastapi import HTTPException
from client.grok_client import grok
from utils.prompt_utils import prompt


logger = logging.getLogger(__name__)



class Process_Chat:
    def __init__(self):
        pass

    def output_parser(self, response):
        try:
            if "error" in response:
                raise HTTPException(
                    status_code=500,
                    detail="Something went wrong while processing the chat input.",
                )
            return response.get("response", "")
        except Exception:
            logger.error("Output parsing failed", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Something went wrong while processing the chat input.",
            )

    async def process_chat(self, message: str):
        try:
            messages = [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": message},
                ]
            response = grok.invoke_model(messages=messages)
            return {"response": response}
        except Exception:
            logger.error("Chat processing failed", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Something went wrong while processing the chat input.",
            )


process_chat = Process_Chat()