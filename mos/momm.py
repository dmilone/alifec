# =====================================================================
# MOmm: mov minus minus
# Translated from C++ to Python
# =====================================================================

from lib.microorg import Microorganismo
from lib.agar import Movimiento

class MOmm(Microorganismo):
    """
    Simple microorganism that always moves diagonally down-left
    
    @author Compu2 (translated to Python)
    """
    
    def nombre(self) -> str:
        return "MO--"
        
    def autor(self) -> str:
        return "Compu2"
        
    def move(self, mov: Movimiento) -> None:
        """Always move diagonally down-left"""
        mov.dx = -1
        mov.dy = -1
        
    def mitosis(self) -> bool:
        """Default mitosis behavior"""
        return False