"""
Personalized workout plan generator for CaliForge AI.

Builds weekly workout plans based on the user's fitness scores,
assessment data, and exercise database. Incorporates primary goals,
progressive overload across weeks, and targeted zones.
"""

from __future__ import annotations

import logging
import random
from typing import Dict, List, Optional

from app.core.database import Database
from app.models.exercise import ExerciseModel
from app.models.assessment import AssessmentData
from app.models.fitness import FitnessLevel, FitnessScores
from app.models.workout import (
    DailyWorkout,
    DayOfWeek,
    Difficulty,
    ExerciseCategory,
    WeeklySchedule,
    WorkoutExercise,
    WorkoutPlan,
    WorkoutType,
)
# Make sure we can access the progression chain from static data if needed,
# but it's better to fetch from DB for consistency.
from app.data.exercises import get_progression_chain

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════════════════════════

DAYS_OF_WEEK = [
    DayOfWeek.MONDAY,
    DayOfWeek.TUESDAY,
    DayOfWeek.WEDNESDAY,
    DayOfWeek.THURSDAY,
    DayOfWeek.FRIDAY,
    DayOfWeek.SATURDAY,
    DayOfWeek.SUNDAY,
]

# Maps fitness level to exercise difficulty
LEVEL_TO_DIFFICULTY: Dict[FitnessLevel, str] = {
    FitnessLevel.BEGINNER: "Beginner",
    FitnessLevel.NOVICE: "Novice",
    FitnessLevel.INTERMEDIATE: "Intermediate",
    FitnessLevel.ADVANCED: "Advanced",
}

# Training day templates incorporating the new "Pull" category
TRAINING_SPLITS: Dict[int, List[Dict[str, str]]] = {
    2: [
        {"title": "Upper Body", "focus": "Push & Pull", "categories": ["Push", "Pull", "Core"]},
        {"title": "Lower Body & Core", "focus": "Legs & Cond", "categories": ["Legs", "Core", "Conditioning"]},
    ],
    3: [
        {"title": "Upper Body Push", "focus": "Push", "categories": ["Push", "Core"]},
        {"title": "Lower Body", "focus": "Legs", "categories": ["Legs", "Conditioning"]},
        {"title": "Upper Body Pull", "focus": "Pull", "categories": ["Pull", "Core"]},
    ],
    4: [
        {"title": "Push Day", "focus": "Push", "categories": ["Push", "Core"]},
        {"title": "Pull Day", "focus": "Pull", "categories": ["Pull", "Conditioning"]},
        {"title": "Legs Day", "focus": "Legs", "categories": ["Legs", "Core"]},
        {"title": "Full Body", "focus": "Full Body", "categories": ["Push", "Pull", "Legs"]},
    ],
    5: [
        {"title": "Push Focus", "focus": "Push", "categories": ["Push"]},
        {"title": "Pull Focus", "focus": "Pull", "categories": ["Pull"]},
        {"title": "Legs Focus", "focus": "Legs", "categories": ["Legs"]},
        {"title": "Core & Conditioning", "focus": "Core", "categories": ["Core", "Conditioning"]},
        {"title": "Full Body Pump", "focus": "Full Body", "categories": ["Push", "Pull", "Legs"]},
    ],
    6: [
        {"title": "Push A", "focus": "Push", "categories": ["Push", "Core"]},
        {"title": "Pull A", "focus": "Pull", "categories": ["Pull", "Conditioning"]},
        {"title": "Legs A", "focus": "Legs", "categories": ["Legs"]},
        {"title": "Push B", "focus": "Push", "categories": ["Push", "Core"]},
        {"title": "Pull B", "focus": "Pull", "categories": ["Pull", "Conditioning"]},
        {"title": "Legs B", "focus": "Legs", "categories": ["Legs"]},
    ],
}

# Duration mapping (minutes) → approximate exercise count for main section
DURATION_EXERCISE_COUNT: Dict[str, int] = {
    "10-15": 3,
    "15-20": 4,
    "20-25": 6,
    "25+": 8,
    "dont_know": 5,
}

# Sets/Reps baseline by fitness level
LEVEL_SETS: Dict[FitnessLevel, int] = {
    FitnessLevel.BEGINNER: 2,
    FitnessLevel.NOVICE: 3,
    FitnessLevel.INTERMEDIATE: 3,
    FitnessLevel.ADVANCED: 4,
}

LEVEL_REP_MULTIPLIER: Dict[FitnessLevel, float] = {
    FitnessLevel.BEGINNER: 0.6,
    FitnessLevel.NOVICE: 0.8,
    FitnessLevel.INTERMEDIATE: 1.0,
    FitnessLevel.ADVANCED: 1.2,
}


# ═══════════════════════════════════════════════════════════════════════
#  GOAL MODIFIERS
# ═══════════════════════════════════════════════════════════════════════

class GoalModifiers:
    def __init__(self, primary_goal: str):
        self.goal = primary_goal.lower()
        self.rep_mult = 1.0
        self.set_adjust = 0
        self.rest_adjust = 0
        self.difficulty_push = False

        if "muscle" in self.goal or "gain" in self.goal:
            # Hypertrophy focus
            self.rep_mult = 1.2
            self.set_adjust = 1
            self.rest_adjust = 15  # Slightly longer rest for volume
        elif "weight" in self.goal or "lose" in self.goal or "fat" in self.goal:
            # Fat loss focus
            self.rep_mult = 1.5
            self.set_adjust = 0
            self.rest_adjust = -20  # Keep heart rate up
        elif "strength" in self.goal:
            # Strength focus
            self.rep_mult = 0.6
            self.set_adjust = 2
            self.rest_adjust = 45  # Need full recovery between heavy sets
            self.difficulty_push = True
        elif "endurance" in self.goal:
            # Endurance focus
            self.rep_mult = 1.8
            self.set_adjust = -1
            self.rest_adjust = -30

    def apply_sets(self, base_sets: int) -> int:
        return max(1, base_sets + self.set_adjust)

    def apply_reps(self, base_reps: int) -> int:
        return max(3, int(base_reps * self.rep_mult))

    def apply_rest(self, base_rest: int) -> int:
        return max(20, base_rest + self.rest_adjust)


# ═══════════════════════════════════════════════════════════════════════
#  REST PERIOD CALCULATOR
# ═══════════════════════════════════════════════════════════════════════

def _calculate_base_rest_seconds(recovery_score: float, level: FitnessLevel) -> int:
    """Calculate baseline rest period between sets based on recovery score."""
    base_rest = 60
    if recovery_score < 30:
        recovery_adj = 30
    elif recovery_score < 50:
        recovery_adj = 15
    elif recovery_score < 70:
        recovery_adj = 0
    else:
        recovery_adj = -10

    level_adj = {
        FitnessLevel.BEGINNER: 15,
        FitnessLevel.NOVICE: 5,
        FitnessLevel.INTERMEDIATE: -5,
        FitnessLevel.ADVANCED: -15,
    }.get(level, 0)

    rest = base_rest + recovery_adj + level_adj
    return max(20, min(120, rest))


# ═══════════════════════════════════════════════════════════════════════
#  EXERCISE SELECTION
# ═══════════════════════════════════════════════════════════════════════

def _get_user_limitations(data: AssessmentData) -> List[str]:
    limitations = getattr(data, "physicalLimitations", [])
    return [lim for lim in limitations if lim != "none"]


async def _fetch_exercises_by_category(category: str, difficulty: str) -> List[ExerciseModel]:
    """Fetch exercises from MongoDB."""
    collection = Database.get_collection("exercises")
    cursor = collection.find({"category": category, "difficulty": difficulty})
    docs = await cursor.to_list(length=100)
    
    # Fallback to Beginner if no exercises found for the specific difficulty
    if not docs and difficulty != "Beginner":
        cursor = collection.find({"category": category, "difficulty": "Beginner"})
        docs = await cursor.to_list(length=100)
        
    return [ExerciseModel(**doc) for doc in docs]


def _shift_difficulty(difficulty: str, shift: int) -> str:
    """Shift difficulty up or down by a given number of steps."""
    order = ["Beginner", "Novice", "Intermediate", "Advanced"]
    if difficulty not in order:
        return difficulty
    idx = order.index(difficulty)
    new_idx = max(0, min(len(order) - 1, idx + shift))
    return order[new_idx]


async def _select_exercises(
    categories: List[str],
    difficulty: str,
    limitations: List[str],
    target_zones: List[str],
    count: int,
    modifiers: GoalModifiers,
    week_progression_shift: int = 0
) -> List[ExerciseModel]:
    selected: List[ExerciseModel] = []
    seen_ids: set = set()

    # Map zones to categories more comprehensively
    zone_to_category = {
        "Belly": ["Core"],
        "Pecs": ["Push"],
        "Arms": ["Push", "Pull"],
        "Legs": ["Legs"],
        "Back": ["Pull"],
        "Full Body": ["Push", "Pull", "Legs", "Core"],
    }

    prioritized = list(categories)
    for zone in target_zones:
        cats = zone_to_category.get(zone, [])
        for cat in cats:
            if cat in prioritized:
                # Move to front to prioritize
                prioritized.remove(cat)
                prioritized.insert(0, cat)

    # Adjust difficulty based on goal (strength) and weekly progression overload
    target_diff = difficulty
    if modifiers.difficulty_push:
        target_diff = _shift_difficulty(target_diff, 1)
    if week_progression_shift > 0:
        # Every 2 weeks, we might shift difficulty up if possible
        target_diff = _shift_difficulty(target_diff, week_progression_shift // 2)

    for category in prioritized:
        available = await _fetch_exercises_by_category(category, target_diff)
        
        # Filter by limitations
        safe_available = [ex for ex in available if not set(limitations).intersection(set(ex.contraindications))]
        random.shuffle(safe_available)

        for exercise in safe_available:
            if exercise.id not in seen_ids and len(selected) < count:
                selected.append(exercise)
                seen_ids.add(exercise.id)

    # Fill remaining slots if we didn't find enough prioritized exercises
    if len(selected) < count:
        all_categories = ["Push", "Pull", "Legs", "Core", "Conditioning"]
        for cat in all_categories:
            if cat not in categories:
                extras = await _fetch_exercises_by_category(cat, difficulty)
                safe_extras = [ex for ex in extras if not set(limitations).intersection(set(ex.contraindications))]
                random.shuffle(safe_extras)
                for ex in safe_extras:
                    if ex.id not in seen_ids and len(selected) < count:
                        selected.append(ex)
                        seen_ids.add(ex.id)

    return selected[:count]


async def _select_warmup_exercises(limitations: List[str]) -> List[ExerciseModel]:
    warmup: List[ExerciseModel] = []
    seen: set = set()

    mob_exercises = await _fetch_exercises_by_category("Mobility", "Beginner")
    safe_mob = [e for e in mob_exercises if not set(limitations).intersection(set(e.contraindications))]
    random.shuffle(safe_mob)
    
    for ex in safe_mob[:2]:
        if ex.id not in seen:
            warmup.append(ex)
            seen.add(ex.id)

    cond_exercises = await _fetch_exercises_by_category("Conditioning", "Beginner")
    safe_cond = [e for e in cond_exercises if not set(limitations).intersection(set(e.contraindications))]
    random.shuffle(safe_cond)
    
    for ex in safe_cond[:1]:
        if ex.id not in seen:
            warmup.append(ex)
            seen.add(ex.id)

    return warmup


async def _select_cooldown_exercises(limitations: List[str]) -> List[ExerciseModel]:
    cooldown: List[ExerciseModel] = []
    seen: set = set()

    mob_exercises = await _fetch_exercises_by_category("Mobility", "Beginner")
    safe_mob = [e for e in mob_exercises if not set(limitations).intersection(set(e.contraindications))]
    random.shuffle(safe_mob)

    for ex in safe_mob[:3]:
        if ex.id not in seen:
            cooldown.append(ex)
            seen.add(ex.id)

    return cooldown


# ═══════════════════════════════════════════════════════════════════════
#  WORKOUT EXERCISE BUILDER
# ═══════════════════════════════════════════════════════════════════════

def _build_workout_exercise(
    exercise: ExerciseModel,
    section: WorkoutType,
    level: FitnessLevel,
    base_rest: int,
    order: int,
    modifiers: GoalModifiers,
    week_number: int,
) -> WorkoutExercise:
    
    # Weekly progressive overload: increase base sets/reps slightly over time
    week_multiplier = 1.0 + (week_number - 1) * 0.05  # 5% increase per week

    base_level_sets = LEVEL_SETS.get(level, 3)
    base_level_rep_mult = LEVEL_REP_MULTIPLIER.get(level, 1.0) * week_multiplier

    sets = modifiers.apply_sets(base_level_sets)
    rest_seconds = modifiers.apply_rest(base_rest)

    if section == WorkoutType.WARMUP or section == WorkoutType.COOLDOWN:
        sets = 1
        rest_seconds = 15

    reps = None
    duration = None
    
    if exercise.is_timed:
        base_dur = exercise.default_duration_seconds or 30
        dur_target = int(base_dur * base_level_rep_mult)
        duration = max(10, modifiers.apply_reps(dur_target)) # Use apply_reps for duration scaling too
    else:
        base_reps_target = exercise.default_reps or 10
        rep_target = int(base_reps_target * base_level_rep_mult)
        reps = max(3, modifiers.apply_reps(rep_target))

    if section in (WorkoutType.WARMUP, WorkoutType.COOLDOWN):
        if reps:
            reps = max(5, reps)
        if duration:
            duration = max(15, duration)

    return WorkoutExercise(
        exercise_id=exercise.id,
        name=exercise.name,
        category=ExerciseCategory(exercise.category),
        section=section,
        sets=sets,
        reps=reps,
        duration_seconds=duration,
        rest_seconds=rest_seconds,
        notes=exercise.coaching_cues[0] if exercise.coaching_cues else None,
        difficulty=Difficulty(exercise.difficulty),
        order=order,
    )


# ═══════════════════════════════════════════════════════════════════════
#  DAILY WORKOUT BUILDER
# ═══════════════════════════════════════════════════════════════════════

async def _build_daily_workout(
    day: DayOfWeek,
    day_number: int,
    template: Dict[str, str],
    data: AssessmentData,
    scores: FitnessScores,
    main_exercise_count: int,
    modifiers: GoalModifiers,
    week_number: int,
) -> DailyWorkout:
    limitations = _get_user_limitations(data)
    difficulty = LEVEL_TO_DIFFICULTY.get(scores.level, "Beginner")
    base_rest = _calculate_base_rest_seconds(scores.recovery, scores.level)
    target_zones = getattr(data, "targetZone", [])

    order_counter = 0

    # Warmup
    warmup_raw = await _select_warmup_exercises(limitations)
    warmup_exercises = []
    for ex in warmup_raw:
        we = _build_workout_exercise(ex, WorkoutType.WARMUP, scores.level, 15, order_counter, modifiers, week_number)
        warmup_exercises.append(we)
        order_counter += 1

    # Main exercises
    categories = template.get("categories", ["Push", "Pull", "Legs", "Core"])
    
    # progressive shift
    week_progression_shift = max(0, week_number - 1)
    
    main_raw = await _select_exercises(
        categories, difficulty, limitations, target_zones, main_exercise_count, modifiers, week_progression_shift
    )
    main_exercises = []
    for ex in main_raw:
        we = _build_workout_exercise(ex, WorkoutType.MAIN, scores.level, base_rest, order_counter, modifiers, week_number)
        main_exercises.append(we)
        order_counter += 1

    # Cooldown
    cooldown_raw = await _select_cooldown_exercises(limitations)
    cooldown_exercises = []
    for ex in cooldown_raw:
        we = _build_workout_exercise(ex, WorkoutType.COOLDOWN, scores.level, 15, order_counter, modifiers, week_number)
        cooldown_exercises.append(we)
        order_counter += 1

    total_exercises = len(warmup_exercises) + len(main_exercises) + len(cooldown_exercises)
    avg_rest = modifiers.apply_rest(base_rest)
    avg_sets = modifiers.apply_sets(LEVEL_SETS.get(scores.level, 3))
    
    est_duration = total_exercises * 3 + len(main_exercises) * (avg_rest // 60) * avg_sets

    return DailyWorkout(
        day=day,
        day_number=day_number,
        title=template["title"],
        focus=template["focus"],
        is_rest_day=False,
        estimated_duration_minutes=max(15, min(90, est_duration)),
        exercises=main_exercises,
        warmup_exercises=warmup_exercises,
        cooldown_exercises=cooldown_exercises,
    )


def _build_rest_day(day: DayOfWeek, day_number: int) -> DailyWorkout:
    return DailyWorkout(
        day=day,
        day_number=day_number,
        title="Rest & Recovery",
        focus="Active Recovery",
        is_rest_day=True,
        estimated_duration_minutes=0,
        exercises=[],
        warmup_exercises=[],
        cooldown_exercises=[],
    )


# ═══════════════════════════════════════════════════════════════════════
#  WEEKLY SCHEDULE BUILDER
# ═══════════════════════════════════════════════════════════════════════

def _get_training_days(days_per_week: int) -> List[int]:
    if days_per_week >= 7: return list(range(7))
    if days_per_week == 6: return [0, 1, 2, 3, 4, 5]
    if days_per_week == 5: return [0, 1, 2, 3, 4]
    if days_per_week == 4: return [0, 1, 3, 4]
    if days_per_week == 3: return [0, 2, 4]
    if days_per_week == 2: return [0, 3]
    return [0]


async def _build_weekly_schedule(
    week_number: int,
    data: AssessmentData,
    scores: FitnessScores,
    days_per_week: int,
    main_exercise_count: int,
    modifiers: GoalModifiers,
) -> WeeklySchedule:
    training_day_indices = _get_training_days(days_per_week)
    templates = TRAINING_SPLITS.get(days_per_week, TRAINING_SPLITS[3])

    days: List[DailyWorkout] = []
    template_idx = 0

    for day_idx in range(7):
        day_enum = DAYS_OF_WEEK[day_idx]
        day_number = day_idx + 1

        if day_idx in training_day_indices:
            template = templates[template_idx % len(templates)]
            workout = await _build_daily_workout(
                day_enum, day_number, template, data, scores, main_exercise_count, modifiers, week_number
            )
            days.append(workout)
            template_idx += 1
        else:
            days.append(_build_rest_day(day_enum, day_number))

    # Add a progression note based on the week
    note = f"Week {week_number} – "
    if week_number == 1:
        note += "Focus on learning proper form and building a habit."
    elif week_number == 2:
        note += "Slight increase in volume. Push yourself for those extra reps."
    elif week_number == 3:
        note += "Volume and intensity peak. You might see some harder exercise variations."
    else:
        note += "Final stretch! Give it everything you have."

    return WeeklySchedule(
        week_number=week_number,
        days=days,
        notes=note,
    )


# ═══════════════════════════════════════════════════════════════════════
#  MAIN GENERATOR ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════

async def generate_workout_plan(
    user_id: str,
    assessment_id: str,
    fitness_score_id: str,
    data: AssessmentData,
    scores: FitnessScores,
    duration_weeks: int = 4,
) -> WorkoutPlan:
    # Determine days per week based on preference
    pref = getattr(data, "weeklyTraining", "")
    if pref == "1-2":
        days_per_week = 2
    elif pref == "3-4":
        days_per_week = 3  # Adjusted to standard 3 day split for 3-4
    else:
        days_per_week = 5

    # Determine exercise count based on requested duration
    main_exercise_count = DURATION_EXERCISE_COUNT.get(getattr(data, "workoutDuration", ""), 5)

    # Initialize goal modifiers from assessment data
    primary_goal = getattr(data, "primaryGoal", "general_fitness")
    modifiers = GoalModifiers(primary_goal)

    weekly_schedules: List[WeeklySchedule] = []
    for week in range(1, duration_weeks + 1):
        schedule = await _build_weekly_schedule(
            week, data, scores, days_per_week, main_exercise_count, modifiers
        )
        weekly_schedules.append(schedule)

    level_name = scores.level.value
    
    # Format the title nicely
    formatted_goal = primary_goal.replace("_", " ").title()
    title = f"{level_name} {formatted_goal} Plan – {days_per_week} Days/Week"
    
    description = (
        f"A personalized {duration_weeks}-week {level_name.lower()} calisthenics program "
        f"designed to optimize for {formatted_goal}. "
        f"Focus areas: {', '.join(getattr(data, 'targetZone', [])) if getattr(data, 'targetZone', []) else 'Full Body'}."
    )

    plan = WorkoutPlan(
        user_id=user_id,
        assessment_id=assessment_id,
        fitness_score_id=fitness_score_id,
        title=title,
        description=description,
        difficulty=Difficulty(LEVEL_TO_DIFFICULTY[scores.level]),
        duration_weeks=duration_weeks,
        days_per_week=days_per_week,
        weekly_schedules=weekly_schedules,
    )

    logger.info(
        "Generated %d-week workout plan for user %s: %s (Goal: %s, %d days/week)",
        duration_weeks, user_id, title, primary_goal, days_per_week
    )

    return plan
