#!/usr/bin/env python3
"""
Tests pour le module solve.py
"""

import unittest
from solve import solve_hanoi, calculate_min_moves, parse_input


class TestHanoiSolver(unittest.TestCase):
    """Tests pour le solveur de la Tour de Hanoï"""
    
    def test_calculate_min_moves(self):
        """Test du calcul du nombre minimum de mouvements"""
        self.assertEqual(calculate_min_moves(1), 1)
        self.assertEqual(calculate_min_moves(2), 3)
        self.assertEqual(calculate_min_moves(3), 7)
        self.assertEqual(calculate_min_moves(4), 15)
        self.assertEqual(calculate_min_moves(5), 31)
    
    def test_parse_input_valid(self):
        """Test du parsing d'entrées valides"""
        self.assertEqual(parse_input("3,3"), (3, 3))
        self.assertEqual(parse_input("8,3"), (8, 3))
        self.assertEqual(parse_input("172,5"), (172, 5))
        self.assertEqual(parse_input(" 4 , 4 "), (4, 4))
    
    def test_parse_input_invalid(self):
        """Test du parsing d'entrées invalides"""
        with self.assertRaises(ValueError):
            parse_input("3")  # Format incorrect
        
        with self.assertRaises(ValueError):
            parse_input("3,3,3")  # Trop de paramètres
        
        with self.assertRaises(ValueError):
            parse_input("0,3")  # Nombre de disques invalide
        
        with self.assertRaises(ValueError):
            parse_input("3,2")  # Pas assez de bâtonnets
        
        with self.assertRaises(ValueError):
            parse_input("abc,3")  # Caractères non numériques
    
    def test_solve_hanoi_small_cases(self):
        """Test de la résolution pour de petits cas"""
        # 1 disque
        moves = solve_hanoi(1, 3, verbose=False)
        self.assertEqual(len(moves), 1)
        self.assertEqual(moves[0], "1->3")
        
        # 2 disques
        moves = solve_hanoi(2, 3, verbose=False)
        self.assertEqual(len(moves), 3)
        expected = ["1->2", "1->3", "2->3"]
        self.assertEqual(moves, expected)
        
        # 3 disques
        moves = solve_hanoi(3, 3, verbose=False)
        self.assertEqual(len(moves), 7)
    
    def test_solve_hanoi_move_count(self):
        """Test que le nombre de mouvements correspond à la formule 2^n - 1"""
        for n in range(1, 8):  # Test jusqu'à 7 disques
            moves = solve_hanoi(n, 3, verbose=False)
            expected_count = calculate_min_moves(n)
            self.assertEqual(len(moves), expected_count, 
                           f"Pour {n} disques, attendu {expected_count} mouvements, obtenu {len(moves)}")
    
    def test_solve_hanoi_empty_case(self):
        """Test du cas avec 0 disque"""
        moves = solve_hanoi(0, 3, verbose=False)
        self.assertEqual(moves, [])
    
    def test_solve_hanoi_move_format(self):
        """Test que les mouvements sont au bon format"""
        moves = solve_hanoi(3, 3, verbose=False)
        for move in moves:
            self.assertRegex(move, r'^\d+->\d+$', f"Format de mouvement invalide: {move}")
            source, dest = move.split('->')
            self.assertIn(int(source), [1, 2, 3], f"Source invalide: {source}")
            self.assertIn(int(dest), [1, 2, 3], f"Destination invalide: {dest}")
            self.assertNotEqual(source, dest, f"Source et destination identiques: {move}")


def run_performance_test():
    """Test de performance pour différentes tailles"""
    import time
    
    print("\nTest de performance:")
    print("Disques | Mouvements | Temps (s)")
    print("-" * 35)
    
    for n in range(1, 16):  # Test jusqu'à 15 disques
        start_time = time.time()
        moves = solve_hanoi(n, 3, verbose=False)
        end_time = time.time()
        
        print(f"{n:7d} | {len(moves):10d} | {end_time - start_time:.6f}")
        
        # Arrêter si ça prend trop de temps
        if end_time - start_time > 1.0:
            print("Arrêt du test de performance (temps > 1s)")
            break


if __name__ == "__main__":
    # Exécuter les tests unitaires
    print("Exécution des tests unitaires...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Exécuter le test de performance
    run_performance_test()

