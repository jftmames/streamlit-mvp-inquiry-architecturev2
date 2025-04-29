# reasoning_tracker.py

import json
import csv
import os
from datetime import datetime
import streamlit as st

class ReasoningTracker:
    def __init__(self):
        self.records = []

    def add_entry(self, user_question, subquestion, response, refinements=None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "pregunta_central": user_question,
            "subpregunta": subquestion,
            "respuesta_generada": response,
            "refinamientos": refinements if refinements else []
        }
        self.records.append(entry)

    def show_history(self):
        st.write("### Historial de razonamiento")
        for entry in self.records:
            st.markdown(f"**[{entry['timestamp']}]**")
            st.write(f"- Pregunta central: {entry['pregunta_central']}")
            st.write(f"- Subpregunta: {entry['subpregunta']}")
            st.write(f"- Respuesta: {entry['respuesta_generada']}")
            if entry['refinamientos']:
                st.write(f"- Refinamientos: {entry['refinamientos']}")
            st.markdown("---")

    def export_to_json(self, filename="historial_razonamiento.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)
        st.success(f"Historial exportado a {filename}")

    def export_to_csv(self, filename="historial_razonamiento.csv"):
        if not self.records:
            st.warning("No hay entradas para exportar.")
            return

        keys = self.records[0].keys()
        with open(filename, "w", newline="", encoding="utf-8") as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.records)
        st.success(f"Historial exportado a {filename}")
