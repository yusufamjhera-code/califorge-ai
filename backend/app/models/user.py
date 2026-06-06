"""
User profile model for CaliForge AI.

Stores user metadata synced from Firebase Auth along with
profile preferences and onboarding state.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class OnboardingStatus(str, Enum):
    PENDING = "pending"
    ASSESSMENT_STARTED = "assessment_started"
    ASSESSMENT_COMPLETED = "assessment_completed"
    PLAN_GENERATED = "plan_generated"
    COMPLETED = "completed"


class UserProfile(BaseModel):
    """Complete user profile document stored in MongoDB."""

    firebase_uid: str = Field(..., description="Firebase Authentication UID")
    email: Optional[EmailStr] = Field(None, description="User email address")
    display_name: Optional[str] = Field(None, max_length=100, description="Display name")
    photo_url: Optional[str] = Field(None, description="Profile photo URL")
    gender: Optional[Gender] = None
    age: Optional[int] = Field(None, ge=13, le=120, description="User's actual age")
    height_cm: Optional[float] = Field(None, ge=50, le=300, description="Height in cm")
    current_weight_kg: Optional[float] = Field(None, ge=20, le=500, description="Current weight in kg")
    goal_weight_kg: Optional[float] = Field(None, ge=20, le=500, description="Goal weight in kg")

    # Onboarding
    onboarding_status: OnboardingStatus = OnboardingStatus.PENDING
    assessment_completed: bool = False
    latest_assessment_id: Optional[str] = None
    latest_fitness_score_id: Optional[str] = None
    active_workout_plan_id: Optional[str] = None

    # Preferences
    preferred_units: str = Field(default="metric", pattern=r"^(metric|imperial)$")
    notification_enabled: bool = True
    dark_mode: bool = False

    # Metadata
    is_admin: bool = False
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login_at: Optional[datetime] = None

    model_config = {"populate_by_name": True}


class UserProfileCreate(BaseModel):
    """Schema for creating a new user profile."""

    firebase_uid: str
    email: Optional[EmailStr] = None
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
    gender: Optional[Gender] = None


class UserProfileUpdate(BaseModel):
    """Schema for updating an existing user profile."""

    display_name: Optional[str] = Field(None, max_length=100)
    photo_url: Optional[str] = None
    gender: Optional[Gender] = None
    age: Optional[int] = Field(None, ge=13, le=120)
    height_cm: Optional[float] = Field(None, ge=50, le=300)
    current_weight_kg: Optional[float] = Field(None, ge=20, le=500)
    goal_weight_kg: Optional[float] = Field(None, ge=20, le=500)
    preferred_units: Optional[str] = Field(None, pattern=r"^(metric|imperial)$")
    notification_enabled: Optional[bool] = None
    dark_mode: Optional[bool] = None


class UserProfileResponse(BaseModel):
    """Public-facing user profile response."""

    id: str = Field(..., alias="_id")
    firebase_uid: str
    email: Optional[str] = None
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    height_cm: Optional[float] = None
    current_weight_kg: Optional[float] = None
    goal_weight_kg: Optional[float] = None
    onboarding_status: str
    assessment_completed: bool
    preferred_units: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"populate_by_name": True}
