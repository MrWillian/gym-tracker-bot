"""Service to interact with OpenAI API."""
import os
import json
from openai import OpenAI

client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)

functions = [
    {
        "name": "register_workouts",
        "description": "Extrai uma lista de treinos de uma mensagem do usuário",
        "parameters": {
            "type": "object",
            "properties": {
                "exercises": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "exercise": {"type": "string"},
                            "sets": {"type": "integer"},
                            "reps": {"type": "integer"},
                            "weight": {"type": "number"},
                            "equipment": {"type": "string"}
                        },
                        "required": ["exercise", "sets", "reps"]
                    }
                }
            },
            "required": ["exercises"]
        }
    }
]

SYSTEM_PROMPT = """
Você é um assistente especializado em treinos.
Sua função é extrair exercícios de mensagens informais do WhatsApp e estruturar em JSON.

Regras:
- Uma mesma mensagem pode conter 1 ou vários exercícios.
- Identifique corretamente o exercício (ex: supino reto, voador, agachamento).
- Sempre extraia: sets (séries), reps (repetições) e weight (peso, se existir).
- Inferir o tipo de equipamento:
    - supino reto com 50kg ou mais → provavelmente “barra”
    - supino reto com 10–35kg → halteres
    - se a pessoa escrever “máquina” → equipamento = máquina
    - se não conseguir inferir → null
- Retorne *sempre* um array “exercises”.

Se houver múltiplas linhas, cada linha deve virar 1 exercício.
Caso esta mensagem não contenha exercício(s), responda a ela apropriadamente sem chamar a função.
"""

def parse_whatsapp_message(message: str) -> tuple[str | None, dict]:
    """
    Use GPT to sanitize the incoming message.
    """
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ],
        functions=functions,
        function_call="auto"
    )

    choice = response.choices[0]

    if choice.finish_reason == "function_call":
        function_name = choice.message.function_call.name
        raw_args = choice.message.function_call.arguments
        data = json.loads(raw_args)
        return function_name, data

    return None, choice.message.content

def prepare_response_with_last_workout(current_workout: dict, last_workout: dict | None) -> str:
    """Prepare a response comparing with the last workout."""
    if last_workout:
        prompt = (
            "Elabore uma resposta amigável para o usuário, "
            "comparando seu treino atual com o último treino registrado, "
            "destacando melhorias e motivando-o a continuar."
        )
        prompt += (
            "Responda de forma breve e direta, com no máximo 2 frases curtas, "
            "focando apenas nos pontos mais importantes da comparação. "
            "Use uma linguagem motivacional e adequada para WhatsApp."
        )
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": f"Último treino: {last_workout}, Treino atual: {current_workout}"
                }
            ],
            temperature=0.2
        )
        return response.choices[0].message.content
    return "Treino registrado com sucesso! Este é o seu primeiro registro para este exercício."
