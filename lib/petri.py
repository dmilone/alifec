# =====================================================================
# PETRI: Simulación de una cápsula de Petri
# =====================================================================

import random
import math
import time
from typing import List, Dict, Type, Tuple
from .defs import *
from .agar import Posicion, Movimiento, agar, Celda
from .colonia import Colonia
from .microorg import Microorganismo


class Petri:
    """
    Una cápsula de Petri es un recipiente poco profundo que los biólogos usan
    para cultivar células (bacterianas, animales, vegetales o fúngicas).

    No modificar esta clase directamente.
    @autor Diego (traducido a Python también por Diego)
    """

    def __init__(self, radius: int, dist: int, selected_cols: List[int], microorg_classes: Dict[int, Type[Microorganismo]]):
        # Dimensiones
        self.radio: int = radius
        self.max_x: int = 2 * radius
        self.max_y: int = 2 * radius

        # Desplazamiento de nutrientes (x,y)
        self.despl_x: int = 0
        self.despl_y: int = 0

        # Distribución y tiempo
        self.dist_n: int = dist  # distribución de nutrientes actual
        self.tiempo: int = 0  # contador de tiempo
        self.max_tx_col: float = PROD_X_COL / 1e6  # tiempo máximo por movimiento de colonia

        # Estructuras principales
        self.colonias: List[Colonia] = []
        self.vivos: List[Posicion] = []
        self.clases_microorg = microorg_classes
        

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
            self.agregar_colonia(radius, selected_cols[c])

        # Asignar posiciones y energías iniciales
        for c in range(N_COL):
            mo = 0
            while mo < MOS_INICIAL:
                pos = Posicion(random.randint(0, self.max_x - 1),
                               random.randint(0, self.max_y - 1))
                if self.esta_en_plato(pos):
                    if agar.celdas[pos.x][pos.y].id_mo == VACIO:
                        self.crear_mo(pos, c + 1, E_INICIAL)
                        mo += 1

        # Calcular la distribución de nutrientes
        self.dist_n = dist
        total_nutri = 0.0

        for x in range(self.max_x):
            for y in range(self.max_y):
                nutrient_value = self.calcular_nutrientes(x, y, dist)
                agar.celdas[x][y].nutrientes = nutrient_value
                total_nutri += nutrient_value

        print(f"Total de nutrientes: {total_nutri}")

        agar.dist_n = self.dist_n
        agar.rx = random.randint(0, self.max_x - 1) - self.max_x // 2
        agar.ry = random.randint(0, self.max_y - 1) - self.max_y // 2
        self.dx = random.randint(-1, 1)
        self.dy = random.randint(-1, 1)

    def calcular_nutrientes(self, x: int, y: int, dist: int) -> float:
        """Calcula la cantidad de nutrientes según el tipo de distribución (castellano)."""
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
            if hasattr(self, 'colonias'):
                for colony in self.colonias:
                    del colony
        except (AttributeError, TypeError):
            # Ignorar errores de limpieza durante la recolección de basura
            pass

    # Nota: eliminados aliases en inglés. Usar los métodos en castellano.

    def mover_colonias(self) -> None:
        """Aplicar reglas de la vida y avanzar las colonias (nombres en castellano)."""
        # Avanzar tiempo
        self.tiempo += 1

        # Construir vector con las posiciones de organismos vivos
        n_mos = sum(col.n_vivos() for col in self.colonias)
        self.vivos = []

        for x in range(self.max_x):
            for y in range(self.max_y):
                if agar.celdas[x][y].id_mo != VACIO:
                    self.vivos.append(Posicion(x, y))

        # Vector para recorrer aleatoriamente todos los organismos vivos
        initial_count = len(self.vivos)
        rand_indices = list(range(initial_count))
        random.shuffle(rand_indices)

        # Bucle principal de reglas
        for m in range(initial_count):
            if m >= len(rand_indices):
                break
            rm = rand_indices[m]
            if rm >= len(self.vivos):
                continue  # Saltar este organismo, murió

            x, y = self.vivos[rm].x, self.vivos[rm].y
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
                if c < len(self.colonias):
                    # Iteración de vida usando API en castellano
                    self.colonias[c].vivir(x, y)

                    # Restar energía por moverse
                    if self.colonias[c].movio(x, y):
                        agar.celdas[x][y].energia_mo -= E_MOVERSE

                    # Verificar si murió
                    old = Posicion(x, y)
                    if agar.celdas[x][y].energia_mo <= 0:
                        self.eliminar_mo(old)
                    else:
                        # Si quiere reproducirse
                        if self.colonias[c].duplica(x, y):
                            self.mitosis(old)

                        # Movimiento o competencia
                        if self.colonias[c].movio(x, y):
                            neu = Posicion(0, 0)
                            if self.puede_mover(old, self.colonias[c].movimiento(x, y), neu):
                                        if agar.celdas[neu.x][neu.y].id_mo == VACIO:
                                            self.mover_mo(old, neu)
                                        else:
                                            if agar.celdas[neu.x][neu.y].id_mo != id_mo:
                                                self.competir(old, neu)

        # Mover nutrientes
        if self.tiempo % 10 < 5:
            if self.tiempo % 6 == 0:
                self.dx = random.randint(-1, 1)
                self.dy = random.randint(-1, 1)
            agar.rx += self.dx
            agar.ry += self.dy

    def nombre_colonia(self, id: int) -> str:
        """Obtener el nombre de la colonia (nombre en castellano)."""
        # Las colonias ahora exponen `nombre()` (Colonia.nombre)
        return self.colonias[(id - 1) % N_COL].nombre()

    def autor_colonia(self, id: int) -> str:
        """Obtener el nombre del autor (en castellano)."""
        return self.colonias[(id - 1) % N_COL].autor()

    def puede_mover(self, old: Posicion, mov: Movimiento, neu: Posicion) -> bool:
        """Verificar si el movimiento es válido (nombre en castellano)."""
        neu.x = old.x
        neu.y = old.y

        pos = Posicion(old.x + mov.dx, old.y + mov.dy)
        if self.esta_en_plato(pos):
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

    def esta_en_plato(self, pos: Posicion) -> bool:
        """Verificar si una posición está dentro del plato de Petri (castellano)."""
        x, y, r = pos.x, pos.y, self.radio
        return (r - x) * (r - x) + (r - y) * (r - y) < r * r

    def competir(self, old: Posicion, neu: Posicion) -> None:
        """Combate entre dos microorganismos (nombre en castellano)."""
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
            self.eliminar_mo(los)

    def mitosis(self, pos: Posicion) -> None:
        """Mitosis (división celular)"""
        # Buscar lugar vacío alrededor (aleatoriamente)
        directions = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]
        random.shuffle(directions)

        place_found = False
        for dx, dy in directions:
            neu = Posicion(pos.x + dx, pos.y + dy)
            if self.esta_en_plato(neu):
                if agar.celdas[neu.x][neu.y].id_mo == VACIO:
                    place_found = True
                    ener1 = agar.celdas[pos.x][pos.y].energia_mo
                    ener = ener1 * 0.5 - ener1 * 0.01  # Mitad menos 1%
                    agar.celdas[pos.x][pos.y].energia_mo = ener  # Reducir energía del progenitor
                    self.crear_mo(neu, agar.celdas[pos.x][pos.y].id_mo, ener)
                    break

    def crear_mo(self, pos: Posicion, id: int, ener: float) -> None:
        """Crear microorganismo (nombre en castellano)."""
        agar.celdas[pos.x][pos.y].id_mo = id
        agar.celdas[pos.x][pos.y].energia_mo = ener

        # Notificar a la colonia
        if id - 1 < len(self.colonias):
            self.colonias[id - 1].crear(pos.x, pos.y)

    def mover_mo(self, old: Posicion, neu: Posicion) -> None:
        """Mover microorganismo (castellano)."""
        id_mo = agar.celdas[old.x][old.y].id_mo

        # Copiar a la nueva posición
        agar.celdas[neu.x][neu.y].id_mo = agar.celdas[old.x][old.y].id_mo
        agar.celdas[neu.x][neu.y].energia_mo = agar.celdas[old.x][old.y].energia_mo

        # Vaciar la posición anterior
        agar.celdas[old.x][old.y].id_mo = VACIO
        agar.celdas[old.x][old.y].energia_mo = 0.0

        # Notificar a la colonia
        if id_mo - 1 < len(self.colonias):
            self.colonias[id_mo - 1].mover(old, neu)

    def eliminar_mo(self, pos: Posicion) -> None:
        """Eliminar microorganismo (castellano)."""
        id_mo = agar.celdas[pos.x][pos.y].id_mo

        # Vaciar la celda
        agar.celdas[pos.x][pos.y].id_mo = VACIO
        agar.celdas[pos.x][pos.y].energia_mo = 0.0

        # Notificar a la colonia
        if id_mo - 1 < len(self.colonias):
            self.colonias[id_mo - 1].eliminar(pos.x, pos.y)

    def agregar_colonia(self, radius: int, selected_col: int) -> None:
        """Agregar una colonia del tipo especificado (castellano)."""
        id_colony = len(self.colonias) + 1

        if selected_col in self.clases_microorg:
            colony = Colonia(self.clases_microorg[selected_col], id_colony, radius)
            self.colonias.append(colony)
        else:
            print(f"Advertencia: Tipo de microorganismo {selected_col} no encontrado")
