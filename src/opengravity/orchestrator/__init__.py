"""
Motor de Orquestación y Enjambre Multi-Agente de OpenGravity.
=============================================================
Coordina la selección de modelos, enrutamiento de tareas y debate interactivo.
"""

from opengravity.orchestrator.model_selector import select_best_model
from opengravity.orchestrator.task_router import route_task
from opengravity.orchestrator.single_agent import run_single_agent
from opengravity.orchestrator.team_solver import run_team_solve

__all__ = ["select_best_model", "route_task", "run_single_agent", "run_team_solve"]
