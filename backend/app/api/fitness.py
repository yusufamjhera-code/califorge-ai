"""
Fitness analysis API routes.

Handles fitness score calculation, retrieval, and overview
for the user dashboard.
"""

from __future__ import annotations

import logging
from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.database import Database
from app.core.security import get_current_user
from app.models.fitness import (
    FitnessLevel,
    FitnessOverview,
    FitnessScoreDocument,
    FitnessScoreResponse,
)
from app.services.fitness_engine import calculate_fitness_scores
from app.services.insights_engine import generate_insights

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/fitness", tags=["Fitness"])


def _serialize(doc: dict) -> dict:
    """Convert a MongoDB document to a serializable dict."""
    doc["_id"] = str(doc["_id"])
    return doc


# ─────────────────────────────────────────────────────────────────────────
#  POST /fitness/calculate – Calculate fitness scores
# ─────────────────────────────────────────────────────────────────────────

@router.post(
    "/calculate",
    response_model=FitnessScoreResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Calculate fitness scores from latest assessment",
    description="Runs the fitness engine on the user's latest assessment "
                "to compute all five score dimensions and fitness level.",
)
async def calculate_scores(
    current_user: dict = Depends(get_current_user),
    assessment_id: str | None = None,
):
    """Calculate and store fitness scores.

    If assessment_id is not provided, uses the latest assessment.
    """
    uid = current_user["uid"]
    assessments_col = Database.get_collection("assessments")
    fitness_col = Database.get_collection("fitness_scores")
    users_col = Database.get_collection("users")

    # Get assessment
    if assessment_id:
        try:
            oid = ObjectId(assessment_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid assessment ID.",
            )
        assessment = await assessments_col.find_one(
            {"_id": oid, "user_id": uid}
        )
    else:
        assessment = await assessments_col.find_one(
            {"user_id": uid, "is_latest": True},
            sort=[("created_at", -1)],
        )

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No assessment found. Please complete the assessment first.",
        )

    # Import and reconstruct AssessmentData
    from app.models.assessment import AssessmentData
    assessment_data = AssessmentData(**assessment["data"])

    # Calculate scores
    scores = calculate_fitness_scores(assessment_data)

    # Store scores
    score_doc = FitnessScoreDocument(
        user_id=uid,
        assessment_id=str(assessment["_id"]),
        scores=scores,
    )

    result = await fitness_col.insert_one(score_doc.model_dump())
    score_id = str(result.inserted_id)

    # Update user profile with latest fitness score
    await users_col.update_one(
        {"firebase_uid": uid},
        {
            "$set": {
                "latest_fitness_score_id": score_id,
                "updated_at": datetime.utcnow(),
            }
        },
    )

    created = await fitness_col.find_one({"_id": result.inserted_id})
    logger.info(
        "Fitness scores calculated for user %s: %.1f (%s)",
        uid, scores.overall_fitness, scores.level.value,
    )
    return _serialize(created)


# ─────────────────────────────────────────────────────────────────────────
#  GET /fitness/latest – Get latest fitness scores
# ─────────────────────────────────────────────────────────────────────────

@router.get(
    "/latest",
    response_model=FitnessScoreResponse,
    summary="Get latest fitness scores",
)
async def get_latest_scores(
    current_user: dict = Depends(get_current_user),
):
    """Retrieve the most recent fitness scores for the user."""
    collection = Database.get_collection("fitness_scores")

    scores = await collection.find_one(
        {"user_id": current_user["uid"]},
        sort=[("calculated_at", -1)],
    )

    if not scores:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No fitness scores found. Run /fitness/calculate first.",
        )

    return _serialize(scores)


# ─────────────────────────────────────────────────────────────────────────
#  GET /fitness/overview – Dashboard fitness overview
# ─────────────────────────────────────────────────────────────────────────

@router.get(
    "/overview",
    response_model=FitnessOverview,
    summary="Get fitness overview for dashboard",
)
async def get_fitness_overview(
    current_user: dict = Depends(get_current_user),
):
    """Get a comprehensive fitness overview including scores and insights."""
    uid = current_user["uid"]
    fitness_col = Database.get_collection("fitness_scores")
    assessments_col = Database.get_collection("assessments")

    # Get latest scores
    score_doc = await fitness_col.find_one(
        {"user_id": uid},
        sort=[("calculated_at", -1)],
    )

    if not score_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No fitness data available. Complete assessment and calculate scores first.",
        )

    scores_data = score_doc["scores"]
    level = FitnessLevel(scores_data["level"])

    # Get assessment for insights
    assessment = await assessments_col.find_one(
        {"user_id": uid, "is_latest": True},
        sort=[("created_at", -1)],
    )

    # Generate insights
    insights_list = []
    if assessment:
        from app.models.assessment import AssessmentData
        from app.models.fitness import FitnessScores as FS
        assessment_data = AssessmentData(**assessment["data"])
        fitness_scores = FS(**scores_data)
        insights_list = generate_insights(fitness_scores, assessment_data)
        # Extract just the message strings for the overview
        insights_list = [i["message"] for i in insights_list[:5]]

    return FitnessOverview(
        overall_fitness=scores_data["overall_fitness"],
        strength=scores_data["strength"],
        recovery=scores_data["recovery"],
        consistency=scores_data["consistency"],
        mobility=scores_data["mobility"],
        level=level,
        level_label=FitnessOverview.level_to_label(level),
        insights=insights_list,
    )


# ─────────────────────────────────────────────────────────────────────────
#  GET /fitness/insights – Get coaching insights
# ─────────────────────────────────────────────────────────────────────────

@router.get(
    "/insights",
    summary="Get personalized coaching insights",
)
async def get_insights(
    current_user: dict = Depends(get_current_user),
):
    """Get detailed personalized coaching insights."""
    uid = current_user["uid"]
    fitness_col = Database.get_collection("fitness_scores")
    assessments_col = Database.get_collection("assessments")

    score_doc = await fitness_col.find_one(
        {"user_id": uid},
        sort=[("calculated_at", -1)],
    )

    if not score_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No fitness data available.",
        )

    assessment = await assessments_col.find_one(
        {"user_id": uid, "is_latest": True},
    )

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No assessment data available.",
        )

    from app.models.assessment import AssessmentData
    from app.models.fitness import FitnessScores as FS
    assessment_data = AssessmentData(**assessment["data"])
    fitness_scores = FS(**score_doc["scores"])

    # Optionally include progress stats
    progress_stats = None
    try:
        from app.models.progress import ProgressStats
        workout_logs_col = Database.get_collection("workout_logs")
        total = await workout_logs_col.count_documents({"user_id": uid})
        if total > 0:
            progress_stats = ProgressStats(total_workouts=total)
    except Exception:
        pass

    insights = generate_insights(fitness_scores, assessment_data, progress_stats)
    return {"insights": insights, "count": len(insights)}


# ─────────────────────────────────────────────────────────────────────────
#  GET /fitness/history – Score history for charts
# ─────────────────────────────────────────────────────────────────────────

@router.get(
    "/history",
    summary="Get fitness score history",
)
async def get_score_history(
    current_user: dict = Depends(get_current_user),
    limit: int = 10,
):
    """Retrieve fitness score history for trend visualization."""
    collection = Database.get_collection("fitness_scores")

    cursor = collection.find(
        {"user_id": current_user["uid"]},
    ).sort("calculated_at", -1).limit(limit)

    history = []
    async for doc in cursor:
        history.append({
            "id": str(doc["_id"]),
            "overall_fitness": doc["scores"]["overall_fitness"],
            "strength": doc["scores"]["strength"],
            "recovery": doc["scores"]["recovery"],
            "consistency": doc["scores"]["consistency"],
            "mobility": doc["scores"]["mobility"],
            "level": doc["scores"]["level"],
            "calculated_at": doc["calculated_at"],
        })

    return {"history": history, "count": len(history)}
