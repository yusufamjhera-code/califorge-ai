import asyncio
import os
import sys

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import Database
from app.models.exercise import ExerciseModel
from app.data.exercises import EXERCISES

async def seed_database():
    print("Connecting to database...")
    await Database.connect()
    
    collection = Database.get_collection("exercises")
    
    # Clear existing exercises to prevent duplicates on rerun
    print("Clearing existing exercises...")
    await collection.delete_many({})
    
    print(f"Seeding {len(EXERCISES)} exercises into MongoDB...")
    
    docs = []
    for ex_id, exercise in EXERCISES.items():
        # exercise is an app.data.exercises.Exercise model, we convert it to ExerciseModel 
        # (or just dict) to insert into mongo.
        
        # We need to map `muscles_primary` to `primary_muscles` if ExerciseModel expects it
        data = exercise.model_dump()
        
        # Adapt fields to match ExerciseModel if needed
        data["primary_muscles"] = data.get("muscles_primary", [])
        # We put all instructions in instructions, coaching cues in coaching_cues
        data["instructions"] = data.get("coaching_cues", [])
        data["coaching_cues"] = data.get("coaching_cues", [])
        data["equipment_required"] = ["None"] # Default fallback
        
        ex_model = ExerciseModel(**data)
        doc = ex_model.model_dump(by_alias=True)
        # Override the random ObjectId with the stable string ID for easy reference if needed
        doc["_id"] = ex_id
        
        docs.append(doc)
        
    result = await collection.insert_many(docs)
    
    print(f"Successfully inserted {len(result.inserted_ids)} exercises!")
    
    await Database.close_db()

if __name__ == "__main__":
    asyncio.run(seed_database())
