# =====================================================================
# PETRI: A Petri dish simulation for artificial life contests
# Translated from C++ to Python
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
    A Petri dish is a shallow glass or plastic cylindrical dish that biologists
    use to culture cells, which can be bacterial, animal, plant, or fungus.

    Don't modify this class!
    @author Diego (translated to Python)
    """
    
    def __init__(self, radius: int, dist: int, selected_cols: List[int], microorg_classes: Dict[int, Type[Microorganismo]]):
        self.radius: int = radius
        self.max_x: int = 2 * radius
        self.max_y: int = 2 * radius
        self.dx: int = 0  # direction of nutrient movement
        self.dy: int = 0
        self.dist_n: int = dist  # current nutrient distribution
        self.t: int = 0  # time counter
        self.max_tx_col: float = PROD_X_COL / 1e6  # max time per colony move
        
        self.colonies: List[Colony] = []
        self.alives: List[Posicion] = []
        self.microorg_classes = microorg_classes
        
        random.seed(int(time.time()))
        
        # Create cells matrix
        agar.celdas = [[Celda() for _ in range(self.max_y)] for _ in range(self.max_x)]
        agar.mx_x = self.max_x
        agar.mx_y = self.max_y
        
        # Initialize cells
        for x in range(self.max_x):
            for y in range(self.max_y):
                agar.celdas[x][y].id_mo = VACIO
                
        # Create colonies
        for c in range(N_COL):
            self.add_colony(radius, selected_cols[c])
            
        # Set initial positions and energies
        for c in range(N_COL):
            mo = 0
            while mo < MOS_INICIAL:
                pos = Posicion(random.randint(0, self.max_x - 1), 
                              random.randint(0, self.max_y - 1))
                if self.is_in_dish(pos):
                    if agar.celdas[pos.x][pos.y].id_mo == VACIO:
                        self.create_mo(pos, c + 1, E_INICIAL)
                        mo += 1
                        
        # Set nutrients distribution
        self.dist_n = dist
        total_nutri = 0.0
        
        for x in range(self.max_x):
            for y in range(self.max_y):
                nutrient_value = self.calculate_nutrients(x, y, dist)
                agar.celdas[x][y].nutrientes = nutrient_value
                total_nutri += nutrient_value
                
        print(f"Total of nutrients: {total_nutri}")
        
        agar.dist_n = self.dist_n
        agar.rx = random.randint(0, self.max_x - 1) - self.max_x // 2
        agar.ry = random.randint(0, self.max_y - 1) - self.max_y // 2
        self.dx = random.randint(-1, 1)
        self.dy = random.randint(-1, 1)
        
    def calculate_nutrients(self, x: int, y: int, dist: int) -> float:
        """Calculate nutrient distribution based on distribution type"""
        max_x, max_y = self.max_x, self.max_y
        
        if dist == 1:  # Inclined plane
            return MAX_NUTRI * (max_x - x) * (max_y - y) / (max_x * max_y) / 2.875
        elif dist == 2:  # Vertical bar
            return MAX_NUTRI / 4.2 if max_x//2 - 5 < x < max_x//2 + 5 else 0.0
        elif dist == 3:  # Ring
            center_x, center_y = 0.5 * max_x, 0.5 * max_y
            dist_from_center = (x - center_x)**2 + (y - center_y)**2
            return MAX_NUTRI / 1.008 if 40 < dist_from_center < 115 else 0.0
        elif dist == 4:  # Lattice
            if (x + y) % (max_x // 4) <= 1 or (y - x) % (max_x // 3) <= 1:
                return MAX_NUTRI * (max_x - x) * (max_y - y) / (max_x * max_y) * 1.277
            return 0.0
        elif dist == 5:  # Two gaussians
            term1 = math.exp(-((x - 0.6*max_x/2)/(max_x/8))**2 - ((y - 0.6*max_y/2)/(max_y/8))**2)
            term2 = math.exp(-((x - 1.4*max_x/2)/(max_x/8))**2 - ((y - 1.4*max_y/2)/(max_y/8))**2)
            return MAX_NUTRI * (term1 + term2)
        elif dist == 6:  # Famine (uniform)
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
            # Ignore cleanup errors during garbage collection
            pass
            
    def move_colonies(self) -> None:
        """Apply rules of life and move colonies"""
        self.t += 1
        
        # Build vector with positions of living organisms
        n_mos = sum(colony.n_alives() for colony in self.colonies)
        self.alives = []
        
        for x in range(self.max_x):
            for y in range(self.max_y):
                if agar.celdas[x][y].id_mo != VACIO:
                    self.alives.append(Posicion(x, y))
                    
        # Vector to randomly traverse all living organisms
        initial_count = len(self.alives)
        rand_indices = list(range(initial_count))
        random.shuffle(rand_indices)
        
        # Main rules loop
        for m in range(initial_count):
            if m >= len(rand_indices):
                break
            rm = rand_indices[m]
            if rm >= len(self.alives):
                continue  # Skip this organism, it died
                
            x, y = self.alives[rm].x, self.alives[rm].y
            id_mo = agar.celdas[x][y].id_mo
            
            if id_mo != VACIO:  # Could have died in combat with previous MO
                    c = id_mo - 1  # colony index
                    xr = (x + agar.rx) % self.max_x
                    yr = (y + agar.ry) % self.max_y
                    
                    # Eat from current position
                    nutrient_consumption = 0.01 * agar.celdas[xr][yr].nutrientes
                    agar.celdas[x][y].energia_mo += nutrient_consumption
                    agar.celdas[xr][yr].nutrientes -= nutrient_consumption
                    if agar.celdas[xr][yr].nutrientes < 0:
                        agar.celdas[xr][yr].nutrientes = 0.0
                        
                    # Subtract energy for living
                    agar.celdas[x][y].energia_mo -= E_VIVIR
                    
                    # Ask MO to make a life iteration
                    if c < len(self.colonies):
                        self.colonies[c].live(x, y)
                        
                        # Subtract energy for moving
                        if self.colonies[c].moved(x, y):
                            agar.celdas[x][y].energia_mo -= E_MOVERSE
                            
                        # Check if it died
                        old = Posicion(x, y)
                        if agar.celdas[x][y].energia_mo <= 0:
                            self.kill_mo(old)
                        else:
                            # If it wants to reproduce
                            if self.colonies[c].duplicate(x, y):
                                self.mitosis(old)
                                
                            # Movement or competition
                            if self.colonies[c].moved(x, y):
                                neu = Posicion(0, 0)
                                if self.can_move(old, self.colonies[c].mov(x, y), neu):
                                    if agar.celdas[neu.x][neu.y].id_mo == VACIO:
                                        self.move_mo(old, neu)
                                    else:
                                        if agar.celdas[neu.x][neu.y].id_mo != id_mo:
                                            self.compite(old, neu)
                                            
        # Move nutrients
        if self.t % 10 < 5:
            if self.t % 6 == 0:
                self.dx = random.randint(-1, 1)
                self.dy = random.randint(-1, 1)
            agar.rx += self.dx
            agar.ry += self.dy
            
    def colony_name(self, id: int) -> str:
        """Get colony name"""
        return self.colonies[(id - 1) % N_COL].name()
        
    def author_name(self, id: int) -> str:
        """Get author name"""
        return self.colonies[(id - 1) % N_COL].author()
        
    def can_move(self, old: Posicion, mov: Movimiento, neu: Posicion) -> bool:
        """Check if movement is valid"""
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
        """Check if position is inside the petri dish"""
        x, y, r = pos.x, pos.y, self.radius
        return (r - x) * (r - x) + (r - y) * (r - y) < r * r
        
    def compite(self, old: Posicion, neu: Posicion) -> None:
        """Combat between two microorganisms"""
        ener1 = agar.celdas[old.x][old.y].energia_mo
        ener2 = agar.celdas[neu.x][neu.y].energia_mo
        
        # If same energy, random winner
        if ener2 == ener1:
            ener2 += 0.01 if random.random() > 0.5 else -0.01
            
        # Define winner and loser
        if ener2 > ener1:
            win, los = neu, old
        else:
            win, los = old, neu
            
        # Update energies
        diff = abs(ener2 - ener1)
        # Winner gains percentage of loser's energy
        agar.celdas[win.x][win.y].energia_mo += 0.075 * agar.celdas[los.x][los.y].energia_mo
        # Loser loses energy difference
        agar.celdas[los.x][los.y].energia_mo -= diff
        
        # If loser has negative energy, it dies
        if agar.celdas[los.x][los.y].energia_mo <= 0:
            self.kill_mo(los)
            
    def mitosis(self, pos: Posicion) -> None:
        """Cell division"""
        # Look for empty place around (randomly)
        directions = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]
        random.shuffle(directions)
        
        place_found = False
        for dx, dy in directions:
            neu = Posicion(pos.x + dx, pos.y + dy)
            if self.is_in_dish(neu):
                if agar.celdas[neu.x][neu.y].id_mo == VACIO:
                    place_found = True
                    ener1 = agar.celdas[pos.x][pos.y].energia_mo
                    ener = ener1 * 0.5 - ener1 * 0.01  # Half minus 1%
                    agar.celdas[pos.x][pos.y].energia_mo = ener  # Reduce parent energy
                    self.create_mo(neu, agar.celdas[pos.x][pos.y].id_mo, ener)
                    break
                    
    def create_mo(self, pos: Posicion, id: int, ener: float) -> None:
        """Create microorganism"""
        agar.celdas[pos.x][pos.y].id_mo = id
        agar.celdas[pos.x][pos.y].energia_mo = ener
        
        # Notify colony
        if id - 1 < len(self.colonies):
            self.colonies[id - 1].create(pos.x, pos.y)
            
    def move_mo(self, old: Posicion, neu: Posicion) -> None:
        """Move microorganism"""
        id_mo = agar.celdas[old.x][old.y].id_mo
        
        # Copy to new position
        agar.celdas[neu.x][neu.y].id_mo = agar.celdas[old.x][old.y].id_mo
        agar.celdas[neu.x][neu.y].energia_mo = agar.celdas[old.x][old.y].energia_mo
        
        # Clear old position
        agar.celdas[old.x][old.y].id_mo = VACIO
        agar.celdas[old.x][old.y].energia_mo = 0.0
        
        # Notify colony
        if id_mo - 1 < len(self.colonies):
            self.colonies[id_mo - 1].move(old, neu)
            
    def kill_mo(self, pos: Posicion) -> None:
        """Kill microorganism"""
        id_mo = agar.celdas[pos.x][pos.y].id_mo
        
        # Empty cell
        agar.celdas[pos.x][pos.y].id_mo = VACIO
        agar.celdas[pos.x][pos.y].energia_mo = 0.0
        
        # Notify colony
        if id_mo - 1 < len(self.colonies):
            self.colonies[id_mo - 1].kill(pos.x, pos.y)
            
    def add_colony(self, radius: int, selected_col: int) -> None:
        """Add a colony of the specified type"""
        id_colony = len(self.colonies) + 1
        
        if selected_col in self.microorg_classes:
            colony = Colony(self.microorg_classes[selected_col], id_colony, radius)
            self.colonies.append(colony)
        else:
            print(f"Warning: Microorganism type {selected_col} not found")