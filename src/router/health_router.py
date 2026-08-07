import logging
from fastapi import APIRouter, HTTPException
router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/health")
async def health_check():
    try:
        health_status = {"status": "Healthy"}
        return health_status

    except Exception as e:
        logger.error("Health check failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Something went wrong while checking the health of the application.")