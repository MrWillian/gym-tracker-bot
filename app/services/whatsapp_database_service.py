"""Service to handle with database operations for WhatsApp messages."""
from app.database.supabase_client import supabase
from app.helpers.sanitize import normalize_exercise_name

def user_exists(user_number):
    """Check if a user exists in the Supabase database."""
    response = supabase.table("users").select("number").eq(
        "number", user_number
    ).execute()
    return len(response.data) > 0

def save_user_to_db(user_data):
    """Save the user data to the Supabase database."""
    supabase.table("users").insert(user_data).execute()

def save_workout_to_db(user_number: str, data: dict):
    """Save the workout data to the Supabase database."""
    exercise_name = normalize_exercise_name(data.get("exercise"))

    supabase.table("workouts").insert({
        "user_number": user_number,
        "exercise": exercise_name,
        "sets": data.get("sets"),
        "reps": data.get("reps"),
        "weight": data.get("weight")
    }).execute()

def select_last_exercise_workout(user_number, exercise_name) -> dict | None:
    """Select the last workout for a specific exercise by the user."""
    response = supabase.table("workouts").select("sets", "reps", "weight").eq(
        "user_number", user_number
    ).eq(
        "exercise", exercise_name
    ).order("created_at", desc=True).limit(1).execute()
    if response.data:
        return response.data[0]
    return None
