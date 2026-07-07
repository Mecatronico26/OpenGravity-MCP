"""
Módulo de Verificación de Calidad y Cumplimiento General (Vibe-Coding).
======================================================================
Analiza el código generado para detectar malas prácticas comunes como
credenciales hardcodeadas (API Keys) o comentarios de depuración huérfanos.
"""

import re


def enforce_compliance(text: str) -> tuple[str, list[str]]:
    """
    Analiza el texto generado y remueve o advierte sobre malas prácticas de código.
    Retorna: (texto, lista_de_advertencias)
    """
    warnings = []

    # 1. Comprobar patrones de claves de API expuestas
    groq_key_pattern = r"\bgsk_[a-zA-Z0-9]{30,}\b"
    openrouter_key_pattern = r"\bsk-or-v1-[a-zA-Z0-9]{40,}\b"

    if re.search(groq_key_pattern, text):
        warnings.append(
            "⚠️ ATENCIÓN: Se detectó un posible patrón de clave API de Groq hardcodeada en la respuesta."
        )

    if re.search(openrouter_key_pattern, text):
        warnings.append(
            "⚠️ ATENCIÓN: Se detectó un posible patrón de clave API de OpenRouter hardcodeada en la respuesta."
        )

    # 2. Comprobar marcas de desarrollo/depuración olvidadas
    debug_marks = ["TODO", "FIXME", "DEBUG_ME"]
    for mark in debug_marks:
        matches = re.findall(r"\b" + re.escape(mark) + r"\b", text)
        if matches:
            warnings.append(
                f"⚠️ Recordatorio: Se encontraron {len(matches)} comentarios '{mark}' huérfanos en la entrega."
            )

    return text, warnings
