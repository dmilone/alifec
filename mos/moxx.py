# =====================================================================
# MOxx: Simple microorganism example
# Translated from C++ to Python
# =====================================================================

from lib.microorg import Microorganismo
from lib.agar import Movimiento, agar

class MOxx(Microorganismo):
    """
    Microorganism that moves horizontally towards food
    
    @author Compu2 (translated to Python)
    """
    
    def nombre(self) -> str:
        return "MOxx"
        
    def autor(self) -> str:
        return "Compu2"
        
    def move(self, mov: Movimiento) -> None:
        """Move towards where there is more food, but only in x direction"""
        if agar.nutrientes(self.pos.x - 1, self.pos.y) > agar.nutrientes(self.pos.x, self.pos.y):
            mov.dx = -1
        elif agar.nutrientes(self.pos.x + 1, self.pos.y) > agar.nutrientes(self.pos.x, self.pos.y):
            mov.dx = 1
        else:
            mov.dx = 0
        mov.dy = 0
        
    def mitosis(self) -> bool:
        """Reproduce if energy > 500"""
        return self.ene > 500