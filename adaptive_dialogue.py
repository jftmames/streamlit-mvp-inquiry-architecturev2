# adaptive_dialogue.py

import openai
import os
from dotenv import load_dotenv
import streamlit as st

# Cargar variables de entorno
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def adaptive_dialogue_flow(current_subquestion):
    """
    Permite al usuario refinar la subpregunta o abrir nuevas líneas de indagación.

    Args:
        current_subquestion (str): Subpregunta actual elegida.
    """
    st.write("### ¿Quieres refinar aún más esta subpregunta?")
    refine = st.radio(
        "Elige una opción:",
        ("No, continuar", "Sí, generar refinamientos")
    )

    if refine == "Sí, generar refinamientos":
        try:
            refinement_prompt = (
                f"A partir de la siguiente subpregunta:\n\n"
                f"\"{current_subquestion}\"\n\n"
                f"Genera entre 2 y 3 sub-subpreguntas que permitan explorar el tema con mayor detalle, "
                f"considerando aspectos conceptuales, metodológicos o éticos. Sé específico y crítico."
            )

            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Eres un experto en análisis crítico y generación de preguntas profundas."},
                    {"role": "user", "content": refinement_prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )

            output_text = response.choices[0].message.content
            refinements = [line.strip("- ").strip() for line in output_text.split("\n") if line.strip()]

            st.write("### Sub-subpreguntas sugeridas:")
            for idx, ref in enumerate(refinements):
                st.markdown(f"- {ref}")

            st.success("Puedes elegir alguna sub-subpregunta para seguir indagando o simplemente reflexionar sobre ellas.")
        
        except Exception as e:
            st.error(f"Error generando refinamientos: {e}")

    else:
        st.info("Continuando con la subpregunta seleccionada.")
