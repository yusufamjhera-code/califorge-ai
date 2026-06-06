"""
Adaptive progression engine for CaliForge AI.

Analyzes workout logs to determine when a user is ready to
progress (or regress) exercise difficulty, and adjusts future
workouts accordingly.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from app.data.exercises import EXERCISES, get_progression_chain
from app.models.fitness import FitnessLevel, FitnessScores
from app.models.progress import ExerciseLog, WorkoutLog
from app.models.workout import (
    DailyWorkout,
    Difficulty,
    WorkoutExercise,
    WorkoutPlan,
)

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════
#  CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════

# Number of consecutive successful completions needed to progress
PROGRESSION_THRESHOLD = 3

# Number of consecutive skips/failures needed to regress
REGRESSION_THRESHOLD = 2

# Minimum completion ratio for a workout to be "successful"
MIN_COMPLETION_RATIO = 0.75

# Difficulty rating thresholds
EASY_THRESHOLD = 2  # Rating ≤ 2 means "too easy"
HARD_THRESHOLD = 4  # Rating ≥ 4 means "too hard"

# Rep increase per progression step
REP_INCREMENT = 2
SET_INCREMENT = 1
DURATION_INCREMENT = 5  # seconds


# ═══════════════════════════════════════════════════════════════════════
#  ANALYSIS TYPES
# ═══════════════════════════════════════════════════════════════════════

class ProgressionRecommendation:
    """Recommendation for how to adjust an exercise or workout."""

    def __init__(
        self,
        exercise_id: str,
        exercise_name: str,
        action: str,  # "progress", "regress", "increase_volume", "decrease_volume", "maintain"
        reason: str,
        new_exercise_id: Optional[str] = None,
        new_exercise_name: Optional[str] = None,
        new_reps: Optional[int] = None,
        new_sets: Optional[int] = None,
        new_duration: Optional[int] = None,
    ):
        self.exercise_id = exercise_id
        self.exercise_name = exercise_name
        self.action = action
        self.reason = reason
        self.new_exercise_id = new_exercise_id
        self.new_exercise_name = new_exercise_name
        self.new_reps = new_reps
        self.new_sets = new_sets
        self.new_duration = new_duration

    def to_dict(self) -> dict:
        return {
            "exercise_id": self.exercise_id,
            "exercise_name": self.exercise_name,
            "action": self.action,
            "reason": self.reason,
            "new_exercise_id": self.new_exercise_id,
            "new_exercise_name": self.new_exercise_name,
            "new_reps": self.new_reps,
            "new_sets": self.new_sets,
            "new_duration": self.new_duration,
        }


class WorkoutAnalysis:
    """Overall analysis of recent workout performance."""

    def __init__(
        self,
        overall_trend: str,  # "improving", "plateauing", "declining"
        avg_completion_rate: float,
        avg_difficulty_rating: Optional[float],
        recommendations: List[ProgressionRecommendation],
        should_advance_week: bool = False,
        message: str = "",
    ):
        self.overall_trend = overall_trend
        self.avg_completion_rate = avg_completion_rate
        self.avg_difficulty_rating = avg_difficulty_rating
        self.recommendations = recommendations
        self.should_advance_week = should_advance_week
        self.message = message

    def to_dict(self) -> dict:
        return {
            "overall_trend": self.overall_trend,
            "avg_completion_rate": round(self.avg_completion_rate, 2),
            "avg_difficulty_rating": (
                round(self.avg_difficulty_rating, 1)
                if self.avg_difficulty_rating
                else None
            ),
            "recommendations": [r.to_dict() for r in self.recommendations],
            "should_advance_week": self.should_advance_week,
            "message": self.message,
        }


# ═══════════════════════════════════════════════════════════════════════
#  EXERCISE-LEVEL ANALYSIS
# ═══════════════════════════════════════════════════════════════════════

def _analyze_exercise_performance(
    exercise_id: str,
    logs: List[ExerciseLog],
) -> Optional[ProgressionRecommendation]:
    """Analyze performance on a single exercise across multiple workouts.

    Args:
        exercise_id: The exercise being analyzed.
        logs: Recent ExerciseLog entries for this exercise.

    Returns:
        A ProgressionRecommendation if a change is warranted, else None.
    """
    if not logs:
        return None

    exercise = EXERCISES.get(exercise_id)
    if not exercise:
        return None

    # Count successes and skips
    successful = sum(1 for log in logs if not log.skipped and log.sets_completed > 0)
    skipped = sum(1 for log in logs if log.skipped)
    total = len(logs)

    completion_rate = successful / total if total > 0 else 0

    # Check for progression
    if successful >= PROGRESSION_THRESHOLD and completion_rate >= MIN_COMPLETION_RATIO:
        # Check if there's a harder progression available
        if exercise.progression_to and exercise.progression_to in EXERCISES:
            next_exercise = EXERCISES[exercise.progression_to]
            return ProgressionRecommendation(
                exercise_id=exercise_id,
                exercise_name=exercise.name,
                action="progress",
                reason=f"Consistently completed {exercise.name} in {successful}/{total} sessions. "
                       f"Ready to advance to {next_exercise.name}.",
                new_exercise_id=next_exercise.id,
                new_exercise_name=next_exercise.name,
            )
        else:
            # No progression available – increase volume
            return ProgressionRecommendation(
                exercise_id=exercise_id,
                exercise_name=exercise.name,
                action="increase_volume",
                reason=f"Mastering {exercise.name}. Increasing volume for continued progress.",
                new_reps=(exercise.default_reps or 10) + REP_INCREMENT if not exercise.is_timed else None,
                new_duration=(exercise.default_duration_seconds or 30) + DURATION_INCREMENT if exercise.is_timed else None,
                new_sets=(exercise.default_sets or 3) + SET_INCREMENT,
            )

    # Check for regression
    if skipped >= REGRESSION_THRESHOLD:
        if exercise.progression_from and exercise.progression_from in EXERCISES:
            prev_exercise = EXERCISES[exercise.progression_from]
            return ProgressionRecommendation(
                exercise_id=exercise_id,
                exercise_name=exercise.name,
                action="regress",
                reason=f"Struggling with {exercise.name} (skipped {skipped}/{total} times). "
                       f"Stepping back to {prev_exercise.name} to build foundation.",
                new_exercise_id=prev_exercise.id,
                new_exercise_name=prev_exercise.name,
            )
        else:
            return ProgressionRecommendation(
                exercise_id=exercise_id,
                exercise_name=exercise.name,
                action="decrease_volume",
                reason=f"Finding {exercise.name} challenging. Reducing volume to improve form.",
                new_reps=max(3, (exercise.default_reps or 10) - REP_INCREMENT) if not exercise.is_timed else None,
                new_duration=max(10, (exercise.default_duration_seconds or 30) - DURATION_INCREMENT) if exercise.is_timed else None,
            )

    return None


# ═══════════════════════════════════════════════════════════════════════
#  WORKOUT-LEVEL ANALYSIS
# ═══════════════════════════════════════════════════════════════════════

def analyze_recent_performance(
    workout_logs: List[WorkoutLog],
    current_plan: Optional[WorkoutPlan] = None,
) -> WorkoutAnalysis:
    """Analyze recent workout logs to generate progression recommendations.

    Args:
        workout_logs: Recent workout logs (newest first), typically last 7–14 days.
        current_plan: The current active workout plan for context.

    Returns:
        WorkoutAnalysis with trend, stats, and per-exercise recommendations.
    """
    if not workout_logs:
        return WorkoutAnalysis(
            overall_trend="insufficient_data",
            avg_completion_rate=0,
            avg_difficulty_rating=None,
            recommendations=[],
            message="Not enough workout data to analyze. Keep training!",
        )

    # Calculate aggregate stats
    completion_rates = []
    difficulty_ratings = []
    exercise_logs_by_id: Dict[str, List[ExerciseLog]] = {}

    for log in workout_logs:
        if log.total_exercises > 0:
            rate = log.completed_exercises / log.total_exercises
            completion_rates.append(rate)

        if log.difficulty_rating is not None:
            difficulty_ratings.append(log.difficulty_rating)

        for ex_log in log.exercises:
            if ex_log.exercise_id not in exercise_logs_by_id:
                exercise_logs_by_id[ex_log.exercise_id] = []
            exercise_logs_by_id[ex_log.exercise_id].append(ex_log)

    avg_completion = sum(completion_rates) / len(completion_rates) if completion_rates else 0
    avg_difficulty = (
        sum(difficulty_ratings) / len(difficulty_ratings)
        if difficulty_ratings
        else None
    )

    # Determine overall trend
    if len(completion_rates) >= 3:
        recent = completion_rates[:3]
        older = completion_rates[3:6] if len(completion_rates) > 3 else completion_rates[:3]
        recent_avg = sum(recent) / len(recent)
        older_avg = sum(older) / len(older)

        if recent_avg > older_avg + 0.05:
            trend = "improving"
        elif recent_avg < older_avg - 0.05:
            trend = "declining"
        else:
            trend = "plateauing"
    elif avg_completion >= MIN_COMPLETION_RATIO:
        trend = "improving"
    else:
        trend = "building_foundation"

    # Analyze each exercise
    recommendations: List[ProgressionRecommendation] = []
    for exercise_id, ex_logs in exercise_logs_by_id.items():
        rec = _analyze_exercise_performance(exercise_id, ex_logs)
        if rec:
            recommendations.append(rec)

    # Check if user should advance to next week
    should_advance = (
        avg_completion >= MIN_COMPLETION_RATIO
        and len(workout_logs) >= 2
        and trend in ("improving", "plateauing")
    )

    # Build message
    if trend == "improving":
        message = "🚀 Great progress! You're consistently completing workouts and getting stronger."
    elif trend == "plateauing":
        message = "💪 You're maintaining well! Consider pushing for progression on key exercises."
    elif trend == "declining":
        message = "📉 Recent workouts have been tougher. Consider extra rest or reducing intensity."
    else:
        message = "🌱 Building your foundation – focus on consistency and form."

    if avg_difficulty is not None:
        if avg_difficulty <= EASY_THRESHOLD:
            message += " Workouts feel easy – ready to level up!"
        elif avg_difficulty >= HARD_THRESHOLD:
            message += " Workouts feel very challenging – that's okay, recovery is key."

    return WorkoutAnalysis(
        overall_trend=trend,
        avg_completion_rate=avg_completion,
        avg_difficulty_rating=avg_difficulty,
        recommendations=recommendations,
        should_advance_week=should_advance,
        message=message,
    )


# ═══════════════════════════════════════════════════════════════════════
#  PLAN ADJUSTMENT
# ═══════════════════════════════════════════════════════════════════════

def apply_recommendations(
    plan: WorkoutPlan,
    recommendations: List[ProgressionRecommendation],
) -> Tuple[WorkoutPlan, List[str]]:
    """Apply progression recommendations to a workout plan.

    Modifies exercise selections, sets, reps, and durations
    in the plan's future weeks based on recommendations.

    Args:
        plan: The current workout plan.
        recommendations: List of recommendations to apply.

    Returns:
        Tuple of (updated_plan, list_of_changes_applied).
    """
    changes: List[str] = []
    rec_map = {r.exercise_id: r for r in recommendations}

    for schedule in plan.weekly_schedules:
        if schedule.week_number <= plan.current_week:
            continue  # Only modify future weeks

        for day in schedule.days:
            if day.is_rest_day:
                continue

            all_exercises = day.exercises + day.warmup_exercises + day.cooldown_exercises
            for i, ex in enumerate(all_exercises):
                rec = rec_map.get(ex.exercise_id)
                if not rec:
                    continue

                if rec.action == "progress" and rec.new_exercise_id:
                    new_ex = EXERCISES.get(rec.new_exercise_id)
                    if new_ex:
                        ex.exercise_id = new_ex.id
                        ex.name = new_ex.name
                        ex.difficulty = Difficulty(new_ex.difficulty)
                        if new_ex.is_timed:
                            ex.reps = None
                            ex.duration_seconds = new_ex.default_duration_seconds
                        else:
                            ex.reps = new_ex.default_reps
                            ex.duration_seconds = None
                        changes.append(f"Progressed from {rec.exercise_name} → {new_ex.name}")

                elif rec.action == "regress" and rec.new_exercise_id:
                    new_ex = EXERCISES.get(rec.new_exercise_id)
                    if new_ex:
                        ex.exercise_id = new_ex.id
                        ex.name = new_ex.name
                        ex.difficulty = Difficulty(new_ex.difficulty)
                        if new_ex.is_timed:
                            ex.reps = None
                            ex.duration_seconds = new_ex.default_duration_seconds
                        else:
                            ex.reps = new_ex.default_reps
                            ex.duration_seconds = None
                        changes.append(f"Stepped back from {rec.exercise_name} → {new_ex.name}")

                elif rec.action == "increase_volume":
                    if rec.new_reps and ex.reps:
                        ex.reps = rec.new_reps
                    if rec.new_duration and ex.duration_seconds:
                        ex.duration_seconds = rec.new_duration
                    if rec.new_sets:
                        ex.sets = min(5, rec.new_sets)
                    changes.append(f"Increased volume for {ex.name}")

                elif rec.action == "decrease_volume":
                    if rec.new_reps and ex.reps:
                        ex.reps = rec.new_reps
                    if rec.new_duration and ex.duration_seconds:
                        ex.duration_seconds = rec.new_duration
                    changes.append(f"Decreased volume for {ex.name}")

    logger.info("Applied %d progression adjustments to plan", len(changes))
    return plan, changes
