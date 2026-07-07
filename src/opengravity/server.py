"""
OpenGravity MCP Server Entry Point.
===================================
Inicializa la pasarela FastMCP de comunicación bidireccional stdio.
Usa logging de sistema redirigido a stderr para no interferir con el protocolo.
"""

import sys
import logging
from mcp.server.fastmcp import FastMCP
from opengravity.config import get_settings

# Configurar logging redirigiendo logs al stderr (CRÍTICO para stdio MCP)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("opengravity.server")

# 1. Inicialización de la instancia de FastMCP
mcp = FastMCP(
    "OpenGravity",
    instructions=(
        "Pasarela hacia modelos de IA externos via Groq y OpenRouter. "
        "Permite orquestar agentes y debatir soluciones industriales bajo Vibe-Coding."
    ),
)

# 2. Importar todas las herramientas para que se registren en la instancia de mcp anterior
# (Importante: Se debe hacer después de crear la instancia de 'mcp' para evitar importación circular)
import opengravity.tools  # noqa: F401


def main() -> None:
    """Función de inicio del servidor MCP."""
    try:
        logger.info("🚀 Iniciando OpenGravity MCP Server...")
        settings = get_settings()
        settings.print_status(file=sys.stderr)
        logger.info("Servidor MCP escuchando en modo stdio...")

        # Iniciar loop del servidor stdio
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Servidor detenido por solicitud del usuario.")
    except Exception as e:
        logger.critical("Fallo catastrófico al arrancar el servidor: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
