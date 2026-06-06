"""
Authentication API routes.

Handles user registration (syncing Firebase user to local DB),
login tracking, profile retrieval, and profile updates.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.database import Database
from app.core.security import get_current_user
from app.models.user import (
    UserProfile,
    UserProfileCreate,
    UserProfileResponse,
    UserProfileUpdate,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _serialize_user(doc: dict) -> dict:
    """Convert a MongoDB user document to a serializable dict."""
    doc["_id"] = str(doc["_id"])
    return doc


# ─────────────────────────────────────────────────────────────────────────
#  POST /auth/register – Create or sync user profile
# ─────────────────────────────────────────────────────────────────────────

@router.post(
    "/register",
    response_model=UserProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register or sync a Firebase user",
    description="Creates a local user profile from a Firebase auth token. "
                "If the user already exists, returns the existing profile.",
)
async def register_user(
    current_user: dict = Depends(get_current_user),
):
    """Register a new user or return existing profile."""
    collection = Database.get_collection("users")
    uid = current_user["uid"]

    # Check if user already exists
    existing = await collection.find_one({"firebase_uid": uid})
    if existing:
        logger.info("User %s already registered, returning existing profile", uid)
        return _serialize_user(existing)

    # Create new user profile
    profile = UserProfile(
        firebase_uid=uid,
        email=current_user.get("email"),
        display_name=current_user.get("name"),
        photo_url=current_user.get("picture"),
        last_login_at=datetime.utcnow(),
    )

    result = await collection.insert_one(profile.model_dump())
    created = await collection.find_one({"_id": result.inserted_id})

    logger.info("New user registered: %s (%s)", uid, profile.email)
    return _serialize_user(created)


# ─────────────────────────────────────────────────────────────────────────
#  GET /auth/me – Get current user profile
# ─────────────────────────────────────────────────────────────────────────

@router.get(
    "/me",
    response_model=UserProfileResponse,
    summary="Get current user profile",
)
async def get_my_profile(
    current_user: dict = Depends(get_current_user),
):
    """Retrieve the authenticated user's profile."""
    collection = Database.get_collection("users")
    user = await collection.find_one({"firebase_uid": current_user["uid"]})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found. Please register first.",
        )

    # Update last login timestamp
    await collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_login_at": datetime.utcnow()}},
    )

    return _serialize_user(user)


# ─────────────────────────────────────────────────────────────────────────
#  PATCH /auth/me – Update current user profile
# ─────────────────────────────────────────────────────────────────────────

@router.patch(
    "/me",
    response_model=UserProfileResponse,
    summary="Update current user profile",
)
async def update_my_profile(
    update_data: UserProfileUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Update the authenticated user's profile fields."""
    collection = Database.get_collection("users")

    # Build update dict, excluding None values
    update_fields = update_data.model_dump(exclude_none=True)
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update.",
        )

    update_fields["updated_at"] = datetime.utcnow()

    result = await collection.find_one_and_update(
        {"firebase_uid": current_user["uid"]},
        {"$set": update_fields},
        return_document=True,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found.",
        )

    logger.info("Profile updated for user %s", current_user["uid"])
    return _serialize_user(result)


# ─────────────────────────────────────────────────────────────────────────
#  DELETE /auth/me – Deactivate user account
# ─────────────────────────────────────────────────────────────────────────

@router.delete(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Deactivate user account",
)
async def deactivate_account(
    current_user: dict = Depends(get_current_user),
):
    """Soft-delete the user's account by marking it inactive."""
    collection = Database.get_collection("users")

    result = await collection.find_one_and_update(
        {"firebase_uid": current_user["uid"]},
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
            detail="User profile not found.",
        )

    logger.info("Account deactivated for user %s", current_user["uid"])
    return {"message": "Account deactivated successfully."}


# ─────────────────────────────────────────────────────────────────────────
#  GET /auth/onboarding-status – Check onboarding progress
# ─────────────────────────────────────────────────────────────────────────

@router.get(
    "/onboarding-status",
    summary="Get onboarding status",
)
async def get_onboarding_status(
    current_user: dict = Depends(get_current_user),
):
    """Return the user's current onboarding progress."""
    collection = Database.get_collection("users")
    user = await collection.find_one(
        {"firebase_uid": current_user["uid"]},
        {
            "onboarding_status": 1,
            "assessment_completed": 1,
            "latest_assessment_id": 1,
            "latest_fitness_score_id": 1,
            "active_workout_plan_id": 1,
        },
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return {
        "onboarding_status": user.get("onboarding_status", "pending"),
        "assessment_completed": user.get("assessment_completed", False),
        "has_assessment": user.get("latest_assessment_id") is not None,
        "has_fitness_scores": user.get("latest_fitness_score_id") is not None,
        "has_workout_plan": user.get("active_workout_plan_id") is not None,
    }
