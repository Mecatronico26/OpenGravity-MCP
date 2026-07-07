"""
Sistema de Agentes Especializados de OpenGravity.
==================================================
Define la estructura base para los agentes del enjambre
y gestiona el registro dinámico de los mismos.
"""

from opengravity.agents.base_agent import AgentProfile
from opengravity.agents.registry import AgentRegistry

# Instancia global del registro de agentes
registry = AgentRegistry()

# Importar todos los agentes especializados para forzar su registro dinámico
import opengravity.agents.architect
import opengravity.agents.coder
import opengravity.agents.analyst
import opengravity.agents.security
import opengravity.agents.validator

__all__ = ["AgentProfile", "registry"]
