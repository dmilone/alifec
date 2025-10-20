"""Shim de compatibilidad: reexporta Grafica como Grapher

Este archivo mantiene la compatibilidad con imports antiguos que
esperan `from lib.grapher import Grapher`. La implementación real
se encuentra en `lib.grafica`.
"""

from .grafica import Grafica

# Exponer nombre histórico Grapher para compatibilidad
class Grapher(Grafica):
    pass

# También dejar el nombre en español accesible directamente
ColaGrafica = Grafica