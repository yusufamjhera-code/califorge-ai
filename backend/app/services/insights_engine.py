"""
Rule-based coaching insights engine for CaliForge AI.

Generates personalized coaching insights, tips, and
recommendations based on the user's fitness scores,
assessment data, and progress history.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

from app.models.assessment import AssessmentData
from app.models.fitness import FitnessLevel, FitnessScores
from app.models.progress import ProgressStats

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════
#  INSIGHT TYPES
# ═══════════════════════════════════════════════════════════════════════

class Insight:
    """A single coaching insight or tip."""

    def __init__(
        self,
        category: str,
        title: str,
        message: str,
        priority: int = 5,
        icon: str = "💡",
        action: Optional[str] = None,
    ):
        """
        Args:
            category: E.g. "strength", "recovery", "nutrition", "motivation"
            title: Short headline
            message: Detailed coaching message
            priority: 1 (highest) to 10 (lowest)
            icon: Emoji icon for display
            action: Optional actionable next step
        """
        self.category = category
        self.title = title
        self.message = message
        self.priority = priority
        self.icon = icon
        self.action = action

    def to_dict(self) -> dict:
        result = {
            "category": self.category,
            "title": self.title,
            "message": self.message,
            "priority": self.priority,
            "icon": self.icon,
        }
        if self.action:
            result["action"] = self.action
        return result


# ═══════════════════════════════════════════════════════════════════════
#  SCORE-BASED INSIGHTS
# ═══════════════════════════════════════════════════════════════════════

def _generate_fitness_insights(scores: FitnessScores) -> List[Insight]:
    """Generate insights based on fitness score dimensions."""
    insights: List[Insight] = []

    # Overall fitness level insight
    if scores.level == FitnessLevel.BEGINNER:
        insights.append(Insight(
            category="fitness",
            title="Starting Your Journey",
            message="You're at the beginning of your calisthenics journey. "
                    "Focus on building consistency and learning proper form. "
                    "Every expert was once a beginner!",
            priority=1,
            icon="🌱",
            action="Complete your first 3 workouts this week",
        ))
    elif scores.level == FitnessLevel.NOVICE:
        insights.append(Insight(
            category="fitness",
            title="Building Foundation",
            message="You've got a solid foundation forming. Keep building "
                    "on your consistency and start pushing for slightly harder "
                    "progressions when exercises feel easy.",
            priority=2,
            icon="🌿",
            action="Try the next progression for one exercise this week",
        ))
    elif scores.level == FitnessLevel.INTERMEDIATE:
        insights.append(Insight(
            category="fitness",
            title="Leveling Up",
            message="You're making serious progress! Focus on progressive "
                    "overload and consider targeting specific skill goals "
                    "like archer push-ups or pistol squat progressions.",
            priority=2,
            icon="🌳",
            action="Set a specific skill goal for the next 4 weeks",
        ))
    elif scores.level == FitnessLevel.ADVANCED:
        insights.append(Insight(
            category="fitness",
            title="Elite Performer",
            message="You're at an advanced level! Focus on skill refinement, "
                    "volume management, and recovery optimization. Consider "
                    "training for specific advanced skills.",
            priority=3,
            icon="🏆",
        ))

    # Strength-specific insights
    if scores.strength < 30:
        insights.append(Insight(
            category="strength",
            title="Build Your Base Strength",
            message="Your strength score suggests room for growth. Focus on "
                    "mastering the fundamental movements – push-ups, squats, "
                    "and planks – before advancing.",
            priority=2,
            icon="💪",
            action="Practice push-ups and squats daily, even just a few reps",
        ))
    elif scores.strength > 70:
        insights.append(Insight(
            category="strength",
            title="Impressive Strength!",
            message="Your strength metrics are strong. To continue progressing, "
                    "focus on harder progressions and slower, controlled movements.",
            priority=5,
            icon="🔥",
        ))

    # Recovery insights
    if scores.recovery < 40:
        insights.append(Insight(
            category="recovery",
            title="Recovery Needs Attention",
            message="Your recovery score is low, which can hinder progress and "
                    "increase injury risk. Prioritize sleep, hydration, and "
                    "stress management.",
            priority=1,
            icon="😴",
            action="Aim for 7+ hours of sleep and 2+ liters of water daily",
        ))
    elif scores.recovery > 75:
        insights.append(Insight(
            category="recovery",
            title="Excellent Recovery Habits",
            message="Your lifestyle supports great recovery. This gives you an "
                    "edge in training consistency and muscle building.",
            priority=7,
            icon="✨",
        ))

    # Consistency insights
    if scores.consistency < 30:
        insights.append(Insight(
            category="consistency",
            title="Consistency is Key",
            message="Building a regular workout habit is the #1 factor for "
                    "success. Start with just 2 days per week and build from there. "
                    "A short workout beats no workout!",
            priority=1,
            icon="📅",
            action="Schedule your workouts at fixed times",
        ))

    # Mobility insights
    if scores.mobility < 35:
        insights.append(Insight(
            category="mobility",
            title="Improve Your Mobility",
            message="Limited mobility can hold back your strength gains and "
                    "increase injury risk. Include stretching and mobility work "
                    "in every session.",
            priority=2,
            icon="🧘",
            action="Add 5 minutes of stretching after every workout",
        ))
    elif scores.mobility > 70:
        insights.append(Insight(
            category="mobility",
            title="Great Mobility",
            message="Your flexibility is above average. This helps with "
                    "exercise form and reduces injury risk. Keep it up!",
            priority=7,
            icon="🦎",
        ))

    return insights


# ═══════════════════════════════════════════════════════════════════════
#  ASSESSMENT-BASED INSIGHTS
# ═══════════════════════════════════════════════════════════════════════

def _generate_assessment_insights(data: AssessmentData) -> List[Insight]:
    """Generate insights based on specific assessment answers."""
    insights: List[Insight] = []

    # Goal-specific insights
    if getattr(data, "mainGoal", "") == "lose_weight":
        insights.append(Insight(
            category="nutrition",
            title="Weight Loss Strategy",
            message="Calisthenics builds muscle which boosts metabolism. "
                    "Combine your workouts with a moderate caloric deficit "
                    "(300-500 calories below maintenance) for sustainable fat loss.",
            priority=3,
            icon="⚡",
            action="Track your meals for one week to understand your intake",
        ))
    elif getattr(data, "mainGoal", "") == "gain_muscle":
        insights.append(Insight(
            category="nutrition",
            title="Muscle Building Focus",
            message="To build muscle with calisthenics, ensure you're eating "
                    "enough protein (1.6-2.2g per kg of bodyweight) and "
                    "progressively increasing exercise difficulty.",
            priority=3,
            icon="🥩",
            action="Aim for protein-rich foods at every meal",
        ))

    # Sedentary lifestyle insight
    if getattr(data, "dailyActivity", "") == "mostly_sitting":
        insights.append(Insight(
            category="lifestyle",
            title="Beat the Sedentary Trap",
            message="A sedentary lifestyle can undermine workout gains. "
                    "Try to move more throughout the day – take walks, "
                    "use a standing desk, or do mini movement breaks.",
            priority=2,
            icon="🚶",
            action="Set a timer to stand and move every 60 minutes",
        ))

    # Weight trend insights
    if getattr(data, "weightTrend", "") == "gain_fast_lose_slow" and getattr(data, "mainGoal", "") in (
        "lose_weight", "lose_fat_gain_muscle"
    ):
        insights.append(Insight(
            category="nutrition",
            title="Addressing Weight Gain",
            message="You mentioned your weight is trending up while your goal "
                    "involves fat loss. Small, sustainable changes to eating "
                    "habits are more effective than drastic diets.",
            priority=2,
            icon="📊",
        ))

    # Energy level insight
    if getattr(data, "energyLevel", "") == "low":
        insights.append(Insight(
            category="recovery",
            title="Boost Your Energy",
            message="Low energy can make workouts feel impossible. "
                    "Check your sleep quality, hydration, and iron levels. "
                    "Shorter, more intense workouts may work better for you.",
            priority=2,
            icon="🔋",
            action="Try working out at your peak energy time of day",
        ))

    # Physical limitations insights
    limitations = getattr(data, "physicalLimitations", [])
    real_limitations = [l for l in limitations if l != "none"]
    if real_limitations:
        lim_names = ", ".join(real_limitations[:3])
        insights.append(Insight(
            category="safety",
            title="Working Around Limitations",
            message=f"Your plan accounts for your {lim_names}. "
                    "Always listen to your body – sharp pain means stop. "
                    "Dull muscle ache during exercise is normal.",
            priority=1,
            icon="⚠️",
            action="Consult a healthcare provider if pain persists",
        ))

    # Flexibility-specific
    if getattr(data, "flexibility", "") == "not_good":
        insights.append(Insight(
            category="mobility",
            title="Flexibility First",
            message="Not being able to touch your toes is very common and "
                    "totally fixable! Daily stretching for just 5-10 minutes "
                    "can dramatically improve your flexibility within weeks.",
            priority=3,
            icon="🧘",
            action="Do 5 minutes of hamstring and hip stretches daily",
        ))

    # Build-specific insight
    if getattr(data, "physicalBuild", "") == "overweight":
        insights.append(Insight(
            category="safety",
            title="Smart Progression",
            message="Your plan starts with joint-friendly exercises. "
                    "As you get stronger and lighter, more advanced "
                    "movements will become accessible. Be patient with yourself!",
            priority=2,
            icon="🛡️",
        ))

    return insights


# ═══════════════════════════════════════════════════════════════════════
#  PROGRESS-BASED INSIGHTS
# ═══════════════════════════════════════════════════════════════════════

def _generate_progress_insights(stats: Optional[ProgressStats]) -> List[Insight]:
    """Generate insights based on progress statistics."""
    insights: List[Insight] = []

    if not stats:
        return insights

    # Streak-based motivation
    if stats.current_streak >= 7:
        insights.append(Insight(
            category="motivation",
            title=f"🔥 {stats.current_streak}-Day Streak!",
            message=f"You've worked out {stats.current_streak} days in a row! "
                    "That's incredible consistency. Remember to schedule rest "
                    "days too – recovery is when muscles grow.",
            priority=4,
            icon="🔥",
        ))
    elif stats.current_streak >= 3:
        insights.append(Insight(
            category="motivation",
            title=f"{stats.current_streak}-Day Streak!",
            message="You're building momentum! Keep showing up. "
                    "It takes about 21 days to build a habit.",
            priority=5,
            icon="⚡",
        ))
    elif stats.total_workouts > 0 and stats.current_streak == 0:
        insights.append(Insight(
            category="motivation",
            title="Time to Get Back!",
            message="You've taken a break – that's okay! The hardest part "
                    "is showing up. Even a 15-minute workout counts.",
            priority=1,
            icon="💪",
            action="Do a quick workout today – even 10 minutes helps",
        ))

    # Workout milestone celebrations
    if stats.total_workouts == 10:
        insights.append(Insight(
            category="motivation",
            title="10 Workouts Completed! 🎉",
            message="Double digits! You're proving you can stick with it. "
                    "You should be feeling noticeably stronger already.",
            priority=3,
            icon="🎉",
        ))

    # Weight change insight
    if stats.weight_change_kg is not None:
        if stats.weight_change_kg < -1:
            insights.append(Insight(
                category="progress",
                title="Weight Loss Progress",
                message=f"You've lost {abs(stats.weight_change_kg):.1f} kg! "
                        "Sustainable weight loss is 0.5-1 kg per week.",
                priority=4,
                icon="📉",
            ))
        elif stats.weight_change_kg > 1:
            insights.append(Insight(
                category="progress",
                title="Weight Gain Noted",
                message=f"Your weight has increased by {stats.weight_change_kg:.1f} kg. "
                        "This could be muscle gain if you're strength training "
                        "consistently. Track body measurements too!",
                priority=4,
                icon="📈",
            ))

    # Difficulty rating insight
    if stats.average_difficulty_rating is not None:
        if stats.average_difficulty_rating <= 2.0:
            insights.append(Insight(
                category="training",
                title="Workouts Too Easy?",
                message="Your difficulty ratings suggest workouts aren't "
                        "challenging enough. Time to progress to harder exercises "
                        "or increase volume.",
                priority=2,
                icon="🎯",
                action="Advance one exercise to its next progression",
            ))
        elif stats.average_difficulty_rating >= 4.5:
            insights.append(Insight(
                category="training",
                title="Consider Scaling Back",
                message="Your workouts feel very hard. This increases injury "
                        "risk. Consider adding more rest days or reducing volume.",
                priority=2,
                icon="⚠️",
            ))

    return insights


# ═══════════════════════════════════════════════════════════════════════
#  MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════

def generate_insights(
    scores: FitnessScores,
    data: AssessmentData,
    stats: Optional[ProgressStats] = None,
    max_insights: int = 8,
) -> List[dict]:
    """Generate personalized coaching insights.

    Combines score-based, assessment-based, and progress-based
    insights, sorted by priority.

    Args:
        scores: User's current fitness scores.
        data: User's assessment data.
        stats: Optional progress statistics.
        max_insights: Maximum number of insights to return.

    Returns:
        List of insight dicts sorted by priority (most important first).
    """
    all_insights: List[Insight] = []

    all_insights.extend(_generate_fitness_insights(scores))
    all_insights.extend(_generate_assessment_insights(data))
    all_insights.extend(_generate_progress_insights(stats))

    # Sort by priority (lower number = higher priority)
    all_insights.sort(key=lambda x: x.priority)

    # Deduplicate by category (keep highest priority per category)
    seen_categories: set = set()
    unique_insights: List[Insight] = []
    for insight in all_insights:
        key = f"{insight.category}:{insight.title}"
        if key not in seen_categories:
            seen_categories.add(key)
            unique_insights.append(insight)

    result = [i.to_dict() for i in unique_insights[:max_insights]]

    logger.info("Generated %d coaching insights for user", len(result))
    return result
