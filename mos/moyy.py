# =====================================================================
# MOyy: Simple microorganism example
# Translated from C++ to Python
# =====================================================================

from lib.microorg import Microorganismo
from lib.agar import Movimiento, agar

class MOyy(Microorganismo):
    """
    Microorganism that moves vertically towards food
    
    @author Compu2 (translated to Python)
    """
    
    def nombre(self) -> str:
        return "MOyy"
        
    def autor(self) -> str:
        return "Compu2"
        
    def move(self, mov: Movimiento) -> None:
        """Move towards where there is more food, but only in y direction"""
        if agar.nutrientes(self.pos.x, self.pos.y - 1) > agar.nutrientes(self.pos.x, self.pos.y):
            mov.dy = -1
        elif agar.nutrientes(self.pos.x, self.pos.y + 1) > agar.nutrientes(self.pos.x, self.pos.y):
            mov.dy = 1
        else:
            mov.dy = 0
        mov.dx = 0
        
    def mitosis(self) -> bool:
        """Reproduce if energy > 500"""
        return self.ene > 500