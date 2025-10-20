"""Shim de compatibilidad: reexporta Colonia como Colony

Este archivo existe para evitar romper imports en `mos/` y en el
resto del código que esperan `from lib.colony import Colony`.
La implementación en castellano está en `lib.colonia`.
"""

from .colonia import Colonia

# Exponer el nombre original Colony para compatibilidad
class Colony(Colonia):
    pass
# =====================================================================
# COLONY: Cada colonia gobierna un grupo de microorganismos
# Traducido de C++ a Python
# =====================================================================
# Module removed: legacy shim for Colony
# The functionality has been migrated to `lib.colonia` and `lib.grafica`.
# This file is intentionally disabled to force callers to use the new modules.
raise ImportError(
    "lib.colony has been removed. Use 'from lib.colonia import Colonia' (and update callers to Colonia.nombre()/autor())."
)