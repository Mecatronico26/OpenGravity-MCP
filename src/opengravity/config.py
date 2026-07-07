"""
Configuración centralizada de OpenGravity.
==========================================
Carga las variables de entorno, valida claves de API y expone
constantes globales utilizadas en todo el paquete.
"""

import os
import sys
import logging
from pathlib import Path
from dataclasses import dataclass, field
from dotenv import load_dotenv

logger = logging.getLogger("opengravity.config")

# ---------------------------------------------------------------------------
# Constantes de las APIs
# ---------------------------------------------------------------------------
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 4096
TECHNICAL_TEMPERATURE = 0.3
REFACTOR_TEMPERATURE = 0.1


# ---------------------------------------------------------------------------
# Dataclass de configuración
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Settings:
    """Configuración inmutable del servidor."""

    groq_api_key: str = ""
    openrouter_api_key: str = ""
    groq_base_url: str = GROQ_BASE_URL
    openrouter_base_url: str = OPENROUTER_BASE_URL
    default_temperature: float = DEFAULT_TEMPERATURE
    default_max_tokens: int = DEFAULT_MAX_TOKENS

    @property
    def groq_configured(self) -> bool:
        """Verifica si la clave de Groq es válida (no vacía ni placeholder)."""
        return bool(self.groq_api_key) and not self.groq_api_key.startswith("gsk_XXXX")

    @property
    def openrouter_configured(self) -> bool:
        """Verifica si la clave de OpenRouter es válida (no vacía ni placeholder)."""
        return bool(self.openrouter_api_key) and not self.openrouter_api_key.startswith(
            "sk-or-v1-XXXX"
        )

    def print_status(self, file=sys.stderr) -> None:
        """Imprime el estado de configuración al stderr."""
        print(
            f"   Groq API Key: {'✅ configurada' if self.groq_configured else '❌ NO configurada'}",
            file=file,
        )
        print(
            f"   OpenRouter API Key: {'✅ configurada' if self.openrouter_configured else '❌ NO configurada'}",
            file=file,
        )


# ---------------------------------------------------------------------------
# Carga de configuración
# ---------------------------------------------------------------------------
_settings: Settings | None = None


def _find_env_file() -> Path | None:
    """Busca el archivo .env en varias ubicaciones posibles."""
    candidates = [
        Path(__file__).resolve().parent.parent.parent / ".env",  # raíz del repo
        Path.cwd() / ".env",  # directorio actual
    ]
    for path in candidates:
        if path.exists():
            logger.debug("Archivo .env encontrado en: %s", path)
            return path
    return None


def get_settings(force_reload: bool = False) -> Settings:
    """
    Carga y retorna la configuración del servidor.

    La configuración se cachea después de la primera carga.
    Usa force_reload=True para recargar desde disco.
    """
    global _settings
    if _settings is not None and not force_reload:
        return _settings

    env_path = _find_env_file()
    if env_path:
        load_dotenv(dotenv_path=env_path, override=True)
        logger.info("Variables de entorno cargadas desde: %s", env_path)
    else:
        logger.warning(
            "No se encontró archivo .env. "
            "Las claves deben estar definidas como variables de entorno del sistema."
        )

    _settings = Settings(
        groq_api_key=os.getenv("GROQ_API_KEY", ""),
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY", ""),
    )

    return _settings
