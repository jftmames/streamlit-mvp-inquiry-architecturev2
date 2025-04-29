# epistemic_navigator.py

import streamlit as st

def display_navigation(main_question, subquestions):
    st.write("**Pregunta Central:**")
    st.info(main_question)

    st.write("**Exploración de Subpreguntas:**")
    for idx, subq in enumerate(subquestions):
        st.markdown(f"- {subq}")
