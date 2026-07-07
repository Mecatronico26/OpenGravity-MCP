"""Pruebas unitarias de las herramientas del ecosistema Gentleman Programming."""

import os
import shutil
import sys
from pathlib import Path
from opengravity.tools.gentleman_tools import (
    gentleman_create_spec,
    gentleman_validate_spec,
    gentleman_scaffold_clean_arch,
    gentleman_audit_clean_code,
    gentleman_save_engram,
    gentleman_search_engrams,
    gentleman_autonomous_develop,
)


def test_gentleman_scaffold_and_audit():
    """Valida la creación de scaffolding de Arquitectura Limpia y su auditoría."""
    test_dir = Path.cwd() / "tests" / "temp_project"
    test_dir.mkdir(parents=True, exist_ok=True)

    try:
        # 1. Probar Scaffolding
        scaffold_res = gentleman_scaffold_clean_arch(
            project_path=str(test_dir), language="python"
        )
        assert "src" in scaffold_res
        assert "domain" in scaffold_res
        assert "application" in scaffold_res
        assert "infrastructure" in scaffold_res

        # Validar existencia de carpetas físicas
        assert (test_dir / "src" / "domain" / "entities" / "__init__.py").exists()
        assert (test_dir / "src" / "infrastructure" / "repositories" / "__init__.py").exists()

        # 2. Probar Auditoría de acoplamiento de capas
        # Crear un archivo de dominio ilegal que importa de infraestructura
        domain_file = test_dir / "src" / "domain" / "entities" / "user.py"
        domain_file.write_text(
            "from src.infrastructure.database.models import UserDbModel\n"
            "class User:\n"
            "    pass\n",
            encoding="utf-8",
        )

        try:
            audit_res = gentleman_audit_clean_code(
                code_file_path=str(domain_file), language="python"
            )
            if "Error en la auditoría" in audit_res:
                # Comprobar si fue por rate limits de red y emitir advertencia
                if any(x in audit_res.lower() for x in ["rate limit", "credits", "429", "402"]):
                    print(f"\n[TEST GENTLEMAN] [WARNING] Auditoría omitida por límites de las APIs: {audit_res}")
                else:
                    assert False, f"Fallo en auditoría: {audit_res}"
            else:
                assert "Violación de Capas" in audit_res
                assert "user.py" in audit_res
        except Exception as e:
            err_msg = str(e).lower()
            if "rate limit" in err_msg or "credits" in err_msg or "429" in err_msg or "402" in err_msg:
                print(f"\n[TEST GENTLEMAN] [WARNING] Test de auditoría omitido debido a cuotas de red: {e}")
            else:
                raise e


    finally:
        # Limpiar directorio de pruebas
        if test_dir.exists():
            shutil.rmtree(test_dir)


def test_gentleman_engrams():
    """Valida el registro y búsqueda de memoria persistente (Engrams)."""
    test_root = Path.cwd() / "tests" / "temp_engrams"
    test_root.mkdir(parents=True, exist_ok=True)

    try:
        # 1. Guardar Engram
        save_res = gentleman_save_engram(
            topic="RxJS State Management",
            lesson_learned="Evitar suscripciones anidadas usando switchMap.",
            project_root=str(test_root),
        )
        assert "RxJS" in save_res
        assert "engrams.md" in save_res

        # Validar archivo físico
        engrams_md = test_root / "memoria" / "engrams.md"
        assert engrams_md.exists()

        # 2. Buscar Engram
        search_res = gentleman_search_engrams(
            query="rxjs", project_root=str(test_root)
        )
        assert "RxJS State Management" in search_res
        assert "switchMap" in search_res

        # Probar búsqueda sin resultados
        empty_res = gentleman_search_engrams(
            query="nonexistent", project_root=str(test_root)
        )
        assert "No se encontraron" in empty_res

    finally:
        # Limpiar
        if test_root.exists():
            shutil.rmtree(test_root)


def test_gentleman_autonomous_develop():
    """Valida la ejecución del pipeline autónomo completo en un directorio temporal."""
    test_root = Path.cwd() / "tests" / "temp_auto"
    test_root.mkdir(parents=True, exist_ok=True)

    try:
        prompt = "Crea una función simple para calcular el área de un círculo dado su radio."
        try:
            report = gentleman_autonomous_develop(
                prompt=prompt,
                project_path=str(test_root),
                language="python"
            )

            # Si arrojó un error controlado del orquestador por cuotas de red
            if "Error catastrófico" in report or "Error Autónomo" in report:
                if any(x in report.lower() for x in ["rate limit", "credits", "429", "402"]):
                    print(f"\n[TEST GENTLEMAN] [WARNING] Desarrollo Autónomo omitido por cuotas de las APIs: {report}")
                else:
                    assert False, f"Fallo en desarrollo autónomo: {report}"
            else:
                assert "Desarrollo Autónomo Completado" in report
                assert "SPEC.md" in report
                assert "engrams.md" in report
                
                # Comprobar que se crearon carpetas de Clean Architecture
                assert (test_root / "src" / "domain" / "entities").exists()
                assert (test_root / "docs" / "SPEC.md").exists()
                assert (test_root / "memoria" / "engrams.md").exists()
        except Exception as e:
            err_msg = str(e).lower()
            if any(x in err_msg for x in ["rate limit", "credits", "429", "402"]):
                print(f"\n[TEST GENTLEMAN] [WARNING] Test de desarrollo autónomo omitido por límites de las APIs: {e}")
            else:
                raise e

    finally:
        # Limpiar
        if test_root.exists():
            shutil.rmtree(test_root)

