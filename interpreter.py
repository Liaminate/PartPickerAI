import openai
import os
import json  # Import JSON for safer parsing\
import datetime
from dotenv import load_dotenv


def configure():
    load_dotenv() 

openai.api_key = os.getenv('OPENAI_API_KEY')


def interpreter_query(text):
    now = datetime.datetime.now()
    system_prompt = f"""
                        You are a vehicle part query parser. Given a user query like:
                        "I need an alternator for a 1990 mazda miata"
                        Extract the following as JSON:
                        {{
                        "year": "optional - can be null",
                        "make": "<standardized>",
                        "model": "<standardized>",
                        "part": "<thing they want>"
                        }}
                        Standardize common nicknames (e.g., "miata" = "MX-5 MIATA", "beetle" = "NEW BEETLE").
                        The current date and time is: {now.strftime('%Y-%m-%d %H:%M:%S')}.
                    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ]

    try:
        response = openai.chat.completions.create(
            model="gpt-4.1-mini",
            max_tokens=250,
            messages=messages,
            temperature=0,
        )
        content = response.choices[0].message.content
        return json.loads(content)  # Safely parse the JSON response
    except json.JSONDecodeError:
        raise ValueError("The response is not valid JSON.")
    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")

