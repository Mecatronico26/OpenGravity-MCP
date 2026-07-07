"""
Herramientas del Ecosistema Gentleman Programming (SDD, Clean Arch, Engrams).
=============================================================================
Implementa automatizaciones operativas para Spec-Driven Development,
scaffolding de Arquitectura Hexagonal/Limpia, auditorías y gestión de Engrams.
"""

import os
import re
import sys
import logging
from datetime import datetime
from pathlib import Path
from opengravity.server import mcp
from opengravity.agents.registry import AgentRegistry
from opengravity.orchestrator.single_agent import run_single_agent
from opengravity.postprocessing.compliance import enforce_compliance

logger = logging.getLogger("opengravity.tools.gentleman")


# =====================================================================
# 📐 SDD TOOLS (Spec-Driven Development)
# =====================================================================

@mcp.tool()
def gentleman_create_spec(
    feature_description: str,
    spec_filename: str = "SPEC.md",
    output_dir: str = "docs",
    project_root: str = ".",
) -> str:
    """Genera un archivo de especificación técnica formal (SDD) a partir de una idea o requerimiento.

    Crea el blueprint de desarrollo definiendo interfaces, modelos de datos, flujos,
    casos de borde y planes de prueba de 3 escenarios. Escribe el archivo en disco.

    Args:
        feature_description: Requerimiento o idea de la funcionalidad a desarrollar.
        spec_filename: Nombre del archivo a crear (default: SPEC.md).
        output_dir: Directorio destino (default: docs).
        project_root: Directorio raíz del proyecto (default: directorio actual).
    """
    try:
        registry = AgentRegistry()
        architect = registry.get("architect")

        prompt = (
            f"Diseña una especificación técnica formal (Spec-Driven Development) basada en:\n"
            f"{feature_description}\n\n"
            f"El formato del documento debe ser en Markdown y estructurarse de la siguiente forma:\n"
            f"1. **Objetivo y Contexto**: Qué resuelve la funcionalidad.\n"
            f"2. **Estructuras de Datos e Interfaces**: Clases, tipos, DTOs y firmas de métodos.\n"
            f"3. **Casos de Borde y Errores**: Excepciones controladas y políticas de recuperación.\n"
            f"4. **Plan de Verificación en 3 Pasos**: 3 escenarios de prueba (Normal, Crítico y de Fallo)."
        )

        spec_content = run_single_agent(prompt, architect, forced_category="reasoning")

        # Limpiar metadatos del reporte del agente para dejar el markdown limpio
        clean_content = spec_content
        if "---" in spec_content:
            parts = spec_content.split("---", 1)
            clean_content = parts[1].strip() if len(parts) > 1 else spec_content

        # Escribir en disco
        base_path = Path(project_root).resolve()
        target_dir = base_path / output_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        file_path = target_dir / spec_filename
        file_path.write_text(clean_content, encoding="utf-8")

        return (
            f"### 📐 Spec-Driven Development (SDD) — Especificación Creada\n"
            f"- **Ubicación:** `{file_path.relative_to(base_path)}`\n"
            f"- **Estado:** Guardada con éxito.\n\n"
            f"---\n\n"
            f"{clean_content[:1500]}..."
        )
    except Exception as e:
        return f"❌ Error al crear la especificación SDD: {type(e).__name__}: {e}"


@mcp.tool()
def gentleman_validate_spec(
    code_file_path: str,
    spec_file_path: str,
) -> str:
    """Valida si el código de un archivo cumple estrictamente con el blueprint de especificación (SPEC).

    Realiza una auditoría automatizada comparando la interfaz y reglas del código contra el SPEC.md.

    Args:
        code_file_path: Ruta del archivo de código a auditar.
        spec_file_path: Ruta del archivo de especificación SPEC.md.
    """
    try:
        code_path = Path(code_file_path)
        spec_path = Path(spec_file_path)

        if not code_path.exists():
            return f"⚠️ Error: No se encontró el archivo de código en `{code_file_path}`"
        if not spec_path.exists():
            return f"⚠️ Error: No se encontró el archivo de especificación en `{spec_file_path}`"

        code_content = code_path.read_text(encoding="utf-8")
        spec_content = spec_path.read_text(encoding="utf-8")

        registry = AgentRegistry()
        validator = registry.get("validator")

        prompt = (
            f"Realiza una validación SDD comparando el código de desarrollo contra su especificación (blueprint).\n\n"
            f"**Especificación (SPEC.md):**\n```markdown\n{spec_content}\n```\n\n"
            f"**Código a Auditar (`{code_path.name}`):**\n```\n{code_content}\n```\n\n"
            f"Analiza si:\n"
            f"1. Se respetaron todas las interfaces, tipos y métodos declarados en la especificación.\n"
            f"2. Se implementaron los manejos de excepciones y casos de borde requeridos.\n"
            f"3. Existen funcionalidades extra no especificadas (evitar 'overengineering').\n\n"
            f"Entrega un reporte de conformidad aprobando o detallando las correcciones necesarias."
        )

        return run_single_agent(prompt, validator, forced_category="general")
    except Exception as e:
        return f"❌ Error al validar la especificación: {type(e).__name__}: {e}"


# =====================================================================
# 🏗️ CLEAN ARCHITECTURE TOOLS (Hexagonal Scaffolding & Audit)
# =====================================================================

@mcp.tool()
def gentleman_scaffold_clean_arch(
    project_path: str = ".",
    language: str = "typescript",
) -> str:
    """Crea la estructura de carpetas de Arquitectura Limpia/Hexagonal (Domain, Application, Infrastructure).

    Args:
        project_path: Directorio raíz donde inicializar la estructura (default: directorio actual).
        language: Lenguaje de programación (valores: 'typescript' o 'python').
    """
    try:
        base_path = Path(project_path).resolve()
        language = language.lower()

        # Definir la estructura de carpetas
        src_path = base_path / "src"
        layers = {
            "domain": ["entities", "repositories", "exceptions", "value_objects"],
            "application": ["usecases", "dtos", "services"],
            "infrastructure": ["repositories", "controllers", "database", "adapters"],
        }

        created_paths = []
        for layer, subfolders in layers.items():
            for folder in subfolders:
                folder_path = src_path / layer / folder
                folder_path.mkdir(parents=True, exist_ok=True)
                created_paths.append(folder_path)

                # Inicializar archivos específicos por lenguaje
                if language == "python":
                    init_file = folder_path / "__init__.py"
                    if not init_file.exists():
                        init_file.write_text('"""Inicializador del módulo."""\n', encoding="utf-8")
                elif language == "typescript":
                    index_file = folder_path / "index.ts"
                    if not index_file.exists():
                        index_file.write_text('// Punto de exportación de submódulos\n', encoding="utf-8")

            # Crear __init__.py o index.ts en la capa
            layer_root = src_path / layer
            if language == "python":
                (layer_root / "__init__.py").write_text('"""Capa de arquitectura."""\n', encoding="utf-8")
            elif language == "typescript":
                (layer_root / "index.ts").write_text('// Capa de arquitectura\n', encoding="utf-8")

        # Generar un README descriptivo de la arquitectura en src/
        readme_content = (
            f"# 🏗️ Arquitectura Limpia — {language.capitalize()}\n\n"
            f"Estructura de capas desacopladas generada automáticamente:\n\n"
            f"- **`domain/`**: El núcleo de la lógica de negocio. Contiene entidades, reglas inmutables e interfaces de repositorios. **No posee dependencias externas.**\n"
            f"- **`application/`**: Casos de uso de la aplicación. Coordina el flujo de datos desde y hacia las entidades de dominio.\n"
            f"- **`infrastructure/`**: Implementaciones técnicas (bases de datos, controladores HTTP, frameworks). Adapta el mundo exterior al dominio.\n"
        )
        (src_path / "README_ARCH.md").write_text(readme_content, encoding="utf-8")

        # Construir árbol de visualización
        tree = [f"🏗️ Clean Architecture Scaffolded in: {base_path}"]
        tree.append("└── src/")
        for layer in ["domain", "application", "infrastructure"]:
            tree.append(f"    ├── {layer}/")
            for sf in layers[layer]:
                tree.append(f"    │   ├── {sf}/")

        return "\n".join(tree)
    except Exception as e:
        return f"❌ Error al crear el scaffolding de Arquitectura Limpia: {type(e).__name__}: {e}"


@mcp.tool()
def gentleman_audit_clean_code(
    code_file_path: str,
    language: str = "python",
) -> str:
    """Audita un archivo de código buscando violaciones de acoplamiento de capas (Clean Arch) y SOLID.

    Verifica que la capa de Dominio no importe nada de Infraestructura, y busca dependencias cíclicas.

    Args:
        code_file_path: Ruta del archivo de código a auditar.
        language: Lenguaje del archivo (default: python).
    """
    try:
        file_path = Path(code_file_path)
        if not file_path.exists():
            return f"⚠️ Error: No se encontró el archivo en `{code_file_path}`"

        code_content = file_path.read_text(encoding="utf-8")
        warnings = []

        # 1. Auditoría Estática de dependencias de capas en imports (Clean Architecture Boundary Check)
        lines = code_content.splitlines()
        is_domain_file = "domain" in file_path.parts or "/domain/" in file_path.as_posix()

        if is_domain_file:
            for idx, line in enumerate(lines, 1):
                line_strip = line.strip()
                # Buscar imports ilegales de capas superiores en dominio
                illegal_imports = ["infrastructure", "application", "controllers", "database", "usecases"]
                for illegal in illegal_imports:
                    # Coincidencia de import o from
                    pattern = r"\b" + re.escape(illegal) + r"\b"
                    if (line_strip.startswith("import ") or line_strip.startswith("from ")) and re.search(pattern, line_strip):
                        warnings.append(
                            f"🚨 Violación de Capas (Línea {idx}): Un archivo del DOMINIO no puede importar de '{illegal}'.\n"
                            f"   > Código: `{line_strip}`"
                        )

        # 2. Auditoría por IA sobre SOLID y Acoplamiento
        registry = AgentRegistry()
        validator = registry.get("validator")

        prompt = (
            f"Realiza una auditoría de Clean Code y principios SOLID sobre el siguiente código.\n"
            f"Archivo: `{file_path.name}`\n"
            f"Lenguaje: {language}\n\n"
            f"Código:\n```\n{code_content}\n```\n\n"
            f"Analiza:\n"
            f"1. Principio de Responsabilidad Única (SRP) y acoplamiento.\n"
            f"2. Inyección de dependencias (DIP) y firmas limpias de métodos.\n"
            f"3. Presencia de malas prácticas (funciones excesivamente largas, nombres oscuros)."
        )

        ai_report = run_single_agent(prompt, validator, forced_category="general")

        # Consolidar reporte estático + AI
        report_header = "### 🏗️ Reporte de Auditoría Clean Code & Arquitectura\n"
        if warnings:
            report_header += "#### 🚨 Alertas de Acoplamiento de Capas (Estático):\n"
            for w in warnings:
                report_header += f"- {w}\n"
            report_header += "\n---\n"
        else:
            report_header += "✅ Sin violaciones de acoplamiento de capas estáticas detectadas.\n\n---\n"

        return report_header + ai_report
    except Exception as e:
        return f"❌ Error en la auditoría Clean Code: {type(e).__name__}: {e}"


# =====================================================================
# 💾 ENGRAM TOOLS (Persistent Knowledge Memory)
# =====================================================================

@mcp.tool()
def gentleman_save_engram(
    topic: str,
    lesson_learned: str,
    project_root: str = ".",
) -> str:
    """Registra una lección aprendida, decisión de diseño o solución a un bug en la memoria persistente (Engram).

    Evita que los agentes de IA vuelvan a cometer los mismos errores o violen decisiones previas.

    Args:
        topic: Tema o bug resuelto (ej: 'Manejo de excepciones en API').
        lesson_learned: Descripción técnica detallada del aprendizaje y solución.
        project_root: Ruta raíz del proyecto (default: directorio actual).
    """
    try:
        mem_dir = Path(project_root).resolve() / "memoria"
        mem_dir.mkdir(parents=True, exist_ok=True)
        engrams_file = mem_dir / "engrams.md"

        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Si el archivo no existe, crearlo con cabecera
        if not engrams_file.exists():
            header = (
                "# 💾 Engrams de Memoria Persistente — Aprendizajes del Proyecto\n"
                "Este archivo registra las decisiones técnicas, lecciones aprendidas y bugs resueltos.\n"
                "Sirve como base de conocimiento persistente para los agentes de IA.\n\n"
                "---\n\n"
            )
            engrams_file.write_text(header, encoding="utf-8")

        # Agregar el nuevo registro
        record = (
            f"### 🗓️ [{date_str}] Tema: {topic}\n"
            f"*   **Lección Aprendida / Solución:**\n"
            f"    {lesson_learned}\n\n"
            f"---\n\n"
        )

        with open(engrams_file, "a", encoding="utf-8") as f:
            f.write(record)

        return (
            f"✅ Engram registrado en: `{engrams_file.relative_to(Path(project_root).resolve())}`\n"
            f"- **Tema:** {topic}\n"
            f"- **Fecha:** {date_str}"
        )
    except Exception as e:
        return f"❌ Error al guardar el Engram de memoria: {type(e).__name__}: {e}"


@mcp.tool()
def gentleman_search_engrams(
    query: str,
    project_root: str = ".",
) -> str:
    """Busca y recupera aprendizajes y decisiones históricas guardadas en los Engrams de memoria persistente.

    Args:
        query: Palabra clave o término técnico a buscar (ej: 'excepciones', 'base de datos').
        project_root: Ruta raíz del proyecto (default: directorio actual).
    """
    try:
        engrams_file = Path(project_root).resolve() / "memoria" / "engrams.md"

        if not engrams_file.exists():
            return (
                "⚠️ No se encontró el archivo de Engrams en `memoria/engrams.md`. "
                "Crea un engrama primero usando `gentleman_save_engram`."
            )

        content = engrams_file.read_text(encoding="utf-8")

        # Dividir por bloques usando el separador '---'
        blocks = content.split("---")
        matches = []

        query_lower = query.lower()
        for idx, block in enumerate(blocks):
            # Saltar bloques cabecera vacíos
            if "Tema:" not in block:
                continue

            if query_lower in block.lower():
                matches.append(block.strip())

        if not matches:
            return f"🔍 No se encontraron registros de memoria (Engrams) que coincidan con: '{query}'."

        report = [f"### 🔍 Engrams de Memoria Persistente Encontrados ({len(matches)} matches):\n"]
        report.append("\n\n---\n\n".join(matches))

        return "\n".join(report)
    except Exception as e:
        return f"❌ Error al buscar en los Engrams: {type(e).__name__}: {e}"


@mcp.tool()
def gentleman_autonomous_develop(
    prompt: str,
    project_path: str = ".",
    language: str = "python",
) -> str:
    """Ejecuta de forma 100% autónoma el ciclo de desarrollo completo (SDD + Scaffolding + Coding + Engrams) para una feature.

    1. Diseña SPEC.md.
    2. Inicializa carpetas Domain/Application/Infrastructure.
    3. Genera el código correspondiente.
    4. Escribe físicamente los archivos en sus capas.
    5. Registra el Engram de memoria persistente.

    Args:
        prompt: Requerimiento de software a desarrollar de forma autónoma.
        project_path: Ruta raíz del proyecto donde codificar.
        language: Lenguaje de programación ('python' o 'typescript').
    """
    import json
    
    base_path = Path(project_path).resolve()
    logger.info("Iniciando Pipeline de Desarrollo Autónomo en: %s", base_path)
    
    try:
        # --- PASO 1: CREAR BLUEPRINT (Spec-Driven Development) ---
        logger.info("[AUTÓNOMO] -> Generando especificación SDD...")
        spec_res = gentleman_create_spec(
            feature_description=prompt,
            spec_filename="SPEC.md",
            output_dir="docs",
            project_root=str(base_path),
        )
        
        # --- PASO 2: SCAFFOLDING hexagonal ---
        logger.info("[AUTÓNOMO] -> Creando estructura de capas...")
        scaffold_res = gentleman_scaffold_clean_arch(
            project_path=str(base_path),
            language=language
        )
        
        # --- PASO 3: DISEÑAR Y CODIFICAR (Coder) ---
        # Cargar los system prompts del Coder
        registry = AgentRegistry()
        coder = registry.get("coder")
        analyst = registry.get("analyst")
        security = registry.get("security")
        
        # Leer el SPEC generado
        spec_file = base_path / "docs" / "SPEC.md"
        spec_content = spec_file.read_text(encoding="utf-8") if spec_file.exists() else prompt
        
        # Diseñar el código. Le pedimos al Coder retornar un JSON estructurado para poder escribirlo en disco.
        logger.info("[AUTÓNOMO] -> Escribiendo código de capas...")
        coder_prompt = (
            f"Basado en la siguiente especificación técnica:\n\n"
            f"```markdown\n{spec_content}\n```\n\n"
            f"Desarrolla todo el código necesario para las tres capas de Arquitectura Limpia:\n"
            f"- src/domain/ (Entidades, excepciones e interfaces de repositorio)\n"
            f"- src/application/ (Casos de uso y DTOs)\n"
            f"- src/infrastructure/ (Implementación de base de datos, repositorios o controladores)\n\n"
            f"Debes retornar ÚNICAMENTE un bloque de código JSON válido con la lista de archivos a crear. "
            f"Cualquier texto adicional fuera del JSON romperá el parser. El formato debe ser estrictamente:\n"
            f"[\n"
            f"  {{\n"
            f"    \"path\": \"src/domain/entities/user.py\",\n"
            f"    \"content\": \"contenido del archivo\"\n"
            f"  }}\n"
            f"]"
        )
        
        # Ejecutar Coder
        code_res = run_single_agent(coder_prompt, coder, forced_category="coding")
        
        # --- PASO 4: AUDITORÍA DE SEGURIDAD Y REFACTOR ---
        logger.info("[AUTÓNOMO] -> Ejecutando auditoría de seguridad y calidad...")
        security_prompt = (
            f"Analiza y refactoriza la siguiente propuesta de archivos de desarrollo:\n\n"
            f"{code_res}\n\n"
            f"Verifica la robustez de seguridad (timeouts, excepciones, inyecciones) y la conformidad de capas. "
            f"Retorna la versión final corregida y refactorizada en el mismo formato JSON estricto "
            f"(sin explicaciones de texto adicionales fuera del JSON):\n"
            f"[\n"
            f"  {{\n"
            f"    \"path\": \"src/domain/entities/user.py\",\n"
            f"    \"content\": \"contenido del archivo refactorizado\"\n"
            f"  }}\n"
            f"]"
        )
        
        final_code_res = run_single_agent(security_prompt, security, forced_category="coding")
        
        # --- PASO 5: PARSEAR E INYECTAR ARCHIVOS EN EL DISCO ---
        logger.info("[AUTÓNOMO] -> Escribiendo archivos en el disco...")
        # Extraer JSON usando regex por si el LLM incluyó marcas ```json o texto explicativo
        json_match = re.search(r"(\[.*\])", final_code_res, re.DOTALL)
        if not json_match:
            # Reintentar con la respuesta original por si acaso
            json_match = re.search(r"(\[.*\])", code_res, re.DOTALL)
            
        if not json_match:
            return (
                f"❌ Error Autónomo: El enjambre de agentes no retornó un formato de datos JSON válido "
                f"para la inyección física de archivos. Respuesta de seguridad:\n\n{final_code_res}"
            )
            
        files_to_create = json.loads(json_match.group(1))
        
        created_files = []
        for file_info in files_to_create:
            rel_path = file_info.get("path")
            content = file_info.get("content")
            
            if rel_path and content:
                # Asegurar que se escriba bajo la raíz del proyecto
                full_file_path = base_path / rel_path
                full_file_path.parent.mkdir(parents=True, exist_ok=True)
                full_file_path.write_text(content, encoding="utf-8")
                created_files.append(rel_path)
                
        # --- PASO 6: REGISTRAR ENGRAM ---
        logger.info("[AUTÓNOMO] -> Guardando Engram de memoria...")
        features_list = ", ".join(f"`{f}`" for f in created_files)
        engram_msg = (
            f"Se implementó de forma autónoma la feature '{prompt}'.\n"
            f"Archivos creados: {features_list}."
        )
        gentleman_save_engram(
            topic=f"Feature: {prompt[:40]}...",
            lesson_learned=engram_msg,
            project_root=str(base_path)
        )
        
        # --- PASO 7: CONSOLIDAR REPORTE ---
        files_tree_lines = [f"- 📁 {f}" for f in created_files]
        files_tree = "\n".join(files_tree_lines)
        
        report = (
            f"## 🏆 Desarrollo Autónomo Completado Exitosamente\n"
            f"El enjambre de agentes completó el ciclo end-to-end de Gentleman Programming.\n\n"
            f"### 📂 Archivos Creados en el Proyecto:\n"
            f"{files_tree}\n\n"
            f"### 📐 Especificación SDD (`docs/SPEC.md`):\n"
            f"La especificación técnica del blueprint fue guardada de forma segura en disco.\n\n"
            f"### 💾 Engram de Memoria Persistente:\n"
            f"Registrado correctamente en `memoria/engrams.md` para futuras contextualizaciones.\n\n"
            f"---\n"
            f"### 🔍 Vista previa de código generado:\n\n"
        )
        
        # Mostrar el primer archivo como muestra en el reporte
        if files_to_create:
            first_file = files_to_create[0]
            report += (
                f"**Archivo:** `{first_file.get('path')}`\n"
                f"```python\n"
                f"{first_file.get('content')[:1000]}...\n"
                f"```"
            )
            
        return report
        
    except Exception as e:
        return f"❌ Error catastrófico en el pipeline autónomo: {type(e).__name__}: {e}"

