import asyncio
import os
import sys
import json

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import Database
from app.services.workout_generator import generate_workout_plan
from app.models.assessment import AssessmentData
from app.models.fitness import FitnessScores, FitnessLevel

async def test():
    await Database.connect()
    
    # Mock data
    assessment = AssessmentData(
        age="25-34",
        gender="male",
        height="180",
        weight="80",
        fitnessLevel="intermediate",
        primaryGoal="gain_muscle",
        targetZone=["Back", "Chest"],
        weeklyTraining="3-4",
        workoutDuration="20-25",
        physicalLimitations=["none"],
        equipmentAccess=["pull_up_bar"]
    )
    
    scores = FitnessScores(
        overall_fitness=65,
        strength=60,
        endurance=60,
        mobility=70,
        core=60,
        consistency=60,
        level=FitnessLevel.INTERMEDIATE,
        recovery=80
    )
    
    plan = await generate_workout_plan(
        user_id="test_user",
        assessment_id="test_assessment",
        fitness_score_id="test_score",
        data=assessment,
        scores=scores,
        duration_weeks=2
    )
    
    print(json.dumps(plan.model_dump(), default=str, indent=2))
    
    await Database.disconnect()

if __name__ == "__main__":
    asyncio.run(test())
