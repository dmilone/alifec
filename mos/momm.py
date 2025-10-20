# =====================================================================
# MOmm: mov minus minus
# Traducido de C++ a Python
# =====================================================================

from lib.microorganismo import Microorganismo
from lib.agar import Movimiento

class MOmm(Microorganismo):
    """
    Microorganismo simple que siempre se mueve en diagonal abajo-izquierda

    @autor Compu2 (traducido a Python)
    """
    
    def nombre(self) -> str:
        return "MO--"
        
    def autor(self) -> str:
        return "Compu2"
        
    def decidir_movimiento(self, mov: Movimiento) -> None:
        """Siempre moverse en diagonal abajo-izquierda"""
        mov.dx = -1
        mov.dy = -1

    def quiere_mitosis(self) -> bool:
        """Comportamiento por defecto de mitosis"""
        return False