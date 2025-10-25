# =====================================================================
# MOyy: Ejemplo simple de microorganismo
# Traducido de C++ a Python
# =====================================================================

from vida.microorganismo import Microorganismo
from vida.agar import Movimiento, agar

class MOyy(Microorganismo):
    """
    Microorganismo que se mueve verticalmente hacia más comida

    @autor Compu2 (traducido a Python)
    """
    
    def nombre(self) -> str:
        return "MOyy"
        
    def autor(self) -> str:
        return "Compu2"
        
    def decidir_movimiento(self, mov: Movimiento) -> None:
        """Moverse hacia donde hay más alimento, pero sólo en la dirección y"""
        if agar.nutrientes(self.pos.x, self.pos.y - 1) > agar.nutrientes(self.pos.x, self.pos.y):
            mov.dy = -1
        elif agar.nutrientes(self.pos.x, self.pos.y + 1) > agar.nutrientes(self.pos.x, self.pos.y):
            mov.dy = 1
        else:
            mov.dy = 0
        mov.dx = 0

    def quiere_mitosis(self) -> bool:
        """Se reproduce si la energía > 500"""
        return self.ene > 500