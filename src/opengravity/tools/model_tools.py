"""Herramientas MCP de listado de modelos disponibles."""

import logging
from opengravity.clients.groq_client import GroqClient
from opengravity.clients.openrouter_client import OpenRouterClient
from opengravity.server import mcp

logger = logging.getLogger("opengravity.tools.models")


@mcp.tool()
def groq_list_models(search: str = "") -> str:
    """Lista todos los modelos disponibles actualmente en la API de Groq, con opción de filtrar.

    Args:
        search: Texto para filtrar modelos por nombre (ej: "qwen", "llama").
                Si está vacío, muestra todos los modelos.
    """
    try:
        client = GroqClient()
        return client.list_models(search=search)
    except Exception as e:
        return f"❌ Error al listar modelos de Groq: {type(e).__name__}: {e}"


@mcp.tool()
def openrouter_list_models(search: str = "", limit: int = 30) -> str:
    """Lista los modelos disponibles en OpenRouter, con opción de filtrar.

    Args:
        search: Texto para filtrar modelos por nombre (ej: "qwen", "llama").
                Si está vacío, muestra los primeros modelos disponibles.
        limit: Máximo de modelos a mostrar (default: 30).
    """
    try:
        client = OpenRouterClient()
        return client.list_models(search=search, limit=limit)
    except Exception as e:
        return f"❌ Error al listar modelos de OpenRouter: {type(e).__name__}: {e}"
