"""Herramientas MCP del Orquestador de OpenGravity."""

import logging
from opengravity.orchestrator.task_router import route_task
from opengravity.orchestrator.single_agent import run_single_agent
from opengravity.orchestrator.team_solver import run_team_solve
from opengravity.server import mcp

logger = logging.getLogger("opengravity.tools.orchestrator")


@mcp.tool()
def opengravity_orchestrate(
    task_description: str,
    role: str = "",
    category: str = "",
) -> str:
    """Delega una tarea técnica de automatización al motor de orquestación de OpenGravity.

    El orquestador seleccionará dinámicamente el mejor modelo disponible en Groq u OpenRouter
    según el tipo de tarea y el rol del agente (Architect, Coder, Mathematician, Security, Validator).

    Args:
        task_description: La descripción de la tarea a resolver.
        role: Rol del agente especializado (valores: 'architect', 'coder', 'mathematician', 'security', 'validator').
              Si está vacío, el orquestador auto-enruta según palabras clave de la tarea.
        category: Categoría de modelo forzada (valores: 'reasoning', 'coding', 'general', 'fast').
                  Si está vacío, se determina automáticamente según el rol del agente.
    """
    try:
        agent = route_task(task_description, forced_role=role)
        return run_single_agent(
            task_description=task_description,
            agent=agent,
            forced_category=category,
        )
    except Exception as e:
        return f"❌ Error en la herramienta de orquestación: {type(e).__name__}: {e}"


@mcp.tool()
def opengravity_team_solve(
    task_description: str,
) -> str:
    """Ejecuta un enjambre de agentes orquestados interactivo (Debate de ingeniería multi-agente).

    El Líder (DeepSeek R1) diseñará las directivas de arquitectura, el Matemático validará
    escalas y ecuaciones, el Programador (Qwen Coder) escribirá el código base, el Razonador
    de Seguridad auditará fallas lógicas de raíz y watchdogs, el Programador refactorizará
    el código final, y el Líder consolidará la solución técnica completa.

    Este enjambre opera bajo las reglas de Vibe-Coding Profesional (diseño previo, análisis
    de causa raíz, y autocorrección de compatibilidad Rockwell).

    Args:
        task_description: La descripción detallada de la tarea a resolver.
    """
    try:
        return run_team_solve(task_description)
    except Exception as e:
        return f"❌ Error en la orquestación del enjambre: {type(e).__name__}: {e}"
