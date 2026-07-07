"""
Definición de AgentProfile y modelo base.
=========================================
Sigue la metodología de Vibe-Coding Profesional integrando
directrices operativas, limitaciones y comportamiento Failsafe.
"""

import re
from typing import Pattern
from dataclasses import dataclass, field


@dataclass(frozen=True)
class AgentProfile:
    """Perfil descriptivo y operativo de un agente especializado."""

    role_id: str
    name: str
    system_prompt: str
    default_category: str = "general"
    keywords: list[str] = field(default_factory=list)

    def matches(self, task_description: str) -> bool:
        """Determina si la descripción de la tarea coincide con las keywords del agente."""
        task_lower = task_description.lower()
        for keyword in self.keywords:
            if re.search(r"\b" + re.escape(keyword.lower()) + r"\b", task_lower):
                return True
        return False
