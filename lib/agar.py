# =====================================================================
# AGAR: Gelatinous substance used as a culture medium for microbiological work
# Translated from C++ to Python
# =====================================================================

from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class Posicion:
    """Absolute position of a microorganism"""
    x: int
    y: int

@dataclass 
class Movimiento:
    """Relative movement of a microorganism"""
    dx: int
    dy: int

@dataclass
class Celda:
    """Cell containing microorganism and nutrient information"""
    id_mo: int = 0           # microorganism identifier
    energia_mo: float = 0.0  # energy of the microorganism
    nutrientes: float = 0.0  # amount of nutrients in this position

# Type alias for the grid of cells
Celdas = List[List[Celda]]

class Agar:
    """
    Agar is a gelatinous substance chiefly used as a culture medium 
    for microbiological work.
    
    Don't modify this class!
    @author Diego (translated to Python)
    """
    
    def __init__(self):
        self.mx_x: int = 0
        self.mx_y: int = 0
        self.rx: int = 0  # relative movement of the nutrients
        self.ry: int = 0
        self.dist_n: int = 0  # copy of the nutrient distribution
        self.celdas: Celdas = []  # the information about MOs and nutrients
        
    def max_x(self) -> int:
        """Returns the width of the Agar"""
        return self.mx_x
        
    def max_y(self) -> int:
        """Returns the height of the Agar"""
        return self.mx_y
        
    def dist_nutri(self) -> int:
        """Returns the actual nutrient distribution"""
        return self.dist_n
        
    def ocupacion(self, x: int, y: int) -> int:
        """Returns the identifier of the MO in position x,y"""
        return self.celdas[x % self.mx_x][y % self.mx_y].id_mo
        
    def energia(self, x: int, y: int) -> float:
        """Returns the vital energy of the MO in position x,y"""
        return self.celdas[x % self.mx_x][y % self.mx_y].energia_mo
        
    def nutrientes(self, x: int, y: int) -> float:
        """Returns the total amount of nutrients in position x,y"""
        return self.celdas[(x + self.rx) % self.mx_x][(y + self.ry) % self.mx_y].nutrientes

# This instance is the interface to supply information to the MOs
agar = Agar()