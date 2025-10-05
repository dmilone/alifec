# =====================================================================
# COLONY: Each colony governs a group of microorganisms
# Translated from C++ to Python
# =====================================================================

from typing import List, Type, Optional
from .defs import *
from .agar import Posicion, Movimiento, agar
from .microorg import Microorganismo

class Colony:
    """
    Colony class that manages a group of microorganisms of the same type.
    
    Don't modify this class!
    @author Diego (translated to Python)
    """
    
    def __init__(self, microorg_class: Type[Microorganismo], id: int, rad: int):
        self.ident: int = id
        self.n_mo_alives: int = 0
        self.max_x: int = 2 * rad
        self.max_y: int = 2 * rad
        self.microorg_class = microorg_class
        
        # Initialize grids
        self.my_mos: List[List[Optional[Microorganismo]]] = [[None for _ in range(self.max_y)] 
                                                             for _ in range(self.max_x)]
        self.movs: List[List[Movimiento]] = [[Movimiento(0, 0) for _ in range(self.max_y)] 
                                             for _ in range(self.max_x)]
        self.dups: List[List[bool]] = [[False for _ in range(self.max_y)] 
                                       for _ in range(self.max_x)]
        
        # Prototype MO for getting name and author
        self.proto_mo: Microorganismo = microorg_class()
        
        # Random order arrays
        self.xr: List[int] = list(range(self.max_x))
        self.yr: List[int] = list(range(self.max_y))
        
    def __del__(self):
        """Destructor to clean up microorganisms"""
        try:
            if hasattr(self, 'my_mos') and hasattr(self, 'max_x') and hasattr(self, 'max_y'):
                for x in range(self.max_x):
                    for y in range(self.max_y):
                        if x < len(self.my_mos) and y < len(self.my_mos[x]):
                            if self.my_mos[x][y] is not None:
                                del self.my_mos[x][y]
            if hasattr(self, 'proto_mo'):
                del self.proto_mo
        except (AttributeError, IndexError, TypeError):
            # Ignore cleanup errors during garbage collection
            pass
        
    def n_alives(self) -> int:
        """Returns the number of alive microorganisms"""
        return self.n_mo_alives
        
    def mov(self, x: int, y: int) -> Movimiento:
        """Returns the movement that the MO at position x,y wants to make"""
        try:
            return self.movs[x][y]
        except IndexError:
            return Movimiento(0, 0)
        
    def moved(self, x: int, y: int) -> bool:
        """Returns True if the MO tried to move"""
        try:
            return self.movs[x][y].dx != 0 or self.movs[x][y].dy != 0
        except IndexError:
            return False
        
    def duplicate(self, x: int, y: int) -> bool:
        """Returns True if the MO tried to reproduce"""
        try:
            return self.dups[x][y]
        except IndexError:
            return False
        
    def kill(self, x: int, y: int) -> None:
        """Eliminates a MO"""
        try:
            if self.my_mos[x][y] is not None:
                del self.my_mos[x][y]
                self.my_mos[x][y] = None
                self.n_mo_alives -= 1
                self.movs[x][y].dx = 0
                self.movs[x][y].dy = 0
                self.dups[x][y] = False
        except IndexError:
            return
            
    def create(self, x: int, y: int) -> None:
        """Creates a new MO"""
        try:
            if self.my_mos[x][y] is None:
                self.my_mos[x][y] = self.microorg_class()
                self.n_mo_alives += 1
        except IndexError:
            return
            
    def move(self, old: Posicion, neu: Posicion) -> None:
        """Moves a MO from one place to another"""
        try:
            self.my_mos[neu.x][neu.y] = self.my_mos[old.x][old.y]
            self.my_mos[old.x][old.y] = None
            self.movs[old.x][old.y].dx = 0
            self.movs[old.x][old.y].dy = 0
            self.dups[old.x][old.y] = False
        except IndexError:
            return  # Skip invalid moves
        
    def live(self, x: int, y: int) -> None:
        """Gives a MO the possibility to move"""
        x %= self.max_x
        y %= self.max_y
        
        if x >= len(self.my_mos) or y >= len(self.my_mos[0]):
            return
            
        if x >= len(self.xr) or y >= len(self.yr) or x < 0 or y < 0:
            return
            
        xr_idx = self.xr[x]
        yr_idx = self.yr[y]
        
        try:
            if self.my_mos[xr_idx][yr_idx] is not None:
                pos = Posicion(xr_idx, yr_idx)
                mo = self.my_mos[xr_idx][yr_idx]
                mo.update(self.ident, pos, agar.energia(xr_idx, yr_idx))
                mo.move(self.movs[xr_idx][yr_idx])
                self.dups[xr_idx][yr_idx] = mo.mitosis()
            else:
                self.movs[xr_idx][yr_idx].dx = 0
                self.movs[xr_idx][yr_idx].dy = 0
                self.dups[xr_idx][yr_idx] = False
        except IndexError:
            return
            
    def name(self) -> str:
        """Returns the name of the microorganism type"""
        return self.proto_mo.nombre()
        
    def author(self) -> str:
        """Returns the author of the microorganism type"""
        return self.proto_mo.autor()