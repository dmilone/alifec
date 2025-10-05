#!/usr/bin/env python3
# =====================================================================
# COMVIDA: Competition of microorganism colonies
# Translated from C++ to Python
# =====================================================================

import sys
import signal
import argparse
import os
import importlib
import inspect
from typing import Dict, Type, List

# Import core classes
from lib.defs import *
from lib.petri import Petri
from lib.microorg import Microorganismo
from lib.ranking import RankingSystem
# Grapher will be imported conditionally based on plot mode

def get_microorganism_classes() -> Dict[int, Type[Microorganismo]]:
    """Dynamically discover and return all microorganism classes from mos folder"""
    microorg_classes = {}
    mos_dir = os.path.join(os.path.dirname(__file__), 'mos')
    
    # Get all python files in mos directory
    py_files = [f[:-3] for f in os.listdir(mos_dir) if f.endswith('.py') and f != '__init__.py']
    py_files.sort()  # Ensure consistent ordering
    
    index = 0
    for module_name in py_files:
        try:
            # Import the module
            module = importlib.import_module(f'mos.{module_name}')
            
            # Find classes that inherit from Microorganismo
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (obj != Microorganismo and 
                    issubclass(obj, Microorganismo) and 
                    obj.__module__ == f'mos.{module_name}'):
                    microorg_classes[index] = obj
                    index += 1
                    break  # Only take the first valid class per module
                    
        except Exception as e:
            print(f"Warning: Could not load microorganism from {module_name}: {e}")
            continue
    
    return microorg_classes

def signal_handler(signum, frame):
    """Handle interrupt signals gracefully"""
    print("\nSimulation interrupted by user")
    sys.exit(0)




def main():
    """Main function - entry point of the program"""
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    parser = argparse.ArgumentParser(
        description='Artificial Life Contest - Microorganism Competition',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python comvida.py --list-mos
  python comvida.py --dist 4 --colonies 3 4
  python comvida.py --dist 1 --colonies 2 1
  python comvida.py --update-global global_ranking.txt
        '''
    )
    
    parser.add_argument('--dist', '-d', type=int, default=MAX_DNUTRI,
                       help=f'Nutrients distribution, between 1 and {MAX_DNUTRI}')
    parser.add_argument('--colonies', '-c', type=int, nargs='+',
                       help='List of micro-organisms (space-separated numbers)')
    parser.add_argument('--list-mos', action='store_true',
                       help='List all available microorganisms and exit')
    parser.add_argument('--update-global', type=str, metavar='GLOBAL_RANKING_FILE',
                       help='Update global ranking file with all available results')
    parser.add_argument('--no-plot', action='store_true',
                       help='Run simulation in headless mode without graphical display')
    
    args = parser.parse_args()
    
    # Get available microorganisms
    microorg_classes = get_microorganism_classes()
    max_cols = len(microorg_classes) - 1  # 0-indexed
    
    # Handle list microorganisms mode
    if args.list_mos:
        print("Available microorganisms:")
        for i, cls in microorg_classes.items():
            instance = cls()
            print(f"  {i}: {instance.nombre()} by {instance.autor()}")
        return 0
    
    # Handle global ranking update mode
    if args.update_global:
        ranking_system = RankingSystem()
        return ranking_system.update_global_ranking(args.update_global)
    
    # Validate that colonies argument is provided for match mode
    if not args.colonies:
        print("\nError: --colonies required for single match mode!")
        print(f"Usage: {sys.argv[0]} --dist <1-{MAX_DNUTRI}> --colonies <organism1_ID> <organism2_ID>")
        print(f"Available organisms: 0-{max_cols}")
        print("Use --list-mos to see all available microorganisms.")
        return 1
    
    # Validate parameters for single match mode
    error = False
    if args.dist > MAX_DNUTRI or len(args.colonies) != 2:
        error = True
    else:
        # Verify each colony is within available colonies
        for col in args.colonies:
            if col > max_cols:
                error = True
                break
                
    if error:
        print("\nError: Invalid parameters!")
        print(f"Usage: {sys.argv[0]} --dist <1-{MAX_DNUTRI}> --colonies <organism1_ID> <organism2_ID>")
        print(f"Exactly 2 organisms required. Available organisms: 0-{max_cols}")
        print("Use --list-mos to see all available microorganisms.")
        return 1
        
    petri = None
    grapher = None
    
    try:
        # Create Petri dish with selected colonies
        petri = Petri(R, args.dist, args.colonies, microorg_classes)
        
        # Set matplotlib backend for headless mode before importing Grapher
        if args.no_plot:
            import matplotlib
            matplotlib.use('Agg')
        
        # Create and run visualization (headless mode only with --no-plot)
        from lib.grapher import Grapher
        grapher = Grapher(headless=args.no_plot)
        grapher.create_windows(petri)
        
        # Get contest result data from grapher
        contest_data = grapher.get_contest_result()
        
        # Only save results if contest completed successfully
        if contest_data.get('completed', False):
            # Save contest result and generate daily ranking using RankingSystem
            ranking_system = RankingSystem()
            ranking_system.save_contest_result(contest_data)
            ranking_system.generate_daily_ranking()
        else:
            print("Contest did not complete successfully - results not saved")
        
        return 0
        
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user")
        return 0
    except Exception as e:
        print(f"Error during simulation: {e}")
        return 1
    finally:
        # Clean up resources
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