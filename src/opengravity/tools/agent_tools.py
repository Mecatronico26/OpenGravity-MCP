"""Herramientas MCP de administración de agentes."""

import logging
from opengravity.agents.registry import AgentRegistry
from opengravity.orchestrator.single_agent import run_single_agent
from opengravity.server import mcp

logger = logging.getLogger("opengravity.tools.agents")


@mcp.tool()
def opengravity_list_agents() -> str:
    """Retorna una lista en formato markdown de todos los agentes registrados y sus keywords.

    Permite conocer los roles disponibles en el enjambre de OpenGravity y sus áreas de especialidad.
    """
    try:
        registry = AgentRegistry()
        agents = registry.list_all()

        lines = [
            "# 👥 Agentes Registrados en OpenGravity",
            "| ID | Nombre | Categoría Default | Palabras Clave |",
            "|----|--------|-------------------|----------------|",
        ]
        for a in agents:
            kw_str = ", ".join(f"`{k}`" for k in a.keywords)
            lines.append(
                f"| `{a.role_id}` | {a.name} | `{a.default_category}` | {kw_str} |"
            )

        return "\n".join(lines)
    except Exception as e:
        return f"❌ Error al listar agentes: {type(e).__name__}: {e}"


@mcp.tool()
def opengravity_agent_solve(
    role_id: str,
    task_description: str,
    category: str = "",
) -> str:
    """Ejecuta una tarea técnica forzando el uso de un agente especializado específico.

    Args:
        role_id: ID del agente (ej: 'architect', 'coder', 'mathematician', 'security', 'validator').
        task_description: Descripción detallada de la tarea a resolver.
        category: Categoría de modelo forzada (valores: 'reasoning', 'coding', 'general', 'fast').
    """
    try:
        registry = AgentRegistry()
        agent = registry.get(role_id)
        if not agent:
            available = ", ".join(f"'{a.role_id}'" for a in registry.list_all())
            return (
                f"⚠️ Error: El agente con ID '{role_id}' no está registrado. "
                f"Agentes disponibles: {available}"
            )

        return run_single_agent(
            task_description=task_description,
            agent=agent,
            forced_category=category,
        )
    except Exception as e:
        return f"❌ Error al ejecutar el agente '{role_id}': {type(e).__name__}: {e}"
