# =====================================================================
# BUSCAN: Ejemplo simple de microorganismo (busca nutrientes)
# Traducido de C++ a Python
# =====================================================================

from lib.microorganismo import Microorganismo
from lib.agar import Movimiento, agar

class BuscaN(Microorganismo):
    """
    Microorganismo buscador de nutrientes - se mueve hacia la mayor concentración de nutrientes

    @autor Compu2 (traducido a Python)
    """
    
    def nombre(self) -> str:
        return "Busca Nutrientes"
        
    def autor(self) -> str:
        return "Compu2"
        
    def move(self, mov: Movimiento) -> None:
        """Moverse a una de las 8 posiciones vecinas con más nutrientes"""
        x_max = 0
        y_max = 0
        
        # Revisar las 8 posiciones vecinas
        for x_rel in range(-1, 2):
            for y_rel in range(-1, 2):
                if (agar.nutrientes(self.pos.x + x_rel, self.pos.y + y_rel) > 
                    agar.nutrientes(self.pos.x + x_max, self.pos.y + y_max)):
                    x_max = x_rel
                    y_max = y_rel
                    
        mov.dx = x_max
        mov.dy = y_max
        
    def mitosis(self) -> bool:
        """Se reproduce si la energía > 5000"""
        return self.ene > 5000