#!/usr/bin/env python3
# =====================================================================
# COMVIDA: COMpetencia de VIDa Artificial
# Traducción del proyecto desde C++ a Python
# https://github.com/dmilone/alifec
# https://sourceforge.net/projects/alifecontest/
# =====================================================================

import sys
import signal
import argparse
import os
import importlib
import inspect
from typing import Dict, Type, List

from lib.defs import *
from lib.petri import Petri
from lib.microorg import Microorganismo
from lib.ranking import RankingSystem

def get_microorganism_classes() -> Dict[int, Type[Microorganismo]]:
    """Descubre dinámicamente las clases de microorganismos en la carpeta mos"""
    microorg_classes = {}
    mos_dir = os.path.join(os.path.dirname(__file__), 'mos')
    
    # Todos los archivos .py del directorio
    py_files = [f[:-3] for f in os.listdir(mos_dir) if f.endswith('.py') and f != '__init__.py']
    py_files.sort()
    
    # Se importan los módulos y se buscan las clases
    index = 0
    for module_name in py_files:
        try:
            module = importlib.import_module(f'mos.{module_name}')
            
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (obj != Microorganismo and 
                    issubclass(obj, Microorganismo) and 
                    obj.__module__ == f'mos.{module_name}'):
                    microorg_classes[index] = obj
                    index += 1
                    break  # Solo se considera la 1ra clase Microorganismo de cada módulo
                    
        except Exception as e:
            print(f"Error: no se pudo cargar el microorganismo desde {module_name}: {e}")
            continue
    
    return microorg_classes

def signal_handler(signum, frame):
    print("\n La simulación fue interrumpida desde afuera.")
    sys.exit(0)

# =====================================================================
def main():

    # Para interrumpir la simulación
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    parser = argparse.ArgumentParser(
        description='COMpetencia de VIDa Artificial',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Ejemplos:
  python comvida.py --list-mos
  python comvida.py --dist 4 --colonies 3 4
  python comvida.py --dist 1 --colonies 2 1
  python comvida.py --update-global global_ranking.txt
        '''
    )
    
    parser.add_argument('--dist', '-d', type=int, default=MAX_DNUTRI,
                       help=f'Distribución de nutrientes, entre 1 y {MAX_DNUTRI}')
    parser.add_argument('--colonies', '-c', type=int, nargs='+',
                       help='Lista de microorganismos (números separados por espacios)')
    parser.add_argument('--list-mos', action='store_true',
                       help='Listar todos los microorganismos disponibles y salir')
    parser.add_argument('--update-global', type=str, metavar='ARCHIVO_RANKING_GLOBAL',
                       help='Actualizar el archivo de ranking global con todos los resultados disponibles')
    parser.add_argument('--no-plot', action='store_true',
                       help='Ejecutar la simulación en modo sin gráficos (headless)')
    
    args = parser.parse_args()
    
    # Descubrir las clases de microorganismos disponibles
    microorg_classes = get_microorganism_classes()
    max_cols = len(microorg_classes) - 1  # 0-indexed
    
    # Listar microorganismos y salir
    if args.list_mos:
        print("Microorganismos disponibles:")
        for i, cls in microorg_classes.items():
            instance = cls()
            print(f"  {i}: {instance.nombre()} por {instance.autor()}")
        return 0
    
    # Actualizar ranking global y salir
    if args.update_global:
        ranking_system = RankingSystem()
        return ranking_system.update_global_ranking(args.update_global)

    # Validar que se definan las colonias a competir
    if not args.colonies:
        print("\nError: --colonies es necesario para iniciar la competencia")
        print(f"Uso: {sys.argv[0]} --dist <1-{MAX_DNUTRI}> --colonies <organismo1_ID> <organismo2_ID>")
        print(f"Microorganismos disponibles: 0-{max_cols}")
        print("Puede usar --list-mos para ver todos los microorganismos disponibles.")
        return 1
    
    # Verificar parámetros de entrada para la competencia simple
    error = False
    if args.dist > MAX_DNUTRI or len(args.colonies) != 2:
        error = True
    else:
        for col in args.colonies:
            if col > max_cols:
                error = True
                break
    if error:
        print("\nError: hay parámetros inválidos")
        print(f"Uso: {sys.argv[0]} --dist <1-{MAX_DNUTRI}> --colonies <organismo1_ID> <organismo2_ID>")
        print(f"Se requieren exactamente 2 organismos. Microorganismos disponibles: 0-{max_cols}")
        print("Use --list-mos para ver todos los microorganismos disponibles.")
        return 1
    
    # Ejecutar la simulación
    petri = None
    grapher = None
    try:
        # Crear cápsula de Petri con colonias seleccionadas
        petri = Petri(R, args.dist, args.colonies, microorg_classes)

        # Definir el backend de matplotlib para el modo sin gráficos antes de importar Grapher
        if args.no_plot:
            import matplotlib
            matplotlib.use('Agg')

        # Crear y ejecutar visualización (modo headless --no-plot)
        from lib.grapher import Grapher
        grapher = Grapher(headless=args.no_plot)
        grapher.create_windows(petri)

        # Obtener datos de resultados de la competencia
        contest_data = grapher.resultado_competencia()

        # Solo guardar resultados si la competencia se completó bien
        if contest_data.get('completed', False):
            # Guardar resultado de la Competencia y generar ranking
            ranking_system = RankingSystem()
            ranking_system.guardar_resultado_competencia(contest_data)
            ranking_system.generar_ranking_diario()
        else:
            print("La competencia no se completó bien - resultados no guardados")

        return 0
        
    except KeyboardInterrupt:
        print("\nSimulación interrumpida desde afuera")
        return 0
    except Exception as e:
        print(f"Error durante la simulación: {e}")
        return 1
    finally:
        # Limpieza...
        if grapher:
            try:
                grapher.cleanup()
            except:
                pass
        if petri:
            try:
                del petri
            except:
                pass

if __name__ == "__main__":
    sys.exit(main())