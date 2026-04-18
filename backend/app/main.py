from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.questions import router as questions_router
from app.api.routes.recommend import router as recommend_router

app = FastAPI(
    title="GRS Backend",
    description="Minimal FastAPI backend for the Game Recommendation System.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "https://grs-k1ew.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(questions_router)
app.include_router(recommend_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}