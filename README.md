# Artificial Life Contest

The framework provides the main rules of the game, a visualization interface using matplotlib, and examples of elementary microorganisms. The central idea of this project is the development of the environment, while users develop their own microorganisms to compete for survival in a common environment. All created microorganisms must compete for survival in a common petri dish. The colony that dominates the others and accumulates the most living energy wins the tournament.



## Requirements

- Python 3.7+
- matplotlib
- numpy

### Option 1: Using conda (recommended)
```bash
conda env create -f environment.yml
conda activate alife
```

### Option 2: Using pip
```bash
pip install matplotlib numpy
```

## Usage

Run a simulation with two microorganism colonies:

```bash
python comvida.py --dist 4 --colonies 0 1
```

### Command line options

- `--dist, -d`: Nutrient distribution pattern (1-6)
  - 1: Inclined plane
  - 2: Vertical bar
  - 3: Ring
  - 4: Lattice
  - 5: Two gaussians
  - 6: Famine (uniform)

- `--colonies, -c`: List of microorganism types to compete (space-separated numbers)

### Simple examples of microorganisms

- **0: Aleatorio** - Random movement (by Compu2)
- **1: BuscaN** - Nutrient seeker (by Compu2)
- **2: MOmm** - Always moves diagonally down-left (by Compu2)
- **3: MOpp** - Always moves diagonally up-right (by Compu2)
- **4: MOxx** - Moves horizontally towards food (by Compu2)
- **5: MOyy** - Moves vertically towards food (by Compu2)
- **6: Tacticas1** - Strategic: kill→eat→reproduce (by Compu2)
- **7: Tacticas2** - Strategic: eat→kill→reproduce (by Compu2)

## Contest examples

```bash
# Simple random vs nutrient-seeker
python comvida.py --dist 1 --colonies 0 1

# Strategic battle
python comvida.py --dist 5 --colonies 6 7

```

## Project structure

```
alifec/
├── lib/                    # Core simulation classes
│   ├── defs.py            # Constants and definitions
│   ├── agar.py            # Petri dish environment
│   ├── microorg.py        # Abstract microorganism base class
│   ├── colony.py          # Colony management
│   ├── petri.py           # Main simulation engine
│   └── grapher.py         # Visualization (matplotlib)
├── mos/                   # Microorganism implementations
│   ├── aleatorio.py       # Random movement
│   ├── buscan.py          # Nutrient seeker
│   ├── momm.py            # Diagonal down-left
│   ├── mopp.py            # Diagonal up-right
│   ├── moxx.py            # Horizontal food seeker
│   ├── moyy.py            # Vertical food seeker
│   ├── tacticas1.py       # Strategic type 1
│   └── tacticas2.py       # Strategic type 2
├── results/               # Contest results and rankings
│   ├── contests_YYMMDD.yml  # Daily contest results
│   ├── ranking_YYMMDD.txt   # Daily rankings  
│   ├── global_ranking.txt   # Global rankings
│   └── bkp/                 # Ranking backups
└── comvida.py            # Main program entry point
```

## Creating new microorganisms

1. Create a new Python file in the `mos/` directory
2. Inherit from `Microorganismo` class
3. Implement required methods:
   - `nombre()`: Return microorganism name
   - `autor()`: Return author name  
   - `move(mov)`: Define movement strategy
   - `mitosis()`: Define reproduction strategy

Example:
```python
from ..lib.microorg import Microorganismo
from ..lib.agar import Movimiento

class MyMicroorganism(Microorganismo):
    def nombre(self) -> str:
        return "My Organism"
        
    def autor(self) -> str:
        return "Your Name"
        
    def move(self, mov: Movimiento) -> None:
        # Your movement logic here
        mov.dx = 1  # Move right
        mov.dy = 0  # Don't move vertically
        
    def mitosis(self) -> bool:
        return self.ene > 1000  # Reproduce if energy > 1000
```

4. The system will automatically discover the new microorganism

## Simulation rules

- Microorganisms start with initial energy
- Each time step costs energy for living
- Moving costs additional energy
- Microorganisms can consume nutrients from their environment
- Combat occurs when microorganisms occupy the same space
- Reproduction (mitosis) is possible when energy is sufficient
- The simulation continues until one colony dominates or time limit is reached

## Visualization

The simulation displays:
- **Left panel**: Petri dish with microorganisms (red/blue dots) and nutrients (background color)
- **Right panel**: Real-time statistics showing energy levels and population counts over time

## Contest system

- **Dynamic Discovery**: Microorganisms are automatically discovered from the `mos/` folder
- **Automatic Results**: Contest results are automatically saved to `results/contests_YYMMDD.yml`
- **Daily Rankings**: Daily rankings are generated as `results/ranking_YYMMDD.txt`
- **Global Rankings**: Use `--update-global filename.txt` to create comprehensive rankings


