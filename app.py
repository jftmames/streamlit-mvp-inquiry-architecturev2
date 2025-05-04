# app.py

import streamlit as st
from inquiry_engine import generate_subquestions
from epistemic_navigator import display_navigation
from contextual_generator import generate_contextual_response
from adaptive_dialogue import adaptive_dialogue_flow
from reasoning_tracker import ReasoningTracker
from erotetic_equilibrium_evaluator import evaluate_equilibrium


# app.py  (extracto)
import streamlit as st
from modules.epistemic_profile_adapter import (
    load_profile, adapt_prompt,
    get_nav_weights, get_eee_target, get_critique_level
)

# 1. Selección de perfil desde la barra lateral
st.sidebar.title("Perfil epistémico")
profile_name = st.sidebar.selectbox(
    "Selecciona contexto:",
    ["educativo", "juridico", "clinico", "etico"]
)
profile = load_profile(profile_name)

# 2. Guarda en session_state (útil para otros módulos)
st.session_state["epistemic_profile"] = profile

# 3. Entrada del usuario
user_question = st.text_area("Plantea tu dilema o pregunta:")

if st.button("Analizar"):
    # 4. Adaptar prompt antes de enviarlo al motor / LLM
    full_prompt = adapt_prompt(user_question, profile)

    # 5. Pasar pesos y umbrales a módulos inferiores
    nav_weights = get_nav_weights(profile)
    eee_target = get_eee_target(profile)
    critique_level = get_critique_level(profile)

    # Ejemplo de llamada al motor (pseudo-código):
    from core.engine import run_deliberation
    result = run_deliberation(
        prompt=full_prompt,
        nav_priorities=nav_weights,
        eee_target=eee_target,
        critique_level=critique_level
    )
    st.write(result)

# Configurar página
st.set_page_config(page_title="Arquitectura Cognitiva - Complejos de Indagación", layout="wide")
st.title("Arquitectura Cognitiva para Modelos de Lenguaje Generativo")
st.subheader("Explora y verifica trayectorias epistémicas mediante complejos de indagación jerárquicos")

# Inicializar tracker en session_state
if "tracker" not in st.session_state:
    st.session_state.tracker = ReasoningTracker()

# Entrada de pregunta central
user_question = st.text_input("Introduce tu pregunta central:")

if user_question:
    # Generar subpreguntas
    subquestions = generate_subquestions(user_question)
    
    st.write("### Subpreguntas generadas:")
    for idx, subq in enumerate(subquestions):
        st.write(f"{idx+1}. {subq}")

    # Visualizar navegación
    st.write("### Mapa de Indagación:")
    display_navigation(user_question, subquestions)

    # Seleccionar subpregunta
    selected_idx = st.selectbox("Selecciona una subpregunta para explorar:", range(len(subquestions)))

    if st.button("Explorar Subpregunta"):
        selected_question = subquestions[selected_idx]
        st.write("### Subpregunta seleccionada:")
        st.info(selected_question)

        # Diálogo adaptativo
        adaptive_dialogue_flow(selected_question)

        # Generar respuesta contextual
        st.write("### Respuesta reflexiva generada:")
        contextual_response = generate_contextual_response(selected_question)
        st.write(contextual_response)

        # Evaluación de equilibrio erotético
        eee_result = evaluate_equilibrium(selected_question, contextual_response)
        if eee_result["estado"] != "error":
            st.subheader("⚖️ Evaluación de Equilibrio Erotético")
            st.write(f"**Estado:** {eee_result['estado'].capitalize()}")
            st.write("**Contra-preguntas generadas:**")
            for q in eee_result["contra_preguntas"]:
                st.markdown(f"- {q}")
            with st.expander("Ver comentario completo del verificador"):
                st.markdown(eee_result["comentario"])

        # Registrar razonamiento
        st.session_state.tracker.add_entry(
            user_question=user_question,
            subquestion=selected_question,
            response=contextual_response,
            refinements=eee_result["contra_preguntas"]
        )
        st.success("Entrada registrada en el historial.")

    # Mostrar historial y exportar
    st.markdown("---")
    st.subheader("Historial de Razonamiento")

    if st.button("Mostrar historial"):
        st.session_state.tracker.show_history()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Exportar como JSON"):
            st.session_state.tracker.export_to_json()
    with col2:
        if st.button("Exportar como CSV"):
            st.session_state.tracker.export_to_csv()
