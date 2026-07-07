# 🌊 Vibe-Coding Profesional: Manifiesto de Desarrollo
======================================================
Este documento define las directrices y estándares del **Vibe-Coding Profesional** que rigen el desarrollo en este repositorio.

Los agentes de Inteligencia Artificial y los desarrolladores humanos deben adherirse estrictamente a estas reglas para asegurar un desarrollo rápido, robusto y libre de fallas técnicas críticas en entornos de producción.

---

## 📋 1. Blueprint Antes que Código (Planificar Primero)
*   **Prohibición de Generación Directa:** Ningún agente de código (Coder, etc.) debe escribir líneas de código o modificar archivos sin un diseño previo.
*   **Definición de Requisitos y Estructura:** Se debe realizar un análisis completo de las variables, tipos de datos, interlocks de seguridad y dependencias lógicas antes del primer commit.
*   **Aprobación del Plan:** El Líder del Enjambre o el desarrollador principal debe revisar y validar el plan técnico.

## 🔍 2. Resolución de Causa Raíz (Address Root Cause)
*   **Prohibición de Parches Temporales:** No se permiten soluciones cosméticas o "workarounds" para silenciar errores del compilador o advertencias del sistema.
*   **Hardening y Robustez:** Ante cualquier bug o falla:
    1.  Rastrear el origen exacto de la colisión de variables, la división por cero o el desbordamiento.
    2.  Proponer una refactorización estructural.
    3.  Asegurar que el problema no pueda repetirse bajo condiciones de borde anómalas.
*   **Control de Fallos de Red/I/O:** Todo código que consuma APIs de red o recursos del sistema debe manejar la pérdida de comunicaciones mediante lógica de *Watchdog*, timeouts o fallbacks a estados seguros (Failsafe).

## 🛡️ 3. Disciplina del Stack Tecnológico (Stack Discipline)
*   **Sin Dependencias Fantasma:** Está estrictamente prohibido introducir nuevas dependencias o librerías sin el consentimiento explícito y la justificación técnica en el plan.
*   **Estandarización de Estilo:**
    *   Mantener el código limpio, modularizado y portable.
    *   Cumplimiento estricto de las guías de estilo oficiales del lenguaje (PEP8, ESLint, etc.).

## ✍️ 4. Auto-Documentación y Legibilidad
*   **Regla de los 3 Meses:** Todo código generado debe documentarse de tal forma que cualquier desarrollador que abra el archivo en tres meses pueda comprender el flujo lógico de inmediato.
*   **Comentarios Estructurados:** Explicar el *por qué* detrás de la lógica y no el *cómo* (el código ya muestra el cómo).

## 🧪 5. Validación en 3 Pasos (Three-Step Verification)
Antes de marcar una tarea como completada, se debe ejecutar el siguiente pipeline de validación:
1.  **Validación de Sintaxis e Integridad:** Compilación o ejecución de linters de forma limpia.
2.  **Validación Lógica y de Seguridad:** Análisis de casos extremos (división por cero, desbordamiento, tipos nulos).
3.  **Registro de Pruebas:** Proporcionar un plan de pruebas detallado con 3 escenarios de prueba (Escenario Normal, Escenario Crítico, Escenario de Fallo).

---

## 🚫 Reglas de Contención (Boundaries)
*   **Regla de los 3 Intentos:** Si un agente de código no logra resolver un bug en 3 iteraciones consecutivas, debe **detenerse de inmediato**, revertir los cambios locales, estructurar una lista de supuestos vs. hechos conocidos y solicitar intervención humana.
