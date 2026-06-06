"""
Admin management API routes.

Provides admin-only endpoints for user management,
statistics, and system health monitoring.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import List, Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.database import Database
from app.core.security import get_admin_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["Admin"])


def _serialize(doc: dict) -> dict:
    """Convert a MongoDB document to a serializable dict."""
    doc["_id"] = str(doc["_id"])
    return doc


# ─────────────────────────────────────────────────────────────────────────
#  GET /admin/health – System health check
# ─────────────────────────────────────────────────────────────────────────

@router.get(
    "/health",
    summary="System health check",
)
async def health_check(
    admin_user: dict = Depends(get_admin_user),
):
    """Check system health including database connectivity."""
    db_health = await Database.health_check()

    return {
        "status": "healthy" if db_health["status"] == "healthy" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": db_health,
            "api": {"status": "healthy"},
        },
    }


# ─────────────────────────────────────────────────────────────────────────
#  GET /admin/stats – Platform statistics
# ─────────────────────────────────────────────────────────────────────────

@router.get(
    "/stats",
    summary="Get platform-wide statistics",
)
async def get_platform_stats(
    admin_user: dict = Depends(get_admin_user),
):
    """Get aggregate platform statistics."""
    users_col = Database.get_collection("users")
    assessments_col = Database.get_collection("assessments")
    plans_col = Database.get_collection("workout_plans")
    logs_col = Database.get_collection("workout_logs")

    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    total_users = await users_col.count_documents({})
    active_users = await users_col.count_documents({"is_active": True})
    new_users_week = await users_col.count_documents(
        {"created_at": {"$gte": week_ago}}
    )
    new_users_month = await users_col.count_documents(
        {"created_at": {"$gte": month_ago}}
    )

    total_assessments = await assessments_col.count_documents({})
    total_plans = await plans_col.count_documents({})
    active_plans = await plans_col.count_documents({"is_active": True})
    total_workouts = await logs_col.count_documents({})
    workouts_this_week = await logs_col.count_documents(
        {"completed_at": {"$gte": week_ago}}
    )

    # Onboarding funnel
    completed_assessment = await users_col.count_documents(
        {"assessment_completed": True}
    )
    generated_plan = await users_col.count_documents(
        {"active_workout_plan_id": {"$exists": True, "$ne": None}}
    )

    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "new_this_week": new_users_week,
            "new_this_month": new_users_month,
        },
        "assessments": {
            "total": total_assessments,
        },
        "workout_plans": {
            "total": total_plans,
            "active": active_plans,
        },
        "workout_logs": {
            "total": total_workouts,
            "this_week": workouts_this_week,
        },
        "funnel": {
            "registered": total_users,
            "assessment_completed": completed_assessment,
            "plan_generated": generated_plan,
            "conversion_rate": round(
                (generated_plan / max(1, total_users)) * 100, 1
            ),
        },
        "generated_at": now.isoformat(),
    }


# ─────────────────────────────────────────────────────────────────────────
#  GET /admin/users – List all users
# ─────────────────────────────────────────────────────────────────────────

@router.get(
    "/users",
    summary="List all users",
)
async def list_users(
    admin_user: dict = Depends(get_admin_user),
    limit: int = Query(default=50, ge=1, le=200),
    skip: int = 0,
    active_only: bool = True,
    search: Optional[str] = None,
):
    """List all users with optional filtering."""
    collection = Database.get_collection("users")

    query = {}
    if active_only:
        query["is_active"] = True
    if search:
        query["$or"] = [
            {"email": {"$regex": search, "$options": "i"}},
            {"display_name": {"$regex": search, "$options": "i"}},
        ]

    cursor = collection.find(
        query,
        {
            "firebase_uid": 1,
            "email": 1,
            "display_name": 1,
            "onboarding_status": 1,
            "assessment_completed": 1,
            "is_active": 1,
            "created_at": 1,
            "last_login_at": 1,
        },
    ).sort("created_at", -1).skip(skip).limit(limit)

    users = []
    async for doc in cursor:
        users.append(_serialize(doc))

    total = await collection.count_documents(query)

    return {
        "users": users,
        "total": total,
        "limit": limit,
        "skip": skip,
    }


# ─────────────────────────────────────────────────────────────────────────
#  GET /admin/users/{uid} – Get specific user details
# ─────────────────────────────────────────────────────────────────────────

@router.get(
    "/users/{uid}",
    summary="Get user details",
)
async def get_user_details(
    uid: str,
    admin_user: dict = Depends(get_admin_user),
):
    """Get detailed information about a specific user."""
    users_col = Database.get_collection("users")
    assessments_col = Database.get_collection("assessments")
    fitness_col = Database.get_collection("fitness_scores")
    plans_col = Database.get_collection("workout_plans")
    logs_col = Database.get_collection("workout_logs")

    user = await users_col.find_one({"firebase_uid": uid})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    # Get counts
    assessment_count = await assessments_col.count_documents({"user_id": uid})
    plan_count = await plans_col.count_documents({"user_id": uid})
    workout_count = await logs_col.count_documents({"user_id": uid})

    # Get latest fitness scores
    latest_scores = await fitness_col.find_one(
        {"user_id": uid},
        sort=[("calculated_at", -1)],
    )

    user_data = _serialize(user)
    user_data["stats"] = {
        "assessment_count": assessment_count,
        "plan_count": plan_count,
        "workout_count": workout_count,
    }
    if latest_scores:
        user_data["latest_scores"] = {
            "overall_fitness": latest_scores["scores"]["overall_fitness"],
            "level": latest_scores["scores"]["level"],
            "calculated_at": latest_scores["calculated_at"],
        }

    return user_data


# ─────────────────────────────────────────────────────────────────────────
#  PATCH /admin/users/{uid}/deactivate – Deactivate a user
# ─────────────────────────────────────────────────────────────────────────

@router.patch(
    "/users/{uid}/deactivate",
    summary="Deactivate a user account",
)
async def admin_deactivate_user(
    uid: str,
    admin_user: dict = Depends(get_admin_user),
):
    """Deactivate a user account (admin action)."""
    collection = Database.get_collection("users")

    result = await collection.find_one_and_update(
        {"firebase_uid": uid},
        {
            "$set": {
                "is_active": False,
                "updated_at": datetime.utcnow(),
            }
        },
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    logger.info("Admin deactivated user %s", uid)
    return {"message": f"User {uid} deactivated."}


# ─────────────────────────────────────────────────────────────────────────
#  PATCH /admin/users/{uid}/activate – Reactivate a user
# ─────────────────────────────────────────────────────────────────────────

@router.patch(
    "/users/{uid}/activate",
    summary="Reactivate a user account",
)
async def admin_activate_user(
    uid: str,
    admin_user: dict = Depends(get_admin_user),
):
    """Reactivate a previously deactivated user account."""
    collection = Database.get_collection("users")

    result = await collection.find_one_and_update(
        {"firebase_uid": uid},
        {
            "$set": {
                "is_active": True,
                "updated_at": datetime.utcnow(),
            }
        },
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    logger.info("Admin reactivated user %s", uid)
    return {"message": f"User {uid} reactivated."}


# ─────────────────────────────────────────────────────────────────────────
#  GET /admin/exercises – List all exercises in the database
# ─────────────────────────────────────────────────────────────────────────

@router.get(
    "/exercises",
    summary="List all exercises in the database",
)
async def list_exercises(
    admin_user: dict = Depends(get_admin_user),
    category: Optional[str] = None,
):
    """List all exercises in the exercise database."""
    from app.data.exercises import EXERCISES, get_exercises_by_category

    if category:
        exercises = get_exercises_by_category(category)
    else:
        exercises = list(EXERCISES.values())

    return {
        "exercises": [ex.model_dump() for ex in exercises],
        "total": len(exercises),
        "categories": list(set(ex.category for ex in EXERCISES.values())),
    }
