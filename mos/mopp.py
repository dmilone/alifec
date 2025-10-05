# =====================================================================
# MOpp: mov plus plus
# Translated from C++ to Python
# =====================================================================

from lib.microorg import Microorganismo
from lib.agar import Movimiento

class MOpp(Microorganismo):
    """
    Simple microorganism that always moves diagonally up-right
    
    @author Compu2 (translated to Python)
    """
    
    def nombre(self) -> str:
        return "MO++"
        
    def autor(self) -> str:
        return "Compu2"
        
    def move(self, mov: Movimiento) -> None:
        """Always move diagonally up-right"""
        mov.dx = 1
        mov.dy = 1
        
    def mitosis(self) -> bool:
        """Default mitosis behavior"""
        return False