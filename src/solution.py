from fastapi import FastAPI
from router.health_router import router as health_router
from router.chat_router import router as chat_router
import uvicorn
app=FastAPI()


app.include_router(health_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run( "solution:app", host="0.0.0.0",port=8080, reload=True)