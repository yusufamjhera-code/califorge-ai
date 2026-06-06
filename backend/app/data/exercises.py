"""
Complete bodyweight exercise database for CaliForge AI.

Contains 100+ exercises across 6 categories (Push, Pull, Legs, Core,
Conditioning, Mobility) with difficulty levels, muscle targets,
recommended sets/reps, and coaching cues.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Exercise(BaseModel):
    """Definition of a single exercise in the database."""

    id: str
    name: str
    category: str  # Push, Pull, Legs, Core, Conditioning, Mobility
    difficulty: str  # Beginner, Novice, Intermediate, Advanced
    muscles_primary: List[str]
    muscles_secondary: List[str] = Field(default_factory=list)
    is_timed: bool = False  # True for holds/planks, False for reps
    default_reps: Optional[int] = None
    default_duration_seconds: Optional[int] = None
    default_sets: int = 3
    default_rest_seconds: int = 60
    coaching_cues: List[str] = Field(default_factory=list)
    contraindications: List[str] = Field(
        default_factory=list,
        description="Physical limitations that contraindicate this exercise",
    )
    progression_from: Optional[str] = Field(
        None, description="ID of the easier exercise this progresses from"
    )
    progression_to: Optional[str] = Field(
        None, description="ID of the harder exercise this progresses to"
    )


# ═══════════════════════════════════════════════════════════════════════
#  EXERCISE DATABASE – 100+ Bodyweight Exercises
# ═══════════════════════════════════════════════════════════════════════

EXERCISES: Dict[str, Exercise] = {}


def _register(ex: Exercise) -> Exercise:
    EXERCISES[ex.id] = ex
    return ex


# ── PUSH (20 exercises) ──────────────────────────────────────────────────

_register(Exercise(
    id="push_wall_pushup", name="Wall Push-up", category="Push", difficulty="Beginner",
    muscles_primary=["Chest", "Triceps"], muscles_secondary=["Shoulders", "Core"],
    default_reps=15, coaching_cues=["Stand arm's length from wall", "Keep body straight"],
    contraindications=["Wrist Pain"], progression_to="push_incline_pushup"
))
_register(Exercise(
    id="push_incline_pushup", name="Incline Push-up", category="Push", difficulty="Beginner",
    muscles_primary=["Chest", "Triceps"], muscles_secondary=["Shoulders", "Core"],
    default_reps=12, coaching_cues=["Hands on elevated surface", "Lower chest to edge"],
    contraindications=["Wrist Pain"], progression_from="push_wall_pushup", progression_to="push_knee_pushup"
))
_register(Exercise(
    id="push_knee_pushup", name="Knee Push-up", category="Push", difficulty="Beginner",
    muscles_primary=["Chest", "Triceps"], muscles_secondary=["Shoulders", "Core"],
    default_reps=12, coaching_cues=["Knees on ground", "Lower chest to floor"],
    contraindications=["Wrist Pain", "Knee Issues"], progression_from="push_incline_pushup", progression_to="push_pushup"
))
_register(Exercise(
    id="push_pushup", name="Push-up", category="Push", difficulty="Novice",
    muscles_primary=["Chest", "Triceps"], muscles_secondary=["Shoulders", "Core", "Serratus Anterior"],
    default_reps=10, coaching_cues=["Hands shoulder-width", "Body forms straight line"],
    contraindications=["Wrist Pain", "Shoulder Problems"], progression_from="push_knee_pushup", progression_to="push_diamond_pushup"
))
_register(Exercise(
    id="push_wide_pushup", name="Wide Push-up", category="Push", difficulty="Novice",
    muscles_primary=["Chest"], muscles_secondary=["Shoulders", "Triceps"],
    default_reps=10, coaching_cues=["Hands wider than shoulders", "Flared elbows slightly"],
    contraindications=["Shoulder Problems"], progression_from="push_pushup"
))
_register(Exercise(
    id="push_decline_pushup", name="Decline Push-up", category="Push", difficulty="Novice",
    muscles_primary=["Upper Chest", "Shoulders"], muscles_secondary=["Triceps", "Core"],
    default_reps=10, coaching_cues=["Feet elevated", "Maintain core tension"],
    contraindications=["Shoulder Problems"], progression_from="push_pushup", progression_to="push_pike_pushup"
))
_register(Exercise(
    id="push_diamond_pushup", name="Diamond Push-up", category="Push", difficulty="Intermediate",
    muscles_primary=["Triceps", "Chest"], muscles_secondary=["Shoulders", "Core"],
    default_reps=8, coaching_cues=["Hands form diamond under chest", "Keep elbows close"],
    contraindications=["Wrist Pain"], progression_from="push_pushup", progression_to="push_archer_pushup"
))
_register(Exercise(
    id="push_staggered_pushup", name="Staggered Push-up", category="Push", difficulty="Intermediate",
    muscles_primary=["Chest", "Triceps"], muscles_secondary=["Shoulders", "Core"],
    default_reps=8, coaching_cues=["One hand high, one hand low", "Switch positions"],
    contraindications=["Shoulder Problems"], progression_from="push_pushup"
))
_register(Exercise(
    id="push_spiderman_pushup", name="Spiderman Push-up", category="Push", difficulty="Intermediate",
    muscles_primary=["Chest", "Triceps"], muscles_secondary=["Shoulders", "Core", "Obliques"],
    default_reps=8, coaching_cues=["Bring knee to elbow as you lower", "Alternate sides"],
    contraindications=["Hip Issues"], progression_from="push_pushup"
))
_register(Exercise(
    id="push_pike_pushup", name="Pike Push-up", category="Push", difficulty="Intermediate",
    muscles_primary=["Shoulders", "Triceps"], muscles_secondary=["Upper Chest", "Core"],
    default_reps=8, coaching_cues=["Hips high in V-shape", "Lower top of head to floor"],
    contraindications=["Shoulder Problems", "Neck Pain"], progression_from="push_decline_pushup", progression_to="push_elevated_pike"
))
_register(Exercise(
    id="push_elevated_pike", name="Elevated Pike Push-up", category="Push", difficulty="Advanced",
    muscles_primary=["Shoulders", "Triceps"], muscles_secondary=["Upper Chest", "Core"],
    default_reps=6, coaching_cues=["Feet on box/chair", "Hips stacked over shoulders"],
    contraindications=["Shoulder Problems", "Neck Pain"], progression_from="push_pike_pushup", progression_to="push_hspu_wall"
))
_register(Exercise(
    id="push_hspu_wall", name="Wall Handstand Push-up", category="Push", difficulty="Advanced",
    muscles_primary=["Shoulders", "Triceps"], muscles_secondary=["Core", "Upper Chest"],
    default_reps=4, coaching_cues=["Kick up to wall", "Lower until head taps floor"],
    contraindications=["Shoulder Problems", "Neck Pain"], progression_from="push_elevated_pike"
))
_register(Exercise(
    id="push_archer_pushup", name="Archer Push-up", category="Push", difficulty="Advanced",
    muscles_primary=["Chest", "Triceps"], muscles_secondary=["Shoulders", "Core"],
    default_reps=6, coaching_cues=["Shift weight to one arm", "Keep assisting arm straight"],
    contraindications=["Shoulder Problems"], progression_from="push_diamond_pushup", progression_to="push_one_arm_pushup"
))
_register(Exercise(
    id="push_one_arm_pushup", name="One Arm Push-up", category="Push", difficulty="Advanced",
    muscles_primary=["Chest", "Triceps"], muscles_secondary=["Shoulders", "Core", "Obliques"],
    default_reps=3, coaching_cues=["Wide stance", "Keep hips as square as possible"],
    contraindications=["Shoulder Problems", "Wrist Pain"], progression_from="push_archer_pushup"
))
_register(Exercise(
    id="push_pseudo_planche_pushup", name="Pseudo Planche Push-up", category="Push", difficulty="Advanced",
    muscles_primary=["Chest", "Shoulders", "Triceps"], muscles_secondary=["Core", "Biceps"],
    default_reps=6, coaching_cues=["Lean far forward", "Hands by waist"],
    contraindications=["Wrist Pain", "Shoulder Problems"], progression_from="push_pushup", progression_to="push_tuck_planche"
))
_register(Exercise(
    id="push_tuck_planche", name="Tuck Planche Hold", category="Push", difficulty="Advanced",
    muscles_primary=["Shoulders", "Chest"], muscles_secondary=["Core", "Biceps", "Triceps"],
    is_timed=True, default_duration_seconds=15, coaching_cues=["Knees tucked to chest", "Press ground away"],
    contraindications=["Wrist Pain"], progression_from="push_pseudo_planche_pushup"
))
_register(Exercise(
    id="push_hindu_pushup", name="Hindu Push-up", category="Push", difficulty="Intermediate",
    muscles_primary=["Chest", "Shoulders"], muscles_secondary=["Triceps", "Core", "Spine"],
    default_reps=8, coaching_cues=["Swoop under fence", "Push up to cobra", "Return to downward dog"],
    contraindications=["Shoulder Problems", "Back Pain"], progression_from="push_pushup"
))
_register(Exercise(
    id="push_explosive_pushup", name="Explosive Push-up", category="Push", difficulty="Intermediate",
    muscles_primary=["Chest", "Triceps"], muscles_secondary=["Shoulders", "Core"],
    default_reps=6, coaching_cues=["Explode up so hands leave floor", "Land softly"],
    contraindications=["Wrist Pain"], progression_from="push_pushup", progression_to="push_clap_pushup"
))
_register(Exercise(
    id="push_clap_pushup", name="Clap Push-up", category="Push", difficulty="Advanced",
    muscles_primary=["Chest", "Triceps"], muscles_secondary=["Shoulders", "Core"],
    default_reps=6, coaching_cues=["Explode up and clap", "Land softly into next rep"],
    contraindications=["Wrist Pain"], progression_from="push_explosive_pushup"
))
_register(Exercise(
    id="push_tricep_extension", name="Bodyweight Tricep Extension", category="Push", difficulty="Intermediate",
    muscles_primary=["Triceps"], muscles_secondary=["Core", "Shoulders"],
    default_reps=8, coaching_cues=["Hands on low bar or floor", "Bend at elbows, lower head to hands", "Press back up"],
    contraindications=["Elbow Issues"], progression_from="push_diamond_pushup"
))


# ── PULL (20 exercises) ──────────────────────────────────────────────────

_register(Exercise(
    id="pull_wall_pull", name="Wall Pull", category="Pull", difficulty="Beginner",
    muscles_primary=["Back", "Biceps"], muscles_secondary=["Rear Delts", "Core"],
    default_reps=15, coaching_cues=["Hold doorframe or pole", "Lean back", "Pull chest to hands"],
    contraindications=[], progression_to="pull_australian_pullup"
))
_register(Exercise(
    id="pull_australian_pullup", name="Australian Pull-up (Body Row)", category="Pull", difficulty="Beginner",
    muscles_primary=["Back", "Biceps"], muscles_secondary=["Rear Delts", "Core"],
    default_reps=10, coaching_cues=["Under a low bar", "Keep body straight", "Pull chest to bar"],
    contraindications=["Shoulder Problems"], progression_from="pull_wall_pull", progression_to="pull_negative_pullup"
))
_register(Exercise(
    id="pull_negative_pullup", name="Negative Pull-up", category="Pull", difficulty="Novice",
    muscles_primary=["Lats", "Biceps"], muscles_secondary=["Core", "Grip"],
    default_reps=5, coaching_cues=["Jump to top position", "Lower slowly over 3-5 seconds"],
    contraindications=["Shoulder Problems", "Elbow Issues"], progression_from="pull_australian_pullup", progression_to="pull_pullup"
))
_register(Exercise(
    id="pull_pullup", name="Pull-up", category="Pull", difficulty="Intermediate",
    muscles_primary=["Lats", "Back"], muscles_secondary=["Biceps", "Core", "Grip"],
    default_reps=6, coaching_cues=["Overhand grip", "Pull chin over bar", "Full extension at bottom"],
    contraindications=["Shoulder Problems", "Elbow Issues"], progression_from="pull_negative_pullup", progression_to="pull_wide_pullup"
))
_register(Exercise(
    id="pull_chinup", name="Chin-up", category="Pull", difficulty="Intermediate",
    muscles_primary=["Lats", "Biceps"], muscles_secondary=["Core", "Grip"],
    default_reps=6, coaching_cues=["Underhand grip", "Pull chin over bar", "Focus on bicep squeeze"],
    contraindications=["Shoulder Problems", "Elbow Issues"], progression_from="pull_negative_pullup", progression_to="pull_l_sit_pullup"
))
_register(Exercise(
    id="pull_wide_pullup", name="Wide Grip Pull-up", category="Pull", difficulty="Intermediate",
    muscles_primary=["Lats"], muscles_secondary=["Rear Delts", "Core", "Grip"],
    default_reps=5, coaching_cues=["Grip wider than shoulders", "Pull chest to bar"],
    contraindications=["Shoulder Problems"], progression_from="pull_pullup", progression_to="pull_archer_pullup"
))
_register(Exercise(
    id="pull_commando_pullup", name="Commando Pull-up", category="Pull", difficulty="Intermediate",
    muscles_primary=["Back", "Biceps"], muscles_secondary=["Core", "Grip"],
    default_reps=6, coaching_cues=["Mixed grip, hands close", "Pull head to one side of bar", "Alternate sides"],
    contraindications=["Shoulder Problems"], progression_from="pull_pullup"
))
_register(Exercise(
    id="pull_archer_pullup", name="Archer Pull-up", category="Pull", difficulty="Advanced",
    muscles_primary=["Lats", "Biceps"], muscles_secondary=["Core", "Grip"],
    default_reps=4, coaching_cues=["Pull toward one hand", "Keep other arm straight"],
    contraindications=["Shoulder Problems", "Elbow Issues"], progression_from="pull_wide_pullup", progression_to="pull_one_arm_pullup"
))
_register(Exercise(
    id="pull_typewriter_pullup", name="Typewriter Pull-up", category="Pull", difficulty="Advanced",
    muscles_primary=["Lats", "Back", "Biceps"], muscles_secondary=["Core", "Grip"],
    default_reps=4, coaching_cues=["Pull up, shift chin to left hand, then right hand", "Lower down"],
    contraindications=["Shoulder Problems", "Elbow Issues"], progression_from="pull_archer_pullup"
))
_register(Exercise(
    id="pull_l_sit_pullup", name="L-Sit Pull-up", category="Pull", difficulty="Advanced",
    muscles_primary=["Lats", "Biceps"], muscles_secondary=["Core", "Hip Flexors", "Grip"],
    default_reps=5, coaching_cues=["Hold legs parallel to floor", "Perform pull-up without losing leg height"],
    contraindications=["Shoulder Problems", "Hip Issues"], progression_from="pull_chinup"
))
_register(Exercise(
    id="pull_one_arm_pullup", name="One Arm Pull-up", category="Pull", difficulty="Advanced",
    muscles_primary=["Lats", "Biceps"], muscles_secondary=["Core", "Grip"],
    default_reps=2, coaching_cues=["Grip bar with one hand", "Pull chin over bar"],
    contraindications=["Shoulder Problems", "Elbow Issues", "Wrist Pain"], progression_from="pull_archer_pullup"
))
_register(Exercise(
    id="pull_muscle_up_transition", name="Muscle-up Transition", category="Pull", difficulty="Advanced",
    muscles_primary=["Back", "Chest"], muscles_secondary=["Triceps", "Biceps", "Core"],
    default_reps=3, coaching_cues=["Explosive high pull-up", "Quick wrist turnover"],
    contraindications=["Shoulder Problems", "Elbow Issues", "Wrist Pain"], progression_from="pull_high_pullup", progression_to="pull_muscle_up"
))
_register(Exercise(
    id="pull_muscle_up", name="Muscle-up", category="Pull", difficulty="Advanced",
    muscles_primary=["Lats", "Chest", "Triceps"], muscles_secondary=["Biceps", "Core", "Shoulders"],
    default_reps=3, coaching_cues=["Explosive pull", "Transition over bar", "Dip to finish"],
    contraindications=["Shoulder Problems", "Elbow Issues", "Wrist Pain"], progression_from="pull_muscle_up_transition"
))
_register(Exercise(
    id="pull_high_pullup", name="High Pull-up", category="Pull", difficulty="Advanced",
    muscles_primary=["Lats", "Back"], muscles_secondary=["Biceps", "Core"],
    default_reps=5, coaching_cues=["Explosive pull", "Pull bar to stomach/waist level"],
    contraindications=["Shoulder Problems"], progression_from="pull_pullup", progression_to="pull_muscle_up_transition"
))
_register(Exercise(
    id="pull_towel_pullup", name="Towel Pull-up", category="Pull", difficulty="Intermediate",
    muscles_primary=["Forearms", "Grip"], muscles_secondary=["Lats", "Biceps"],
    default_reps=5, coaching_cues=["Hang two towels over bar", "Grip towels and pull up"],
    contraindications=["Wrist Pain", "Elbow Issues"], progression_from="pull_pullup"
))
_register(Exercise(
    id="pull_inverted_row_feet_elevated", name="Elevated Inverted Row", category="Pull", difficulty="Novice",
    muscles_primary=["Back", "Biceps"], muscles_secondary=["Rear Delts", "Core"],
    default_reps=10, coaching_cues=["Feet on chair/box", "Pull chest to bar"],
    contraindications=["Shoulder Problems"], progression_from="pull_australian_pullup"
))
_register(Exercise(
    id="pull_front_lever_tuck", name="Tuck Front Lever", category="Pull", difficulty="Intermediate",
    muscles_primary=["Lats", "Core"], muscles_secondary=["Shoulders", "Back"],
    is_timed=True, default_duration_seconds=15, coaching_cues=["Hang from bar", "Tuck knees to chest", "Lean back until back is horizontal"],
    contraindications=["Shoulder Problems", "Back Pain"], progression_from="pull_pullup", progression_to="pull_front_lever_adv_tuck"
))
_register(Exercise(
    id="pull_front_lever_adv_tuck", name="Adv. Tuck Front Lever", category="Pull", difficulty="Advanced",
    muscles_primary=["Lats", "Core"], muscles_secondary=["Shoulders", "Back"],
    is_timed=True, default_duration_seconds=10, coaching_cues=["Back flat", "Knees slightly past 90 degrees"],
    contraindications=["Shoulder Problems", "Back Pain"], progression_from="pull_front_lever_tuck"
))
_register(Exercise(
    id="pull_scapular_pulls", name="Scapular Pulls", category="Pull", difficulty="Beginner",
    muscles_primary=["Traps", "Rhomboids"], muscles_secondary=["Lats", "Grip"],
    default_reps=10, coaching_cues=["Dead hang", "Pull shoulder blades down and together", "Keep arms straight"],
    contraindications=[], progression_to="pull_australian_pullup"
))
_register(Exercise(
    id="pull_bicep_chinup", name="Concentration Chin-up", category="Pull", difficulty="Intermediate",
    muscles_primary=["Biceps"], muscles_secondary=["Lats", "Core"],
    default_reps=6, coaching_cues=["Hands close together", "Focus heavily on squeezing biceps at top"],
    contraindications=["Elbow Issues"], progression_from="pull_chinup"
))


# ── LEGS (20 exercises) ──────────────────────────────────────────────────

_register(Exercise(
    id="legs_squat", name="Squat", category="Legs", difficulty="Beginner",
    muscles_primary=["Quadriceps", "Glutes"], muscles_secondary=["Hamstrings", "Core", "Calves"],
    default_reps=15, coaching_cues=["Feet shoulder-width", "Sit back into invisible chair", "Chest up"],
    contraindications=[], progression_to="legs_jump_squat"
))
_register(Exercise(
    id="legs_assisted_squat", name="Assisted Squat", category="Legs", difficulty="Beginner",
    muscles_primary=["Quadriceps", "Glutes"], muscles_secondary=["Hamstrings", "Core"],
    default_reps=15, coaching_cues=["Hold onto pole or doorway", "Sit back into squat"],
    contraindications=[], progression_to="legs_squat"
))
_register(Exercise(
    id="legs_box_squat", name="Box Squat", category="Legs", difficulty="Beginner",
    muscles_primary=["Quadriceps", "Glutes"], muscles_secondary=["Hamstrings", "Core"],
    default_reps=15, coaching_cues=["Squat until glutes touch a chair/box", "Stand back up"],
    contraindications=[], progression_to="legs_squat"
))
_register(Exercise(
    id="legs_jump_squat", name="Jump Squat", category="Legs", difficulty="Novice",
    muscles_primary=["Quadriceps", "Glutes"], muscles_secondary=["Calves", "Hamstrings", "Core"],
    default_reps=10, coaching_cues=["Explode upward", "Land softly with bent knees"],
    contraindications=["Knee Issues", "Ankle Issues"], progression_from="legs_squat", progression_to="legs_lunge_jumps"
))
_register(Exercise(
    id="legs_reverse_lunge", name="Reverse Lunge", category="Legs", difficulty="Beginner",
    muscles_primary=["Quadriceps", "Glutes"], muscles_secondary=["Hamstrings", "Core"],
    default_reps=12, coaching_cues=["Step backward", "Both knees 90 degrees", "Push through front heel"],
    contraindications=["Knee Issues"], progression_to="legs_split_squat"
))
_register(Exercise(
    id="legs_forward_lunge", name="Forward Lunge", category="Legs", difficulty="Beginner",
    muscles_primary=["Quadriceps", "Glutes"], muscles_secondary=["Hamstrings", "Core"],
    default_reps=12, coaching_cues=["Step forward", "Both knees 90 degrees", "Push back to start"],
    contraindications=["Knee Issues"], progression_to="legs_split_squat"
))
_register(Exercise(
    id="legs_split_squat", name="Split Squat", category="Legs", difficulty="Novice",
    muscles_primary=["Quadriceps", "Glutes"], muscles_secondary=["Hamstrings", "Core"],
    default_reps=10, coaching_cues=["Staggered stance", "Lower straight down", "Drive up"],
    contraindications=["Knee Issues"], progression_from="legs_reverse_lunge", progression_to="legs_bulgarian_split_squat"
))
_register(Exercise(
    id="legs_bulgarian_split_squat", name="Bulgarian Split Squat", category="Legs", difficulty="Intermediate",
    muscles_primary=["Quadriceps", "Glutes"], muscles_secondary=["Hamstrings", "Core"],
    default_reps=8, coaching_cues=["Back foot elevated on bench/chair", "Lower until front thigh is parallel"],
    contraindications=["Knee Issues", "Ankle Issues"], progression_from="legs_split_squat", progression_to="legs_shrimp_squat"
))
_register(Exercise(
    id="legs_lunge_jumps", name="Jumping Lunges", category="Legs", difficulty="Intermediate",
    muscles_primary=["Quadriceps", "Glutes"], muscles_secondary=["Calves", "Hamstrings"],
    default_reps=10, coaching_cues=["Start in lunge", "Explode up and switch legs in air", "Land softly in lunge"],
    contraindications=["Knee Issues", "Ankle Issues"], progression_from="legs_jump_squat"
))
_register(Exercise(
    id="legs_shrimp_squat", name="Shrimp Squat", category="Legs", difficulty="Intermediate",
    muscles_primary=["Quadriceps", "Glutes"], muscles_secondary=["Hamstrings", "Core", "Calves"],
    default_reps=6, coaching_cues=["Hold one foot behind you", "Lower knee to floor", "Push up"],
    contraindications=["Knee Issues", "Ankle Issues"], progression_from="legs_bulgarian_split_squat", progression_to="legs_pistol_squat"
))
_register(Exercise(
    id="legs_assisted_pistol", name="Assisted Pistol Squat", category="Legs", difficulty="Intermediate",
    muscles_primary=["Quadriceps", "Glutes"], muscles_secondary=["Hamstrings", "Core"],
    default_reps=5, coaching_cues=["Hold doorway/pole", "One leg forward", "Squat deep and pull/push up"],
    contraindications=["Knee Issues", "Ankle Issues"], progression_from="legs_shrimp_squat", progression_to="legs_pistol_squat"
))
_register(Exercise(
    id="legs_pistol_squat", name="Pistol Squat", category="Legs", difficulty="Advanced",
    muscles_primary=["Quadriceps", "Glutes"], muscles_secondary=["Hamstrings", "Core", "Calves"],
    default_reps=4, coaching_cues=["One leg forward", "Deep squat", "Heel stays planted"],
    contraindications=["Knee Issues", "Ankle Issues", "Hip Issues"], progression_from="legs_assisted_pistol", progression_to="legs_dragon_pistol"
))
_register(Exercise(
    id="legs_dragon_pistol", name="Dragon Pistol Squat", category="Legs", difficulty="Advanced",
    muscles_primary=["Quadriceps", "Glutes", "Hip Flexors"], muscles_secondary=["Hamstrings", "Core"],
    default_reps=3, coaching_cues=["Wrap non-working leg behind the squatting leg", "Squat deep"],
    contraindications=["Knee Issues", "Ankle Issues", "Hip Issues"], progression_from="legs_pistol_squat"
))
_register(Exercise(
    id="legs_sissy_squat", name="Sissy Squat", category="Legs", difficulty="Advanced",
    muscles_primary=["Quadriceps"], muscles_secondary=["Core"],
    default_reps=6, coaching_cues=["Lean back", "Knees track far forward", "Keep straight line from knees to shoulders"],
    contraindications=["Knee Issues"], progression_from="legs_bulgarian_split_squat"
))
_register(Exercise(
    id="legs_glute_bridge", name="Glute Bridge", category="Legs", difficulty="Beginner",
    muscles_primary=["Glutes", "Hamstrings"], muscles_secondary=["Lower Back", "Core"],
    default_reps=15, coaching_cues=["Lie on back, knees bent", "Squeeze glutes and lift hips", "Don't overarch lower back"],
    contraindications=["Back Pain"], progression_to="legs_single_leg_glute_bridge"
))
_register(Exercise(
    id="legs_single_leg_glute_bridge", name="Single Leg Glute Bridge", category="Legs", difficulty="Novice",
    muscles_primary=["Glutes", "Hamstrings"], muscles_secondary=["Lower Back", "Core"],
    default_reps=10, coaching_cues=["One leg extended straight", "Push through planted heel to lift hips"],
    contraindications=["Back Pain"], progression_from="legs_glute_bridge", progression_to="legs_sliding_leg_curl"
))
_register(Exercise(
    id="legs_sliding_leg_curl", name="Sliding Leg Curl", category="Legs", difficulty="Intermediate",
    muscles_primary=["Hamstrings"], muscles_secondary=["Glutes", "Core"],
    default_reps=8, coaching_cues=["Feet on sliders/socks on smooth floor", "Bridge hips up", "Slide feet out and pull back in"],
    contraindications=["Knee Issues", "Hamstring Issues"], progression_from="legs_single_leg_glute_bridge", progression_to="legs_nordic_curl"
))
_register(Exercise(
    id="legs_nordic_curl", name="Nordic Hamstring Curl", category="Legs", difficulty="Advanced",
    muscles_primary=["Hamstrings"], muscles_secondary=["Glutes", "Calves"],
    default_reps=4, coaching_cues=["Secure feet", "Lower body slowly", "Use hands to catch and push back up"],
    contraindications=["Knee Issues", "Hamstring Issues"], progression_from="legs_sliding_leg_curl"
))
_register(Exercise(
    id="legs_calf_raises", name="Calf Raises", category="Legs", difficulty="Beginner",
    muscles_primary=["Calves"], muscles_secondary=["Ankles"],
    default_reps=20, coaching_cues=["Stand on edge of step", "Drop heels", "Push high onto toes"],
    contraindications=["Ankle Issues"], progression_to="legs_single_leg_calf_raises"
))
_register(Exercise(
    id="legs_single_leg_calf_raises", name="Single Leg Calf Raises", category="Legs", difficulty="Novice",
    muscles_primary=["Calves"], muscles_secondary=["Ankles"],
    default_reps=12, coaching_cues=["One foot on step", "Full stretch at bottom", "Full contraction at top"],
    contraindications=["Ankle Issues"], progression_from="legs_calf_raises"
))


# ── CORE (20 exercises) ──────────────────────────────────────────────────

_register(Exercise(
    id="core_plank", name="Plank", category="Core", difficulty="Beginner",
    muscles_primary=["Core", "Rectus Abdominis"], muscles_secondary=["Shoulders", "Glutes", "Lower Back"],
    is_timed=True, default_duration_seconds=30, coaching_cues=["Forearms and toes", "Straight line from head to heels"],
    contraindications=["Shoulder Problems"], progression_to="core_hollow_hold"
))
_register(Exercise(
    id="core_side_plank", name="Side Plank", category="Core", difficulty="Beginner",
    muscles_primary=["Obliques", "Core"], muscles_secondary=["Shoulders", "Glutes"],
    is_timed=True, default_duration_seconds=20, coaching_cues=["Support on one forearm", "Hips high"],
    contraindications=["Shoulder Problems"], progression_to="core_side_plank_dips"
))
_register(Exercise(
    id="core_dead_bug", name="Dead Bug", category="Core", difficulty="Beginner",
    muscles_primary=["Core", "Transverse Abdominis"], muscles_secondary=["Hip Flexors"],
    default_reps=12, coaching_cues=["Lower back pressed to floor", "Extend opposite arm/leg"],
    contraindications=["Back Pain"]
))
_register(Exercise(
    id="core_bird_dog", name="Bird Dog", category="Core", difficulty="Beginner",
    muscles_primary=["Core", "Lower Back"], muscles_secondary=["Glutes", "Shoulders"],
    default_reps=12, coaching_cues=["Tabletop position", "Extend opposite arm/leg", "Keep hips square"],
    contraindications=[]
))
_register(Exercise(
    id="core_crunches", name="Crunches", category="Core", difficulty="Beginner",
    muscles_primary=["Rectus Abdominis"], muscles_secondary=["Core"],
    default_reps=15, coaching_cues=["Hands gently behind ears", "Lift shoulder blades off floor", "Squeeze abs"],
    contraindications=["Neck Pain", "Back Pain"]
))
_register(Exercise(
    id="core_hollow_hold", name="Hollow Hold", category="Core", difficulty="Novice",
    muscles_primary=["Core", "Rectus Abdominis"], muscles_secondary=["Hip Flexors", "Obliques"],
    is_timed=True, default_duration_seconds=20, coaching_cues=["Lower back glued to floor", "Arms/legs slightly raised"],
    contraindications=["Back Pain"], progression_from="core_plank", progression_to="core_hollow_rock"
))
_register(Exercise(
    id="core_leg_raise", name="Lying Leg Raise", category="Core", difficulty="Novice",
    muscles_primary=["Lower Abs", "Hip Flexors"], muscles_secondary=["Core"],
    default_reps=10, coaching_cues=["Keep legs straight", "Lower slowly without touching floor", "Lower back flat"],
    contraindications=["Back Pain", "Hip Issues"], progression_to="core_hanging_leg_raise"
))
_register(Exercise(
    id="core_flutter_kicks", name="Flutter Kicks", category="Core", difficulty="Novice",
    muscles_primary=["Lower Abs", "Hip Flexors"], muscles_secondary=["Core"],
    is_timed=True, default_duration_seconds=30, coaching_cues=["Legs straight, slightly off floor", "Small rapid kicks"],
    contraindications=["Back Pain", "Hip Issues"]
))
_register(Exercise(
    id="core_russian_twists", name="Russian Twists", category="Core", difficulty="Novice",
    muscles_primary=["Obliques", "Core"], muscles_secondary=["Hip Flexors"],
    default_reps=16, coaching_cues=["Sit in V-shape", "Rotate shoulders side to side", "Touch floor on each side"],
    contraindications=["Back Pain"]
))
_register(Exercise(
    id="core_side_plank_dips", name="Side Plank Dips", category="Core", difficulty="Novice",
    muscles_primary=["Obliques", "Core"], muscles_secondary=["Shoulders"],
    default_reps=10, coaching_cues=["Side plank position", "Lower hip to floor and raise back up"],
    contraindications=["Shoulder Problems", "Back Pain"], progression_from="core_side_plank"
))
_register(Exercise(
    id="core_v_up", name="V-Up", category="Core", difficulty="Intermediate",
    muscles_primary=["Core", "Rectus Abdominis"], muscles_secondary=["Hip Flexors"],
    default_reps=10, coaching_cues=["Simultaneously lift arms and legs", "Touch hands to toes", "Form a V"],
    contraindications=["Back Pain"], progression_from="core_leg_raise"
))
_register(Exercise(
    id="core_hollow_rock", name="Hollow Rock", category="Core", difficulty="Intermediate",
    muscles_primary=["Core", "Rectus Abdominis"], muscles_secondary=["Hip Flexors"],
    is_timed=True, default_duration_seconds=20, coaching_cues=["Maintain hollow shape", "Rock forward and back gently"],
    contraindications=["Back Pain"], progression_from="core_hollow_hold"
))
_register(Exercise(
    id="core_hanging_knee_raise", name="Hanging Knee Raise", category="Core", difficulty="Intermediate",
    muscles_primary=["Lower Abs", "Core"], muscles_secondary=["Hip Flexors", "Grip"],
    default_reps=10, coaching_cues=["Hang from bar", "Pull knees up to chest", "Control descent"],
    contraindications=["Shoulder Problems"], progression_from="core_leg_raise", progression_to="core_hanging_leg_raise"
))
_register(Exercise(
    id="core_bicycle_crunches", name="Bicycle Crunches", category="Core", difficulty="Intermediate",
    muscles_primary=["Obliques", "Rectus Abdominis"], muscles_secondary=["Hip Flexors"],
    default_reps=20, coaching_cues=["Opposite elbow to opposite knee", "Extend other leg straight", "Continuous motion"],
    contraindications=["Back Pain", "Neck Pain"]
))
_register(Exercise(
    id="core_hanging_leg_raise", name="Hanging Straight Leg Raise", category="Core", difficulty="Advanced",
    muscles_primary=["Core", "Lower Abs", "Hip Flexors"], muscles_secondary=["Grip", "Shoulders"],
    default_reps=8, coaching_cues=["Hang with straight legs", "Raise legs until parallel to floor", "No swinging"],
    contraindications=["Shoulder Problems", "Hip Issues"], progression_from="core_hanging_knee_raise", progression_to="core_toes_to_bar"
))
_register(Exercise(
    id="core_toes_to_bar", name="Toes to Bar", category="Core", difficulty="Advanced",
    muscles_primary=["Core", "Lats", "Hip Flexors"], muscles_secondary=["Grip", "Shoulders"],
    default_reps=6, coaching_cues=["Raise straight legs all the way until toes touch the bar"],
    contraindications=["Shoulder Problems", "Back Pain"], progression_from="core_hanging_leg_raise"
))
_register(Exercise(
    id="core_dragon_flag_tuck", name="Tuck Dragon Flag", category="Core", difficulty="Advanced",
    muscles_primary=["Core", "Rectus Abdominis"], muscles_secondary=["Lats", "Lower Back"],
    default_reps=5, coaching_cues=["Hold bench behind head", "Tuck knees", "Roll onto upper back, lift hips high"],
    contraindications=["Back Pain", "Neck Pain"], progression_to="core_dragon_flag"
))
_register(Exercise(
    id="core_dragon_flag", name="Dragon Flag", category="Core", difficulty="Advanced",
    muscles_primary=["Core", "Rectus Abdominis"], muscles_secondary=["Lats", "Lower Back"],
    default_reps=3, coaching_cues=["Body straight like a board", "Rest only on upper back", "Lower and raise whole body"],
    contraindications=["Back Pain", "Neck Pain"], progression_from="core_dragon_flag_tuck", progression_to="core_human_flag"
))
_register(Exercise(
    id="core_l_sit", name="L-Sit Hold", category="Core", difficulty="Advanced",
    muscles_primary=["Core", "Hip Flexors", "Triceps"], muscles_secondary=["Shoulders", "Quads"],
    is_timed=True, default_duration_seconds=10, coaching_cues=["Support on hands/parallettes", "Legs straight and parallel to floor"],
    contraindications=["Wrist Pain", "Hip Issues"]
))
_register(Exercise(
    id="core_human_flag", name="Human Flag Hold", category="Core", difficulty="Advanced",
    muscles_primary=["Obliques", "Core", "Shoulders", "Lats"], muscles_secondary=["Back"],
    is_timed=True, default_duration_seconds=5, coaching_cues=["Grip vertical pole", "Body horizontal", "Extreme tension"],
    contraindications=["Shoulder Problems", "Back Pain", "Wrist Pain"], progression_from="core_dragon_flag"
))


# ── CONDITIONING (10 exercises) ──────────────────────────────────────────

_register(Exercise(
    id="cond_high_knees", name="High Knees", category="Conditioning", difficulty="Beginner",
    muscles_primary=["Hip Flexors", "Quadriceps"], muscles_secondary=["Core", "Calves"],
    is_timed=True, default_duration_seconds=30, coaching_cues=["Run in place", "Drive knees up high", "Pump arms"],
    contraindications=["Knee Issues", "Ankle Issues"]
))
_register(Exercise(
    id="cond_jumping_jacks", name="Jumping Jacks", category="Conditioning", difficulty="Beginner",
    muscles_primary=["Full Body"], muscles_secondary=["Calves", "Shoulders", "Core"],
    is_timed=True, default_duration_seconds=45, coaching_cues=["Standard jumping jacks", "Continuous pace"],
    contraindications=["Ankle Issues"]
))
_register(Exercise(
    id="cond_butt_kicks", name="Butt Kicks", category="Conditioning", difficulty="Beginner",
    muscles_primary=["Hamstrings"], muscles_secondary=["Calves", "Quadriceps"],
    is_timed=True, default_duration_seconds=30, coaching_cues=["Jog in place", "Kick heels up to glutes"],
    contraindications=["Knee Issues"]
))
_register(Exercise(
    id="cond_mountain_climbers", name="Mountain Climbers", category="Conditioning", difficulty="Novice",
    muscles_primary=["Core", "Hip Flexors"], muscles_secondary=["Shoulders", "Quadriceps"],
    is_timed=True, default_duration_seconds=30, coaching_cues=["Plank position", "Drive knees to chest alternately", "Fast pace"],
    contraindications=["Wrist Pain", "Shoulder Problems"]
))
_register(Exercise(
    id="cond_skater_hops", name="Skater Hops", category="Conditioning", difficulty="Novice",
    muscles_primary=["Glutes", "Quadriceps"], muscles_secondary=["Calves", "Core"],
    default_reps=16, coaching_cues=["Leap side to side", "Land softly on one foot", "Sweep other leg behind"],
    contraindications=["Knee Issues", "Ankle Issues"]
))
_register(Exercise(
    id="cond_seal_jacks", name="Seal Jacks", category="Conditioning", difficulty="Novice",
    muscles_primary=["Chest", "Shoulders", "Calves"], muscles_secondary=["Core"],
    is_timed=True, default_duration_seconds=40, coaching_cues=["Like jumping jacks, but arms open and close in front of chest"],
    contraindications=["Ankle Issues", "Shoulder Problems"]
))
_register(Exercise(
    id="cond_burpees", name="Burpees", category="Conditioning", difficulty="Intermediate",
    muscles_primary=["Full Body"], muscles_secondary=["Chest", "Quadriceps", "Core", "Shoulders"],
    default_reps=10, coaching_cues=["Squat, jump to plank", "Push-up", "Jump to squat, jump up"],
    contraindications=["Wrist Pain", "Knee Issues", "Back Pain"]
))
_register(Exercise(
    id="cond_squat_jumps_continuous", name="Continuous Squat Jumps", category="Conditioning", difficulty="Intermediate",
    muscles_primary=["Quadriceps", "Glutes"], muscles_secondary=["Calves", "Core"],
    is_timed=True, default_duration_seconds=30, coaching_cues=["Non-stop squat jumps", "Pacing is key", "Soft landings"],
    contraindications=["Knee Issues", "Ankle Issues"]
))
_register(Exercise(
    id="cond_tuck_jumps", name="Tuck Jumps", category="Conditioning", difficulty="Advanced",
    muscles_primary=["Quadriceps", "Core", "Hip Flexors"], muscles_secondary=["Calves", "Glutes"],
    default_reps=10, coaching_cues=["Jump high", "Pull knees up to chest in mid-air", "Land softly"],
    contraindications=["Knee Issues", "Ankle Issues", "Back Pain"]
))
_register(Exercise(
    id="cond_sprawls", name="Sprawls", category="Conditioning", difficulty="Advanced",
    muscles_primary=["Full Body", "Core"], muscles_secondary=["Shoulders", "Hip Flexors"],
    default_reps=12, coaching_cues=["Drop hips quickly to floor into a sprawling plank", "Pop immediately back to feet"],
    contraindications=["Wrist Pain", "Back Pain", "Shoulder Problems"]
))


# ── MOBILITY (10 exercises) ──────────────────────────────────────────────

_register(Exercise(
    id="mob_child_pose", name="Child Pose", category="Mobility", difficulty="Beginner",
    muscles_primary=["Lower Back", "Hips"], muscles_secondary=["Shoulders", "Lats"],
    is_timed=True, default_duration_seconds=30, coaching_cues=["Kneel, sit back on heels", "Extend arms forward"],
    contraindications=["Knee Issues"]
))
_register(Exercise(
    id="mob_cobra_stretch", name="Cobra Stretch", category="Mobility", difficulty="Beginner",
    muscles_primary=["Core", "Hip Flexors"], muscles_secondary=["Lower Back", "Chest"],
    is_timed=True, default_duration_seconds=20, coaching_cues=["Lie face down", "Press chest up, keep hips down"],
    contraindications=["Back Pain"]
))
_register(Exercise(
    id="mob_cat_cow", name="Cat Cow", category="Mobility", difficulty="Beginner",
    muscles_primary=["Spine", "Core"], muscles_secondary=["Shoulders", "Hips"],
    default_reps=10, coaching_cues=["Tabletop", "Round back (cat)", "Drop belly (cow)", "Flow with breath"],
    contraindications=["Wrist Pain"]
))
_register(Exercise(
    id="mob_hip_openers", name="Deep Lunge Hip Openers", category="Mobility", difficulty="Beginner",
    muscles_primary=["Hip Flexors", "Glutes"], muscles_secondary=["Inner Thighs"],
    is_timed=True, default_duration_seconds=30, coaching_cues=["Deep lunge, back knee down", "Press hips forward gently"],
    contraindications=["Hip Issues", "Knee Issues"]
))
_register(Exercise(
    id="mob_shoulder_dislocates", name="Shoulder Dislocates (Towel/Band)", category="Mobility", difficulty="Beginner",
    muscles_primary=["Shoulders", "Chest"], muscles_secondary=["Upper Back"],
    default_reps=10, coaching_cues=["Hold towel wide", "Keep arms straight", "Rotate over head to lower back"],
    contraindications=["Shoulder Problems"]
))
_register(Exercise(
    id="mob_pigeon_pose", name="Pigeon Pose", category="Mobility", difficulty="Novice",
    muscles_primary=["Glutes", "Outer Hips"], muscles_secondary=["Lower Back"],
    is_timed=True, default_duration_seconds=30, coaching_cues=["One leg folded in front", "Other leg straight back", "Fold over front leg"],
    contraindications=["Knee Issues", "Hip Issues"]
))
_register(Exercise(
    id="mob_downward_dog", name="Downward Dog", category="Mobility", difficulty="Beginner",
    muscles_primary=["Calves", "Hamstrings"], muscles_secondary=["Shoulders", "Upper Back"],
    is_timed=True, default_duration_seconds=30, coaching_cues=["V-shape with body", "Press heels toward floor", "Push chest toward knees"],
    contraindications=["Wrist Pain", "Shoulder Problems"]
))
_register(Exercise(
    id="mob_thoracic_rotations", name="Thoracic Rotations", category="Mobility", difficulty="Beginner",
    muscles_primary=["Upper Back", "Spine"], muscles_secondary=["Chest", "Shoulders"],
    default_reps=10, coaching_cues=["Tabletop position", "Hand behind head", "Rotate elbow up to ceiling, then down under body"],
    contraindications=["Back Pain"]
))
_register(Exercise(
    id="mob_asian_squat", name="Deep Resting Squat (Asian Squat)", category="Mobility", difficulty="Novice",
    muscles_primary=["Hips", "Ankles", "Lower Back"], muscles_secondary=["Knees"],
    is_timed=True, default_duration_seconds=45, coaching_cues=["Squat as deep as possible", "Keep heels flat on floor", "Chest up"],
    contraindications=["Knee Issues", "Ankle Issues"]
))
_register(Exercise(
    id="mob_neck_circles", name="Neck Rotations", category="Mobility", difficulty="Beginner",
    muscles_primary=["Neck", "Traps"], muscles_secondary=[],
    default_reps=10, coaching_cues=["Slow, controlled circles", "Don't force range of motion", "Both directions"],
    contraindications=["Neck Pain"]
))


# ═══════════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def get_exercise(exercise_id: str) -> Optional[Exercise]:
    """Get a single exercise by its ID."""
    return EXERCISES.get(exercise_id)


def get_exercises_by_category(category: str) -> List[Exercise]:
    """Get all exercises in a given category."""
    return [e for e in EXERCISES.values() if e.category == category]


def get_exercises_by_difficulty(difficulty: str) -> List[Exercise]:
    """Get all exercises at a given difficulty level."""
    return [e for e in EXERCISES.values() if e.difficulty == difficulty]


def get_exercises_for_level(
    category: str,
    difficulty: str,
    limitations: Optional[List[str]] = None,
) -> List[Exercise]:
    """Get exercises filtered by category, difficulty, and contraindications.

    Returns exercises at or below the specified difficulty that are safe
    given the user's physical limitations.
    """
    difficulty_order = ["Beginner", "Novice", "Intermediate", "Advanced"]
    max_idx = difficulty_order.index(difficulty) if difficulty in difficulty_order else 0
    allowed_difficulties = difficulty_order[: max_idx + 1]

    limitations = limitations or []
    limitation_set = set(limitations)

    return [
        e
        for e in EXERCISES.values()
        if e.category == category
        and e.difficulty in allowed_difficulties
        and not limitation_set.intersection(set(e.contraindications))
    ]


def get_all_categories() -> List[str]:
    """Return all unique exercise categories."""
    return list(sorted(set(e.category for e in EXERCISES.values())))


def get_progression_chain(exercise_id: str) -> List[Exercise]:
    """Get the full progression chain for an exercise."""
    current = EXERCISES.get(exercise_id)
    if not current:
        return []

    # Walk backward to the easiest
    chain_start = current
    while chain_start.progression_from and chain_start.progression_from in EXERCISES:
        chain_start = EXERCISES[chain_start.progression_from]

    # Walk forward to build the chain
    chain: List[Exercise] = [chain_start]
    while chain[-1].progression_to and chain[-1].progression_to in EXERCISES:
        chain.append(EXERCISES[chain[-1].progression_to])

    return chain
