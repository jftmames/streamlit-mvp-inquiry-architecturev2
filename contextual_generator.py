# contextual_generator.py

import openai
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_contextual_response(subquestion):
    prompt = (
        f"Responde de manera reflexiva y estructurada a la siguiente subpregunta:\n\n"
        f"\"{subquestion}\"\n\n"
        f"La respuesta debe incluir:\n"
        f"- Una explicación conceptual breve.\n"
        f"- Un análisis crítico (opciones o enfoques posibles).\n"
        f"- Consideraciones éticas o metodológicas relevantes si aplica.\n"
        f"Usa un estilo claro, objetivo y profesional."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en razonamiento científico y reflexivo."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        output_text = response.choices[0].message.content
        return output_text

    except Exception as e:
        print(f"Error generando respuesta contextual: {e}")
        return "No se pudo generar una respuesta en este momento."
