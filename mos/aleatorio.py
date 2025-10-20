# =====================================================================
# ALEATORIO: Ejemplo simple de microorganismo (Escherichia Coli)
# Traducido de C++ a Python
# =====================================================================

import random
from lib.microorganismo import Microorganismo
from lib.agar import Movimiento

class Aleatorio(Microorganismo):
    """
    Microorganismo de movimiento aleatorio - ejemplo simple

    @autor Compu2 (traducido a Python)
    """
    
    def nombre(self) -> str:
        return "Aleatorio"
        
    def autor(self) -> str:
        return "Compu2"
        
    def decidir_movimiento(self, mov: Movimiento) -> None:
        """Elegir aleatoriamente cualquiera de las 8 celdas vecinas"""
        mov.dx = random.randint(0, 2) - 1  # -1, 0 o 1
        mov.dy = random.randint(0, 2) - 1  # -1, 0 o 1
        
    def quiere_mitosis(self) -> bool:
        """Se reproduce si la energía > 5000"""
        return self.ene > 5000