"""Pruebas del selector de modelos dinámico."""

from opengravity.orchestrator.model_selector import select_best_model


def test_select_best_model():
    """Valida la resolución de categorías a nombres de modelos válidos."""
    # Probar que las categorías técnicas mapeen correctamente a tuplas (provider, model_id)
    provider_c, model_c = select_best_model("coding")
    provider_r, model_r = select_best_model("reasoning")
    provider_g, model_g = select_best_model("general")
    provider_f, model_f = select_best_model("fast")

    assert provider_c in ["groq", "openrouter"]
    assert provider_r in ["groq", "openrouter"]
    assert provider_g in ["groq", "openrouter"]
    assert provider_f in ["groq", "openrouter"]

    assert len(model_c) > 0
    assert len(model_r) > 0
    assert len(model_g) > 0
    assert len(model_f) > 0

    print(f"\n[TEST] Modelos seleccionados:")
    print(f"  - Coding:    {model_c} ({provider_c})")
    print(f"  - Reasoning: {model_r} ({provider_r})")
    print(f"  - General:   {model_g} ({provider_g})")
    print(f"  - Fast:      {model_f} ({provider_f})")
