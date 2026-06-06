"""
Fitness scoring engine for CaliForge AI.

Calculates five fitness dimensions (Overall Fitness, Strength,
Recovery, Consistency, Mobility) from assessment data using
weighted scoring formulas, and classifies users into levels.
"""

from __future__ import annotations

import logging
from typing import Dict

from app.models.assessment import AssessmentData
from app.models.fitness import FitnessLevel, FitnessScores

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════
#  SCORE MAPPING TABLES
# ═══════════════════════════════════════════════════════════════════════

PUSHUP_SCORES: Dict[str, float] = {
    "0": 5,
    "1-10": 25,
    "11-20": 50,
    "20+": 95,
}

SQUAT_SCORES: Dict[str, float] = {
    "0": 5,
    "11-20": 25,
    "21-40": 50,
    "40+": 95,
}

PLANK_SCORES: Dict[str, float] = {
    "less_15s": 10,
    "15-30s": 35,
    "30-60s": 65,
    "more_60s": 95,
}

FLEXIBILITY_SCORES: Dict[str, float] = {
    "not_good": 15,
    "not_sure": 25,
    "pretty_flexible": 60,
    "very_flexible": 95,
}

FREQUENCY_SCORES: Dict[str, float] = {
    "none": 5,
    "several_times_month": 35,
    "several_times_week": 65,
    "almost_every_day": 90,
}

ACTIVITY_SCORES: Dict[str, float] = {
    "mostly_sitting": 10,
    "changes_daily": 45,
    "balance": 65,
    "constantly_on_feet": 90,
}

ENERGY_SCORES: Dict[str, float] = {
    "low": 15,
    "fluctuate": 35,
    "steady": 60,
    "high": 90,
}

BUILD_SCORES: Dict[str, float] = {
    "overweight": 20,
    "stocky": 45,
    "medium": 70,
    "slender": 60,
}

BEST_SHAPE_SCORES: Dict[str, float] = {
    "never": 10,
    "more_than_3_years": 30,
    "1_to_2_years": 60,
    "less_than_1_year": 85,
}

TRAINING_PREFERENCE_SCORES: Dict[str, float] = {
    "1-2": 30,
    "3-4": 65,
    "5+": 90,
}

AGE_MOBILITY_MODIFIER: Dict[str, float] = {
    "18_29": 1.0,
    "30_39": 0.95,
    "40_49": 0.85,
    "50_plus": 0.75,
}


# ═══════════════════════════════════════════════════════════════════════
#  LEVEL CLASSIFICATION
# ═══════════════════════════════════════════════════════════════════════

def classify_level(score: float) -> FitnessLevel:
    """Classify a fitness score into a level.

    Args:
        score: Overall fitness score (0–100).

    Returns:
        FitnessLevel enum value.
    """
    if score <= 25:
        return FitnessLevel.BEGINNER
    elif score <= 50:
        return FitnessLevel.NOVICE
    elif score <= 75:
        return FitnessLevel.INTERMEDIATE
    else:
        return FitnessLevel.ADVANCED


# ═══════════════════════════════════════════════════════════════════════
#  SCORING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    """Clamp a value between low and high bounds."""
    return max(low, min(high, value))


def calculate_overall_fitness(data: AssessmentData) -> tuple[float, Dict[str, float]]:
    """Calculate the overall fitness score.

    Weights:
        - Push-up capacity:     20%
        - Squat capacity:       20%
        - Plank hold time:      15%
        - Flexibility:          10%
        - Workout frequency:    15%
        - Daily activity:       10%
        - Energy levels:        10%

    Returns:
        Tuple of (overall_score, component_scores_dict).
    """
    components = {
        "push_up": PUSHUP_SCORES.get(getattr(data, "pushupCapacity", ""), 25),
        "squat": SQUAT_SCORES.get(getattr(data, "squatCapacity", ""), 25),
        "plank": PLANK_SCORES.get(getattr(data, "plankHold", ""), 25),
        "flexibility": FLEXIBILITY_SCORES.get(getattr(data, "flexibility", ""), 25),
        "frequency": FREQUENCY_SCORES.get(getattr(data, "workoutFrequency", ""), 20),
        "activity": ACTIVITY_SCORES.get(getattr(data, "dailyActivity", ""), 25),
        "energy": ENERGY_SCORES.get(getattr(data, "energyLevel", ""), 25),
    }

    overall = (
        components["push_up"] * 0.20
        + components["squat"] * 0.20
        + components["plank"] * 0.15
        + components["flexibility"] * 0.10
        + components["frequency"] * 0.15
        + components["activity"] * 0.10
        + components["energy"] * 0.10
    )

    return _clamp(round(overall, 1)), components


def calculate_strength_score(data: AssessmentData) -> float:
    """Calculate strength score from exercise capacity and build.

    Weights:
        - Push-ups:     30%
        - Squats:       30%
        - Plank:        25%
        - Body build:   15%
    """
    pushup = PUSHUP_SCORES.get(getattr(data, "pushupCapacity", ""), 25)
    squat = SQUAT_SCORES.get(getattr(data, "squatCapacity", ""), 25)
    plank = PLANK_SCORES.get(getattr(data, "plankHold", ""), 25)
    build = BUILD_SCORES.get(getattr(data, "physicalBuild", ""), 50)

    score = pushup * 0.30 + squat * 0.30 + plank * 0.25 + build * 0.15
    return _clamp(round(score, 1))


def calculate_recovery_score(data: AssessmentData) -> float:
    """Calculate recovery score from lifestyle factors.

    Uses: sleep, water intake, eating habits, smoking, alcohol, energy.
    Each factor contributes equally (~16.67%).
    """
    scores = []

    # Sleep (parse from text)
    sleep_score = _parse_sleep_score(getattr(data, "sleepDuration", ""))
    scores.append(sleep_score)

    # Water intake
    water_score = _parse_water_score(getattr(data, "waterIntake", ""))
    scores.append(water_score)

    # Eating habits
    eating_score = _parse_eating_score(str(getattr(data, "eatingHabits", "")))
    scores.append(eating_score)

    # Smoking
    smoking_score = _parse_smoking_score(getattr(data, "smokingStatus", ""))
    scores.append(smoking_score)

    # Alcohol
    alcohol_score = _parse_alcohol_score(getattr(data, "alcoholFrequency", ""))
    scores.append(alcohol_score)

    # Energy
    energy_score = ENERGY_SCORES.get(getattr(data, "energyLevel", ""), 50)
    scores.append(energy_score)

    avg = sum(scores) / len(scores) if scores else 50
    return _clamp(round(avg, 1))


def calculate_consistency_score(data: AssessmentData) -> float:
    """Calculate consistency score from adherence indicators.

    Weights:
        - Workout frequency:        35%
        - Best shape history:       25%
        - Training preference:      25%
        - Obstacles penalty:        15%
    """
    frequency = FREQUENCY_SCORES.get(getattr(data, "workoutFrequency", ""), 20)
    best_shape = BEST_SHAPE_SCORES.get(getattr(data, "bestShape", ""), 30)
    preference = TRAINING_PREFERENCE_SCORES.get(getattr(data, "weeklyTraining", ""), 40)

    # Obstacles penalty (reduce score if user reports obstacles)
    obstacle_penalty = 0
    obstacles = getattr(data, "fitnessObstacles", [])
    if isinstance(obstacles, list) and obstacles:
        text = " ".join(obstacles).lower()
        if any(w in text for w in ["injury", "pain", "health", "medical"]):
            obstacle_penalty = 20
        elif any(w in text for w in ["time", "busy", "work", "lazy", "motivation"]):
            obstacle_penalty = 10
        else:
            obstacle_penalty = 5

    obstacles_score = max(0, 80 - obstacle_penalty)

    score = (
        frequency * 0.35
        + best_shape * 0.25
        + preference * 0.25
        + obstacles_score * 0.15
    )
    return _clamp(round(score, 1))


def calculate_mobility_score(data: AssessmentData) -> float:
    """Calculate mobility score.

    Weights:
        - Flexibility:      40%
        - Daily activity:   25%
        - Age modifier:     Applied as multiplier
        - Limitations:      Penalty per limitation
    """
    flexibility = FLEXIBILITY_SCORES.get(getattr(data, "flexibility", ""), 30)
    activity = ACTIVITY_SCORES.get(getattr(data, "dailyActivity", ""), 30)

    base = flexibility * 0.60 + activity * 0.40

    # Age modifier
    age_mod = AGE_MOBILITY_MODIFIER.get(getattr(data, "ageCategory", ""), 0.9)
    base *= age_mod

    # Limitation penalty
    limitations = getattr(data, "physicalLimitations", [])
    # Filter out "None" limitation
    real_limitations = [l for l in limitations if l != "none"]
    penalty = len(real_limitations) * 8
    base -= penalty

    return _clamp(round(base, 1))


# ═══════════════════════════════════════════════════════════════════════
#  TEXT FIELD PARSERS (for recovery score)
# ═══════════════════════════════════════════════════════════════════════

def _parse_sleep_score(sleep_text: str | None) -> float:
    """Parse sleep duration text into a 0–100 score."""
    if not sleep_text:
        return 50
    text = sleep_text.lower().strip()

    # Try to extract a number
    import re
    numbers = re.findall(r"[\d.]+", text)
    if numbers:
        hours = float(numbers[0])
        if hours >= 8:
            return 90
        elif hours >= 7:
            return 75
        elif hours >= 6:
            return 55
        elif hours >= 5:
            return 35
        else:
            return 15

    # Keyword fallback
    if any(w in text for w in ["great", "enough", "8", "good"]):
        return 80
    elif any(w in text for w in ["okay", "average", "6", "7"]):
        return 55
    elif any(w in text for w in ["bad", "poor", "little", "4", "5"]):
        return 25
    return 50


def _parse_water_score(water_text: str | None) -> float:
    """Parse water intake text into a 0–100 score."""
    if not water_text:
        return 50
    text = water_text.lower().strip()

    import re
    numbers = re.findall(r"[\d.]+", text)
    if numbers:
        liters = float(numbers[0])
        # Normalize based on common units
        if "glass" in text or "cup" in text:
            liters = liters * 0.25  # ~250ml per glass
        if liters >= 3:
            return 90
        elif liters >= 2:
            return 75
        elif liters >= 1:
            return 50
        else:
            return 25

    if any(w in text for w in ["lot", "plenty", "enough", "good"]):
        return 75
    elif any(w in text for w in ["little", "barely", "not enough"]):
        return 25
    return 50


def _parse_eating_score(eating_text: str | None) -> float:
    """Parse eating habits text into a 0–100 score."""
    if not eating_text:
        return 50
    text = eating_text.lower().strip()

    positive = ["healthy", "balanced", "clean", "whole", "protein", "vegetables",
                "meal prep", "nutritious", "home cook"]
    negative = ["junk", "fast food", "skip meals", "irregular", "processed",
                "sugary", "unhealthy", "binge"]

    pos_count = sum(1 for w in positive if w in text)
    neg_count = sum(1 for w in negative if w in text)

    if pos_count > neg_count:
        return min(90, 50 + pos_count * 15)
    elif neg_count > pos_count:
        return max(10, 50 - neg_count * 15)
    return 50


def _parse_smoking_score(smoking_text: str | None) -> float:
    """Parse smoking status into a 0–100 score."""
    if not smoking_text:
        return 80  # Assume non-smoker if not specified
    text = smoking_text.lower().strip()

    if any(w in text for w in ["no", "never", "non", "don't", "quit", "stopped"]):
        return 95
    elif any(w in text for w in ["occasional", "social", "rarely"]):
        return 55
    elif any(w in text for w in ["yes", "daily", "regular", "pack"]):
        return 15
    return 70


def _parse_alcohol_score(alcohol_text: str | None) -> float:
    """Parse alcohol frequency into a 0–100 score."""
    if not alcohol_text:
        return 80
    text = alcohol_text.lower().strip()

    if any(w in text for w in ["no", "never", "none", "don't", "teetotal"]):
        return 95
    elif any(w in text for w in ["occasional", "social", "rarely", "once"]):
        return 70
    elif any(w in text for w in ["weekly", "few times", "weekend"]):
        return 45
    elif any(w in text for w in ["daily", "heavy", "frequent", "every day"]):
        return 15
    return 60


# ═══════════════════════════════════════════════════════════════════════
#  MAIN CALCULATION ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════

def calculate_fitness_scores(data: AssessmentData) -> FitnessScores:
    """Calculate all fitness scores from assessment data.

    This is the main entry point for the fitness engine.

    Args:
        data: Complete assessment data from the user.

    Returns:
        FitnessScores with all five dimensions and level classification.
    """
    overall, components = calculate_overall_fitness(data)
    strength = calculate_strength_score(data)
    recovery = calculate_recovery_score(data)
    consistency = calculate_consistency_score(data)
    mobility = calculate_mobility_score(data)

    level = classify_level(overall)

    # Add dimension scores to components for transparency
    components.update({
        "overall_fitness": overall,
        "strength": strength,
        "recovery": recovery,
        "consistency": consistency,
        "mobility": mobility,
    })

    logger.info(
        "Fitness scores calculated – Overall: %.1f (%s), "
        "Strength: %.1f, Recovery: %.1f, Consistency: %.1f, Mobility: %.1f",
        overall, level.value, strength, recovery, consistency, mobility,
    )

    return FitnessScores(
        overall_fitness=overall,
        strength=strength,
        recovery=recovery,
        consistency=consistency,
        mobility=mobility,
        level=level,
        component_scores=components,
    )
