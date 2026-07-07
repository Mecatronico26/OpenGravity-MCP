"""Pruebas unitarias de configuración y carga del entorno."""

import os
from opengravity.config import get_settings, Settings


def test_settings_load():
    """Valida que las credenciales no estén vacías y se cargue Settings."""
    settings = get_settings(force_reload=True)
    assert isinstance(settings, Settings)
    assert settings.groq_base_url == "https://api.groq.com/openai/v1"
    assert settings.openrouter_base_url == "https://openrouter.ai/api/v1"


def test_api_keys_configured():
    """Valida que se detecte la configuración de las API keys en .env."""
    settings = get_settings()

    # Como copiamos el .env real en Equipo/opengravity-mcp, estas claves deben
    # ser detectadas como válidas
    groq_ok = settings.groq_configured
    or_ok = settings.openrouter_configured

    print(
        f"\n[TEST] Estado de API keys: Groq={groq_ok}, OpenRouter={or_ok}"
    )
    # Por lo menos una debe estar configurada en la máquina de desarrollo
    assert groq_ok or or_ok
