# app.py

import streamlit as st
from inquiry_engine import generate_subquestions
from epistemic_navigator import display_navigation
from contextual_generator import generate_contextual_response
from adaptive_dialogue import adaptive_dialogue_flow
from reasoning_tracker import ReasoningTracker
from erotetic_equilibrium_evaluator import evaluate_equilibrium

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
