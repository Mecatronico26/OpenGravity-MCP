"""
Cliente Groq — Inferencia ultra-rápida con modelos open-source.
================================================================
Usa el SDK de OpenAI con base_url personalizada (API compatible).

Modelos populares en Groq:
  - llama-3.3-70b-versatile  (Llama 3.3 70B — uso general)
  - qwen-qwq-32b            (Qwen QWQ 32B — razonamiento)
  - gemma2-9b-it             (Gemma 2 9B — ligero y rápido)
  - mistral-saba-24b        (Mistral Saba 24B)
  - meta-llama/llama-4-scout-17b-16e-instruct (Llama 4 Scout)
"""

import logging
from openai import OpenAI

from opengravity.config import get_settings
from opengravity.clients.base import BaseLLMClient, ChatResponse

logger = logging.getLogger("opengravity.clients.groq")


class GroqClient(BaseLLMClient):
    """Cliente para la API de Groq (OpenAI-compatible)."""

    provider_name = "Groq"

    def __init__(self) -> None:
        self._client: OpenAI | None = None

    def _get_client(self) -> OpenAI:
        """Inicialización lazy del cliente. Lanza ValueError si no está configurado."""
        if self._client is not None:
            return self._client

        settings = get_settings()
        if not settings.groq_configured:
            raise ValueError(
                "GROQ_API_KEY no está configurada. "
                "Edita el archivo .env con tu clave de https://console.groq.com"
            )

        self._client = OpenAI(
            api_key=settings.groq_api_key,
            base_url=settings.groq_base_url,
        )
        return self._client

    def is_configured(self) -> bool:
        """Verifica si Groq tiene credenciales válidas."""
        return get_settings().groq_configured

    def chat(
        self,
        prompt: str,
        model: str = "llama-3.3-70b-versatile",
        system_prompt: str = "Eres un asistente técnico experto.",
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> ChatResponse:
        """Envía un prompt a Groq y retorna la respuesta estandarizada."""
        client = self._get_client()

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

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

    def list_models(self, search: str = "") -> str:
        """Lista modelos disponibles en Groq con formato tabla markdown."""
        client = self._get_client()
        models = client.models.list()

        filtered = models.data
        if search:
            search_lower = search.lower()
            filtered = [m for m in filtered if search_lower in m.id.lower()]

        filtered = sorted(filtered, key=lambda x: x.id)

        lines = ["| # | Model ID | Owner |", "|---|----------|-------|"]
        for i, m in enumerate(filtered, 1):
            owner = getattr(m, "owned_by", "—")
            lines.append(f"| {i} | `{m.id}` | {owner} |")

        header = "**Modelos disponibles en Groq"
        if search:
            header += f" (filtro: '{search}')"
        header += f"** — mostrando {len(filtered)} de {len(models.data)} total:\n\n"

        return header + "\n".join(lines)

    def get_model_ids(self) -> list[str]:
        """Retorna lista cruda de IDs de modelos en Groq."""
        try:
            client = self._get_client()
            models = client.models.list()
            return [m.id for m in models.data]
        except Exception as e:
            logger.warning("Error al obtener modelos de Groq: %s", e)
            return []
