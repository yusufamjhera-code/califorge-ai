from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class ExerciseModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str
    category: str  # Push, Pull, Core, Legs, Mobility, Conditioning
    difficulty: str  # Beginner, Novice, Intermediate, Advanced
    primary_muscles: List[str]
    equipment_required: List[str]  # e.g., ["None"], ["Pull-up Bar"], ["Rings"]
    instructions: List[str]
    coaching_cues: List[str]
    contraindications: List[str] = Field(default_factory=list)
    is_timed: bool = False
    default_reps: Optional[int] = None
    default_duration_seconds: Optional[int] = None
    video_url: Optional[str] = None
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "Push-up",
                "category": "Push",
                "difficulty": "Beginner",
                "primary_muscles": ["Chest", "Triceps", "Shoulders"],
                "equipment_required": ["None"],
                "instructions": ["Start in a plank position", "Lower your body", "Push back up"],
                "coaching_cues": ["Keep core tight", "Don't flare elbows"],
                "is_timed": False,
                "default_reps": 10
            }
        }
