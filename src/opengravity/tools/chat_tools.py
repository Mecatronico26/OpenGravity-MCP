"""Herramientas MCP de Chat Directo con APIs."""

import logging
from opengravity.clients.groq_client import GroqClient
from opengravity.clients.openrouter_client import OpenRouterClient

# Obtenemos la instancia global de FastMCP a través del registrador lazy
from opengravity.server import mcp

logger = logging.getLogger("opengravity.tools.chat")


@mcp.tool()
def groq_chat(
    prompt: str,
    model: str = "llama-3.3-70b-versatile",
    system_prompt: str = "Eres un asistente técnico experto.",
    temperature: float = 0.7,
    max_tokens: int = 4096,
) -> str:
    """Envía un prompt a un modelo alojado en Groq y devuelve la respuesta.

    Groq ofrece inferencia ultra-rápida con modelos open-source.

    Modelos populares en Groq:
      - llama-3.3-70b-versatile  (Llama 3.3 70B — uso general)
      - qwen-qwq-32b            (Qwen QWQ 32B — razonamiento)
      - gemma2-9b-it             (Gemma 2 9B — ligero y rápido)
      - mistral-saba-24b        (Mistral Saba 24B)

    Args:
        prompt: El mensaje o pregunta para el modelo.
        model: ID del modelo en Groq (default: llama-3.3-70b-versatile).
        system_prompt: Instrucción de sistema para el modelo.
        temperature: Creatividad de la respuesta (0.0 = determinista, 1.0 = creativo).
        max_tokens: Máximo de tokens en la respuesta.
    """
    try:
        client = GroqClient()
        response = client.chat(
            prompt=prompt,
            model=model,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.format_report()
    except Exception as e:
        return f"❌ Error al llamar a Groq: {type(e).__name__}: {e}"


@mcp.tool()
def openrouter_chat(
    prompt: str,
    model: str = "qwen/qwen3-coder-next",
    system_prompt: str = "Eres un asistente técnico experto.",
    temperature: float = 0.7,
    max_tokens: int = 4096,
) -> str:
    """Envía un prompt a un modelo alojado en OpenRouter y devuelve la respuesta.

    OpenRouter es un agregador de modelos de IA con acceso a cientos de modelos.

    Modelos populares en OpenRouter:
      - qwen/qwen3-coder-next           (Qwen 3 Coder — programación)
      - qwen/qwen3.5-27b                (Qwen 3.5 27B — uso general)
      - meta-llama/llama-4-maverick     (Llama 4 Maverick)
      - anthropic/claude-sonnet-4       (Claude Sonnet 4)
      - deepseek/deepseek-r1            (DeepSeek R1 — razonamiento)

    Args:
        prompt: El mensaje o pregunta para el modelo.
        model: ID del modelo en OpenRouter (default: qwen/qwen3-coder-next).
        system_prompt: Instrucción de sistema para el modelo.
        temperature: Creatividad de la respuesta (0.0 = determinista, 1.0 = creativo).
        max_tokens: Máximo de tokens en la respuesta.
    """
    try:
        client = OpenRouterClient()
        response = client.chat(
            prompt=prompt,
            model=model,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.format_report()
    except Exception as e:
        return f"❌ Error al llamar a OpenRouter: {type(e).__name__}: {e}"
