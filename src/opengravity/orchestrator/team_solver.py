"""
Orquestador Enjambre Multi-Agente — Debate Técnico e Integración de Vibe-Coding.
================================================================================
Simula un debate iterativo de ingeniería de software:
Líder (DeepSeek R1) -> Analista de Algoritmos (DeepSeek R1) -> Programador (Qwen Coder) ->
Razonador de Seguridad (DeepSeek R1) -> Programador (Refactor) -> Reporte Consolidado.
"""

import logging
from opengravity.agents.registry import AgentRegistry
from opengravity.clients.openrouter_client import OpenRouterClient
from opengravity.clients.groq_client import GroqClient
from opengravity.postprocessing.compliance import enforce_compliance

logger = logging.getLogger("opengravity.orchestrator.team")


def _safe_swarm_chat(
    or_client: OpenRouterClient,
    groq_client: GroqClient,
    prompt: str,
    system_prompt: str,
    preferred_model_or: str,
    preferred_model_groq: str,
    temperature: float = 0.3,
) -> str:
    """
    Realiza una llamada segura utilizando OpenRouter primero.
    Si OpenRouter falla o no está configurado, hace fallback a Groq de forma transparente.
    """
    if or_client.is_configured():
        try:
            logger.info("Llamando a OpenRouter con modelo: %s", preferred_model_or)
            res = or_client.chat(
                prompt=prompt,
                model=preferred_model_or,
                system_prompt=system_prompt,
                temperature=temperature,
            )
            return res.content
        except Exception as e:
            logger.warning(
                "Llamada al enjambre con OpenRouter (%s) falló: %s. Usando fallback Groq (%s)...",
                preferred_model_or,
                e,
                preferred_model_groq,
            )

    # Fallback a Groq
    if groq_client.is_configured():
        logger.info("Llamando a Groq (fallback) con modelo: %s", preferred_model_groq)
        res = groq_client.chat(
            prompt=prompt,
            model=preferred_model_groq,
            system_prompt=system_prompt,
            temperature=temperature,
        )
        return res.content

    raise RuntimeError(
        "Ningún proveedor (OpenRouter o Groq) está disponible o configurado correctamente."
    )


def run_team_solve(task_description: str) -> str:
    """
    Ejecuta el enjambre de agentes interactivo.
    Se utiliza OpenRouter como base preferente, y Groq como fallback dinámico transparente.
    """
    registry = AgentRegistry()
    or_client = OpenRouterClient()
    groq_client = GroqClient()

    # 1. Definir los agentes que participan
    leader = registry.get("architect")
    analyst = registry.get("analyst")
    coder = registry.get("coder")
    security = registry.get("security")

    # Definición de system prompts locales de resguardo
    leader_prompt_sys = leader.system_prompt if leader else "Eres el Líder Arquitecto."
    analyst_prompt_sys = (
        analyst.system_prompt if analyst else "Eres el Analista Técnico."
    )
    coder_prompt_sys = coder.system_prompt if coder else "Eres el Desarrollador Software."
    security_prompt_sys = (
        security.system_prompt if security else "Eres el Analista de Robustez y Seguridad."
    )

    logger.info("Iniciando enjambre de ingeniería de software...")

    # --- PASO 1: LÍDER PLANIFICA (Vibe-Coding Rule: Blueprint Primero) ---
    logger.info("[ENJAMBRE] -> Paso 1: Líder diseña directivas...")
    leader_prompt = (
        f"Objetivo de Desarrollo Requerido:\n{task_description}\n\n"
        "Establece las directivas iniciales del proyecto, la jerarquía de módulos "
        "y los requerimientos técnicos que el Analista y el Programador deben resolver."
    )
    directives = _safe_swarm_chat(
        or_client=or_client,
        groq_client=groq_client,
        prompt=leader_prompt,
        system_prompt=leader_prompt_sys,
        preferred_model_or="deepseek/deepseek-r1",
        preferred_model_groq="llama-3.3-70b-versatile",
        temperature=0.4,
    )

    # --- PASO 2: ANALISTA PREVIENE CAUSA RAÍZ ---
    logger.info("[ENJAMBRE] -> Paso 2: Analista diseña lógica y algoritmos...")
    analyst_prompt = (
        f"Basado en las directivas del Líder:\n{directives}\n\n"
        "Analiza y define:\n"
        "1. Estructuras de datos óptimas y algoritmos clave.\n"
        "2. Manejo de tipos de datos, validación lógica de variables y aserciones.\n"
        "3. Protecciones contra desbordamientos, variables nulas o divisiones por cero."
    )
    analyst_analysis = _safe_swarm_chat(
        or_client=or_client,
        groq_client=groq_client,
        prompt=analyst_prompt,
        system_prompt=analyst_prompt_sys,
        preferred_model_or="deepseek/deepseek-r1",
        preferred_model_groq="llama-3.3-70b-versatile",
        temperature=0.3,
    )

    # --- PASO 3: PROGRAMADOR CODIFICA ---
    logger.info("[ENJAMBRE] -> Paso 3: Programador genera el código base...")
    coder_prompt = (
        f"Directivas del Líder:\n{directives}\n\n"
        f"Análisis Algorítmico y Lógico:\n{analyst_analysis}\n\n"
        "Escribe el código completo estructurado necesario para resolver la tarea. "
        "Aplica buenas prácticas y encapsulamiento limpio."
    )
    code_output = _safe_swarm_chat(
        or_client=or_client,
        groq_client=groq_client,
        prompt=coder_prompt,
        system_prompt=coder_prompt_sys,
        preferred_model_or="qwen/qwen3-coder-next",
        preferred_model_groq="llama-3.3-70b-versatile",
        temperature=0.2,
    )

    # --- PASO 4: RAZONADOR DE SEGURIDAD AUDITA CAUSA RAÍZ ---
    logger.info("[ENJAMBRE] -> Paso 4: Seguridad audita riesgos y robustez...")
    security_prompt = (
        f"Código generado:\n{code_output}\n\n"
        f"Ecuaciones y Estructuras:\n{analyst_analysis}\n\n"
        "Busca fallas lógicas ocultas, inyecciones, fugas de memoria, o comportamiento inseguro "
        "ante fallos de recursos. Diseña excepciones controladas y flujos de recuperación segura."
    )
    security_audit = _safe_swarm_chat(
        or_client=or_client,
        groq_client=groq_client,
        prompt=security_prompt,
        system_prompt=security_prompt_sys,
        preferred_model_or="deepseek/deepseek-r1",
        preferred_model_groq="llama-3.3-70b-versatile",
        temperature=0.3,
    )

    # --- PASO 5: PROGRAMADOR CORRIGE Y REFACTORIZA ---
    logger.info(
        "[ENJAMBRE] -> Paso 5: Programador refactoriza código según auditoría de seguridad..."
    )
    refactor_prompt = (
        f"Código Base:\n{code_output}\n\n"
        f"Auditoría de Seguridad Lógica y Robustez:\n{security_audit}\n\n"
        "Refactoriza el código original integrando de raíz todos los manejos de excepciones, "
        "timeouts, validaciones y flujos seguros recomendados por el analista de seguridad."
    )
    final_code = _safe_swarm_chat(
        or_client=or_client,
        groq_client=groq_client,
        prompt=refactor_prompt,
        system_prompt=coder_prompt_sys,
        preferred_model_or="qwen/qwen3-coder-next",
        preferred_model_groq="llama-3.3-70b-versatile",
        temperature=0.1,
    )

    # --- PASO 6: LÍDER SINTETIZA EL CONSENSO FINAL ---
    logger.info("[ENJAMBRE] -> Paso 6: Líder consolida reporte...")
    synthesis_prompt = (
        "Hemos concluido el ciclo de debate del enjambre:\n"
        f"1. Directivas de Arquitectura: {directives[:500]}...\n"
        f"2. Análisis Algorítmico: {analyst_analysis[:500]}...\n"
        f"3. Auditoría de Seguridad: {security_audit[:500]}...\n"
        f"4. Código Final Refactorizado:\n{final_code}\n\n"
        "Genera un reporte técnico de ingeniería consolidado. Explica las decisiones de diseño, "
        "las optimizaciones de robustez añadidas y presenta el código de software final listo para producción."
    )
    final_report = _safe_swarm_chat(
        or_client=or_client,
        groq_client=groq_client,
        prompt=synthesis_prompt,
        system_prompt=leader_prompt_sys,
        preferred_model_or="deepseek/deepseek-r1",
        preferred_model_groq="llama-3.3-70b-versatile",
        temperature=0.3,
    )

    # Aplicar post-procesamiento de cumplimiento general al reporte consolidado final
    final_report, warnings = enforce_compliance(final_report)
    if warnings:
        final_report += (
            "\n\n---\n**⚠️ Advertencias de calidad aplicadas al código final:**\n"
        )
        for w in warnings:
            final_report += f"- {w}\n"

    return final_report
