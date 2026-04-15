from fastapi import APIRouter

from app.schemas.recommend import RecommendRequest, RecommendResponse
from app.services.recommendation_service import build_mock_recommendations

router = APIRouter()


@router.post("/recommend", response_model=RecommendResponse)
def recommend(payload: RecommendRequest) -> RecommendResponse:
    recommendations = build_mock_recommendations(payload.answers, payload.lang)
    return RecommendResponse(recommendations=recommendations)