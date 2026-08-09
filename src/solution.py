from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from router.chat_router import router as chat_router
from router.health_router import router as health_router
from service.embedding_service import embedding_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    result = embedding_service.create_vector_store()

    if result.get("status") == "success":
        print("Embeddings created successfully on startup")
    else:
        print(f"Embedding startup status: {result}")

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(health_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run(
        "solution:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )