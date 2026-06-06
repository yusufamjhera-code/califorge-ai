"""
Assessment API routes.

Handles creating, retrieving, and managing user assessments.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.database import Database
from app.core.security import get_current_user
from app.models.assessment import (
    AssessmentCreate,
    AssessmentDocument,
    AssessmentResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/assessments", tags=["Assessment"])


def _serialize(doc: dict) -> dict:
    """Convert a MongoDB assessment document to a serializable dict."""
    doc["_id"] = str(doc["_id"])
    return doc


# ─────────────────────────────────────────────────────────────────────────
#  POST /assessments – Submit a new assessment
# ─────────────────────────────────────────────────────────────────────────

@router.post(
    "/",
    response_model=AssessmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a new assessment",
    description="Submit all 36 assessment questions. Marks any previous "
                "assessment as non-latest and updates user onboarding status.",
)
async def create_assessment(
    payload: AssessmentCreate,
    current_user: dict = Depends(get_current_user),
):
    """Create a new assessment for the authenticated user."""
    uid = current_user["uid"]
    collection = Database.get_collection("assessments")
    users_collection = Database.get_collection("users")

    # Count existing assessments for versioning
    count = await collection.count_documents({"user_id": uid})

    # Mark all previous assessments as non-latest
    if count > 0:
        await collection.update_many(
            {"user_id": uid, "is_latest": True},
            {"$set": {"is_latest": False}},
        )

    # Create new assessment document
    doc = AssessmentDocument(
        user_id=uid,
        data=payload.data,
        is_latest=True,
        version=count + 1,
    )

    result = await collection.insert_one(doc.model_dump())
    assessment_id = str(result.inserted_id)

    # Update user profile
    await users_collection.update_one(
        {"firebase_uid": uid},
        {
            "$set": {
                "assessment_completed": True,
                "latest_assessment_id": assessment_id,
                "onboarding_status": "assessment_completed",
                "updated_at": datetime.utcnow(),
                # Sync body metrics to user profile
                "height_cm": payload.data.height_cm,
                "current_weight_kg": payload.data.current_weight_kg,
                "goal_weight_kg": payload.data.goal_weight_kg,
                "age": payload.data.actual_age,
                "gender": payload.data.gender,
            }
        },
    )

    created = await collection.find_one({"_id": result.inserted_id})
    logger.info("Assessment created for user %s (version %d)", uid, count + 1)
    return _serialize(created)


# ─────────────────────────────────────────────────────────────────────────
#  GET /assessments/latest – Get latest assessment
# ─────────────────────────────────────────────────────────────────────────

@router.get(
    "/latest",
    response_model=AssessmentResponse,
    summary="Get latest assessment",
)
async def get_latest_assessment(
    current_user: dict = Depends(get_current_user),
):
    """Retrieve the most recent assessment for the authenticated user."""
    collection = Database.get_collection("assessments")

    assessment = await collection.find_one(
        {"user_id": current_user["uid"], "is_latest": True},
        sort=[("created_at", -1)],
    )

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No assessment found. Please complete the assessment first.",
        )

    return _serialize(assessment)


# ─────────────────────────────────────────────────────────────────────────
#  GET /assessments/{assessment_id} – Get specific assessment
# ─────────────────────────────────────────────────────────────────────────

@router.get(
    "/{assessment_id}",
    response_model=AssessmentResponse,
    summary="Get assessment by ID",
)
async def get_assessment(
    assessment_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Retrieve a specific assessment by its ID."""
    collection = Database.get_collection("assessments")

    try:
        oid = ObjectId(assessment_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid assessment ID format.",
        )

    assessment = await collection.find_one(
        {"_id": oid, "user_id": current_user["uid"]}
    )

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found.",
        )

    return _serialize(assessment)


# ─────────────────────────────────────────────────────────────────────────
#  GET /assessments – List all assessments
# ─────────────────────────────────────────────────────────────────────────

@router.get(
    "/",
    response_model=List[AssessmentResponse],
    summary="List all assessments",
)
async def list_assessments(
    current_user: dict = Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
):
    """List all assessments for the authenticated user (newest first)."""
    collection = Database.get_collection("assessments")

    cursor = collection.find(
        {"user_id": current_user["uid"]},
    ).sort("created_at", -1).skip(skip).limit(limit)

    assessments = []
    async for doc in cursor:
        assessments.append(_serialize(doc))

    return assessments


# ─────────────────────────────────────────────────────────────────────────
#  DELETE /assessments/{assessment_id} – Delete an assessment
# ─────────────────────────────────────────────────────────────────────────

@router.delete(
    "/{assessment_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an assessment",
)
async def delete_assessment(
    assessment_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Delete a specific assessment."""
    collection = Database.get_collection("assessments")

    try:
        oid = ObjectId(assessment_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid assessment ID format.",
        )

    result = await collection.delete_one(
        {"_id": oid, "user_id": current_user["uid"]}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found.",
        )

    logger.info("Assessment %s deleted for user %s", assessment_id, current_user["uid"])
    return {"message": "Assessment deleted successfully."}
