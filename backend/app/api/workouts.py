"""
Workout generation and management API routes.

Handles workout plan generation, retrieval, progression
analysis, and plan lifecycle management.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.database import Database
from app.core.security import get_current_user
from app.models.workout import (
    PlanStatus,
    WorkoutPlan,
    WorkoutPlanResponse,
    WorkoutPlanSummary,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/workouts", tags=["Workouts"])


def _serialize(doc: dict) -> dict:
    """Convert a MongoDB workout document to a serializable dict."""
    doc["_id"] = str(doc["_id"])
    return doc


# ─────────────────────────────────────────────────────────────────────────
#  POST /workouts/generate – Generate a new workout plan
# ─────────────────────────────────────────────────────────────────────────

@router.post(
    "/generate",
    response_model=WorkoutPlanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate a personalized workout plan",
    description="Uses the latest assessment and fitness scores to generate "
                "a complete multi-week workout plan tailored to the user.",
)
async def generate_workout_plan(
    current_user: dict = Depends(get_current_user),
    duration_weeks: int = Query(default=4, ge=1, le=12),
):
    """Generate a new workout plan for the authenticated user."""
    uid = current_user["uid"]
    assessments_col = Database.get_collection("assessments")
    fitness_col = Database.get_collection("fitness_scores")
    workouts_col = Database.get_collection("workout_plans")
    users_col = Database.get_collection("users")

    # Get latest assessment
    assessment = await assessments_col.find_one(
        {"user_id": uid, "is_latest": True},
        sort=[("created_at", -1)],
    )
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No assessment found. Complete the assessment first.",
        )

    # Get latest fitness scores
    score_doc = await fitness_col.find_one(
        {"user_id": uid},
        sort=[("calculated_at", -1)],
    )
    if not score_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No fitness scores found. Calculate fitness scores first.",
        )

    # Reconstruct data objects
    from app.models.assessment import AssessmentData
    from app.models.fitness import FitnessScores
    assessment_data = AssessmentData(**assessment["data"])
    fitness_scores = FitnessScores(**score_doc["scores"])

    assessment_id = str(assessment["_id"])
    fitness_score_id = str(score_doc["_id"])

    # Deactivate any existing active plans
    await workouts_col.update_many(
        {"user_id": uid, "is_active": True},
        {
            "$set": {
                "is_active": False,
                "status": PlanStatus.ARCHIVED.value,
                "updated_at": datetime.utcnow(),
            }
        },
    )

    # Generate the plan
    from app.services.workout_generator import generate_workout_plan as gen_plan
    plan = await gen_plan(
        user_id=uid,
        assessment_id=assessment_id,
        fitness_score_id=fitness_score_id,
        data=assessment_data,
        scores=fitness_scores,
        duration_weeks=duration_weeks,
    )

    # Store in MongoDB
    result = await workouts_col.insert_one(plan.model_dump())
    plan_id = str(result.inserted_id)

    # Update user profile
    await users_col.update_one(
        {"firebase_uid": uid},
        {
            "$set": {
                "active_workout_plan_id": plan_id,
                "onboarding_status": "plan_generated",
                "updated_at": datetime.utcnow(),
            }
        },
    )

    created = await workouts_col.find_one({"_id": result.inserted_id})
    logger.info("Workout plan generated for user %s: %s", uid, plan.title)
    return _serialize(created)


# ─────────────────────────────────────────────────────────────────────────
#  GET /workouts/active – Get active workout plan
# ─────────────────────────────────────────────────────────────────────────

@router.get(
    "/active",
    response_model=WorkoutPlanResponse,
    summary="Get active workout plan",
)
async def get_active_plan(
    current_user: dict = Depends(get_current_user),
):
    """Retrieve the user's currently active workout plan."""
    collection = Database.get_collection("workout_plans")

    plan = await collection.find_one(
        {"user_id": current_user["uid"], "is_active": True},
        sort=[("created_at", -1)],
    )

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active workout plan. Generate one first.",
        )

    return _serialize(plan)


# ─────────────────────────────────────────────────────────────────────────
#  GET /workouts/{plan_id} – Get specific workout plan
# ─────────────────────────────────────────────────────────────────────────

@router.get(
    "/{plan_id}",
    response_model=WorkoutPlanResponse,
    summary="Get workout plan by ID",
)
async def get_plan(
    plan_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Retrieve a specific workout plan by its ID."""
    collection = Database.get_collection("workout_plans")

    try:
        oid = ObjectId(plan_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan ID format.",
        )

    plan = await collection.find_one(
        {"_id": oid, "user_id": current_user["uid"]}
    )

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout plan not found.",
        )

    return _serialize(plan)


# ─────────────────────────────────────────────────────────────────────────
#  GET /workouts – List all workout plans
# ─────────────────────────────────────────────────────────────────────────

@router.get(
    "/",
    response_model=List[WorkoutPlanSummary],
    summary="List all workout plans",
)
async def list_plans(
    current_user: dict = Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
):
    """List all workout plans for the user (newest first)."""
    collection = Database.get_collection("workout_plans")

    cursor = collection.find(
        {"user_id": current_user["uid"]},
        {
            "title": 1,
            "difficulty": 1,
            "duration_weeks": 1,
            "days_per_week": 1,
            "status": 1,
            "is_active": 1,
            "current_week": 1,
            "created_at": 1,
        },
    ).sort("created_at", -1).skip(skip).limit(limit)

    plans = []
    async for doc in cursor:
        plans.append(_serialize(doc))

    return plans


# ─────────────────────────────────────────────────────────────────────────
#  GET /workouts/active/today – Get today's workout
# ─────────────────────────────────────────────────────────────────────────

@router.get(
    "/active/today",
    summary="Get today's workout from active plan",
)
async def get_todays_workout(
    current_user: dict = Depends(get_current_user),
):
    """Get the workout scheduled for today from the active plan."""
    collection = Database.get_collection("workout_plans")

    plan = await collection.find_one(
        {"user_id": current_user["uid"], "is_active": True},
    )

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active workout plan.",
        )

    # Determine today's day of week
    import calendar
    today = datetime.utcnow()
    day_name = calendar.day_name[today.weekday()]

    # Find today's workout in the current week
    current_week = plan.get("current_week", 1)
    weekly_schedules = plan.get("weekly_schedules", [])

    if current_week <= len(weekly_schedules):
        week = weekly_schedules[current_week - 1]
        for day in week.get("days", []):
            if day.get("day") == day_name:
                # Check if it was already completed today
                logs_col = Database.get_collection("workout_logs")
                start_of_today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
                already_logged = await logs_col.find_one({
                    "user_id": current_user["uid"],
                    "workout_plan_id": str(plan["_id"]),
                    "completed_at": {"$gte": start_of_today}
                })
                
                return {
                    "plan_id": str(plan["_id"]),
                    "plan_title": plan["title"],
                    "current_week": current_week,
                    "day_of_week": day_name,
                    "workout": day,
                    "is_completed": bool(already_logged),
                }

    return {
        "plan_id": str(plan["_id"]),
        "plan_title": plan["title"],
        "current_week": current_week,
        "day_of_week": day_name,
        "workout": None,
        "message": "No workout scheduled for today.",
    }


# ─────────────────────────────────────────────────────────────────────────
#  PATCH /workouts/{plan_id}/advance – Advance to next week
# ─────────────────────────────────────────────────────────────────────────

@router.patch(
    "/{plan_id}/advance",
    summary="Advance to next week in the plan",
)
async def advance_week(
    plan_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Advance the workout plan to the next week."""
    collection = Database.get_collection("workout_plans")

    try:
        oid = ObjectId(plan_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan ID format.",
        )

    plan = await collection.find_one(
        {"_id": oid, "user_id": current_user["uid"]}
    )

    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout plan not found.",
        )

    current_week = plan.get("current_week", 1)
    duration_weeks = plan.get("duration_weeks", 4)

    if current_week >= duration_weeks:
        # Plan completed
        await collection.update_one(
            {"_id": oid},
            {
                "$set": {
                    "status": PlanStatus.COMPLETED.value,
                    "is_active": False,
                    "completed_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                }
            },
        )
        return {"message": "Plan completed! 🎉", "completed": True}

    await collection.update_one(
        {"_id": oid},
        {
            "$set": {
                "current_week": current_week + 1,
                "current_day": 1,
                "updated_at": datetime.utcnow(),
            }
        },
    )

    return {
        "message": f"Advanced to week {current_week + 1}",
        "current_week": current_week + 1,
        "completed": False,
    }


# ─────────────────────────────────────────────────────────────────────────
#  POST /workouts/{plan_id}/analyze – Analyze progression
# ─────────────────────────────────────────────────────────────────────────

@router.post(
    "/{plan_id}/analyze",
    summary="Analyze performance and get progression recommendations",
)
async def analyze_progression(
    plan_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Analyze recent workout performance and generate progression recommendations."""
    uid = current_user["uid"]
    workouts_col = Database.get_collection("workout_plans")
    logs_col = Database.get_collection("workout_logs")

    try:
        oid = ObjectId(plan_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan ID format.",
        )

    plan_doc = await workouts_col.find_one(
        {"_id": oid, "user_id": uid}
    )

    if not plan_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout plan not found.",
        )

    # Get recent workout logs
    from app.models.progress import WorkoutLog
    cursor = logs_col.find(
        {"user_id": uid, "workout_plan_id": plan_id},
    ).sort("completed_at", -1).limit(10)

    logs = []
    async for doc in cursor:
        logs.append(WorkoutLog(**doc))

    # Run progression analysis
    from app.services.progression_engine import analyze_recent_performance
    analysis = analyze_recent_performance(logs)

    return analysis.to_dict()


# ─────────────────────────────────────────────────────────────────────────
#  DELETE /workouts/{plan_id} – Delete a workout plan
# ─────────────────────────────────────────────────────────────────────────

@router.delete(
    "/{plan_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a workout plan",
)
async def delete_plan(
    plan_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Delete a specific workout plan."""
    collection = Database.get_collection("workout_plans")

    try:
        oid = ObjectId(plan_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan ID format.",
        )

    result = await collection.delete_one(
        {"_id": oid, "user_id": current_user["uid"]}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout plan not found.",
        )

    logger.info("Workout plan %s deleted for user %s", plan_id, current_user["uid"])
    return {"message": "Workout plan deleted successfully."}
