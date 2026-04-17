from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.exceptions import AppError
from app.db.session import get_session
from app.schemas.common import ErrorResponse
from app.schemas.recommend import RecommendRequest, RecommendResponse
from app.services.answer_validation_service import validate_answers
from app.services.profile_service import build_user_profile
from app.services.reason_service import generate_reasons
from app.services.recommendation_service import (
    build_recommend_response,
    score_games,
    select_top_candidates,
)

router = APIRouter()


@router.post(
    "/recommend",
    response_model=RecommendResponse,
    responses={
        400: {"model": ErrorResponse},
    },
)
def recommend(
    payload: RecommendRequest,
    session: Session = Depends(get_session),
) -> RecommendResponse:
    try:
        validated_answers = validate_answers(session, payload.answers)
        user_profile = build_user_profile(session, validated_answers)
        scored_candidates = score_games(session, user_profile)
        top_candidates = select_top_candidates(scored_candidates, limit=3)
        reasoned_candidates = generate_reasons(top_candidates, user_profile)

        return build_recommend_response(reasoned_candidates)

    except AppError as error:
        raise HTTPException(
            status_code=error.status_code,
            detail={
                "error": {
                    "code": error.code,
                    "message": error.message,
                }
            },
        )