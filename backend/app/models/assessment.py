"""
Assessment data model for CaliForge AI.

Captures all 36 assessment questions covering fitness level,
lifestyle, goals, body metrics, and health information.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class AssessmentData(BaseModel):
    """All 36 assessment fields captured during user onboarding.
    Accepts arbitrary key-value pairs from the dynamic frontend questionnaire.
    """
    model_config = {"extra": "allow"}

    # We can still keep the explicit numeric fields for easy access by other services:
    height_cm: Optional[float] = None
    current_weight_kg: Optional[float] = None
    goal_weight_kg: Optional[float] = None
    actual_age: Optional[int] = None
    gender: Optional[str] = None


class AssessmentDocument(BaseModel):
    """Full assessment document as stored in MongoDB."""

    user_id: str = Field(..., description="Reference to user's Firebase UID")
    data: AssessmentData
    is_latest: bool = Field(default=True, description="Whether this is the latest assessment")
    version: int = Field(default=1, description="Assessment version for tracking changes")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}


class AssessmentCreate(BaseModel):
    """Schema for submitting a new assessment."""

    data: AssessmentData


class AssessmentResponse(BaseModel):
    """Public-facing assessment response."""

    id: str = Field(..., alias="_id")
    user_id: str
    data: AssessmentData
    is_latest: bool
    version: int
    created_at: datetime
    updated_at: datetime

    model_config = {"populate_by_name": True}
