import sys
import os

# Añadir el path del módulo a sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'taximetrocli')))

from taximetro import calculate_fare

def test_calculate_fare():
     assert calculate_fare(10, 20, 0.02, 0.05, 2, 1) == (10*0.02 + 20*0.05 + 2)

def test_calculate_fare_zero_time():
     assert calculate_fare(0, 0, 0.02, 0.05, 2, 1) == 2

def test_calculate_fare_no_suitcases():
    assert calculate_fare(15, 15, 0.02, 0.05, 2, 0) == (15*0.02 + 15*0.05)

def test_calculate_fare_large_values():
    assert calculate_fare(100, 200, 0.03, 0.07, 3, 4) == (100*0.03 + 200*0.07 + 3*4)