"""
Fitness scoring and level classification models.

Stores computed fitness metrics derived from assessment data,
including overall fitness, strength, recovery, consistency,
and mobility scores.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, Field


class FitnessLevel(str, Enum):
    """Classification based on overall fitness score."""

    BEGINNER = "Beginner"          # 0–25
    NOVICE = "Novice"              # 26–50
    INTERMEDIATE = "Intermediate"  # 51–75
    ADVANCED = "Advanced"          # 76–100


class FitnessScores(BaseModel):
    """Computed fitness scores (all 0–100 scale).

    These scores are derived deterministically from assessment data
    using weighted scoring formulas in the fitness engine.
    """

    # ── Core Scores ──────────────────────────────────────────────────
    overall_fitness: float = Field(
        ..., ge=0, le=100,
        description="Weighted composite: push-up 20%, squat 20%, plank 15%, "
                    "flexibility 10%, frequency 15%, activity 10%, energy 10%"
    )
    strength: float = Field(
        ..., ge=0, le=100,
        description="Derived from push-ups, squats, plank, and body build"
    )
    recovery: float = Field(
        ..., ge=0, le=100,
        description="Derived from sleep, water, eating, smoking, alcohol, energy"
    )
    consistency: float = Field(
        ..., ge=0, le=100,
        description="Derived from frequency, best shape history, obstacles, preference"
    )
    mobility: float = Field(
        ..., ge=0, le=100,
        description="Derived from flexibility, activity, age, limitations"
    )

    # ── Derived Classification ───────────────────────────────────────
    level: FitnessLevel = Field(
        ..., description="Fitness level classification based on overall score"
    )

    # ── Component Breakdown ──────────────────────────────────────────
    component_scores: Dict[str, float] = Field(
        default_factory=dict,
        description="Individual component scores used in calculations"
    )


class FitnessScoreDocument(BaseModel):
    """Fitness score document stored in MongoDB."""

    user_id: str = Field(..., description="Reference to user's Firebase UID")
    assessment_id: str = Field(..., description="Reference to the assessment used")
    scores: FitnessScores
    calculated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}


class FitnessScoreResponse(BaseModel):
    """Public-facing fitness score response."""

    id: str = Field(..., alias="_id")
    user_id: str
    assessment_id: str
    scores: FitnessScores
    calculated_at: datetime

    model_config = {"populate_by_name": True}


class FitnessOverview(BaseModel):
    """Summary fitness overview returned to the dashboard."""

    overall_fitness: float
    strength: float
    recovery: float
    consistency: float
    mobility: float
    level: FitnessLevel
    level_label: str = Field(
        ..., description="Human-readable level label with emoji"
    )
    insights: list[str] = Field(
        default_factory=list,
        description="Key insights based on scores"
    )

    @staticmethod
    def level_to_label(level: FitnessLevel) -> str:
        labels = {
            FitnessLevel.BEGINNER: "🌱 Beginner",
            FitnessLevel.NOVICE: "🌿 Novice",
            FitnessLevel.INTERMEDIATE: "🌳 Intermediate",
            FitnessLevel.ADVANCED: "🏆 Advanced",
        }
        return labels.get(level, "🌱 Beginner")
