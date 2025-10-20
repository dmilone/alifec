# =====================================================================
# MICROORGANISMO: Clase base en castellano con aliases en inglés
# Se mantiene compatibilidad exportando los nombres en inglés como alias
# =====================================================================

from abc import ABC, abstractmethod
from .agar import Posicion, Movimiento

class Microorganismo(ABC):
    """
    Esta es la clase abstracta para construir microorganismos.
    Para crear un nuevo microorganismo hay que heredar de esta clase.

    No modificar esta clase directamente.
    @autor Diego (traducido a Python por Diego)
    """

    def __init__(self):
        self.id: int = 0          # identificador de la colonia
        self.pos: Posicion = None # posición actual: actualizada en cada paso de tiempo
        self.ene: float = 0.0     # energía actual: actualizada en cada paso de tiempo

    # --- API en castellano (preferida) ---------------------------------
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

    @abstractmethod
    def decidir_movimiento(self, mov: Movimiento) -> None:
        """
        El microorganismo decide la próxima posición mediante movimiento relativo.

        Args:
            mov: movimiento relativo deseado por el microorganismo (modificado en sitio)
        """
        mov.dx = 0
        mov.dy = 0

    @abstractmethod
    def quiere_mitosis(self) -> bool:
        """
        El microorganismo decide si se duplica.

        Returns:
            True si el microorganismo quiere duplicarse
        """
        return False

    # --- Aliases en inglés para compatibilidad (obsoletos) ---------------
    # Mantener estos métodos aquí para que código existente no rompa de
    # forma inmediata. Los nuevos microorganismos deberían implementar la
    # API en castellano.
    def update(self, i: int, p: Posicion, e: float) -> None:
        """Alias obsoleto de `actualizar`."""
        return self.actualizar(i, p, e)

    def move(self, mov: Movimiento) -> None:
        """Alias obsoleto de `decidir_movimiento`.

        Nota: implementar `decidir_movimiento` en subclasses; el alias llama a ella.
        """
        return self.decidir_movimiento(mov)

    def mitosis(self) -> bool:
        """Alias obsoleto de `quiere_mitosis`."""
        return self.quiere_mitosis()

    # Método por compatibilidad hacia atrás (el antiguo `mover`)
    def mover(self, pos: Posicion, mov: Movimiento) -> None:
        """
        Compatibilidad hacia atrás: no usar este método, será ELIMINADO en la próxima versión.

        Args:
            pos: posición absoluta del microorganismo
            mov: movimiento relativo deseado por el microorganismo (modificado en sitio)
        """
        mov.dx = 0
        mov.dy = 0
