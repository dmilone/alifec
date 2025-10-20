# =====================================================================
# MICROORGANISMO: Clase base en castellano con aliases en inglés
# Se mantiene compatibilidad exportando los nombres en inglés como alias
# =====================================================================

from abc import ABC
from .agar import Posicion, Movimiento


class Microorganismo(ABC):
    """
    Clase base para construir microorganismos (API en castellano).
    Los nuevos microorganismos deben implementar la API en castellano.

    @autor Diego (traducido a Python)
    """

    def __init__(self):
        self.id: int = 0          # identificador de la colonia
        self.pos: Posicion = None # posición actual: actualizada en cada paso de tiempo
        self.ene: float = 0.0     # energía actual: actualizada en cada paso de tiempo

    # --- API en castellano ---------------------------------------------
    def nombre(self) -> str:
        """Devuelve el nombre del microorganismo."""
        return "microorganismo abstracto"

    def autor(self) -> str:
        """Devuelve el autor del microorganismo."""
        return "no sabe, no contesta"

    def actualizar(self, i: int, p: Posicion, e: float) -> None:
        """
        Petri actualiza los atributos del microorganismo.

        Args:
            i: identificador de la colonia
            p: posición absoluta del microorganismo
            e: energía actual del microorganismo
        """
        self.id = i
        self.pos = p
        self.ene = e

    def decidir_movimiento(self, mov: Movimiento) -> None:
        """
        Método en castellano para decidir el movimiento.

        Implementación por defecto: quedarse en sitio.
        Sobrescribir en subclases para definir comportamiento.
        """
        mov.dx = 0
        mov.dy = 0

    def quiere_mitosis(self) -> bool:
        """
        Método en castellano para decidir si se reproduce.
        Devolver True si desea duplicarse.
        """
        return False
