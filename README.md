# COMpetencia de VIDa Artificial

El marco provee las reglas principales del juego, una interfaz de visualización con matplotlib y ejemplos de microorganismos elementales. La idea central es el desarrollo del entorno; los usuarios crean sus propios microorganismos para competir por la supervivencia en un mismo ambiente. Todas las criaturas compiten en un mismo plato de Petri. La colonia que domine a las demás y acumule más energía viviente gana el concurso.


## Requisitos

- Python 3.7+
- matplotlib
- numpy

### Opción 1: Usando conda (recomendado)
```bash
conda env create -f environment.yml
conda activate alife
```

### Opción 2: Usando pip
```bash
pip install matplotlib numpy
```

## Uso

Ejecutar una simulación entre dos colonias de microorganismos:

```bash
python comvida.py --dist 4 --colonies 0 1
```

### Opciones de línea de comandos

- `--dist, -d`: Patrón de distribución de nutrientes (1-6)
  - 1: Plano inclinado
  - 2: Barra vertical
  - 3: Anillo
  - 4: Lattice (rejilla)
  - 5: Dos gaussianas
  - 6: Hambruna (uniforme)

- `--colonies, -c`: Lista de tipos de microorganismos a competir (números separados por espacios)

### Ejemplos simples de microorganismos

- **0: Aleatorio** - Movimiento aleatorio (por Compu2)
- **1: BuscaN** - Buscador de nutrientes (por Compu2)
- **2: MOmm** - Siempre se mueve en diagonal abajo-izquierda (por Compu2)
- **3: MOpp** - Siempre se mueve en diagonal arriba-derecha (por Compu2)
- **4: MOxx** - Se mueve horizontalmente hacia la comida (por Compu2)
- **5: MOyy** - Se mueve verticalmente hacia la comida (por Compu2)
- **6: Tacticas1** - Estratégico: matar→comer→reproducir (por Compu2)
- **7: Tacticas2** - Estratégico: comer→matar→reproducir (por Compu2)

## Ejemplos de competencia

```bash
# Aleatorio vs buscador de nutrientes
python comvida.py --dist 1 --colonies 0 1

# Batalla estratégica
python comvida.py --dist 5 --colonies 6 7

```

## Estructura del proyecto

```
alifec/
├── lib/                    # Clases principales de la simulación
│   ├── definiciones.py    # Constantes y definiciones (antes `defs.py`)
│   ├── agar.py            # Entorno (plato de Petri)
│   ├── microorganismo.py  # Clase base abstracta para microorganismos (API en castellano)
│   ├── colonia.py         # Gestión de colonias (API en castellano)
│   ├── petri.py           # Motor principal de la simulación (API en castellano)
│   └── graficacion.py     # Visualización (matplotlib) — clase principal: `Graficadora`
├── mos/                   # Implementaciones de microorganismos
│   ├── aleatorio.py       # Movimiento aleatorio
│   ├── buscan.py          # Buscador de nutrientes
│   ├── momm.py            # Diagonales abajo-izquierda
│   ├── mopp.py            # Diagonales arriba-derecha
│   ├── moxx.py            # Buscador horizontal
│   ├── moyy.py            # Buscador vertical
│   ├── tacticas1.py       # Implementación estratégica 1
│   └── tacticas2.py       # Implementación estratégica 2
├── resultados/            # Resultados de concursos y rankings
│   ├── competencias_YYMMDD.yml  # Resultados diarios de concursos
│   ├── ranking_YYMMDD.txt       # Rankings diarios
│   ├── global_ranking.txt       # Ranking global
│   └── bkp/                     # Backups de rankings
└── comvida.py            # Punto de entrada principal
```

## Crear nuevos microorganismos

1. Crear un nuevo archivo Python en el directorio `mos/`
3. Heredar de la clase `Microorganismo`
4. Implementar los métodos requeridos (API en castellano):
    - `nombre()`: Devuelve el nombre del microorganismo
    - `autor()`: Devuelve el nombre del autor
    - `decidir_movimiento(mov)`: Define la estrategia de movimiento (obligatorio)
    - `quiere_mitosis()`: Define la estrategia de reproducción (obligatorio)

Ejemplo (API en castellano):
```python
from ..lib.microorganismo import Microorganismo
from ..lib.agar import Movimiento

class MiMicroorganismo(Microorganismo):
    def nombre(self) -> str:
        return "Mi Organismo"
        
    def autor(self) -> str:
        return "Tu Nombre"
        
    def decidir_movimiento(self, mov: Movimiento) -> None:
        # Lógica de movimiento
        mov.dx = 1  # Mover a la derecha
        mov.dy = 0  # No moverse verticalmente
        
    def quiere_mitosis(self) -> bool:
        return self.ene > 1000  # Reproducir si la energía > 1000
```

Nota: desde esta versión la API pública de microorganismos es exclusivamente
en castellano. Implementa `decidir_movimiento` y `quiere_mitosis` en tus
microorganismos. Los nombres legacy en inglés han sido eliminados.

4. El sistema detectará automáticamente el nuevo microorganismo

## Reglas de la simulación

- Los microorganismos comienzan con energía inicial
- Cada paso de tiempo consume energía por vivir
- Moverse consume energía adicional
- Los microorganismos pueden consumir nutrientes del entorno
- Ocurre combate cuando dos microorganismos ocupan el mismo casillero
- La reproducción (mitosis) es posible cuando la energía es suficiente
- La simulación continúa hasta que una colonia domina o se alcanza el tiempo límite

## Visualización

La simulación muestra:
- **Panel izquierdo**: Plato de Petri con microorganismos (puntos rojo/azul) y nutrientes (color de fondo)
- **Panel derecho**: Estadísticas en tiempo real mostrando niveles de energía y recuento de poblaciones en el tiempo

## Sistema de concursos

- **Descubrimiento dinámico**: Los microorganismos se detectan automáticamente desde la carpeta `mos/`
- **Resultados automáticos**: Los resultados se guardan en `resultados/competencias_YYMMDD.yml`
 - **Rankings diarios**: Se generan como `resultados/ranking_YYMMDD.txt`.
- **Rankings globales**: Usar `--update-global filename.txt` para crear rankings globales

## Enlaces
- Repositorio GitHub: https://github.com/dmilone/alifec
- Proyecto original: https://sourceforge.net/projects/alifecontest/
