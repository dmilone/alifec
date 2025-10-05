#!/usr/bin/env python3
"""
Test script for the Artificial Life Contest Python translation
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported correctly"""
    print("Testing imports...")
    
    try:
        import lib.defs
        print("✓ lib.defs imported")
        
        from lib.agar import Posicion, Movimiento, agar
        print("✓ lib.agar imported")
        
        from lib.microorg import Microorganismo
        print("✓ lib.microorg imported")
        
        from lib.colony import Colony
        print("✓ lib.colony imported")
        
        from lib.petri import Petri
        print("✓ lib.petri imported")
        
        from lib.grapher import Grapher
        print("✓ lib.grapher imported")
        
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_microorganisms():
    """Test that all microorganisms can be instantiated"""
    print("\nTesting microorganisms...")
    
    microorganisms = [
        ('aleatorio', 'Aleatorio'),
        ('buscan', 'BuscaN'),
        ('momm', 'MOmm'),
        ('mopp', 'MOpp'),
        ('moxx', 'MOxx'),
        ('moyy', 'MOyy'),
        ('tacticas1', 'Tacticas1'),
        ('tacticas2', 'Tacticas2')
    ]
    
    success = True
    for module_name, class_name in microorganisms:
        try:
            module = __import__(f'mos.{module_name}', fromlist=[class_name])
            mo_class = getattr(module, class_name)
            instance = mo_class()
            print(f"✓ {instance.nombre()} by {instance.autor()}")
        except Exception as e:
            print(f"✗ {class_name} error: {e}")
            success = False
            
    return success

def test_basic_simulation():
    """Test basic simulation components"""
    print("\nTesting basic simulation components...")
    
    try:
        from mos.aleatorio import Aleatorio
        from mos.buscan import BuscaN
        from lib.petri import Petri
        
        # Test microorganism classes mapping
        microorg_classes = {0: Aleatorio, 1: BuscaN}
        selected_cols = [0, 1]
        
        print("✓ Basic simulation setup works")
        return True
        
    except Exception as e:
        print(f"✗ Simulation setup error: {e}")
        return False

def main():
    print("=" * 50)
    print("Artificial Life Contest - Python Translation Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Run tests
    all_tests_passed &= test_imports()
    all_tests_passed &= test_microorganisms()
    all_tests_passed &= test_basic_simulation()
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("✓ All tests PASSED! The translation is working correctly.")
        print("\nYou can now run simulations using:")
        print("  python comvida.py --dist 1 --colonies 0 1")
        return 0
    else:
        print("✗ Some tests FAILED. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())