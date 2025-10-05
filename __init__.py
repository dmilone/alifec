# =====================================================================
# Artificial Life Contest - Python Version
# Competition of microorganism colonies
# =====================================================================

"""
Artificial Life Contest - Python Translation

This project is aimed at the development of a framework for artificial life contests.
The framework provides the main rules of the game, a visualization interface, and 
examples of elementary microorganisms.

The central idea is the development of the environment, while users develop their
own microorganisms to compete for survival in a common environment.

Translated from C++ to Python by the community.

Original authors: Diego Milone, Maximiliano Boscovich, Gaston Ramos
Python translation: Community effort

Usage:
    python comvida.py --dist 4 --colonies 0 1
    
Available microorganisms:
    0: Aleatorio (Random movement)
    1: BuscaN (Nutrient seeker)  
    2: MOmm (Move diagonal down-left)
    3: MOpp (Move diagonal up-right)
    4: MOxx (Move horizontally towards food)
    5: MOyy (Move vertically towards food) 
    6: Tacticas1 (Strategic: kill->eat->reproduce)
    7: Tacticas2 (Strategic: eat->kill->reproduce)
"""

__version__ = "0.41-py"
__author__ = "Diego Milone, Maximiliano Boscovich, Gaston Ramos (Python translation)"

from . import lib
from . import mos