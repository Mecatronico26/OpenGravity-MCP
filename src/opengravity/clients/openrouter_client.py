"""
Cliente OpenRouter — Acceso unificado a cientos de modelos de IA.
==================================================================
Usa el SDK de OpenAI con base_url personalizada (API compatible).
Incluye headers HTTP-Referer y X-Title requeridos por OpenRouter.

Modelos populares en OpenRouter:
  - qwen/qwen3-coder-next           (Qwen 3 Coder — programación)
  - qwen/qwen3.5-27b                (Qwen 3.5 27B — uso general)
  - meta-llama/llama-4-maverick     (Llama 4 Maverick)
  - anthropic/claude-sonnet-4       (Claude Sonnet 4)
  - google/gemini-2.5-pro           (Gemini 2.5 Pro)
  - deepseek/deepseek-r1            (DeepSeek R1 — razonamiento)
"""

import logging
from openai import OpenAI

from opengravity.config import get_settings
from opengravity.clients.base import BaseLLMClient, ChatResponse

logger = logging.getLogger("opengravity.clients.openrouter")


class OpenRouterClient(BaseLLMClient):
    """Cliente para la API de OpenRouter (OpenAI-compatible)."""

    provider_name = "OpenRouter"

    def __init__(self) -> None:
        self._client: OpenAI | None = None

    def _get_client(self) -> OpenAI:
        """Inicialización lazy del cliente. Lanza ValueError si no está configurado."""
        if self._client is not None:
            return self._client

        settings = get_settings()
        if not settings.openrouter_configured:
            raise ValueError(
                "OPENROUTER_API_KEY no está configurada. "
                "Edita el archivo .env con tu clave de https://openrouter.ai/keys"
            )

        self._client = OpenAI(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
        )
        return self._client

    def is_configured(self) -> bool:
        """Verifica si OpenRouter tiene credenciales válidas."""
        return get_settings().openrouter_configured

    def chat(
        self,
        prompt: str,
        model: str = "qwen/qwen3-coder-next",
        system_prompt: str = "Eres un asistente técnico experto.",
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> ChatResponse:
        """Envía un prompt a OpenRouter y retorna la respuesta estandarizada."""
        client = self._get_client()

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                extra_headers={
                    "HTTP-Referer": "https://opengravity.local",
                    "X-Title": "OpenGravity MCP",
                },
            )
        except Exception as e:
            # Capturar error de créditos en OpenRouter (Error 402) e intentar recuperar
            # reduciendo dinámicamente los max_tokens
            if hasattr(e, "status_code") and e.status_code == 402:
                logger.warning(
                    "Créditos insuficientes en OpenRouter para max_tokens=%d. Reintentando con max_tokens=1536...",
                    max_tokens,
                )
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": prompt},
                        ],
                        temperature=temperature,
                        max_tokens=1536,  # Reducción de tokens para ajustarse al presupuesto
                        extra_headers={
                            "HTTP-Referer": "https://opengravity.local",
                            "X-Title": "OpenGravity MCP (Fallback de Presupuesto)",
                        },
                    )
                except Exception as ex:
                    # Si falla de nuevo, lanzar excepción clara para el orquestador
                    raise ValueError(
                        f"Créditos insuficientes en OpenRouter: {ex}"
                    ) from ex
            else:
                raise e

        content = response.choices[0].message.content or ""
        model_used = response.model or model
        usage = response.usage


        return ChatResponse(
            content=content,
            model=model_used,
            provider=self.provider_name,
            prompt_tokens=usage.prompt_tokens if usage else 0,
            completion_tokens=usage.completion_tokens if usage else 0,
            total_tokens=usage.total_tokens if usage else 0,
        )

    def list_models(self, search: str = "", limit: int = 30) -> str:
        """Lista modelos disponibles en OpenRouter con formato tabla markdown."""
        client = self._get_client()
        models = client.models.list()

        filtered = models.data
        if search:
            search_lower = search.lower()
            filtered = [m for m in filtered if search_lower in m.id.lower()]

        filtered = sorted(filtered, key=lambda x: x.id)[:limit]

        lines = ["| # | Model ID | Context |", "|---|----------|---------|"]
        for i, m in enumerate(filtered, 1):
            ctx = getattr(m, "context_length", "—")
            if ctx == "—":
                raw = m.model_dump() if hasattr(m, "model_dump") else {}
                ctx = raw.get("context_length", "—")
            lines.append(f"| {i} | `{m.id}` | {ctx} |")

        header = "**Modelos en OpenRouter"
        if search:
            header += f" (filtro: '{search}')"
        header += f"** — mostrando {len(filtered)} de {len(models.data)} total:\n\n"

        return header + "\n".join(lines)

    def get_model_ids(self) -> list[str]:
        """Retorna lista cruda de IDs de modelos en OpenRouter."""
        try:
            client = self._get_client()
            models = client.models.list()
            return [m.id for m in models.data]
        except Exception as e:
            logger.warning("Error al obtener modelos de OpenRouter: %s", e)
            return []
