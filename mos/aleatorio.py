# =====================================================================
# ALEATORIO: Simple example of microorganism (Escherichia Coli)
# Translated from C++ to Python
# =====================================================================

import random
from lib.microorg import Microorganismo
from lib.agar import Movimiento

class Aleatorio(Microorganismo):
    """
    Random movement microorganism - simple example
    
    @author Compu2 (translated to Python)
    """
    
    def nombre(self) -> str:
        return "Aleatorio"
        
    def autor(self) -> str:
        return "Compu2"
        
    def move(self, mov: Movimiento) -> None:
        """Randomly choose any of the 8 neighboring cells"""
        mov.dx = random.randint(0, 2) - 1  # -1, 0, or 1
        mov.dy = random.randint(0, 2) - 1  # -1, 0, or 1
        
    def mitosis(self) -> bool:
        """Reproduce if energy > 5000"""
        return self.ene > 5000