"""
Workout plan models for CaliForge AI.

Defines the complete hierarchy: WorkoutPlan → WeeklySchedule
→ DailyWorkout → WorkoutExercise, along with schemas for
plan generation and management.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


# ── Enums ────────────────────────────────────────────────────────────────


class ExerciseCategory(str, Enum):
    PUSH = "Push"
    PULL = "Pull"
    LEGS = "Legs"
    CORE = "Core"
    CONDITIONING = "Conditioning"
    MOBILITY = "Mobility"


class Difficulty(str, Enum):
    BEGINNER = "Beginner"
    NOVICE = "Novice"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


class WorkoutType(str, Enum):
    WARMUP = "Warmup"
    MAIN = "Main"
    COOLDOWN = "Cooldown"


class DayOfWeek(str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"


class PlanStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


# ── Exercise in a Workout ───────────────────────────────────────────────


class WorkoutExercise(BaseModel):
    """A single exercise within a workout, with prescribed volume."""

    exercise_id: str = Field(..., description="Reference to exercise database ID")
    name: str = Field(..., description="Exercise display name")
    category: ExerciseCategory
    section: WorkoutType = Field(..., description="Warmup, Main, or Cooldown")
    sets: int = Field(..., ge=1, le=10, description="Number of sets")
    reps: Optional[int] = Field(None, ge=1, le=100, description="Reps per set (if applicable)")
    duration_seconds: Optional[int] = Field(
        None, ge=5, le=300, description="Hold/duration in seconds (for timed exercises)"
    )
    rest_seconds: int = Field(
        default=60, ge=10, le=300, description="Rest between sets in seconds"
    )
    notes: Optional[str] = Field(None, description="Coaching notes or form cues")
    difficulty: Difficulty = Difficulty.BEGINNER
    order: int = Field(..., ge=0, description="Exercise order within the workout")


# ── Daily Workout ────────────────────────────────────────────────────────


class DailyWorkout(BaseModel):
    """A single day's complete workout session."""

    day: DayOfWeek
    day_number: int = Field(..., ge=1, le=7, description="Day number in the week (1-7)")
    title: str = Field(..., description="Workout title, e.g. 'Upper Body Push'")
    focus: str = Field(..., description="Primary focus area")
    is_rest_day: bool = False
    estimated_duration_minutes: int = Field(
        default=30, ge=0, le=120,
        description="Estimated total duration including rest (0 for rest days)"
    )
    exercises: List[WorkoutExercise] = Field(default_factory=list)
    warmup_exercises: List[WorkoutExercise] = Field(default_factory=list)
    cooldown_exercises: List[WorkoutExercise] = Field(default_factory=list)


# ── Weekly Schedule ──────────────────────────────────────────────────────


class WeeklySchedule(BaseModel):
    """One week of workouts within a plan."""

    week_number: int = Field(..., ge=1, description="Week number in the plan")
    days: List[DailyWorkout] = Field(default_factory=list)
    notes: Optional[str] = None


# ── Workout Plan ─────────────────────────────────────────────────────────


class WorkoutPlan(BaseModel):
    """Complete workout plan generated for a user."""

    user_id: str = Field(..., description="Reference to user's Firebase UID")
    assessment_id: str = Field(..., description="Assessment used to generate this plan")
    fitness_score_id: str = Field(..., description="Fitness scores used to generate this plan")

    title: str = Field(default="Personalized Calisthenics Plan")
    description: Optional[str] = None
    difficulty: Difficulty = Difficulty.BEGINNER
    duration_weeks: int = Field(default=4, ge=1, le=12, description="Plan duration in weeks")
    days_per_week: int = Field(default=3, ge=1, le=7)

    weekly_schedules: List[WeeklySchedule] = Field(default_factory=list)

    # ── State ────────────────────────────────────────────────────────
    status: PlanStatus = PlanStatus.ACTIVE
    is_active: bool = True
    current_week: int = Field(default=1, ge=1)
    current_day: int = Field(default=1, ge=1)

    # ── Metadata ─────────────────────────────────────────────────────
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    model_config = {"populate_by_name": True}


class WorkoutPlanResponse(BaseModel):
    """Public-facing workout plan response."""

    id: str = Field(..., alias="_id")
    user_id: str
    title: str
    description: Optional[str] = None
    difficulty: str
    duration_weeks: int
    days_per_week: int
    weekly_schedules: List[WeeklySchedule]
    status: str
    is_active: bool
    current_week: int
    current_day: int
    created_at: datetime
    updated_at: datetime

    model_config = {"populate_by_name": True}


class WorkoutPlanSummary(BaseModel):
    """Lightweight plan summary for listings."""

    id: str = Field(..., alias="_id")
    title: str
    difficulty: str
    duration_weeks: int
    days_per_week: int
    status: str
    is_active: bool
    current_week: int
    created_at: datetime

    model_config = {"populate_by_name": True}
