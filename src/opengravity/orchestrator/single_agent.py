"""
Orquestador Single-Agent con Resiliencia y Fallback de APIs.
===========================================================
Ejecuta la tarea en un único agente resolviendo de forma dinámica
su modelo y reintentando con un proveedor alternativo en caso de error.
"""

import logging
from opengravity.agents.base_agent import AgentProfile
from opengravity.orchestrator.model_selector import select_best_model
from opengravity.clients.groq_client import GroqClient
from opengravity.clients.openrouter_client import OpenRouterClient
from opengravity.postprocessing.compliance import enforce_compliance

logger = logging.getLogger("opengravity.orchestrator.single")


def run_single_agent(
    task_description: str,
    agent: AgentProfile,
    forced_category: str = "",
) -> str:
    """
    Ejecuta un agente contra el modelo ideal. Si falla, hace fallback al otro proveedor.
    Aplica post-procesamiento de compatibilidad Structured Text de Rockwell.
    """
    # 1. Resolver categoría y modelo dinámico
    category = forced_category if forced_category else agent.default_category
    provider, model_id = select_best_model(category)

    logger.info("Enrutando tarea a agente: %s", agent.name)
    logger.info("Modelo seleccionado: %s (%s)", model_id, provider.upper())

    # 2. Intentar ejecución
    result_content = ""
    error_occurred = False
    error_msg = ""

    try:
        if provider == "groq":
            client = GroqClient()
        else:
            client = OpenRouterClient()

        response = client.chat(
            prompt=task_description,
            model=model_id,
            system_prompt=agent.system_prompt,
            temperature=0.3,
        )
        result_content = response.content

    except Exception as e:
        error_occurred = True
        error_msg = str(e)
        logger.warning(
            "Fallo al invocar a %s (%s): %s. Iniciando fallback...",
            model_id,
            provider,
            e,
        )

    # 3. Fallback en caso de fallo del proveedor primario
    if error_occurred:
        alt_provider = "openrouter" if provider == "groq" else "groq"
        alt_model = (
            "qwen/qwen3-coder-next"
            if alt_provider == "openrouter"
            else "llama-3.3-70b-versatile"
        )

        try:
            if alt_provider == "groq":
                client = GroqClient()
            else:
                client = OpenRouterClient()

            if client.is_configured():
                logger.info(
                    "Ejecutando fallback en proveedor alternativo: %s con modelo %s",
                    alt_provider.upper(),
                    alt_model,
                )
                response = client.chat(
                    prompt=task_description,
                    model=alt_model,
                    system_prompt=agent.system_prompt,
                    temperature=0.3,
                )
                result_content = response.content
                provider = alt_provider
                model_id = alt_model
            else:
                return (
                    f"❌ Error Crítico: Falló el proveedor primario ({provider}) debido a: {error_msg}. "
                    f"Y el proveedor alternativo ({alt_provider}) no está configurado en el archivo .env."
                )
        except Exception as ex:
            return (
                f"❌ Error Crítico en Orquestador (con fallo de Fallback): {ex}. "
                f"Error original: {error_msg}"
            )

    # 4. Post-procesamiento (Vibe-Coding compliance: verificación general)
    result_content, warnings = enforce_compliance(result_content)
    if warnings:
        result_content += (
            "\n\n---\n**⚠️ Advertencias de calidad (Vibe-Coding):**\n"
        )
        for w in warnings:
            result_content += f"- {w}\n"

    # 5. Formatear reporte final
    report = (
        f"### 🤖 OpenGravity Orchestrator Report\n"
        f"- **Agente Especializado:** {agent.name}\n"
        f"- **Modelo Utilizado:** `{model_id}` ({provider.upper()})\n"
        f"- **Categoría de Tarea:** `{category}`\n\n"
        f"---\n\n"
        f"{result_content}"
    )

    return report
