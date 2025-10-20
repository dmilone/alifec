# =====================================================================
# MOxx: Ejemplo simple de microorganismo
# Traducido de C++ a Python
# =====================================================================

from lib.microorganismo import Microorganismo
from lib.agar import Movimiento, agar

class MOxx(Microorganismo):
    """
    Microorganismo que se mueve horizontalmente hacia más comida

    @autor Compu2 (traducido a Python)
    """
    
    def nombre(self) -> str:
        return "MOxx"
        
    def autor(self) -> str:
        return "Compu2"
        
    def move(self, mov: Movimiento) -> None:
        """Moverse hacia donde hay más alimento, pero sólo en la dirección x"""
        if agar.nutrientes(self.pos.x - 1, self.pos.y) > agar.nutrientes(self.pos.x, self.pos.y):
            mov.dx = -1
        elif agar.nutrientes(self.pos.x + 1, self.pos.y) > agar.nutrientes(self.pos.x, self.pos.y):
            mov.dx = 1
        else:
            mov.dx = 0
        mov.dy = 0
        
    def mitosis(self) -> bool:
        """Se reproduce si la energía > 500"""
        return self.ene > 500