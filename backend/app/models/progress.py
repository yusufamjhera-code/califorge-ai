"""
Progress tracking models for CaliForge AI.

Tracks weight entries, workout completion logs, achievements,
and aggregate progress statistics.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


# ── Weight Tracking ──────────────────────────────────────────────────────


class WeightEntry(BaseModel):
    """A single weight measurement entry."""

    user_id: str
    weight_kg: float = Field(..., ge=20, le=500)
    notes: Optional[str] = Field(None, max_length=500)
    recorded_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}


class WeightEntryCreate(BaseModel):
    """Schema for logging a new weight entry."""

    weight_kg: float = Field(..., ge=20, le=500)
    notes: Optional[str] = Field(None, max_length=500)
    recorded_at: Optional[datetime] = None


class WeightEntryResponse(BaseModel):
    """Public weight entry response."""

    id: str = Field(..., alias="_id")
    user_id: str
    weight_kg: float
    notes: Optional[str] = None
    recorded_at: datetime

    model_config = {"populate_by_name": True}


# ── Workout Logging ─────────────────────────────────────────────────────


class ExerciseLog(BaseModel):
    """Log for a single exercise within a workout."""

    exercise_id: str
    exercise_name: str
    sets_completed: int = Field(default=0, ge=0)
    reps_completed: Optional[int] = Field(None, ge=0)
    duration_seconds: Optional[int] = Field(None, ge=0)
    skipped: bool = False
    notes: Optional[str] = None


class WorkoutLog(BaseModel):
    """Log for a completed workout session."""

    user_id: str
    workout_plan_id: str
    week_number: int = Field(..., ge=1)
    day_number: int = Field(..., ge=1)
    day_of_week: str
    workout_title: str

    exercises: List[ExerciseLog] = Field(default_factory=list)
    total_exercises: int = Field(default=0, ge=0)
    completed_exercises: int = Field(default=0, ge=0)
    skipped_exercises: int = Field(default=0, ge=0)

    duration_minutes: Optional[int] = Field(None, ge=0)
    difficulty_rating: Optional[int] = Field(None, ge=1, le=5, description="1=Easy, 5=Brutal")
    energy_rating: Optional[int] = Field(None, ge=1, le=5, description="1=Low, 5=High")
    notes: Optional[str] = Field(None, max_length=1000)

    completed_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}


class WorkoutLogCreate(BaseModel):
    """Schema for logging a completed workout."""

    workout_plan_id: str
    week_number: int = Field(..., ge=1)
    day_number: int = Field(..., ge=1)
    day_of_week: str
    workout_title: str

    exercises: List[ExerciseLog] = Field(default_factory=list)
    duration_minutes: Optional[int] = Field(None, ge=0)
    difficulty_rating: Optional[int] = Field(None, ge=1, le=5)
    energy_rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = Field(None, max_length=1000)


class WorkoutLogResponse(BaseModel):
    """Public workout log response."""

    id: str = Field(..., alias="_id")
    user_id: str
    workout_plan_id: str
    week_number: int
    day_number: int
    day_of_week: str
    workout_title: str
    exercises: List[ExerciseLog]
    total_exercises: int
    completed_exercises: int
    skipped_exercises: int
    duration_minutes: Optional[int] = None
    difficulty_rating: Optional[int] = None
    energy_rating: Optional[int] = None
    notes: Optional[str] = None
    completed_at: datetime

    model_config = {"populate_by_name": True}


# ── Achievements ─────────────────────────────────────────────────────────


class AchievementType(str, Enum):
    FIRST_WORKOUT = "first_workout"
    STREAK_3 = "streak_3"
    STREAK_7 = "streak_7"
    STREAK_14 = "streak_14"
    STREAK_30 = "streak_30"
    WORKOUTS_10 = "workouts_10"
    WORKOUTS_25 = "workouts_25"
    WORKOUTS_50 = "workouts_50"
    WORKOUTS_100 = "workouts_100"
    WEIGHT_GOAL_REACHED = "weight_goal_reached"
    LEVEL_UP_NOVICE = "level_up_novice"
    LEVEL_UP_INTERMEDIATE = "level_up_intermediate"
    LEVEL_UP_ADVANCED = "level_up_advanced"
    PLAN_COMPLETED = "plan_completed"
    PERFECT_WEEK = "perfect_week"


class Achievement(BaseModel):
    """An achievement unlocked by the user."""

    user_id: str
    achievement_type: AchievementType
    title: str
    description: str
    icon: str = "🏅"
    unlocked_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}


class AchievementResponse(BaseModel):
    """Public achievement response."""

    id: str = Field(..., alias="_id")
    achievement_type: str
    title: str
    description: str
    icon: str
    unlocked_at: datetime

    model_config = {"populate_by_name": True}


# ── Progress Statistics ──────────────────────────────────────────────────


class ProgressStats(BaseModel):
    """Aggregate progress statistics for the dashboard."""

    total_workouts: int = 0
    total_workout_minutes: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    workouts_this_week: int = 0
    workouts_this_month: int = 0
    average_difficulty_rating: Optional[float] = None
    average_energy_rating: Optional[float] = None
    weight_change_kg: Optional[float] = None
    weight_entries_count: int = 0
    achievements_count: int = 0
    plan_completion_percent: Optional[float] = None
    last_workout_at: Optional[datetime] = None


class ProgressOverview(BaseModel):
    """Complete progress overview combining stats and recent activity."""

    stats: ProgressStats
    recent_workouts: List[WorkoutLogResponse] = Field(default_factory=list)
    recent_weight_entries: List[WeightEntryResponse] = Field(default_factory=list)
    achievements: List[AchievementResponse] = Field(default_factory=list)
