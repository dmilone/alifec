# =====================================================================
# TACTICAS2: Conjunto de tácticas para comportamientos estratégicos (Estrategia 2)
# Traducido de C++ a Python
# =====================================================================

import random
from typing import List, Tuple
from lib.microorganismo import Microorganismo
from lib.agar import Movimiento, agar, Posicion
from lib.defs import VACIO

class Tacticas2(Microorganismo):
    """
    Microorganismo con prioridades tácticas diferentes a Tacticas1

    @autor Compu2 (traducido a Python)
    """
    
    def __init__(self):
        super().__init__()
        self.mi_f = 0  # my row
        self.mi_c = 0  # my column
        
    def nombre(self) -> str:
        return "Tacticas2"
        
    def autor(self) -> str:
        return "Compu2"
        
    def donde_estoy(self, pos: Posicion) -> None:
        """Establecer posición actual"""
        self.mi_f = pos.y
        self.mi_c = pos.x
        
    def ver_vecindario(self) -> Tuple[List[int], List[float], List[float]]:
        """Ver vecindario - devuelve ID_MO, energía y nutrientes para 9 celdas"""
        id_mo = []
        energia = []
        nutriente = []
        
        for d_fil in range(-1, 2):
            for d_col in range(-1, 2):
                id_mo.append(agar.ocupacion(self.mi_f + d_fil, self.mi_c + d_col))
                energia.append(agar.energia(self.mi_f + d_fil, self.mi_c + d_col))
                nutriente.append(agar.nutrientes(self.mi_f + d_fil, self.mi_c + d_col))
                
        return id_mo, energia, nutriente
        
    def num_vecino_a_movimiento(self, num: int) -> Tuple[int, int]:
        """Convertir número de vecino a coordenadas relativas"""
        moves = [
            (-1, -1), (-1, 0), (-1, 1),  # 0, 1, 2
            (0, -1),  (0, 0),  (0, 1),   # 3, 4, 5
            (1, -1),  (1, 0),  (1, 1)    # 6, 7, 8
        ]
        if 0 <= num < len(moves):
            return moves[num]
        return (0, 0)
        
    def contar_vivos(self) -> Tuple[int, int]:
        """Contar organismos vivos - propios y de otros"""
        max_f = agar.max_y()
        max_c = agar.max_x()
        
        propios = 0
        otros = 0
        
        for f in range(max_f):
            for c in range(max_c):
                if agar.ocupacion(f, c) == self.id:
                    propios += 1
                elif agar.ocupacion(f, c) != VACIO:
                    otros += 1
                    
        return propios, otros
        
    def matar(self, id_mo: List[int], energia: List[float]) -> Tuple[bool, int, int]:
        """Intentar matar - moverse al vecino con menos energía y distinto tipo"""
        mov_f, mov_c = 0, 0
        encontro = False
        
        for vec in range(9):
            if (id_mo[vec] != id_mo[4] and id_mo[vec] != VACIO and 
                energia[vec] < energia[4]):
                mov_f, mov_c = self.num_vecino_a_movimiento(vec)
                encontro = True
                break
                
        return encontro, mov_f, mov_c
        
    def comer(self, id_mo: List[int], nutriente: List[float]) -> Tuple[bool, int, int]:
        """Intentar comer - ir al lugar con más alimento"""
        mov_f, mov_c = 0, 0
        nutriente_max = 0.0
        encontro = False
        
        for vec in range(9):
            if id_mo[vec] == VACIO and nutriente[vec] > nutriente_max:
                mov_f, mov_c = self.num_vecino_a_movimiento(vec)
                nutriente_max = nutriente[vec]
                encontro = True
                
        return encontro, mov_f, mov_c
        
    def reproducir(self, id_mo: List[int], energia: List[float]) -> Tuple[bool, int, int]:
        """Intentar reproducirse - moverse hacia la misma especie con mayor energía"""
        mov_f, mov_c = 0, 0
        energia_max = 0.0
        encontro = False
        
        for vec in range(9):
            if (id_mo[vec] == id_mo[4] and vec != 4 and 
                energia[vec] > energia_max):
                mov_f, mov_c = self.num_vecino_a_movimiento(vec)
                energia_max = energia[vec]
                encontro = True
                
        return encontro, mov_f, mov_c
        
    def azar(self) -> Tuple[int, int]:
        """Movimiento aleatorio a cualquiera de las 8 celdas vecinas"""
        mov_f = random.randint(0, 2) - 1
        mov_c = random.randint(0, 2) - 1
        return mov_f, mov_c
        
    def move(self, mov: Movimiento) -> None:
        """Estrategia principal de movimiento - ESTRATEGIA 2: comer -> matar -> reproducir"""
        mov_f, mov_c = 0, 0
        
        self.donde_estoy(self.pos)
        id_mo, energia, nutriente = self.ver_vecindario()
        
    # ESTRATEGIA 2 - mejor que la 1: comer -> matar -> reproducir
        encontro, mov_f, mov_c = self.comer(id_mo, nutriente)
        if not encontro:
            encontro, mov_f, mov_c = self.matar(id_mo, energia)
            if not encontro:
                encontro, mov_f, mov_c = self.reproducir(id_mo, energia)
                # if not encontro:
                #     mov_f, mov_c = self.azar()
                    
        mov.dx = mov_c
        mov.dy = mov_f
        
    def mitosis(self) -> bool:
        """Reproduce if energy > 500"""
        return self.ene > 500