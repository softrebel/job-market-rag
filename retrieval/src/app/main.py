from fastapi import FastAPI

from app.api.routes.search import router as search_router


app = FastAPI(
    title="Job Market RAG Retrieval API",
    version="0.1.0",
)


app.include_router(search_router)


@app.get("/health")
def health():
    return {"status": "ok"}
