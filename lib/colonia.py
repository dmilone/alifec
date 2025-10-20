"""
COLONIA: una colonia de microorganismos del mismo tipo
"""
from typing import List, Type, Optional
from .definiciones import *
from .agar import Posicion, Movimiento, agar
from .microorganismo import Microorganismo


class Colonia:
    """ Un grupo de microorganismos del mismo tipo.
    """

    def __init__(self, microorg_class: Type[Microorganismo], ident: int, rad: int):
        self.ident: int = ident
        self.n_mos_vivos: int = 0
        self.max_x: int = 2 * rad
        self.max_y: int = 2 * rad
        self.microorg_class = microorg_class

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
        self.proto_mo: Microorganismo = microorg_class()

        # Órdenes aleatorios para iteración
        self.orden_x: List[int] = list(range(self.max_x))
        self.orden_y: List[int] = list(range(self.max_y))

    def __del__(self):
        try:
            if hasattr(self, 'mis_mos') and hasattr(self, 'max_x') and hasattr(self, 'max_y'):
                for x in range(self.max_x):
                    for y in range(self.max_y):
                        if x < len(self.mis_mos) and y < len(self.mis_mos[x]):
                            if self.mis_mos[x][y] is not None:
                                del self.mis_mos[x][y]
            if hasattr(self, 'proto_mo'):
                del self.proto_mo
        except (AttributeError, IndexError, TypeError):
            pass

    # ----- Consultas -----
    def n_vivos(self) -> int:
        return self.n_mos_vivos

    def movimiento(self, x: int, y: int) -> Movimiento:
        try:
            return self.movimientos[x][y]
        except IndexError:
            return Movimiento(0, 0)

    def movio(self, x: int, y: int) -> bool:
        try:
            return self.movimientos[x][y].dx != 0 or self.movimientos[x][y].dy != 0
        except IndexError:
            return False

    def duplica(self, x: int, y: int) -> bool:
        try:
            return self.duplicaciones[x][y]
        except IndexError:
            return False

    # ----- Mutadores -----
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

    def crear(self, x: int, y: int) -> None:
        try:
            if self.mis_mos[x][y] is None:
                self.mis_mos[x][y] = self.microorg_class()
                self.n_mos_vivos += 1
        except IndexError:
            return

    def mover(self, old: Posicion, neu: Posicion) -> None:
        try:
            self.mis_mos[neu.x][neu.y] = self.mis_mos[old.x][old.y]
            self.mis_mos[old.x][old.y] = None
            self.movimientos[old.x][old.y].dx = 0
            self.movimientos[old.x][old.y].dy = 0
            self.duplicaciones[old.x][old.y] = False
        except IndexError:
            return

    def vivir(self, x: int, y: int) -> None:
        """Permite que el MO en la posición actúe (mover/mitosis)."""
        x %= self.max_x
        y %= self.max_y

        if x >= len(self.mis_mos) or y >= len(self.mis_mos[0]):
            return

        if x >= len(self.orden_x) or y >= len(self.orden_y) or x < 0 or y < 0:
            return

        xr_idx = self.orden_x[x]
        yr_idx = self.orden_y[y]

        try:
            if self.mis_mos[xr_idx][yr_idx] is not None:
                pos = Posicion(xr_idx, yr_idx)
                mo = self.mis_mos[xr_idx][yr_idx]
                # Actualizar estado del microorganismo usando la API en castellano
                mo.actualizar(self.ident, pos, agar.energia(xr_idx, yr_idx))
                # Pedir al microorganismo que decida su movimiento
                mo.decidir_movimiento(self.movimientos[xr_idx][yr_idx])
                # Consultar si quiere mitosis (reproducirse)
                self.duplicaciones[xr_idx][yr_idx] = mo.quiere_mitosis()
            else:
                self.movimientos[xr_idx][yr_idx].dx = 0
                self.movimientos[xr_idx][yr_idx].dy = 0
                self.duplicaciones[xr_idx][yr_idx] = False
        except IndexError:
            return

    # ----- Metadatos -----
    def nombre(self) -> str:
        return self.proto_mo.nombre()

    def autor(self) -> str:
        return self.proto_mo.autor()
