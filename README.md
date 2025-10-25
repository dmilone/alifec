# COMpetencia de VIDa Artificial

El marco provee las reglas principales del juego, una interfaz de visualización con matplotlib y ejemplos de microorganismos elementales. La idea central es el desarrollo del entorno; los usuarios crean sus propios microorganismos para competir por la supervivencia en un mismo ambiente. Todas las criaturas compiten en un mismo plato de Petri. La colonia que domine a las demás y acumule más energía viviente gana el concurso.


## Requisitos

- Python 3.7+
- matplotlib
- numpy

### Instalación

```bash
conda env create -f environment.yml
conda activate alife
```

## Uso

Ejecutar una simulación entre dos colonias de microorganismos:

```bash
python comvida.py --distribucion 4 --colonias 0 1
```

### Opciones de línea de comandos

- `--distribucion, -d`: Patrón de distribución de nutrientes (1-6)
  - 1: Plano inclinado
  - 2: Barra vertical
  - 3: Anillo
  - 4: Lattice (rejilla)
  - 5: Dos gaussianas
  - 6: Hambruna (uniforme)

- `--colonias, -c`: Lista de tipos de microorganismos a competir (números separados por espacios)
- `--listar-mos`: Lista todos los microorganismos disponibles y sale
- `--actualizar-global <archivo>`: Actualiza el ranking global combinando todos los resultados disponibles
- `--sin-grafico, --sin-graficos`: Ejecuta la simulación en modo sin gráficos (headless)

#### Listar microorganismos

```bash
python comvida.py --listar-mos
```

### Ejemplos simples de microorganismos

- **0: Aleatorio** - Movimiento aleatorio (por Compu2)
- **1: BuscaN** - Buscador de nutrientes (por Compu2)
- **2: MOmm** - Siempre se mueve en diagonal abajo-izquierda (por Compu2)
- **3: MOpp** - Siempre se mueve en diagonal arriba-derecha (por Compu2)
- **4: MOxx** - Se mueve horizontalmente hacia la comida (por Compu2)
- **5: MOyy** - Se mueve verticalmente hacia la comida (por Compu2)
- **6: Tacticas1** - Estrategia: matar→comer→reproducir (por Compu2)
- **7: Tacticas2** - Estrategia: comer→matar→reproducir (por Compu2)

## Ejemplos de competencia

```bash
# Aleatorio vs buscador de nutrientes
python comvida.py --distribucion 1 --colonias 0 1

# Batalla estratégica
python comvida.py --distribucion 5 --colonias 6 7

```

### Modo sin gráficos (headless)

Para ejecutar sin abrir ventanas (útil en servidores/CI):

```bash
python comvida.py --sin-grafico --distribucion 2 --colonias 1 2
```

## Estructura del proyecto

```
alifec/
├── vida/                   # Clases principales de la simulación
│   ├── definiciones.py    # Constantes y definiciones
│   ├── agar.py            # Entorno (plato de Petri)
│   ├── microorganismo.py  # Clase base abstracta para microorganismos
│   ├── colonia.py         # Gestión de colonias
│   ├── petri.py           # Motor principal de la simulación
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
2. Heredar de la clase `Microorganismo`
3. Implementar los métodos requeridos:
    - `nombre()`: Devuelve el nombre del microorganismo
    - `autor()`: Devuelve el nombre del autor
    - `decidir_movimiento(mov)`: Define la estrategia de movimiento (obligatorio)
    - `quiere_mitosis()`: Define la estrategia de reproducción (obligatorio)

Ejemplo:
```python
from vida.microorganismo import Microorganismo
from vida.agar import Movimiento

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
- **Rankings globales**: Usar `--actualizar-global filename.txt` para crear/actualizar el ranking global

## Enlaces
- Repositorio GitHub: https://github.com/dmilone/alifec
- Proyecto original: https://sourceforge.net/projects/alifecontest/
