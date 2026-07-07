"""
Selector dinámico de modelos de IA de OpenGravity.
===================================================
Consulta las APIs activas de Groq y OpenRouter para mapear
y elegir el mejor modelo disponible según la categoría de la tarea.
"""

import re
import logging
from opengravity.clients.groq_client import GroqClient
from opengravity.clients.openrouter_client import OpenRouterClient

logger = logging.getLogger("opengravity.orchestrator.selector")

# Preferencias ordenadas de modelos (regex matching) por categoría técnica
MODEL_PREFERENCES = {
    "reasoning": [
        r"deepseek.*r1",
        r"qwen.*qwq",
        r"llama.*70b.*reasoning",
        r"o1-mini",
        r"o3-mini",
    ],
    "coding": [
        r"qwen.*coder.*next",
        r"qwen.*coder.*32b",
        r"claude-3-5-sonnet",
        r"gpt-4o.*coder",
        r"gemini.*flash.*coder",
    ],
    "general": [
        r"llama-3\.3-70b-versatile",
        r"gemini-2\.5-pro",
        r"claude-3-5-sonnet",
        r"llama-3-70b",
        r"gpt-4o-mini",
    ],
    "fast": [
        r"gemma2-9b-it",
        r"claude-3-5-haiku",
        r"llama-3-8b-instruct",
        r"gpt-4o-mini",
    ],
}

# Defaults estáticos en caso de fallo de red o falta de claves
STATIC_DEFAULTS = {
    "reasoning": ("groq", "llama-3.3-70b-versatile"),
    "coding": ("openrouter", "qwen/qwen3-coder-next"),
    "general": ("groq", "llama-3.3-70b-versatile"),
    "fast": ("groq", "gemma2-9b-it"),
}


def _get_active_models() -> dict[str, list[str]]:
    """Consulta en paralelo o secuencia los modelos disponibles en las APIs configuradas."""
    models = {"groq": [], "openrouter": []}

    groq = GroqClient()
    if groq.is_configured():
        models["groq"] = groq.get_model_ids()

    openrouter = OpenRouterClient()
    if openrouter.is_configured():
        models["openrouter"] = openrouter.get_model_ids()

    return models


def select_best_model(category: str) -> tuple[str, str]:
    """
    Selecciona dinámicamente el mejor modelo y su proveedor para una categoría dada.
    Retorna: (provider_name, model_id)
    """
    category = category.lower()
    if category not in MODEL_PREFERENCES:
        category = "general"

    preferences = MODEL_PREFERENCES[category]

    try:
        active_models = _get_active_models()

        # Intentar coincidir con las preferencias sobre la API de OpenRouter primero
        for pattern in preferences:
            regex = re.compile(pattern, re.IGNORECASE)
            for m_id in active_models["openrouter"]:
                if regex.search(m_id):
                    return "openrouter", m_id

        # Intentar coincidir con las preferencias sobre la API de Groq
        for pattern in preferences:
            regex = re.compile(pattern, re.IGNORECASE)
            for m_id in active_models["groq"]:
                if regex.search(m_id):
                    return "groq", m_id

    except Exception as e:
        logger.warning(
            "Fallo al descubrir modelos de forma dinámica: %s. Usando defaults estáticos.",
            e,
        )

    # Si no hay match o hay error, usar el fallback estático
    provider, model_id = STATIC_DEFAULTS[category]

    # Verificar si el proveedor del fallback estático está configurado
    if provider == "groq" and not GroqClient().is_configured():
        return "openrouter", "qwen/qwen3-coder-next"
    if provider == "openrouter" and not OpenRouterClient().is_configured():
        return "groq", "llama-3.3-70b-versatile"

    return provider, model_id
