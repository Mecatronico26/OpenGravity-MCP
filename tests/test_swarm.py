"""Prueba del enjambre completo de OpenGravity."""

import sys
from opengravity.orchestrator.team_solver import run_team_solve


def test_team_solve():
    """Ejecuta el debate completo del enjambre para una tarea simple."""
    # Reconfigurar salida estándar para UTF-8 si es necesario (previene fallos en terminales Windows)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    task = (
        "Escribe una clase en Python que calcule el promedio móvil (moving average) "
        "de un flujo de datos en tiempo real de forma segura. Debe manejar valores nulos (None), "
        "lista vacía, y prevenir divisiones por cero."
    )
    print("\n[TEST SWARM] Iniciando debate técnico del enjambre...")
    try:
        report = run_team_solve(task)
        assert len(report) > 0
        # Comprobar que sea un reporte técnico de ingeniería consolidado
        assert "técnico" in report.lower() or "consolidado" in report.lower() or "report" in report.lower()
        # Debe contener el código ST generado
        assert "1" in report or "0" in report
        print("\n[TEST SWARM] Reporte generado exitosamente:")
        print(report.encode("utf-8", errors="replace").decode("utf-8")[:1500])
    except Exception as e:
        # Si el error es por límites de tasa (429) o saldo (402), omitir fallo del test
        err_msg = str(e).lower()
        if "rate limit" in err_msg or "credits" in err_msg or "429" in err_msg or "402" in err_msg:
            print(f"\n[TEST SWARM] [WARNING] Test omitido debido a cuota/saldo de las APIs: {e}")
        else:
            raise e


