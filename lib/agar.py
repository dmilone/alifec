# =====================================================================
# AGAR: Sustancia gelatinosa usada como medio de cultivo para trabajos microbiológicos
# Traducido desde C++ a Python
# =====================================================================

from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class Posicion:
    """Posición absoluta de un microorganismo"""
    x: int
    y: int

@dataclass 
class Movimiento:
    """Movimiento relativo de un microorganismo"""
    dx: int
    dy: int

@dataclass
class Celda:
    """Celda que contiene información del microorganismo y de nutrientes"""
    id_mo: int = 0           # identificador del microorganismo
    energia_mo: float = 0.0  # energía del microorganismo
    nutrientes: float = 0.0  # cantidad de nutrientes en esta posición

# Alias de tipo para la grilla de celdas
Celdas = List[List[Celda]]

class Agar:
    """
    Agar es una sustancia gelatinosa usada como medio de cultivo.

    No modificar esta clase directamente.
    @autor Diego (traducido a Python)
    """
    
    def __init__(self):
        self.mx_x: int = 0
        self.mx_y: int = 0
        self.rx: int = 0  # desplazamiento relativo de los nutrientes
        self.ry: int = 0
        self.dist_n: int = 0  # copia de la distribución de nutrientes
        self.celdas: Celdas = []  # información sobre MOs y nutrientes
        
    def max_x(self) -> int:
        """Devuelve el ancho del Agar"""
        return self.mx_x
        
    def max_y(self) -> int:
        """Devuelve la altura del Agar"""
        return self.mx_y
        
    def dist_nutri(self) -> int:
        """Devuelve la distribución de nutrientes actual"""
        return self.dist_n
        
    def ocupacion(self, x: int, y: int) -> int:
        """Devuelve el identificador del MO en la posición x,y"""
        return self.celdas[x % self.mx_x][y % self.mx_y].id_mo
        
    def energia(self, x: int, y: int) -> float:
        """Devuelve la energía vital del MO en la posición x,y"""
        return self.celdas[x % self.mx_x][y % self.mx_y].energia_mo
        
    def nutrientes(self, x: int, y: int) -> float:
        """Devuelve la cantidad total de nutrientes en la posición x,y"""
        return self.celdas[(x + self.rx) % self.mx_x][(y + self.ry) % self.mx_y].nutrientes

# Esta instancia es la interfaz para proveer información a los MOs
agar = Agar()