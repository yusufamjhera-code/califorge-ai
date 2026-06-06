"""
Progress tracking API routes.

Handles weight logging, workout completion logging,
achievements, streaks, and aggregate progress statistics.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import List, Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.database import Database
from app.core.security import get_current_user
from app.models.progress import (
    Achievement,
    AchievementResponse,
    AchievementType,
    ProgressOverview,
    ProgressStats,
    WeightEntry,
    WeightEntryCreate,
    WeightEntryResponse,
    WorkoutLog,
    WorkoutLogCreate,
    WorkoutLogResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/progress", tags=["Progress"])


def _serialize(doc: dict) -> dict:
    """Convert a MongoDB document to a serializable dict."""
    doc["_id"] = str(doc["_id"])
    return doc


# ═══════════════════════════════════════════════════════════════════════
#  WEIGHT TRACKING
# ═══════════════════════════════════════════════════════════════════════

@router.post(
    "/weight",
    response_model=WeightEntryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Log a weight entry",
)
async def log_weight(
    payload: WeightEntryCreate,
    current_user: dict = Depends(get_current_user),
):
    """Log a new weight measurement."""
    uid = current_user["uid"]
    collection = Database.get_collection("weight_entries")

    entry = WeightEntry(
        user_id=uid,
        weight_kg=payload.weight_kg,
        notes=payload.notes,
        recorded_at=payload.recorded_at or datetime.utcnow(),
    )

    result = await collection.insert_one(entry.model_dump())

    # Update current weight on user profile
    users_col = Database.get_collection("users")
    await users_col.update_one(
        {"firebase_uid": uid},
        {
            "$set": {
                "current_weight_kg": payload.weight_kg,
                "updated_at": datetime.utcnow(),
            }
        },
    )

    created = await collection.find_one({"_id": result.inserted_id})
    logger.info("Weight logged for user %s: %.1f kg", uid, payload.weight_kg)

    # Check for weight goal achievement
    await _check_weight_achievement(uid, payload.weight_kg)

    return _serialize(created)


@router.get(
    "/weight",
    response_model=List[WeightEntryResponse],
    summary="Get weight history",
)
async def get_weight_history(
    current_user: dict = Depends(get_current_user),
    limit: int = Query(default=30, ge=1, le=365),
    days: int = Query(default=90, ge=7, le=365),
):
    """Get weight entries for the specified time period."""
    collection = Database.get_collection("weight_entries")
    cutoff = datetime.utcnow() - timedelta(days=days)

    cursor = collection.find(
        {"user_id": current_user["uid"], "recorded_at": {"$gte": cutoff}},
    ).sort("recorded_at", -1).limit(limit)

    entries = []
    async for doc in cursor:
        entries.append(_serialize(doc))

    return entries


@router.delete(
    "/weight/{entry_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a weight entry",
)
async def delete_weight_entry(
    entry_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Delete a specific weight entry."""
    collection = Database.get_collection("weight_entries")

    try:
        oid = ObjectId(entry_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid entry ID.",
        )

    result = await collection.delete_one(
        {"_id": oid, "user_id": current_user["uid"]}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weight entry not found.",
        )

    return {"message": "Weight entry deleted."}


# ═══════════════════════════════════════════════════════════════════════
#  WORKOUT LOGGING
# ═══════════════════════════════════════════════════════════════════════

@router.post(
    "/workouts",
    response_model=WorkoutLogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Log a completed workout",
)
async def log_workout(
    payload: WorkoutLogCreate,
    current_user: dict = Depends(get_current_user),
):
    """Log a completed workout session."""
    uid = current_user["uid"]
    collection = Database.get_collection("workout_logs")

    # Calculate exercise counts
    total = len(payload.exercises)
    completed = sum(1 for e in payload.exercises if not e.skipped and e.sets_completed > 0)
    skipped = sum(1 for e in payload.exercises if e.skipped)

    log = WorkoutLog(
        user_id=uid,
        workout_plan_id=payload.workout_plan_id,
        week_number=payload.week_number,
        day_number=payload.day_number,
        day_of_week=payload.day_of_week,
        workout_title=payload.workout_title,
        exercises=payload.exercises,
        total_exercises=total,
        completed_exercises=completed,
        skipped_exercises=skipped,
        duration_minutes=payload.duration_minutes,
        difficulty_rating=payload.difficulty_rating,
        energy_rating=payload.energy_rating,
        notes=payload.notes,
    )

    result = await collection.insert_one(log.model_dump())
    created = await collection.find_one({"_id": result.inserted_id})

    logger.info(
        "Workout logged for user %s: %s (%d/%d exercises)",
        uid, payload.workout_title, completed, total,
    )

    # Check for achievements
    await _check_workout_achievements(uid)

    return _serialize(created)


@router.get(
    "/workouts",
    response_model=List[WorkoutLogResponse],
    summary="Get workout log history",
)
async def get_workout_history(
    current_user: dict = Depends(get_current_user),
    limit: int = Query(default=20, ge=1, le=100),
    skip: int = 0,
):
    """Get recent workout logs."""
    collection = Database.get_collection("workout_logs")

    cursor = collection.find(
        {"user_id": current_user["uid"]},
    ).sort("completed_at", -1).skip(skip).limit(limit)

    logs = []
    async for doc in cursor:
        logs.append(_serialize(doc))

    return logs


# ═══════════════════════════════════════════════════════════════════════
#  ACHIEVEMENTS
# ═══════════════════════════════════════════════════════════════════════

@router.get(
    "/achievements",
    response_model=List[AchievementResponse],
    summary="Get user achievements",
)
async def get_achievements(
    current_user: dict = Depends(get_current_user),
):
    """Get all achievements unlocked by the user."""
    collection = Database.get_collection("achievements")

    cursor = collection.find(
        {"user_id": current_user["uid"]},
    ).sort("unlocked_at", -1)

    achievements = []
    async for doc in cursor:
        achievements.append(_serialize(doc))

    return achievements


# ═══════════════════════════════════════════════════════════════════════
#  PROGRESS STATISTICS
# ═══════════════════════════════════════════════════════════════════════

@router.get(
    "/stats",
    response_model=ProgressStats,
    summary="Get aggregate progress statistics",
)
async def get_progress_stats(
    current_user: dict = Depends(get_current_user),
):
    """Calculate and return aggregate progress statistics."""
    uid = current_user["uid"]
    return await _calculate_stats(uid)


@router.get(
    "/overview",
    response_model=ProgressOverview,
    summary="Get complete progress overview",
)
async def get_progress_overview(
    current_user: dict = Depends(get_current_user),
):
    """Get a comprehensive progress overview for the dashboard."""
    uid = current_user["uid"]

    stats = await _calculate_stats(uid)

    # Recent workouts
    logs_col = Database.get_collection("workout_logs")
    cursor = logs_col.find(
        {"user_id": uid},
    ).sort("completed_at", -1).limit(5)
    recent_workouts = [_serialize(doc) async for doc in cursor]

    # Recent weight entries
    weight_col = Database.get_collection("weight_entries")
    cursor = weight_col.find(
        {"user_id": uid},
    ).sort("recorded_at", -1).limit(5)
    recent_weight = [_serialize(doc) async for doc in cursor]

    # Achievements
    ach_col = Database.get_collection("achievements")
    cursor = ach_col.find(
        {"user_id": uid},
    ).sort("unlocked_at", -1)
    achievements = [_serialize(doc) async for doc in cursor]

    return ProgressOverview(
        stats=stats,
        recent_workouts=recent_workouts,
        recent_weight_entries=recent_weight,
        achievements=achievements,
    )


# ═══════════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

async def _calculate_stats(uid: str) -> ProgressStats:
    """Calculate aggregate progress statistics for a user."""
    logs_col = Database.get_collection("workout_logs")
    weight_col = Database.get_collection("weight_entries")
    ach_col = Database.get_collection("achievements")

    # Total workouts
    total_workouts = await logs_col.count_documents({"user_id": uid})

    # Total workout minutes
    pipeline = [
        {"$match": {"user_id": uid, "duration_minutes": {"$exists": True, "$ne": None}}},
        {"$group": {"_id": None, "total": {"$sum": "$duration_minutes"}}},
    ]
    result = await logs_col.aggregate(pipeline).to_list(1)
    total_minutes = result[0]["total"] if result else 0

    # Workouts this week
    week_start = datetime.utcnow() - timedelta(days=datetime.utcnow().weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    workouts_this_week = await logs_col.count_documents(
        {"user_id": uid, "completed_at": {"$gte": week_start}}
    )

    # Workouts this month
    month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    workouts_this_month = await logs_col.count_documents(
        {"user_id": uid, "completed_at": {"$gte": month_start}}
    )

    # Average ratings
    pipeline = [
        {"$match": {"user_id": uid}},
        {
            "$group": {
                "_id": None,
                "avg_difficulty": {"$avg": "$difficulty_rating"},
                "avg_energy": {"$avg": "$energy_rating"},
            }
        },
    ]
    result = await logs_col.aggregate(pipeline).to_list(1)
    avg_difficulty = result[0]["avg_difficulty"] if result and result[0].get("avg_difficulty") else None
    avg_energy = result[0]["avg_energy"] if result and result[0].get("avg_energy") else None

    # Streak calculation
    current_streak, longest_streak = await _calculate_streaks(uid)

    # Weight change
    weight_change = None
    weight_count = await weight_col.count_documents({"user_id": uid})
    if weight_count >= 2:
        first = await weight_col.find_one(
            {"user_id": uid}, sort=[("recorded_at", 1)]
        )
        latest = await weight_col.find_one(
            {"user_id": uid}, sort=[("recorded_at", -1)]
        )
        if first and latest:
            weight_change = round(latest["weight_kg"] - first["weight_kg"], 1)

    # Achievements count
    ach_count = await ach_col.count_documents({"user_id": uid})

    # Last workout
    last_log = await logs_col.find_one(
        {"user_id": uid}, sort=[("completed_at", -1)]
    )

    # Plan completion
    plan_completion = None
    plans_col = Database.get_collection("workout_plans")
    active_plan = await plans_col.find_one(
        {"user_id": uid, "is_active": True}
    )
    if active_plan:
        total_plan_days = active_plan.get("duration_weeks", 4) * active_plan.get("days_per_week", 3)
        completed_days = await logs_col.count_documents(
            {"user_id": uid, "workout_plan_id": str(active_plan["_id"])}
        )
        plan_completion = round((completed_days / max(1, total_plan_days)) * 100, 1)

    return ProgressStats(
        total_workouts=total_workouts,
        total_workout_minutes=total_minutes,
        current_streak=current_streak,
        longest_streak=longest_streak,
        workouts_this_week=workouts_this_week,
        workouts_this_month=workouts_this_month,
        average_difficulty_rating=round(avg_difficulty, 1) if avg_difficulty else None,
        average_energy_rating=round(avg_energy, 1) if avg_energy else None,
        weight_change_kg=weight_change,
        weight_entries_count=weight_count,
        achievements_count=ach_count,
        plan_completion_percent=plan_completion,
        last_workout_at=last_log["completed_at"] if last_log else None,
    )


async def _calculate_streaks(uid: str) -> tuple[int, int]:
    """Calculate current and longest workout streaks.

    A streak is consecutive calendar days with at least one workout.
    """
    logs_col = Database.get_collection("workout_logs")

    # Get all workout dates (unique days), sorted descending
    pipeline = [
        {"$match": {"user_id": uid}},
        {
            "$group": {
                "_id": {
                    "$dateToString": {"format": "%Y-%m-%d", "date": "$completed_at"}
                }
            }
        },
        {"$sort": {"_id": -1}},
    ]

    results = await logs_col.aggregate(pipeline).to_list(365)
    if not results:
        return 0, 0

    dates = sorted(
        [datetime.strptime(r["_id"], "%Y-%m-%d").date() for r in results],
        reverse=True,
    )

    # Calculate current streak
    current_streak = 0
    today = datetime.utcnow().date()

    if dates[0] >= today - timedelta(days=1):
        current_streak = 1
        for i in range(1, len(dates)):
            if dates[i - 1] - dates[i] == timedelta(days=1):
                current_streak += 1
            else:
                break

    # Calculate longest streak
    longest = 1
    current = 1
    for i in range(1, len(dates)):
        if dates[i - 1] - dates[i] == timedelta(days=1):
            current += 1
            longest = max(longest, current)
        else:
            current = 1

    return current_streak, longest


async def _check_workout_achievements(uid: str) -> None:
    """Check and award workout-based achievements."""
    logs_col = Database.get_collection("workout_logs")
    ach_col = Database.get_collection("achievements")

    total = await logs_col.count_documents({"user_id": uid})
    current_streak, _ = await _calculate_streaks(uid)

    achievement_checks = [
        (1, AchievementType.FIRST_WORKOUT, "First Workout! 💪", "You completed your first workout!", "🎯"),
        (10, AchievementType.WORKOUTS_10, "10 Workouts! 🔥", "You've completed 10 workouts!", "🔥"),
        (25, AchievementType.WORKOUTS_25, "25 Workouts! ⭐", "Quarter century of workouts!", "⭐"),
        (50, AchievementType.WORKOUTS_50, "50 Workouts! 🏅", "Half a hundred workouts strong!", "🏅"),
        (100, AchievementType.WORKOUTS_100, "100 Workouts! 🏆", "Triple digit warrior!", "🏆"),
    ]

    for threshold, ach_type, title, desc, icon in achievement_checks:
        if total >= threshold:
            existing = await ach_col.find_one(
                {"user_id": uid, "achievement_type": ach_type.value}
            )
            if not existing:
                achievement = Achievement(
                    user_id=uid,
                    achievement_type=ach_type,
                    title=title,
                    description=desc,
                    icon=icon,
                )
                await ach_col.insert_one(achievement.model_dump())
                logger.info("Achievement unlocked for %s: %s", uid, title)

    # Streak achievements
    streak_checks = [
        (3, AchievementType.STREAK_3, "3-Day Streak! 🔥", "Three days in a row!"),
        (7, AchievementType.STREAK_7, "7-Day Streak! 💎", "A full week streak!"),
        (14, AchievementType.STREAK_14, "14-Day Streak! 🌟", "Two weeks of consistency!"),
        (30, AchievementType.STREAK_30, "30-Day Streak! 👑", "A whole month! Legendary!"),
    ]

    for threshold, ach_type, title, desc in streak_checks:
        if current_streak >= threshold:
            existing = await ach_col.find_one(
                {"user_id": uid, "achievement_type": ach_type.value}
            )
            if not existing:
                achievement = Achievement(
                    user_id=uid,
                    achievement_type=ach_type,
                    title=title,
                    description=desc,
                    icon="🔥",
                )
                await ach_col.insert_one(achievement.model_dump())
                logger.info("Streak achievement unlocked for %s: %s", uid, title)


async def _check_weight_achievement(uid: str, current_weight: float) -> None:
    """Check if the user has reached their weight goal."""
    users_col = Database.get_collection("users")
    ach_col = Database.get_collection("achievements")

    user = await users_col.find_one({"firebase_uid": uid})
    if not user or not user.get("goal_weight_kg"):
        return

    goal = user["goal_weight_kg"]
    initial_weight = user.get("current_weight_kg", current_weight)

    # Check if weight goal is reached (within 0.5 kg)
    if abs(current_weight - goal) <= 0.5:
        existing = await ach_col.find_one(
            {"user_id": uid, "achievement_type": AchievementType.WEIGHT_GOAL_REACHED.value}
        )
        if not existing:
            achievement = Achievement(
                user_id=uid,
                achievement_type=AchievementType.WEIGHT_GOAL_REACHED,
                title="Weight Goal Reached! 🎯",
                description=f"You reached your goal weight of {goal} kg!",
                icon="🎯",
            )
            await ach_col.insert_one(achievement.model_dump())
            logger.info("Weight goal achievement unlocked for %s", uid)
