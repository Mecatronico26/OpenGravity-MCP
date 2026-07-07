"""
Enrutador de tareas a perfiles de agentes (Router).
===================================================
Analiza la tarea del usuario para asociar el mejor agente registrado.
Si no hay match, retorna un agente por defecto (Coder o Generalist).
"""

import logging
from opengravity.agents.base_agent import AgentProfile
from opengravity.agents.registry import AgentRegistry

logger = logging.getLogger("opengravity.orchestrator.router")


def route_task(task_description: str, forced_role: str = "") -> AgentProfile:
    """
    Enruta una tarea técnica al agente especializado más óptimo.
    Si se especifica forced_role, se utiliza dicho agente directamente.
    """
    registry = AgentRegistry()

    # Si se fuerza un rol específico, intentar cargarlo
    if forced_role:
        agent = registry.get(forced_role)
        if agent:
            logger.info("Rol forzado por usuario: %s", agent.name)
            return agent
        logger.warning("Rol forzado '%s' no encontrado. Auto-enrutando...", forced_role)

    # Intentar buscar por coincidencia de keywords en la descripción
    agent = registry.find_by_task(task_description)
    if agent:
        logger.info("Agente auto-enrutado por keywords: %s", agent.name)
        return agent

    # Agente por defecto si no hay coincidencia
    # Si contiene palabras típicas de programación, usar Coder, sino usar Arquitecto
    task_lower = task_description.lower()
    if any(k in task_lower for k in ["código", "st", "ladder", "funcion", "script"]):
        default_agent = registry.get("coder")
    else:
        default_agent = registry.get("architect")

    if default_agent:
        logger.info("Agente por defecto seleccionado: %s", default_agent.name)
        return default_agent

    # Fallback extremo (nunca debería ocurrir debido al registro estático)
    return AgentProfile(
        role_id="generalist",
        name="Agente Técnico Generalista",
        system_prompt="Eres un asistente técnico experto en automatización industrial.",
        default_category="general",
    )
