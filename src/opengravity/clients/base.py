"""
Clase base abstracta para clientes LLM.
========================================
Define la interfaz que deben cumplir todos los clientes (Groq, OpenRouter, etc.)
para garantizar interoperabilidad y facilitar la extensión con nuevos proveedores.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ChatResponse:
    """Respuesta estandarizada de un chat LLM."""

    content: str
    model: str
    provider: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    def format_report(self) -> str:
        """Formatea la respuesta como reporte legible para MCP."""
        lines = [
            f"**Modelo:** {self.model}",
            f"**Proveedor:** {self.provider}",
        ]
        if self.total_tokens > 0:
            lines.append(
                f"**Tokens:** {self.prompt_tokens} prompt + "
                f"{self.completion_tokens} completion = {self.total_tokens} total"
            )
        lines.append(f"\n---\n\n{self.content}")
        return "\n".join(lines)


class BaseLLMClient(ABC):
    """Interfaz base para clientes de modelos de lenguaje."""

    provider_name: str = "unknown"

    @abstractmethod
    def chat(
        self,
        prompt: str,
        model: str,
        system_prompt: str = "Eres un asistente técnico experto.",
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> ChatResponse:
        """Envía un prompt al modelo y devuelve la respuesta estandarizada."""
        ...

    @abstractmethod
    def list_models(self, search: str = "") -> str:
        """Lista los modelos disponibles, opcionalmente filtrados por texto."""
        ...

    @abstractmethod
    def get_model_ids(self) -> list[str]:
        """Retorna una lista cruda de IDs de modelos disponibles."""
        ...

    @abstractmethod
    def is_configured(self) -> bool:
        """Verifica si el cliente tiene credenciales válidas."""
        ...
