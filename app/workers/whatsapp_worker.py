"""Service to handle WhatsApp webhook processing logic."""
from app.services.whatsapp_database_service import (
    save_workout_to_db,
    user_exists,
    save_user_to_db,
    select_last_exercise_workout
)
from app.services.openai_service import parse_whatsapp_message, prepare_response_with_last_workout
from app.services.whatsapp_sender import send_whatsapp_message
from app.utils.redis_connection import send_queue

def process_incoming_message(data: dict):
    """All logic from what to do with WhatsApp Message webhook data"""
    message = data.get("message_body") or ""
    user_name = data.get("contact_name") or ""
    user_number = data.get("from") or ""

    user_exists_flag = user_exists(user_number)
    if user_exists_flag is False:
        save_user_to_db({
            "name": user_name,
            "number": user_number
        })

    function_name, openai_response = parse_whatsapp_message(message)

    if function_name == "register_workouts":
        for workout in openai_response["exercises"]:
            save_workout_to_db(user_number, workout)
            process_whatsapp_message(user_number, workout)
    else:
        process_whatsapp_openai_message(user_number, openai_response)

def process_whatsapp_message(user_number: str, current_exercise) -> None:
    """All logic from what to do with WhatsApp Message webhook data"""
    exercise_name = current_exercise.get("exercise")
    last_exercise = select_last_exercise_workout(user_number, exercise_name)
    whatsapp_response = prepare_response_with_last_workout(current_exercise, last_exercise)

    print(f"Enviando resposta para {user_number}: {whatsapp_response}")

    send_queue.enqueue(send_whatsapp_message, user_number, whatsapp_response)

def process_whatsapp_openai_message(user_number: str, message: str | dict) -> None:
    """Process message returned from OpenAI that is not a workout registration."""
    send_queue.enqueue(send_whatsapp_message, user_number, message)

def process_whatsapp_common_message(user_number: str) -> None:
    """Process common message that does not match any function."""
    whatsapp_response = (
        "Desculpe, não consegui entender sua mensagem. "
        "Por favor, envie seus treinos no formato correto. "
        "Exemplo:\n"
        "Supino 3x10 50kg\n"
        "Agachamento 4x8 70kg"
    )

    send_queue.enqueue(send_whatsapp_message, user_number, whatsapp_response)
