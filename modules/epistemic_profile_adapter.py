"""
Epistemic Profile Adapter (EPA)
--------------------------------
Capa de personalización: carga un perfil epistémico y expone utilidades
para adaptar prompts, pesos heurísticos y umbrales de evaluación.
"""

from dataclasses import dataclass
from typing import Dict

# ---- 1. Definición de perfiles base -----------------------------------------

@dataclass
class EpistemicProfile:
    name: str
    tone: str                  # tono narrativo (“formal”, “informal”, “experto”…)
    depth_factor: float        # 0-1 → controla longitud / detalle de respuestas
    nav_priorities: Dict[str, float]  # pesos para el Epistemic Navigator
    eee_threshold: float       # valor diana para Equilibrio Erotético
    critique_level: str        # “suave”, “moderada”, “dura” para ECE

DEFAULT_PROFILES = {
    "educativo": EpistemicProfile(
        name="educativo",
        tone="didáctico",
        depth_factor=0.7,
        nav_priorities={"definiciones": 0.6, "ejemplos": 0.9, "crítica": 0.4},
        eee_threshold=0.6,
        critique_level="suave",
    ),
    "juridico": EpistemicProfile(
        name="juridico",
        tone="formal-jurídico",
        depth_factor=0.85,
        nav_priorities={"jurisprudencia": 1.0, "principios": 0.8, "casos": 0.7},
        eee_threshold=0.75,
        critique_level="moderada",
    ),
    "clinico": EpistemicProfile(
        name="clinico",
        tone="científico-clínico",
        depth_factor=0.8,
        nav_priorities={"evidencia": 1.0, "riesgos": 0.9, "ética": 0.6},
        eee_threshold=0.8,
        critique_level="moderada",
    ),
    "etico": EpistemicProfile(
        name="etico",
        tone="reflexivo-ético",
        depth_factor=0.9,
        nav_priorities={"principios": 1.0, "dilemas": 0.8, "casuística": 0.7},
        eee_threshold=0.8,
        critique_level="dura",
    ),
}

# ---- 2. API pública ----------------------------------------------------------

def load_profile(profile_name: str) -> EpistemicProfile:
    """Devuelve el perfil solicitado o uno por defecto."""
    return DEFAULT_PROFILES.get(profile_name.lower(), DEFAULT_PROFILES["educativo"])


def adapt_prompt(prompt: str, profile: EpistemicProfile) -> str:
    """Inyecta información del perfil en el prompt para el LLM."""
    header = (
        f"Eres un asistente con tono {profile.tone}. "
        f"Profundidad deseada: {int(profile.depth_factor*100)}%. "
        "Responde de acuerdo con el dominio y prioriza los siguientes focos: "
        + ", ".join([f"{k}={v}" for k, v in profile.nav_priorities.items()])
        + ".\n\n"
    )
    return header + prompt


def get_nav_weights(profile: EpistemicProfile) -> Dict[str, float]:
    """Devuelve pesos para Epistemic Navigator."""
    return profile.nav_priorities


def get_eee_target(profile: EpistemicProfile) -> float:
    """Umbral objetivo para el Evaluador de Equilibrio Erotético."""
    return profile.eee_threshold


def get_critique_level(profile: EpistemicProfile) -> str:
    """Nivel de severidad para el Epistemic Critique Engine."""
    return profile.critique_level

