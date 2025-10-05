# =====================================================================
# MICROORGANISMO: Abstract base class for building microorganisms
# Translated from C++ to Python
# =====================================================================

from abc import ABC, abstractmethod
from .agar import Posicion, Movimiento

class Microorganismo(ABC):
    """
    This is the abstract class to build microorganisms.
    To build a new microorganism you should always inherit from this class.

    Don't modify this class!
    @author Diego (translated to Python)
    """
    
    def __init__(self):
        self.id: int = 0          # the colony identificator
        self.pos: Posicion = None # actual position: updated with each time step
        self.ene: float = 0.0     # actual energy: updated with each time step
        
    def nombre(self) -> str:
        """Returns the name of the microorganism."""
        return "microorganismo abstracto"
        
    def autor(self) -> str:
        """Returns the author of the microorganism."""
        return "no sabe, no contesta"
        
    def update(self, i: int, p: Posicion, e: float) -> None:
        """
        Petri updates the microorganism attributes
        
        Args:
            i: the colony identifier
            p: the absolute position of the microorganism
            e: the actual energy of the microorganism
        """
        self.id = i
        self.pos = p
        self.ene = e
        
    @abstractmethod
    def move(self, mov: Movimiento) -> None:
        """
        The microorganism decides the next position by relative movement
        
        Args:
            mov: the desired relative movement of the microorganism (modified in place)
        """
        mov.dx = 0
        mov.dy = 0
        
    @abstractmethod
    def mitosis(self) -> bool:
        """
        The microorganism decides its duplication.
        
        Returns:
            True if the microorganism wants to duplicate itself
        """
        return False
        
    # Backward compatibility method (deprecated)
    def mover(self, pos: Posicion, mov: Movimiento) -> None:
        """
        Backward compatibility!!! Please don't use this method, 
        it will be REMOVED in the next release.
        
        Args:
            pos: the absolute position of the microorganism
            mov: the desired relative movement of the microorganism (modified in place)
        """
        mov.dx = 0
        mov.dy = 0