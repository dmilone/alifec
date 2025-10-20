"""Shim de compatibilidad: reexporta Grafica como Grapher

Este archivo mantiene la compatibilidad con imports antiguos que
esperan `from lib.grapher import Grapher`. La implementación real
se encuentra en `lib.grafica`.
"""


# Exponer nombre histórico Grapher para compatibilidad
raise ImportError(
    "lib.grapher has been removed. Use 'from lib.grafica import Graficadora' and update callers accordingly."
)

# También dejar el nombre en español accesible directamente
ColaGrafica = Grafica