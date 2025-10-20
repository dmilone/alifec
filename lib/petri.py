# =====================================================================
# PETRI: Simulación de un plato de Petri para Competencias de vida artificial
# Traducido desde C++ a Python
# =====================================================================

import random
import math
import time
from typing import List, Dict, Type, Tuple
from .defs import *
from .agar import Posicion, Movimiento, agar, Celda
from .colony import Colony
from .microorg import Microorganismo


class Petri:
    """
    Un plato de Petri es un recipiente poco profundo que los biólogos usan
    para cultivar células (bacterianas, animales, vegetales o fúngicas).

    No modificar esta clase directamente.
    @autor Diego (traducido a Python)
    """

    def __init__(self, radius: int, dist: int, selected_cols: List[int], microorg_classes: Dict[int, Type[Microorganismo]]):
        self.radius: int = radius
        self.max_x: int = 2 * radius
        self.max_y: int = 2 * radius
        self.dx: int = 0  # dirección del desplazamiento de nutrientes
        self.dy: int = 0
        self.dist_n: int = dist  # distribución de nutrientes actual
        self.t: int = 0  # contador de tiempo
        self.max_tx_col: float = PROD_X_COL / 1e6  # tiempo máximo por movimiento de colonia

        self.colonies: List[Colony] = []
        self.alives: List[Posicion] = []
        self.microorg_classes = microorg_classes

        random.seed(int(time.time()))

        # Crear la matriz de celdas
        agar.celdas = [[Celda() for _ in range(self.max_y)] for _ in range(self.max_x)]
        agar.mx_x = self.max_x
        agar.mx_y = self.max_y

        # Inicializar celdas
        for x in range(self.max_x):
            for y in range(self.max_y):
                agar.celdas[x][y].id_mo = VACIO

        # Crear colonias
        for c in range(N_COL):
            self.add_colony(radius, selected_cols[c])

        # Asignar posiciones y energías iniciales
        for c in range(N_COL):
            mo = 0
            while mo < MOS_INICIAL:
                pos = Posicion(random.randint(0, self.max_x - 1),
                               random.randint(0, self.max_y - 1))
                if self.is_in_dish(pos):
                    if agar.celdas[pos.x][pos.y].id_mo == VACIO:
                        self.create_mo(pos, c + 1, E_INICIAL)
                        mo += 1

        # Calcular la distribución de nutrientes
        self.dist_n = dist
        total_nutri = 0.0

        for x in range(self.max_x):
            for y in range(self.max_y):
                nutrient_value = self.calculate_nutrients(x, y, dist)
                agar.celdas[x][y].nutrientes = nutrient_value
                total_nutri += nutrient_value

        print(f"Total de nutrientes: {total_nutri}")

        agar.dist_n = self.dist_n
        agar.rx = random.randint(0, self.max_x - 1) - self.max_x // 2
        agar.ry = random.randint(0, self.max_y - 1) - self.max_y // 2
        self.dx = random.randint(-1, 1)
        self.dy = random.randint(-1, 1)

    def calculate_nutrients(self, x: int, y: int, dist: int) -> float:
        """Calcula la cantidad de nutrientes según el tipo de distribución"""
        max_x, max_y = self.max_x, self.max_y

        if dist == 1:  # Plano inclinado
            return MAX_NUTRI * (max_x - x) * (max_y - y) / (max_x * max_y) / 2.875
        elif dist == 2:  # Barra vertical
            return MAX_NUTRI / 4.2 if max_x // 2 - 5 < x < max_x // 2 + 5 else 0.0
        elif dist == 3:  # Anillo
            center_x, center_y = 0.5 * max_x, 0.5 * max_y
            dist_from_center = (x - center_x) ** 2 + (y - center_y) ** 2
            return MAX_NUTRI / 1.008 if 40 < dist_from_center < 115 else 0.0
        elif dist == 4:  # Rejilla (lattice)
            if (x + y) % (max_x // 4) <= 1 or (y - x) % (max_x // 3) <= 1:
                return MAX_NUTRI * (max_x - x) * (max_y - y) / (max_x * max_y) * 1.277
            return 0.0
        elif dist == 5:  # Dos gaussianas
            term1 = math.exp(-((x - 0.6 * max_x / 2) / (max_x / 8)) ** 2 - ((y - 0.6 * max_y / 2) / (max_y / 8)) ** 2)
            term2 = math.exp(-((x - 1.4 * max_x / 2) / (max_x / 8)) ** 2 - ((y - 1.4 * max_y / 2) / (max_y / 8)) ** 2)
            return MAX_NUTRI * (term1 + term2)
        elif dist == 6:  # Hambruna (uniforme)
            return MAX_NUTRI / 11.062
        else:
            return 0.0

    def __del__(self):
        """Destructor"""
        try:
            if hasattr(self, 'colonies'):
                for colony in self.colonies:
                    del colony
        except (AttributeError, TypeError):
            # Ignorar errores de limpieza durante la recolección de basura
            pass

    def move_colonies(self) -> None:
        """Aplicar reglas de la vida y avanzar las colonias"""
        self.t += 1

        # Construir vector con las posiciones de organismos vivos
        n_mos = sum(colony.n_alives() for colony in self.colonies)
        self.alives = []

        for x in range(self.max_x):
            for y in range(self.max_y):
                if agar.celdas[x][y].id_mo != VACIO:
                    self.alives.append(Posicion(x, y))

        # Vector para recorrer aleatoriamente todos los organismos vivos
        initial_count = len(self.alives)
        rand_indices = list(range(initial_count))
        random.shuffle(rand_indices)

        # Bucle principal de reglas
        for m in range(initial_count):
            if m >= len(rand_indices):
                break
            rm = rand_indices[m]
            if rm >= len(self.alives):
                continue  # Saltar este organismo, murió

            x, y = self.alives[rm].x, self.alives[rm].y
            id_mo = agar.celdas[x][y].id_mo

            if id_mo != VACIO:  # Podría haber muerto en combate con otro MO previo
                c = id_mo - 1  # índice de colonia
                xr = (x + agar.rx) % self.max_x
                yr = (y + agar.ry) % self.max_y

                # Comer en la posición actual
                nutrient_consumption = 0.01 * agar.celdas[xr][yr].nutrientes
                agar.celdas[x][y].energia_mo += nutrient_consumption
                agar.celdas[xr][yr].nutrientes -= nutrient_consumption
                if agar.celdas[xr][yr].nutrientes < 0:
                    agar.celdas[xr][yr].nutrientes = 0.0

                # Restar energía por vivir
                agar.celdas[x][y].energia_mo -= E_VIVIR

                # Pedir al MO que ejecute una iteración de vida
                if c < len(self.colonies):
                    self.colonies[c].live(x, y)

                    # Restar energía por moverse
                    if self.colonies[c].moved(x, y):
                        agar.celdas[x][y].energia_mo -= E_MOVERSE

                    # Verificar si murió
                    old = Posicion(x, y)
                    if agar.celdas[x][y].energia_mo <= 0:
                        self.kill_mo(old)
                    else:
                        # Si quiere reproducirse
                        if self.colonies[c].duplicate(x, y):
                            self.mitosis(old)

                        # Movimiento o competencia
                        if self.colonies[c].moved(x, y):
                            neu = Posicion(0, 0)
                            if self.can_move(old, self.colonies[c].mov(x, y), neu):
                                if agar.celdas[neu.x][neu.y].id_mo == VACIO:
                                    self.move_mo(old, neu)
                                else:
                                    if agar.celdas[neu.x][neu.y].id_mo != id_mo:
                                        self.compite(old, neu)

        # Mover nutrientes
        if self.t % 10 < 5:
            if self.t % 6 == 0:
                self.dx = random.randint(-1, 1)
                self.dy = random.randint(-1, 1)
            agar.rx += self.dx
            agar.ry += self.dy

    def colony_name(self, id: int) -> str:
        """Obtener el nombre de la colonia"""
        return self.colonies[(id - 1) % N_COL].name()

    # Aliases en español para compatibilidad y gradual migración
    def nombre_colonia(self, id: int) -> str:
        """Alias en español de colony_name (compatibilidad)."""
        return self.colony_name(id)

    def author_name(self, id: int) -> str:
        """Obtener el nombre del autor"""
        return self.colonies[(id - 1) % N_COL].author()

    def autor_colonia(self, id: int) -> str:
        """Alias en español de author_name (compatibilidad)."""
        return self.author_name(id)

    def can_move(self, old: Posicion, mov: Movimiento, neu: Posicion) -> bool:
        """Verificar si el movimiento es válido"""
        neu.x = old.x
        neu.y = old.y

        pos = Posicion(old.x + mov.dx, old.y + mov.dy)
        if self.is_in_dish(pos):
            if mov.dx > 0:
                neu.x = old.x + 1
            elif mov.dx < 0:
                neu.x = old.x - 1
            if mov.dy > 0:
                neu.y = old.y + 1
            elif mov.dy < 0:
                neu.y = old.y - 1
            return True
        return False

    def is_in_dish(self, pos: Posicion) -> bool:
        """Verificar si una posición está dentro del plato de Petri"""
        x, y, r = pos.x, pos.y, self.radius
        return (r - x) * (r - x) + (r - y) * (r - y) < r * r

    def compite(self, old: Posicion, neu: Posicion) -> None:
        """Combate entre dos microorganismos"""
        ener1 = agar.celdas[old.x][old.y].energia_mo
        ener2 = agar.celdas[neu.x][neu.y].energia_mo

        # Si tienen la misma energía, elegir ganador al azar
        if ener2 == ener1:
            ener2 += 0.01 if random.random() > 0.5 else -0.01

        # Definir ganador y perdedor
        if ener2 > ener1:
            win, los = neu, old
        else:
            win, los = old, neu

        # Actualizar energías
        diff = abs(ener2 - ener1)
        # El ganador gana un porcentaje de la energía del perdedor
        agar.celdas[win.x][win.y].energia_mo += 0.075 * agar.celdas[los.x][los.y].energia_mo
        # El perdedor pierde la diferencia de energía
        agar.celdas[los.x][los.y].energia_mo -= diff

        # Si el perdedor queda con energía negativa, muere
        if agar.celdas[los.x][los.y].energia_mo <= 0:
            self.kill_mo(los)

    def mitosis(self, pos: Posicion) -> None:
        """Mitosis (división celular)"""
        # Buscar lugar vacío alrededor (aleatoriamente)
        directions = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]
        random.shuffle(directions)

        place_found = False
        for dx, dy in directions:
            neu = Posicion(pos.x + dx, pos.y + dy)
            if self.is_in_dish(neu):
                if agar.celdas[neu.x][neu.y].id_mo == VACIO:
                    place_found = True
                    ener1 = agar.celdas[pos.x][pos.y].energia_mo
                    ener = ener1 * 0.5 - ener1 * 0.01  # Mitad menos 1%
                    agar.celdas[pos.x][pos.y].energia_mo = ener  # Reducir energía del progenitor
                    self.create_mo(neu, agar.celdas[pos.x][pos.y].id_mo, ener)
                    break

    def create_mo(self, pos: Posicion, id: int, ener: float) -> None:
        """Crear microorganismo"""
        agar.celdas[pos.x][pos.y].id_mo = id
        agar.celdas[pos.x][pos.y].energia_mo = ener

        # Notificar a la colonia
        if id - 1 < len(self.colonies):
            self.colonies[id - 1].create(pos.x, pos.y)

    def move_mo(self, old: Posicion, neu: Posicion) -> None:
        """Mover microorganismo"""
        id_mo = agar.celdas[old.x][old.y].id_mo

        # Copiar a la nueva posición
        agar.celdas[neu.x][neu.y].id_mo = agar.celdas[old.x][old.y].id_mo
        agar.celdas[neu.x][neu.y].energia_mo = agar.celdas[old.x][old.y].energia_mo

        # Vaciar la posición anterior
        agar.celdas[old.x][old.y].id_mo = VACIO
        agar.celdas[old.x][old.y].energia_mo = 0.0

        # Notificar a la colonia
        if id_mo - 1 < len(self.colonies):
            self.colonies[id_mo - 1].move(old, neu)

    def kill_mo(self, pos: Posicion) -> None:
        """Eliminar microorganismo"""
        id_mo = agar.celdas[pos.x][pos.y].id_mo

        # Vaciar la celda
        agar.celdas[pos.x][pos.y].id_mo = VACIO
        agar.celdas[pos.x][pos.y].energia_mo = 0.0

        # Notificar a la colonia
        if id_mo - 1 < len(self.colonies):
            self.colonies[id_mo - 1].kill(pos.x, pos.y)

    def add_colony(self, radius: int, selected_col: int) -> None:
        """Agregar una colonia del tipo especificado"""
        id_colony = len(self.colonies) + 1

        if selected_col in self.microorg_classes:
            colony = Colony(self.microorg_classes[selected_col], id_colony, radius)
            self.colonies.append(colony)
        else:
            print(f"Advertencia: Tipo de microorganismo {selected_col} no encontrado")