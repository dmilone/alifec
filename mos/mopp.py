# =====================================================================
# MOpp: mov plus plus
# Traducido de C++ a Python
# =====================================================================

from lib.microorganismo import Microorganismo
from lib.agar import Movimiento

class MOpp(Microorganismo):
    """
    Microorganismo simple que siempre se mueve en diagonal arriba-derecha

    @autor Compu2 (traducido a Python)
    """
    
    def nombre(self) -> str:
        return "MO++"
        
    def autor(self) -> str:
        return "Compu2"
        
    def move(self, mov: Movimiento) -> None:
        """Siempre moverse en diagonal arriba-derecha"""
        mov.dx = 1
        mov.dy = 1
        
    def mitosis(self) -> bool:
        """Comportamiento por defecto de mitosis"""
        return False