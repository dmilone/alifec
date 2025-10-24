# =====================================================================
# COLONIA: una grupo de microorganismos del mismo tipo
# =====================================================================

from typing import List, Type, Optional
from .definiciones import *
from .agar import Posicion, Movimiento, agar
from .microorganismo import Microorganismo

class Colonia:
    """ 
    Un grupo de microorganismos del mismo tipo.

    No modificar esta clase!
    @autor Diego (traducido a Python también por Diego)
    """

    def __init__(self, clase_mo: Type[Microorganismo], identidad: int, radio: int):
        self.identidad: int = identidad     # tipo de MOs
        self.n_mos_vivos: int = 0
        self.max_x: int = 2 * radio
        self.max_y: int = 2 * radio
        self.clase_mo = clase_mo

        # Rejillas internas
        self.mis_mos: List[List[Optional[Microorganismo]]] = [
            [None for _ in range(self.max_y)] for _ in range(self.max_x)
        ]
        self.movimientos: List[List[Movimiento]] = [
            [Movimiento(0, 0) for _ in range(self.max_y)] for _ in range(self.max_x)
        ]
        self.duplicaciones: List[List[bool]] = [
            [False for _ in range(self.max_y)] for _ in range(self.max_x)
        ]
        # Protótipo de MO para obtener nombre y autor
        self.proto_mo: Microorganismo = self.clase_mo()

    # Movimiento que quiere hacer el de la posicion x,y
    def movimiento(self, x: int, y: int) -> Movimiento:
        try:
            return self.movimientos[x][y]
        except IndexError:
            return Movimiento(0, 0)
    
    # Si el MO intento moverse devuelve True
    def movio(self, x: int, y: int) -> bool:
        try:
            return self.movimientos[x][y].dx != 0 or self.movimientos[x][y].dy != 0
        except IndexError:
            return False
    
    # Si el MO intento reproducirse devuelve True
    def duplica(self, x: int, y: int) -> bool:
        try:
            return self.duplicaciones[x][y]
        except IndexError:
            return False

    # Elimina un MO
    def eliminar(self, x: int, y: int) -> None:
        try:
            if self.mis_mos[x][y] is not None:
                del self.mis_mos[x][y]
                self.mis_mos[x][y] = None
                self.n_mos_vivos -= 1
                self.movimientos[x][y].dx = 0
                self.movimientos[x][y].dy = 0
                self.duplicaciones[x][y] = False
        except IndexError:
            return

    # Crea un nuevo MO
    def crear(self, x: int, y: int) -> None:
        try:
            if self.mis_mos[x][y] is None:
                self.mis_mos[x][y] = self.clase_mo()
                self.n_mos_vivos += 1
        except IndexError:
            return

    # Mueve un MO de lugar
    def mover(self, anterior: Posicion, nueva: Posicion) -> None:
        try:
            self.mis_mos[nueva.x][nueva.y] = self.mis_mos[anterior.x][anterior.y]
            self.mis_mos[anterior.x][anterior.y] = None
            self.movimientos[anterior.x][anterior.y].dx = 0
            self.movimientos[anterior.x][anterior.y].dy = 0
            self.duplicaciones[anterior.x][anterior.y] = False
        except IndexError:
            return

    # Le da la posibilidad al MO de actuar (moverse y/o reproducirse)
    def vivir(self, x: int, y: int) -> None:
        x %= self.max_x
        y %= self.max_y # por las dudas nomas...

        try:
            if self.mis_mos[x][y] is not None:
                pos = Posicion(x, y)
                mo = self.mis_mos[x][y]
                # Actualizar estado del microorganismo
                mo.actualizar(self.identidad, pos, agar.energia(x, y))
                # Pedir al microorganismo que decida su movimiento
                mo.decidir_movimiento(self.movimientos[x][y])
                # Consultar si quiere mitosis (reproducirse)
                self.duplicaciones[x][y] = mo.quiere_mitosis()
            else:
                self.movimientos[x][y].dx = 0
                self.movimientos[x][y].dy = 0
                self.duplicaciones[x][y] = False
        except IndexError:
            return

    def n_vivos(self) -> int:
        return self.n_mos_vivos

    def nombre(self) -> str:
        return self.proto_mo.nombre()

    def autor(self) -> str:
        return self.proto_mo.autor()
