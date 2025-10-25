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

from vida.definiciones import *
from vida.petri import Petri
from vida.microorganismo import Microorganismo
from vida.ranking import RankingSystem

def obtener_clases_mo() -> Dict[int, Type[Microorganismo]]:
    """Descubre dinámicamente las clases de microorganismos en la carpeta mos"""
    clases_mo = {}
    mos_dir = os.path.join(os.path.dirname(__file__), 'mos')
    
    # Archivos .py del directorio
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
                    clases_mo[index] = obj
                    index += 1
                    break  # Solo se considera la 1ra clase Microorganismo de cada módulo
                    
        except Exception as e:
            print(f"Error: no se pudo cargar el microorganismo desde {module_name}: {e}")
            continue
    
    return clases_mo

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
  python comvida.py --listar-mos
  python comvida.py --distribucion 4 --colonias 3 4
  python comvida.py --distribucion 1 --colonias 2 1
  python comvida.py --actualizar-global global_ranking.txt
    '''
    )
    
    parser.add_argument('--distribucion', '-d', dest='distribucion', type=int, default=MAX_DNUTRI,
                       help=f'Distribución de nutrientes, entre 1 y {MAX_DNUTRI}')
    parser.add_argument('--colonias', '-c', dest='colonias', type=int, nargs='+',
                       help='Lista de microorganismos (números separados por espacios)')
    parser.add_argument('--listar-mos', dest='listar_mos', action='store_true',
                       help='Listar todos los microorganismos disponibles y salir')
    parser.add_argument('--actualizar-global', dest='actualizar_global', type=str, metavar='ARCHIVO_RANKING_GLOBAL',
                       help='Actualizar el archivo de ranking global con todos los resultados disponibles')
    parser.add_argument('--sin-grafico', '--sin-graficos', dest='sin_grafico', action='store_true',
                       help='Ejecutar la simulación en modo sin gráficos (headless)')
    
    args = parser.parse_args()
    
    # Descubrir las clases de microorganismos disponibles
    clases_mo = obtener_clases_mo()
    max_cols = len(clases_mo) - 1  # 0-indexed
    
    # Listar microorganismos y salir
    if args.listar_mos:
        print("Microorganismos disponibles:")
        for i, cls in clases_mo.items():
            instance = cls()
            print(f"  {i}: {instance.nombre()} por {instance.autor()}")
        return 0
    
    # Actualizar ranking global y salir
    if args.actualizar_global:
        ranking_system = RankingSystem()
        return ranking_system.update_global_ranking(args.actualizar_global)

    # Validar que se definan las colonias a competir
    if not args.colonias:
        print("\nError: --colonias es necesario para iniciar la competencia")
        print(f"Uso: {sys.argv[0]} --distribucion <1-{MAX_DNUTRI}> --colonias <organismo1_ID> <organismo2_ID>")
        print(f"Microorganismos disponibles: 0-{max_cols}")
        print("Puede usar --listar-mos para ver todos los microorganismos disponibles.")
        return 1
    
    # Verificar parámetros de entrada para la competencia simple
    error = False
    if args.distribucion > MAX_DNUTRI or len(args.colonias) != 2:
        error = True
    else:
        for col in args.colonias:
            if col > max_cols:
                error = True
                break
    if error:
        print("\nError: hay parámetros inválidos")
        print(f"Uso: {sys.argv[0]} --distribucion <1-{MAX_DNUTRI}> --colonias <organismo1_ID> <organismo2_ID>")
        print(f"Se requieren exactamente 2 organismos. Microorganismos disponibles: 0-{max_cols}")
        print("Use --listar-mos para ver todos los microorganismos disponibles.")
        return 1
    
    # Ejecutar la simulación
    petri = None
    graficadora = None
    try:
        # Crear cápsula de Petri con colonias seleccionadas
        petri = Petri(R, args.distribucion, args.colonias, clases_mo)

        # Definir el backend de matplotlib para el modo sin gráficos antes de importar Graficadora
        if args.sin_grafico:
            import matplotlib
            matplotlib.use('Agg')

        # Crear y ejecutar visualización (modo headless)
        from vida.graficacion import Graficadora
        graficadora = Graficadora(headless=args.sin_grafico)
        graficadora.crear_ventanas(petri)

        # Obtener datos de resultados de la competencia
        contest_data = graficadora.resultado_competencia()

        if contest_data.get('completada', False):
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
        if 'graficadora' in locals() and graficadora:
            try:
                graficadora.limpiar()
            except:
                pass
        if petri:
            try:
                del petri
            except:
                pass

if __name__ == "__main__":
    sys.exit(main())