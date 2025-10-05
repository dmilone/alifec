# =====================================================================
# BUSCAN: Simple microorganism example (searches for nutrients)
# Translated from C++ to Python
# =====================================================================

from lib.microorg import Microorganismo
from lib.agar import Movimiento, agar

class BuscaN(Microorganismo):
    """
    Nutrient-seeking microorganism - moves towards highest nutrient concentration
    
    @author Compu2 (translated to Python)
    """
    
    def nombre(self) -> str:
        return "Busca Nutrientes"
        
    def autor(self) -> str:
        return "Compu2"
        
    def move(self, mov: Movimiento) -> None:
        """Move to one of the 8 neighboring positions with most food"""
        x_max = 0
        y_max = 0
        
        # Check all 8 neighboring positions
        for x_rel in range(-1, 2):
            for y_rel in range(-1, 2):
                if (agar.nutrientes(self.pos.x + x_rel, self.pos.y + y_rel) > 
                    agar.nutrientes(self.pos.x + x_max, self.pos.y + y_max)):
                    x_max = x_rel
                    y_max = y_rel
                    
        mov.dx = x_max
        mov.dy = y_max
        
    def mitosis(self) -> bool:
        """Reproduce if energy > 5000"""
        return self.ene > 5000