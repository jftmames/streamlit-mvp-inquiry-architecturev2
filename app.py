# ──────────────────────────────────────────────────────────────
# app.py – MVP Arquitectura Cognitiva (versión consolidada)
# ──────────────────────────────────────────────────────────────
import streamlit as st

# Configuración de página (¡DEBE ser la 1.ª instrucción Streamlit!)
st.set_page_config(
    page_title="Arquitectura Cognitiva - Complejos de Indagación",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ╭─────────────────────────── Import propios ─────────────────────────╮
from modules.epistemic_profile_adapter import (
    load_profile,
    adapt_prompt,
    get_nav_weights,
    get_eee_target,
    get_critique_level,
)

from inquiry_engine import generate_subquestions
from epistemic_navigator import display_navigation
from contextual_generator import generate_contextual_response
from adaptive_dialogue import adaptive_dialogue_flow
from reasoning_tracker import ReasoningTracker
from erotetic_equilibrium_evaluator import evaluate_equilibrium

# Si tu orquestador general está en core/engine.py:
from core.engine import run_deliberation
# ╰────────────────────────────────────────────────────────────────────╯


# ╭──────────────────────── Sidebar: Perfil epistémico ───────────────╮
st.sidebar.title("⚙️ Perfil epistémico")
profile_name = st.sidebar.selectbox(
    "Selecciona contexto:",
    ("educativo", "juridico", "clinico", "etico"),
)
profile = load_profile(profile_name)
st.session_state["epistemic_profile"] = profile
# ╰────────────────────────────────────────────────────────────────────╯


# ╭─────────────────────────── Título principal ──────────────────────╮
st.title("Arquitectura Cognitiva para Modelos de Lenguaje Generativo")
st.subheader(
    "Explora y verifica trayectorias epistémicas mediante complejos de indagación jerárquicos"
)
# ╰────────────────────────────────────────────────────────────────────╯


# ╭──────────────────────────────── Inicialización ────────────────────╮
if "tracker" not in st.session_state:
    st.session_state.tracker = ReasoningTracker()
# ╰────────────────────────────────────────────────────────────────────╯


# ╭───────────────────────── Entrada pregunta central ────────────────╮
user_question = st.text_input("Introduce tu pregunta central:")

if st.button("Analizar (modo completo)"):
    # —— Adaptar prompt al perfil
    full_prompt = adapt_prompt(user_question, profile)

    # —— Parámetros epistémicos
    nav_weights = get_nav_weights(profile)
    eee_target = get_eee_target(profile)
    critique_level = get_critique_level(profile)

    # —— Ejecución del motor deliberativo global
    result = run_deliberation(
        prompt=full_prompt,
        nav_priorities=nav_weights,
        eee_target=eee_target,
        critique_level=critique_level,
    )
    st.write(result)


# ╭───────────────────── Flujo interactivo paso a paso ───────────────╮
if user_question:

    # 1️⃣  Generar subpreguntas
    subquestions = generate_subquestions(user_question)
    st.write("### Subpreguntas generadas:")
    for i, sq in enumerate(subquestions, start=1):
        st.write(f"{i}. {sq}")

    # 2️⃣  Mostrar mapa de navegación
    st.write("### Mapa de Indagación:")
    display_navigation(user_question, subquestions)

    # 3️⃣  Selección de subpregunta
    sel_idx = st.selectbox(
        "Selecciona una subpregunta para explorar:",
        range(len(subquestions)),
        format_func=lambda x: f"{x+1}",
    )

    if st.button("Explorar subpregunta"):
        selected_question = subquestions[sel_idx]
        st.write("### Subpregunta seleccionada:")
        st.info(selected_question)

        # 3.a  Diálogo adaptativo
        adaptive_dialogue_flow(selected_question)

        # 3.b  Respuesta contextual
        st.write("### Respuesta reflexiva generada:")
        contextual_resp = generate_contextual_response(selected_question)
        st.write(contextual_resp)

        # 3.c  Evaluación de equilibrio
        eee = evaluate_equilibrium(selected_question, contextual_resp)
        if eee["estado"] != "error":
            st.subheader("⚖️ Evaluación de Equilibrio Erotético")
            st.write(f"**Estado:** {eee['estado'].capitalize()}")
            st.write("**Contra-preguntas generadas:**")
            for q in eee["contra_preguntas"]:
                st.markdown(f"- {q}")
            with st.expander("Ver comentario completo del verificador"):
                st.markdown(eee["comentario"])

        # 3.d  Registro en el tracker
        st.session_state.tracker.add_entry(
            user_question=user_question,
            subquestion=selected_question,
            response=contextual_resp,
            refinements=eee["contra_preguntas"],
        )
        st.success("Entrada registrada en el historial.")

    # 4️⃣  Historial y exportación
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
# ╰────────────────────────────────────────────────────────────────────╯
