import logging
from fastapi import APIRouter, HTTPException
from model.chat_model import ChatModel
from service.chat_service import Process_Chat

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/chat")
async def chat(message: ChatModel):
    try:
        processor = Process_Chat()
        response = await processor.process_chat(message=message.message)
        return response
    except Exception:
        logger.error("Chat processing failed", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while processing the chat input.",
        )