# Arquitectura Cognitiva para Modelos de Lenguaje Generativo basada en Complejos de Indagación Jerárquicos

Este proyecto implementa un prototipo mínimo viable (MVP) de una arquitectura cognitiva diseñada para modelos de lenguaje generativo (LLMs), basada en la navegación, expansión y resolución de **complejos de indagación jerárquicos**.

## Objetivo
Desarrollar una prueba de concepto funcional que:
- Estructure el razonamiento de la IA en forma de redes jerárquicas de preguntas.
- Permita una navegación epistémica deliberada.
- Genere respuestas adaptadas al estado del complejo de indagación.
- Registre y justifique el proceso de razonamiento seguido.

## Módulos principales
- **Inquiry Engine**: Motor de formulación de preguntas.
- **Epistemic Navigator**: Motor de navegación epistémica.
- **Contextual Generator**: Generador de respuestas reflexivas.
- **Adaptive Dialogue Engine**: Motor de diálogo adaptativo.
- **Reasoning Tracker**: Registrador de trayectorias de indagación.

## Tecnologías utilizadas
- Python 3.11
- Streamlit
- OpenAI API (o modelos equivalentes)
- Graphviz (para visualización de preguntas, opcional)
- Pandas / JSON (para registro de razonamiento)

## Cómo ejecutar el proyecto
1. Clonar este repositorio:

		git clone https://github.com/tu_usuario/streamlit-mvp-inquiry-architecture.git

2. Instalar las dependencias:
		pip install -r requirements.txt


3. Ejecutar la app:
		streamlit run app.py

## Estado del proyecto
- [x] Estructura inicial creada
- [ ] Desarrollo de Inquiry Engine
- [ ] Desarrollo de Epistemic Navigator
- [ ] Integración de módulos en Streamlit
- [ ] Documentación final

## Autor
José Fernández Tamames

---