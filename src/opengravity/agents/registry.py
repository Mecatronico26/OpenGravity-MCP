"""
Registro dinámico de agentes (Singleton).
=========================================
Permite registrar y buscar agentes especializados según el contexto de la tarea.
"""

import logging
from opengravity.agents.base_agent import AgentProfile

logger = logging.getLogger("opengravity.agents.registry")


class AgentRegistry:
    """Registro global e hilo-seguro de perfiles de agentes."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentRegistry, cls).__new__(cls)
            cls._instance._agents = {}
        return cls._instance

    def register(self, profile: AgentProfile) -> None:
        """Registra un nuevo agente especializado."""
        role_id = profile.role_id.lower()
        if role_id in self._agents:
            logger.warning("Agente '%s' ya registrado. Sobrescribiendo...", role_id)
        self._agents[role_id] = profile
        logger.info("Agente '%s' (%s) registrado exitosamente.", role_id, profile.name)

    def get(self, role_id: str) -> AgentProfile | None:
        """Obtiene el perfil del agente por su role_id."""
        return self._agents.get(role_id.lower())

    def list_all(self) -> list[AgentProfile]:
        """Retorna una lista de todos los agentes registrados."""
        return list(self._agents.values())

    def find_by_task(self, task_description: str) -> AgentProfile | None:
        """Encuentra el agente más adecuado analizando la descripción de la tarea."""
        for agent in self._agents.values():
            if agent.matches(task_description):
                return agent
        return None
