import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"


def generate_ai_reply(email_text: str, sender_name: str, user_name: str):
    prompt = f"""
You are a professional email assistant.

Write a complete professional email reply.

Rules:
- Use proper greeting with sender name
- Keep tone polite and natural
- Do NOT use placeholders
- End with user's name

Sender Name: {sender_name}
User Name: {user_name}

Email:
{email_text}

Reply:
"""

    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/free",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    data = response.json()

    return data["choices"][0]["message"]["content"]


def generate_custom_reply(email_text: str, instruction: str, sender_name: str, user_name: str):
    prompt = f"""
You are a professional email assistant.

Write a complete formal email reply.

Rules:
- Always start with: Dear {sender_name},
- Add a blank line after greeting
- Clearly respond to the email using the instruction
- Keep tone polite and professional
- End with:

Best regards,  
{user_name}

- Do NOT use user's name in greeting
- Do NOT leave signature incomplete
- Do NOT use placeholders

Email:
{email_text}

Instruction:
{instruction}

Reply:
"""

    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/free",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    data = response.json()

    return data["choices"][0]["message"]["content"]