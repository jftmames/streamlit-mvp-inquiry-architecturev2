# erotetic_equilibrium_evaluator.py

import openai
import os
from dotenv import load_dotenv
import streamlit as st

# Cargar clave API
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def evaluate_equilibrium(subquestion, response):
    """
    Evalúa si una respuesta se mantiene en equilibrio erotético.
    
    Returns:
        dict: {
            "estado": "estable" | "inestable",
            "contra_preguntas": [...],
            "comentario": str
        }
    """
    prompt = (
        f"A continuación se presenta una subpregunta y una respuesta generada.\n\n"
        f"Subpregunta: {subquestion}\n"
        f"Respuesta: {response}\n\n"
        f"Tu tarea es:\n"
        f"1. Generar 2 o 3 contra-preguntas críticas que pongan a prueba la coherencia, completitud o consistencia de la respuesta.\n"
        f"2. Evaluar si la respuesta se mantiene válida frente a esas preguntas.\n"
        f"3. Concluir si la respuesta está en equilibrio o no.\n\n"
        f"Formato de salida:\n"
        f"Contra-preguntas:\n"
        f"- ...\n"
        f"Evaluación:\n"
        f"- Equilibrio: Sí / No\n"
        f"- Comentario: ..."
    )

    try:
        response_eval = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un verificador experto en razonamiento epistémico."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=600
        )

        output_text = response_eval.choices[0].message.content

        # Interpretar resultado de forma simplificada
        estado = "inestable" if "Equilibrio: No" in output_text else "estable"
        contra_preguntas = []
        for line in output_text.splitlines():
            if line.strip().startswith("- "):
                contra_preguntas.append(line.strip("- ").strip())

        return {
            "estado": estado,
            "contra_preguntas": contra_preguntas,
            "comentario": output_text
        }

    except Exception as e:
        st.error(f"Error en evaluación de equilibrio: {e}")
        return {
            "estado": "error",
            "contra_preguntas": [],
            "comentario": str(e)
        }
